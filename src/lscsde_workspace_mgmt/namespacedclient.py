from logging import Logger
from kubernetes_asyncio import client
from os import getenv
from uuid import uuid4
from pytz import utc

class KubernetesNamespacedCustomClient:
    """
    Represents a namespaced client for interacting with kubernetes objects
    """
    def __init__(self, k8s_api : client.CustomObjectsApi, log : Logger, group : str, version : str, plural : str, kind : str):
        self.group = group
        self.version = version
        self.plural = plural
        self.kind = kind
        self.api = k8s_api
        self.log : Logger = log

    def get_api_version(self):
        """
        Gets the API version
        """
        return f"{self.group}/{self.version}"

    
    async def get(self, namespace, name):
        """
        Gets the requested resource
        """
        return await self.api.get_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name
        )
    
    async def list(self, namespace, **kwargs):
        """
        Lists the requested resources
        """
        return await self.api.list_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            **kwargs
        )
    
    async def patch(self, namespace : str, name : str, body : dict):
        """
        Patches the requested resource
        """
        return await self.api.patch_namespaced_custom_object(
            group = self.group, 
            version = self.version, 
            namespace = namespace,
            plural = self.plural, 
            name = name, 
            body = body
            )
    
    async def patch_status(self, namespace : str, name : str, body : dict):
        """
        Patches the status of the requested resource
        """
        return await self.api.patch_namespaced_custom_object_status(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name,
            body = body
        )
    
    async def replace(self, namespace : str, name : str, body : dict):
        """
        Replaces the requested resource with the one supplied
        """
        return await self.api.replace_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name,
            body = body
        )
    
    
    async def create(self, namespace : str, body : dict):
        """
        Creates the requested resource
        """
        return await self.api.create_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            body = body
        )
    
    async def delete(self, namespace : str, name : str):
        """
        Deletes the requested resource
        """
        return await self.api.delete_namespaced_custom_object(
            group = self.group,
            version = self.version,
            namespace = namespace,
            plural = self.plural,
            name = name
        )
