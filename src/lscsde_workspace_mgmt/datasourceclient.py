from .datasourcebindingclient import AnalyticsDataSourceBindingClient
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
    AnalyticsDataSourceStatus,
    AnalyticsDataSourceSpec,
    AnalyticsDataSource,
)


class AnalyticsDataSourceClient(KubernetesNamespacedCustomClient):
    """
    AnalyticsDataSourceClient provides an interface to interact with AnalyticsDataSource
    custom resources in Kubernetes.

    This client allows developers to perform CRUD operations on AnalyticsDataSource objects
    such as creating, listing, updating, patching, and deleting resources. It also provides
    specialized methods for working with AnalyticsDataSources in the context of workspaces.

    The client handles serialization and deserialization of Kubernetes resources to and from
    the AnalyticsDataSource model using Pydantic validation.
    """

    adaptor = TypeAdapter(AnalyticsDataSource)

    def __init__(
        self, k8s_api: client.CustomObjectsApi, log: Logger, event_client: EventClient
    ):
        """
        Initialize the AnalyticsDataSourceClient.

        Args:
            k8s_api (client.CustomObjectsApi): Kubernetes API client for custom resources
            log (Logger): Logger instance for recording operations
            event_client (EventClient): Client for publishing events related to AnalyticsDataSource operations
        """
        super().__init__(
            k8s_api=k8s_api,
            log=log,
            group="xlscsde.nhs.uk",
            version="v1",
            plural="analyticsdatasources",
            kind="AnalyticsDataSource",
        )
        self.event_client = event_client

    async def get(self, namespace, name):
        """
        Gets an individual AnalyticsDataSource.

        Args:
            namespace (str): The namespace containing the resource
            name (str): Name of the AnalyticsDataSource to retrieve

        Returns:
            AnalyticsDataSource: The retrieved and validated AnalyticsDataSource object
        """
        result = await super().get(namespace, name)
        return self.adaptor.validate_python(result)

    async def list(self, namespace, **kwargs):
        """
        Lists the AnalyticsDataSource resources in a specified namespace.

        Args:
            namespace (str): The namespace to list resources from
            **kwargs: Additional parameters to pass to the Kubernetes API

        Returns:
            list[AnalyticsDataSource]: List of AnalyticsDataSource objects in the namespace
        """
        result = await super().list(namespace, **kwargs)

        return [self.adaptor.validate_python(item) for item in result["items"]]

    async def list_by_workspace(
        self,
        binding_client: AnalyticsDataSourceBindingClient,
        namespace: str,
        workspace: str,
    ):
        """
        Lists the AnalyticsDataSource resources in a specified namespace for the given workspace.

        This method returns data sources that are bound to the specified workspace through
        AnalyticsDataSourceBinding resources. It also adjusts expiration dates based on
        binding-specific constraints.

        Args:
            binding_client (AnalyticsDataSourceBindingClient): Client for accessing binding resources
            namespace (str): The namespace to list resources from
            workspace (str): The workspace identifier to filter by

        Returns:
            list[AnalyticsDataSource]: List of AnalyticsDataSource objects bound to the workspace
        """
        bindings = await binding_client.list_by_workspace(
            namespace=namespace, workspace=workspace
        )
        bound_datasources = {x.metadata.name: x.spec for x in bindings}
        datasources = []
        for bound_datasource in bound_datasources.keys():
            try:
                datasource_name: str = bound_datasources[bound_datasource].datasource

                if datasource_name not in [x.metadata.name for x in datasources]:
                    datasource = await self.get(
                        namespace=namespace, name=datasource_name
                    )

                    if datasource is not None:
                        if (
                            bound_datasources[bound_datasource].expires
                            < datasource.spec.validity.expires
                        ):
                            datasource.spec.validity.expires = bound_datasources[
                                bound_datasource
                            ].expires

                        datasources.append(datasource)
                else:
                    for datasource in datasources:
                        if datasource.metadata.name == datasource_name:
                            if (
                                bound_datasources[bound_datasource].expires
                                < datasource.spec.validity.expires
                            ):
                                datasource.spec.validity.expires = bound_datasources[
                                    bound_datasource
                                ].expires

            except ApiException as e:
                if e.status == 404:
                    self.log.error(
                        f"DataSource {bound_datasource} referenced by datasource {datasource} on {namespace} does not exist"
                    )
                else:
                    raise e

        return datasources

    async def create(self, body: AnalyticsDataSource):
        """
        Creates a new AnalyticsDataSource resource.

        Args:
            body (AnalyticsDataSource): The AnalyticsDataSource object to create

        Returns:
            AnalyticsDataSource: The created AnalyticsDataSource with server-side fields populated

        Fires:
            DataSourceCreated event via the event_client
        """
        result = await super().create(
            namespace=body.metadata.namespace,
            body=self.adaptor.dump_python(body, by_alias=True),
        )
        created_datasource: AnalyticsDataSource = self.adaptor.validate_python(result)
        await self.event_client.DataSourceCreated(created_datasource)
        return created_datasource

    async def patch(
        self,
        namespace: str = None,
        name: str = None,
        patch_body: dict = None,
        body: AnalyticsDataSource = None,
    ):
        """
        Patches an existing AnalyticsDataSource resource.

        This method can be called either with explicit namespace, name and patch_body parameters,
        or with a complete AnalyticsDataSource object in the body parameter.

        Args:
            namespace (str, optional): The namespace containing the resource
            name (str, optional): Name of the AnalyticsDataSource to patch
            patch_body (dict, optional): JSON patch operations to apply
            body (AnalyticsDataSource, optional): Complete AnalyticsDataSource object to derive patch from

        Returns:
            AnalyticsDataSource: The updated AnalyticsDataSource after patching

        Raises:
            InvalidParameterException: If neither the (namespace, name, patch_body) combination
                                      nor the body parameter is provided

        Fires:
            DataSourceUpdated event via the event_client
        """
        if not patch_body:
            if not body:
                raise InvalidParameterException(
                    "Either namespace, name and patch_body or body must be provided"
                )

            spec_adapter = TypeAdapter(AnalyticsDataSourceSpec)
            status_adapter = TypeAdapter(AnalyticsDataSourceStatus)

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

        result = await super().patch(namespace=namespace, name=name, body=patch_body)

        updated_datasource: AnalyticsDataSource = self.adaptor.validate_python(result)
        await self.event_client.DataSourceUpdated(updated_datasource)
        return updated_datasource

    async def patch_status(
        self, namespace: str, name: str, status: AnalyticsDataSourceStatus
    ):
        """
        Patches the status segment of an AnalyticsDataSource resource.

        Args:
            namespace (str): The namespace containing the resource
            name (str): Name of the AnalyticsDataSource to patch
            status (AnalyticsDataSourceStatus): The new status to apply

        Returns:
            AnalyticsDataSource: The updated AnalyticsDataSource after patching the status
        """
        status_adapter = TypeAdapter(AnalyticsDataSourceStatus)
        body = [
            {
                "op": "replace",
                "path": "/status",
                "value": status_adapter.dump_python(status, by_alias=True),
            }
        ]
        result = await super().patch_status(namespace=namespace, name=name, body=body)
        return self.adaptor.validate_python(result)

    async def replace(self, body: AnalyticsDataSource):
        """
        Replaces an existing AnalyticsDataSource resource with the one provided.

        Unlike patch, this completely replaces the existing resource with the new one.

        Args:
            body (AnalyticsDataSource): The new AnalyticsDataSource object to replace the existing one

        Returns:
            AnalyticsDataSource: The replaced AnalyticsDataSource with server-side fields updated
        """
        result = await super().replace(
            namespace=body.metadata.namespace,
            name=body.metadata.name,
            body=self.adaptor.dump_python(body, by_alias=True),
        )
        return self.adaptor.validate_python(result)

    async def delete(
        self, body: AnalyticsDataSource = None, namespace: str = None, name: str = None
    ):
        """
        Deletes an AnalyticsDataSource resource.

        This method first updates the status to "Deleting" before performing the actual deletion.

        Args:
            body (AnalyticsDataSource, optional): The AnalyticsDataSource object to delete
            namespace (str, optional): The namespace containing the resource
            name (str, optional): Name of the AnalyticsDataSource to delete

        Returns:
            dict: The Kubernetes API response for the delete operation

        Fires:
            DataSourceDeleted event via the event_client when a body is provided
        """
        if body:
            if not namespace:
                namespace = body.metadata.namespace
            if not name:
                name = body.metadata.name

        patch_body = [
            {"op": "replace", "path": "/status/statusText", "value": "Deleting"}
        ]

        current = await super().get(namespace, name)
        if not current.get("status"):
            patch_body = [
                {"op": "add", "path": "/status", "value": {"statusText": "Deleting"}}
            ]

        await super().patch_status(
            namespace=body.metadata.namespace, name=body.metadata.name, body=patch_body
        )

        if body:
            await self.event_client.DataSourceDeleted(body)

        return await super().delete(
            namespace=body.metadata.namespace, name=body.metadata.name
        )
