# Databricks notebook: 01_bronze_ingestion
# Purpose: Read raw Bronze CSV files from ADLS Gen2 and validate row counts

storage_account_name = "stinsuranceclaimsvv"
container_name = "insurance-data"

bronze_base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/bronze/raw"

customers_path = f"{bronze_base_path}/customers.csv"
policies_path = f"{bronze_base_path}/policies.csv"
claims_path = f"{bronze_base_path}/claims.csv"
payments_path = f"{bronze_base_path}/payments.csv"

customers_df = spark.read.option("header", "true").csv(customers_path)
policies_df = spark.read.option("header", "true").csv(policies_path)
claims_df = spark.read.option("header", "true").csv(claims_path)
payments_df = spark.read.option("header", "true").csv(payments_path)

print("Bronze data loaded successfully")
print("Customers count:", customers_df.count())
print("Policies count:", policies_df.count())
print("Claims count:", claims_df.count())
print("Payments count:", payments_df.count())