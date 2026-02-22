# RiskGuard – Assurance Analytics Report

## Objective

Perform repeatable, data-driven control testing to support 2LOD assurance reviews by identifying exceptions, summarising results, and generating evidence-based recommendations.

## Summary

- Total exceptions identified: **9**
- Exceptions by control: `{'C01': 5, 'C03': 2, 'C02': 1, 'C04': 1}`
- Exceptions by risk rating: `{'Medium': 6, 'Low': 2, 'High': 1}`

## Controls Tested

- **C01:** High value transactions require at least 2 approvals
- **C02:** Segregation of duties (maker cannot approve own transaction)
- **C03:** Approvals completed within SLA
- **C04:** Duplicate payments detection

## Exceptions Register (Top 20)

| control_id   | risk_rating   | txn_id   | txn_ts              | account_id   | counterparty   |   amount | exception_reason                      |
|:-------------|:--------------|:---------|:--------------------|:-------------|:---------------|---------:|:--------------------------------------|
| C01          | Medium        | t0002    | 2026-02-10 10:05:00 | acc01        | VendorA        |    10500 | High value txn has < 2 approvals      |
| C01          | Medium        | t0004    | 2026-02-11 08:50:00 | acc03        | VendorC        |    12000 | High value txn has < 2 approvals      |
| C01          | Medium        | t0005    | 2026-02-11 09:02:00 | acc03        | VendorC        |    12000 | High value txn has < 2 approvals      |
| C01          | Medium        | t0007    | 2026-02-12 16:40:00 | acc02        | VendorE        |    18000 | High value txn has < 2 approvals      |
| C01          | Medium        | t0008    | 2026-02-13 11:15:00 | acc02        | VendorE        |    18000 | High value txn has < 2 approvals      |
| C02          | High          | t0002    | 2026-02-10 10:05:00 | acc01        | VendorA        |    10500 | Maker approved own transaction        |
| C03          | Low           | t0004    | 2026-02-11 08:50:00 | acc03        | VendorC        |    12000 | First approval exceeded SLA (24h)     |
| C03          | Low           | t0007    | 2026-02-12 16:40:00 | acc02        | VendorE        |    18000 | First approval exceeded SLA (24h)     |
| C04          | Medium        | t0005    | 2026-02-11 09:02:00 | acc03        | VendorC        |    12000 | Potential duplicate within 60 minutes |

## Recommendations (Actionable)

1. Confirm **control design**: validate high-value approval thresholds and required approval levels.
2. Improve **operating effectiveness**: implement preventive checks to block maker self-approval.
3. Enhance **monitoring**: create periodic exception dashboards and trend exception rates by business unit.
4. Strengthen **traceability**: ensure approvals retain full audit trail metadata (who/when/level/decision).

## Notes

- This prototype uses **synthetic data** to demonstrate assurance-style analytics and reporting.
