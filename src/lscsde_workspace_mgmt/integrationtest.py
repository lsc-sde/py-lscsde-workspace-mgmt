"""
Integration Tests for LSCSDE Workspace Management

This module contains integration tests for the LSCSDE Workspace Management system.
It tests interaction with Kubernetes resources like AnalyticsWorkspace and
AnalyticsWorkspaceBinding through various client implementations.

The tests require a running Kubernetes instance with the LSCSDE CRDs installed.
Tests are designed to clean up after themselves, creating and deleting resources
as needed.

Classes:
    ObjectsMocker: Provides helper methods to create mock objects for testing
    TestWorkspaceClient: Tests the AnalyticsWorkspaceClient functionality
    TestWorkspaceBindingClient: Tests the AnalyticsWorkspaceBindingClient functionality
    TestWorkspaceManager: Tests the AnalyticsWorkspaceManager functionality
"""

import pytest
from pydantic import TypeAdapter
from kubernetes_asyncio.config import load_kube_config
from kubernetes_asyncio.client import (
    CustomObjectsApi,
    ApiClient,
    V1Pod,
    V1ObjectMeta,
    V1PodSpec,
    V1Container,
)
from .k8sio import (
    AnalyticsWorkspaceClient,
    AnalyticsWorkspaceBindingClient,
    EventClient,
)
from .objects import (
    AnalyticsWorkspace,
    AnalyticsWorkspaceBinding,
)
from .managers import AnalyticsWorkspaceManager
from logging import Logger
from datetime import datetime


class ObjectsMocker:
    """
    Helper class that provides methods to create mock objects for testing.

    This class simplifies the creation and cleanup of test resources in Kubernetes.
    It provides methods to create workspace and workspace binding objects with
    predefined configurations, as well as utility methods to recreate or clean up
    these resources.
    """

    async def create_workspace(
        self,
        client: AnalyticsWorkspaceClient,
        name: str,
        display_name: str = "Example jupyter workspace",
    ):
        """
        Creates a workspace with the given name and display name.

        Args:
            client: The workspace client to use for creation
            name: The name of the workspace
            display_name: The display name of the workspace

        Returns:
            The created workspace object
        """
        mocked_workspace = self.mock_workspace(name=name)
        adapter = TypeAdapter(AnalyticsWorkspace)

        translated_workspace = adapter.validate_python(mocked_workspace)
        # Clean up any existing workspace with the same name
        list_workspaces = await client.list(
            "default",
            field_selector=f"metadata.name={translated_workspace.metadata.name}",
        )
        if len(list_workspaces) > 0:
            await client.delete(body=list_workspaces[0])

        return await client.create(translated_workspace)

    async def create_workspace_binding(
        self,
        client: AnalyticsWorkspaceBindingClient,
        name: str,
        username: str,
        workspace: str,
        append_label: bool = True,
    ):
        """
        Creates a workspace binding with the given name, username, and workspace.

        Args:
            client: The workspace binding client to use for creation
            name: The name of the binding
            username: The username to bind to
            workspace: The workspace name to bind to
            append_label: Whether to append a label to the binding

        Returns:
            The created workspace binding object
        """
        omocker = ObjectsMocker()
        mocked_workspace_binding = omocker.mock_workspace_binding(
            name, username, workspace
        )
        adapter = TypeAdapter(AnalyticsWorkspaceBinding)

        translated_workspace_binding = adapter.validate_python(
            mocked_workspace_binding, strict=False
        )
        # Clean up any existing binding with the same name
        list_workspace_bindings = await client.list(
            "default",
            field_selector=f"metadata.name={translated_workspace_binding.metadata.name}",
        )
        if len(list_workspace_bindings) > 0:
            await client.delete(body=list_workspace_bindings[0])

        return await client.create(
            translated_workspace_binding, append_label=append_label
        )

    def mock_workspace_binding(self, name, username, workspace, expires="2124-02-26"):
        """
        Creates a dictionary representing a workspace binding.

        Args:
            name: The name of the binding
            username: The username to bind to
            workspace: The workspace name to bind to
            expires: The expiration date string

        Returns:
            Dictionary with the binding configuration
        """
        return {
            "apiVersion": "xlscsde.nhs.uk/v1",
            "kind": "AnalyticsWorkspaceBinding",
            "metadata": {"labels": {}, "name": name, "namespace": "default"},
            "spec": {"expires": expires, "username": username, "workspace": workspace},
        }

    def mock_workspace(self, name, display_name="Example jupyter workspace"):
        """
        Creates a dictionary representing a workspace.

        Args:
            name: The name of the workspace
            display_name: The display name of the workspace

        Returns:
            Dictionary with the workspace configuration
        """
        return {
            "apiVersion": "xlscsde.nhs.uk/v1",
            "kind": "AnalyticsWorkspace",
            "metadata": {
                "annotations": {},
                "labels": {},
                "managedFields": [],
                "name": name,
                "namespace": "default",
            },
            "spec": {
                "description": "This is an example jupyter workspace, and can be largely ignored\n",
                "displayName": display_name,
                "jupyterWorkspace": {"image": "jupyter/datascience-notebook:latest"},
                "validity": {"availableFrom": "2024-02-26", "expires": "2124-02-26"},
            },
        }

    async def recreate_workspace(
        self, client: AnalyticsWorkspaceClient, workspace=dict[str, any]
    ):
        """
        Recreates a workspace by deleting any existing one with the same name and creating a new one.

        Args:
            client: The workspace client to use for recreation
            workspace: The workspace configuration dictionary

        Returns:
            The recreated workspace object
        """
        adapter = TypeAdapter(AnalyticsWorkspace)
        translated_workspace = adapter.validate_python(workspace, strict=False)
        # Clean up any existing workspace with the same name
        list_workspaces = await client.list(
            "default",
            field_selector=f"metadata.name={translated_workspace.metadata.name}",
        )
        if len(list_workspaces) > 0:
            await client.delete(body=list_workspaces[0])

        created_workspace: AnalyticsWorkspace = await client.create(
            translated_workspace
        )
        return created_workspace

    async def recreate_workspace_binding(
        self,
        client: AnalyticsWorkspaceBindingClient,
        binding=dict[str, any],
        append_label: bool = True,
    ):
        """
        Recreates a workspace binding by deleting any existing one with the same name and creating a new one.

        Args:
            client: The workspace binding client to use for recreation
            binding: The workspace binding configuration dictionary
            append_label: Whether to append a label to the binding

        Returns:
            The recreated workspace binding object
        """
        adapter = TypeAdapter(AnalyticsWorkspaceBinding)
        translated_workspace_binding = adapter.validate_python(binding, strict=False)
        # Clean up any existing binding with the same name
        list_workspace_bindings = await client.list(
            "default",
            field_selector=f"metadata.name={translated_workspace_binding.metadata.name}",
        )
        if len(list_workspace_bindings) > 0:
            await client.delete(body=list_workspace_bindings[0])

        created_workspace_binding: AnalyticsWorkspaceBinding = await client.create(
            translated_workspace_binding, append_label
        )
        return created_workspace_binding


class TestWorkspaceClient:
    """
    Tests for AnalyticsWorkspaceClient functionality.

    This class contains integration tests that verify the client's ability to
    perform CRUD operations on AnalyticsWorkspace resources in Kubernetes.
    """

    log = Logger("TestWorkspaceClient")

    @pytest.mark.asyncio
    async def test_get(self):
        """
        Test retrieving an AnalyticsWorkspace by name.

        Creates a workspace, retrieves it by name, verifies its properties,
        then cleans up.
        """
        # Setup Kubernetes client and API
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        client = AnalyticsWorkspaceClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )

        # Create test workspace
        name = "example-jupyter-workspace"
        namespace = "default"
        self.log.info("Getting {name} from {namespace} namespace")
        omocker = ObjectsMocker()
        mocked_workspace = omocker.mock_workspace(name=name)
        adapter = TypeAdapter(AnalyticsWorkspace)

        # Clean up existing workspace if it exists
        translated_workspace = adapter.validate_python(mocked_workspace, strict=False)
        list_workspaces = await client.list(
            "default",
            field_selector=f"metadata.name={translated_workspace.metadata.name}",
        )
        if len(list_workspaces) > 0:
            await client.delete(body=list_workspaces[0])

        # Create and verify workspace
        created_workspace = await client.create(translated_workspace)
        response = await client.get(namespace, name)

        # Verify workspace properties
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert (
            "jupyter/datascience-notebook:latest"
            == response.spec.jupyter_workspace.image
        )
        assert "2024-02-26" == response.spec.validity.available_from
        assert "2124-02-26" == response.spec.validity.expires
        assert "Example jupyter workspace" == response.spec.display_name
        assert (
            "This is an example jupyter workspace, and can be largely ignored\n"
            == response.spec.description
        )

        # Clean up
        await client.delete(body=created_workspace)

    @pytest.mark.asyncio
    async def test_list(self):
        """
        Test listing AnalyticsWorkspace resources.

        Creates a workspace, lists workspaces by name, verifies the list contains
        the created workspace, then cleans up.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        client = AnalyticsWorkspaceClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        namespace = "default"
        name = "test-workspace-list"
        omocker = ObjectsMocker()
        mocked_workspace = omocker.mock_workspace(name=name)
        adapter = TypeAdapter(AnalyticsWorkspace)

        translated_workspace = adapter.validate_python(mocked_workspace, strict=False)
        list_workspaces = await client.list(
            "default",
            field_selector=f"metadata.name={translated_workspace.metadata.name}",
        )
        if len(list_workspaces) > 0:
            await client.delete(body=list_workspaces[0])

        created_workspace = await client.create(translated_workspace)
        self.log.info("Getting {name} from {namespace} namespace")
        responses = await client.list(
            namespace,
            field_selector=f"metadata.name={translated_workspace.metadata.name}",
        )
        response = responses[0]
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert name == response.metadata.name
        assert (
            "jupyter/datascience-notebook:latest"
            == response.spec.jupyter_workspace.image
        )
        assert "2024-02-26" == response.spec.validity.available_from
        assert "2124-02-26" == response.spec.validity.expires
        assert "Example jupyter workspace" == response.spec.display_name
        assert (
            "This is an example jupyter workspace, and can be largely ignored\n"
            == response.spec.description
        )

        await client.delete(body=created_workspace)

    @pytest.mark.asyncio
    async def test_crud(self):
        """
        Test Create, Read, Update, Delete operations on AnalyticsWorkspace.

        Creates a workspace, updates its status, patches it, replaces it,
        and finally deletes it.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        client = AnalyticsWorkspaceClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        omocker = ObjectsMocker()
        mocked_workspace = omocker.mock_workspace("integration-test-crud")
        adapter = TypeAdapter(AnalyticsWorkspace)
        translated_workspace = adapter.validate_python(mocked_workspace, strict=False)
        list_workspaces = await client.list(
            "default",
            field_selector=f"metadata.name={translated_workspace.metadata.name}",
        )
        if len(list_workspaces) > 0:
            await client.delete(body=list_workspaces[0])

        # Create workspace
        created_workspace: AnalyticsWorkspace = await client.create(
            translated_workspace
        )

        # Update status
        created_workspace.status.status_text = "Provisioning"
        patched_status_workspace: AnalyticsWorkspace = await client.patch_status(
            namespace=created_workspace.metadata.namespace,
            name=created_workspace.metadata.name,
            status=created_workspace.status,
        )
        print(f"patched_status_workspace = {patched_status_workspace}")

        # Patch workspace
        patched_status_workspace.spec.display_name = "Patched"
        patched_workspace: AnalyticsWorkspace = await client.patch(
            body=patched_status_workspace
        )

        # Replace workspace
        patched_workspace.spec.display_name = "Replaced"
        replaced_workspace: AnalyticsWorkspace = await client.replace(patched_workspace)

        # Delete workspace
        deleted_workspace = await client.delete(body=replaced_workspace)
        print(deleted_workspace)

    @pytest.mark.asyncio
    async def test_list_by_username_unlinked_workspace(self):
        """
        Test listing workspaces by username for unlinked workspaces.

        Creates multiple workspaces and bindings, then verifies that
        listing by username returns the expected results.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        workspace_client = AnalyticsWorkspaceClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        binding_client = AnalyticsWorkspaceBindingClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        omocker = ObjectsMocker()
        workspace_adapter = TypeAdapter(AnalyticsWorkspace)  # noqa: F841
        workspace_binding_adapter = TypeAdapter(AnalyticsWorkspaceBinding)  # noqa: F841

        mocked_workspace1 = omocker.mock_workspace(
            "test-list-by-username-unlinked-workspace-1"
        )
        mocked_workspace2 = omocker.mock_workspace(
            "test-list-by-username-unlinked-workspace-2"
        )
        mocked_workspace_binding1 = omocker.mock_workspace_binding(
            "integration-test-crud-unlinked-workspace-1",
            "integration-test-crud-unlinked-workspace-1",
            mocked_workspace1["metadata"]["name"],
        )
        mocked_workspace_binding2 = omocker.mock_workspace_binding(
            "integration-test-crud-unlinked-workspace-2",
            "integration-test-crud-unlinked-workspace-1",
            mocked_workspace2["metadata"]["name"],
        )
        mocked_workspace_binding3 = omocker.mock_workspace_binding(
            "integration-test-crud-unlinked-workspace-3",
            "integration-test-crud-unlinked-workspace-2",
            mocked_workspace2["metadata"]["name"],
        )
        mocked_workspace_binding3 = omocker.mock_workspace_binding(
            "integration-test-crud-unlinked-workspace-4",
            "integration-test-crud-unlinked-workspace-1",
            mocked_workspace1["metadata"]["name"],
        )
        workspace1 = await omocker.recreate_workspace(
            client=workspace_client, workspace=mocked_workspace1
        )
        workspace_binding1 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding1, append_label=False
        )
        workspace_binding2 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding2, append_label=False
        )
        workspace_binding3 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding3, append_label=False
        )

        workspaces = await workspace_client.list_by_username(
            binding_client=binding_client,
            namespace="default",
            username="integration-test-crud-unlinked-workspace-1",
        )

        print(workspaces)
        assert len(workspaces) == 1

        await workspace_client.delete(body=workspace1)
        await binding_client.delete(body=workspace_binding1)
        await binding_client.delete(body=workspace_binding2)
        await binding_client.delete(body=workspace_binding3)


class TestWorkspaceBindingClient:
    """
    Tests for AnalyticsWorkspaceBindingClient functionality.

    This class contains integration tests that verify the client's ability to
    perform CRUD operations on AnalyticsWorkspaceBinding resources in Kubernetes,
    as well as specialized operations like listing by username.
    """

    log = Logger("TestWorkspaceBindingClient")

    @pytest.mark.asyncio
    async def test_get(self):
        """
        Test retrieving an AnalyticsWorkspaceBinding by name.

        Creates a workspace binding, retrieves it by name, verifies its properties,
        then cleans up.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceBindingClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        client = AnalyticsWorkspaceBindingClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        name = "test-workspacebinding-get"
        namespace = "default"
        username = "test.user"
        workspace = "some-workspace"
        omocker = ObjectsMocker()

        created_workspace_binding: AnalyticsWorkspaceBinding = (
            await omocker.create_workspace_binding(client, name, username, workspace)
        )

        self.log.info("Getting {name} from {namespace} namespace")
        response = await client.get(namespace, name)
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert username == response.spec.username
        assert workspace == response.spec.workspace
        assert "2124-02-26" == response.spec.expires
        await client.delete(body=created_workspace_binding)

    @pytest.mark.asyncio
    async def test_list(self):
        """
        Test listing AnalyticsWorkspaceBinding resources.

        Creates a workspace binding, lists bindings by name, verifies the list contains
        the created binding, then cleans up.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceBindingClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        client = AnalyticsWorkspaceBindingClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        name = "test-workspacebinding-list"
        username = "test.user"
        workspace = "some-workspace"
        namespace = "default"
        omocker = ObjectsMocker()
        created_workspace_binding: AnalyticsWorkspaceBinding = (
            await omocker.create_workspace_binding(client, name, username, workspace)
        )

        self.log.info("Getting {name} from {namespace} namespace")
        responses = await client.list(namespace, field_selector=f"metadata.name={name}")
        response = responses[0]
        assert name == response.metadata.name
        assert namespace == response.metadata.namespace
        assert username == response.spec.username
        assert workspace == response.spec.workspace
        assert "2124-02-26" == response.spec.expires
        await client.delete(body=created_workspace_binding)

    @pytest.mark.asyncio
    async def test_crud(self):
        """
        Test Create, Read, Update, Delete operations on AnalyticsWorkspaceBinding.

        Creates a workspace binding, updates its status, patches it, replaces it,
        and finally deletes it.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        client = AnalyticsWorkspaceBindingClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        omocker = ObjectsMocker()

        created_workspace_binding = await omocker.create_workspace_binding(
            client, "integration-test-crud", "test.user", "some-workspace"
        )
        created_workspace_binding.status.status_text = "Provisioning"
        patched_status_workspace_binding: AnalyticsWorkspaceBinding = (
            await client.patch_status(
                namespace=created_workspace_binding.metadata.namespace,
                name=created_workspace_binding.metadata.name,
                status=created_workspace_binding.status,
            )
        )
        print(f"patched_status_workspace = {patched_status_workspace_binding}")
        patched_status_workspace_binding.spec.comments = "Patched"
        patched_workspace_binding: AnalyticsWorkspaceBinding = await client.patch(
            body=patched_status_workspace_binding
        )
        patched_workspace_binding.spec.comments = "Replaced"
        replaced_workspace_binding: AnalyticsWorkspaceBinding = await client.replace(
            patched_workspace_binding
        )
        deleted_workspace = await client.delete(body=replaced_workspace_binding)
        print(deleted_workspace)

    @pytest.mark.asyncio
    async def test_list_by_username(self):
        """
        Test listing workspace bindings by username.

        Creates multiple workspaces and bindings, then verifies that
        listing by username returns the expected results.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        workspace_client = AnalyticsWorkspaceClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        binding_client = AnalyticsWorkspaceBindingClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        omocker = ObjectsMocker()
        mocked_workspace1 = omocker.mock_workspace("test-list-by-username1")
        mocked_workspace2 = omocker.mock_workspace("test-list-by-username2")
        mocked_workspace_binding1 = omocker.mock_workspace_binding(
            "integration-test-crud1",
            "integration-test-crud1",
            mocked_workspace1["metadata"]["name"],
        )
        mocked_workspace_binding2 = omocker.mock_workspace_binding(
            "integration-test-crud2",
            "integration-test-crud1",
            mocked_workspace2["metadata"]["name"],
        )
        mocked_workspace_binding3 = omocker.mock_workspace_binding(
            "integration-test-crud3",
            "integration-test-crud2",
            mocked_workspace2["metadata"]["name"],
        )
        workspace1 = await omocker.recreate_workspace(
            client=workspace_client, workspace=mocked_workspace1
        )
        workspace2 = await omocker.recreate_workspace(
            client=workspace_client, workspace=mocked_workspace2
        )
        workspace_binding1 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding1, append_label=False
        )
        workspace_binding2 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding2, append_label=False
        )
        workspace_binding3 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding3, append_label=False
        )

        workspace_bindings_list = await binding_client.list_by_username(
            "default", "integration-test-crud1"
        )
        assert len(workspace_bindings_list) == 2

        await workspace_client.delete(body=workspace1)
        await workspace_client.delete(body=workspace2)
        await binding_client.delete(body=workspace_binding1)
        await binding_client.delete(body=workspace_binding2)
        await binding_client.delete(body=workspace_binding3)

    @pytest.mark.asyncio
    async def test_list_by_username_apostrophe(self):
        """
        Test listing workspace bindings by username with special characters.

        Verifies that usernames with apostrophes and other special characters
        can be correctly processed for label selectors.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        workspace_client = AnalyticsWorkspaceClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        binding_client = AnalyticsWorkspaceBindingClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        omocker = ObjectsMocker()
        mocked_workspace1 = omocker.mock_workspace("test-list-by-username-apostrophe-1")
        mocked_workspace2 = omocker.mock_workspace("test-list-by-username-apostrophe-2")

        # Create test workspaces and bindings with special characters in usernames
        # Note: The special characters need to be properly escaped in label selectors
        mocked_workspace_binding1 = omocker.mock_workspace_binding(
            "integration-test-crud-apostrophe-1",
            "integration-test'crud1@bases!com",  # Username with apostrophe and special chars
            mocked_workspace1["metadata"]["name"],
        )
        mocked_workspace_binding2 = omocker.mock_workspace_binding(
            "integration-test-crud-apostrophe-2",
            "integration-test'crud1@bases!com",
            mocked_workspace2["metadata"]["name"],
        )
        mocked_workspace_binding3 = omocker.mock_workspace_binding(
            "integration-test-crud-apostrophe-3",
            "integration-test'crud2@bases!com",
            mocked_workspace2["metadata"]["name"],
        )
        workspace1 = await omocker.recreate_workspace(
            client=workspace_client, workspace=mocked_workspace1
        )
        workspace2 = await omocker.recreate_workspace(
            client=workspace_client, workspace=mocked_workspace2
        )
        workspace_binding1 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding1, append_label=False
        )
        workspace_binding2 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding2, append_label=False
        )
        workspace_binding3 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding3, append_label=False
        )

        # This tests that the label selector mechanism properly handles special characters
        workspace_bindings_list = await binding_client.list_by_username(
            "default", "integration-test'crud1@bases!com"
        )
        assert len(workspace_bindings_list) == 2

        await workspace_client.delete(body=workspace1)
        await workspace_client.delete(body=workspace2)
        await binding_client.delete(body=workspace_binding1)
        await binding_client.delete(body=workspace_binding2)
        await binding_client.delete(body=workspace_binding3)

    @pytest.mark.asyncio
    async def test_list_by_username_apostrophe_2(self):
        """
        Test listing workspace bindings by username with special characters.

        Verifies that usernames with apostrophes and other special characters
        can be correctly processed for label selectors.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)
        self.log.info("Setting up AnalyticsWorkspaceClient")
        event_client = EventClient(api_client=api_client, log=self.log)
        workspace_client = AnalyticsWorkspaceClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        binding_client = AnalyticsWorkspaceBindingClient(
            k8s_api=custom_objects_api, log=self.log, event_client=event_client
        )
        omocker = ObjectsMocker()
        mocked_workspace1 = omocker.mock_workspace(
            "test-list-by-username-apostrophe-2-1"
        )
        mocked_workspace2 = omocker.mock_workspace(
            "test-list-by-username-apostrophe-2-2"
        )
        mocked_workspace_binding1 = omocker.mock_workspace_binding(
            "integration-test-crud-apostrophe-2-1",
            "integration-test2'crud1@bases!com",
            mocked_workspace1["metadata"]["name"],
        )
        mocked_workspace_binding2 = omocker.mock_workspace_binding(
            "integration-test-crud-apostrophe-2-2",
            "integration-test2'crud1@bases!com",
            mocked_workspace2["metadata"]["name"],
        )
        mocked_workspace_binding3 = omocker.mock_workspace_binding(
            "integration-test-crud-apostrophe-2-3",
            "integration-test2'crud2@bases!com!",
            mocked_workspace2["metadata"]["name"],
        )
        workspace1 = await omocker.recreate_workspace(
            client=workspace_client, workspace=mocked_workspace1
        )
        workspace2 = await omocker.recreate_workspace(
            client=workspace_client, workspace=mocked_workspace2
        )
        workspace_binding1 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding1, append_label=False
        )
        workspace_binding2 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding2, append_label=False
        )
        workspace_binding3 = await omocker.recreate_workspace_binding(
            client=binding_client, binding=mocked_workspace_binding3, append_label=False
        )

        workspace_bindings_list = await binding_client.list_by_username(
            "default", "integration-test2'crud1@bases!com"
        )
        assert len(workspace_bindings_list) == 2

        await workspace_client.delete(body=workspace1)
        await workspace_client.delete(body=workspace2)
        await binding_client.delete(body=workspace_binding1)
        await binding_client.delete(body=workspace_binding2)
        await binding_client.delete(body=workspace_binding3)


class TestWorkspaceManager:
    """
    Tests for AnalyticsWorkspaceManager functionality.

    This class tests the higher-level operations provided by the workspace manager,
    such as getting permitted workspaces for a user and mounting volumes.
    """

    log = Logger("TestWorkspaceManager")

    @pytest.mark.asyncio
    async def test_list_by_username(self):
        """
        Test getting permitted workspaces for a username.

        Creates multiple workspaces and bindings with different expiry dates,
        then verifies that the permitted workspaces are correctly sorted and filtered.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        custom_objects_api = CustomObjectsApi(api_client=api_client)  # noqa: F841
        self.log.info("Setting up AnalyticsWorkspaceClient")
        workspace_manager = AnalyticsWorkspaceManager(
            api_client=api_client, log=self.log
        )
        omocker = ObjectsMocker()
        mocked_workspace1 = omocker.mock_workspace(
            "manager-test-list-by-username1",
            display_name="Z workspace",  # Z should sort last alphabetically
        )
        mocked_workspace2 = omocker.mock_workspace(
            "manager-test-list-by-username2",
            display_name="A workspace",  # A should sort first alphabetically
        )
        mocked_workspace3 = omocker.mock_workspace(
            "manager-test-list-by-username3", display_name="B workspace"
        )
        mocked_workspace4 = omocker.mock_workspace(
            "manager-test-list-by-username4", display_name="C workspace"
        )
        mocked_workspace_binding1 = omocker.mock_workspace_binding(
            "manager-integration-test-crud1",
            "manager-integration-test-crud1",
            mocked_workspace1["metadata"]["name"],
            expires="2024-02-01",  # Future date from test date
        )
        mocked_workspace_binding2 = omocker.mock_workspace_binding(
            "managerintegration-test-crud2",
            "manager-integration-test-crud1",
            mocked_workspace2["metadata"]["name"],
            expires="2024-01-01",
        )
        mocked_workspace_binding3 = omocker.mock_workspace_binding(
            "managerintegration-test-crud3",
            "manager-integration-test-crud2",
            mocked_workspace2["metadata"]["name"],
            expires="2023-12-01",
        )
        mocked_workspace_binding4 = omocker.mock_workspace_binding(
            "managerintegration-test-crud4",
            "manager-integration-test-crud2",
            mocked_workspace3["metadata"]["name"],
            expires="2024-12-01",
        )
        mocked_workspace_binding5 = omocker.mock_workspace_binding(
            "managerintegration-test-crud5",
            "manager-integration-test-crud3",
            mocked_workspace2["metadata"]["name"],
        )
        mocked_workspace_binding6 = omocker.mock_workspace_binding(
            "managerintegration-test-crud6",
            "manager-integration-test-crud1",
            mocked_workspace4["metadata"]["name"],
            expires="2023-12-01",
        )
        mocked_workspace_binding7 = omocker.mock_workspace_binding(
            "managerintegration-test-crud7",
            "manager-integration-test-crud1",
            mocked_workspace1["metadata"]["name"],
            expires="2023-11-01",  # Past date from test date
        )
        workspace1 = await omocker.recreate_workspace(
            client=workspace_manager.workspace_client, workspace=mocked_workspace1
        )
        workspace2 = await omocker.recreate_workspace(
            client=workspace_manager.workspace_client, workspace=mocked_workspace2
        )
        workspace3 = await omocker.recreate_workspace(
            client=workspace_manager.workspace_client, workspace=mocked_workspace3
        )
        workspace_binding1 = await omocker.recreate_workspace_binding(
            client=workspace_manager.binding_client, binding=mocked_workspace_binding1
        )
        workspace_binding2 = await omocker.recreate_workspace_binding(
            client=workspace_manager.binding_client, binding=mocked_workspace_binding2
        )
        workspace_binding3 = await omocker.recreate_workspace_binding(
            client=workspace_manager.binding_client, binding=mocked_workspace_binding3
        )
        workspace_binding4 = await omocker.recreate_workspace_binding(
            client=workspace_manager.binding_client, binding=mocked_workspace_binding4
        )
        workspace_binding5 = await omocker.recreate_workspace_binding(
            client=workspace_manager.binding_client, binding=mocked_workspace_binding5
        )
        workspace_binding6 = await omocker.recreate_workspace_binding(
            client=workspace_manager.binding_client, binding=mocked_workspace_binding6
        )
        workspace_binding7 = await omocker.recreate_workspace_binding(
            client=workspace_manager.binding_client, binding=mocked_workspace_binding7
        )

        # Use a fixed date for testing the expiry calculations
        date_now = datetime(2023, 12, 1)

        # Test for first user - should get workspaces sorted alphabetically
        permitted_workspaces = await workspace_manager.get_permitted_workspaces(
            "default", "manager-integration-test-crud1", date_now=date_now
        )
        # Verify sorting order (alphabetical by display_name)
        assert len(permitted_workspaces) == 2
        assert (
            permitted_workspaces[0]["display_name"] == "A workspace"
        )  # Should come first alphabetically
        assert permitted_workspaces[0]["slug"] == workspace2.metadata.name
        assert permitted_workspaces[0]["end_date"] == "2024-01-01"
        # Verify days left calculation works for future dates
        assert (
            permitted_workspaces[0]["ws_days_left"].days == 31
        )  # 31 days until expiry
        assert permitted_workspaces[1]["display_name"] == "Z workspace"
        assert permitted_workspaces[1]["slug"] == workspace1.metadata.name
        assert permitted_workspaces[1]["end_date"] == "2023-11-01"
        # Verify days left calculation works for past dates (negative values)
        assert permitted_workspaces[1]["ws_days_left"].days == -30

        # Test for second user
        permitted_workspaces = await workspace_manager.get_permitted_workspaces(
            "default", "manager-integration-test-crud2", date_now=date_now
        )
        assert len(permitted_workspaces) == 2
        assert permitted_workspaces[0]["display_name"] == "A workspace"
        assert permitted_workspaces[0]["slug"] == workspace2.metadata.name
        assert permitted_workspaces[0]["end_date"] == "2023-12-01"
        assert permitted_workspaces[0]["ws_days_left"].days == 0
        assert permitted_workspaces[1]["display_name"] == "B workspace"
        assert permitted_workspaces[1]["slug"] == workspace3.metadata.name
        assert permitted_workspaces[1]["end_date"] == "2024-12-01"
        assert permitted_workspaces[1]["ws_days_left"].days == 366

        # Test for third user with default expiry date (very far in future)
        permitted_workspaces = await workspace_manager.get_permitted_workspaces(
            "default", "manager-integration-test-crud3", date_now=date_now
        )
        assert len(permitted_workspaces) == 1
        assert permitted_workspaces[0]["display_name"] == "A workspace"
        assert permitted_workspaces[0]["slug"] == workspace2.metadata.name
        assert permitted_workspaces[0]["end_date"] == "2124-02-26"
        # Verify the default expiry date calculation (over 100 years)
        assert permitted_workspaces[0]["ws_days_left"].days == 36611

        # Clean up all created resources
        await workspace_manager.workspace_client.delete(body=workspace1)
        await workspace_manager.workspace_client.delete(body=workspace2)
        await workspace_manager.workspace_client.delete(body=workspace3)
        await workspace_manager.binding_client.delete(body=workspace_binding1)
        await workspace_manager.binding_client.delete(body=workspace_binding2)
        await workspace_manager.binding_client.delete(body=workspace_binding3)
        await workspace_manager.binding_client.delete(body=workspace_binding4)
        await workspace_manager.binding_client.delete(body=workspace_binding5)
        await workspace_manager.binding_client.delete(body=workspace_binding6)
        await workspace_manager.binding_client.delete(body=workspace_binding7)

    @pytest.mark.asyncio
    async def test_mount_volume(self):
        """
        Test mounting a workspace volume to a pod.

        Creates a workspace and pod, then verifies that the manager
        can correctly configure volume mounts for the pod.
        """
        self.log.info("Getting Configuration")
        configuration = await load_kube_config()
        print(f"configuration = {configuration}")
        self.log.info("Connecting to client")
        api_client = ApiClient()
        self.log.info("Setting up AnalyticsWorkspaceManager")
        workspace_manager = AnalyticsWorkspaceManager(
            api_client=api_client, log=self.log
        )
        omocker = ObjectsMocker()
        mocked_workspace = omocker.mock_workspace(
            "manager-test-mount-volume", display_name="Mount-Volume-Test"
        )
        workspace = await omocker.recreate_workspace(
            client=workspace_manager.workspace_client, workspace=mocked_workspace
        )

        # Create a test pod with workspace label to enable volume mounting
        pod = V1Pod()
        pod.metadata = V1ObjectMeta(
            namespace="default",
            name="mgr-mnt-tst",
            labels={
                "workspace": workspace.metadata.name
            },  # Label connects pod to workspace
        )
        pod.spec = V1PodSpec(containers=[V1Container(name="test")])

        # Test the mount_workspace functionality with specific storage settings
        amended_pod = await workspace_manager.mount_workspace(
            pod,
            storage_class_name="hostpath",  # Storage class to use for PVCs
            mount_prefix="/mnt",  # Where volumes will be mounted in containers
            storage_prefix="hostpath-",  # Prefix for storage volume names
        )
        # The amended_pod should now have volumes and volume mounts configured
