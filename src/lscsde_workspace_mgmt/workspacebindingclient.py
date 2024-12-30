from .namespacedclient import KubernetesNamespacedCustomClient
from .eventclient import EventClient

from logging import Logger
from kubernetes_asyncio import client
from kubernetes_asyncio.client.exceptions import ApiException
from pydantic import TypeAdapter
from .exceptions import (
    InvalidParameterException,
    InvalidLabelFormatException
)

from .models import (
    AnalyticsWorkspaceBinding,
    AnalyticsWorkspaceBindingStatus,
    AnalyticsWorkspaceBindingSpec,
    KubernetesHelper,
    AnalyticsWorkspaceBinding
)

from os import getenv
from uuid import uuid4
from pytz import utc

class AnalyticsWorkspaceBindingClient(KubernetesNamespacedCustomClient):
    adaptor = TypeAdapter(AnalyticsWorkspaceBinding)
    def __init__(self, k8s_api: client.CustomObjectsApi, log: Logger, event_client : EventClient):
        super().__init__(
            k8s_api = k8s_api, 
            log = log, 
            group = "xlscsde.nhs.uk",
            version = "v1",
            plural = "analyticsworkspacebindings",
            kind = "AnalyticsWorkspaceBinding"
        )
        self.event_client = event_client

    async def get(self, namespace, name):
        result = await super().get(namespace, name)
        return self.adaptor.validate_python(result)
    
    async def list(self, namespace, **kwargs):
        result = await super().list(namespace, **kwargs)
        return [self.adaptor.validate_python(item) for item in result["items"]]

    async def list_by_username(self, namespace, username):
        helper = KubernetesHelper() 
        formatted_username = helper.format_as_label(username)
        no_label = await self.list(namespace = namespace, label_selector = f"!xlscsde.nhs.uk/username")
        for item in no_label:
            if item.spec.username:
                try:
                    if not item.metadata.labels:
                        patch_body = [{"op": "add", "path": "/metadata/labels", "value": { "xlscsde.nhs.uk/username" : item.spec.username_as_label() }}]
                    else:
                        patch_body = [{"op": "add", "path": "/metadata/labels/xlscsde.nhs.uk~1username", "value": item.spec.username_as_label() }]

                    patch_response = await self.patch(
                        namespace = item.metadata.namespace, 
                        name = item.metadata.name, 
                        patch_body = patch_body
                        )
                except InvalidLabelFormatException as ex:
                    self.log.error(f"Could not validate {item.metadata.name} due to a label format exception: {ex}")

        return await self.list(namespace = namespace, label_selector = f"xlscsde.nhs.uk/username={formatted_username}")

    async def create(self, body : AnalyticsWorkspaceBinding, append_label : bool = True):
        contents = self.adaptor.dump_python(body, by_alias=True)
        
        if append_label:
            contents["metadata"]["labels"]["xlscsde.nhs.uk/username"] = body.spec.username_as_label()

        result = await super().create(
            namespace = body.metadata.namespace,
            body = contents
        )
        
        created_binding : AnalyticsWorkspaceBinding = self.adaptor.validate_python(result)
        await self.event_client.WorkspaceBindingUpdated(created_binding)
        return created_binding

    async def patch(self, namespace : str = None, name : str = None, patch_body : dict = None, body : AnalyticsWorkspaceBinding = None):
        if not patch_body:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            
            spec_adapter = TypeAdapter(AnalyticsWorkspaceBindingSpec)
            status_adapter = TypeAdapter(AnalyticsWorkspaceBindingStatus)
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
        
        updated_binding : AnalyticsWorkspaceBinding = self.adaptor.validate_python(result)
        await self.event_client.WorkspaceBindingUpdated(updated_binding)
        return updated_binding

    async def patch_status(self, namespace : str, name : str, status : AnalyticsWorkspaceBindingStatus):
        status_adapter = TypeAdapter(AnalyticsWorkspaceBindingStatus)
        body = [{"op": "replace", "path": "/status", "value": status_adapter.dump_python(status, by_alias=True)}] 
        result = await super().patch_status(
            namespace = namespace,
            name = name,
            body = body
        )
        return self.adaptor.validate_python(result)

    async def replace(self, body : AnalyticsWorkspaceBinding, append_label : bool = True):
        contents = self.adaptor.dump_python(body, by_alias=True)
        if append_label:
            contents["metadata"]["labels"]["xlscsde.nhs.uk/username"] = body.spec.username_as_label()

        result = await super().replace(
            namespace = body.metadata.namespace,
            name = body.metadata.name,
            body = contents
        )
        updated_binding : AnalyticsWorkspaceBinding = self.adaptor.validate_python(result)
        await self.event_client.WorkspaceBindingUpdated(updated_binding)
        return updated_binding
    
    async def delete(self, body : AnalyticsWorkspaceBinding = None, namespace : str = None, name : str = None):
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
            await self.event_client.WorkspaceBindingDeleted(body)

        return await super().delete(
            namespace = body.metadata.namespace,
            name = body.metadata.name
        )

