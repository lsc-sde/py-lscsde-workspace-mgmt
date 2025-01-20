from logging import Logger
from kubernetes_asyncio import client

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
from os import getenv
from uuid import uuid4
from pytz import utc

class PersistentVolumeClaimClient:
    """
    Client used for interacting with PersistentVolumeClaim resources in kubernetes
    """
    
    def __init__(self, api_client : client.ApiClient, log : Logger):
        self.api = client.CoreV1Api(api_client)
        self.log = log
        self.default_storage_class_name : str = getenv("DEFAULT_STORAGE_CLASS", "jupyter-default") 
        self.default_storage_access_modes : list[str] = getenv("DEFAULT_STORAGE_ACCESS_MODES", "ReadWriteMany").split(",")
        self.default_storage_capacity : str = getenv("DEFAULT_STORAGE_CAPACITY", "1Gi")
        
    
    async def get(self, name: str, namespace: str) -> V1PersistentVolumeClaim:
        """
        Gets a specific PVC
        """
        self.log.info(f"Searching for PVC {name} on {namespace} exists")
        response : V1PersistentVolumeClaimList = await self.api.list_namespaced_persistent_volume_claim(namespace, field_selector = f"metadata.name={name}")
        
        if len(response.items) == 0:
            return None
        
        return response.items[0]

    async def create_if_not_exists(self, name: str, namespace: str, storage_class_name : str = None, labels: dict[str, str] = {}, access_modes : list[str]=None, storage_requested : str = None):
        """
        Create a specific PVC if it doesn't already exist
        """
        if not storage_class_name:
            storage_class_name = self.default_storage_class_name

        if not access_modes:
            access_modes = self.default_storage_access_modes

        if not storage_requested:
            storage_requested = self.default_storage_capacity
        
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
        """
        mounts a PVC into a pod
        """
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
