from pydantic import TypeAdapter

from ..models import (
    AnalyticsDataSourceBinding
)

class TestDataSourceBinding:
    def test_datasource_conversion(self):
        datasource_dict = self.mock_binding()
        print(datasource_dict)
        adaptor = TypeAdapter(AnalyticsDataSourceBinding)
        datasource = adaptor.validate_python(datasource_dict, strict=False)
        assert "dsb-782b4a1f07234229980f75f2f651412a" == datasource.metadata.name 
        assert "ds-782b4a1f07234229980f75f2f651412a" == datasource.spec.datasource
        assert "advanced-generic-workspace" == datasource.spec.workspace

    def mock_binding(self):
        return {
            "apiVersion": "xlscsde.nhs.uk/v1",
            "kind": "AnalyticsDataSourceBinding",
            "metadata": {
                "annotations": {
                    "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"xlscsde.nhs.uk/v1\",\"kind\":\"AnalyticsDataSourceBinding\",\"metadata\":{\"annotations\":{},\"name\":\"dsb-782b4a1f07234229980f75f2f651412a\",\"namespace\":\"default\"},\"spec\":{\"datasource\":\"ds-782b4a1f07234229980f75f2f651412a\",\"workspace\":\"advanced-generic-workspace\"}}\n"
                },
                "creationTimestamp": "2024-12-27T16:27:23Z",
                "generation": 1,
                "name": "dsb-782b4a1f07234229980f75f2f651412a",
                "namespace": "default",
                "resourceVersion": "105938",
                "uid": "f01c7e09-0d23-42a0-8f02-a63347238c24"
            },
            "spec": {
                "datasource": "ds-782b4a1f07234229980f75f2f651412a",
                "workspace": "advanced-generic-workspace"
            }
        }