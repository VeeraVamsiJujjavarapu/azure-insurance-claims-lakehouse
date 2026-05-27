# Architecture Diagram

## Azure Insurance Claims Analytics Lakehouse

```text
Local CSV Files
customers.csv
policies.csv
claims.csv
payments.csv
        |
        v
Azure Data Lake Storage Gen2
Container: insurance-data
        |
        v
Bronze Layer
Raw CSV files
        |
        v
Azure Databricks
PySpark cleaning and validation
        |
        v
Silver Layer
Clean Delta tables
Quarantine table for bad claims
        |
        v
Azure Databricks
Gold business transformations
        |
        v
Gold Layer
Delta tables and CSV exports
        |
        v
Azure Data Factory
Pipeline: pl_load_gold_tables_to_sql
        |
        v
Azure SQL Database
Final reporting tables
        |
        v
Business Reporting
SQL queries / Power BI-ready tables