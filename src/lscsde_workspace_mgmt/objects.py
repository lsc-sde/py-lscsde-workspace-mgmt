from datetime import datetime, timedelta
from kubernetes_asyncio.client.models import V1ObjectMeta

class KubernetesObject:
    def __init__(self, response : dict, api_version : str, kind : str):
        metadata = response.get("metadata", {})
        self.api_version = api_version
        self.kind = kind
        self.metadata = V1ObjectMeta(
            name=metadata.get("name"),
            namespace=metadata.get("namespace"),
            annotations=metadata.get("annotations"),
            labels=metadata.get("labels")
        )

    def to_dictionary(self):
        contents = {}
        contents["apiVersion"] = self.api_version
        contents["kind"] = self.kind
        contents["metadata"] = {}
        contents["metadata"]["name"] = self.metadata.name
        contents["metadata"]["namespace"] = self.metadata.namespace
        contents["metadata"]["annotations"] = self.metadata.annotations
        contents["metadata"]["labels"] = self.metadata.labels
        return contents 

class AnalyticsWorkspaceValidity:
    def __init__(self, json : dict):
        self.available_from = json.get("availableFrom", "1900-01-01")
        self.expires = json.get("expires", "1900-01-01")        

    def to_dictionary(self):
        contents = {}
        contents["availableFrom"] = self.available_from
        contents["expires"] = self.expires
        return contents 

class VirtualMachineWorkspaceSpec:
    def __init__(self, json : dict):
        self.max_hosts : int = json.get("maxHosts")

    def to_dictionary(self):
        contents = {}
        contents["maxHosts"] = self.max_hosts
        return contents 
        
class JupyterWorkspaceStorage:
    def __init__(self, json : dict):
        self.mount_path : str = json.get("mountPath")
        self.persistent_volume_claim = json.get("persistentVolumeClaim")
        self.storage_class_name = json.get("storageClassName")

    def to_dictionary(self):
        contents = {}
        contents["mountPath"] = self.mount_path
        contents["persistentVolumeClaim"] = self.persistent_volume_claim
        contents["storageClassName"] = self.storage_class_name
        return contents 

class JupyterWorkspaceSpec:
    def __init__(self, json : dict):
        self.image : str = json.get("image")
        self.extra_labels : dict = json.get("extraLabels", {})
        self.default_uri : str = json.get("defaultUri")
        self.node_selector : dict = json.get("nodeSelector")
        self.tolerations : dict = json.get("tolerations")
        self.resources : dict = json.get("resources")
        self.additional_storage = []
        additional_storage_json : list = json.get("additionalStorage")
        if additional_storage_json:
            for storage in additional_storage_json:
                self.additional_storage.append(JupyterWorkspaceStorage(storage))

    def to_dictionary(self):
        contents = {}
        contents["image"] = self.image
        if self.extra_labels:
            contents["extraLabels"] = self.extra_labels
        
        if self.default_uri:
            contents["defaultUri"] = self.default_uri
        
        if self.node_selector:
            contents["nodeSelector"] = self.node_selector

        if self.tolerations:
            contents["tolerations"] = self.tolerations

        if self.resources:
            contents["resources"] = self.resources

        if self.additional_storage:
            additional_storage = []
            for storage in self.additional_storage:
                additional_storage.append(storage.to_dictionary())
            contents["additionalStorage"] = additional_storage
        return contents 

class AnalyticsWorkspace(KubernetesObject):
    def __init__(self, response : dict, api_version : str, kind : str):
         super().__init__(response, api_version, kind)
         self.spec = AnalyticsWorkspaceSpec(response.get("spec", {}))

    def to_dictionary(self):
        contents = super().to_dictionary()
        contents["spec"] = self.spec.to_dictionary()
        return contents 


class AnalyticsWorkspaceSpec:
    def __init__(self, json : dict):
        self.display_name : str = json.get("displayName")
        self.description : str = json.get("description")
        self.validity = AnalyticsWorkspaceValidity(json.get("validity", {}))

        jupyter_workspace = json.get("jupyterWorkspace", {})
        if jupyter_workspace:
            self.jupyter_workspace = JupyterWorkspaceSpec(jupyter_workspace)

        virtual_machine_workspace = json.get("virtualMachineWorkspace", {})
        self.virtual_machine_workspace : VirtualMachineWorkspaceSpec = None

        if virtual_machine_workspace:
            self.virtual_machine_workspace = VirtualMachineWorkspaceSpec(virtual_machine_workspace)
    
    def to_dictionary(self):
        contents = {}
        contents["displayName"] = self.display_name
        contents["description"] = self.description
        contents["validity"] = self.validity.to_dictionary()
        if self.virtual_machine_workspace:
            contents["virtualMachineWorkspace"] = self.virtual_machine_workspace.to_dictionary()

        if self.jupyter_workspace:
            contents["jupyterWorkspace"] = self.jupyter_workspace.to_dictionary()
        
        return contents
    
class AnalyticsWorkspaceBindingClaim:
    def __init__(self, json : dict):
        self.name = json.get("name")
        self.operator = json.get("operator", "EQUALS")
        self.value = json.get("value")

    def to_dictionary(self):
        contents = {}
        contents["name"] = self.name
        contents["operator"] = self.operator
        contents["value"] = self.value
        return contents


class AnalyticsWorkspaceBinding(KubernetesObject):
    def __init__(self, response : dict, api_version : str, kind : str):
         super().__init__(response, api_version, kind)
         self.spec = AnalyticsWorkspaceBindingSpec(response["spec"])

    def to_dictionary(self):
        contents = super().to_dictionary()
        contents["spec"] = self.spec.to_dictionary()
        return contents

class AnalyticsWorkspaceBindingSpec:
    def __init__(self, json : dict):
        self.workspace = json.get("workspace")
        self.expires = json.get("expires")
        self.username = json.get("username")
        self.claims = []
        claims = json.get("claims")
        if claims:
            self.claims = [AnalyticsWorkspaceBindingClaim(claim) for claim in claims]
                

    def to_dictionary(self):
        contents = {}
        contents["workspace"] = self.workspace
        
        if self.expires:
            contents["expires"] = self.expires
        
        if self.username:
            contents["username"] = self.username

        if self.claims:
            claims = [claim.to_dictionary() for claim in claims]
        
        return contents

class WorkspaceVolumeStatus:
    def __init__(self, name : str, namespace: str, exists : bool):
        self.name = name
        self.exists = exists
        self.namespace = namespace
        