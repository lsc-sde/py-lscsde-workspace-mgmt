# LSCSDE Workspace Management

The `lscsde-workspace-mgmt` Python library provides models and clients for interacting with Kubernetes custom resources for workspace management.

## Overview

This library produces models based on the custom resource definitions for:

* AnalyticsCrates
* AnalyticsDataSources
* AnalyticsDataSourceBindings
* AnalyticsWorkspaces
* AnalyticsWorkspaceBindings

Clients are provided to interact with these resources through the Kubernetes API.

## Key Features

- Strongly typed models for all resources using Pydantic
- Asynchronous Kubernetes clients for each resource type
- Workspace and data source management capabilities
- Kubernetes event integration
- Persistent volume claim handling
- Converters for integration with JupyterHub KubeSpawner

## Used By

The library is used by:

* The SDE customised JupyterHub image
* The AWMS Guacamole Operator
* The AMWS Datasource Operator
* The AWMS Crate Operator
