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

from os import getenv
from uuid import uuid4
from pytz import utc

class AnalyticsWorkspaceClient(KubernetesNamespacedCustomClient):
    """
    Client for interacting with AnalyticsWorkspacess
    """
    adaptor = TypeAdapter(AnalyticsWorkspace)

    def __init__(self, k8s_api: client.CustomObjectsApi, log: Logger, event_client : EventClient):
        super().__init__(
            k8s_api = k8s_api, 
            log = log, 
            group = "xlscsde.nhs.uk",
            version = "v1",
            plural = "analyticsworkspaces",
            kind = "AnalyticsWorkspace"
        )
        self.event_client = event_client
        
    
    async def get(self, namespace, name):
        """
        Gets a specific AnalyticsWorkspace resource
        """
        result = await super().get(namespace, name)
        return self.adaptor.validate_python(result)
    
    
    async def list(self, namespace, **kwargs):
        """
        Lists AnalyticsWorkspace resources in the namespace supplied
        """
        result = await super().list(namespace, **kwargs)
        
        return [self.adaptor.validate_python(item) for item in result["items"]]
    
    async def list_by_username(self, binding_client : AnalyticsWorkspaceBindingClient, namespace : str, username : str):
        """
        Lists AnalyticsWorkspace resources in the namespace supplied that match the username
        """
        bindings = await binding_client.list_by_username(
            namespace = namespace,
            username = username
            )
        bound_workspaces = {x.metadata.name:x.spec for x in bindings}
        workspaces = []
        for bound_workspace in bound_workspaces.keys():
            try:
                workspace_name : str = bound_workspaces[bound_workspace].workspace

                if workspace_name not in [x.metadata.name for x in workspaces]:
                    workspace = await self.get(namespace = namespace, name = workspace_name)
                    
                    if workspace != None:
                        if bound_workspaces[bound_workspace].expires < workspace.spec.validity.expires:
                            workspace.spec.validity.expires = bound_workspaces[bound_workspace].expires

                        workspaces.append(workspace)
                else:
                    for workspace in workspaces:
                        if workspace.metadata.name == workspace_name:
                            if bound_workspaces[bound_workspace].expires < workspace.spec.validity.expires:
                                workspace.spec.validity.expires = bound_workspaces[bound_workspace].expires
    
            except ApiException as e:
                if e.status == 404:
                    self.log.error(f"Workspace {bound_workspace} referenced by user {username} on {namespace} does not exist")
                else:
                    raise e    
        
        return workspaces     
            
    async def create(self, body : AnalyticsWorkspace):
        """
        Creates a AnalyticsWorkspace resource in the namespace supplied
        """
        result = await super().create(
            namespace = body.metadata.namespace,
            body = self.adaptor.dump_python(body, by_alias=True)
        )
        created_workspace : AnalyticsWorkspace = self.adaptor.validate_python(result)
        await self.event_client.WorkspaceCreated(created_workspace)
        return created_workspace

    async def patch(self, namespace : str = None, name : str = None, patch_body : dict = None, body : AnalyticsWorkspace = None):
        """
        Patches a AnalyticsWorkspace resource in the namespace supplied
        """
        if not patch_body:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            
            spec_adapter = TypeAdapter(AnalyticsWorkspaceSpec)
            status_adapter = TypeAdapter(AnalyticsWorkspaceStatus)

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
        
        updated_workspace : AnalyticsWorkspace = self.adaptor.validate_python(result)
        await self.event_client.WorkspaceUpdated(updated_workspace)
        return updated_workspace

    
    async def patch_status(self, namespace : str, name : str, status : AnalyticsWorkspaceStatus):
        """
        Patches the status of an AnalyticsWorkspace resource in the namespace supplied
        """
        status_adapter = TypeAdapter(AnalyticsWorkspaceStatus)
        body = [{"op": "replace", "path": "/status", "value": status_adapter.dump_python(status, by_alias=True)}] 
        result = await super().patch_status(
            namespace = namespace,
            name = name,
            body = body
        )
        return self.adaptor.validate_python(result)

    async def replace(self, body : AnalyticsWorkspace):
        """
        Replaces a AnalyticsWorkspace resource with the one supplied
        """
        result = await super().replace(
            namespace = body.metadata.namespace,
            name = body.metadata.name,
            body = self.adaptor.dump_python(body, by_alias=True)
        )
        return self.adaptor.validate_python(result)
        
    async def delete(self, body : AnalyticsWorkspace = None, namespace : str = None, name : str = None):
        """
        Deletes a AnalyticsWorkspace resource in the namespace supplied
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
            await self.event_client.WorkspaceDeleted(body)
        
        return await super().delete(
            namespace = body.metadata.namespace,
            name = body.metadata.name
        )

