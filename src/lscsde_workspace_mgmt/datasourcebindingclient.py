from .namespacedclient import KubernetesNamespacedCustomClient
from .eventclient import EventClient
from logging import Logger
from kubernetes_asyncio import client
from pydantic import TypeAdapter
from .exceptions import (
    InvalidParameterException,
    InvalidLabelFormatException
)

from .models import (
    AnalyticsDataSourceBinding,
    AnalyticsDataSourceBindingSpec,
    AnalyticsDataSourceBindingStatus,
)

from os import getenv
from uuid import uuid4
from pytz import utc

class AnalyticsDataSourceBindingClient(KubernetesNamespacedCustomClient):
    """
    This class allows developers to interact with AnalyticsDataSourceBinding objects on kubernetes
    """

    adaptor = TypeAdapter(AnalyticsDataSourceBinding)
    def __init__(self, k8s_api: client.CustomObjectsApi, log: Logger, event_client : EventClient):
        super().__init__(
            k8s_api = k8s_api, 
            log = log, 
            group = "xlscsde.nhs.uk",
            version = "v1",
            plural = "analyticsdatasourcebindings",
            kind = "AnalyticsDataSourceBinding"
        )
        self.event_client = event_client

    async def get(self, namespace, name):
        """
        Gets an individual AnalyticsDataSourceBinding
        """
        result = await super().get(namespace, name)
        return self.adaptor.validate_python(result)
    
    async def list(self, namespace, **kwargs):
        """
        Lists the AnalyticsDataSourceBindings in a specified namespace
        """
        result = await super().list(namespace, **kwargs)
        return [self.adaptor.validate_python(item) for item in result["items"]]

    
    async def list_by_workspace(self, namespace, workspace):
        """
        Lists the AnalyticsDataSourceBindings in a specified namespace which belong to a specific workspace
        
        If a binding does not have the relevant labels defined, the service will assign the label automatically based upon the workspace. 
        This makes the query more performant when querying etcd.
        """

        no_label = await self.list(namespace = namespace, label_selector = f"!xlscsde.nhs.uk/workspace")
        for item in no_label:
            if item.spec.workspace:
                try:
                    if not item.metadata.labels:
                        patch_body = [{"op": "add", "path": "/metadata/labels", "value": { "xlscsde.nhs.uk/workspace" : item.spec.workspace }}]
                    else:
                        patch_body = [{"op": "add", "path": "/metadata/labels/xlscsde.nhs.uk~1workspace", "value": item.spec.workspace }]

                    patch_response = await self.patch(
                        namespace = item.metadata.namespace, 
                        name = item.metadata.name, 
                        patch_body = patch_body
                        )
                except InvalidLabelFormatException as ex:
                    self.log.error(f"Could not validate {item.metadata.name} due to a label format exception: {ex}")

        return await self.list(namespace = namespace, label_selector = f"xlscsde.nhs.uk/workspace={workspace}")

    async def create(self, body : AnalyticsDataSourceBinding, append_label : bool = True):
        """
        Creates a AnalyticsDataSourceBinding resource
        """

        contents = self.adaptor.dump_python(body, by_alias=True)
        
        if append_label:
            contents["metadata"]["labels"]["xlscsde.nhs.uk/workspace"] = body.spec.workspace

        result = await super().create(
            namespace = body.metadata.namespace,
            body = contents
        )
        
        created_binding : AnalyticsDataSourceBinding = self.adaptor.validate_python(result)
        await self.event_client.DataSourceBindingUpdated(created_binding)
        return created_binding

    async def patch(self, namespace : str = None, name : str = None, patch_body : dict = None, body : AnalyticsDataSourceBinding = None):
        """
        Patches a AnalyticsDataSourceBinding resource
        """
        if not patch_body:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            
            spec_adapter = TypeAdapter(AnalyticsDataSourceBindingSpec)
            status_adapter = TypeAdapter(AnalyticsDataSourceBindingStatus)
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
        
        updated_binding : AnalyticsDataSourceBinding = self.adaptor.validate_python(result)
        await self.event_client.DataSourceBindingUpdated(updated_binding)
        return updated_binding

    async def patch_status(self, namespace : str, name : str, status : AnalyticsDataSourceBindingStatus):
        """
        Patches a AnalyticsDataSourceBinding resources status segment
        """
        status_adapter = TypeAdapter(AnalyticsDataSourceBindingStatus)
        body = [{"op": "replace", "path": "/status", "value": status_adapter.dump_python(status, by_alias=True)}] 
        result = await super().patch_status(
            namespace = namespace,
            name = name,
            body = body
        )
        return self.adaptor.validate_python(result)

    async def replace(self, body : AnalyticsDataSourceBinding, append_label : bool = True):
        """
        Replaces a AnalyticsDataSourceBinding resource with the one provided
        """
        contents = self.adaptor.dump_python(body, by_alias=True)
        if append_label:
            contents["metadata"]["labels"]["xlscsde.nhs.uk/workspace"] = body.spec.workspace

        result = await super().replace(
            namespace = body.metadata.namespace,
            name = body.metadata.name,
            body = contents
        )
        updated_binding : AnalyticsDataSourceBinding = self.adaptor.validate_python(result)
        await self.event_client.DataSourceBindingUpdated(updated_binding)
        return updated_binding
    
    async def delete(self, body : AnalyticsDataSourceBinding = None, namespace : str = None, name : str = None):
        """
        Deletes a AnalyticsDataSourceBinding resource
        """
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
            await self.event_client.DataSourceBindingDeleted(body)

        return await super().delete(
            namespace = body.metadata.namespace,
            name = body.metadata.name
        )

