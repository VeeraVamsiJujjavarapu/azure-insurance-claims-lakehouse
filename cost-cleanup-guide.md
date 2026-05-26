# Azure Cost Cleanup Guide

## Purpose

This guide explains how to control Azure costs after completing the Azure Insurance Claims Analytics Lakehouse project.

## Resources Created

The project created these Azure resources:

- Resource Group
- Azure Data Lake Storage Gen2
- Azure Data Factory
- Azure Databricks Workspace
- Azure Databricks Access Connector
- Azure SQL Server
- Azure SQL Database

## Cost Control Notes

Azure services may use credits while resources are active.

To reduce cost:

- Stop or avoid running Databricks compute when not needed.
- Do not run ADF pipelines repeatedly unless testing.
- Use small SQL Database settings.
- Delete the full resource group when the project is no longer needed.

## Safest Cleanup Method

The safest way to remove all project resources is to delete the project resource group.

Resource group name:

rg-insurance-claims-lakehouse

## Steps to Delete Resource Group

1. Open Azure Portal.
2. Search for Resource groups.
3. Open rg-insurance-claims-lakehouse.
4. Click Delete resource group.
5. Type the resource group name when asked.
6. Confirm deletion.

## Warning

Deleting the resource group removes all Azure resources inside it.

Do this only after:

- The project is complete.
- Screenshots are captured.
- Code is saved locally.
- GitHub repository is updated.

## Recommended Before Deleting

Before deleting Azure resources, save these screenshots:

- Resource group with all resources
- ADLS Bronze, Silver, and Gold folders
- Databricks notebooks
- ADF pipeline success
- Azure SQL query results

## Project Status

Cleanup should be done only after final documentation and GitHub publishing are complete.