import asyncio
import pytest
import requests
from unittest.mock import Mock
from .objects import AnalyticsWorkspace


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

    def mock_workspace(self):
        return {'apiVersion': 'xlscsde.nhs.uk/v1', 'kind': 'AnalyticsWorkspace', 'metadata': {'annotations': {'meta.helm.sh/release-name': 'xlscsde-ws-mgmt', 'meta.helm.sh/release-namespace': 'default'}, 'creationTimestamp': '2024-02-27T10:37:58Z', 'generation': 1, 'labels': {'app.kubernetes.io/managed-by': 'Helm'}, 'managedFields': [{'apiVersion': 'xlscsde.nhs.uk/v1', 'fieldsType': 'FieldsV1', 'fieldsV1': {'f:metadata': {'f:annotations': {'.': {}, 'f:meta.helm.sh/release-name': {}, 'f:meta.helm.sh/release-namespace': {}}, 'f:labels': {'.': {}, 'f:app.kubernetes.io/managed-by': {}}}, 'f:spec': {'.': {}, 'f:description': {}, 'f:displayName': {}, 'f:jupyterWorkspace': {'.': {}, 'f:image': {}}, 'f:validity': {'.': {}, 'f:availableFrom': {}, 'f:expires': {}}}}, 'manager': 'helm', 'operation': 'Update', 'time': '2024-02-27T10:37:58Z'}], 'name': 'example-jupyter-workspace', 'namespace': 'default', 'resourceVersion': '834601', 'uid': '190997a8-3bf6-4a9f-8302-4db6018c8a93'}, 'spec': {'description': 'This is an example jupyter workspace, and can be largely ignored\n', 'displayName': 'Example jupyter workspace', 'jupyterWorkspace': {'image': 'jupyter/datascience-notebook:latest'}, 'validity': {'availableFrom': '2024-02-26', 'expires': '2124-02-26'}}}