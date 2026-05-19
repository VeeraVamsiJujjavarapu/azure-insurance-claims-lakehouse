# Azure Insurance Claims Sample Dataset

This dataset is fully fake and safe to use for a portfolio project.

## Files

### customers.csv
Customer master data.

Important columns:
- customer_id: Unique customer identifier
- customer_name: Fake customer name
- customer_state: US state code
- customer_segment: Individual, Family, or Business
- signup_date: Date customer joined

### policies.csv
Insurance policy data.

Important columns:
- policy_id: Unique policy identifier
- customer_id: Links policy to customer
- policy_type: Auto, Home, Life, or Commercial
- premium_amount: Policy premium amount

### claims.csv
Insurance claim transactions.

Important columns:
- claim_id: Unique claim identifier
- policy_id: Links claim to policy
- customer_id: Links claim to customer
- claim_type: Type of claim
- claim_amount: Claimed amount
- claim_status: Open, Pending, Approved, Paid, Rejected, or Closed
- claim_date: Date claim was filed
- settlement_date: Date claim was settled, if available

### payments.csv
Claim payment data.

Important columns:
- payment_id: Unique payment identifier
- claim_id: Links payment to claim
- payment_amount: Amount paid
- payment_date: Date payment was made
- payment_method: ACH, Check, or Wire

## Intentional data quality issues

These issues are included on purpose so the project can show data cleaning skills:

- claims.csv has one duplicate claim record: CLM015
- claims.csv has one negative claim amount: CLM010
- claims.csv has one missing claim amount: CLM011
- claims.csv has one lowercase status value: approved
- claims.csv has one future claim date: CLM020
- customers.csv has one missing customer_state value: CUST011
