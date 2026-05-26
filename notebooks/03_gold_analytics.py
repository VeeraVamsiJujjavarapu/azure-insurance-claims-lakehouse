# Databricks notebook: 03_gold_analytics
# Purpose: Create business-ready Gold analytics tables from Silver Delta tables

from pyspark.sql.functions import (
    col,
    count,
    sum as spark_sum,
    avg,
    round,
    date_format,
    datediff,
    current_date,
    coalesce
)

storage_account_name = "stinsuranceclaimsvv"
container_name = "insurance-data"

silver_base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/silver"
gold_base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/gold"

claims_silver_df = spark.read.format("delta").load(f"{silver_base_path}/claims_clean")
customers_silver_df = spark.read.format("delta").load(f"{silver_base_path}/customers_clean")
policies_silver_df = spark.read.format("delta").load(f"{silver_base_path}/policies_clean")
payments_silver_df = spark.read.format("delta").load(f"{silver_base_path}/payments_clean")

print("Silver data loaded successfully")
print("Claims:", claims_silver_df.count())
print("Customers:", customers_silver_df.count())
print("Policies:", policies_silver_df.count())
print("Payments:", payments_silver_df.count())


# --------------------------------------------------
# Gold Table 1: Claims detail enriched table
# --------------------------------------------------

gold_claims_detail_df = (
    claims_silver_df.alias("c")
    .join(
        policies_silver_df.alias("p"),
        col("c.policy_id") == col("p.policy_id"),
        "left"
    )
    .join(
        customers_silver_df.alias("cu"),
        col("c.customer_id") == col("cu.customer_id"),
        "left"
    )
    .join(
        payments_silver_df.alias("pay"),
        col("c.claim_id") == col("pay.claim_id"),
        "left"
    )
    .select(
        col("c.claim_id"),
        col("c.policy_id"),
        col("c.customer_id"),
        col("cu.customer_name"),
        col("cu.customer_state"),
        col("cu.customer_segment"),
        col("p.policy_type"),
        col("p.premium_amount"),
        col("c.claim_type"),
        col("c.claim_amount"),
        col("c.claim_status"),
        col("c.claim_date"),
        col("c.settlement_date"),
        col("pay.payment_amount"),
        col("pay.payment_date"),
        col("pay.payment_method"),
        datediff(
            coalesce(col("c.settlement_date"), current_date()),
            col("c.claim_date")
        ).alias("claim_processing_days")
    )
)


# --------------------------------------------------
# Gold Table 2: Claims summary by status
# --------------------------------------------------

gold_claims_by_status_df = (
    gold_claims_detail_df
    .groupBy("claim_status")
    .agg(
        count("claim_id").alias("total_claims"),
        round(spark_sum("claim_amount"), 2).alias("total_claim_amount"),
        round(avg("claim_amount"), 2).alias("average_claim_amount"),
        round(spark_sum("payment_amount"), 2).alias("total_paid_amount")
    )
    .orderBy("claim_status")
)


# --------------------------------------------------
# Gold Table 3: Claims summary by customer state
# --------------------------------------------------

gold_claims_by_region_df = (
    gold_claims_detail_df
    .groupBy("customer_state")
    .agg(
        count("claim_id").alias("total_claims"),
        round(spark_sum("claim_amount"), 2).alias("total_claim_amount"),
        round(avg("claim_amount"), 2).alias("average_claim_amount")
    )
    .orderBy(col("total_claim_amount").desc())
)


# --------------------------------------------------
# Gold Table 4: Monthly claim trends
# --------------------------------------------------

gold_monthly_claim_trends_df = (
    gold_claims_detail_df
    .withColumn("claim_month", date_format(col("claim_date"), "yyyy-MM"))
    .groupBy("claim_month")
    .agg(
        count("claim_id").alias("total_claims"),
        round(spark_sum("claim_amount"), 2).alias("total_claim_amount"),
        round(avg("claim_amount"), 2).alias("average_claim_amount")
    )
    .orderBy("claim_month")
)


# --------------------------------------------------
# Gold Table 5: High value claims
# --------------------------------------------------

gold_high_value_claims_df = (
    gold_claims_detail_df
    .filter(col("claim_amount") >= 10000)
    .orderBy(col("claim_amount").desc())
)


# --------------------------------------------------
# Save Gold tables as Delta in ADLS Gold layer
# --------------------------------------------------

gold_claims_detail_df.write.mode("overwrite").format("delta").save(f"{gold_base_path}/gold_claims_detail")
gold_claims_by_status_df.write.mode("overwrite").format("delta").save(f"{gold_base_path}/gold_claims_by_status")
gold_claims_by_region_df.write.mode("overwrite").format("delta").save(f"{gold_base_path}/gold_claims_by_region")
gold_monthly_claim_trends_df.write.mode("overwrite").format("delta").save(f"{gold_base_path}/gold_monthly_claim_trends")
gold_high_value_claims_df.write.mode("overwrite").format("delta").save(f"{gold_base_path}/gold_high_value_claims")

print("Gold Delta tables created successfully")


# --------------------------------------------------
# Export Gold tables as CSV for Azure Data Factory
# --------------------------------------------------

gold_csv_base_path = f"{gold_base_path}/csv_exports"

gold_claims_detail_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(
    f"{gold_csv_base_path}/gold_claims_detail"
)

gold_claims_by_status_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(
    f"{gold_csv_base_path}/gold_claims_by_status"
)

gold_claims_by_region_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(
    f"{gold_csv_base_path}/gold_claims_by_region"
)

gold_monthly_claim_trends_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(
    f"{gold_csv_base_path}/gold_monthly_claim_trends"
)

gold_high_value_claims_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(
    f"{gold_csv_base_path}/gold_high_value_claims"
)

print("Gold CSV exports created successfully")
print(gold_csv_base_path)


# --------------------------------------------------
# Display Gold analytics outputs
# --------------------------------------------------

print("Claims by Status")
display(gold_claims_by_status_df)

print("Claims by Region")
display(gold_claims_by_region_df)

print("Monthly Claim Trends")
display(gold_monthly_claim_trends_df)

print("High Value Claims")
display(gold_high_value_claims_df)