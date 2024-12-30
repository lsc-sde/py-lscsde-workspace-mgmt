from pydantic import TypeAdapter

from ..models import (
    AnalyticsDataSource
)

class TestDataSource:
    def test_datasource_conversion(self):
        datasource_dict = self.mock_datasource()
        print(datasource_dict)
        adaptor = TypeAdapter(AnalyticsDataSource)
        datasource = adaptor.validate_python(datasource_dict, strict=False)
        assert "ds-782b4a1f07234229980f75f2f651412a" == datasource.metadata.name 
        assert "d4e6" == datasource.spec.project.id
        assert None != datasource.spec.connections
        assert 1 == len(datasource.spec.connections)
        assert None != datasource.spec.connections[0].databricks_connection
        assert None == datasource.spec.connections[0].connection_string
        assert "test" == datasource.spec.connections[0].databricks_connection.host_name
        assert "/test" == datasource.spec.connections[0].databricks_connection.http_path
        assert "/test" == datasource.spec.connections[0].databricks_connection.http_path
        assert "test-secret" == datasource.spec.connections[0].databricks_connection.personal_access_token.secret_name
        assert "TOKEN" == datasource.spec.connections[0].databricks_connection.personal_access_token.secret_key

    def mock_datasource(self):
        return {
            "apiVersion": "xlscsde.nhs.uk/v1",
            "kind": "AnalyticsDataSource",
            "metadata": {
                "annotations": {
                    "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"xlscsde.nhs.uk/v1\",\"kind\":\"AnalyticsDataSource\",\"metadata\":{\"annotations\":{},\"labels\":{\"xlscsde.nhs.uk/type\":\"uploaded\"},\"name\":\"ds-782b4a1f07234229980f75f2f651412a\",\"namespace\":\"default\"},\"spec\":{\"connections\":[{\"databricksConnection\":{\"hostName\":\"test\",\"httpPath\":\"/test\",\"personalAccessToken\":{\"secretName\":\"test-secret\"}},\"name\":\"pvc-782b4a1f07234229980f75f2f651412a\",\"type\":\"pvc\"}],\"description\":\"An example dataset which the user has brought for themselves and uploaded into the system.\\n\",\"displayName\":\"An uploaded example dataset\",\"license\":\"This sample data may ONLY be used for demos\\n\",\"project\":{\"id\":\"d4e6\"},\"publisher\":{\"contact\":{\"name\":\"Joe Bloggs\",\"role\":\"Research Engineer\"},\"organisation\":\"Some Organisation\"},\"type\":\"Uploaded\"}}\n"
                },
                "creationTimestamp": "2024-12-27T16:03:32Z",
                "generation": 1,
                "labels": {
                    "xlscsde.nhs.uk/type": "uploaded"
                },
                "name": "ds-782b4a1f07234229980f75f2f651412a",
                "namespace": "default",
                "resourceVersion": "100448",
                "uid": "78f5e970-08bb-40c8-936d-d41561881a17"
            },
            "spec": {
                "connections": [
                    {
                        "databricksConnection": {
                            "hostName": "test",
                            "httpPath": "/test",
                            "personalAccessToken": {
                                "secretKey": "TOKEN",
                                "secretName": "test-secret"
                            }
                        },
                        "name": "pvc-782b4a1f07234229980f75f2f651412a",
                        "type": "pvc"
                    }
                ],
                "description": "An example dataset which the user has brought for themselves and uploaded into the system.\n",
                "displayName": "An uploaded example dataset",
                "license": "This sample data may ONLY be used for demos\n",
                "project": {
                    "id": "d4e6"
                },
                "publisher": {
                    "contact": {
                        "name": "Joe Bloggs",
                        "role": "Research Engineer"
                    },
                    "organisation": "Some Organisation"
                },
                "type": "Uploaded"
            }
        }