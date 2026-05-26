-- SQL script: create_gold_tables.sql
-- Purpose: Create Azure SQL reporting tables for Gold layer outputs

DROP TABLE IF EXISTS dbo.gold_claims_detail;
DROP TABLE IF EXISTS dbo.gold_claims_by_status;
DROP TABLE IF EXISTS dbo.gold_claims_by_region;
DROP TABLE IF EXISTS dbo.gold_monthly_claim_trends;
DROP TABLE IF EXISTS dbo.gold_high_value_claims;

CREATE TABLE dbo.gold_claims_detail (
    claim_id VARCHAR(50),
    policy_id VARCHAR(50),
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    customer_state VARCHAR(10),
    customer_segment VARCHAR(50),
    policy_type VARCHAR(50),
    premium_amount FLOAT,
    claim_type VARCHAR(100),
    claim_amount FLOAT,
    claim_status VARCHAR(50),
    claim_date DATE,
    settlement_date DATE,
    payment_amount FLOAT,
    payment_date DATE,
    payment_method VARCHAR(50),
    claim_processing_days INT
);

CREATE TABLE dbo.gold_claims_by_status (
    claim_status VARCHAR(50),
    total_claims INT,
    total_claim_amount FLOAT,
    average_claim_amount FLOAT,
    total_paid_amount FLOAT
);

CREATE TABLE dbo.gold_claims_by_region (
    customer_state VARCHAR(10),
    total_claims INT,
    total_claim_amount FLOAT,
    average_claim_amount FLOAT
);

CREATE TABLE dbo.gold_monthly_claim_trends (
    claim_month VARCHAR(20),
    total_claims INT,
    total_claim_amount FLOAT,
    average_claim_amount FLOAT
);

CREATE TABLE dbo.gold_high_value_claims (
    claim_id VARCHAR(50),
    policy_id VARCHAR(50),
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    customer_state VARCHAR(10),
    customer_segment VARCHAR(50),
    policy_type VARCHAR(50),
    premium_amount FLOAT,
    claim_type VARCHAR(100),
    claim_amount FLOAT,
    claim_status VARCHAR(50),
    claim_date DATE,
    settlement_date DATE,
    payment_amount FLOAT,
    payment_date DATE,
    payment_method VARCHAR(50),
    claim_processing_days INT
);