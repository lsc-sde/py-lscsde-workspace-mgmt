---
title: Python Module
layout: page
parent: Analytics Workspace Management Services
grand_parent: Architecture
---
The repository defines python modules for Analytics Workspace Management is located at [https://github.com/lsc-sde/py-lscsde-workspace-mgmt](https://github.com/lsc-sde/py-lscsde-workspace-mgmt)

This library produces models based on the custom resource definitions for:
* [AnalyticsCrates](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsCrates.md)
* [AnalyticsDataSources](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsDataSources.md)
* [AnalyticsDataSourceBindings](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsDataSourceBindings.md)
* [AnalyticsWorkspaces](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.md)
* [AnalyticsWorkspaceBindings](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaceBindings.md)

Clients are then provided which allow services to interact with the various objects via the kubernetes API's. 

Additionally there are also converters which will provide conversion from pytest to other object types such as kubespawner override blocks.

# Used by
The python library is used by:
* [The SDE customised jupyter hub image](../../../docker/jupyterhub/docs/image.md)
* [The AWMS Guacamole Operator](../../../products/sde/analytics-workspace-management/awms-guacamole-operator/docs/operator.md)
* [The AMWS Datasource Operator](../../../products/sde/analytics-datasource-management/awms-datasource-operator/docs/operator.md)
* [The AWMS Crate Operator](../../../products/sde/analytics-datasource-management/awms-crate-operator/docs/operator.md)

# Code Documentation

* [lscsde\_workspace\_mgmt](#lscsde_workspace_mgmt)
* [lscsde\_workspace\_mgmt.datasourcebindingclient](#lscsde_workspace_mgmt.datasourcebindingclient)
  * [AnalyticsDataSourceBindingClient](#lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient)
    * [get](#lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.get)
    * [list](#lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.list)
    * [list\_by\_workspace](#lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.list_by_workspace)
    * [create](#lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.create)
    * [patch](#lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.patch)
    * [patch\_status](#lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.patch_status)
    * [replace](#lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.replace)
    * [delete](#lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.delete)
* [lscsde\_workspace\_mgmt.k8sio](#lscsde_workspace_mgmt.k8sio)
* [lscsde\_workspace\_mgmt.eventclient](#lscsde_workspace_mgmt.eventclient)
  * [EventClient](#lscsde_workspace_mgmt.eventclient.EventClient)
    * [RegisterWorkspaceEvent](#lscsde_workspace_mgmt.eventclient.EventClient.RegisterWorkspaceEvent)
    * [RegisterWorkspaceBindingEvent](#lscsde_workspace_mgmt.eventclient.EventClient.RegisterWorkspaceBindingEvent)
    * [RegisterDataSourceEvent](#lscsde_workspace_mgmt.eventclient.EventClient.RegisterDataSourceEvent)
    * [RegisterDataSourceBindingEvent](#lscsde_workspace_mgmt.eventclient.EventClient.RegisterDataSourceBindingEvent)
    * [WorkspaceCreated](#lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceCreated)
    * [WorkspaceUpdated](#lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceUpdated)
    * [WorkspaceDeleted](#lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceDeleted)
    * [WorkspaceBindingCreated](#lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceBindingCreated)
    * [WorkspaceBindingUpdated](#lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceBindingUpdated)
    * [WorkspaceBindingDeleted](#lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceBindingDeleted)
    * [DataSourceCreated](#lscsde_workspace_mgmt.eventclient.EventClient.DataSourceCreated)
    * [DataSourceUpdated](#lscsde_workspace_mgmt.eventclient.EventClient.DataSourceUpdated)
    * [DataSourceDeleted](#lscsde_workspace_mgmt.eventclient.EventClient.DataSourceDeleted)
    * [DataSourceBindingCreated](#lscsde_workspace_mgmt.eventclient.EventClient.DataSourceBindingCreated)
    * [DataSourceBindingUpdated](#lscsde_workspace_mgmt.eventclient.EventClient.DataSourceBindingUpdated)
    * [DataSourceBindingDeleted](#lscsde_workspace_mgmt.eventclient.EventClient.DataSourceBindingDeleted)
* [lscsde\_workspace\_mgmt.exceptions](#lscsde_workspace_mgmt.exceptions)
  * [NoAssignedValidWorkspaces](#lscsde_workspace_mgmt.exceptions.NoAssignedValidWorkspaces)
  * [WorkspaceNotFoundException](#lscsde_workspace_mgmt.exceptions.WorkspaceNotFoundException)
* [lscsde\_workspace\_mgmt.workspaceclient](#lscsde_workspace_mgmt.workspaceclient)
  * [AnalyticsWorkspaceClient](#lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient)
    * [get](#lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.get)
    * [list](#lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.list)
    * [list\_by\_username](#lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.list_by_username)
    * [create](#lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.create)
    * [patch](#lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.patch)
    * [patch\_status](#lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.patch_status)
    * [replace](#lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.replace)
    * [delete](#lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.delete)
* [lscsde\_workspace\_mgmt.pvclient](#lscsde_workspace_mgmt.pvclient)
  * [PersistentVolumeClaimClient](#lscsde_workspace_mgmt.pvclient.PersistentVolumeClaimClient)
    * [get](#lscsde_workspace_mgmt.pvclient.PersistentVolumeClaimClient.get)
    * [create\_if\_not\_exists](#lscsde_workspace_mgmt.pvclient.PersistentVolumeClaimClient.create_if_not_exists)
    * [mount](#lscsde_workspace_mgmt.pvclient.PersistentVolumeClaimClient.mount)
* [lscsde\_workspace\_mgmt.managers](#lscsde_workspace_mgmt.managers)
  * [AnalyticsDataSourceManager](#lscsde_workspace_mgmt.managers.AnalyticsDataSourceManager)
  * [AnalyticsWorkspaceManager](#lscsde_workspace_mgmt.managers.AnalyticsWorkspaceManager)
    * [get\_workspaces\_for\_user](#lscsde_workspace_mgmt.managers.AnalyticsWorkspaceManager.get_workspaces_for_user)
    * [get\_permitted\_workspaces](#lscsde_workspace_mgmt.managers.AnalyticsWorkspaceManager.get_permitted_workspaces)
    * [mount\_workspace](#lscsde_workspace_mgmt.managers.AnalyticsWorkspaceManager.mount_workspace)
  * [AnalyticsManager](#lscsde_workspace_mgmt.managers.AnalyticsManager)
* [lscsde\_workspace\_mgmt.namespacedclient](#lscsde_workspace_mgmt.namespacedclient)
  * [KubernetesNamespacedCustomClient](#lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient)
    * [get\_api\_version](#lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.get_api_version)
    * [get](#lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.get)
    * [list](#lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.list)
    * [patch](#lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.patch)
    * [patch\_status](#lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.patch_status)
    * [replace](#lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.replace)
    * [create](#lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.create)
    * [delete](#lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.delete)
* [lscsde\_workspace\_mgmt.objects](#lscsde_workspace_mgmt.objects)
  * [AnalyticsWorkspaceConverter](#lscsde_workspace_mgmt.objects.AnalyticsWorkspaceConverter)
    * [days\_until\_expiry](#lscsde_workspace_mgmt.objects.AnalyticsWorkspaceConverter.days_until_expiry)
    * [to\_workspace\_dict](#lscsde_workspace_mgmt.objects.AnalyticsWorkspaceConverter.to_workspace_dict)
* [lscsde\_workspace\_mgmt.\_version](#lscsde_workspace_mgmt._version)
* [lscsde\_workspace\_mgmt.datasourceclient](#lscsde_workspace_mgmt.datasourceclient)
  * [AnalyticsDataSourceClient](#lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient)
    * [get](#lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.get)
    * [list](#lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.list)
    * [list\_by\_workspace](#lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.list_by_workspace)
    * [create](#lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.create)
    * [patch](#lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.patch)
    * [patch\_status](#lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.patch_status)
    * [replace](#lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.replace)
    * [delete](#lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.delete)
* [lscsde\_workspace\_mgmt.models](#lscsde_workspace_mgmt.models)
  * [KubernetesHelper](#lscsde_workspace_mgmt.models.KubernetesHelper)
    * [format\_as\_label](#lscsde_workspace_mgmt.models.KubernetesHelper.format_as_label)
  * [KubernetesMetadata](#lscsde_workspace_mgmt.models.KubernetesMetadata)
  * [AnalyticsWorkspaceValidity](#lscsde_workspace_mgmt.models.AnalyticsWorkspaceValidity)
  * [VirtualMachineWorkspaceSpec](#lscsde_workspace_mgmt.models.VirtualMachineWorkspaceSpec)
  * [JupyterWorkspaceStorage](#lscsde_workspace_mgmt.models.JupyterWorkspaceStorage)
  * [JupyterWorkspacePersistentVolumeClaim](#lscsde_workspace_mgmt.models.JupyterWorkspacePersistentVolumeClaim)
  * [JupyterWorkspaceSpecResources](#lscsde_workspace_mgmt.models.JupyterWorkspaceSpecResources)
  * [JupyterWorkspaceSpecNodeSelector](#lscsde_workspace_mgmt.models.JupyterWorkspaceSpecNodeSelector)
  * [JupyterWorkspaceSpecToleration](#lscsde_workspace_mgmt.models.JupyterWorkspaceSpecToleration)
  * [JupyterWorkspaceSpec](#lscsde_workspace_mgmt.models.JupyterWorkspaceSpec)
  * [AnalyticsWorkspaceStatus](#lscsde_workspace_mgmt.models.AnalyticsWorkspaceStatus)
  * [AnalyticsWorkspaceBindingStatus](#lscsde_workspace_mgmt.models.AnalyticsWorkspaceBindingStatus)
  * [AnalyticsWorkspaceSpec](#lscsde_workspace_mgmt.models.AnalyticsWorkspaceSpec)
  * [AnalyticsWorkspaceBindingClaim](#lscsde_workspace_mgmt.models.AnalyticsWorkspaceBindingClaim)
  * [AnalyticsWorkspaceBindingSpec](#lscsde_workspace_mgmt.models.AnalyticsWorkspaceBindingSpec)
    * [username\_as\_label](#lscsde_workspace_mgmt.models.AnalyticsWorkspaceBindingSpec.username_as_label)
  * [AnalyticsWorkspaceBinding](#lscsde_workspace_mgmt.models.AnalyticsWorkspaceBinding)
  * [AnalyticsWorkspace](#lscsde_workspace_mgmt.models.AnalyticsWorkspace)
  * [AnalyticsDataSourcePublisherContact](#lscsde_workspace_mgmt.models.AnalyticsDataSourcePublisherContact)
  * [AnalyticsDataSourcePublisher](#lscsde_workspace_mgmt.models.AnalyticsDataSourcePublisher)
  * [AnalyticsDataSourceProject](#lscsde_workspace_mgmt.models.AnalyticsDataSourceProject)
  * [AnalyticsDataSourceConnectionString](#lscsde_workspace_mgmt.models.AnalyticsDataSourceConnectionString)
  * [AnalyticsDataSourceSecret](#lscsde_workspace_mgmt.models.AnalyticsDataSourceSecret)
  * [AnalyticsDataSourceSecretWithKey](#lscsde_workspace_mgmt.models.AnalyticsDataSourceSecretWithKey)
  * [AnalyticsDataSourceDataBricksConnection](#lscsde_workspace_mgmt.models.AnalyticsDataSourceDataBricksConnection)
  * [AnalyticsApproval](#lscsde_workspace_mgmt.models.AnalyticsApproval)
  * [AnalyticsDataSourceConnection](#lscsde_workspace_mgmt.models.AnalyticsDataSourceConnection)
  * [AnalyticsDataSourceSpec](#lscsde_workspace_mgmt.models.AnalyticsDataSourceSpec)
  * [AnalyticsDataSourceBindingStatus](#lscsde_workspace_mgmt.models.AnalyticsDataSourceBindingStatus)
  * [AnalyticsDataSourceStatus](#lscsde_workspace_mgmt.models.AnalyticsDataSourceStatus)
  * [AnalyticsDataSourceBindingSpec](#lscsde_workspace_mgmt.models.AnalyticsDataSourceBindingSpec)
  * [AnalyticsDataSource](#lscsde_workspace_mgmt.models.AnalyticsDataSource)
  * [AnalyticsDataSourceBinding](#lscsde_workspace_mgmt.models.AnalyticsDataSourceBinding)
  * [AnalyticsCrateSpecRepository](#lscsde_workspace_mgmt.models.AnalyticsCrateSpecRepository)
  * [AnalyticsCrateSpec](#lscsde_workspace_mgmt.models.AnalyticsCrateSpec)
  * [AnalyticsCrateStatus](#lscsde_workspace_mgmt.models.AnalyticsCrateStatus)
  * [AnalyticsCrate](#lscsde_workspace_mgmt.models.AnalyticsCrate)
* [lscsde\_workspace\_mgmt.tests.workspaces](#lscsde_workspace_mgmt.tests.workspaces)
* [lscsde\_workspace\_mgmt.tests.datasources](#lscsde_workspace_mgmt.tests.datasources)
* [lscsde\_workspace\_mgmt.tests.datasourcesbindings](#lscsde_workspace_mgmt.tests.datasourcesbindings)
* [lscsde\_workspace\_mgmt.tests.k8shelper](#lscsde_workspace_mgmt.tests.k8shelper)
* [lscsde\_workspace\_mgmt.tests.workspacebindings](#lscsde_workspace_mgmt.tests.workspacebindings)
* [lscsde\_workspace\_mgmt.integrationtest](#lscsde_workspace_mgmt.integrationtest)
* [lscsde\_workspace\_mgmt.test](#lscsde_workspace_mgmt.test)
* [lscsde\_workspace\_mgmt.workspacebindingclient](#lscsde_workspace_mgmt.workspacebindingclient)
  * [AnalyticsWorkspaceBindingClient](#lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient)
    * [get](#lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.get)
    * [list](#lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.list)
    * [list\_by\_username](#lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.list_by_username)
    * [create](#lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.create)
    * [patch](#lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.patch)
    * [patch\_status](#lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.patch_status)
    * [replace](#lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.replace)
    * [delete](#lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.delete)

<a id="lscsde_workspace_mgmt"></a>

# lscsde\_workspace\_mgmt

<a id="lscsde_workspace_mgmt.datasourcebindingclient"></a>

# lscsde\_workspace\_mgmt.datasourcebindingclient

<a id="lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient"></a>

## AnalyticsDataSourceBindingClient

```python
class AnalyticsDataSourceBindingClient(KubernetesNamespacedCustomClient)
```

This class allows developers to interact with AnalyticsDataSourceBinding objects on kubernetes

<a id="lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets an individual AnalyticsDataSourceBinding

<a id="lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists the AnalyticsDataSourceBindings in a specified namespace

<a id="lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.list_by_workspace"></a>

#### list\_by\_workspace

```python
async def list_by_workspace(namespace, workspace)
```

Lists the AnalyticsDataSourceBindings in a specified namespace which belong to a specific workspace

If a binding does not have the relevant labels defined, the service will assign the label automatically based upon the workspace. 
This makes the query more performant when querying etcd.

<a id="lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.create"></a>

#### create

```python
async def create(body: AnalyticsDataSourceBinding, append_label: bool = True)
```

Creates a AnalyticsDataSourceBinding resource

<a id="lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.patch"></a>

#### patch

```python
async def patch(namespace: str = None,
                name: str = None,
                patch_body: dict = None,
                body: AnalyticsDataSourceBinding = None)
```

Patches a AnalyticsDataSourceBinding resource

<a id="lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str,
                       status: AnalyticsDataSourceBindingStatus)
```

Patches a AnalyticsDataSourceBinding resources status segment

<a id="lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.replace"></a>

#### replace

```python
async def replace(body: AnalyticsDataSourceBinding, append_label: bool = True)
```

Replaces a AnalyticsDataSourceBinding resource with the one provided

<a id="lscsde_workspace_mgmt.datasourcebindingclient.AnalyticsDataSourceBindingClient.delete"></a>

#### delete

```python
async def delete(body: AnalyticsDataSourceBinding = None,
                 namespace: str = None,
                 name: str = None)
```

Deletes a AnalyticsDataSourceBinding resource

<a id="lscsde_workspace_mgmt.k8sio"></a>

# lscsde\_workspace\_mgmt.k8sio

<a id="lscsde_workspace_mgmt.eventclient"></a>

# lscsde\_workspace\_mgmt.eventclient

<a id="lscsde_workspace_mgmt.eventclient.EventClient"></a>

## EventClient

```python
class EventClient()
```

A class for interacting with Events objects in kubernetes

<a id="lscsde_workspace_mgmt.eventclient.EventClient.RegisterWorkspaceEvent"></a>

#### RegisterWorkspaceEvent

```python
async def RegisterWorkspaceEvent(workspace: AnalyticsWorkspace, reason: str,
                                 note: str)
```

Records a workspace event

<a id="lscsde_workspace_mgmt.eventclient.EventClient.RegisterWorkspaceBindingEvent"></a>

#### RegisterWorkspaceBindingEvent

```python
async def RegisterWorkspaceBindingEvent(binding: AnalyticsWorkspaceBinding,
                                        reason: str, note: str)
```

Records a workspace binding event

<a id="lscsde_workspace_mgmt.eventclient.EventClient.RegisterDataSourceEvent"></a>

#### RegisterDataSourceEvent

```python
async def RegisterDataSourceEvent(datasource: AnalyticsDataSource, reason: str,
                                  note: str)
```

Records a datasource event

<a id="lscsde_workspace_mgmt.eventclient.EventClient.RegisterDataSourceBindingEvent"></a>

#### RegisterDataSourceBindingEvent

```python
async def RegisterDataSourceBindingEvent(binding: AnalyticsDataSourceBinding,
                                         reason: str, note: str)
```

Records a datasource binding event

<a id="lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceCreated"></a>

#### WorkspaceCreated

```python
async def WorkspaceCreated(workspace: AnalyticsWorkspace, note: str = None)
```

Records a workspace was created

<a id="lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceUpdated"></a>

#### WorkspaceUpdated

```python
async def WorkspaceUpdated(workspace: AnalyticsWorkspace, note: str = None)
```

Records a workspace was updates

<a id="lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceDeleted"></a>

#### WorkspaceDeleted

```python
async def WorkspaceDeleted(workspace: AnalyticsWorkspace, note: str = None)
```

Records a workspace was deleted

<a id="lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceBindingCreated"></a>

#### WorkspaceBindingCreated

```python
async def WorkspaceBindingCreated(binding: AnalyticsWorkspaceBinding,
                                  note: str = None)
```

Records a workspace binding was created

<a id="lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceBindingUpdated"></a>

#### WorkspaceBindingUpdated

```python
async def WorkspaceBindingUpdated(binding: AnalyticsWorkspaceBinding,
                                  note: str = None)
```

Records a workspace binding was updated

<a id="lscsde_workspace_mgmt.eventclient.EventClient.WorkspaceBindingDeleted"></a>

#### WorkspaceBindingDeleted

```python
async def WorkspaceBindingDeleted(binding: AnalyticsWorkspaceBinding,
                                  note: str = None)
```

Records a workspace binding was deleted

<a id="lscsde_workspace_mgmt.eventclient.EventClient.DataSourceCreated"></a>

#### DataSourceCreated

```python
async def DataSourceCreated(datasource: AnalyticsDataSource, note: str = None)
```

Records a data source was created

<a id="lscsde_workspace_mgmt.eventclient.EventClient.DataSourceUpdated"></a>

#### DataSourceUpdated

```python
async def DataSourceUpdated(datasource: AnalyticsDataSource, note: str = None)
```

Records a data source was updated

<a id="lscsde_workspace_mgmt.eventclient.EventClient.DataSourceDeleted"></a>

#### DataSourceDeleted

```python
async def DataSourceDeleted(datasource: AnalyticsDataSource, note: str = None)
```

Records a data source was deleted

<a id="lscsde_workspace_mgmt.eventclient.EventClient.DataSourceBindingCreated"></a>

#### DataSourceBindingCreated

```python
async def DataSourceBindingCreated(binding: AnalyticsDataSourceBinding,
                                   note: str = None)
```

Records a data source binding was created

<a id="lscsde_workspace_mgmt.eventclient.EventClient.DataSourceBindingUpdated"></a>

#### DataSourceBindingUpdated

```python
async def DataSourceBindingUpdated(binding: AnalyticsDataSourceBinding,
                                   note: str = None)
```

Records a data source binding was updated

<a id="lscsde_workspace_mgmt.eventclient.EventClient.DataSourceBindingDeleted"></a>

#### DataSourceBindingDeleted

```python
async def DataSourceBindingDeleted(binding: AnalyticsDataSourceBinding,
                                   note: str = None)
```

Records a data source binding was deleted

<a id="lscsde_workspace_mgmt.exceptions"></a>

# lscsde\_workspace\_mgmt.exceptions

<a id="lscsde_workspace_mgmt.exceptions.NoAssignedValidWorkspaces"></a>

## NoAssignedValidWorkspaces

```python
class NoAssignedValidWorkspaces(Exception)
```

Represents an error where a user is not assigned any valid workspaces

<a id="lscsde_workspace_mgmt.exceptions.WorkspaceNotFoundException"></a>

## WorkspaceNotFoundException

```python
class WorkspaceNotFoundException(Exception)
```

Represents an exception where a workspace is not found in the labels from jupyterhub

<a id="lscsde_workspace_mgmt.workspaceclient"></a>

# lscsde\_workspace\_mgmt.workspaceclient

<a id="lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient"></a>

## AnalyticsWorkspaceClient

```python
class AnalyticsWorkspaceClient(KubernetesNamespacedCustomClient)
```

Client for interacting with AnalyticsWorkspacess

<a id="lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets a specific AnalyticsWorkspace resource

<a id="lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists AnalyticsWorkspace resources in the namespace supplied

<a id="lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.list_by_username"></a>

#### list\_by\_username

```python
async def list_by_username(binding_client: AnalyticsWorkspaceBindingClient,
                           namespace: str, username: str)
```

Lists AnalyticsWorkspace resources in the namespace supplied that match the username

<a id="lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.create"></a>

#### create

```python
async def create(body: AnalyticsWorkspace)
```

Creates a AnalyticsWorkspace resource in the namespace supplied

<a id="lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.patch"></a>

#### patch

```python
async def patch(namespace: str = None,
                name: str = None,
                patch_body: dict = None,
                body: AnalyticsWorkspace = None)
```

Patches a AnalyticsWorkspace resource in the namespace supplied

<a id="lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str,
                       status: AnalyticsWorkspaceStatus)
```

Patches the status of an AnalyticsWorkspace resource in the namespace supplied

<a id="lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.replace"></a>

#### replace

```python
async def replace(body: AnalyticsWorkspace)
```

Replaces a AnalyticsWorkspace resource with the one supplied

<a id="lscsde_workspace_mgmt.workspaceclient.AnalyticsWorkspaceClient.delete"></a>

#### delete

```python
async def delete(body: AnalyticsWorkspace = None,
                 namespace: str = None,
                 name: str = None)
```

Deletes a AnalyticsWorkspace resource in the namespace supplied

<a id="lscsde_workspace_mgmt.pvclient"></a>

# lscsde\_workspace\_mgmt.pvclient

<a id="lscsde_workspace_mgmt.pvclient.PersistentVolumeClaimClient"></a>

## PersistentVolumeClaimClient

```python
class PersistentVolumeClaimClient()
```

Client used for interacting with PersistentVolumeClaim resources in kubernetes

<a id="lscsde_workspace_mgmt.pvclient.PersistentVolumeClaimClient.get"></a>

#### get

```python
async def get(name: str, namespace: str) -> V1PersistentVolumeClaim
```

Gets a specific PVC

<a id="lscsde_workspace_mgmt.pvclient.PersistentVolumeClaimClient.create_if_not_exists"></a>

#### create\_if\_not\_exists

```python
async def create_if_not_exists(name: str,
                               namespace: str,
                               storage_class_name: str = None,
                               labels: dict[str, str] = {},
                               access_modes: list[str] = None,
                               storage_requested: str = None)
```

Create a specific PVC if it doesn't already exist

<a id="lscsde_workspace_mgmt.pvclient.PersistentVolumeClaimClient.mount"></a>

#### mount

```python
async def mount(pod: V1Pod,
                storage_name: str,
                namespace: str,
                storage_class_name: str,
                mount_path: str,
                read_only: bool = False) -> V1Pod
```

mounts a PVC into a pod

<a id="lscsde_workspace_mgmt.managers"></a>

# lscsde\_workspace\_mgmt.managers

<a id="lscsde_workspace_mgmt.managers.AnalyticsDataSourceManager"></a>

## AnalyticsDataSourceManager

```python
class AnalyticsDataSourceManager()
```

creates a manager for Analytics Data sources, their associated bindings, events and pvc's.

<a id="lscsde_workspace_mgmt.managers.AnalyticsWorkspaceManager"></a>

## AnalyticsWorkspaceManager

```python
class AnalyticsWorkspaceManager()
```

creates a manager for Analytics Workspaces, their associated bindings, events and pvc's.

<a id="lscsde_workspace_mgmt.managers.AnalyticsWorkspaceManager.get_workspaces_for_user"></a>

#### get\_workspaces\_for\_user

```python
async def get_workspaces_for_user(namespace: str, username: str)
```

Gets a workspace for a user

<a id="lscsde_workspace_mgmt.managers.AnalyticsWorkspaceManager.get_permitted_workspaces"></a>

#### get\_permitted\_workspaces

```python
async def get_permitted_workspaces(namespace: str,
                                   username: str,
                                   date_now=datetime.today())
```

Gets the workspaces that are permitted for a user

<a id="lscsde_workspace_mgmt.managers.AnalyticsWorkspaceManager.mount_workspace"></a>

#### mount\_workspace

```python
async def mount_workspace(pod: V1Pod,
                          storage_class_name,
                          mount_prefix,
                          storage_prefix: str = "",
                          read_only: bool = False,
                          mount_path="")
```

Mounts the workspace persistent volume claims

<a id="lscsde_workspace_mgmt.managers.AnalyticsManager"></a>

## AnalyticsManager

```python
class AnalyticsManager()
```

A high level manager for both workspace and datasource

<a id="lscsde_workspace_mgmt.namespacedclient"></a>

# lscsde\_workspace\_mgmt.namespacedclient

<a id="lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient"></a>

## KubernetesNamespacedCustomClient

```python
class KubernetesNamespacedCustomClient()
```

Represents a namespaced client for interacting with kubernetes objects

<a id="lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.get_api_version"></a>

#### get\_api\_version

```python
def get_api_version()
```

Gets the API version

<a id="lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets the requested resource

<a id="lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists the requested resources

<a id="lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.patch"></a>

#### patch

```python
async def patch(namespace: str, name: str, body: dict)
```

Patches the requested resource

<a id="lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str, body: dict)
```

Patches the status of the requested resource

<a id="lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.replace"></a>

#### replace

```python
async def replace(namespace: str, name: str, body: dict)
```

Replaces the requested resource with the one supplied

<a id="lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.create"></a>

#### create

```python
async def create(namespace: str, body: dict)
```

Creates the requested resource

<a id="lscsde_workspace_mgmt.namespacedclient.KubernetesNamespacedCustomClient.delete"></a>

#### delete

```python
async def delete(namespace: str, name: str)
```

Deletes the requested resource

<a id="lscsde_workspace_mgmt.objects"></a>

# lscsde\_workspace\_mgmt.objects

<a id="lscsde_workspace_mgmt.objects.AnalyticsWorkspaceConverter"></a>

## AnalyticsWorkspaceConverter

```python
class AnalyticsWorkspaceConverter()
```

The converter allows us to perform operations against an analytics workspace to convert them for use in other platforms

<a id="lscsde_workspace_mgmt.objects.AnalyticsWorkspaceConverter.days_until_expiry"></a>

#### days\_until\_expiry

```python
def days_until_expiry(time_str, date_now=datetime.today())
```

Calculates the number of days until the workspace or workspace binding expires

<a id="lscsde_workspace_mgmt.objects.AnalyticsWorkspaceConverter.to_workspace_dict"></a>

#### to\_workspace\_dict

```python
def to_workspace_dict(workspace: AnalyticsWorkspace,
                      date_now=datetime.today())
```

Converts the workspace to the dictionary used by kubespawner to create the pod resource

<a id="lscsde_workspace_mgmt._version"></a>

# lscsde\_workspace\_mgmt.\_version

<a id="lscsde_workspace_mgmt.datasourceclient"></a>

# lscsde\_workspace\_mgmt.datasourceclient

<a id="lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient"></a>

## AnalyticsDataSourceClient

```python
class AnalyticsDataSourceClient(KubernetesNamespacedCustomClient)
```

This class allows developers to interact with AnalyticsDataSource objects on kubernetes

<a id="lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets an individual AnalyticsDataSource

<a id="lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists the AnalyticsDataSource in a specified namespace

<a id="lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.list_by_workspace"></a>

#### list\_by\_workspace

```python
async def list_by_workspace(binding_client: AnalyticsDataSourceBindingClient,
                            namespace: str, workspace: str)
```

Lists the AnalyticsDataSource in a specified namespace for the workspace specified

<a id="lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.create"></a>

#### create

```python
async def create(body: AnalyticsDataSource)
```

Creates a AnalyticsDataSource resource

<a id="lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.patch"></a>

#### patch

```python
async def patch(namespace: str = None,
                name: str = None,
                patch_body: dict = None,
                body: AnalyticsDataSource = None)
```

Patches a AnalyticsDataSource resource

<a id="lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str,
                       status: AnalyticsDataSourceStatus)
```

Patches a AnalyticsDataSource resources status segment

<a id="lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.replace"></a>

#### replace

```python
async def replace(body: AnalyticsDataSource)
```

Replaces a AnalyticsDataSource resource with the one provided

<a id="lscsde_workspace_mgmt.datasourceclient.AnalyticsDataSourceClient.delete"></a>

#### delete

```python
async def delete(body: AnalyticsDataSource = None,
                 namespace: str = None,
                 name: str = None)
```

Deletes a AnalyticsDataSource resource

<a id="lscsde_workspace_mgmt.models"></a>

# lscsde\_workspace\_mgmt.models

<a id="lscsde_workspace_mgmt.models.KubernetesHelper"></a>

## KubernetesHelper

```python
class KubernetesHelper()
```

A helper to help us interact with kubernetes as it would like

<a id="lscsde_workspace_mgmt.models.KubernetesHelper.format_as_label"></a>

#### format\_as\_label

```python
def format_as_label(username: str)
```

reformats a string to make it compatible for use in kubernetes label field

<a id="lscsde_workspace_mgmt.models.KubernetesMetadata"></a>

## KubernetesMetadata

```python
class KubernetesMetadata(BaseModel)
```

A standard Kubernetes Metadata object

<a id="lscsde_workspace_mgmt.models.AnalyticsWorkspaceValidity"></a>

## AnalyticsWorkspaceValidity

```python
class AnalyticsWorkspaceValidity(BaseModel)
```

Represents the validity of the a workspace

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacevalidity

<a id="lscsde_workspace_mgmt.models.VirtualMachineWorkspaceSpec"></a>

## VirtualMachineWorkspaceSpec

```python
class VirtualMachineWorkspaceSpec(BaseModel)
```

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacevirtualmachine

<a id="lscsde_workspace_mgmt.models.JupyterWorkspaceStorage"></a>

## JupyterWorkspaceStorage

```python
class JupyterWorkspaceStorage(BaseModel)
```

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspaceadditionalstorage

<a id="lscsde_workspace_mgmt.models.JupyterWorkspacePersistentVolumeClaim"></a>

## JupyterWorkspacePersistentVolumeClaim

```python
class JupyterWorkspacePersistentVolumeClaim(BaseModel)
```

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspacepersistentvolumeclaim

<a id="lscsde_workspace_mgmt.models.JupyterWorkspaceSpecResources"></a>

## JupyterWorkspaceSpecResources

```python
class JupyterWorkspaceSpecResources(TypedDict)
```

Represents the resources object on a jupyter workspace

TODO: This needs to be converted to use https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ResourceRequirements.md

<a id="lscsde_workspace_mgmt.models.JupyterWorkspaceSpecNodeSelector"></a>

## JupyterWorkspaceSpecNodeSelector

```python
class JupyterWorkspaceSpecNodeSelector(TypedDict)
```

Represents a node selector

TODO: Convert to a dict of strings of a jupyter workspace

<a id="lscsde_workspace_mgmt.models.JupyterWorkspaceSpecToleration"></a>

## JupyterWorkspaceSpecToleration

```python
class JupyterWorkspaceSpecToleration(BaseModel)
```

Represents a toleration property of a jupyter workspace

TODO: This needs to be converted to use https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Toleration.md

<a id="lscsde_workspace_mgmt.models.JupyterWorkspaceSpec"></a>

## JupyterWorkspaceSpec

```python
class JupyterWorkspaceSpec(BaseModel)
```

Represents the jupyterWorkspace property

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspace

<a id="lscsde_workspace_mgmt.models.AnalyticsWorkspaceStatus"></a>

## AnalyticsWorkspaceStatus

```python
class AnalyticsWorkspaceStatus(BaseModel)
```

Represents the status field of the analyticsworkspace resource

<a id="lscsde_workspace_mgmt.models.AnalyticsWorkspaceBindingStatus"></a>

## AnalyticsWorkspaceBindingStatus

```python
class AnalyticsWorkspaceBindingStatus(BaseModel)
```

Represents the status field of the analyticsworkspacebinding resource

<a id="lscsde_workspace_mgmt.models.AnalyticsWorkspaceSpec"></a>

## AnalyticsWorkspaceSpec

```python
class AnalyticsWorkspaceSpec(BaseModel)
```

Represents the spec segment of the analyticsworkspace resource

<a id="lscsde_workspace_mgmt.models.AnalyticsWorkspaceBindingClaim"></a>

## AnalyticsWorkspaceBindingClaim

```python
class AnalyticsWorkspaceBindingClaim(BaseModel)
```

Represents the claims segment on a AnalyticsWorkspaceBinding resource

This has not yet been implemented

<a id="lscsde_workspace_mgmt.models.AnalyticsWorkspaceBindingSpec"></a>

## AnalyticsWorkspaceBindingSpec

```python
class AnalyticsWorkspaceBindingSpec(BaseModel)
```

Represents the spec segment of an AnalyticsWorkspaceBinding resource

<a id="lscsde_workspace_mgmt.models.AnalyticsWorkspaceBindingSpec.username_as_label"></a>

#### username\_as\_label

```python
def username_as_label()
```

Reads the username formatted as a kubernetes label

<a id="lscsde_workspace_mgmt.models.AnalyticsWorkspaceBinding"></a>

## AnalyticsWorkspaceBinding

```python
class AnalyticsWorkspaceBinding(BaseModel)
```

Represents an AnalyticsWorkspaceBinding object

<a id="lscsde_workspace_mgmt.models.AnalyticsWorkspace"></a>

## AnalyticsWorkspace

```python
class AnalyticsWorkspace(BaseModel)
```

Represents an AnalyticsWorkspace resource

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourcePublisherContact"></a>

## AnalyticsDataSourcePublisherContact

```python
class AnalyticsDataSourcePublisherContact(BaseModel)
```

Represents the publisher contact of a datasource object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourcePublisher"></a>

## AnalyticsDataSourcePublisher

```python
class AnalyticsDataSourcePublisher(BaseModel)
```

Represents the publisher of a datasource object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceProject"></a>

## AnalyticsDataSourceProject

```python
class AnalyticsDataSourceProject(BaseModel)
```

Represents the project of a datasource object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceConnectionString"></a>

## AnalyticsDataSourceConnectionString

```python
class AnalyticsDataSourceConnectionString(BaseModel)
```

Represents the connection string of a datasource object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceSecret"></a>

## AnalyticsDataSourceSecret

```python
class AnalyticsDataSourceSecret(BaseModel)
```

Represents a datasource secret

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceSecretWithKey"></a>

## AnalyticsDataSourceSecretWithKey

```python
class AnalyticsDataSourceSecretWithKey(AnalyticsDataSourceSecret)
```

Represents a datasource secret with a key

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceDataBricksConnection"></a>

## AnalyticsDataSourceDataBricksConnection

```python
class AnalyticsDataSourceDataBricksConnection(BaseModel)
```

Represents a databricks connection

<a id="lscsde_workspace_mgmt.models.AnalyticsApproval"></a>

## AnalyticsApproval

```python
class AnalyticsApproval(BaseModel)
```

Represents an analytics approval object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceConnection"></a>

## AnalyticsDataSourceConnection

```python
class AnalyticsDataSourceConnection(BaseModel)
```

Represents an connection on a datasource object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceSpec"></a>

## AnalyticsDataSourceSpec

```python
class AnalyticsDataSourceSpec(BaseModel)
```

represents a spec segment of an AnalyticsDataSource object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceBindingStatus"></a>

## AnalyticsDataSourceBindingStatus

```python
class AnalyticsDataSourceBindingStatus(BaseModel)
```

Represents the status segment of a AnalyticsDataSourceBinding object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceStatus"></a>

## AnalyticsDataSourceStatus

```python
class AnalyticsDataSourceStatus(BaseModel)
```

Represents a status of an AnalyticsDataSource object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceBindingSpec"></a>

## AnalyticsDataSourceBindingSpec

```python
class AnalyticsDataSourceBindingSpec(BaseModel)
```

Represents the spec of an AnalyticsDataSourceBinding object

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSource"></a>

## AnalyticsDataSource

```python
class AnalyticsDataSource(BaseModel)
```

Represents the AnalyticsDataSource Resource

<a id="lscsde_workspace_mgmt.models.AnalyticsDataSourceBinding"></a>

## AnalyticsDataSourceBinding

```python
class AnalyticsDataSourceBinding(BaseModel)
```

Represents the AnalyticsDataSourceBinding resource

<a id="lscsde_workspace_mgmt.models.AnalyticsCrateSpecRepository"></a>

## AnalyticsCrateSpecRepository

```python
class AnalyticsCrateSpecRepository(BaseModel)
```

Represents repository on a AnalyticsCrateSpec object

<a id="lscsde_workspace_mgmt.models.AnalyticsCrateSpec"></a>

## AnalyticsCrateSpec

```python
class AnalyticsCrateSpec(BaseModel)
```

Represents the spec segment of a AnalyticsCrate Object

<a id="lscsde_workspace_mgmt.models.AnalyticsCrateStatus"></a>

## AnalyticsCrateStatus

```python
class AnalyticsCrateStatus(BaseModel)
```

Represents the status field of a AnalyticsCrate object

<a id="lscsde_workspace_mgmt.models.AnalyticsCrate"></a>

## AnalyticsCrate

```python
class AnalyticsCrate(BaseModel)
```

Represents an AnalyticsCrate resource

<a id="lscsde_workspace_mgmt.tests.workspaces"></a>

# lscsde\_workspace\_mgmt.tests.workspaces

<a id="lscsde_workspace_mgmt.tests.datasources"></a>

# lscsde\_workspace\_mgmt.tests.datasources

<a id="lscsde_workspace_mgmt.tests.datasourcesbindings"></a>

# lscsde\_workspace\_mgmt.tests.datasourcesbindings

<a id="lscsde_workspace_mgmt.tests.k8shelper"></a>

# lscsde\_workspace\_mgmt.tests.k8shelper

<a id="lscsde_workspace_mgmt.tests.workspacebindings"></a>

# lscsde\_workspace\_mgmt.tests.workspacebindings

<a id="lscsde_workspace_mgmt.integrationtest"></a>

# lscsde\_workspace\_mgmt.integrationtest

<a id="lscsde_workspace_mgmt.test"></a>

# lscsde\_workspace\_mgmt.test

<a id="lscsde_workspace_mgmt.workspacebindingclient"></a>

# lscsde\_workspace\_mgmt.workspacebindingclient

<a id="lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient"></a>

## AnalyticsWorkspaceBindingClient

```python
class AnalyticsWorkspaceBindingClient(KubernetesNamespacedCustomClient)
```

Client for interacting with AnalyticsWorkspaceBindings

<a id="lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets a specific AnalyticsWorkspaceBinding resource

<a id="lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists AnalyticsWorkspaceBinding resources in the namespace supplied

<a id="lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.list_by_username"></a>

#### list\_by\_username

```python
async def list_by_username(namespace, username)
```

Lists AnalyticsWorkspaceBinding resources in the namespace supplied that match the username

If the label doesn't exist, it will be patched into the definition to increase performance in etcd

<a id="lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.create"></a>

#### create

```python
async def create(body: AnalyticsWorkspaceBinding, append_label: bool = True)
```

Creates a AnalyticsWorkspaceBinding resource in the namespace supplied

<a id="lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.patch"></a>

#### patch

```python
async def patch(namespace: str = None,
                name: str = None,
                patch_body: dict = None,
                body: AnalyticsWorkspaceBinding = None)
```

Patches a AnalyticsWorkspaceBinding resource in the namespace supplied

<a id="lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str,
                       status: AnalyticsWorkspaceBindingStatus)
```

Patches the status of a AnalyticsWorkspaceBinding resource in the namespace supplied

<a id="lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.replace"></a>

#### replace

```python
async def replace(body: AnalyticsWorkspaceBinding, append_label: bool = True)
```

Replaces a AnalyticsWorkspaceBinding resource with the one supplied

<a id="lscsde_workspace_mgmt.workspacebindingclient.AnalyticsWorkspaceBindingClient.delete"></a>

#### delete

```python
async def delete(body: AnalyticsWorkspaceBinding = None,
                 namespace: str = None,
                 name: str = None)
```

Deletes a AnalyticsWorkspaceBinding resource in the namespace supplied

