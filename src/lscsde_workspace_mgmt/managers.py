"""
Analytics Workspace Manager Module
=================================

This module provides manager classes that coordinate operations between different
Kubernetes custom resources related to analytics workspaces and data sources.

The managers serve as high-level interfaces that abstract away the details of
interacting with individual Kubernetes clients, providing a simplified API for
common operations like retrieving workspaces for users or mounting volumes.

Classes:
    - AnalyticsDataSourceManager: Manages operations for data sources and their bindings
    - AnalyticsWorkspaceManager: Manages operations for workspaces and their bindings
    - AnalyticsManager: Provides a unified interface to both workspace and datasource managers
"""

from datetime import datetime
from .k8sio import (
    AnalyticsWorkspaceClient,
    AnalyticsWorkspaceBindingClient,
    AnalyticsDataSourceClient,
    AnalyticsDataSourceBindingClient,
    PersistentVolumeClaimClient,
    V1ObjectMeta,
    V1Pod,
)

from .eventclient import EventClient

from .models import AnalyticsWorkspace

from .objects import AnalyticsWorkspaceConverter

from .exceptions import WorkspaceNotFoundException

from kubernetes_asyncio.client import CustomObjectsApi, ApiClient
from logging import Logger


class AnalyticsDataSourceManager:
    """
    Manager for Analytics Data sources, their associated bindings, events and PVCs.

    This class coordinates operations between data sources, bindings, and persistent
    volume claims, providing a high-level interface for data source operations.

    Attributes:
        event_client (EventClient): Client for recording Kubernetes events
        datasource_client (AnalyticsDataSourceClient): Client for data source operations
        binding_client (AnalyticsDataSourceBindingClient): Client for data source binding operations
        pvc_client (PersistentVolumeClaimClient): Client for PVC operations
        log (Logger): Logger instance for recording operations
    """

    def __init__(
        self,
        api_client: ApiClient,
        log: Logger,
        reporting_controller: str = "xlscsde.nhs.uk/unspecified-controller",
        reporting_user="Unknown User",
    ):
        """
        Initialize the AnalyticsDataSourceManager.

        Args:
            api_client (ApiClient): Kubernetes API client
            log (Logger): Logger instance
            reporting_controller (str, optional): Controller name for event reporting.
                Defaults to "xlscsde.nhs.uk/unspecified-controller".
            reporting_user (str, optional): User name for event reporting.
                Defaults to "Unknown User".
        """
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.event_client = EventClient(
            api_client=api_client,
            log=log,
            reporting_controller=reporting_controller,
            reporting_user=reporting_user,
        )
        self.datasource_client = AnalyticsDataSourceClient(
            custom_objects_api, log, event_client=self.event_client
        )
        self.binding_client = AnalyticsDataSourceBindingClient(
            custom_objects_api, log, event_client=self.event_client
        )
        self.pvc_client = PersistentVolumeClaimClient(api_client, log)
        self.log = log


class AnalyticsWorkspaceManager:
    """
    Manager for Analytics Workspaces, their associated bindings, events and PVCs.

    This class coordinates operations between workspaces, bindings, and persistent
    volume claims, providing a high-level interface for workspace operations.

    Attributes:
        event_client (EventClient): Client for recording Kubernetes events
        workspace_client (AnalyticsWorkspaceClient): Client for workspace operations
        binding_client (AnalyticsWorkspaceBindingClient): Client for workspace binding operations
        pvc_client (PersistentVolumeClaimClient): Client for PVC operations
        log (Logger): Logger instance for recording operations
    """

    def __init__(
        self,
        api_client: ApiClient,
        log: Logger,
        reporting_controller: str = "xlscsde.nhs.uk/unspecified-controller",
        reporting_user="Unknown User",
    ):
        """
        Initialize the AnalyticsWorkspaceManager.

        Args:
            api_client (ApiClient): Kubernetes API client
            log (Logger): Logger instance
            reporting_controller (str, optional): Controller name for event reporting.
                Defaults to "xlscsde.nhs.uk/unspecified-controller".
            reporting_user (str, optional): User name for event reporting.
                Defaults to "Unknown User".
        """
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.event_client = EventClient(
            api_client=api_client,
            log=log,
            reporting_controller=reporting_controller,
            reporting_user=reporting_user,
        )
        self.workspace_client = AnalyticsWorkspaceClient(
            custom_objects_api, log, event_client=self.event_client
        )
        self.binding_client = AnalyticsWorkspaceBindingClient(
            custom_objects_api, log, event_client=self.event_client
        )
        self.pvc_client = PersistentVolumeClaimClient(api_client, log)
        self.log = log

    async def get_workspaces_for_user(self, namespace: str, username: str):
        """
        Gets workspaces that a user has access to.

        Retrieves all workspaces that the specified user is allowed to access
        based on workspace bindings.

        Args:
            namespace (str): Kubernetes namespace to search in
            username (str): Username to check permissions for

        Returns:
            dict[str, AnalyticsWorkspace]: Dictionary of workspace name to workspace object
            for all workspaces the user has access to
        """
        workspaces = await self.workspace_client.list_by_username(
            self.binding_client, namespace, username
        )
        permitted_workspaces: dict[str, AnalyticsWorkspace] = {}
        for workspace in workspaces:
            if workspace.metadata.name not in permitted_workspaces:
                permitted_workspaces[workspace.metadata.name] = workspace

        return permitted_workspaces

    async def get_permitted_workspaces(
        self, namespace: str, username: str, date_now=datetime.today()
    ):
        """
        Gets the workspaces that are permitted for a user as dictionary objects.

        Retrieves workspace information in a format suitable for use in APIs
        or user interfaces, including display name, expiration dates, and
        remaining days.

        Args:
            namespace (str): Kubernetes namespace to search in
            username (str): Username to check permissions for
            date_now (datetime, optional): Reference date for calculating days remaining.
                Defaults to current date.

        Returns:
            list[dict]: List of workspace information dictionaries, sorted by display name
        """
        permitted_workspaces = await self.get_workspaces_for_user(namespace, username)
        sorted_workspaces = sorted(
            permitted_workspaces.values(), key=lambda x: x.spec.display_name
        )
        converter = AnalyticsWorkspaceConverter()
        return [
            converter.to_workspace_dict(item, date_now=date_now)
            for item in sorted_workspaces
        ]

    async def mount_workspace(
        self,
        pod: V1Pod,
        storage_class_name,
        mount_prefix,
        storage_prefix: str = "",
        read_only: bool = False,
        mount_path="",
    ):
        """
        Mounts the workspace persistent volume claims to a pod.

        Configures a pod to mount the persistent volume claim associated with
        a workspace. Updates the workspace status if needed.

        Args:
            pod (V1Pod): Kubernetes pod to mount the volume to
            storage_class_name (str): Storage class to use if a new PVC is created
            mount_prefix (str): Prefix to use for the mount path
            storage_prefix (str, optional): Prefix to use for storage name. Defaults to "".
            read_only (bool, optional): Whether to mount as read-only. Defaults to False.
            mount_path (str, optional): Custom mount path. If empty, one will be generated.
                Defaults to "".

        Raises:
            WorkspaceNotFoundException: If the pod does not have a workspace label

        Returns:
            V1Pod: The amended pod with volume mounts configured
        """
        metadata: V1ObjectMeta = pod.metadata
        namespace = metadata.namespace
        name = metadata.name
        workspace_name = metadata.labels.get("workspace")

        if not workspace_name:
            raise WorkspaceNotFoundException(namespace, name)

        workspace = await self.workspace_client.get(namespace, workspace_name)

        storage_name: str = f"{storage_prefix}{workspace_name}"

        if workspace.status.persistent_volume_claim:
            storage_name = workspace.status.persistent_volume_claim

        if workspace.spec.jupyter_workspace.persistent_volume_claim.name:
            storage_name = workspace.spec.jupyter_workspace.persistent_volume_claim.name

        if workspace.spec.jupyter_workspace.persistent_volume_claim.storage_class_name:
            storage_class_name = workspace.spec.jupyter_workspace.persistent_volume_claim.storage_class_name

        if not mount_path:
            mount_path = f"{mount_prefix}/{workspace_name}"

        amended_pod = await self.pvc_client.mount(  # noqa: F841
            pod=pod,
            storage_name=storage_name,
            namespace=namespace,
            mount_path=mount_path,
            storage_class_name=storage_class_name,
            read_only=read_only,
        )

        update_status: bool = False
        if not workspace.status.persistent_volume_claim:
            workspace.status.persistent_volume_claim = storage_name
            update_status = True

        if workspace.status.status_text != "Provisioned":
            workspace.status.status_text = "Provisioned"
            update_status = True

        if update_status is True:
            await self.workspace_client.patch_status(
                namespace=workspace.metadata.namespace,
                name=workspace.metadata.name,
                status=workspace.status,
            )


class AnalyticsManager:
    """
    A high level manager for both workspace and datasource operations.

    Provides unified access to both AnalyticsWorkspaceManager and
    AnalyticsDataSourceManager through a single interface.

    Attributes:
        workspace (AnalyticsWorkspaceManager): Manager for workspace operations
        datasource (AnalyticsDataSourceManager): Manager for datasource operations
    """

    def __init__(
        self,
        api_client: ApiClient,
        log: Logger,
        reporting_controller: str = "xlscsde.nhs.uk/unspecified-controller",
        reporting_user="Unknown User",
    ):
        """
        Initialize the AnalyticsManager.

        Args:
            api_client (ApiClient): Kubernetes API client
            log (Logger): Logger instance
            reporting_controller (str, optional): Controller name for event reporting.
                Defaults to "xlscsde.nhs.uk/unspecified-controller".
            reporting_user (str, optional): User name for event reporting.
                Defaults to "Unknown User".
        """
        self.workspace = AnalyticsWorkspaceManager(
            api_client, log, reporting_controller, reporting_user
        )
        self.datasource = AnalyticsDataSourceManager(
            api_client, log, reporting_controller, reporting_user
        )
