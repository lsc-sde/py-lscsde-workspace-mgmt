# lscsde-workspace-mgmt

A Python module for managing analytics workspaces and data sources in Kubernetes.

## Overview

The `lscsde-workspace-mgmt` module provides a comprehensive set of classes and utilities for interacting with custom Kubernetes resources related to analytics workspaces and data sources. It enables programmatic management of workspaces, workspace bindings, data sources, and data source bindings within a Kubernetes cluster.

This package is designed to simplify the creation, management, and access control of analytics environments in Kubernetes using custom resource definitions (CRDs).

## Installation

```bash
pip install lscsde-workspace-mgmt
```

## Core Components

### Workspace Management

- **AnalyticsWorkspaceClient**: Manages AnalyticsWorkspace resources in Kubernetes, handling CRUD operations and specialized queries
- **AnalyticsWorkspaceBindingClient**: Manages AnalyticsWorkspaceBinding resources that connect users to workspaces with expiration dates
- **AnalyticsWorkspaceManager**: High-level manager that coordinates operations between workspaces, bindings, and persistent volume claims

### Data Source Management

- **AnalyticsDataSourceClient**: Manages AnalyticsDataSource resources in Kubernetes
- **AnalyticsDataSourceBindingClient**: Manages AnalyticsDataSourceBinding resources that connect workspaces to data sources
- **AnalyticsDataSourceManager**: High-level manager for data source operations

### Utilities

- **EventClient**: Records Kubernetes events for tracking resource changes and operations
- **KubernetesNamespacedCustomClient**: Base class providing common functionality for interacting with namespaced custom resources
- **PersistentVolumeClaimClient**: Manages PVCs associated with workspaces and handles volume mounting

## Custom Resources Overview

### AnalyticsWorkspace

Represents a workspace environment that users can access for analytics activities:
- **Metadata**: Name, namespace, and labels
- **Spec**: Configuration including display name, description, Jupyter settings, and validity period
- **Status**: Current state of the workspace, including provisioning status and PVC information

### AnalyticsWorkspaceBinding

Creates a relationship between users and workspaces:
- **Username-based access control**: Maps specific users to workspaces
- **Expiration dates**: Controls access duration independently from workspace lifecycle
- **Labels**: Automatically adds username labels for efficient filtering

### AnalyticsDataSource

Defines data sources that can be connected to workspaces:
- Connection information
- Metadata including publisher and approval status
- Access control parameters

### AnalyticsDataSourceBinding

Connects data sources to specific workspaces:
- Workspace association
- Access duration control
- Mounting configurations

## Key Features

- **User-based workspace access**: Retrieve and manage workspaces a specific user has access to
- **Expiration management**: Handle expiry dates at both workspace and binding levels
- **Volume management**: Automatically provision and mount persistent volumes for workspaces
- **Event recording**: Track important operations on resources with Kubernetes events
- **Status management**: Update and track the status of resources through their lifecycle

## Usage Examples

### Creating a Workspace Manager

```python
from lscsde_workspace_mgmt import AnalyticsManager
from kubernetes_asyncio import client, config
import logging

# Setup logging
log = logging.getLogger("workspace-example")
log.setLevel(logging.INFO)

# Create Kubernetes client and manager
async def create_manager():
    await config.load_kube_config()
    api_client = client.ApiClient()
    
    # Create analytics manager that provides access to both workspace and datasource managers
    manager = AnalyticsManager(
        api_client=api_client,
        log=log,
        reporting_controller="example-controller",
        reporting_user="example-user"
    )
    return manager
```

### Getting Workspaces for a User

```python
async def get_user_workspaces(manager, namespace, username):
    # Get permitted workspaces in a format suitable for displaying to users
    workspaces = await manager.workspace.get_permitted_workspaces(
        namespace=namespace,
        username=username
    )
    
    # Each workspace includes displayName, expiration, and days remaining
    for workspace in workspaces:
        print(f"Workspace: {workspace['display_name']}")
        print(f"Expires: {workspace['end_date']}")
        print(f"Days remaining: {workspace['ws_days_left'].days}")
        print("---")
    
    return workspaces
```

### Creating a Workspace

```python
from lscsde_workspace_mgmt.objects import AnalyticsWorkspace
from kubernetes_asyncio import client

async def create_workspace(manager, namespace, name, display_name, image):
    # Create workspace metadata
    metadata = client.V1ObjectMeta(
        name=name,
        namespace=namespace
    )
    
    # Create a workspace object
    workspace = AnalyticsWorkspace(
        api_version="xlscsde.nhs.uk/v1",
        kind="AnalyticsWorkspace",
        metadata=metadata,
        spec={
            "displayName": display_name,
            "description": "Example workspace created programmatically",
            "jupyterWorkspace": {
                "image": image
            },
            "validity": {
                "availableFrom": "2023-01-01",
                "expires": "2024-12-31"
            }
        }
    )
    
    # Create the workspace in Kubernetes
    created_workspace = await manager.workspace.workspace_client.create(workspace)
    return created_workspace
```

### Mounting a Workspace Volume to a Pod

```python
from kubernetes_asyncio.client import V1Pod, V1ObjectMeta

async def mount_workspace_volume(manager, namespace, pod_name, workspace_name):
    # Create a pod that will use the workspace
    pod = V1Pod(
        metadata=V1ObjectMeta(
            name=pod_name,
            namespace=namespace,
            labels={"workspace": workspace_name}  # This label connects pod to workspace
        )
    )
    
    # Mount the workspace volume to the pod
    amended_pod = await manager.workspace.mount_workspace(
        pod=pod,
        storage_class_name="standard",
        mount_prefix="/home/jovyan/work",
        storage_prefix="workspace-"
    )
    
    return amended_pod
```

## Error Handling

The package provides several exception classes to handle specific error scenarios:

- **WorkspaceNotFoundException**: When a pod is missing a workspace label
- **InvalidParameterException**: When required parameters are missing or invalid
- **InvalidLabelFormatException**: When label formats are incorrect
- **NoAssignedValidWorkspaces**: When a user has no valid workspaces assigned

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Developer Instructions
### Incrementing the version
The version of this package is located in the following file:
[/src/lscsde_workspace_mgmt/_version.py](./src/lscsde_workspace_mgmt/_version.py)

Please increment this before building.

### Building
```bash
python3 -m build
```

### Publishing built artifacts to pypi
```bash
python -m twine upload --repository pypi dist/*
```