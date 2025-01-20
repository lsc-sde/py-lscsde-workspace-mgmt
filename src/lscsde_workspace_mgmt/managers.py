from datetime import datetime
from .k8sio import (
    AnalyticsWorkspaceClient,
    AnalyticsWorkspaceBindingClient,
    AnalyticsDataSourceClient,
    AnalyticsDataSourceBindingClient,
    PersistentVolumeClaimClient,
    V1ObjectMeta,
    V1Pod
)

from .eventclient import EventClient

from .models import (
    AnalyticsWorkspace,
    AnalyticsWorkspaceBinding
)

from .objects import (
    AnalyticsWorkspaceConverter
)

from .exceptions import (
    WorkspaceNotFoundException
)

from kubernetes_asyncio.client import (
    CustomObjectsApi,
    ApiClient
)
from logging import Logger

class AnalyticsDataSourceManager:
    """
    creates a manager for Analytics Data sources, their associated bindings, events and pvc's.
    """

    def __init__(self, api_client : ApiClient, log : Logger, reporting_controller : str = "xlscsde.nhs.uk/unspecified-controller", reporting_user = "Unknown User"):
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.event_client = EventClient(api_client=api_client,log = log, reporting_controller = reporting_controller, reporting_user=reporting_user)
        self.datasource_client = AnalyticsDataSourceClient(custom_objects_api, log, event_client=self.event_client)
        self.binding_client = AnalyticsDataSourceBindingClient(custom_objects_api, log, event_client=self.event_client)
        self.pvc_client = PersistentVolumeClaimClient(api_client, log)
        self.log = log

class AnalyticsWorkspaceManager:
    """
    creates a manager for Analytics Workspaces, their associated bindings, events and pvc's.
    """

    def __init__(self, api_client : ApiClient, log : Logger, reporting_controller : str = "xlscsde.nhs.uk/unspecified-controller", reporting_user = "Unknown User"):
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.event_client = EventClient(api_client=api_client,log = log, reporting_controller = reporting_controller, reporting_user=reporting_user)
        self.workspace_client = AnalyticsWorkspaceClient(custom_objects_api, log, event_client=self.event_client)
        self.binding_client = AnalyticsWorkspaceBindingClient(custom_objects_api, log, event_client=self.event_client)
        self.pvc_client = PersistentVolumeClaimClient(api_client, log)
        self.log = log

    async def get_workspaces_for_user(self, namespace : str, username : str):
        """
        Gets a workspace for a user
        """
        workspaces = await self.workspace_client.list_by_username(self.binding_client, namespace, username)
        permitted_workspaces : dict[str, AnalyticsWorkspace] = {}
        for workspace in workspaces:
            if workspace.metadata.name not in permitted_workspaces:
                permitted_workspaces[workspace.metadata.name] = workspace

        return permitted_workspaces

    
    async def get_permitted_workspaces(self, namespace : str, username : str, date_now = datetime.today()):
        """
        Gets the workspaces that are permitted for a user
        """
        permitted_workspaces = await self.get_workspaces_for_user(namespace, username)
        sorted_workspaces = sorted(
            permitted_workspaces.values(), key=lambda x: x.spec.display_name
        )
        converter = AnalyticsWorkspaceConverter()
        return [converter.to_workspace_dict(item, date_now = date_now) for item in sorted_workspaces]
    
    
    async def mount_workspace(self, pod : V1Pod, storage_class_name, mount_prefix, storage_prefix : str = "", read_only : bool = False, mount_path = ""):
        """
        Mounts the workspace persistent volume claims
        """
        metadata : V1ObjectMeta = pod.metadata
        namespace = metadata.namespace
        name = metadata.name
        workspace_name = metadata.labels.get("workspace")

        if not workspace_name:
            raise WorkspaceNotFoundException(namespace, name)
        
        workspace = await self.workspace_client.get(namespace, workspace_name)
        
        storage_name : str = f"{storage_prefix}{workspace_name}"

        if workspace.status.persistent_volume_claim:
            storage_name = workspace.status.persistent_volume_claim 

        if workspace.spec.jupyter_workspace.persistent_volume_claim.name:
            storage_name = workspace.spec.jupyter_workspace.persistent_volume_claim.name

        if workspace.spec.jupyter_workspace.persistent_volume_claim.storage_class_name:
            storage_class_name = workspace.spec.jupyter_workspace.persistent_volume_claim.storage_class_name

        if not mount_path:
            mount_path = f"{mount_prefix}/{workspace_name}"
        
        amended_pod = await self.pvc_client.mount(
            pod = pod, 
            storage_name = storage_name, 
            namespace = namespace,
            mount_path = mount_path,
            storage_class_name = storage_class_name,
            read_only = read_only
            )
        
        update_status : bool = False
        if not workspace.status.persistent_volume_claim:
            workspace.status.persistent_volume_claim = storage_name
            update_status = True

        if workspace.status.status_text != "Provisioned":
            workspace.status.status_text = "Provisioned"
            update_status = True
        
        if update_status == True:
            await self.workspace_client.patch_status(
                namespace = workspace.metadata.namespace,
                name = workspace.metadata.name,
                status = workspace.status
                )
            
class AnalyticsManager:
    """
    A high level manager for both workspace and datasource
    """
    def __init__(self, api_client : ApiClient, log : Logger, reporting_controller : str = "xlscsde.nhs.uk/unspecified-controller", reporting_user = "Unknown User"):
        self.workspace = AnalyticsWorkspaceManager(api_client, log, reporting_controller, reporting_user)
        self.datasource = AnalyticsDataSourceManager(api_client, log, reporting_controller, reporting_user)