# API Documentation

This document describes the API for the `lscsde-workspace-mgmt` module.

## Clients

### AnalyticsWorkspaceClient

A client for interacting with AnalyticsWorkspace resources in Kubernetes.

#### Methods

- `get(namespace, name)`: Retrieves a specific AnalyticsWorkspace
- `list(namespace, **kwargs)`: Lists AnalyticsWorkspace resources in a namespace
- `list_by_username(binding_client, namespace, username)`: Lists workspaces accessible to a specific user
- `create(body)`: Creates an AnalyticsWorkspace
- `patch(namespace, name, patch_body, body)`: Updates an AnalyticsWorkspace
- `patch_status(namespace, name, status)`: Updates just the status of an AnalyticsWorkspace
- `replace(body)`: Replaces an AnalyticsWorkspace
- `delete(body, namespace, name)`: Deletes an AnalyticsWorkspace

### AnalyticsWorkspaceBindingClient

A client for interacting with AnalyticsWorkspaceBinding resources that connect users to workspaces.

#### Methods

- `get(namespace, name)`: Retrieves a specific binding
- `list(namespace, **kwargs)`: Lists bindings in a namespace
- `list_by_username(namespace, username)`: Lists bindings for a specific user
- `create(body, append_label)`: Creates a binding
- `patch(namespace, name, patch_body, body)`: Updates a binding
- `patch_status(namespace, name, status)`: Updates just the status of a binding
- `replace(body, append_label)`: Replaces a binding
- `delete(body, namespace, name)`: Deletes a binding

### AnalyticsDataSourceClient

A client for interacting with AnalyticsDataSource resources in Kubernetes.

#### Methods

- `get(namespace, name)`: Retrieves a specific data source
- `list(namespace, **kwargs)`: Lists data sources in a namespace
- `list_by_workspace(binding_client, namespace, workspace)`: Lists data sources accessible to a specific workspace
- `create(body)`: Creates a data source
- `patch(namespace, name, patch_body, body)`: Updates a data source
- `patch_status(namespace, name, status)`: Updates just the status of a data source
- `replace(body)`: Replaces a data source
- `delete(body, namespace, name)`: Deletes a data source

### AnalyticsDataSourceBindingClient

A client for interacting with AnalyticsDataSourceBinding resources that connect workspaces to data sources.

#### Methods

- `get(namespace, name)`: Retrieves a specific binding
- `list(namespace, **kwargs)`: Lists bindings in a namespace
- `list_by_workspace(namespace, workspace)`: Lists bindings for a specific workspace
- `create(body, append_label)`: Creates a binding
- `patch(namespace, name, patch_body, body)`: Updates a binding
- `patch_status(namespace, name, status)`: Updates just the status of a binding
- `replace(body, append_label)`: Replaces a binding
- `delete(body, namespace, name)`: Deletes a binding

## Managers

### AnalyticsWorkspaceManager

A high-level manager for working with AnalyticsWorkspace resources.

#### Methods

- `get_workspaces_for_user(namespace, username)`: Gets all workspaces available to a user
- `get_permitted_workspaces(namespace, username, date_now)`: Gets permitted workspaces as a dictionary
- `mount_workspace(pod, storage_class_name, mount_prefix, storage_prefix, read_only, mount_path)`: Mounts workspace storage to a pod

### AnalyticsDataSourceManager

A high-level manager for working with AnalyticsDataSource resources.

## EventClient

Records Kubernetes events for tracking changes to resources.

#### Methods

- `WorkspaceCreated(workspace, note)`: Records a workspace creation event
- `WorkspaceUpdated(workspace, note)`: Records a workspace update event
- `WorkspaceDeleted(workspace, note)`: Records a workspace deletion event
- `WorkspaceBindingCreated(binding, note)`: Records a workspace binding creation event
- `WorkspaceBindingUpdated(binding, note)`: Records a workspace binding update event
- `WorkspaceBindingDeleted(binding, note)`: Records a workspace binding deletion event
- `DataSourceCreated(datasource, note)`: Records a data source creation event
- `DataSourceUpdated(datasource, note)`: Records a data source update event
- `DataSourceDeleted(datasource, note)`: Records a data source deletion event
- `DataSourceBindingCreated(binding, note)`: Records a data source binding creation event
- `DataSourceBindingUpdated(binding, note)`: Records a data source binding update event
- `DataSourceBindingDeleted(binding, note)`: Records a data source binding deletion event

## Models

The module defines several Pydantic models that represent Kubernetes resources:

- `AnalyticsWorkspace`: Represents a workspace for analytics activities
- `AnalyticsWorkspaceBinding`: Connects users to workspaces
- `AnalyticsDataSource`: Represents a data source
- `AnalyticsDataSourceBinding`: Connects data sources to workspaces
- `AnalyticsCrate`: Represents an analytics crate resource
