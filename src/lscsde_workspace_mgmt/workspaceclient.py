from .workspacebindingclient import AnalyticsWorkspaceBindingClient
from logging import Logger
from kubernetes_asyncio import client
from kubernetes_asyncio.client.exceptions import ApiException
from pydantic import TypeAdapter
from .exceptions import (
    InvalidParameterException,
)
from .namespacedclient import KubernetesNamespacedCustomClient
from .eventclient import EventClient


from .models import (
    AnalyticsWorkspaceStatus,
    AnalyticsWorkspaceSpec,
    AnalyticsWorkspace,
)


class AnalyticsWorkspaceClient(KubernetesNamespacedCustomClient):
    """
    Client for interacting with AnalyticsWorkspace objects in Kubernetes.

    The AnalyticsWorkspaceClient provides methods to create, read, update, and delete
    AnalyticsWorkspace resources in a Kubernetes cluster. It handles serialization,
    deserialization, and validation of these objects using Pydantic models.

    It extends the KubernetesNamespacedCustomClient to provide specialized functionality
    for AnalyticsWorkspace resources, including managing the workspace lifecycle and
    recording relevant events.
    """

    # TypeAdapter for validating and serializing/deserializing workspace objects
    adaptor = TypeAdapter(AnalyticsWorkspace)

    def __init__(
        self, k8s_api: client.CustomObjectsApi, log: Logger, event_client: EventClient
    ):
        """
        Initialize the AnalyticsWorkspaceClient.

        Args:
            k8s_api (client.CustomObjectsApi): Kubernetes API client for interacting with custom resources
            log (Logger): Logger for recording operational events and errors
            event_client (EventClient): Client for emitting Kubernetes events related to AnalyticsWorkspaces
        """
        # Initialize with the specific CRD details for AnalyticsWorkspace
        super().__init__(
            k8s_api=k8s_api,
            log=log,
            group="xlscsde.nhs.uk",
            version="v1",
            plural="analyticsworkspaces",
            kind="AnalyticsWorkspace",
        )
        self.event_client = event_client

    async def get(self, namespace, name):
        """
        Gets a specific AnalyticsWorkspace resource.

        Args:
            namespace (str): Kubernetes namespace containing the resource
            name (str): Name of the AnalyticsWorkspace resource

        Returns:
            AnalyticsWorkspace: The validated workspace object

        Raises:
            ApiException: If the resource does not exist or cannot be accessed
        """
        result = await super().get(namespace, name)
        return self.adaptor.validate_python(result)

    async def list(self, namespace, **kwargs):
        """
        Lists AnalyticsWorkspace resources in the namespace supplied.

        Args:
            namespace (str): Kubernetes namespace to list resources from
            **kwargs: Additional parameters to pass to the Kubernetes API
                      (e.g., label_selector, field_selector)

        Returns:
            list[AnalyticsWorkspace]: List of validated workspace objects
        """
        result = await super().list(namespace, **kwargs)

        return [self.adaptor.validate_python(item) for item in result["items"]]

    async def list_by_username(
        self,
        binding_client: AnalyticsWorkspaceBindingClient,
        namespace: str,
        username: str,
    ):
        """
        Lists AnalyticsWorkspace resources in the namespace supplied that match the username.

        Retrieves all workspaces that a specific user has access to based on workspace bindings.
        The function also handles expiration dates, ensuring that the earliest expiration date
        from bindings is applied to the workspace.

        Args:
            binding_client (AnalyticsWorkspaceBindingClient): Client for workspace binding operations
            namespace (str): Kubernetes namespace to search in
            username (str): Username to filter workspaces by

        Returns:
            list[AnalyticsWorkspace]: List of workspaces the user has access to
        """
        # Get all bindings for this user
        bindings = await binding_client.list_by_username(
            namespace=namespace, username=username
        )
        # Create a lookup dictionary of binding name to binding spec
        bound_workspaces = {x.metadata.name: x.spec for x in bindings}
        workspaces = []
        for bound_workspace in bound_workspaces.keys():
            try:
                # Extract the workspace name from the binding
                workspace_name: str = bound_workspaces[bound_workspace].workspace

                # Check if we've already processed this workspace
                if workspace_name not in [x.metadata.name for x in workspaces]:
                    # Retrieve the workspace details
                    workspace = await self.get(namespace=namespace, name=workspace_name)

                    if workspace is not None:
                        # Apply binding expiration if it's earlier than workspace expiration
                        # This enforces the earliest expiry date between binding and workspace
                        if (
                            bound_workspaces[bound_workspace].expires
                            < workspace.spec.validity.expires
                        ):
                            workspace.spec.validity.expires = bound_workspaces[
                                bound_workspace
                            ].expires

                        workspaces.append(workspace)
                else:
                    # If this workspace was already added, check if this binding has an earlier expiry
                    for workspace in workspaces:
                        if workspace.metadata.name == workspace_name:
                            if (
                                bound_workspaces[bound_workspace].expires
                                < workspace.spec.validity.expires
                            ):
                                workspace.spec.validity.expires = bound_workspaces[
                                    bound_workspace
                                ].expires

            except ApiException as e:
                # Handle case where a referenced workspace doesn't exist
                if e.status == 404:
                    self.log.error(
                        f"Workspace {bound_workspace} referenced by user {username} on {namespace} does not exist"
                    )
                else:
                    raise e

        return workspaces

    async def create(self, body: AnalyticsWorkspace):
        """
        Creates an AnalyticsWorkspace resource in the namespace supplied.

        Args:
            body (AnalyticsWorkspace): The workspace object to create

        Returns:
            AnalyticsWorkspace: The created workspace object as returned by the API

        Raises:
            ApiException: If the creation fails
        """
        # Convert the Pydantic model to a Kubernetes-compatible dict
        result = await super().create(
            namespace=body.metadata.namespace,
            body=self.adaptor.dump_python(body, by_alias=True),
        )
        # Validate the response and emit creation event
        created_workspace: AnalyticsWorkspace = self.adaptor.validate_python(result)
        await self.event_client.WorkspaceCreated(created_workspace)
        return created_workspace

    async def patch(
        self,
        namespace: str = None,
        name: str = None,
        patch_body: dict = None,
        body: AnalyticsWorkspace = None,
    ):
        """
        Patches an AnalyticsWorkspace resource in the namespace supplied.

        This method supports two approaches:
        1. Providing namespace, name, and patch_body for a direct JSON patch
        2. Providing a body object to generate a patch from the object

        Args:
            namespace (str, optional): Kubernetes namespace. Required if body not provided.
            name (str, optional): Resource name. Required if body not provided.
            patch_body (dict, optional): JSON Patch document. Required if body not provided.
            body (AnalyticsWorkspace, optional): The workspace object to generate a patch from.

        Returns:
            AnalyticsWorkspace: The updated workspace object

        Raises:
            InvalidParameterException: If neither (namespace, name, patch_body) nor body is provided
            ApiException: If the patch operation fails
        """
        # If no patch body is provided, create one from the workspace object
        if not patch_body:
            if not body:
                raise InvalidParameterException(
                    "Either namespace, name and patch_body or body must be provided"
                )

            # Create adapters for spec and status to serialize them properly
            spec_adapter = TypeAdapter(AnalyticsWorkspaceSpec)
            status_adapter = TypeAdapter(AnalyticsWorkspaceStatus)

            # Create a JSON patch that replaces both spec and status
            patch_body = [
                {
                    "op": "replace",
                    "path": "/spec",
                    "value": spec_adapter.dump_python(body.spec, by_alias=True),
                },
                {
                    "op": "replace",
                    "path": "/status",
                    "value": status_adapter.dump_python(body.status, by_alias=True),
                },
            ]

        # Extract namespace and name from body if not explicitly provided
        if not namespace:
            if not body:
                raise InvalidParameterException(
                    "Either namespace, name and patch_body or body must be provided"
                )
            namespace = body.metadata.namespace

        if not name:
            if not body:
                raise InvalidParameterException(
                    "Either namespace, name and patch_body or body must be provided"
                )
            name = body.metadata.name

        # Apply the patch and validate response
        result = await super().patch(namespace=namespace, name=name, body=patch_body)

        updated_workspace: AnalyticsWorkspace = self.adaptor.validate_python(result)
        # Record that the workspace was updated
        await self.event_client.WorkspaceUpdated(updated_workspace)
        return updated_workspace

    async def patch_status(
        self, namespace: str, name: str, status: AnalyticsWorkspaceStatus
    ):
        """
        Patches the status of an AnalyticsWorkspace resource in the namespace supplied.

        Updates only the status subresource of the workspace, which is more efficient than
        patching the entire object when only the status needs to change.

        Args:
            namespace (str): Kubernetes namespace containing the resource
            name (str): Name of the resource
            status (AnalyticsWorkspaceStatus): New status object to apply

        Returns:
            AnalyticsWorkspace: The workspace object with updated status

        Raises:
            ApiException: If the status patch operation fails
        """
        status_adapter = TypeAdapter(AnalyticsWorkspaceStatus)
        body = [
            {
                "op": "replace",
                "path": "/status",
                "value": status_adapter.dump_python(status, by_alias=True),
            }
        ]
        result = await super().patch_status(namespace=namespace, name=name, body=body)
        return self.adaptor.validate_python(result)

    async def replace(self, body: AnalyticsWorkspace):
        """
        Replaces an AnalyticsWorkspace resource with the one supplied.

        Performs a full replacement of the workspace, not just a patch operation.

        Args:
            body (AnalyticsWorkspace): The complete new definition of the workspace

        Returns:
            AnalyticsWorkspace: The replaced workspace object as returned by the API

        Raises:
            ApiException: If the replace operation fails
        """
        result = await super().replace(
            namespace=body.metadata.namespace,
            name=body.metadata.name,
            body=self.adaptor.dump_python(body, by_alias=True),
        )
        return self.adaptor.validate_python(result)

    async def delete(
        self, body: AnalyticsWorkspace = None, namespace: str = None, name: str = None
    ):
        """
        Deletes an AnalyticsWorkspace resource in the namespace supplied.

        Updates the status to "Deleting" before performing the actual deletion to provide
        visibility into the deletion process.

        Args:
            body (AnalyticsWorkspace, optional): The workspace object to delete
            namespace (str, optional): Kubernetes namespace. Required if body not provided.
            name (str, optional): Resource name. Required if body not provided.

        Returns:
            dict: The response from the Kubernetes API

        Raises:
            ApiException: If the deletion fails
        """
        # Extract namespace and name from body if not explicitly provided
        if body:
            if not namespace:
                namespace = body.metadata.namespace
            if not name:
                name = body.metadata.name

        # Create a patch to update status to "Deleting" before actual deletion
        # This provides visibility into the deletion process
        patch_body = [
            {"op": "replace", "path": "/status/statusText", "value": "Deleting"}
        ]

        # Check if status field exists and create it if not
        current = await super().get(namespace, name)
        if not current.get("status"):
            patch_body = [
                {"op": "add", "path": "/status", "value": {"statusText": "Deleting"}}
            ]

        # Apply the status update
        await super().patch_status(
            namespace=body.metadata.namespace, name=body.metadata.name, body=patch_body
        )

        # Record deletion event before the resource is removed
        if body:
            await self.event_client.WorkspaceDeleted(body)

        # Perform the actual deletion in Kubernetes
        return await super().delete(
            namespace=body.metadata.namespace, name=body.metadata.name
        )
