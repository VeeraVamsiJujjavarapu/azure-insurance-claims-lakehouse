# Azure Data Factory Pipeline Documentation

## Pipeline Name

pl_load_gold_tables_to_sql

## Purpose

This pipeline loads Gold layer analytics CSV files from Azure Data Lake Storage Gen2 into Azure SQL Database reporting tables.

## Source

Azure Data Lake Storage Gen2

Container:

insurance-data

Source folder:

gold/csv_exports

Each Gold table is exported by Databricks as a CSV folder containing a file that starts with:

part-*.csv

## Sink

Azure SQL Database

Database:

sqldb-insurance-claims

## Linked Services

### ADLS Gen2 Linked Service

ls_adls_insurance_claims

Used to connect Azure Data Factory to Azure Data Lake Storage Gen2.

### Azure SQL Linked Service

ls_azuresql_insurance_claims

Used to connect Azure Data Factory to Azure SQL Database.

## Copy Activities

### 1. copy_gold_claims_by_status_to_sql

Source:

gold/csv_exports/gold_claims_by_status/part-*.csv

Sink:

dbo.gold_claims_by_status

Pre-copy script:

TRUNCATE TABLE dbo.gold_claims_by_status;

### 2. copy_gold_claims_by_region_to_sql

Source:

gold/csv_exports/gold_claims_by_region/part-*.csv

Sink:

dbo.gold_claims_by_region

Pre-copy script:

TRUNCATE TABLE dbo.gold_claims_by_region;

### 3. copy_gold_monthly_claim_trends_to_sql

Source:

gold/csv_exports/gold_monthly_claim_trends/part-*.csv

Sink:

dbo.gold_monthly_claim_trends

Pre-copy script:

TRUNCATE TABLE dbo.gold_monthly_claim_trends;

### 4. copy_gold_high_value_claims_to_sql

Source:

gold/csv_exports/gold_high_value_claims/part-*.csv

Sink:

dbo.gold_high_value_claims

Pre-copy script:

TRUNCATE TABLE dbo.gold_high_value_claims;

### 5. copy_gold_claims_detail_to_sql

Source:

gold/csv_exports/gold_claims_detail/part-*.csv

Sink:

dbo.gold_claims_detail

Pre-copy script:

TRUNCATE TABLE dbo.gold_claims_detail;

## Pipeline Flow

1. Databricks creates Gold Delta tables.
2. Databricks exports Gold tables as CSV files to ADLS Gen2.
3. ADF reads each Gold CSV folder using wildcard file name part-*.csv.
4. ADF truncates the matching Azure SQL table before loading.
5. ADF inserts the latest Gold data into Azure SQL.
6. Azure SQL becomes the final reporting layer.

## Validation

The pipeline was tested using Debug mode.

All 5 Copy data activities completed successfully.

## Notes

Spark writes CSV output as folders, not as a single named file.

That is why the ADF source uses:

part-*.csv

This avoids reading Spark system files like:

_SUCCESS
_committed_*
_started_*