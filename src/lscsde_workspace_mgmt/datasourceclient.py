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

from os import getenv
from uuid import uuid4
from pytz import utc

# This class allows developers to interact with AnalyticsDataSource objects on kubernetes
class AnalyticsDataSourceClient(KubernetesNamespacedCustomClient):
    adaptor = TypeAdapter(AnalyticsDataSource)

    def __init__(self, k8s_api: client.CustomObjectsApi, log: Logger, event_client : EventClient):
        super().__init__(
            k8s_api = k8s_api, 
            log = log, 
            group = "xlscsde.nhs.uk",
            version = "v1",
            plural = "analyticsdatasources",
            kind = "AnalyticsDataSource"
        )
        self.event_client = event_client
        
    # Gets an individual AnalyticsDataSource
    async def get(self, namespace, name):
        result = await super().get(namespace, name)
        return self.adaptor.validate_python(result)
    
    # Lists the AnalyticsDataSource in a specified namespace
    async def list(self, namespace, **kwargs):
        result = await super().list(namespace, **kwargs)
        
        return [self.adaptor.validate_python(item) for item in result["items"]]
    
    async def list_by_workspace(self, binding_client : AnalyticsDataSourceBindingClient, namespace : str, workspace : str):
        bindings = await binding_client.list_by_workspace(
            namespace = namespace,
            workspace = workspace
            )
        bound_datasources = {x.metadata.name:x.spec for x in bindings}
        datasources = []
        for bound_datasource in bound_datasources.keys():
            try:
                datasource_name : str = bound_datasources[bound_datasource].datasource

                if datasource_name not in [x.metadata.name for x in datasources]:
                    datasource = await self.get(namespace = namespace, name = datasource_name)
                    
                    if datasource != None:
                        if bound_datasources[bound_datasource].expires < datasource.spec.validity.expires:
                            datasource.spec.validity.expires = bound_datasources[bound_datasource].expires

                        datasources.append(datasource)
                else:
                    for datasource in datasources:
                        if datasource.metadata.name == datasource_name:
                            if bound_datasources[bound_datasource].expires < datasource.spec.validity.expires:
                                datasource.spec.validity.expires = bound_datasources[bound_datasource].expires
    
            except ApiException as e:
                if e.status == 404:
                    self.log.error(f"DataSource {bound_datasource} referenced by datasource {datasource} on {namespace} does not exist")
                else:
                    raise e    
        
        return datasources     
            
    # Creates a AnalyticsDataSource resource
    async def create(self, body : AnalyticsDataSource):
        result = await super().create(
            namespace = body.metadata.namespace,
            body = self.adaptor.dump_python(body, by_alias=True)
        )
        created_datasource : AnalyticsDataSource = self.adaptor.validate_python(result)
        await self.event_client.DataSourceCreated(created_datasource)
        return created_datasource

    # Patches a AnalyticsDataSource resource
    async def patch(self, namespace : str = None, name : str = None, patch_body : dict = None, body : AnalyticsDataSource = None):
        if not patch_body:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            
            spec_adapter = TypeAdapter(AnalyticsDataSourceSpec)
            status_adapter = TypeAdapter(AnalyticsDataSourceStatus)

            patch_body = [
                {"op": "replace", "path": "/spec", "value": spec_adapter.dump_python(body.spec, by_alias=True)},
                {"op": "replace", "path": "/status", "value": status_adapter.dump_python(body.status, by_alias=True)}
            ]

        if not namespace:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            namespace = body.metadata.namespace

        if not name:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            name = body.metadata.name
            
        result = await super().patch(
            namespace = namespace,
            name = name,
            body = patch_body
        )        
        
        updated_datasource : AnalyticsDataSource = self.adaptor.validate_python(result)
        await self.event_client.DataSourceUpdated(updated_datasource)
        return updated_datasource

    # Patches a AnalyticsDataSource resources status segment
    async def patch_status(self, namespace : str, name : str, status : AnalyticsDataSourceStatus):
        status_adapter = TypeAdapter(AnalyticsDataSourceStatus)
        body = [{"op": "replace", "path": "/status", "value": status_adapter.dump_python(status, by_alias=True)}] 
        result = await super().patch_status(
            namespace = namespace,
            name = name,
            body = body
        )
        return self.adaptor.validate_python(result)


    # Replaces a AnalyticsDataSource resource with the one provided
    async def replace(self, body : AnalyticsDataSource):
        result = await super().replace(
            namespace = body.metadata.namespace,
            name = body.metadata.name,
            body = self.adaptor.dump_python(body, by_alias=True)
        )
        return self.adaptor.validate_python(result)
        
    
    # Deletes a AnalyticsDataSource resource
    async def delete(self, body : AnalyticsDataSource = None, namespace : str = None, name : str = None):
        if body:
            if not namespace:
                namespace = body.metadata.namespace
            if not name:
                name = body.metadata.name
        
        
        patch_body = [{"op": "replace", "path": "/status/statusText", "value": "Deleting"}] 

        current = await super().get(namespace, name)
        if not current.get("status"):
            patch_body = [{"op": "add", "path": "/status", "value": { "statusText" : "Deleting" }}] 

        await super().patch_status(
            namespace = body.metadata.namespace,
            name = body.metadata.name,
            body = patch_body
        )

        if body:
            await self.event_client.DataSourceDeleted(body)
        
        return await super().delete(
            namespace = body.metadata.namespace,
            name = body.metadata.name
        )