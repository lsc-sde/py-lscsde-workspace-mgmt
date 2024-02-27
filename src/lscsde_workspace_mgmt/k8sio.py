from logging import Logger
from kubernetes_asyncio import client
from .objects import (
    WorkspaceVolumeStatus,
    AnalyticsWorkspace,
    AnalyticsWorkspaceBinding
)
from kubernetes_asyncio.client.models import (
    V1ObjectMeta,
    V1Pod,
    V1Volume,
    V1VolumeMount,
    V1PersistentVolumeClaim,
    V1PersistentVolumeClaimSpec,
    V1PersistentVolumeClaimVolumeSource,
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
    
class VolumeManager:
    def __init__(self,k8s_api : client.ApiClient, log):
        self.v1_api = client.CoreV1Api(k8s_api)
        self.log = log
        
    async def get_workspace_volume_status(self, workspace_name: str, namespace: str):
        name = f"jupyter-{workspace_name}"
        exists = True
        try:
            self.log.info(f"Checking if PVC {name} on {namespace} exists")
            response = await self.v1_api.read_namespaced_persistent_volume_claim(name, namespace)
            self.log.info(f"response: {response}")

        except client.exceptions.ApiException as e:
            if e.status == 404:
                exists = False
            else:
                raise e
        
        return WorkspaceVolumeStatus(name, namespace, exists)

    async def create_workspace_volume_if_not_exists(self, workspace_name: str, namespace: str):
        status = await self.get_workspace_volume_status(workspace_name, namespace)
        if not status.exists:
            self.log.info(f"PVC {status.name} on {status.namespace} does not exist.")
            
            pvc = V1PersistentVolumeClaim(
                metadata = V1ObjectMeta(
                    name=status.name,
                    namespace= namespace,
                    labels={
                        "workspace.xlscsde.nhs.uk/workspace" : workspace_name,
                        "workspace.xlscsde.nhs.uk/storageType" : "workspace",
                    }
                ),
                spec=V1PersistentVolumeClaimSpec(
                    storage_class_name="jupyter-default",
                    access_modes=["ReadWriteMany"],
                    resources= {
                        "requests": { 
                            "storage": "10Gi"
                        }
                    }
                )
            )
            await self.v1_api.create_namespaced_persistent_volume_claim(namespace, pvc)
            status.exists = True
        else: 
            self.log.info(f"PVC {status.name} on {status.namespace} already exists.")

        return status
    
    async def mount_volume(self, pod: V1Pod, storage_name : str, namespace: str, read_only : bool = False):
        self.log.info(f"Attempting to mount {storage_name} on {namespace}...")
        storage = await self.create_workspace_volume_if_not_exists(storage_name, namespace)

        if storage:
            volume = V1Volume(
                name = storage_name,
                persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(
                    claim_name=storage.name
                )
            )

            mount_path= f"/home/jovyan/{storage_name}"
            volume_mount = V1VolumeMount(
                name = storage_name,
                mount_path= mount_path,
                read_only = read_only
            )
            pod.spec.volumes.append(volume)
            pod.spec.containers[0].volume_mounts.append(volume_mount)

            self.log.info(f"Successfully mounted {storage.name} to {mount_path}.")
