import asyncio
import pytest
import requests
from unittest.mock import Mock
from .objects import AnalyticsWorkspace, AnalyticsWorkspaceBinding, KubernetesHelper
from .exceptions import InvalidLabelFormatException

class TestKubernetesHelper:
    def test_format_label_basic(self):
        helper = KubernetesHelper()
        test1 = helper.format_as_label("joe.blogs@someplace.co.uk")
        assert "joe.blogs___someplace.co.uk" == test1

    def test_format_label_apostrophe(self):
        helper = KubernetesHelper()
        test1 = helper.format_as_label("joe.o'keef@someplace.co.uk")
        assert "joe.o___keef___someplace.co.uk" == test1

    def test_format_label_apostrophe_ending_with_special(self):
        helper = KubernetesHelper()
        with pytest.raises(InvalidLabelFormatException):
            test1 = helper.format_as_label("joe.o'keef@someplace.co.uk!")

class TestWorkspaceBindings:
    def mock_binding(self, name: str, username : str, workspace : str):
        binding = AnalyticsWorkspaceBinding(
            api_version="xlscsde.nhs.uk/v1",
            kind="AnalyticsWorkspaceBinding",
            response={}
            )
        binding.metadata.name = name
        binding.metadata.namespace = "default"
        binding.spec.username = username
        binding.spec.workspace = workspace
        return binding

    def test_binding_label_generation_simple(self):
        binding = self.mock_binding(
            name = "test1", 
            username = "joe.blogs@someplace.co.uk",
            workspace = "test_label_generation")
        assert "joe.blogs___someplace.co.uk" == binding.spec.username_as_label()


class TestWorkspace:
    def test_workspace_conversion(self):
        workspace_dict = self.mock_workspace()
        workspace = AnalyticsWorkspace(workspace_dict, "xlscsde.nhs.uk/v1", "AnalyticsWorkspace")
        assert "example-jupyter-workspace" == workspace.metadata.name 
        assert "jupyter/datascience-notebook:latest" == workspace.spec.jupyter_workspace.image
        assert "2024-02-26" == workspace.spec.validity.available_from
        assert "2124-02-26" == workspace.spec.validity.expires
        assert "Example jupyter workspace" == workspace.spec.display_name
        assert "This is an example jupyter workspace, and can be largely ignored\n" == workspace.spec.description

    def test_workspace_conversion_to_dict(self):
        workspace_dict = self.mock_workspace()
        workspace = AnalyticsWorkspace(workspace_dict, "xlscsde.nhs.uk/v1", "AnalyticsWorkspace")
        workspace_converted = workspace.to_dictionary()
        assert "xlscsde.nhs.uk/v1" == workspace_converted["apiVersion"]
        assert "AnalyticsWorkspace" == workspace_converted["kind"]
        assert "example-jupyter-workspace" == workspace_converted["metadata"]["name"]
        assert "jupyter/datascience-notebook:latest" == workspace_converted["spec"]["jupyterWorkspace"]["image"]
        assert "2024-02-26" == workspace_converted["spec"]["validity"]["availableFrom"]
        assert "2124-02-26" == workspace_converted["spec"]["validity"]["expires"]
        assert "Example jupyter workspace" == workspace_converted["spec"]["displayName"]
        assert "This is an example jupyter workspace, and can be largely ignored\n" == workspace_converted["spec"]["description"]

    def test_workspace_conversion_to_workspace_dict(self):
        mock_workspace = self.mock_workspace()
        workspace = AnalyticsWorkspace(mock_workspace, "xlscsde.nhs.uk/v1", "AnalyticsWorkspace")
        ws = workspace.to_workspace_dict()
        assert ws["display_name"] == "Example jupyter workspace"
        assert ws["description"] == "This is an example jupyter workspace, and can be largely ignored\n"
        assert ws["kubespawner_override"] != None
        assert ws["kubespawner_override"]["image"] == "jupyter/datascience-notebook:latest"
        assert ws["kubespawner_override"]["extra_labels"] != None
        assert ws["kubespawner_override"]["extra_labels"]["workspace"] == "example-jupyter-workspace"
        assert ws["slug"] == "example-jupyter-workspace"
        assert ws["start_date"] == "2024-02-26"
        assert ws["end_date"] == "2124-02-26"

    def mock_workspace(self):
        return {
            'apiVersion': 'xlscsde.nhs.uk/v1', 
            'kind': 'AnalyticsWorkspace', 
            'metadata': {
                'annotations': {
                    'meta.helm.sh/release-name': 'xlscsde-ws-mgmt', 
                    'meta.helm.sh/release-namespace': 'default'
                }, 
                'creationTimestamp': '2024-02-27T10:37:58Z', 
                'generation': 1, 
                'labels': {
                    'app.kubernetes.io/managed-by': 'Helm'
                }, 
                'managedFields': [
                    {
                        'apiVersion': 'xlscsde.nhs.uk/v1', 
                        'fieldsType': 'FieldsV1', 
                        'fieldsV1': {'f:metadata': {'f:annotations': {'.': {}, 'f:meta.helm.sh/release-name': {}, 'f:meta.helm.sh/release-namespace': {}}, 'f:labels': {'.': {}, 'f:app.kubernetes.io/managed-by': {}}}, 'f:spec': {'.': {}, 'f:description': {}, 'f:displayName': {}, 'f:jupyterWorkspace': {'.': {}, 'f:image': {}}, 'f:validity': {'.': {}, 'f:availableFrom': {}, 'f:expires': {}}}}, 
                        'manager': 'helm', 
                        'operation': 'Update', 
                        'time': '2024-02-27T10:37:58Z'
                    }
                ], 
                'name': 'example-jupyter-workspace', 
                'namespace': 'default', 
                'resourceVersion': '834601', 
                'uid': '190997a8-3bf6-4a9f-8302-4db6018c8a93'
            }, 
            'spec': {
                'description': 'This is an example jupyter workspace, and can be largely ignored\n', 
                'displayName': 'Example jupyter workspace', 
                'jupyterWorkspace': {
                    'image': 'jupyter/datascience-notebook:latest'
                }, 
                'validity': {
                    'availableFrom': '2024-02-26', 
                    'expires': '2124-02-26'
                }
            }
        }