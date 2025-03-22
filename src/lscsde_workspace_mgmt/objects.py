from datetime import datetime, timedelta
from .models import AnalyticsWorkspace


class AnalyticsWorkspaceConverter:
    """
    The converter allows us to perform operations against an analytics workspace to convert them for use in other platforms.

    This class is responsible for transforming AnalyticsWorkspace objects into formats suitable for various purposes,
    especially for kubespawner configurations. It provides utility methods to calculate expiry times and
    convert workspace objects to dictionary representations that can be directly consumed by kubespawner.

    The converter handles all aspects of workspace configuration translation including resource requirements,
    image specifications, node selection policies, and environment configurations.
    """

    def days_until_expiry(self, time_str, date_now=datetime.today()):
        """
        Calculates the number of days until the workspace or workspace binding expires.

        Args:
            time_str (str): The expiration date string in "YYYY-MM-DD" format.
            date_now (datetime, optional): The reference date to calculate from.
                                          Defaults to today's date.
                                          Primarily used for testing.

        Returns:
            timedelta: A timedelta object representing the days remaining until expiry.
        """
        ws_end_date = datetime.strptime(time_str, "%Y-%m-%d")
        ws_days_left: timedelta = ws_end_date - date_now
        return ws_days_left

    def to_workspace_dict(
        self, workspace: AnalyticsWorkspace, date_now=datetime.today()
    ):
        """
        Converts the workspace to the dictionary used by kubespawner to create the pod resource.

        This method transforms an AnalyticsWorkspace object into a dictionary format that kubespawner
        can use directly to provision and configure Jupyter notebook pods in a Kubernetes environment.
        It extracts and formats all relevant configurations including resource limits, image specs,
        node selectors, and other pod settings.

        Args:
            workspace (AnalyticsWorkspace): The workspace object to convert.
            date_now (datetime, optional): The reference date for calculating expiry.
                                          Defaults to today's date.

        Returns:
            dict: A dictionary containing all kubespawner configuration parameters derived from
                 the workspace specification.
        """
        # Initialize the basic workspace information
        contents = {}
        contents["display_name"] = workspace.spec.display_name
        contents["description"] = workspace.spec.description

        if workspace.spec.jupyter_workspace:
            # Include the original workspace definition for reference
            contents["workspace_definition"] = workspace.spec.jupyter_workspace

            # Configure kubespawner-specific overrides
            contents["kubespawner_override"] = {}
            contents["kubespawner_override"]["image"] = (
                workspace.spec.jupyter_workspace.image
            )

            # Set up labels, ensuring workspace name is always included
            extra_labels = {}
            if workspace.spec.jupyter_workspace.extra_labels:
                extra_labels = workspace.spec.jupyter_workspace.extra_labels.copy()
            extra_labels["workspace"] = workspace.metadata.name
            contents["kubespawner_override"]["extra_labels"] = extra_labels

            # Configure resource limits and requests if specified
            if workspace.spec.jupyter_workspace.resources:
                # Memory request configuration
                mem_guarantee = workspace.spec.jupyter_workspace.resources["requests"][
                    "memory"
                ]
                if mem_guarantee:
                    contents["kubespawner_override"]["mem_guarantee"] = mem_guarantee

                # Memory limit configuration
                mem_limit = workspace.spec.jupyter_workspace.resources["limits"][
                    "memory"
                ]
                if mem_limit:
                    contents["kubespawner_override"]["mem_limit"] = mem_limit

                # CPU request configuration
                cpu_guarantee = workspace.spec.jupyter_workspace.resources["requests"][
                    "cpu"
                ]
                if cpu_guarantee:
                    contents["kubespawner_override"]["cpu_guarantee"] = cpu_guarantee

                # CPU limit configuration
                cpu_limit = workspace.spec.jupyter_workspace.resources["limits"]["cpu"]
                if cpu_limit:
                    contents["kubespawner_override"]["cpu_limit"] = cpu_limit

            # Set default URL if specified
            default_url = workspace.spec.jupyter_workspace.default_uri
            if default_url:
                contents["kubespawner_override"]["default_url"] = default_url

            # Configure node selection if specified
            if workspace.spec.jupyter_workspace.node_selector:
                contents["kubespawner_override"]["node_selector"] = (
                    workspace.spec.jupyter_workspace.node_selector
                )

            # Configure tolerations if specified
            if workspace.spec.jupyter_workspace.tolerations:
                contents["kubespawner_override"]["tolerations"] = (
                    workspace.spec.jupyter_workspace.tolerations
                )

        # Set basic workspace identification and time information
        contents["slug"] = workspace.metadata.name
        contents["start_date"] = workspace.spec.validity.available_from
        contents["end_date"] = workspace.spec.validity.expires
        contents["ws_days_left"] = self.days_until_expiry(
            workspace.spec.validity.expires, date_now=date_now
        )
        return contents
