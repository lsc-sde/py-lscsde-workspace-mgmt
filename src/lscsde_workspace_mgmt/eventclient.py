from logging import Logger
from kubernetes_asyncio import client

from .models import (
    AnalyticsDataSource,
    AnalyticsDataSourceBinding,
    AnalyticsWorkspaceBinding,
    AnalyticsWorkspace, 
    AnalyticsWorkspaceBinding
)


from kubernetes_asyncio.client.models import (
    V1ObjectMeta,
)
from os import getenv
from datetime import datetime
from uuid import uuid4
from pytz import utc

# A class for interacting with Events objects in kubernetes
class EventClient:
    def __init__(self, api_client : client.ApiClient, log : Logger, reporting_controller : str = "xlscsde.nhs.uk/undefined-controller", reporting_user = "Unknown User"):
        self.api = client.EventsV1Api(api_client)
        self.log = log
        self.reporting_controller = reporting_controller
        self.reporting_instance = getenv("HOSTNAME", getenv("COMPUTERNAME", "unknown"))
        self.reporting_user = reporting_user

    # Records a workspace event
    async def RegisterWorkspaceEvent(self, workspace : AnalyticsWorkspace, reason : str, note : str):
        event_time = datetime.now(utc)
        body = client.EventsV1Event(
            action=reason,
            metadata = V1ObjectMeta(
                namespace = workspace.metadata.namespace,
                name = f"ws-{uuid4().hex}-{workspace.metadata.resource_version}-evt"
            ),
            event_time = event_time,
            reason = reason,
            note = note,
            reporting_controller = self.reporting_controller,
            reporting_instance = self.reporting_instance,
            regarding=client.V1ObjectReference(
                api_version = workspace.api_version,
                kind = workspace.kind,
                namespace = workspace.metadata.namespace,
                name = workspace.metadata.name
            ),
            type = "Normal"
        )
        await self.api.create_namespaced_event(namespace = workspace.metadata.namespace, body = body)
    
    # Records a workspace binding event
    async def RegisterWorkspaceBindingEvent(self, binding : AnalyticsWorkspaceBinding, reason : str, note : str):
        event_time = datetime.now(utc)
        body = client.EventsV1Event(
            action=reason,
            metadata = V1ObjectMeta(
                namespace = binding.metadata.namespace,
                name = f"wsb-{uuid4().hex}-{binding.metadata.resource_version}-evt"
            ),
            event_time = event_time,
            reason = reason,
            note = note,
            reporting_controller = self.reporting_controller,
            reporting_instance = self.reporting_instance,
            regarding=client.V1ObjectReference(
                api_version = binding.api_version,
                kind = binding.kind,
                namespace = binding.metadata.namespace,
                name = binding.metadata.name
            ),
            type = "Normal"
        )
        await self.api.create_namespaced_event(namespace = binding.metadata.namespace, body = body)
    
    # Records a datasource event
    async def RegisterDataSourceEvent(self, datasource : AnalyticsDataSource, reason : str, note : str):
        event_time = datetime.now(utc)
        body = client.EventsV1Event(
            action=reason,
            metadata = V1ObjectMeta(
                namespace = datasource.metadata.namespace,
                name = f"ds-{uuid4().hex}-{datasource.metadata.resource_version}-evt"
            ),
            event_time = event_time,
            reason = reason,
            note = note,
            reporting_controller = self.reporting_controller,
            reporting_instance = self.reporting_instance,
            regarding=client.V1ObjectReference(
                api_version = datasource.api_version,
                kind = datasource.kind,
                namespace = datasource.metadata.namespace,
                name = datasource.metadata.name
            ),
            type = "Normal"
        )
        await self.api.create_namespaced_event(namespace = datasource.metadata.namespace, body = body)
    
    # Records a datasource binding event
    async def RegisterDataSourceBindingEvent(self, binding : AnalyticsDataSourceBinding, reason : str, note : str):
        event_time = datetime.now(utc)
        body = client.EventsV1Event(
            action=reason,
            metadata = V1ObjectMeta(
                namespace = binding.metadata.namespace,
                name = f"wsb-{uuid4().hex}-{binding.metadata.resource_version}-evt"
            ),
            event_time = event_time,
            reason = reason,
            note = note,
            reporting_controller = self.reporting_controller,
            reporting_instance = self.reporting_instance,
            regarding=client.V1ObjectReference(
                api_version = binding.api_version,
                kind = binding.kind,
                namespace = binding.metadata.namespace,
                name = binding.metadata.name
            ),
            type = "Normal"
        )
        await self.api.create_namespaced_event(namespace = binding.metadata.namespace, body = body)
    
    # Records a workspace was created
    async def WorkspaceCreated(self, workspace : AnalyticsWorkspace, note : str = None):
        if not note:
            note = f"Workspace Created by {self.reporting_user}"

        await self.RegisterWorkspaceEvent(workspace, "WorkspaceCreated", note)

    # Records a workspace was updates
    async def WorkspaceUpdated(self, workspace : AnalyticsWorkspace, note : str = None):
        if not note:
            note = f"Workspace Updated by {self.reporting_user}"

        await self.RegisterWorkspaceEvent(workspace, "WorkspaceUpdated", note)

    # Records a workspace was deleted
    async def WorkspaceDeleted(self, workspace : AnalyticsWorkspace, note : str = None):
        if not note:
            note = f"Workspace Deleted by {self.reporting_user}"

        await self.RegisterWorkspaceEvent(workspace, "WorkspaceDeleted", note)

    # Records a workspace binding was created
    async def WorkspaceBindingCreated(self, binding : AnalyticsWorkspaceBinding, note : str = None):
        if not note:
            note = f"Workspace Binding Created by {self.reporting_user}"
        await self.RegisterWorkspaceBindingEvent(binding, "WorkspaceBindingCreated", note)

    # Records a workspace binding was updated
    async def WorkspaceBindingUpdated(self, binding : AnalyticsWorkspaceBinding, note : str = None):
        if not note:
            note = f"Workspace Binding Updated by {self.reporting_user}"
        await self.RegisterWorkspaceBindingEvent(binding, "WorkspaceBindingUpdated", note)

    # Records a workspace binding was deleted
    async def WorkspaceBindingDeleted(self, binding : AnalyticsWorkspaceBinding, note : str = None):
        if not note:
            note = f"Workspace Binding Deleted by {self.reporting_user}"
        await self.RegisterWorkspaceBindingEvent(binding, "WorkspaceBindingDeleted", note)

    # Records a data source was created
    async def DataSourceCreated(self, datasource : AnalyticsDataSource, note : str = None):
        if not note:
            note = f"DataSource Created by {self.reporting_user}"

        await self.RegisterDataSourceEvent(datasource, "DataSourceCreated", note)

    # Records a data source was updated
    async def DataSourceUpdated(self, datasource : AnalyticsDataSource, note : str = None):
        if not note:
            note = f"DataSource Updated by {self.reporting_user}"

        await self.RegisterDataSourceEvent(datasource, "DataSourceUpdated", note)

    # Records a data source was deleted
    async def DataSourceDeleted(self, datasource : AnalyticsDataSource, note : str = None):
        if not note:
            note = f"DataSource Deleted by {self.reporting_user}"

        await self.RegisterDataSourceEvent(datasource, "DataSourceDeleted", note)

    # Records a data source binding was created
    async def DataSourceBindingCreated(self, binding : AnalyticsDataSourceBinding, note : str = None):
        if not note:
            note = f"DataSource Binding Created by {self.reporting_user}"
        await self.RegisterDataSourceBindingEvent(binding, "DataSourceBindingCreated", note)

    # Records a data source binding was updated
    async def DataSourceBindingUpdated(self, binding : AnalyticsDataSourceBinding, note : str = None):
        if not note:
            note = f"DataSource Binding Updated by {self.reporting_user}"
        await self.RegisterDataSourceBindingEvent(binding, "DataSourceBindingUpdated", note)

    # Records a data source binding was deleted
    async def DataSourceBindingDeleted(self, binding : AnalyticsDataSourceBinding, note : str = None):
        if not note:
            note = f"DataSource Binding Deleted by {self.reporting_user}"
        await self.RegisterDataSourceBindingEvent(binding, "DataSourceBindingDeleted", note)

        
