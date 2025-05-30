from .namespacedclient import KubernetesNamespacedCustomClient
from .eventclient import EventClient

from logging import Logger
from kubernetes_asyncio import client
from pydantic import TypeAdapter
from .exceptions import InvalidParameterException, InvalidLabelFormatException

from .models import (
    AnalyticsWorkspaceBindingStatus,
    AnalyticsWorkspaceBindingSpec,
    KubernetesHelper,
    AnalyticsWorkspaceBinding,
)


class AnalyticsWorkspaceBindingClient(KubernetesNamespacedCustomClient):
    """
    This class allows developers to interact with AnalyticsWorkspaceBinding objects on kubernetes

    The AnalyticsWorkspaceBindingClient provides methods to create, read, update, and delete
    AnalyticsWorkspaceBinding resources in a Kubernetes cluster. It handles serialization,
    deserialization, and validation of these objects using Pydantic models.

    It extends the KubernetesNamespacedCustomClient to provide specialized functionality
    for AnalyticsWorkspaceBinding resources.
    """

    # TypeAdapter for validating and serializing/deserializing workspace binding objects
    adaptor = TypeAdapter(AnalyticsWorkspaceBinding)

    def __init__(
        self, k8s_api: client.CustomObjectsApi, log: Logger, event_client: EventClient
    ):
        """
        Initialize the AnalyticsWorkspaceBindingClient

        Args:
            k8s_api (client.CustomObjectsApi): Kubernetes API client for interacting with custom resources
            log (Logger): Logger for recording operational events and errors
            event_client (EventClient): Client for emitting Kubernetes events related to AnalyticsWorkspaceBindings
        """
        # Initialize with the specific CRD details for AnalyticsWorkspaceBinding
        super().__init__(
            k8s_api=k8s_api,
            log=log,
            group="xlscsde.nhs.uk",
            version="v1",
            plural="analyticsworkspacebindings",
            kind="AnalyticsWorkspaceBinding",
        )
        self.event_client = event_client

    async def get(self, namespace, name):
        """
        Gets an individual AnalyticsWorkspaceBinding

        Args:
            namespace (str): Kubernetes namespace containing the resource
            name (str): Name of the AnalyticsWorkspaceBinding resource

        Returns:
            AnalyticsWorkspaceBinding: The validated binding object

        Raises:
            ApiException: If the resource does not exist or cannot be accessed
        """
        # Retrieve raw object from Kubernetes and validate its structure
        result = await super().get(namespace, name)
        return self.adaptor.validate_python(result)

    async def list(self, namespace, **kwargs):
        """
        Lists the AnalyticsWorkspaceBindings in a specified namespace

        Args:
            namespace (str): Kubernetes namespace to list resources from
            **kwargs: Additional parameters to pass to the Kubernetes API
                      (e.g., label_selector, field_selector)

        Returns:
            list[AnalyticsWorkspaceBinding]: List of validated binding objects
        """
        # Get list of raw objects and validate each one
        result = await super().list(namespace, **kwargs)
        return [self.adaptor.validate_python(item) for item in result["items"]]

    async def list_by_username(self, namespace, username):
        """
        Lists the AnalyticsWorkspaceBindings in a specified namespace which belong to a specific user

        If a binding does not have the relevant labels defined, the service will assign the label automatically
        based upon the username. This makes the query more performant when querying etcd.

        Args:
            namespace (str): Kubernetes namespace to list resources from
            username (str): The username to filter bindings by

        Returns:
            list[AnalyticsWorkspaceBinding]: List of validated binding objects associated with the username
        """
        # Convert username to a valid Kubernetes label format
        helper = KubernetesHelper()
        formatted_username = helper.format_as_label(username)

        # Find bindings without the username label and add the label for better future queries
        no_label = await self.list(
            namespace=namespace, label_selector="!xlscsde.nhs.uk/username"
        )
        for item in no_label:
            if item.spec.username:
                try:
                    # Handle both cases: when labels don't exist yet and when they do
                    if not item.metadata.labels:
                        # Create new labels dictionary if none exists
                        patch_body = [
                            {
                                "op": "add",
                                "path": "/metadata/labels",
                                "value": {
                                    "xlscsde.nhs.uk/username": item.spec.username_as_label()
                                },
                            }
                        ]
                    else:
                        # Add to existing labels - note the JSON patch escaping of '/' with '~1'
                        patch_body = [
                            {
                                "op": "add",
                                "path": "/metadata/labels/xlscsde.nhs.uk~1username",
                                "value": item.spec.username_as_label(),
                            }
                        ]

                    # Apply the patch to update the resource with the label
                    patch_response = await self.patch(  # noqa: F841
                        namespace=item.metadata.namespace,
                        name=item.metadata.name,
                        patch_body=patch_body,
                    )
                except InvalidLabelFormatException as ex:
                    # Log but don't fail if we can't add a label - still allow the query to proceed
                    self.log.error(
                        f"Could not validate {item.metadata.name} due to a label format exception: {ex}"
                    )

        # Now get bindings with the username label using an efficient indexed query
        return await self.list(
            namespace=namespace,
            label_selector=f"xlscsde.nhs.uk/username={formatted_username}",
        )

    async def create(self, body: AnalyticsWorkspaceBinding, append_label: bool = True):
        """
        Creates an AnalyticsWorkspaceBinding resource

        Args:
            body (AnalyticsWorkspaceBinding): The binding object to create
            append_label (bool, optional): Whether to automatically add the username label. Defaults to True.

        Returns:
            AnalyticsWorkspaceBinding: The created binding object as returned by the API

        Raises:
            ApiException: If the creation fails
        """
        # Serialize the object to a Kubernetes-compatible format
        contents = self.adaptor.dump_python(body, by_alias=True)

        # Add username label for efficient queries if requested
        if append_label:
            contents["metadata"]["labels"]["xlscsde.nhs.uk/username"] = (
                body.spec.username_as_label()
            )

        # Create the resource in Kubernetes
        result = await super().create(namespace=body.metadata.namespace, body=contents)

        # Validate and record the creation event
        created_binding: AnalyticsWorkspaceBinding = self.adaptor.validate_python(
            result
        )
        await self.event_client.WorkspaceBindingUpdated(created_binding)
        return created_binding

    async def patch(
        self,
        namespace: str = None,
        name: str = None,
        patch_body: dict = None,
        body: AnalyticsWorkspaceBinding = None,
    ):
        """
        Patches an AnalyticsWorkspaceBinding resource

        This method supports two approaches:
        1. Providing namespace, name, and patch_body for a direct JSON patch
        2. Providing a body object to generate a patch from the object

        Args:
            namespace (str, optional): Kubernetes namespace. Required if body not provided.
            name (str, optional): Resource name. Required if body not provided.
            patch_body (dict, optional): JSON Patch document. Required if body not provided.
            body (AnalyticsWorkspaceBinding, optional): The binding object to generate a patch from.

        Returns:
            AnalyticsWorkspaceBinding: The updated binding object

        Raises:
            InvalidParameterException: If neither (namespace, name, patch_body) nor body is provided
            ApiException: If the patch operation fails
        """
        # Handle the case where a binding object is provided instead of a patch
        if not patch_body:
            if not body:
                raise InvalidParameterException(
                    "Either namespace, name and patch_body or body must be provided"
                )

            # Create a JSON patch that replaces both spec and status
            spec_adapter = TypeAdapter(AnalyticsWorkspaceBindingSpec)
            status_adapter = TypeAdapter(AnalyticsWorkspaceBindingStatus)
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

        # Apply the patch to the Kubernetes resource
        result = await super().patch(namespace=namespace, name=name, body=patch_body)

        # Validate and record the update event
        updated_binding: AnalyticsWorkspaceBinding = self.adaptor.validate_python(
            result
        )
        await self.event_client.WorkspaceBindingUpdated(updated_binding)
        return updated_binding

    async def patch_status(
        self, namespace: str, name: str, status: AnalyticsWorkspaceBindingStatus
    ):
        """
        Patches an AnalyticsWorkspaceBinding resource's status segment

        Args:
            namespace (str): Kubernetes namespace containing the resource
            name (str): Name of the resource
            status (AnalyticsWorkspaceBindingStatus): New status object to apply

        Returns:
            AnalyticsWorkspaceBinding: The updated binding object

        Raises:
            ApiException: If the status patch operation fails
        """
        # Create a JSON patch targeting only the status subresource
        status_adapter = TypeAdapter(AnalyticsWorkspaceBindingStatus)
        body = [
            {
                "op": "replace",
                "path": "/status",
                "value": status_adapter.dump_python(status, by_alias=True),
            }
        ]
        # Use the specialized status patch endpoint provided by Kubernetes
        result = await super().patch_status(namespace=namespace, name=name, body=body)
        return self.adaptor.validate_python(result)

    async def replace(self, body: AnalyticsWorkspaceBinding, append_label: bool = True):
        """
        Replaces an AnalyticsWorkspaceBinding resource with the one provided

        Args:
            body (AnalyticsWorkspaceBinding): The new binding object to replace the existing one
            append_label (bool, optional): Whether to automatically add the username label. Defaults to True.

        Returns:
            AnalyticsWorkspaceBinding: The replaced binding object as returned by the API

        Raises:
            ApiException: If the replace operation fails
        """
        # Serialize the object to a Kubernetes-compatible format
        contents = self.adaptor.dump_python(body, by_alias=True)

        # Add username label for efficient queries if requested
        if append_label:
            contents["metadata"]["labels"]["xlscsde.nhs.uk/username"] = (
                body.spec.username_as_label()
            )

        # Perform a full replacement of the resource (not just a patch)
        result = await super().replace(
            namespace=body.metadata.namespace, name=body.metadata.name, body=contents
        )

        # Validate and record the update event
        updated_binding: AnalyticsWorkspaceBinding = self.adaptor.validate_python(
            result
        )
        await self.event_client.WorkspaceBindingUpdated(updated_binding)
        return updated_binding

    async def delete(
        self,
        body: AnalyticsWorkspaceBinding = None,
        namespace: str = None,
        name: str = None,
    ):
        """
        Deletes an AnalyticsWorkspaceBinding resource

        Args:
            body (AnalyticsWorkspaceBinding, optional): The binding object to delete
            namespace (str, optional): Kubernetes namespace. Required if body not provided.
            name (str, optional): Resource name. Required if body not provided.

        Returns:
            dict: The response from the Kubernetes API

        Raises:
            ApiException: If the deletion fails

        Note:
            This method updates the status to "Deleting" before performing the actual deletion
            and emits a WorkspaceBindingDeleted event if a body was provided.
        """
        # Extract namespace and name from body if not explicitly provided
        if body:
            if not namespace:
                namespace = body.metadata.namespace
            if not name:
                name = body.metadata.name

        # Update status to "Deleting" before actual deletion to inform users
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
            await self.event_client.WorkspaceBindingDeleted(body)

        # Perform the actual deletion in Kubernetes
        return await super().delete(
            namespace=body.metadata.namespace, name=body.metadata.name
        )
