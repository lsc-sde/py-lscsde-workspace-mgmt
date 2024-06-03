import pytest
from pydantic import TypeAdapter
from unittest.mock import Mock
from kubernetes_asyncio.config import load_kube_config
from kubernetes_asyncio.client import (
    CustomObjectsApi, 
    ApiClient, 
    V1Pod, 
    V1ObjectMeta, 
    V1PodSpec,
    V1Container
)
from .k8sio import AnalyticsWorkspaceClient, AnalyticsWorkspaceBindingClient, EventClient
from .objects import AnalyticsWorkspace, AnalyticsWorkspaceStatus, AnalyticsWorkspaceBinding
from .managers import AnalyticsWorkspaceManager
from logging import Logger
from datetime import datetime

class ObjectsMocker:
    
    async def create_workspace(self, client : AnalyticsWorkspaceClient, name : str, display_name : str = "Example jupyter workspace"):
        mocked_workspace = self.mock_workspace(name = name)
        adapter = TypeAdapter(AnalyticsWorkspace)

        translated_workspace = adapter.validate_python(mocked_workspace)
        list_workspaces = await client.list("default", field_selector = f"metadata.name={translated_workspace.metadata.name}")
        if len(list_workspaces) > 0:
            await client.delete(body = list_workspaces[0])
        
        return await client.create(translated_workspace)
    
    async def create_workspace_binding(self, client : AnalyticsWorkspaceBindingClient, name : str, username : str, workspace : str, append_label : bool = True):
        omocker = ObjectsMocker()
        mocked_workspace_binding = omocker.mock_workspace_binding(name, username, workspace)
        adapter = TypeAdapter(AnalyticsWorkspaceBinding)
        
        translated_workspace_binding = adapter.validate_python(mocked_workspace_binding, strict=False)
        list_workspace_bindings = await client.list("default", field_selector = f"metadata.name={translated_workspace_binding.metadata.name}")
        if len(list_workspace_bindings) > 0:
            await client.delete(body = list_workspace_bindings[0])

        return await client.create(translated_workspace_binding, append_label = append_label)
        
    def mock_workspace_binding(self, name, username, workspace, expires = '2124-02-26'):
        return {
            'apiVersion': 'xlscsde.nhs.uk/v1',
            'kind': 'AnalyticsWorkspaceBinding',
            'metadata': {
                'labels': {
                },
                'name': name,
                'namespace': 'default'
            },
            'spec': {
                'expires': expires,
                'username': username,
                'workspace': workspace
            }
        }
    def mock_workspace(self, name, display_name = "Example jupyter workspace"):
        return {
            'apiVersion': 'xlscsde.nhs.uk/v1', 
            'kind': 'AnalyticsWorkspace', 
            'metadata': {
                'annotations': {}, 
                'labels': {}, 
                'managedFields': [], 
                'name': name, 
                'namespace': 'default'}, 
                'spec': {
                    'description': 'This is an example jupyter workspace, and can be largely ignored\n', 
                    'displayName': display_name, 
                    'jupyterWorkspace': {
                        'image': 'jupyter/datascience-notebook:latest'
                    }, 
                    'validity': {
                        'availableFrom': '2024-02-26', 
                        'expires': '2124-02-26'
                    }
                }
            }
    
    async def recreate_workspace(self, client : AnalyticsWorkspaceClient, workspace = dict[str, any]):
        adapter = TypeAdapter(AnalyticsWorkspace)
        translated_workspace = adapter.validate_python(workspace, strict=False)
        list_workspaces = await client.list("default", field_selector = f"metadata.name={translated_workspace.metadata.name}")
        if len(list_workspaces) > 0:
            await client.delete(body = list_workspaces[0])
            
        created_workspace : AnalyticsWorkspace = await client.create(translated_workspace)
        return created_workspace
        
    async def recreate_workspace_binding(self, client : AnalyticsWorkspaceBindingClient, binding = dict[str, any], append_label : bool = True):
        adapter = TypeAdapter(AnalyticsWorkspaceBinding)
        translated_workspace_binding = adapter.validate_python(binding, strict=False)
        list_workspace_bindings = await client.list("default", field_selector = f"metadata.name={translated_workspace_binding.metadata.name}")
        if len(list_workspace_bindings) > 0:
            await client.delete(body = list_workspace_bindings[0])
            
        created_workspace_binding : AnalyticsWorkspaceBinding = await client.create(translated_workspace_binding, append_label)
        return created_workspace_binding

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
        event_client = EventClient(api_client=api_client, log = self.log)
        client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log, event_client=event_client)
        name = "example-jupyter-workspace"
        namespace = "default"
        self.log.info("Getting {name} from {namespace} namespace")
        omocker = ObjectsMocker()
        mocked_workspace = omocker.mock_workspace(name = name)
        adapter = TypeAdapter(AnalyticsWorkspace)
        
        translated_workspace = adapter.validate_python(mocked_workspace, strict=False)
        list_workspaces = await client.list("default", field_selector = f"metadata.name={translated_workspace.metadata.name}")
        if len(list_workspaces) > 0:
            await client.delete(body = list_workspaces[0])
        created_workspace = await client.create(translated_workspace)
        response = await client.get(namespace, name)
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert "jupyter/datascience-notebook:latest" == response.spec.jupyter_workspace.image
        assert "2024-02-26" == response.spec.validity.available_from
        assert "2124-02-26" == response.spec.validity.expires
        assert "Example jupyter workspace" == response.spec.display_name
        assert "This is an example jupyter workspace, and can be largely ignored\n" == response.spec.description
        await client.delete(body = created_workspace)
    
    @pytest.mark.asyncio
    async def test_list(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client = api_client, log = self.log)
        client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log, event_client=event_client)
        namespace = "default"
        name = "test-workspace-list"
        omocker = ObjectsMocker()
        mocked_workspace = omocker.mock_workspace(name = name)
        adapter = TypeAdapter(AnalyticsWorkspace)

        translated_workspace = adapter.validate_python(mocked_workspace, strict=False)
        list_workspaces = await client.list("default", field_selector = f"metadata.name={translated_workspace.metadata.name}")
        if len(list_workspaces) > 0:
            await client.delete(body = list_workspaces[0])

        created_workspace = await client.create(translated_workspace)
        self.log.info("Getting {name} from {namespace} namespace")
        responses = await client.list(namespace, field_selector = f"metadata.name={translated_workspace.metadata.name}")
        response = responses[0]
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert name == response.metadata.name 
        assert "jupyter/datascience-notebook:latest" == response.spec.jupyter_workspace.image
        assert "2024-02-26" == response.spec.validity.available_from
        assert "2124-02-26" == response.spec.validity.expires
        assert "Example jupyter workspace" == response.spec.display_name
        assert "This is an example jupyter workspace, and can be largely ignored\n" == response.spec.description
        
        await client.delete(body = created_workspace)

    @pytest.mark.asyncio
    async def test_crud(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log = self.log)
        client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log, event_client = event_client)
        omocker = ObjectsMocker()
        mocked_workspace = omocker.mock_workspace("integration-test-crud")
        adapter = TypeAdapter(AnalyticsWorkspace)
        translated_workspace = adapter.validate_python(mocked_workspace, strict=False)
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

    @pytest.mark.asyncio
    async def test_list_by_username_unlinked_workspace(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client = api_client, log = self.log)
        workspace_client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log, event_client=event_client)
        binding_client = AnalyticsWorkspaceBindingClient(k8s_api=custom_objects_api, log = self.log, event_client=event_client)
        omocker = ObjectsMocker()
        workspace_adapter = TypeAdapter(AnalyticsWorkspace)
        workspace_binding_adapter = TypeAdapter(AnalyticsWorkspaceBinding)

        mocked_workspace1 = omocker.mock_workspace("test-list-by-username-unlinked-workspace-1")
        mocked_workspace2 = omocker.mock_workspace("test-list-by-username-unlinked-workspace-2")
        mocked_workspace_binding1 = omocker.mock_workspace_binding("integration-test-crud-unlinked-workspace-1", "integration-test-crud-unlinked-workspace-1", mocked_workspace1["metadata"]["name"])
        mocked_workspace_binding2 = omocker.mock_workspace_binding("integration-test-crud-unlinked-workspace-2", "integration-test-crud-unlinked-workspace-1", mocked_workspace2["metadata"]["name"])
        mocked_workspace_binding3 = omocker.mock_workspace_binding("integration-test-crud-unlinked-workspace-3", "integration-test-crud-unlinked-workspace-2", mocked_workspace2["metadata"]["name"])
        mocked_workspace_binding3 = omocker.mock_workspace_binding("integration-test-crud-unlinked-workspace-4", "integration-test-crud-unlinked-workspace-1", mocked_workspace1["metadata"]["name"])
        workspace1 = await omocker.recreate_workspace(client = workspace_client, workspace = mocked_workspace1)
        workspace_binding1 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding1, append_label = False)
        workspace_binding2 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding2, append_label = False)
        workspace_binding3 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding3, append_label = False)

        workspaces = await workspace_client.list_by_username(binding_client = binding_client, namespace = "default", username = "integration-test-crud-unlinked-workspace-1")
        
        print(workspaces)
        assert len(workspaces) == 1

        await workspace_client.delete(body = workspace1)
        await binding_client.delete(body = workspace_binding1)
        await binding_client.delete(body = workspace_binding2)
        await binding_client.delete(body = workspace_binding3)
        
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
        event_client = EventClient(api_client = api_client, log = self.log)
        client = AnalyticsWorkspaceBindingClient(k8s_api=custom_objects_api, log = self.log, event_client = event_client)
        name = "test-workspacebinding-get"
        namespace = "default"
        username = "test.user"
        workspace = "some-workspace"
        omocker = ObjectsMocker()
        
        created_workspace_binding : AnalyticsWorkspaceBinding = await omocker.create_workspace_binding(client, name, username, workspace)
        
        self.log.info("Getting {name} from {namespace} namespace")
        response = await client.get(namespace, name)
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert username == response.spec.username
        assert workspace == response.spec.workspace
        assert "2124-02-26" == response.spec.expires
        await client.delete(body = created_workspace_binding)
        
    @pytest.mark.asyncio
    async def test_list(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceBindingClient")
        event_client = EventClient(api_client = api_client, log = self.log)
        client = AnalyticsWorkspaceBindingClient(k8s_api=custom_objects_api, log = self.log, event_client = event_client)
        name = "test-workspacebinding-list"
        username = "test.user"
        workspace = "some-workspace"
        namespace = "default"
        omocker = ObjectsMocker()
        created_workspace_binding : AnalyticsWorkspaceBinding = await omocker.create_workspace_binding(client, name, username, workspace)
        
        self.log.info("Getting {name} from {namespace} namespace")
        responses = await client.list(namespace, field_selector = f"metadata.name={name}")
        response = responses[0]
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert username == response.spec.username
        assert workspace == response.spec.workspace
        assert "2124-02-26" == response.spec.expires
        await client.delete(body = created_workspace_binding)
        
    @pytest.mark.asyncio
    async def test_crud(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log = self.log)
        client = AnalyticsWorkspaceBindingClient(k8s_api=custom_objects_api, log = self.log, event_client = event_client)
        omocker = ObjectsMocker()

        created_workspace_binding = await omocker.create_workspace_binding(client, "integration-test-crud", "test.user", "some-workspace")
        created_workspace_binding.status.status_text = "Provisioning"
        patched_status_workspace_binding : AnalyticsWorkspaceBinding = await client.patch_status(
            namespace = created_workspace_binding.metadata.namespace,
            name = created_workspace_binding.metadata.name,
            status = created_workspace_binding.status
            )
        print(f"patched_status_workspace = {patched_status_workspace_binding}")
        patched_status_workspace_binding.spec.comments = "Patched"
        patched_workspace_binding : AnalyticsWorkspaceBinding = await client.patch(body = patched_status_workspace_binding)
        patched_workspace_binding.spec.comments = "Replaced"
        replaced_workspace_binding : AnalyticsWorkspaceBinding = await client.replace(patched_workspace_binding)
        deleted_workspace = await client.delete(body = replaced_workspace_binding)
        print(deleted_workspace)

    @pytest.mark.asyncio
    async def test_list_by_username(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client = api_client, log = self.log)
        workspace_client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log, event_client=event_client)
        binding_client = AnalyticsWorkspaceBindingClient(k8s_api=custom_objects_api, log = self.log, event_client=event_client)
        omocker = ObjectsMocker()
        mocked_workspace1 = omocker.mock_workspace("test-list-by-username1")
        mocked_workspace2 = omocker.mock_workspace("test-list-by-username2")
        mocked_workspace_binding1 = omocker.mock_workspace_binding("integration-test-crud1", "integration-test-crud1", mocked_workspace1["metadata"]["name"])
        mocked_workspace_binding2 = omocker.mock_workspace_binding("integration-test-crud2", "integration-test-crud1", mocked_workspace2["metadata"]["name"])
        mocked_workspace_binding3 = omocker.mock_workspace_binding("integration-test-crud3", "integration-test-crud2", mocked_workspace2["metadata"]["name"])
        workspace1 = await omocker.recreate_workspace(client = workspace_client, workspace = mocked_workspace1)
        workspace2 = await omocker.recreate_workspace(client = workspace_client, workspace = mocked_workspace2)
        workspace_binding1 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding1, append_label = False)
        workspace_binding2 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding2, append_label = False)
        workspace_binding3 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding3, append_label = False)

        workspace_bindings_list = await binding_client.list_by_username("default", "integration-test-crud1")
        assert len(workspace_bindings_list) == 2

        await workspace_client.delete(body = workspace1)
        await workspace_client.delete(body = workspace2)
        await binding_client.delete(body = workspace_binding1)
        await binding_client.delete(body = workspace_binding2)
        await binding_client.delete(body = workspace_binding3)
        
    @pytest.mark.asyncio
    async def test_list_by_username_apostrophe(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client = api_client, log = self.log)
        workspace_client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log, event_client = event_client)
        binding_client = AnalyticsWorkspaceBindingClient(k8s_api=custom_objects_api, log = self.log, event_client = event_client)
        omocker = ObjectsMocker()
        mocked_workspace1 = omocker.mock_workspace("test-list-by-username-apostrophe-1")
        mocked_workspace2 = omocker.mock_workspace("test-list-by-username-apostrophe-2")
        mocked_workspace_binding1 = omocker.mock_workspace_binding("integration-test-crud-apostrophe-1", "integration-test'crud1@bases!com", mocked_workspace1["metadata"]["name"])
        mocked_workspace_binding2 = omocker.mock_workspace_binding("integration-test-crud-apostrophe-2", "integration-test'crud1@bases!com", mocked_workspace2["metadata"]["name"])
        mocked_workspace_binding3 = omocker.mock_workspace_binding("integration-test-crud-apostrophe-3", "integration-test'crud2@bases!com", mocked_workspace2["metadata"]["name"])
        workspace1 = await omocker.recreate_workspace(client = workspace_client, workspace = mocked_workspace1)
        workspace2 = await omocker.recreate_workspace(client = workspace_client, workspace = mocked_workspace2)
        workspace_binding1 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding1, append_label = False)
        workspace_binding2 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding2, append_label = False)
        workspace_binding3 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding3, append_label = False)

        workspace_bindings_list = await binding_client.list_by_username("default", "integration-test'crud1@bases!com")
        assert len(workspace_bindings_list) == 2

        await workspace_client.delete(body = workspace1)
        await workspace_client.delete(body = workspace2)
        await binding_client.delete(body = workspace_binding1)
        await binding_client.delete(body = workspace_binding2)
        await binding_client.delete(body = workspace_binding3)

    @pytest.mark.asyncio
    async def test_list_by_username_apostrophe_2(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client = api_client, log = self.log)
        workspace_client = AnalyticsWorkspaceClient(k8s_api=custom_objects_api, log = self.log, event_client = event_client)
        binding_client = AnalyticsWorkspaceBindingClient(k8s_api=custom_objects_api, log = self.log, event_client = event_client)
        omocker = ObjectsMocker()
        mocked_workspace1 = omocker.mock_workspace("test-list-by-username-apostrophe-2-1")
        mocked_workspace2 = omocker.mock_workspace("test-list-by-username-apostrophe-2-2")
        mocked_workspace_binding1 = omocker.mock_workspace_binding("integration-test-crud-apostrophe-2-1", "integration-test2'crud1@bases!com", mocked_workspace1["metadata"]["name"])
        mocked_workspace_binding2 = omocker.mock_workspace_binding("integration-test-crud-apostrophe-2-2", "integration-test2'crud1@bases!com", mocked_workspace2["metadata"]["name"])
        mocked_workspace_binding3 = omocker.mock_workspace_binding("integration-test-crud-apostrophe-2-3", "integration-test2'crud2@bases!com!", mocked_workspace2["metadata"]["name"])
        workspace1 = await omocker.recreate_workspace(client = workspace_client, workspace = mocked_workspace1)
        workspace2 = await omocker.recreate_workspace(client = workspace_client, workspace = mocked_workspace2)
        workspace_binding1 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding1, append_label = False)
        workspace_binding2 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding2, append_label = False)
        workspace_binding3 = await omocker.recreate_workspace_binding(client = binding_client, binding = mocked_workspace_binding3, append_label = False)

        workspace_bindings_list = await binding_client.list_by_username("default", "integration-test2'crud1@bases!com")
        assert len(workspace_bindings_list) == 2

        await workspace_client.delete(body = workspace1)
        await workspace_client.delete(body = workspace2)
        await binding_client.delete(body = workspace_binding1)
        await binding_client.delete(body = workspace_binding2)
        await binding_client.delete(body = workspace_binding3)


class TestWorkspaceManager:
    log = Logger("TestWorkspaceManager")
    @pytest.mark.asyncio
    async def test_list_by_username(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        workspace_manager = AnalyticsWorkspaceManager(api_client=api_client, log = self.log)
        omocker = ObjectsMocker()
        mocked_workspace1 = omocker.mock_workspace("manager-test-list-by-username1", display_name = "Z workspace")
        mocked_workspace2 = omocker.mock_workspace("manager-test-list-by-username2", display_name = "A workspace")
        mocked_workspace3 = omocker.mock_workspace("manager-test-list-by-username3", display_name= "B workspace")
        mocked_workspace4 = omocker.mock_workspace("manager-test-list-by-username4", display_name= "C workspace")
        mocked_workspace_binding1 = omocker.mock_workspace_binding("manager-integration-test-crud1", "manager-integration-test-crud1", mocked_workspace1["metadata"]["name"], expires="2024-02-01")
        mocked_workspace_binding2 = omocker.mock_workspace_binding("managerintegration-test-crud2", "manager-integration-test-crud1", mocked_workspace2["metadata"]["name"], expires="2024-01-01")
        mocked_workspace_binding3 = omocker.mock_workspace_binding("managerintegration-test-crud3", "manager-integration-test-crud2", mocked_workspace2["metadata"]["name"], expires="2023-12-01")
        mocked_workspace_binding4 = omocker.mock_workspace_binding("managerintegration-test-crud4", "manager-integration-test-crud2", mocked_workspace3["metadata"]["name"], expires="2024-12-01")
        mocked_workspace_binding5 = omocker.mock_workspace_binding("managerintegration-test-crud5", "manager-integration-test-crud3", mocked_workspace2["metadata"]["name"])
        mocked_workspace_binding6 = omocker.mock_workspace_binding("managerintegration-test-crud6", "manager-integration-test-crud1", mocked_workspace4["metadata"]["name"], expires="2023-12-01")
        mocked_workspace_binding7 = omocker.mock_workspace_binding("managerintegration-test-crud7", "manager-integration-test-crud1", mocked_workspace1["metadata"]["name"], expires="2023-11-01")
        workspace1 = await omocker.recreate_workspace(client = workspace_manager.workspace_client, workspace = mocked_workspace1)
        workspace2 = await omocker.recreate_workspace(client = workspace_manager.workspace_client, workspace = mocked_workspace2)
        workspace3 = await omocker.recreate_workspace(client = workspace_manager.workspace_client, workspace = mocked_workspace3)
        workspace_binding1 = await omocker.recreate_workspace_binding(client = workspace_manager.binding_client, binding = mocked_workspace_binding1)
        workspace_binding2 = await omocker.recreate_workspace_binding(client = workspace_manager.binding_client, binding = mocked_workspace_binding2)
        workspace_binding3 = await omocker.recreate_workspace_binding(client = workspace_manager.binding_client, binding = mocked_workspace_binding3)
        workspace_binding4 = await omocker.recreate_workspace_binding(client = workspace_manager.binding_client, binding = mocked_workspace_binding4)
        workspace_binding5 = await omocker.recreate_workspace_binding(client = workspace_manager.binding_client, binding = mocked_workspace_binding5)
        workspace_binding6 = await omocker.recreate_workspace_binding(client = workspace_manager.binding_client, binding = mocked_workspace_binding6)
        workspace_binding7 = await omocker.recreate_workspace_binding(client = workspace_manager.binding_client, binding = mocked_workspace_binding7)

        date_now = datetime(2023, 12, 1)

        permitted_workspaces = await workspace_manager.get_permitted_workspaces("default", "manager-integration-test-crud1", date_now=date_now)
        assert len(permitted_workspaces) == 2
        assert permitted_workspaces[0]["display_name"] == "A workspace"
        assert permitted_workspaces[0]["slug"] == workspace2.metadata.name 
        assert permitted_workspaces[0]["end_date"] == "2024-01-01"
        assert permitted_workspaces[0]["ws_days_left"].days == 31
        assert permitted_workspaces[1]["display_name"] == "Z workspace"
        assert permitted_workspaces[1]["slug"] == workspace1.metadata.name
        assert permitted_workspaces[1]["end_date"] == "2023-11-01"
        assert permitted_workspaces[1]["ws_days_left"].days == -30
        

        permitted_workspaces = await workspace_manager.get_permitted_workspaces("default", "manager-integration-test-crud2", date_now=date_now)
        assert len(permitted_workspaces) == 2
        assert permitted_workspaces[0]["display_name"] == "A workspace"
        assert permitted_workspaces[0]["slug"] == workspace2.metadata.name 
        assert permitted_workspaces[0]["end_date"] == "2023-12-01"
        assert permitted_workspaces[0]["ws_days_left"].days == 0
        assert permitted_workspaces[1]["display_name"] == "B workspace"
        assert permitted_workspaces[1]["slug"] == workspace3.metadata.name
        assert permitted_workspaces[1]["end_date"] == "2024-12-01"
        assert permitted_workspaces[1]["ws_days_left"].days == 366

        permitted_workspaces = await workspace_manager.get_permitted_workspaces("default", "manager-integration-test-crud3", date_now=date_now)
        assert len(permitted_workspaces) == 1
        assert permitted_workspaces[0]["display_name"] == "A workspace"
        assert permitted_workspaces[0]["slug"] == workspace2.metadata.name
        assert permitted_workspaces[0]["end_date"] == "2124-02-26"
        assert permitted_workspaces[0]["ws_days_left"].days == 36611

        await workspace_manager.workspace_client.delete(body = workspace1)
        await workspace_manager.workspace_client.delete(body = workspace2)
        await workspace_manager.workspace_client.delete(body = workspace3)
        await workspace_manager.binding_client.delete(body = workspace_binding1)
        await workspace_manager.binding_client.delete(body = workspace_binding2)
        await workspace_manager.binding_client.delete(body = workspace_binding3)
        await workspace_manager.binding_client.delete(body = workspace_binding4)
        await workspace_manager.binding_client.delete(body = workspace_binding5)
        await workspace_manager.binding_client.delete(body = workspace_binding6)
        await workspace_manager.binding_client.delete(body = workspace_binding7)
    
    @pytest.mark.asyncio
    async def test_mount_volume(self):
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        self.log.info("Setting up AnalyticsWorkspaceManager")
        workspace_manager = AnalyticsWorkspaceManager(api_client=api_client, log = self.log)
        omocker = ObjectsMocker()
        mocked_workspace = omocker.mock_workspace("manager-test-mount-volume", display_name = "Mount-Volume-Test")
        workspace = await omocker.recreate_workspace(client = workspace_manager.workspace_client, workspace = mocked_workspace)        
        
        pod = V1Pod()
        pod.metadata = V1ObjectMeta(namespace="default", name="mgr-mnt-tst", labels = { "workspace" : workspace.metadata.name })
        pod.spec = V1PodSpec(containers=[V1Container(name = "test")])
        amended_pod = await workspace_manager.mount_workspace(pod, storage_class_name = "hostpath", mount_prefix = "/mnt", storage_prefix="hostpath-")

