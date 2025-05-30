# API Reference

The `lscsde-workspace-mgmt` library provides several modules for interacting with Kubernetes custom resources:

## Core Components

- **Models**: Pydantic models representing the various Kubernetes custom resources
- **Clients**: Classes for interacting with the Kubernetes API for each resource type
- **Managers**: Higher-level interfaces for managing resources and their relationships
- **Converters**: Tools for converting resources to other formats (e.g., KubeSpawner configuration)

## Module Structure

- [Models](models.md): Data models for all resources
- [Workspace Client](workspaceclient.md): Client for AnalyticsWorkspace resources
- [Workspace Binding Client](workspacebindingclient.md): Client for AnalyticsWorkspaceBinding resources  
- [Data Source Client](datasourceclient.md): Client for AnalyticsDataSource resources
- [Data Source Binding Client](datasourcebindingclient.md): Client for AnalyticsDataSourceBinding resources
- [Persistent Volume Claim Client](pvclient.md): Client for managing PVCs
- [Event Client](eventclient.md): Client for Kubernetes events
- [Managers](managers.md): Higher-level resource managers
- [Exceptions](exceptions.md): Custom exceptions
- [Object Converters](objects.md): Conversion utilities
