from logging import Logger
from kubernetes_asyncio import client
from os import getenv
from uuid import uuid4
from pytz import utc

# represents a namespaced client
class KubernetesNamespacedCustomClient:
    def __init__(self, k8s_api : client.CustomObjectsApi, log : Logger, group : str, version : str, plural : str, kind : str):
        self.group = group
        self.version = version
        self.plural = plural
        self.kind = kind
        self.api = k8s_api
        self.log : Logger = log

    # gets the API version
    def get_api_version(self):
        return f"{self.group}/{self.version}"

    # gets the requested resource
    async def get(self, namespace, name):
        return await self.api.get_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name
        )
    
    # lists the requested resources
    async def list(self, namespace, **kwargs):
        return await self.api.list_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            **kwargs
        )
    
    # patches the requested resource
    async def patch(self, namespace : str, name : str, body : dict):
        return await self.api.patch_namespaced_custom_object(
            group = self.group, 
            version = self.version, 
            namespace = namespace,
            plural = self.plural, 
            name = name, 
            body = body
            )
    
    # patches the status of the requested resource
    async def patch_status(self, namespace : str, name : str, body : dict):
        return await self.api.patch_namespaced_custom_object_status(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name,
            body = body
        )
    
    # replaces the requested resource with the one supplied
    async def replace(self, namespace : str, name : str, body : dict):
        return await self.api.replace_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name,
            body = body
        )
    
    # creates the requested resource
    async def create(self, namespace : str, body : dict):
        return await self.api.create_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            body = body
        )
    
    # deletes the requested resource
    async def delete(self, namespace : str, name : str):
        return await self.api.delete_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name
        )
