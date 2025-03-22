"""
lscsde-workspace-mgmt
=====================

A Python module for managing analytics workspaces and data sources in Kubernetes.

This package provides a set of clients and managers for interacting with
custom Kubernetes resources related to analytics workspaces and data sources.

Main Components:
---------------

Workspace Management:
    - AnalyticsWorkspaceClient: Client for AnalyticsWorkspace resources
    - AnalyticsWorkspaceBindingClient: Client for AnalyticsWorkspaceBinding resources
    - AnalyticsWorkspaceManager: High-level manager for workspace operations

Data Source Management:
    - AnalyticsDataSourceClient: Client for AnalyticsDataSource resources
    - AnalyticsDataSourceBindingClient: Client for AnalyticsDataSourceBinding resources
    - AnalyticsDataSourceManager: High-level manager for data source operations

Utilities:
    - EventClient: Records Kubernetes events for tracking resource changes
    - KubernetesNamespacedCustomClient: Base class for custom resource clients
"""

# Version information
__version__ = "0.1.0"

# Expose main components
from .workspaceclient import AnalyticsWorkspaceClient
from .workspacebindingclient import AnalyticsWorkspaceBindingClient
from .datasourceclient import AnalyticsDataSourceClient
from .datasourcebindingclient import AnalyticsDataSourceBindingClient
from .managers import (
    AnalyticsWorkspaceManager,
    AnalyticsDataSourceManager,
    AnalyticsManager,
)
from .eventclient import EventClient
from .exceptions import (
    WorkspaceNotFoundException,
    InvalidParameterException,
    InvalidLabelFormatException,
)

__all__ = [
    "AnalyticsWorkspaceClient",
    "AnalyticsWorkspaceBindingClient",
    "AnalyticsDataSourceClient",
    "AnalyticsDataSourceBindingClient",
    "AnalyticsWorkspaceManager",
    "AnalyticsDataSourceManager",
    "AnalyticsManager",
    "EventClient",
    "WorkspaceNotFoundException",
    "InvalidParameterException",
    "InvalidLabelFormatException",
]
