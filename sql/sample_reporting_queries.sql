-- SQL script: sample_reporting_queries.sql
-- Purpose: Business reporting queries for Azure Insurance Claims Analytics Lakehouse


-- 1. Check row counts for all Gold reporting tables

SELECT 'gold_claims_detail' AS table_name, COUNT(*) AS row_count
FROM dbo.gold_claims_detail

UNION ALL

SELECT 'gold_claims_by_status' AS table_name, COUNT(*) AS row_count
FROM dbo.gold_claims_by_status

UNION ALL

SELECT 'gold_claims_by_region' AS table_name, COUNT(*) AS row_count
FROM dbo.gold_claims_by_region

UNION ALL

SELECT 'gold_monthly_claim_trends' AS table_name, COUNT(*) AS row_count
FROM dbo.gold_monthly_claim_trends

UNION ALL

SELECT 'gold_high_value_claims' AS table_name, COUNT(*) AS row_count
FROM dbo.gold_high_value_claims;


-- 2. Claims summary by status

SELECT
    claim_status,
    total_claims,
    total_claim_amount,
    average_claim_amount,
    total_paid_amount
FROM dbo.gold_claims_by_status
ORDER BY total_claim_amount DESC;


-- 3. Claims summary by customer state

SELECT
    customer_state,
    total_claims,
    total_claim_amount,
    average_claim_amount
FROM dbo.gold_claims_by_region
ORDER BY total_claim_amount DESC;


-- 4. Monthly claim trends

SELECT
    claim_month,
    total_claims,
    total_claim_amount,
    average_claim_amount
FROM dbo.gold_monthly_claim_trends
ORDER BY claim_month;


-- 5. High value claims

SELECT
    claim_id,
    customer_name,
    customer_state,
    policy_type,
    claim_type,
    claim_amount,
    claim_status,
    claim_processing_days
FROM dbo.gold_high_value_claims
ORDER BY claim_amount DESC;


-- 6. Top 10 highest claims from the detailed Gold table

SELECT TOP 10
    claim_id,
    customer_name,
    customer_state,
    customer_segment,
    policy_type,
    claim_type,
    claim_amount,
    claim_status,
    payment_amount,
    claim_processing_days
FROM dbo.gold_claims_detail
ORDER BY claim_amount DESC;


-- 7. Average processing days by claim status

SELECT
    claim_status,
    COUNT(*) AS total_claims,
    AVG(claim_processing_days) AS average_processing_days
FROM dbo.gold_claims_detail
GROUP BY claim_status
ORDER BY average_processing_days DESC;