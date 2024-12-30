from ..models import (
    KubernetesMetadata,
    AnalyticsWorkspaceBindingSpec,
    AnalyticsWorkspaceBinding
)

class TestWorkspaceBindings:
    def mock_binding(self, name: str, username : str, workspace : str):
        metadata = KubernetesMetadata(name = name, namespace = "default")
        spec = AnalyticsWorkspaceBindingSpec(username = username, workspace = workspace)
        binding = AnalyticsWorkspaceBinding()
        binding.metadata = metadata
        binding.spec = spec
        return binding

    def test_binding_label_generation_simple(self):
        binding = self.mock_binding(
            name = "test1", 
            username = "joe.blogs@someplace.co.uk",
            workspace = "test_label_generation")
        assert "joe.blogs___someplace.co.uk" == binding.spec.username_as_label()

