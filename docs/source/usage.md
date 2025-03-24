# Usage

Here are examples of common use cases for the `lscsde-workspace-mgmt` library.

## Initialize the API Client

```python
from kubernetes_asyncio.config import load_kube_config
from kubernetes_asyncio.client import ApiClient, CustomObjectsApi
import asyncio
from logging import getLogger

# Create a logger
logger = getLogger("example")

async def init_client():
    # Load Kubernetes configuration
    await load_kube_config()
    # Create API client
    api_client = ApiClient()
    return api_client

# Run in an async context
api_client = asyncio.run(init_client())
```

## Working with Analytics Workspaces

```python
from lscsde_workspace_mgmt.workspaceclient import AnalyticsWorkspaceClient
from lscsde_workspace_mgmt.eventclient import EventClient
from lscsde_workspace_mgmt.models import AnalyticsWorkspace

async def workspace_example(api_client):
    custom_objects_api = CustomObjectsApi(api_client=api_client)
    event_client = EventClient(api_client=api_client, log=logger)
    
    # Create workspace client
    client = AnalyticsWorkspaceClient(
        k8s_api=custom_objects_api, 
        log=logger, 
        event_client=event_client
    )
    
    # Get a workspace
    workspace = await client.get("default", "example-workspace")
    
    # List workspaces
    workspaces = await client.list("default")
    
    # Create a workspace
    new_workspace = AnalyticsWorkspace(
        metadata={"name": "new-workspace", "namespace": "default"},
        spec={
            "displayName": "New Workspace",
            "description": "A new workspace created via the API"
        }
    )
    created = await client.create(new_workspace)
```

## Using the Workspace Manager

```python
from lscsde_workspace_mgmt.managers import AnalyticsWorkspaceManager

async def manager_example(api_client):
    # Create workspace manager
    manager = AnalyticsWorkspaceManager(api_client=api_client, log=logger)
    
    # Get workspaces for a user
    user_workspaces = await manager.get_permitted_workspaces(
        namespace="default",
        username="user@example.com"
    )
    
    # Mount workspaces to a pod
    from kubernetes_asyncio.client import V1Pod
    pod = V1Pod()  # Define your pod
    
    # Mount workspace volumes to the pod
    updated_pod = await manager.mount_workspace(
        pod=pod,
        storage_class_name="standard",
        mount_prefix="/mnt/data"
    )
```

For more detailed examples, see the API reference for each module.
