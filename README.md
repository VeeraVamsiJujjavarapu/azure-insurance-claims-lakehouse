# Azure Insurance Claims Analytics Lakehouse

## Project Overview

This project is an end-to-end Azure data engineering portfolio project.

It processes fake insurance claims data using a Medallion Architecture with Bronze, Silver, and Gold layers.

The project demonstrates how raw insurance claim files can be ingested, cleaned, transformed, and loaded into Azure SQL Database for analytics and reporting.

## Business Problem

Insurance companies receive claim, policy, customer, and payment data from different systems.

Raw data can contain issues such as:

- Duplicate claim records
- Missing values
- Negative claim amounts
- Future claim dates
- Inconsistent claim statuses
- Incomplete customer information

Business teams need clean and trusted data to answer questions such as:

- How many claims are open, approved, paid, rejected, or closed?
- Which customer regions have the highest claim amounts?
- What are the monthly claim trends?
- Which claims are high value?
- How long does claim processing take?

## Final Solution

This project builds a cloud data pipeline using Azure services.

The pipeline:

1. Stores raw CSV files in Azure Data Lake Storage Gen2.
2. Reads raw files from the Bronze layer using Azure Databricks.
3. Cleans and validates data using PySpark.
4. Stores cleaned Delta tables in the Silver layer.
5. Creates business-ready Gold analytics tables.
6. Exports Gold tables as CSV files to ADLS Gen2.
7. Uses Azure Data Factory to load Gold CSV files into Azure SQL Database.
8. Provides SQL reporting queries for analytics.

## Tech Stack

- Azure Data Lake Storage Gen2
- Azure Databricks
- PySpark
- Delta Lake
- Azure Data Factory
- Azure SQL Database
- SQL
- Git
- GitHub
- Visual Studio Code

## Architecture

```text
Local CSV Files
      |
      v
Azure Data Lake Storage Gen2
      |
      v
Bronze Layer
Raw CSV files
      |
      v
Azure Databricks + PySpark
Cleaning and validation
      |
      v
Silver Layer
Clean Delta tables
      |
      v
Azure Databricks + PySpark
Business transformations
      |
      v
Gold Layer
Analytics Delta tables and CSV exports
      |
      v
Azure Data Factory
Copy Gold CSV files
      |
      v
Azure SQL Database
Final reporting tables