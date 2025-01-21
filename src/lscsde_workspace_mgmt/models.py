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
    """Name of the resource in kubernetes"""
    
    namespace : Optional[str] = Field(default="default")
    """Namespace that the resource is deployed to in kubernetes"""

    annotations : Optional[dict[str, str]] = Field(default={})
    """A dictionary of any annotations assigned to the resource in kubernetes"""

    labels : Optional[dict[str, str]] = Field(default={})
    """A dictionary of any labels assigned to the resource in kubernetes"""

    resource_version : Optional[str] = Field(alias="resourceVersion", default=None)
    """The version of the resource in kubernetes"""

class AnalyticsWorkspaceValidity(BaseModel):
    """
    Represents the validity of the a workspace

    https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacevalidity
    """

    available_from : Optional[str] = Field(alias="availableFrom")
    """The date that the workspace is valid from (in open API date format)"""

    expires : Optional[str] = Field()
    """The date that the workspace expires"""

class VirtualMachineWorkspaceSpec(BaseModel):
    """
    https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacevirtualmachine
    """
    
    max_hosts : Optional[int] = Field(alias="maxHosts")
    """ The maximum number of hosts"""

class JupyterWorkspaceStorage(BaseModel):
    """
    https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspaceadditionalstorage    
    """
    
    mount_path : Optional[str] = Field(alias="mountPath", default=None)
    """The directory to mount this storage in the claim"""

    persistent_volume_claim : Optional[str] = Field(alias="persistentVolumeClaim", default=None)
    """The name of the persistent volume claim to apply"""

    storage_class_name : Optional[str] = Field(alias="storageClassName", default=None)
    """The storage class name applied to the persistent volume claim (if it doesn’t already exist)."""
    
class JupyterWorkspacePersistentVolumeClaim(BaseModel):
    """
    https://lsc-sde.github.io/lsc-sde/imported/iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.html#analyticsworkspacejupyterworkspacepersistentvolumeclaim
    """

    name : Optional[str] = Field(alias="name", default=None)
    """The name of the default persistent volume claim to associate with this workspace. If not populated, it will use the workspace name to generate a new name for the PVC automatically"""
    
    storage_class_name : Optional[str] = Field(alias="storageClassName", default=None)
    """The name of the storage class to create the persistent volume claim. If not populated, it will default to the system default. This is only applied when a PVC is initially created, it is ignored otherwise."""

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
    """The image used when provisioning the pod created by jupyter hub"""

    extra_labels : Optional[dict[str, str]] = Field(alias="extraLabels", default = None)
    """A map of labels to append to the pod created"""

    default_uri : Optional[str] = Field(alias="defaultUri", default = None)
    """The URI that jupyter will use when the items are provisioned."""

    node_selector : Optional[JupyterWorkspaceSpecNodeSelector]  = Field(alias="nodeSelector", default=None)
    """A dictionary of node selector tags per the kubernetes documentation"""

    tolerations: Optional[list[JupyterWorkspaceSpecToleration]]  = Field(alias="tolerations", default=None)
    """The pods tolerations."""

    resources: Optional[JupyterWorkspaceSpecResources]  = Field(alias="resources", default=None)
    """
    Describes the compute resource requirements.
    
    Per https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ResourceRequirements.md
    """

    additional_storage: Optional[list[JupyterWorkspaceStorage]]  = Field(alias="additionalStorage", default=None)
    """A list of additional persistent volume claims to map to the pods created for this environment."""

    persistent_volume_claim: Optional[JupyterWorkspacePersistentVolumeClaim] = Field(alias="persistentVolumeClaim", default=JupyterWorkspacePersistentVolumeClaim())
    """A description of the persistent volume claim provisioned for the workspace"""

class AnalyticsWorkspaceStatus(BaseModel):
    """
    Represents the status field of the analyticsworkspace resource
    """

    status_text : Optional[str] = Field(alias="statusText", default="Waiting")
    """A text field describing the current status of the workspace"""

    persistent_volume_claim : Optional[str] = Field(alias="persistentVolumeClaim", default=None)
    """The name of the assigned pvc for the workspace (if none provided)"""

    additional_storage : Optional[dict[str, str]] = Field(alias="additionalStorage", default=None)
    """A dictionary containing the name of the various additional storage associated with the workspace"""

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
    """The short display name used as the title for the workspace."""

    description : Optional[str] = Field(alias="description", default=None)
    """A simple description which can be multiple lines describing the workspace"""

    validity : Optional[AnalyticsWorkspaceValidity] = Field(alias="validity", default=None)
    """An object describing variables which are validated to ensure that the workspace is still valid"""

    jupyter_workspace : Optional[JupyterWorkspaceSpec] = Field(alias="jupyterWorkspace", default=JupyterWorkspaceSpec())
    """Represents a jupyter workspace"""

    virtual_machine_workspace : Optional[VirtualMachineWorkspaceSpec] = Field(alias="virtualMachineWorkspace", default=None)
    """This is not yet implemented, it is to test validation of the CRD is functioning correctly"""
    
class AnalyticsWorkspaceBindingClaim(BaseModel):
    """
    Represents the claims segment on a AnalyticsWorkspaceBinding resource
    
    This has not yet been implemented
    """

    name : Optional[str] = Field(alias="name", default=None)
    """The name of the claim"""

    operator : Optional[str] = Field(alias="operator", default=None)
    """The operator to test against"""

    value : Optional[str] = Field(alias="value", default=None)
    """The value to look for"""

class AnalyticsWorkspaceBindingSpec(BaseModel):
    """
    Represents the spec segment of an AnalyticsWorkspaceBinding resource
    """

    workspace : Optional[str] = Field(alias="workspace", default=None)
    """
    The name of the workspace in kubernetes. 
    
    It is assumed that the workspace will be located in the same namespace as the current binding
    """

    expires : Optional[str] = Field(alias="expires", default=None)
    """The date at which this binding expires"""

    username : Optional[str] = Field(alias="username", default=None)
    """The username to match"""

    comments : Optional[str] = Field(alias="comments", default=None)
    """Any comments relating to this binding."""

    claims : Optional[list[AnalyticsWorkspaceBindingClaim]] = Field(alias="claims", default=None)
    """This is not yet implemented"""

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
    """The API Version in kubernetes to use"""

    kind : Optional[str] = Field(alias="kind", default="AnalyticsWorkspaceBinding")
    """The Kind of object being defined"""

    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    """The metadata surrounding the resource"""

    spec : Optional[AnalyticsWorkspaceBindingSpec] = Field(alias="spec", default=AnalyticsWorkspaceBindingSpec())
    """The specification of the resource"""

    status : Optional[AnalyticsWorkspaceBindingStatus] = Field(alias="status", default=AnalyticsWorkspaceBindingStatus())
    """The status of the resource"""

class AnalyticsWorkspace(BaseModel):
    """
    Represents an AnalyticsWorkspace resource
    """
    api_version : Optional[str] = Field(alias="apiVersion", default="xlscsde.nhs.uk/v1")
    """The API Version in kubernetes to use"""

    kind : Optional[str] = Field(alias="kind", default="AnalyticsWorkspace")
    """The Kind of object being defined"""

    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    """The metadata surrounding the resource"""

    spec : Optional[AnalyticsWorkspaceSpec] = Field(alias="spec", default=AnalyticsWorkspaceSpec())
    """The specification of the resource"""

    status : Optional[AnalyticsWorkspaceStatus] = Field(alias="status", default = AnalyticsWorkspaceStatus())
    """The status of the resource"""

class AnalyticsDataSourcePublisherContact(BaseModel):
    """
    Represents the publisher contact of a datasource object
    """

    name : Optional[str] = Field(alias="name", default=None)
    """The name of the contact"""

    role : Optional[str] = Field(alias="role", default=None)
    """The role of the contact"""

class AnalyticsDataSourcePublisher(BaseModel):
    """
    Represents the publisher of a datasource object
    """
    organisation : Optional[str] = Field(alias="organisation", default=None)
    """The organisation publishing the resource"""

    contact : Optional[AnalyticsDataSourcePublisherContact] = Field(alias="contact", default=AnalyticsDataSourcePublisherContact())
    """The contact for the publisher of the resource"""

class AnalyticsDataSourceProject(BaseModel):
    """
    Represents the project of a datasource object
    """

    id : Optional[str] = Field(alias="id", default=None)
    """The Id of the project for cross reference in other systems"""
    
class AnalyticsDataSourceConnectionString(BaseModel):
    """
    Represents the connection string of a datasource object
    """

    secret_name : Optional[str] = Field(alias="secretName", default=None)
    """The name of the secret"""

    value : Optional[str] = Field(alias="value", default=None)
    """The value of the connection string"""


class AnalyticsDataSourceSecret(BaseModel):
    """
    Represents a datasource secret
    """

    secret_name : Optional[str] = Field(alias="secretName", default=None)
    """The name of the secret"""

class AnalyticsDataSourceSecretWithKey(AnalyticsDataSourceSecret):
    """
    Represents a datasource secret with a key
    """

    secret_key : Optional[str] = Field(alias="secretKey", default=None)
    """The key to use when accessing the secret"""

class AnalyticsDataSourceDataBricksConnection(BaseModel):
    """
    Represents a databricks connection 
    """
    
    host_name : Optional[str] = Field(alias="hostName", default=None)
    """The host name of the databricks cluster"""

    http_path : Optional[str] = Field(alias="httpPath", default=None)
    """The path of the databricks cluster"""

    personal_access_token : Optional[AnalyticsDataSourceSecretWithKey] = Field(alias="personalAccessToken", default=None)
    """The personal access token to use when connecting if using this auth model"""

    oauth2_token : Optional[AnalyticsDataSourceSecretWithKey] = Field(alias="oauth2Token", default=None)
    """The oauth2 token to use when connecting if using this auth model"""

    service_principle : Optional[AnalyticsDataSourceSecret] = Field(alias="servicePrinciple", default=None)
    """The service principle to use when connecting if using this auth model"""

class AnalyticsApproval(BaseModel):
    """
    Represents an analytics approval object
    """

    type : Optional[str] = Field(alias="type", default=None)
    """The type of approval being given"""

    name : Optional[str] = Field(alias="name", default=None)
    """The name of the approver"""

    email : Optional[str] = Field(alias="email", default=None)
    """The email of the approver"""

    job_title : Optional[str] = Field(alias="jobTitle", default=None)
    """The job title of the approver"""

    approval_given : Optional[str] = Field(alias="approvalGiven", default=None)
    """The date stamp for when approval was given"""

class AnalyticsDataSourceConnection(BaseModel):
    """
    Represents an connection on a datasource object
    """

    type : Optional[str] = Field(alias="type", default=None)
    """The Type of datasource"""

    name : Optional[str] = Field(alias="name", default=None)
    """The name of the datasource"""

    connection_string : Optional[AnalyticsDataSourceConnectionString] = Field(alias="connectionString", default=None)
    """The connection string for the datasource"""

    databricks_connection : Optional[AnalyticsDataSourceDataBricksConnection] = Field(alias="databricksConnection", default=None)
    """The databricks connection to use"""

class AnalyticsDataSourceSpec(BaseModel):
    """
    represents a spec segment of an AnalyticsDataSource object
    """

    type : Optional[str] = Field(alias="type", default="Uploaded")
    """The type of datasource"""

    display_name : Optional[str] = Field(alias="displayName", default=None)
    """A short title for the data source"""

    description : Optional[str] = Field(alias="description", default=None)
    """A description of the data source"""

    license : Optional[str] = Field(alias="license", default=None)
    """Details of what license this datasource has associated with it"""

    publisher : Optional[AnalyticsDataSourcePublisher] = Field(alias="publisher", default=AnalyticsDataSourcePublisher())
    """The publisher of the datasource"""

    project : Optional[AnalyticsDataSourceProject] = Field(alias="project", default=AnalyticsDataSourceProject())
    """The project that this data source is associated with"""

    connections : Optional[list[AnalyticsDataSourceConnection]] = Field(alias="connections", default=None)
    """The connections used to access this data"""

    approvals : Optional[list[AnalyticsApproval]] = Field(alias="approvals", default=None)
    """List of approvals given for this project"""

class AnalyticsDataSourceBindingStatus(BaseModel):
    """
    Represents the status segment of a AnalyticsDataSourceBinding object
    """

    status_text : Optional[str] = Field(alias="statusText", default="Waiting")
    """The current status of the resource"""

class AnalyticsDataSourceStatus(BaseModel):
    """
    Represents a status of an AnalyticsDataSource object
    """

    status_text : Optional[str] = Field(alias="statusText", default="Waiting")
    """The current status of the resource"""

    last_active_check : Optional[str] = Field(alias="lastActiveCheck", default="Waiting")
    """The last time that the solution was active"""

class AnalyticsDataSourceBindingSpec(BaseModel):
    """
    Represents the spec of an AnalyticsDataSourceBinding object
    """

    comments : Optional[str] = Field(alias="comments", default=None)
    """Comments regarding the data source binding"""

    workspace : Optional[str] = Field(alias="workspace", default=None)
    """The name of the workspace associated with this datasource"""

    expires : Optional[str] = Field(alias="expires", default=None)
    """When the binding expires"""

    datasource : Optional[str] = Field(alias="datasource", default=None)
    """The name of the datasource resource"""

    approvals : Optional[list[AnalyticsApproval]] = Field(alias="approvals", default=None)
    """The list of approvals for this binding"""

class AnalyticsDataSource(BaseModel):
    """
    Represents the AnalyticsDataSource Resource
    """
    api_version : Optional[str] = Field(alias="apiVersion", default="xlscsde.nhs.uk/v1")
    """The API Version in kubernetes to use"""

    kind : Optional[str] = Field(alias="kind", default="AnalyticsDataSource")
    """The Kind of object being defined"""

    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    """The metadata surrounding the resource"""

    spec : Optional[AnalyticsDataSourceSpec] = Field(alias="spec", default=AnalyticsDataSourceSpec())
    """The specification for the resource"""

    status : Optional[AnalyticsDataSourceStatus] = Field(alias="status", default = AnalyticsDataSourceStatus())
    """The status of the resource"""

class AnalyticsDataSourceBinding(BaseModel):
    """
    Represents the AnalyticsDataSourceBinding resource
    """

    api_version : Optional[str] = Field(alias="apiVersion", default="xlscsde.nhs.uk/v1")
    """The API Version in kubernetes to use"""

    kind : Optional[str] = Field(alias="kind", default="AnalyticsDataSourceBinding")
    """The Kind of object being defined"""

    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    """The metadata surrounding the resource"""

    spec : Optional[AnalyticsDataSourceBindingSpec] = Field(alias="spec", default=AnalyticsDataSourceBindingSpec())
    """The specification for the resource"""

    status : Optional[AnalyticsDataSourceBindingStatus] = Field(alias="status", default = AnalyticsDataSourceBindingStatus())
    """The status of the resource"""

class AnalyticsCrateSpecRepository(BaseModel):
    """
    Represents repository on a AnalyticsCrateSpec object
    """
    
    url : Optional[str] = Field(alias="url", default=None)
    """The URL of the repository"""
    
    branch : Optional[str] = Field(alias="branch", default="main")
    """The branch to use. Defaults to main branch"""

    secret_name : Optional[str] = Field(alias="secretName", default=None)
    """The name of the secret resource to use to get the PAT Token."""

    secret_key : Optional[str] = Field(alias="secretKey", default=None)
    """The key of the secret resource to get the PAT Token."""

class AnalyticsCrateSpec(BaseModel):
    """
    Represents the spec segment of a AnalyticsCrate Object
    """
    
    display_name : Optional[str] = Field(alias="displayName", default=None)
    """A short title for the resource"""

    description : Optional[str] = Field(alias="description", default=None)
    """A short description of the crate"""

    path : Optional[str] = Field(alias="path", default="/ro-crate-metadata.json")
    """The path to the ro-crate metadata file"""

    repo : Optional[AnalyticsCrateSpecRepository] = Field(alias="repo", default=None)
    """The repository where the data relating to this crate is stored"""
        
class AnalyticsCrateStatus(BaseModel):
    """
    Represents the status field of a AnalyticsCrate object
    """

    status_text : Optional[str] = Field(alias="statusText", default=None)
    """The current status of the resource"""

    commit_id : Optional[str] = Field(alias="commitId", default=None)
    """The commit id for the resource, so we know if it's already been processed"""

    workspace : Optional[str] = Field(alias="workspace", default=None)
    """The workspace to associate with this crate"""

class AnalyticsCrate(BaseModel):
    """
    Represents an AnalyticsCrate resource
    """
    api_version : Optional[str] = Field(alias="apiVersion", default="xlscsde.nhs.uk/v1")
    """The API Version in kubernetes to use"""

    kind : Optional[str] = Field(alias="kind", default="AnalyticsDataSourceBinding")
    """The Kind of object being defined"""

    metadata : Optional[KubernetesMetadata] = Field(alias="metadata", default=KubernetesMetadata())
    """The metadata surrounding the resource"""

    spec : Optional[AnalyticsCrateSpec] = Field(alias="spec", default=AnalyticsCrateSpec())
    """The specification of this resource"""
    
    status : Optional[AnalyticsCrateStatus] = Field(alias="status", default = AnalyticsCrateStatus())
    """The status of this resource"""
