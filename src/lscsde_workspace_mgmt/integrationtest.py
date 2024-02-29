import pytest
from unittest.mock import Mock
from kubernetes_asyncio.config import load_kube_config
from kubernetes_asyncio.client import CustomObjectsApi, ApiClient
from .k8sio import AnalyticsWorkspaceClient, AnalyticsWorkspaceBindingClient
from .objects import AnalyticsWorkspace, AnalyticsWorkspaceStatus, AnalyticsWorkspaceBinding
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
    
    @pytest.mark.asyncio
    async def test_crud(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log)
        mocked_workspace = self.mock_workspace("integration-test-crud")
        translated_workspace = AnalyticsWorkspace(mocked_workspace, client.get_api_version(), client.kind)
        list_workspaces = await client.list("default", field_selector = f"metadata.name={translated_workspace.metadata.name}")
        if len(list_workspaces) > 0:
            await client.delete(body = list_workspaces[0])
            

        created_workspace : AnalyticsWorkspace = await client.create(translated_workspace)
        created_workspace.status.status_text = "Provisioning"
        patched_status_workspace : AnalyticsWorkspace = await client.patch_status(
            namespace = created_workspace.metadata.namespace,
            name = created_workspace.metadata.name,
            status = created_workspace.status
            )
        print(f"patched_status_workspace = {patched_status_workspace}")
        patched_status_workspace.spec.display_name = "Patched"
        patched_workspace : AnalyticsWorkspace = await client.patch(body = patched_status_workspace)
        patched_workspace.spec.display_name = "Replaced"
        replaced_workspace : AnalyticsWorkspace = await client.replace(patched_workspace)
        deleted_workspace = await client.delete(body = replaced_workspace)
        print(deleted_workspace)

        
    def mock_workspace(self, name):
        return {'apiVersion': 'xlscsde.nhs.uk/v1', 'kind': 'AnalyticsWorkspace', 'metadata': {'annotations': {}, 'labels': {}, 'managedFields': [], 'name': name, 'namespace': 'default'}, 'spec': {'description': 'This is an example jupyter workspace, and can be largely ignored\n', 'displayName': 'Example jupyter workspace', 'jupyterWorkspace': {'image': 'jupyter/datascience-notebook:latest'}, 'validity': {'availableFrom': '2024-02-26', 'expires': '2124-02-26'}}}

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