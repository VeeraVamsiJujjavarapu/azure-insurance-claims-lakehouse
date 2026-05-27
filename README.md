# Azure Insurance Claims Analytics Lakehouse

## Project Overview

This is an end-to-end Azure data engineering portfolio project.

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
- Which regions have the highest claim amounts?
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
```

## Data Layers

### Bronze Layer

The Bronze layer stores raw CSV files exactly as received.

Files:

- customers.csv
- policies.csv
- claims.csv
- payments.csv

### Silver Layer

The Silver layer stores cleaned and validated Delta tables.

Cleaning steps include:

- Removing duplicate records
- Standardizing text fields
- Converting amount columns to numeric values
- Converting date columns to date format
- Removing invalid claim records
- Separating bad claim records into a quarantine table

Silver outputs:

- customers_clean
- policies_clean
- claims_clean
- claims_quarantine
- payments_clean

### Gold Layer

The Gold layer stores business-ready analytics tables.

Gold outputs:

- gold_claims_detail
- gold_claims_by_status
- gold_claims_by_region
- gold_monthly_claim_trends
- gold_high_value_claims

## Azure SQL Reporting Tables

The final Azure SQL tables are:

- dbo.gold_claims_detail
- dbo.gold_claims_by_status
- dbo.gold_claims_by_region
- dbo.gold_monthly_claim_trends
- dbo.gold_high_value_claims

These tables can be used by analysts, dashboards, or reporting tools.

## Data Quality Checks

The project handles common data quality issues:

- Duplicate claim records
- Missing claim amount
- Negative claim amount
- Future claim date
- Lowercase claim status
- Missing customer state

Bad claim records are written to a quarantine table instead of being silently deleted.

## Sample Business Queries

The project includes SQL queries for:

- Row count validation
- Claims summary by status
- Claims summary by region
- Monthly claim trends
- High value claims
- Top 10 highest claims
- Average processing days by claim status

See:

```text
sql/sample_reporting_queries.sql
```

## Project Folder Structure

```text
azure-insurance-claims-lakehouse/
│
├── adf/
│   └── pipeline_documentation.md
│
├── data/
│   └── raw/
│       ├── customers.csv
│       ├── policies.csv
│       ├── claims.csv
│       └── payments.csv
│
├── diagrams/
│   └── architecture-diagram.md
│
├── notebooks/
│   ├── 01_bronze_ingestion.py
│   ├── 02_silver_cleaning.py
│   └── 03_gold_analytics.py
│
├── screenshots/
│
├── sql/
│   ├── create_gold_tables.sql
│   └── sample_reporting_queries.sql
│
├── .gitignore
├── README.md
├── cost-cleanup-guide.md
└── data_dictionary.md
```

## Pipeline Summary

### Databricks Notebooks

1. 01_bronze_ingestion.py

Reads raw CSV files from the Bronze layer and validates row counts.

2. 02_silver_cleaning.py

Cleans raw data, applies validation rules, saves clean data to Silver, and separates bad records into quarantine.

3. 03_gold_analytics.py

Creates business-ready Gold tables and exports them as CSV files for Azure Data Factory.

### Azure Data Factory Pipeline

Pipeline name:

```text
pl_load_gold_tables_to_sql
```

The pipeline loads Gold CSV files from ADLS Gen2 into Azure SQL Database.

Copy activities:

- copy_gold_claims_by_status_to_sql
- copy_gold_claims_by_region_to_sql
- copy_gold_monthly_claim_trends_to_sql
- copy_gold_high_value_claims_to_sql
- copy_gold_claims_detail_to_sql

## Key Skills Demonstrated

- Cloud data lake design
- Azure Data Lake Storage Gen2
- Medallion Architecture
- PySpark data cleaning
- Delta Lake table creation
- Data quality validation
- Quarantine handling
- Azure Data Factory pipeline development
- Azure SQL reporting layer
- SQL analytics queries
- End-to-end data engineering workflow

