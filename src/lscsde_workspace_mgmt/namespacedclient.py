from logging import Logger
from kubernetes_asyncio import client


class KubernetesNamespacedCustomClient:
    """
    Represents a namespaced client for interacting with Kubernetes custom resources.

    This class provides an asynchronous interface for CRUD operations on
    Kubernetes CustomResourceDefinitions (CRDs) within a specific namespace.
    It simplifies interactions with custom resources by encapsulating the
    Kubernetes API calls with a more friendly interface.

    Attributes:
        group (str): The API group of the custom resource
        version (str): The API version of the custom resource
        plural (str): The plural name of the custom resource
        kind (str): The kind of the custom resource
        api (CustomObjectsApi): The Kubernetes custom objects API client
        log (Logger): Logger instance for debug and error messages
    """

    def __init__(
        self,
        k8s_api: client.CustomObjectsApi,
        log: Logger,
        group: str,
        version: str,
        plural: str,
        kind: str,
    ):
        """
        Initialize a new namespaced Kubernetes custom resources client.

        Args:
            k8s_api (client.CustomObjectsApi): The Kubernetes custom objects API client
            log (Logger): Logger instance for debug and error messages
            group (str): The API group of the custom resource (e.g., 'example.com')
            version (str): The API version of the custom resource (e.g., 'v1')
            plural (str): The plural name of the custom resource (e.g., 'widgets')
            kind (str): The kind of the custom resource (e.g., 'Widget')
        """
        self.group = group
        self.version = version
        self.plural = plural
        self.kind = kind
        self.api = k8s_api
        self.log: Logger = log

    def get_api_version(self):
        """
        Gets the full API version string for the custom resource.

        Returns:
            str: The API version in the format 'group/version'
        """
        return f"{self.group}/{self.version}"

    async def get(self, namespace, name):
        """
        Gets a specific custom resource by name.

        Args:
            namespace (str): The namespace containing the resource
            name (str): The name of the resource to retrieve

        Returns:
            dict: The requested custom resource as a dictionary

        Raises:
            kubernetes_asyncio.client.exceptions.ApiException: If the resource is not found
                or another API error occurs
        """
        return await self.api.get_namespaced_custom_object(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            name=name,
        )

    async def list(self, namespace, **kwargs):
        """
        Lists all custom resources of this type in the specified namespace.

        Args:
            namespace (str): The namespace to list resources from
            **kwargs: Optional parameters to pass to the list API call, such as:
                      label_selector, field_selector, timeout_seconds, etc.

        Returns:
            dict: A dictionary containing the list of custom resources

        Raises:
            kubernetes_asyncio.client.exceptions.ApiException: If an API error occurs
        """
        return await self.api.list_namespaced_custom_object(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            **kwargs,
        )

    async def patch(self, namespace: str, name: str, body: dict):
        """
        Patches a specific custom resource with the provided data.

        Args:
            namespace (str): The namespace containing the resource
            name (str): The name of the resource to patch
            body (dict): The patch to apply to the resource

        Returns:
            dict: The patched custom resource

        Raises:
            kubernetes_asyncio.client.exceptions.ApiException: If the resource is not found
                or another API error occurs
        """
        return await self.api.patch_namespaced_custom_object(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            name=name,
            body=body,
        )

    async def patch_status(self, namespace: str, name: str, body: dict):
        """
        Patches only the status subresource of a specific custom resource.

        Args:
            namespace (str): The namespace containing the resource
            name (str): The name of the resource to patch the status for
            body (dict): The patch to apply to the resource's status subresource

        Returns:
            dict: The custom resource with updated status

        Raises:
            kubernetes_asyncio.client.exceptions.ApiException: If the resource is not found
                or another API error occurs
        """
        return await self.api.patch_namespaced_custom_object_status(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            name=name,
            body=body,
        )

    async def replace(self, namespace: str, name: str, body: dict):
        """
        Replaces a specific custom resource with the provided data.

        This performs a full replacement, not a patch operation.

        Args:
            namespace (str): The namespace containing the resource
            name (str): The name of the resource to replace
            body (dict): The complete new definition of the resource

        Returns:
            dict: The replaced custom resource

        Raises:
            kubernetes_asyncio.client.exceptions.ApiException: If the resource is not found
                or another API error occurs
        """
        return await self.api.replace_namespaced_custom_object(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            name=name,
            body=body,
        )

    async def create(self, namespace: str, body: dict):
        """
        Creates a new custom resource in the specified namespace.

        Args:
            namespace (str): The namespace to create the resource in
            body (dict): The complete definition of the resource to create

        Returns:
            dict: The created custom resource

        Raises:
            kubernetes_asyncio.client.exceptions.ApiException: If a resource with the same name
                already exists or another API error occurs
        """
        return await self.api.create_namespaced_custom_object(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            body=body,
        )

    async def delete(self, namespace: str, name: str):
        """
        Deletes a specific custom resource by name.

        Args:
            namespace (str): The namespace containing the resource
            name (str): The name of the resource to delete

        Returns:
            dict: The status of the delete operation

        Raises:
            kubernetes_asyncio.client.exceptions.ApiException: If the resource is not found
                or another API error occurs
        """
        return await self.api.delete_namespaced_custom_object(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            name=name,
        )
