from datetime import date,datetime, timedelta
from kubernetes_asyncio.client.models import V1ObjectMeta
from .exceptions import InvalidLabelFormatException
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter
from typing_extensions import TypedDict
from typing import Optional
from pydantic.dataclasses import dataclass
import re 
import json

class KubernetesHelper:
    """
    A helper to help us interact with kubernetes as it would like
    """
    
    def format_as_label(self, username : str):
        """
        reformats a string to make it compatible for use in kubernetes label field
        """
        formatted = re.sub('[^0-9a-z.]+', '___', username.casefold())
        validation_expression = '^(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])?$'
        if not re.match(pattern = validation_expression, string = formatted):
            raise InvalidLabelFormatException(f"Invalid value: \"{formatted}\": a valid label must be an empty string or consist of alphanumeric characters, '-', '_' or '.', and must start and end with an alphanumeric character (e.g. 'MyValue',  or 'my_value',  or '12345', regex used for validation is '{validation_expression}')")
        return formatted

class KubernetesMetadata(BaseModel):
    """
    A standard Kubernetes Metadata object
    """

    name : Optional[str] = Field(default="")
    namespace : Optional[str] = Field(default="default")
    annotations : Optional[dict[str, str]] = Field(default={})
    labels : Optional[dict[str, str]] = Field(default={})
    resource_version : Optional[str] = Field(alias="resourceVersion", default=None)

class AnalyticsWorkspaceValidity(BaseModel):
    """
    Represents the validity of the a workspace

    https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacevalidity
    """

    available_from : Optional[str] = Field(alias="availableFrom")
    expires : Optional[str] = Field()

class VirtualMachineWorkspaceSpec(BaseModel):
    """
    https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacevirtualmachine
    """
    max_hosts : Optional[int] = Field(alias="maxHosts")

class JupyterWorkspaceStorage(BaseModel):
    """
    https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspaceadditionalstorage    
    """
    mount_path : Optional[str] = Field(alias="mountPath", default=None)
    persistent_volume_claim : Optional[str] = Field(alias="persistentVolumeClaim", default=None)
    storage_class_name : Optional[str] = Field(alias="storageClassName", default=None)
    
class JupyterWorkspacePersistentVolumeClaim(BaseModel):
    """
    https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspacepersistentvolumeclaim
    """
    name : Optional[str] = Field(alias="name", default=None)
    storage_class_name : Optional[str] = Field(alias="storageClassName", default=None)

class JupyterWorkspaceSpecResources(TypedDict):
    """
    Represents the resources object on a jupyter workspace
    
    TODO: This needs to be converted to use https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ResourceRequirements.md
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

class JupyterWorkspaceSpecNodeSelector(TypedDict):
    """
    Represents a node selector
    
    TODO: Convert to a dict of strings of a jupyter workspace
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

class JupyterWorkspaceSpecToleration(BaseModel):
    """
    Represents a toleration property of a jupyter workspace
    
    TODO: This needs to be converted to use https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Toleration.md
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

class JupyterWorkspaceSpec(BaseModel):
    """
    Represents the jupyterWorkspace property

    https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspace
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

    image : Optional[str] = Field(default=None)
    extra_labels : Optional[dict[str, str]] = Field(alias="extraLabels", default = None)
    default_uri : Optional[str] = Field(alias="defaultUri", default = None)
    node_selector : Optional[JupyterWorkspaceSpecNodeSelector]  = Field(alias="nodeSelector", default=None)
    tolerations: Optional[list[JupyterWorkspaceSpecToleration]]  = Field(alias="tolerations", default=None)
    resources: Optional[JupyterWorkspaceSpecResources]  = Field(alias="resources", default=None)
    additional_storage: Optional[list[JupyterWorkspaceStorage]]  = Field(alias="additionalStorage", default=None)
    persistent_volume_claim: Optional[JupyterWorkspacePersistentVolumeClaim] = Field(alias="persistentVolumeClaim", default=JupyterWorkspacePersistentVolumeClaim())

class AnalyticsWorkspaceStatus(BaseModel):
    """
    Represents the status field of the analyticsworkspace resource
    """
    status_text : Optional[str] = Field(alias="statusText", default="Waiting")
    persistent_volume_claim : Optional[str] = Field(alias="persistentVolumeClaim", default=None)
    additional_storage : Optional[dict[str, str]] = Field(alias="additionalStorage", default=None)

class AnalyticsWorkspaceBindingStatus(BaseModel):
    """
    Represents the status field of the analyticsworkspacebinding resource
    """
    status_text : Optional[str] = Field(alias="statusText", default="Waiting")


class AnalyticsWorkspaceSpec(BaseModel):
    """
    Represents the spec segment of the analyticsworkspace resource
    """
    display_name : Optional[str] = Field(alias="displayName", default=None)
    description : Optional[str] = Field(alias="description", default=None)
    validity : Optional[AnalyticsWorkspaceValidity] = Field(alias="validity", default=None)
    jupyter_workspace : Optional[JupyterWorkspaceSpec] = Field(alias="jupyterWorkspace", default=JupyterWorkspaceSpec())
    virtual_machine_workspace : Optional[VirtualMachineWorkspaceSpec] = Field(alias="virtualMachineWorkspace", default=None)
    
class AnalyticsWorkspaceBindingClaim(BaseModel):
    """
    Represents the claims segment on a AnalyticsWorkspaceBinding resource
    
    This has not yet been implemented
    """
    name : Optional[str] = Field(alias="name", default=None)
    operator : Optional[str] = Field(alias="operator", default=None)
    value : Optional[str] = Field(alias="value", default=None)

class AnalyticsWorkspaceBindingSpec(BaseModel):
    """
    Represents the spec segment of an AnalyticsWorkspaceBinding resource
    """
    workspace : Optional[str] = Field(alias="workspace", default=None)
    expires : Optional[str] = Field(alias="expires", default=None)
    username : Optional[str] = Field(alias="username", default=None)
    comments : Optional[str] = Field(alias="comments", default=None)
    claims : Optional[list[AnalyticsWorkspaceBindingClaim]] = Field(alias="claims", default=None)

    def username_as_label(self):
        """
        Reads the username formatted as a kubernetes label
        """
        helper = KubernetesHelper()
        return helper.format_as_label(self.username) 

class AnalyticsWorkspaceBinding(BaseModel):
    """
    Represents an AnalyticsWorkspaceBinding object
    """
    api_version : Optional[str] = Field(alias="apiVersion", default="xlscsde.nhs.uk/v1")
    kind : Optional[str] = Field(alias="kind", default="AnalyticsWorkspaceBinding")
    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    spec : Optional[AnalyticsWorkspaceBindingSpec] = Field(alias="spec", default=AnalyticsWorkspaceBindingSpec())
    status : Optional[AnalyticsWorkspaceBindingStatus] = Field(alias="status", default=AnalyticsWorkspaceBindingStatus())

class AnalyticsWorkspace(BaseModel):
    """
    Represents an AnalyticsWorkspace resource
    """
    api_version : Optional[str] = Field(alias="apiVersion", default="xlscsde.nhs.uk/v1")
    kind : Optional[str] = Field(alias="kind", default="AnalyticsWorkspace")
    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    spec : Optional[AnalyticsWorkspaceSpec] = Field(alias="spec", default=AnalyticsWorkspaceSpec())
    status : Optional[AnalyticsWorkspaceStatus] = Field(alias="status", default = AnalyticsWorkspaceStatus())

class AnalyticsDataSourcePublisherContact(BaseModel):
    """
    Represents the publisher contact of a datasource object
    """
    name : Optional[str] = Field(alias="name", default=None)
    role : Optional[str] = Field(alias="role", default=None)

class AnalyticsDataSourcePublisher(BaseModel):
    """
    Represents the publisher of a datasource object
    """
    organisation : Optional[str] = Field(alias="organisation", default=None)
    contact : Optional[AnalyticsDataSourcePublisherContact] = Field(alias="contact", default=AnalyticsDataSourcePublisherContact())

class AnalyticsDataSourceProject(BaseModel):
    """
    Represents the project of a datasource object
    """
    id : Optional[str] = Field(alias="id", default=None)
    
class AnalyticsDataSourceConnectionString(BaseModel):
    """
    Represents the connection string of a datasource object
    """
    secret_name : Optional[str] = Field(alias="secretName", default=None)
    value : Optional[str] = Field(alias="value", default=None)


class AnalyticsDataSourceSecret(BaseModel):
    """
    Represents a datasource secret
    """
    secret_name : Optional[str] = Field(alias="secretName", default=None)

class AnalyticsDataSourceSecretWithKey(AnalyticsDataSourceSecret):
    """
    Represents a datasource secret with a key
    """
    secret_key : Optional[str] = Field(alias="secretKey", default=None)

class AnalyticsDataSourceDataBricksConnection(BaseModel):
    """
    Represents a databricks connection 
    """
    host_name : Optional[str] = Field(alias="hostName", default=None)
    http_path : Optional[str] = Field(alias="httpPath", default=None)
    personal_access_token : Optional[AnalyticsDataSourceSecretWithKey] = Field(alias="personalAccessToken", default=None)
    oauth2_token : Optional[AnalyticsDataSourceSecretWithKey] = Field(alias="oauth2Token", default=None)
    service_principle : Optional[AnalyticsDataSourceSecret] = Field(alias="servicePrinciple", default=None)

class AnalyticsApproval(BaseModel):
    """
    Represents an analytics approval object
    """
    type : Optional[str] = Field(alias="type", default=None)
    name : Optional[str] = Field(alias="name", default=None)
    email : Optional[str] = Field(alias="email", default=None)
    job_title : Optional[str] = Field(alias="jobTitle", default=None)
    approval_given : Optional[str] = Field(alias="approvalGiven", default=None)

class AnalyticsDataSourceConnection(BaseModel):
    """
    Represents an connection on a datasource object
    """
    type : Optional[str] = Field(alias="type", default=None)
    name : Optional[str] = Field(alias="name", default=None)
    connection_string : Optional[AnalyticsDataSourceConnectionString] = Field(alias="connectionString", default=None)
    databricks_connection : Optional[AnalyticsDataSourceDataBricksConnection] = Field(alias="databricksConnection", default=None)

class AnalyticsDataSourceSpec(BaseModel):
    """
    represents a spec segment of an AnalyticsDataSource object
    """
    type : Optional[str] = Field(alias="type", default="Uploaded")
    display_name : Optional[str] = Field(alias="displayName", default=None)
    description : Optional[str] = Field(alias="description", default=None)
    license : Optional[str] = Field(alias="license", default=None)
    publisher : Optional[AnalyticsDataSourcePublisher] = Field(alias="publisher", default=AnalyticsDataSourcePublisher())
    project : Optional[AnalyticsDataSourceProject] = Field(alias="project", default=AnalyticsDataSourceProject())
    connections : Optional[list[AnalyticsDataSourceConnection]] = Field(alias="connections", default=None)
    approvals : Optional[list[AnalyticsApproval]] = Field(alias="approvals", default=None)

class AnalyticsDataSourceBindingStatus(BaseModel):
    """
    Represents the status segment of a AnalyticsDataSourceBinding object
    """
    status_text : Optional[str] = Field(alias="statusText", default="Waiting")

class AnalyticsDataSourceStatus(BaseModel):
    """
    Represents a status of an AnalyticsDataSource object
    """
    status_text : Optional[str] = Field(alias="statusText", default="Waiting")
    last_active_check : Optional[str] = Field(alias="lastActiveCheck", default="Waiting")

class AnalyticsDataSourceBindingSpec(BaseModel):
    """
    Represents the spec of an AnalyticsDataSourceBinding object
    """
    comments : Optional[str] = Field(alias="comments", default=None)
    workspace : Optional[str] = Field(alias="workspace", default=None)
    expires : Optional[str] = Field(alias="expires", default=None)
    datasource : Optional[str] = Field(alias="datasource", default=None)
    approvals : Optional[list[AnalyticsApproval]] = Field(alias="approvals", default=None)


class AnalyticsDataSource(BaseModel):
    """
    Represents the AnalyticsDataSource Resource
    """
    api_version : Optional[str] = Field(alias="apiVersion", default="xlscsde.nhs.uk/v1")
    kind : Optional[str] = Field(alias="kind", default="AnalyticsDataSource")
    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    spec : Optional[AnalyticsDataSourceSpec] = Field(alias="spec", default=AnalyticsDataSourceSpec())
    status : Optional[AnalyticsDataSourceStatus] = Field(alias="status", default = AnalyticsDataSourceStatus())

class AnalyticsDataSourceBinding(BaseModel):
    """
    Represents the AnalyticsDataSourceBinding resource
    """
    api_version : Optional[str] = Field(alias="apiVersion", default="xlscsde.nhs.uk/v1")
    kind : Optional[str] = Field(alias="kind", default="AnalyticsDataSourceBinding")
    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    spec : Optional[AnalyticsDataSourceBindingSpec] = Field(alias="spec", default=AnalyticsDataSourceBindingSpec())
    status : Optional[AnalyticsDataSourceBindingStatus] = Field(alias="status", default = AnalyticsDataSourceBindingStatus())

class AnalyticsCrateSpecRepository(BaseModel):
    """
    Represents repository on a AnalyticsCrateSpec object
    """
    url : Optional[str] = Field(alias="url", default=None)
    branch : Optional[str] = Field(alias="branch", default="main")
    secret_name : Optional[str] = Field(alias="secretName", default=None)
    secret_key : Optional[str] = Field(alias="secretKey", default=None)

class AnalyticsCrateSpec(BaseModel):
    """
    Represents the spec segment of a AnalyticsCrate Object
    """
    display_name : Optional[str] = Field(alias="displayName", default=None)
    description : Optional[str] = Field(alias="description", default=None)
    path : Optional[str] = Field(alias="path", default="/ro-crate-metadata.json")
    repo : Optional[AnalyticsCrateSpecRepository] = Field(alias="repo", default=None)
        
class AnalyticsCrateStatus(BaseModel):
    """
    Represents the status field of a AnalyticsCrate object
    """
    status_text : Optional[str] = Field(alias="statusText", default=None)
    commit_id : Optional[str] = Field(alias="commitId", default=None)
    workspace : Optional[str] = Field(alias="workspace", default=None)

class AnalyticsCrate(BaseModel):
    """
    Represents an AnalyticsCrate resource
    """
    api_version : Optional[str] = Field(alias="apiVersion", default="xlscsde.nhs.uk/v1")
    kind : Optional[str] = Field(alias="kind", default="AnalyticsDataSourceBinding")
    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    spec : Optional[AnalyticsCrateSpec] = Field(alias="spec", default=AnalyticsCrateSpec())
    status : Optional[AnalyticsCrateStatus] = Field(alias="status", default = AnalyticsCrateStatus())