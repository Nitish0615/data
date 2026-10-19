# saayam-org-aggregator Lambda

This folder contains the initial version of the Saayam Org Aggregator Lambda.  
It handles:
- Beneficiary location lookup (request → user → profile → geocode)
- Organization location lookup (address → geocode or online flag)
- Straight‑line distance calculation using the Haversine formula
- Adding distance + status fields to each organization record

## Notes
I do not have access to Saayam DB credentials.  
The DB connection code is included with placeholder values.  
Reviewers can add real credentials later through AWS Lambda environment variables or Secrets Manager.

Local testing was done using mock data in `test_local.py` to verify:
- Distance calculation
- Online org handling
- Location fallback logic

This Lambda is newly added to the repo under:
`data/data-analytics/lambda_functions/saayam-org-aggregator`
