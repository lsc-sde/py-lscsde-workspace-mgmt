# Workspace Client

The `lscsde_workspace_mgmt.workspaceclient` module provides a client for interacting with AnalyticsWorkspace resources in Kubernetes.

## AnalyticsWorkspaceClient

```python
class AnalyticsWorkspaceClient(KubernetesNamespacedCustomClient)
```

Client for interacting with AnalyticsWorkspaces.

### Constructor

```python
def __init__(self, k8s_api: CustomObjectsApi, log: Logger, event_client: EventClient)
```

**Parameters:**
- `k8s_api` (CustomObjectsApi): The Kubernetes custom objects API client
- `log` (Logger): Logger for the client
- `event_client` (EventClient): Client for creating Kubernetes events

### Methods

#### get

```python
async def get(self, namespace: str, name: str) -> AnalyticsWorkspace
```

Gets a specific AnalyticsWorkspace resource.

**Parameters:**
- `namespace` (str): The namespace containing the resource
- `name` (str): The name of the resource

**Returns:**
- `AnalyticsWorkspace`: The requested workspace

#### list

```python
async def list(self, namespace: str, **kwargs) -> list[AnalyticsWorkspace]
```

Lists AnalyticsWorkspace resources in the namespace supplied.

**Parameters:**
- `namespace` (str): The namespace to list resources from
- `**kwargs`: Additional parameters to pass to the Kubernetes API

**Returns:**
- `list[AnalyticsWorkspace]`: List of workspaces

#### list_by_username

```python
async def list_by_username(
    self, 
    binding_client: AnalyticsWorkspaceBindingClient,
    namespace: str, 
    username: str
) -> list[AnalyticsWorkspace]
```

Lists AnalyticsWorkspace resources in the namespace supplied that match the username.

**Parameters:**
- `binding_client` (AnalyticsWorkspaceBindingClient): Client for workspace bindings
- `namespace` (str): The namespace to search in
- `username` (str): The username to match

**Returns:**
- `list[AnalyticsWorkspace]`: List of workspaces matching the username

#### create

```python
async def create(self, body: AnalyticsWorkspace) -> AnalyticsWorkspace
```

Creates a AnalyticsWorkspace resource in the namespace supplied.

**Parameters:**
- `body` (AnalyticsWorkspace): The workspace to create

**Returns:**
- `AnalyticsWorkspace`: The created workspace

#### patch

```python
async def patch(
    self, 
    namespace: str = None,
    name: str = None,
    patch_body: dict = None,
    body: AnalyticsWorkspace = None
) -> AnalyticsWorkspace
```

Patches a AnalyticsWorkspace resource in the namespace supplied.

**Parameters:**
- `namespace` (str, optional): The namespace containing the resource
- `name` (str, optional): The name of the resource
- `patch_body` (dict, optional): The patch body to apply
- `body` (AnalyticsWorkspace, optional): The workspace object with updates

**Returns:**
- `AnalyticsWorkspace`: The patched workspace

#### patch_status

```python
async def patch_status(
    self, 
    namespace: str, 
    name: str,
    status: AnalyticsWorkspaceStatus
) -> AnalyticsWorkspace
```

Patches the status of an AnalyticsWorkspace resource in the namespace supplied.

**Parameters:**
- `namespace` (str): The namespace containing the resource
- `name` (str): The name of the resource
- `status` (AnalyticsWorkspaceStatus): The new status to apply

**Returns:**
- `AnalyticsWorkspace`: The updated workspace

#### replace

```python
async def replace(self, body: AnalyticsWorkspace) -> AnalyticsWorkspace
```

Replaces a AnalyticsWorkspace resource with the one supplied.

**Parameters:**
- `body` (AnalyticsWorkspace): The replacement workspace

**Returns:**
- `AnalyticsWorkspace`: The replaced workspace

#### delete

```python
async def delete(
    self,
    body: AnalyticsWorkspace = None,
    namespace: str = None,
    name: str = None
) -> AnalyticsWorkspace
```

Deletes a AnalyticsWorkspace resource in the namespace supplied.

**Parameters:**
- `body` (AnalyticsWorkspace, optional): The workspace to delete
- `namespace` (str, optional): The namespace containing the resource
- `name` (str, optional): The name of the resource to delete

**Returns:**
- `AnalyticsWorkspace`: The deleted workspace

## Example Usage

```python
# Initialize the client
api_client = ApiClient()
custom_objects_api = CustomObjectsApi(api_client=api_client)
event_client = EventClient(api_client=api_client, log=logger)
workspace_client = AnalyticsWorkspaceClient(
    k8s_api=custom_objects_api, 
    log=logger, 
    event_client=event_client
)

# Get a workspace
workspace = await workspace_client.get("default", "my-workspace")

# Update the workspace
workspace.spec.display_name = "New Display Name"
updated_workspace = await workspace_client.patch(body=workspace)
```
