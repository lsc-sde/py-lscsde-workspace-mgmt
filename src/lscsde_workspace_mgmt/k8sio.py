from logging import Logger
from kubernetes_asyncio import client
from .exceptions import (
    InvalidParameterException
)
from .objects import (
    AnalyticsWorkspace,
    AnalyticsWorkspaceBinding,
    AnalyticsWorkspaceStatus,
    AnalyticsWorkspaceBindingStatus
)
from kubernetes_asyncio.client.models import (
    V1ObjectMeta,
    V1Pod,
    V1Volume,
    V1VolumeMount,
    V1PersistentVolumeClaim,
    V1PersistentVolumeClaimSpec,
    V1PersistentVolumeClaimVolumeSource,
    V1PersistentVolumeClaimList
)

class KubernetesNamespacedCustomClient:
    def __init__(self, k8s_api : client.CustomObjectsApi, log : Logger, group : str, version : str, plural : str, kind : str):
        self.group = group
        self.version = version
        self.plural = plural
        self.kind = kind
        self.api = k8s_api
        self.log : Logger = log

    def get_api_version(self):
        return f"{self.group}/{self.version}"

    async def get(self, namespace, name):
        return await self.api.get_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name
        )
    
    async def list(self, namespace, **kwargs):
        return await self.api.list_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            **kwargs
        )
    
    async def patch(self, namespace : str, name : str, body : dict):
        return await self.api.patch_namespaced_custom_object(
            group = self.group, 
            version = self.version, 
            namespace = namespace,
            plural = self.plural, 
            name = name, 
            body = body
            )
    
    async def patch_status(self, namespace : str, name : str, body : dict):
        return await self.api.patch_namespaced_custom_object_status(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name,
            body = body
        )
    
    async def replace(self, namespace : str, name : str, body : dict):
        return await self.api.replace_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name,
            body = body
        )
    
    async def create(self, namespace : str, body : dict):
        return await self.api.create_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            body = body
        )
    
    async def delete(self, namespace : str, name : str):
        return await self.api.delete_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name
        )

class AnalyticsWorkspaceBindingClient(KubernetesNamespacedCustomClient):
    def __init__(self, k8s_api: client.CustomObjectsApi, log: Logger):
        super().__init__(
            k8s_api = k8s_api, 
            log = log, 
            group = "xlscsde.nhs.uk",
            version = "v1",
            plural = "analyticsworkspacebindings",
            kind = "AnalyticsWorkspaceBinding"
        )

    async def get(self, namespace, name):
        result = await super().get(namespace, name)
        print(result)
        return AnalyticsWorkspaceBinding(result, self.get_api_version(), self.kind)
    
    async def list(self, namespace, **kwargs):
        result = await super().list(namespace, **kwargs)
        return [AnalyticsWorkspaceBinding(item, self.get_api_version(), self.kind) for item in result["items"]]

    def format_username_as_label(self, username : str):
        return username.casefold().replace("@","___")

    async def list_by_username(self, namespace, username):
        formatted_username = self.format_username_as_label(username)
        no_label = await self.list(namespace = namespace, label_selector = f"!xlscsde.nhs.uk/username")
        for item in no_label:
            if item.spec.username:
                if not item.metadata.labels:
                    patch_body = [{"op": "add", "path": "/metadata/labels", "value": { "xlscsde.nhs.uk/username" : self.format_username_as_label(item.spec.username) }}]
                else:
                    patch_body = [{"op": "add", "path": "/metadata/labels/xlscsde.nhs.uk~1username", "value": self.format_username_as_label(item.spec.username) }]

                patch_response = await self.patch(
                    namespace = item.metadata.namespace, 
                    name = item.metadata.name, 
                    patch_body = patch_body
                    )

        return await self.list(namespace = namespace, label_selector = f"xlscsde.nhs.uk/username={self.format_username_as_label(username)}")

    async def create(self, body : AnalyticsWorkspaceBinding):
        contents = body.to_dictionary()
        contents["metadata"]["labels"]["xlscsde.nhs.uk/username"] = self.format_username_as_label(body.spec.username)
        result = await super().create(
            namespace = body.metadata.namespace,
            body = contents
        )
        return AnalyticsWorkspaceBinding(result, self.get_api_version(), self.kind)

    async def patch(self, namespace : str = None, name : str = None, patch_body : dict = None, body : AnalyticsWorkspaceBinding = None):
        if not patch_body:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            patch_body = [
                {"op": "replace", "path": "/spec", "value": body.spec.to_dictionary()},
                {"op": "replace", "path": "/status", "value": body.status.to_dictionary()}
            ]

        if not namespace:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            namespace = body.metadata.namespace

        if not name:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            name = body.metadata.name
            
        result = await super().patch(
            namespace = namespace,
            name = name,
            body = patch_body
        )
        return AnalyticsWorkspaceBinding(result, self.get_api_version(), self.kind)

    async def patch_status(self, namespace : str, name : str, status : AnalyticsWorkspaceBindingStatus):
        body = [{"op": "replace", "path": "/status", "value": status.to_dictionary()}] 
        result = await super().patch_status(
            namespace = namespace,
            name = name,
            body = body
        )
        return AnalyticsWorkspaceBinding(result, self.get_api_version(), self.kind)

    async def replace(self, body : AnalyticsWorkspaceBinding):
        contents = body.to_dictionary()
        contents["metadata"]["labels"]["xlscsde.nhs.uk/username"] = self.format_username_as_label(body.spec.username)
        result = await super().replace(
            namespace = body.metadata.namespace,
            name = body.metadata.name,
            body = contents
        )
        return AnalyticsWorkspaceBinding(result, self.get_api_version(), self.kind)
    
    async def delete(self, body : AnalyticsWorkspaceBinding = None, namespace : str = None, name : str = None):
        if body:
            if not namespace:
                namespace = body.metadata.namespace
            if not name:
                name = body.metadata.name
        
        patch_body = [{"op": "replace", "path": "/status/statusText", "value": "Deleting"}] 

        current = await super().get(namespace, name)
        if not current.get("status"):
            patch_body = [{"op": "add", "path": "/status", "value": { "statusText" : "Deleting" }}] 
            
        await super().patch_status(
            namespace = body.metadata.namespace,
            name = body.metadata.name,
            body = patch_body
        )
        return await super().delete(
            namespace = body.metadata.namespace,
            name = body.metadata.name
        )

class AnalyticsWorkspaceClient(KubernetesNamespacedCustomClient):
    def __init__(self, k8s_api: client.CustomObjectsApi, log: Logger):
        super().__init__(
            k8s_api = k8s_api, 
            log = log, 
            group = "xlscsde.nhs.uk",
            version = "v1",
            plural = "analyticsworkspaces",
            kind = "AnalyticsWorkspace"
        )
        
    async def get(self, namespace, name):
        result = await super().get(namespace, name)
        return AnalyticsWorkspace(result, self.get_api_version(), self.kind)
    
    async def list(self, namespace, **kwargs):
        result = await super().list(namespace, **kwargs)
        return [AnalyticsWorkspace(item, self.get_api_version(), self.kind) for item in result["items"]]
    
    async def create(self, body : AnalyticsWorkspace):
        result = await super().create(
            namespace = body.metadata.namespace,
            body = body.to_dictionary()
        )
        return AnalyticsWorkspace(result, self.get_api_version(), self.kind)

    async def patch(self, namespace : str = None, name : str = None, patch_body : dict = None, body : AnalyticsWorkspace = None):
        if not patch_body:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            patch_body = [
                {"op": "replace", "path": "/spec", "value": body.spec.to_dictionary()},
                {"op": "replace", "path": "/status", "value": body.status.to_dictionary()}
            ]

        if not namespace:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            namespace = body.metadata.namespace

        if not name:
            if not body:
                raise InvalidParameterException("Either namespace, name and patch_body or body must be provided")
            name = body.metadata.name
            
        result = await super().patch(
            namespace = namespace,
            name = name,
            body = patch_body
        )
        return AnalyticsWorkspace(result, self.get_api_version(), self.kind)

    async def patch_status(self, namespace : str, name : str, status : AnalyticsWorkspaceStatus):
        body = [{"op": "replace", "path": "/status", "value": status.to_dictionary()}] 
        result = await super().patch_status(
            namespace = namespace,
            name = name,
            body = body
        )
        return AnalyticsWorkspace(result, self.get_api_version(), self.kind)

    async def replace(self, body : AnalyticsWorkspace):
        result = await super().replace(
            namespace = body.metadata.namespace,
            name = body.metadata.name,
            body = body.to_dictionary()
        )
        return AnalyticsWorkspace(result, self.get_api_version(), self.kind)
    
    async def delete(self, body : AnalyticsWorkspace = None, namespace : str = None, name : str = None):
        if body:
            if not namespace:
                namespace = body.metadata.namespace
            if not name:
                name = body.metadata.name
        
        
        patch_body = [{"op": "replace", "path": "/status/statusText", "value": "Deleting"}] 

        current = await super().get(namespace, name)
        if not current.get("status"):
            patch_body = [{"op": "add", "path": "/status", "value": { "statusText" : "Deleting" }}] 

        await super().patch_status(
            namespace = body.metadata.namespace,
            name = body.metadata.name,
            body = patch_body
        )
        return await super().delete(
            namespace = body.metadata.namespace,
            name = body.metadata.name
        )
    
class PersistentVolumeClaimClient:
    def __init__(self, api_client : client.ApiClient, log : Logger):
        self.api = client.CoreV1Api(api_client)
        self.log = log
        
    async def get(self, name: str, namespace: str) -> V1PersistentVolumeClaim:
        self.log.info(f"Searching for PVC {name} on {namespace} exists")
        response : V1PersistentVolumeClaimList = await self.api.list_namespaced_persistent_volume_claim(namespace, field_selector = f"metadata.name={name}")
        
        if len(response.items) == 0:
            return None
        
        return response.items[0]

    async def create_if_not_exists(self, name: str, namespace: str, storage_class_name : str, labels: dict[str, str] = {}, access_modes : list[str]=["ReadWriteMany"], storage_requested : str = "10Gi"):
        pvc = await self.get(name, namespace)
        if not pvc:
            self.log.info(f"PVC {name} on {namespace} does not exist.")
            
            pvc = V1PersistentVolumeClaim(
                metadata = V1ObjectMeta(
                    name=name,
                    namespace= namespace,
                    labels = labels
                ),
                spec=V1PersistentVolumeClaimSpec(
                    storage_class_name = storage_class_name,
                    access_modes = access_modes,
                    resources= {
                        "requests": { 
                            "storage": storage_requested
                        }
                    }
                )
            )
            return await self.api.create_namespaced_persistent_volume_claim(namespace, pvc)

        return pvc
    
    async def mount(self, pod: V1Pod, storage_name : str, namespace: str, storage_class_name : str, mount_path : str, read_only : bool = False) -> V1Pod:
        self.log.info(f"Attempting to mount {storage_name} on {namespace}...")
        storage : V1PersistentVolumeClaim = await self.create_if_not_exists(storage_name, namespace, storage_class_name)

        volume = V1Volume(
            name = storage_name,
            persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(
                claim_name=storage.metadata.name
            )
        )

        if mount_path == "":
            mount_path= f"/mnt/{storage_name}"

        volume_mount = V1VolumeMount(
            name = storage_name,
            mount_path= mount_path,
            read_only = read_only
        )
        if not pod.spec.volumes:
            pod.spec.volumes = []
        pod.spec.volumes.append(volume)
        if not pod.spec.containers[0].volume_mounts:
            pod.spec.containers[0].volume_mounts = []
        pod.spec.containers[0].volume_mounts.append(volume_mount)

        self.log.info(f"Successfully mounted {storage.metadata.name} to {mount_path}.")

        return pod
