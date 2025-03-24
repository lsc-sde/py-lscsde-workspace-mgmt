# Kubernetes Custom Resources

This document describes the Kubernetes custom resources used by the `lscsde-workspace-mgmt` module.

## AnalyticsWorkspace

Represents a workspace environment for analytics activities.

### Example

```yaml
apiVersion: xlscsde.nhs.uk/v1
kind: AnalyticsWorkspace
metadata:
  name: sample-workspace
  namespace: default
spec:
  displayName: "Sample Analytics Workspace"
  description: "A workspace for data analysis and visualization"
  validity:
    availableFrom: "2023-01-01T00:00:00Z"
    expires: "2023-12-31T23:59:59Z"
  jupyterWorkspace:
    image: "jupyter/datascience-notebook:latest"
    defaultUri: "/lab"
    resources:
      requests:
        memory: "2Gi"
        cpu: "1"
      limits:
        memory: "4Gi"
        cpu: "2"
    persistentVolumeClaim:
      storageClassName: "standard"
```

## AnalyticsWorkspaceBinding

Connects users to workspaces with time-limited access.

### Example

```yaml
apiVersion: xlscsde.nhs.uk/v1
kind: AnalyticsWorkspaceBinding
metadata:
  name: user1-workspace-binding
  namespace: default
spec:
  workspace: "sample-workspace"
  username: "user1@example.com"
  expires: "2023-12-31T23:59:59Z"
  comments: "Standard user access for project XYZ"
```

## AnalyticsDataSource

Represents a data source that can be accessed within workspaces.

### Example

```yaml
apiVersion: xlscsde.nhs.uk/v1
kind: AnalyticsDataSource
metadata:
  name: example-dataset
  namespace: default
  labels:
    xlscsde.nhs.uk/type: "uploaded"
spec:
  type: "Uploaded"
  displayName: "Example Dataset"
  description: "An example dataset containing sample data for analysis"
  license: "This sample data may ONLY be used for demos"
  project:
    id: "project-123"
  publisher:
    organisation: "Example Organisation"
    contact:
      name: "Data Admin"
      role: "Data Steward"
  connections:
    - name: "example-connection"
      type: "pvc"
      databricksConnection:
        hostName: "databricks.example.com"
        httpPath: "/api/2.0/sql/statements"
        personalAccessToken:
          secretName: "databricks-token"
          secretKey: "TOKEN"
```

## AnalyticsDataSourceBinding

Connects data sources to workspaces with time-limited access.

### Example

```yaml
apiVersion: xlscsde.nhs.uk/v1
kind: AnalyticsDataSourceBinding
metadata:
  name: workspace-dataset-binding
  namespace: default
spec:
  workspace: "sample-workspace"
  datasource: "example-dataset"
  expires: "2023-12-31T23:59:59Z"
  comments: "Data access for project XYZ"
```

## AnalyticsCrate

Represents a crate of code/data that can be associated with a workspace.

### Example

```yaml
apiVersion: xlscsde.nhs.uk/v1
kind: AnalyticsCrate
metadata:
  name: example-crate
  namespace: default
spec:
  displayName: "Example Analysis Crate"
  description: "A research analysis crate containing code and metadata"
  path: "/ro-crate-metadata.json"
  repo:
    url: "https://github.com/example/research-crate"
    branch: "main"
    secretName: "github-credentials"
    secretKey: "token"
```
