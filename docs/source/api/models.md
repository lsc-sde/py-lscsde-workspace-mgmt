# Models

The `lscsde_workspace_mgmt.models` module provides Pydantic models representing Kubernetes resources.

## KubernetesHelper

```python
class KubernetesHelper
```

A helper class for interacting with Kubernetes.

### Methods

#### format_as_label

```python
def format_as_label(username: str) -> str
```

Reformats a string to make it compatible for use in a Kubernetes label field.

**Parameters:**
- `username` (str): The username to format

**Returns:**
- String formatted for use as a Kubernetes label

**Raises:**
- `InvalidLabelFormatException`: If the formatted string doesn't meet Kubernetes label requirements

## Kubernetes Resources

### KubernetesMetadata

```python
class KubernetesMetadata(BaseModel)
```

Represents standard Kubernetes metadata.

**Fields:**
- `name` (Optional[str]): Name of the resource
- `namespace` (Optional[str]): Namespace that the resource is deployed to
- `annotations` (Optional[dict[str, str]]): Dictionary of annotations
- `labels` (Optional[dict[str, str]]): Dictionary of labels
- `resource_version` (Optional[str]): Version of the resource

### AnalyticsWorkspace

```python
class AnalyticsWorkspace(BaseModel)
```

Represents an AnalyticsWorkspace resource.

**Fields:**
- `api_version` (Optional[str]): The API Version in Kubernetes
- `kind` (Optional[str]): The Kind of object
- `metadata` (Optional[KubernetesMetadata]): The resource metadata
- `spec` (Optional[AnalyticsWorkspaceSpec]): The workspace specification
- `status` (Optional[AnalyticsWorkspaceStatus]): The workspace status

### AnalyticsWorkspaceBinding

```python
class AnalyticsWorkspaceBinding(BaseModel)
```

Represents an AnalyticsWorkspaceBinding object.

**Fields:**
- `api_version` (Optional[str]): The API Version in Kubernetes
- `kind` (Optional[str]): The Kind of object
- `metadata` (Optional[KubernetesMetadata]): The resource metadata
- `spec` (Optional[AnalyticsWorkspaceBindingSpec]): The binding specification
- `status` (Optional[AnalyticsWorkspaceBindingStatus]): The binding status

### AnalyticsDataSource

```python
class AnalyticsDataSource(BaseModel)
```

Represents the AnalyticsDataSource Resource.

**Fields:**
- `api_version` (Optional[str]): The API Version in Kubernetes
- `kind` (Optional[str]): The Kind of object
- `metadata` (Optional[KubernetesMetadata]): The resource metadata
- `spec` (Optional[AnalyticsDataSourceSpec]): The specification
- `status` (Optional[AnalyticsDataSourceStatus]): The status

### AnalyticsDataSourceBinding

```python
class AnalyticsDataSourceBinding(BaseModel)
```

Represents the AnalyticsDataSourceBinding resource.

**Fields:**
- `api_version` (Optional[str]): The API Version in Kubernetes
- `kind` (Optional[str]): The Kind of object
- `metadata` (Optional[KubernetesMetadata]): The resource metadata
- `spec` (Optional[AnalyticsDataSourceBindingSpec]): The specification
- `status` (Optional[AnalyticsDataSourceBindingStatus]): The status

### AnalyticsCrate

```python
class AnalyticsCrate(BaseModel)
```

Represents an AnalyticsCrate resource.

**Fields:**
- `api_version` (Optional[str]): The API Version in Kubernetes
- `kind` (Optional[str]): The Kind of object
- `metadata` (Optional[KubernetesMetadata]): The resource metadata
- `spec` (Optional[AnalyticsCrateSpec]): The specification
- `status` (Optional[AnalyticsCrateStatus]): The status

## Workspace Components

The module also includes numerous component models that make up the fields of the main resources, such as:

- `AnalyticsWorkspaceValidity`
- `VirtualMachineWorkspaceSpec`
- `JupyterWorkspaceStorage`
- `JupyterWorkspaceSpec`
- `AnalyticsWorkspaceStatus`
- And many more

See the full API documentation for details on all component models.
