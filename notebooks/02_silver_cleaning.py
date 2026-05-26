# Databricks notebook: 02_silver_cleaning
# Purpose: Clean Bronze insurance data and save cleaned Delta tables to Silver layer

from pyspark.sql.functions import col, upper, trim, current_date
from pyspark.sql.types import DoubleType, DateType

storage_account_name = "stinsuranceclaimsvv"
container_name = "insurance-data"

bronze_base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/bronze/raw"
silver_base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/silver"

customers_path = f"{bronze_base_path}/customers.csv"
policies_path = f"{bronze_base_path}/policies.csv"
claims_path = f"{bronze_base_path}/claims.csv"
payments_path = f"{bronze_base_path}/payments.csv"

customers_df = spark.read.option("header", "true").csv(customers_path)
policies_df = spark.read.option("header", "true").csv(policies_path)
claims_df = spark.read.option("header", "true").csv(claims_path)
payments_df = spark.read.option("header", "true").csv(payments_path)

print("Bronze files loaded into Silver cleaning notebook")


# -----------------------------
# Clean claims data
# -----------------------------

claims_dedup_df = claims_df.dropDuplicates()

claims_cleaning_df = (
    claims_dedup_df
    .withColumn("claim_id", trim(col("claim_id")))
    .withColumn("policy_id", trim(col("policy_id")))
    .withColumn("customer_id", trim(col("customer_id")))
    .withColumn("claim_type", trim(col("claim_type")))
    .withColumn("claim_status", upper(trim(col("claim_status"))))
    .withColumn("claim_amount", col("claim_amount").cast("double"))
    .withColumn("claim_date", col("claim_date").cast("date"))
    .withColumn("settlement_date", col("settlement_date").cast("date"))
)

valid_statuses = ["OPEN", "PENDING", "APPROVED", "PAID", "REJECTED", "CLOSED"]

claims_quarantine_df = claims_cleaning_df.filter(
    col("claim_id").isNull() |
    col("policy_id").isNull() |
    col("customer_id").isNull() |
    col("claim_amount").isNull() |
    (col("claim_amount") <= 0) |
    col("claim_date").isNull() |
    (col("claim_date") > current_date()) |
    (~col("claim_status").isin(valid_statuses))
)

claims_silver_df = claims_cleaning_df.filter(
    col("claim_id").isNotNull() &
    col("policy_id").isNotNull() &
    col("customer_id").isNotNull() &
    col("claim_amount").isNotNull() &
    (col("claim_amount") > 0) &
    col("claim_date").isNotNull() &
    (col("claim_date") <= current_date()) &
    (col("claim_status").isin(valid_statuses))
)

claims_silver_df.write.mode("overwrite").format("delta").save(f"{silver_base_path}/claims_clean")
claims_quarantine_df.write.mode("overwrite").format("delta").save(f"{silver_base_path}/claims_quarantine")

print("Raw claims count:", claims_df.count())
print("Claims count after duplicate removal:", claims_dedup_df.count())
print("Clean Silver claims count:", claims_silver_df.count())
print("Quarantine claims count:", claims_quarantine_df.count())


# -----------------------------
# Clean customers data
# -----------------------------

customers_silver_df = (
    customers_df
    .dropDuplicates()
    .withColumn("customer_id", trim(col("customer_id")))
    .withColumn("customer_name", trim(col("customer_name")))
    .withColumn("customer_state", upper(trim(col("customer_state"))))
    .withColumn("customer_segment", trim(col("customer_segment")))
    .withColumn("signup_date", col("signup_date").cast("date"))
    .filter(
        col("customer_id").isNotNull() &
        col("customer_name").isNotNull() &
        col("customer_state").isNotNull()
    )
)


# -----------------------------
# Clean policies data
# -----------------------------

policies_silver_df = (
    policies_df
    .dropDuplicates()
    .withColumn("policy_id", trim(col("policy_id")))
    .withColumn("customer_id", trim(col("customer_id")))
    .withColumn("policy_type", trim(col("policy_type")))
    .withColumn("policy_start_date", col("policy_start_date").cast("date"))
    .withColumn("policy_end_date", col("policy_end_date").cast("date"))
    .withColumn("premium_amount", col("premium_amount").cast("double"))
    .filter(
        col("policy_id").isNotNull() &
        col("customer_id").isNotNull() &
        col("premium_amount").isNotNull() &
        (col("premium_amount") > 0)
    )
)


# -----------------------------
# Clean payments data
# -----------------------------

payments_silver_df = (
    payments_df
    .dropDuplicates()
    .withColumn("payment_id", trim(col("payment_id")))
    .withColumn("claim_id", trim(col("claim_id")))
    .withColumn("payment_amount", col("payment_amount").cast("double"))
    .withColumn("payment_date", col("payment_date").cast("date"))
    .withColumn("payment_method", upper(trim(col("payment_method"))))
    .filter(
        col("payment_id").isNotNull() &
        col("claim_id").isNotNull() &
        col("payment_amount").isNotNull() &
        (col("payment_amount") >= 0)
    )
)


# -----------------------------
# Save cleaned data to Silver layer
# -----------------------------

customers_silver_df.write.mode("overwrite").format("delta").save(f"{silver_base_path}/customers_clean")
policies_silver_df.write.mode("overwrite").format("delta").save(f"{silver_base_path}/policies_clean")
payments_silver_df.write.mode("overwrite").format("delta").save(f"{silver_base_path}/payments_clean")

print("Clean Silver customers count:", customers_silver_df.count())
print("Clean Silver policies count:", policies_silver_df.count())
print("Clean Silver payments count:", payments_silver_df.count())