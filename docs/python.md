---
title: Python Module
layout: page
parent: Analytics Workspace Management Services
grand_parent: Architecture
has_children: true
---
The repository defines python modules for Analytics Workspace Management is located at [https://github.com/lsc-sde/py-lscsde-workspace-mgmt](https://github.com/lsc-sde/py-lscsde-workspace-mgmt)

This library produces models based on the custom resource definitions for:
* [AnalyticsCrates](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsCrates.md)
* [AnalyticsDataSources](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsDataSources.md)
* [AnalyticsDataSourceBindings](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsDataSourceBindings.md)
* [AnalyticsWorkspaces](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaces.md)
* [AnalyticsWorkspaceBindings](../../../iac/helm/analytics-workspace-management/docs/Custom-Resources/AnalyticsWorkspaceBindings.md)

Clients are then provided which allow services to interact with the various objects via the kubernetes API's. 

Additionally there are also converters which will provide conversion from pytest to other object types such as kubespawner override blocks.

# Installation
The module can be installed using the command

```bash
RUN pip install lscsde-workspace-mgmt
```

To install a specific version of the package, please use:
```bash
RUN pip install lscsde-workspace-mgmt==0.1.13
```

# Used by
The python library is used by:
* [The SDE customised jupyter hub image](../../../docker/jupyterhub/docs/image.md)
* [The AWMS Guacamole Operator](../../../products/sde/analytics-workspace-management/awms-guacamole-operator/docs/operator.md)
* [The AMWS Datasource Operator](../../../products/sde/analytics-datasource-management/awms-datasource-operator/docs/operator.md)
* [The AWMS Crate Operator](../../../products/sde/analytics-datasource-management/awms-crate-operator/docs/operator.md)

## Classes
[Documentation of the classes can be found here](./classes.md)
