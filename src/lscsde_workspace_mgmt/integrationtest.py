import pytest
from unittest.mock import Mock
from kubernetes_asyncio.config import load_kube_config
from kubernetes_asyncio.client import CustomObjectsApi, ApiClient
from .k8sio import AnalyticsWorkspaceClient, AnalyticsWorkspaceBindingClient
from logging import Logger

class TestWorkspaceClient:
    log = Logger("TestWorkspaceClient")

    @pytest.mark.asyncio
    async def test_get(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log)
        name = "example-jupyter-workspace"
        namespace = "default"
        self.log.info("Getting {name} from {namespace} namespace")
        response = await client.get(namespace, name)
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert "example-jupyter-workspace" == response.metadata.name 
        assert "jupyter/datascience-notebook:latest" == response.spec.jupyter_workspace.image
        assert "2024-02-26" == response.spec.validity.available_from
        assert "2124-02-26" == response.spec.validity.expires
        assert "Example jupyter workspace" == response.spec.display_name
        assert "This is an example jupyter workspace, and can be largely ignored\n" == response.spec.description
    
    @pytest.mark.asyncio
    async def test_list(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log)
        name = "example-jupyter-workspace"
        namespace = "default"
        self.log.info("Getting {name} from {namespace} namespace")
        responses = await client.list(namespace, field_selector = f"metadata.name={name}")
        response = responses[0]
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert "example-jupyter-workspace" == response.metadata.name 
        assert "jupyter/datascience-notebook:latest" == response.spec.jupyter_workspace.image
        assert "2024-02-26" == response.spec.validity.available_from
        assert "2124-02-26" == response.spec.validity.expires
        assert "Example jupyter workspace" == response.spec.display_name
        assert "This is an example jupyter workspace, and can be largely ignored\n" == response.spec.description

class TestWorkspaceBindingClient:
    log = Logger("TestWorkspaceBindingClient")

    @pytest.mark.asyncio
    async def test_get(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceBindingClient")
        client = AnalyticsWorkspaceBindingClient(k8s_api=custom_objects_api, log = self.log)
        name = "example-jupyter-workspace-shaun-turner"
        namespace = "default"
        self.log.info("Getting {name} from {namespace} namespace")
        response = await client.get(namespace, name)
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert "example-jupyter-workspace" == response.spec.workspace
        assert "shaun.turner1@nhs.net" == response.spec.username
        assert "2124-02-26" == response.spec.expires
        
    @pytest.mark.asyncio
    async def test_list(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceBindingClient")
        client = AnalyticsWorkspaceBindingClient(k8s_api=custom_objects_api, log = self.log)
        name = "example-jupyter-workspace-shaun-turner"
        namespace = "default"
        self.log.info("Getting {name} from {namespace} namespace")
        responses = await client.list(namespace, field_selector = f"metadata.name={name}")
        response = responses[0]
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert "example-jupyter-workspace" == response.spec.workspace
        assert "shaun.turner1@nhs.net" == response.spec.username
        assert "2124-02-26" == response.spec.expires