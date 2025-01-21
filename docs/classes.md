---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="datasourcebindingclient.AnalyticsDataSourceBindingClient"></a>

## AnalyticsDataSourceBindingClient Objects

```python
class AnalyticsDataSourceBindingClient(KubernetesNamespacedCustomClient)
```

This class allows developers to interact with AnalyticsDataSourceBinding objects on kubernetes

<a id="datasourcebindingclient.AnalyticsDataSourceBindingClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets an individual AnalyticsDataSourceBinding

<a id="datasourcebindingclient.AnalyticsDataSourceBindingClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists the AnalyticsDataSourceBindings in a specified namespace

<a id="datasourcebindingclient.AnalyticsDataSourceBindingClient.list_by_workspace"></a>

#### list\_by\_workspace

```python
async def list_by_workspace(namespace, workspace)
```

Lists the AnalyticsDataSourceBindings in a specified namespace which belong to a specific workspace

If a binding does not have the relevant labels defined, the service will assign the label automatically based upon the workspace. 
This makes the query more performant when querying etcd.

<a id="datasourcebindingclient.AnalyticsDataSourceBindingClient.create"></a>

#### create

```python
async def create(body: AnalyticsDataSourceBinding, append_label: bool = True)
```

Creates a AnalyticsDataSourceBinding resource

<a id="datasourcebindingclient.AnalyticsDataSourceBindingClient.patch"></a>

#### patch

```python
async def patch(namespace: str = None,
                name: str = None,
                patch_body: dict = None,
                body: AnalyticsDataSourceBinding = None)
```

Patches a AnalyticsDataSourceBinding resource

<a id="datasourcebindingclient.AnalyticsDataSourceBindingClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str,
                       status: AnalyticsDataSourceBindingStatus)
```

Patches a AnalyticsDataSourceBinding resources status segment

<a id="datasourcebindingclient.AnalyticsDataSourceBindingClient.replace"></a>

#### replace

```python
async def replace(body: AnalyticsDataSourceBinding, append_label: bool = True)
```

Replaces a AnalyticsDataSourceBinding resource with the one provided

<a id="datasourcebindingclient.AnalyticsDataSourceBindingClient.delete"></a>

#### delete

```python
async def delete(body: AnalyticsDataSourceBinding = None,
                 namespace: str = None,
                 name: str = None)
```

Deletes a AnalyticsDataSourceBinding resource

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="eventclient.EventClient"></a>

## EventClient Objects

```python
class EventClient()
```

A class for interacting with Events objects in kubernetes

<a id="eventclient.EventClient.RegisterWorkspaceEvent"></a>

#### RegisterWorkspaceEvent

```python
async def RegisterWorkspaceEvent(workspace: AnalyticsWorkspace, reason: str,
                                 note: str)
```

Records a workspace event

<a id="eventclient.EventClient.RegisterWorkspaceBindingEvent"></a>

#### RegisterWorkspaceBindingEvent

```python
async def RegisterWorkspaceBindingEvent(binding: AnalyticsWorkspaceBinding,
                                        reason: str, note: str)
```

Records a workspace binding event

<a id="eventclient.EventClient.RegisterDataSourceEvent"></a>

#### RegisterDataSourceEvent

```python
async def RegisterDataSourceEvent(datasource: AnalyticsDataSource, reason: str,
                                  note: str)
```

Records a datasource event

<a id="eventclient.EventClient.RegisterDataSourceBindingEvent"></a>

#### RegisterDataSourceBindingEvent

```python
async def RegisterDataSourceBindingEvent(binding: AnalyticsDataSourceBinding,
                                         reason: str, note: str)
```

Records a datasource binding event

<a id="eventclient.EventClient.WorkspaceCreated"></a>

#### WorkspaceCreated

```python
async def WorkspaceCreated(workspace: AnalyticsWorkspace, note: str = None)
```

Records a workspace was created

<a id="eventclient.EventClient.WorkspaceUpdated"></a>

#### WorkspaceUpdated

```python
async def WorkspaceUpdated(workspace: AnalyticsWorkspace, note: str = None)
```

Records a workspace was updates

<a id="eventclient.EventClient.WorkspaceDeleted"></a>

#### WorkspaceDeleted

```python
async def WorkspaceDeleted(workspace: AnalyticsWorkspace, note: str = None)
```

Records a workspace was deleted

<a id="eventclient.EventClient.WorkspaceBindingCreated"></a>

#### WorkspaceBindingCreated

```python
async def WorkspaceBindingCreated(binding: AnalyticsWorkspaceBinding,
                                  note: str = None)
```

Records a workspace binding was created

<a id="eventclient.EventClient.WorkspaceBindingUpdated"></a>

#### WorkspaceBindingUpdated

```python
async def WorkspaceBindingUpdated(binding: AnalyticsWorkspaceBinding,
                                  note: str = None)
```

Records a workspace binding was updated

<a id="eventclient.EventClient.WorkspaceBindingDeleted"></a>

#### WorkspaceBindingDeleted

```python
async def WorkspaceBindingDeleted(binding: AnalyticsWorkspaceBinding,
                                  note: str = None)
```

Records a workspace binding was deleted

<a id="eventclient.EventClient.DataSourceCreated"></a>

#### DataSourceCreated

```python
async def DataSourceCreated(datasource: AnalyticsDataSource, note: str = None)
```

Records a data source was created

<a id="eventclient.EventClient.DataSourceUpdated"></a>

#### DataSourceUpdated

```python
async def DataSourceUpdated(datasource: AnalyticsDataSource, note: str = None)
```

Records a data source was updated

<a id="eventclient.EventClient.DataSourceDeleted"></a>

#### DataSourceDeleted

```python
async def DataSourceDeleted(datasource: AnalyticsDataSource, note: str = None)
```

Records a data source was deleted

<a id="eventclient.EventClient.DataSourceBindingCreated"></a>

#### DataSourceBindingCreated

```python
async def DataSourceBindingCreated(binding: AnalyticsDataSourceBinding,
                                   note: str = None)
```

Records a data source binding was created

<a id="eventclient.EventClient.DataSourceBindingUpdated"></a>

#### DataSourceBindingUpdated

```python
async def DataSourceBindingUpdated(binding: AnalyticsDataSourceBinding,
                                   note: str = None)
```

Records a data source binding was updated

<a id="eventclient.EventClient.DataSourceBindingDeleted"></a>

#### DataSourceBindingDeleted

```python
async def DataSourceBindingDeleted(binding: AnalyticsDataSourceBinding,
                                   note: str = None)
```

Records a data source binding was deleted

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="exceptions.NoAssignedValidWorkspaces"></a>

## NoAssignedValidWorkspaces Objects

```python
class NoAssignedValidWorkspaces(Exception)
```

Represents an error where a user is not assigned any valid workspaces

<a id="exceptions.WorkspaceNotFoundException"></a>

## WorkspaceNotFoundException Objects

```python
class WorkspaceNotFoundException(Exception)
```

Represents an exception where a workspace is not found in the labels from jupyterhub

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="workspaceclient.AnalyticsWorkspaceClient"></a>

## AnalyticsWorkspaceClient Objects

```python
class AnalyticsWorkspaceClient(KubernetesNamespacedCustomClient)
```

Client for interacting with AnalyticsWorkspacess

<a id="workspaceclient.AnalyticsWorkspaceClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets a specific AnalyticsWorkspace resource

<a id="workspaceclient.AnalyticsWorkspaceClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists AnalyticsWorkspace resources in the namespace supplied

<a id="workspaceclient.AnalyticsWorkspaceClient.list_by_username"></a>

#### list\_by\_username

```python
async def list_by_username(binding_client: AnalyticsWorkspaceBindingClient,
                           namespace: str, username: str)
```

Lists AnalyticsWorkspace resources in the namespace supplied that match the username

<a id="workspaceclient.AnalyticsWorkspaceClient.create"></a>

#### create

```python
async def create(body: AnalyticsWorkspace)
```

Creates a AnalyticsWorkspace resource in the namespace supplied

<a id="workspaceclient.AnalyticsWorkspaceClient.patch"></a>

#### patch

```python
async def patch(namespace: str = None,
                name: str = None,
                patch_body: dict = None,
                body: AnalyticsWorkspace = None)
```

Patches a AnalyticsWorkspace resource in the namespace supplied

<a id="workspaceclient.AnalyticsWorkspaceClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str,
                       status: AnalyticsWorkspaceStatus)
```

Patches the status of an AnalyticsWorkspace resource in the namespace supplied

<a id="workspaceclient.AnalyticsWorkspaceClient.replace"></a>

#### replace

```python
async def replace(body: AnalyticsWorkspace)
```

Replaces a AnalyticsWorkspace resource with the one supplied

<a id="workspaceclient.AnalyticsWorkspaceClient.delete"></a>

#### delete

```python
async def delete(body: AnalyticsWorkspace = None,
                 namespace: str = None,
                 name: str = None)
```

Deletes a AnalyticsWorkspace resource in the namespace supplied

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="pvclient.PersistentVolumeClaimClient"></a>

## PersistentVolumeClaimClient Objects

```python
class PersistentVolumeClaimClient()
```

Client used for interacting with PersistentVolumeClaim resources in kubernetes

<a id="pvclient.PersistentVolumeClaimClient.get"></a>

#### get

```python
async def get(name: str, namespace: str) -> V1PersistentVolumeClaim
```

Gets a specific PVC

<a id="pvclient.PersistentVolumeClaimClient.create_if_not_exists"></a>

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

<a id="pvclient.PersistentVolumeClaimClient.mount"></a>

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

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="managers.AnalyticsDataSourceManager"></a>

## AnalyticsDataSourceManager Objects

```python
class AnalyticsDataSourceManager()
```

creates a manager for Analytics Data sources, their associated bindings, events and pvc's.

<a id="managers.AnalyticsWorkspaceManager"></a>

## AnalyticsWorkspaceManager Objects

```python
class AnalyticsWorkspaceManager()
```

creates a manager for Analytics Workspaces, their associated bindings, events and pvc's.

<a id="managers.AnalyticsWorkspaceManager.get_workspaces_for_user"></a>

#### get\_workspaces\_for\_user

```python
async def get_workspaces_for_user(namespace: str, username: str)
```

Gets a workspace for a user

<a id="managers.AnalyticsWorkspaceManager.get_permitted_workspaces"></a>

#### get\_permitted\_workspaces

```python
async def get_permitted_workspaces(namespace: str,
                                   username: str,
                                   date_now=datetime.today())
```

Gets the workspaces that are permitted for a user

<a id="managers.AnalyticsWorkspaceManager.mount_workspace"></a>

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

<a id="managers.AnalyticsManager"></a>

## AnalyticsManager Objects

```python
class AnalyticsManager()
```

A high level manager for both workspace and datasource

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="namespacedclient.KubernetesNamespacedCustomClient"></a>

## KubernetesNamespacedCustomClient Objects

```python
class KubernetesNamespacedCustomClient()
```

Represents a namespaced client for interacting with kubernetes objects

<a id="namespacedclient.KubernetesNamespacedCustomClient.get_api_version"></a>

#### get\_api\_version

```python
def get_api_version()
```

Gets the API version

<a id="namespacedclient.KubernetesNamespacedCustomClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets the requested resource

<a id="namespacedclient.KubernetesNamespacedCustomClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists the requested resources

<a id="namespacedclient.KubernetesNamespacedCustomClient.patch"></a>

#### patch

```python
async def patch(namespace: str, name: str, body: dict)
```

Patches the requested resource

<a id="namespacedclient.KubernetesNamespacedCustomClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str, body: dict)
```

Patches the status of the requested resource

<a id="namespacedclient.KubernetesNamespacedCustomClient.replace"></a>

#### replace

```python
async def replace(namespace: str, name: str, body: dict)
```

Replaces the requested resource with the one supplied

<a id="namespacedclient.KubernetesNamespacedCustomClient.create"></a>

#### create

```python
async def create(namespace: str, body: dict)
```

Creates the requested resource

<a id="namespacedclient.KubernetesNamespacedCustomClient.delete"></a>

#### delete

```python
async def delete(namespace: str, name: str)
```

Deletes the requested resource

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="objects.AnalyticsWorkspaceConverter"></a>

## AnalyticsWorkspaceConverter Objects

```python
class AnalyticsWorkspaceConverter()
```

The converter allows us to perform operations against an analytics workspace to convert them for use in other platforms

<a id="objects.AnalyticsWorkspaceConverter.days_until_expiry"></a>

#### days\_until\_expiry

```python
def days_until_expiry(time_str, date_now=datetime.today())
```

Calculates the number of days until the workspace or workspace binding expires

<a id="objects.AnalyticsWorkspaceConverter.to_workspace_dict"></a>

#### to\_workspace\_dict

```python
def to_workspace_dict(workspace: AnalyticsWorkspace,
                      date_now=datetime.today())
```

Converts the workspace to the dictionary used by kubespawner to create the pod resource

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="datasourceclient.AnalyticsDataSourceClient"></a>

## AnalyticsDataSourceClient Objects

```python
class AnalyticsDataSourceClient(KubernetesNamespacedCustomClient)
```

This class allows developers to interact with AnalyticsDataSource objects on kubernetes

<a id="datasourceclient.AnalyticsDataSourceClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets an individual AnalyticsDataSource

<a id="datasourceclient.AnalyticsDataSourceClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists the AnalyticsDataSource in a specified namespace

<a id="datasourceclient.AnalyticsDataSourceClient.list_by_workspace"></a>

#### list\_by\_workspace

```python
async def list_by_workspace(binding_client: AnalyticsDataSourceBindingClient,
                            namespace: str, workspace: str)
```

Lists the AnalyticsDataSource in a specified namespace for the workspace specified

<a id="datasourceclient.AnalyticsDataSourceClient.create"></a>

#### create

```python
async def create(body: AnalyticsDataSource)
```

Creates a AnalyticsDataSource resource

<a id="datasourceclient.AnalyticsDataSourceClient.patch"></a>

#### patch

```python
async def patch(namespace: str = None,
                name: str = None,
                patch_body: dict = None,
                body: AnalyticsDataSource = None)
```

Patches a AnalyticsDataSource resource

<a id="datasourceclient.AnalyticsDataSourceClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str,
                       status: AnalyticsDataSourceStatus)
```

Patches a AnalyticsDataSource resources status segment

<a id="datasourceclient.AnalyticsDataSourceClient.replace"></a>

#### replace

```python
async def replace(body: AnalyticsDataSource)
```

Replaces a AnalyticsDataSource resource with the one provided

<a id="datasourceclient.AnalyticsDataSourceClient.delete"></a>

#### delete

```python
async def delete(body: AnalyticsDataSource = None,
                 namespace: str = None,
                 name: str = None)
```

Deletes a AnalyticsDataSource resource

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="models.KubernetesHelper"></a>

## KubernetesHelper Objects

```python
class KubernetesHelper()
```

A helper to help us interact with kubernetes as it would like

<a id="models.KubernetesHelper.format_as_label"></a>

#### format\_as\_label

```python
def format_as_label(username: str)
```

reformats a string to make it compatible for use in kubernetes label field

<a id="models.KubernetesMetadata"></a>

## KubernetesMetadata Objects

```python
class KubernetesMetadata(BaseModel)
```

A standard Kubernetes Metadata object

<a id="models.KubernetesMetadata.name"></a>

#### name

Name of the resource in kubernetes

<a id="models.KubernetesMetadata.namespace"></a>

#### namespace

Namespace that the resource is deployed to in kubernetes

<a id="models.KubernetesMetadata.annotations"></a>

#### annotations

A dictionary of any annotations assigned to the resource in kubernetes

<a id="models.KubernetesMetadata.labels"></a>

#### labels

A dictionary of any labels assigned to the resource in kubernetes

<a id="models.KubernetesMetadata.resource_version"></a>

#### resource\_version

The version of the resource in kubernetes

<a id="models.AnalyticsWorkspaceValidity"></a>

## AnalyticsWorkspaceValidity Objects

```python
class AnalyticsWorkspaceValidity(BaseModel)
```

Represents the validity of the a workspace

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacevalidity

<a id="models.AnalyticsWorkspaceValidity.available_from"></a>

#### available\_from

The date that the workspace is valid from (in open API date format)

<a id="models.AnalyticsWorkspaceValidity.expires"></a>

#### expires

The date that the workspace expires

<a id="models.VirtualMachineWorkspaceSpec"></a>

## VirtualMachineWorkspaceSpec Objects

```python
class VirtualMachineWorkspaceSpec(BaseModel)
```

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacevirtualmachine

<a id="models.VirtualMachineWorkspaceSpec.max_hosts"></a>

#### max\_hosts

The maximum number of hosts

<a id="models.JupyterWorkspaceStorage"></a>

## JupyterWorkspaceStorage Objects

```python
class JupyterWorkspaceStorage(BaseModel)
```

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspaceadditionalstorage

<a id="models.JupyterWorkspaceStorage.mount_path"></a>

#### mount\_path

The directory to mount this storage in the claim

<a id="models.JupyterWorkspaceStorage.persistent_volume_claim"></a>

#### persistent\_volume\_claim

The name of the persistent volume claim to apply

<a id="models.JupyterWorkspaceStorage.storage_class_name"></a>

#### storage\_class\_name

The storage class name applied to the persistent volume claim (if it doesn’t already exist).

<a id="models.JupyterWorkspacePersistentVolumeClaim"></a>

## JupyterWorkspacePersistentVolumeClaim Objects

```python
class JupyterWorkspacePersistentVolumeClaim(BaseModel)
```

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspacepersistentvolumeclaim

<a id="models.JupyterWorkspacePersistentVolumeClaim.name"></a>

#### name

The name of the default persistent volume claim to associate with this workspace. If not populated, it will use the workspace name to generate a new name for the PVC automatically

<a id="models.JupyterWorkspacePersistentVolumeClaim.storage_class_name"></a>

#### storage\_class\_name

The name of the storage class to create the persistent volume claim. If not populated, it will default to the system default. This is only applied when a PVC is initially created, it is ignored otherwise.

<a id="models.JupyterWorkspaceSpecResources"></a>

## JupyterWorkspaceSpecResources Objects

```python
class JupyterWorkspaceSpecResources(TypedDict)
```

Represents the resources object on a jupyter workspace

TODO: This needs to be converted to use https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ResourceRequirements.md

<a id="models.JupyterWorkspaceSpecNodeSelector"></a>

## JupyterWorkspaceSpecNodeSelector Objects

```python
class JupyterWorkspaceSpecNodeSelector(TypedDict)
```

Represents a node selector

TODO: Convert to a dict of strings of a jupyter workspace

<a id="models.JupyterWorkspaceSpecToleration"></a>

## JupyterWorkspaceSpecToleration Objects

```python
class JupyterWorkspaceSpecToleration(BaseModel)
```

Represents a toleration property of a jupyter workspace

TODO: This needs to be converted to use https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Toleration.md

<a id="models.JupyterWorkspaceSpec"></a>

## JupyterWorkspaceSpec Objects

```python
class JupyterWorkspaceSpec(BaseModel)
```

Represents the jupyterWorkspace property

https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspace

<a id="models.JupyterWorkspaceSpec.image"></a>

#### image

The image used when provisioning the pod created by jupyter hub

<a id="models.JupyterWorkspaceSpec.extra_labels"></a>

#### extra\_labels

A map of labels to append to the pod created

<a id="models.JupyterWorkspaceSpec.default_uri"></a>

#### default\_uri

The URI that jupyter will use when the items are provisioned.

<a id="models.JupyterWorkspaceSpec.node_selector"></a>

#### node\_selector

A dictionary of node selector tags per the kubernetes documentation

<a id="models.JupyterWorkspaceSpec.tolerations"></a>

#### tolerations

The pods tolerations.

<a id="models.JupyterWorkspaceSpec.resources"></a>

#### resources

Describes the compute resource requirements.

Per https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ResourceRequirements.md

<a id="models.JupyterWorkspaceSpec.additional_storage"></a>

#### additional\_storage

A list of additional persistent volume claims to map to the pods created for this environment.

<a id="models.JupyterWorkspaceSpec.persistent_volume_claim"></a>

#### persistent\_volume\_claim

A description of the persistent volume claim provisioned for the workspace

<a id="models.AnalyticsWorkspaceStatus"></a>

## AnalyticsWorkspaceStatus Objects

```python
class AnalyticsWorkspaceStatus(BaseModel)
```

Represents the status field of the analyticsworkspace resource

<a id="models.AnalyticsWorkspaceStatus.status_text"></a>

#### status\_text

A text field describing the current status of the workspace

<a id="models.AnalyticsWorkspaceStatus.persistent_volume_claim"></a>

#### persistent\_volume\_claim

The name of the assigned pvc for the workspace (if none provided)

<a id="models.AnalyticsWorkspaceStatus.additional_storage"></a>

#### additional\_storage

A dictionary containing the name of the various additional storage associated with the workspace

<a id="models.AnalyticsWorkspaceBindingStatus"></a>

## AnalyticsWorkspaceBindingStatus Objects

```python
class AnalyticsWorkspaceBindingStatus(BaseModel)
```

Represents the status field of the analyticsworkspacebinding resource

<a id="models.AnalyticsWorkspaceSpec"></a>

## AnalyticsWorkspaceSpec Objects

```python
class AnalyticsWorkspaceSpec(BaseModel)
```

Represents the spec segment of the analyticsworkspace resource

<a id="models.AnalyticsWorkspaceSpec.display_name"></a>

#### display\_name

The short display name used as the title for the workspace.

<a id="models.AnalyticsWorkspaceSpec.description"></a>

#### description

A simple description which can be multiple lines describing the workspace

<a id="models.AnalyticsWorkspaceSpec.validity"></a>

#### validity

An object describing variables which are validated to ensure that the workspace is still valid

<a id="models.AnalyticsWorkspaceSpec.jupyter_workspace"></a>

#### jupyter\_workspace

Represents a jupyter workspace

<a id="models.AnalyticsWorkspaceSpec.virtual_machine_workspace"></a>

#### virtual\_machine\_workspace

This is not yet implemented, it is to test validation of the CRD is functioning correctly

<a id="models.AnalyticsWorkspaceBindingClaim"></a>

## AnalyticsWorkspaceBindingClaim Objects

```python
class AnalyticsWorkspaceBindingClaim(BaseModel)
```

Represents the claims segment on a AnalyticsWorkspaceBinding resource

This has not yet been implemented

<a id="models.AnalyticsWorkspaceBindingClaim.name"></a>

#### name

The name of the claim

<a id="models.AnalyticsWorkspaceBindingClaim.operator"></a>

#### operator

The operator to test against

<a id="models.AnalyticsWorkspaceBindingClaim.value"></a>

#### value

The value to look for

<a id="models.AnalyticsWorkspaceBindingSpec"></a>

## AnalyticsWorkspaceBindingSpec Objects

```python
class AnalyticsWorkspaceBindingSpec(BaseModel)
```

Represents the spec segment of an AnalyticsWorkspaceBinding resource

<a id="models.AnalyticsWorkspaceBindingSpec.workspace"></a>

#### workspace

The name of the workspace in kubernetes. 

It is assumed that the workspace will be located in the same namespace as the current binding

<a id="models.AnalyticsWorkspaceBindingSpec.expires"></a>

#### expires

The date at which this binding expires

<a id="models.AnalyticsWorkspaceBindingSpec.username"></a>

#### username

The username to match

<a id="models.AnalyticsWorkspaceBindingSpec.comments"></a>

#### comments

Any comments relating to this binding.

<a id="models.AnalyticsWorkspaceBindingSpec.claims"></a>

#### claims

This is not yet implemented

<a id="models.AnalyticsWorkspaceBindingSpec.username_as_label"></a>

#### username\_as\_label

```python
def username_as_label()
```

Reads the username formatted as a kubernetes label

<a id="models.AnalyticsWorkspaceBinding"></a>

## AnalyticsWorkspaceBinding Objects

```python
class AnalyticsWorkspaceBinding(BaseModel)
```

Represents an AnalyticsWorkspaceBinding object

<a id="models.AnalyticsWorkspaceBinding.api_version"></a>

#### api\_version

The API Version in kubernetes to use

<a id="models.AnalyticsWorkspaceBinding.kind"></a>

#### kind

The Kind of object being defined

<a id="models.AnalyticsWorkspaceBinding.metadata"></a>

#### metadata

The metadata surrounding the resource

<a id="models.AnalyticsWorkspaceBinding.spec"></a>

#### spec

The specification of the resource

<a id="models.AnalyticsWorkspaceBinding.status"></a>

#### status

The status of the resource

<a id="models.AnalyticsWorkspace"></a>

## AnalyticsWorkspace Objects

```python
class AnalyticsWorkspace(BaseModel)
```

Represents an AnalyticsWorkspace resource

<a id="models.AnalyticsWorkspace.api_version"></a>

#### api\_version

The API Version in kubernetes to use

<a id="models.AnalyticsWorkspace.kind"></a>

#### kind

The Kind of object being defined

<a id="models.AnalyticsWorkspace.metadata"></a>

#### metadata

The metadata surrounding the resource

<a id="models.AnalyticsWorkspace.spec"></a>

#### spec

The specification of the resource

<a id="models.AnalyticsWorkspace.status"></a>

#### status

The status of the resource

<a id="models.AnalyticsDataSourcePublisherContact"></a>

## AnalyticsDataSourcePublisherContact Objects

```python
class AnalyticsDataSourcePublisherContact(BaseModel)
```

Represents the publisher contact of a datasource object

<a id="models.AnalyticsDataSourcePublisherContact.name"></a>

#### name

The name of the contact

<a id="models.AnalyticsDataSourcePublisherContact.role"></a>

#### role

The role of the contact

<a id="models.AnalyticsDataSourcePublisher"></a>

## AnalyticsDataSourcePublisher Objects

```python
class AnalyticsDataSourcePublisher(BaseModel)
```

Represents the publisher of a datasource object

<a id="models.AnalyticsDataSourcePublisher.organisation"></a>

#### organisation

The organisation publishing the resource

<a id="models.AnalyticsDataSourcePublisher.contact"></a>

#### contact

The contact for the publisher of the resource

<a id="models.AnalyticsDataSourceProject"></a>

## AnalyticsDataSourceProject Objects

```python
class AnalyticsDataSourceProject(BaseModel)
```

Represents the project of a datasource object

<a id="models.AnalyticsDataSourceProject.id"></a>

#### id

The Id of the project for cross reference in other systems

<a id="models.AnalyticsDataSourceConnectionString"></a>

## AnalyticsDataSourceConnectionString Objects

```python
class AnalyticsDataSourceConnectionString(BaseModel)
```

Represents the connection string of a datasource object

<a id="models.AnalyticsDataSourceConnectionString.secret_name"></a>

#### secret\_name

The name of the secret

<a id="models.AnalyticsDataSourceConnectionString.value"></a>

#### value

The value of the connection string

<a id="models.AnalyticsDataSourceSecret"></a>

## AnalyticsDataSourceSecret Objects

```python
class AnalyticsDataSourceSecret(BaseModel)
```

Represents a datasource secret

<a id="models.AnalyticsDataSourceSecret.secret_name"></a>

#### secret\_name

The name of the secret

<a id="models.AnalyticsDataSourceSecretWithKey"></a>

## AnalyticsDataSourceSecretWithKey Objects

```python
class AnalyticsDataSourceSecretWithKey(AnalyticsDataSourceSecret)
```

Represents a datasource secret with a key

<a id="models.AnalyticsDataSourceSecretWithKey.secret_key"></a>

#### secret\_key

The key to use when accessing the secret

<a id="models.AnalyticsDataSourceDataBricksConnection"></a>

## AnalyticsDataSourceDataBricksConnection Objects

```python
class AnalyticsDataSourceDataBricksConnection(BaseModel)
```

Represents a databricks connection

<a id="models.AnalyticsDataSourceDataBricksConnection.host_name"></a>

#### host\_name

The host name of the databricks cluster

<a id="models.AnalyticsDataSourceDataBricksConnection.http_path"></a>

#### http\_path

The path of the databricks cluster

<a id="models.AnalyticsDataSourceDataBricksConnection.personal_access_token"></a>

#### personal\_access\_token

The personal access token to use when connecting if using this auth model

<a id="models.AnalyticsDataSourceDataBricksConnection.oauth2_token"></a>

#### oauth2\_token

The oauth2 token to use when connecting if using this auth model

<a id="models.AnalyticsDataSourceDataBricksConnection.service_principle"></a>

#### service\_principle

The service principle to use when connecting if using this auth model

<a id="models.AnalyticsApproval"></a>

## AnalyticsApproval Objects

```python
class AnalyticsApproval(BaseModel)
```

Represents an analytics approval object

<a id="models.AnalyticsApproval.type"></a>

#### type

The type of approval being given

<a id="models.AnalyticsApproval.name"></a>

#### name

The name of the approver

<a id="models.AnalyticsApproval.email"></a>

#### email

The email of the approver

<a id="models.AnalyticsApproval.job_title"></a>

#### job\_title

The job title of the approver

<a id="models.AnalyticsApproval.approval_given"></a>

#### approval\_given

The date stamp for when approval was given

<a id="models.AnalyticsDataSourceConnection"></a>

## AnalyticsDataSourceConnection Objects

```python
class AnalyticsDataSourceConnection(BaseModel)
```

Represents an connection on a datasource object

<a id="models.AnalyticsDataSourceConnection.type"></a>

#### type

The Type of datasource

<a id="models.AnalyticsDataSourceConnection.name"></a>

#### name

The name of the datasource

<a id="models.AnalyticsDataSourceConnection.connection_string"></a>

#### connection\_string

The connection string for the datasource

<a id="models.AnalyticsDataSourceConnection.databricks_connection"></a>

#### databricks\_connection

The databricks connection to use

<a id="models.AnalyticsDataSourceSpec"></a>

## AnalyticsDataSourceSpec Objects

```python
class AnalyticsDataSourceSpec(BaseModel)
```

represents a spec segment of an AnalyticsDataSource object

<a id="models.AnalyticsDataSourceSpec.type"></a>

#### type

The type of datasource

<a id="models.AnalyticsDataSourceSpec.display_name"></a>

#### display\_name

A short title for the data source

<a id="models.AnalyticsDataSourceSpec.description"></a>

#### description

A description of the data source

<a id="models.AnalyticsDataSourceSpec.license"></a>

#### license

Details of what license this datasource has associated with it

<a id="models.AnalyticsDataSourceSpec.publisher"></a>

#### publisher

The publisher of the datasource

<a id="models.AnalyticsDataSourceSpec.project"></a>

#### project

The project that this data source is associated with

<a id="models.AnalyticsDataSourceSpec.connections"></a>

#### connections

The connections used to access this data

<a id="models.AnalyticsDataSourceSpec.approvals"></a>

#### approvals

List of approvals given for this project

<a id="models.AnalyticsDataSourceBindingStatus"></a>

## AnalyticsDataSourceBindingStatus Objects

```python
class AnalyticsDataSourceBindingStatus(BaseModel)
```

Represents the status segment of a AnalyticsDataSourceBinding object

<a id="models.AnalyticsDataSourceBindingStatus.status_text"></a>

#### status\_text

The current status of the resource

<a id="models.AnalyticsDataSourceStatus"></a>

## AnalyticsDataSourceStatus Objects

```python
class AnalyticsDataSourceStatus(BaseModel)
```

Represents a status of an AnalyticsDataSource object

<a id="models.AnalyticsDataSourceStatus.status_text"></a>

#### status\_text

The current status of the resource

<a id="models.AnalyticsDataSourceStatus.last_active_check"></a>

#### last\_active\_check

The last time that the solution was active

<a id="models.AnalyticsDataSourceBindingSpec"></a>

## AnalyticsDataSourceBindingSpec Objects

```python
class AnalyticsDataSourceBindingSpec(BaseModel)
```

Represents the spec of an AnalyticsDataSourceBinding object

<a id="models.AnalyticsDataSourceBindingSpec.comments"></a>

#### comments

Comments regarding the data source binding

<a id="models.AnalyticsDataSourceBindingSpec.workspace"></a>

#### workspace

The name of the workspace associated with this datasource

<a id="models.AnalyticsDataSourceBindingSpec.expires"></a>

#### expires

When the binding expires

<a id="models.AnalyticsDataSourceBindingSpec.datasource"></a>

#### datasource

The name of the datasource resource

<a id="models.AnalyticsDataSourceBindingSpec.approvals"></a>

#### approvals

The list of approvals for this binding

<a id="models.AnalyticsDataSource"></a>

## AnalyticsDataSource Objects

```python
class AnalyticsDataSource(BaseModel)
```

Represents the AnalyticsDataSource Resource

<a id="models.AnalyticsDataSource.api_version"></a>

#### api\_version

The API Version in kubernetes to use

<a id="models.AnalyticsDataSource.kind"></a>

#### kind

The Kind of object being defined

<a id="models.AnalyticsDataSource.metadata"></a>

#### metadata

The metadata surrounding the resource

<a id="models.AnalyticsDataSource.spec"></a>

#### spec

The specification for the resource

<a id="models.AnalyticsDataSource.status"></a>

#### status

The status of the resource

<a id="models.AnalyticsDataSourceBinding"></a>

## AnalyticsDataSourceBinding Objects

```python
class AnalyticsDataSourceBinding(BaseModel)
```

Represents the AnalyticsDataSourceBinding resource

<a id="models.AnalyticsDataSourceBinding.api_version"></a>

#### api\_version

The API Version in kubernetes to use

<a id="models.AnalyticsDataSourceBinding.kind"></a>

#### kind

The Kind of object being defined

<a id="models.AnalyticsDataSourceBinding.metadata"></a>

#### metadata

The metadata surrounding the resource

<a id="models.AnalyticsDataSourceBinding.spec"></a>

#### spec

The specification for the resource

<a id="models.AnalyticsDataSourceBinding.status"></a>

#### status

The status of the resource

<a id="models.AnalyticsCrateSpecRepository"></a>

## AnalyticsCrateSpecRepository Objects

```python
class AnalyticsCrateSpecRepository(BaseModel)
```

Represents repository on a AnalyticsCrateSpec object

<a id="models.AnalyticsCrateSpecRepository.url"></a>

#### url

The URL of the repository

<a id="models.AnalyticsCrateSpecRepository.branch"></a>

#### branch

The branch to use. Defaults to main branch

<a id="models.AnalyticsCrateSpecRepository.secret_name"></a>

#### secret\_name

The name of the secret resource to use to get the PAT Token.

<a id="models.AnalyticsCrateSpecRepository.secret_key"></a>

#### secret\_key

The key of the secret resource to get the PAT Token.

<a id="models.AnalyticsCrateSpec"></a>

## AnalyticsCrateSpec Objects

```python
class AnalyticsCrateSpec(BaseModel)
```

Represents the spec segment of a AnalyticsCrate Object

<a id="models.AnalyticsCrateSpec.display_name"></a>

#### display\_name

A short title for the resource

<a id="models.AnalyticsCrateSpec.description"></a>

#### description

A short description of the crate

<a id="models.AnalyticsCrateSpec.path"></a>

#### path

The path to the ro-crate metadata file

<a id="models.AnalyticsCrateSpec.repo"></a>

#### repo

The repository where the data relating to this crate is stored

<a id="models.AnalyticsCrateStatus"></a>

## AnalyticsCrateStatus Objects

```python
class AnalyticsCrateStatus(BaseModel)
```

Represents the status field of a AnalyticsCrate object

<a id="models.AnalyticsCrateStatus.status_text"></a>

#### status\_text

The current status of the resource

<a id="models.AnalyticsCrateStatus.commit_id"></a>

#### commit\_id

The commit id for the resource, so we know if it's already been processed

<a id="models.AnalyticsCrateStatus.workspace"></a>

#### workspace

The workspace to associate with this crate

<a id="models.AnalyticsCrate"></a>

## AnalyticsCrate Objects

```python
class AnalyticsCrate(BaseModel)
```

Represents an AnalyticsCrate resource

<a id="models.AnalyticsCrate.api_version"></a>

#### api\_version

The API Version in kubernetes to use

<a id="models.AnalyticsCrate.kind"></a>

#### kind

The Kind of object being defined

<a id="models.AnalyticsCrate.metadata"></a>

#### metadata

The metadata surrounding the resource

<a id="models.AnalyticsCrate.spec"></a>

#### spec

The specification of this resource

<a id="models.AnalyticsCrate.status"></a>

#### status

The status of this resource

---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
---
title: lscsde-workspace-mgmt package
parent: Python Module
layout: page
grand_parent: Analytics Workspace Management Services
---

The following are the classes that are part of the lscsde-workspace-mgmt python package
<a id="workspacebindingclient.AnalyticsWorkspaceBindingClient"></a>

## AnalyticsWorkspaceBindingClient Objects

```python
class AnalyticsWorkspaceBindingClient(KubernetesNamespacedCustomClient)
```

Client for interacting with AnalyticsWorkspaceBindings

<a id="workspacebindingclient.AnalyticsWorkspaceBindingClient.get"></a>

#### get

```python
async def get(namespace, name)
```

Gets a specific AnalyticsWorkspaceBinding resource

<a id="workspacebindingclient.AnalyticsWorkspaceBindingClient.list"></a>

#### list

```python
async def list(namespace, **kwargs)
```

Lists AnalyticsWorkspaceBinding resources in the namespace supplied

<a id="workspacebindingclient.AnalyticsWorkspaceBindingClient.list_by_username"></a>

#### list\_by\_username

```python
async def list_by_username(namespace, username)
```

Lists AnalyticsWorkspaceBinding resources in the namespace supplied that match the username

If the label doesn't exist, it will be patched into the definition to increase performance in etcd

<a id="workspacebindingclient.AnalyticsWorkspaceBindingClient.create"></a>

#### create

```python
async def create(body: AnalyticsWorkspaceBinding, append_label: bool = True)
```

Creates a AnalyticsWorkspaceBinding resource in the namespace supplied

<a id="workspacebindingclient.AnalyticsWorkspaceBindingClient.patch"></a>

#### patch

```python
async def patch(namespace: str = None,
                name: str = None,
                patch_body: dict = None,
                body: AnalyticsWorkspaceBinding = None)
```

Patches a AnalyticsWorkspaceBinding resource in the namespace supplied

<a id="workspacebindingclient.AnalyticsWorkspaceBindingClient.patch_status"></a>

#### patch\_status

```python
async def patch_status(namespace: str, name: str,
                       status: AnalyticsWorkspaceBindingStatus)
```

Patches the status of a AnalyticsWorkspaceBinding resource in the namespace supplied

<a id="workspacebindingclient.AnalyticsWorkspaceBindingClient.replace"></a>

#### replace

```python
async def replace(body: AnalyticsWorkspaceBinding, append_label: bool = True)
```

Replaces a AnalyticsWorkspaceBinding resource with the one supplied

<a id="workspacebindingclient.AnalyticsWorkspaceBindingClient.delete"></a>

#### delete

```python
async def delete(body: AnalyticsWorkspaceBinding = None,
                 namespace: str = None,
                 name: str = None)
```

Deletes a AnalyticsWorkspaceBinding resource in the namespace supplied

