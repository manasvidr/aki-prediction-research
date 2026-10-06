# G0 — Setup and Environment Gate

**Status:** in progress

## Required evidence before G1

- [ ] Clean Python environment confirmed.
- [ ] Python executable/path recorded.
- [ ] Dependency versions recorded and committed.
- [ ] BigQuery authentication succeeds.
- [ ] Correct GCP/PhysioNet project is confirmed.
- [ ] `INFORMATION_SCHEMA.TABLES` confirms required MIMIC-IV derived tables.
- [ ] Historical results remain marked unvalidated.
- [ ] No patient-level rows, identifiers, credentials, or healthcare-derived artifacts are committed.

## Run

```bash
python scripts/g0_check.py
```

Then run the table-access query documented in `docs/g0_bigquery_check.sql`.

## Required derived-table checks

At minimum confirm access to the derived tables needed for:

- ICU stay timing/details
- diagnosis/ICD information
- creatinine and baseline creatinine
- urine output
- chemistry
- vitals
- KDIGO staging
- SOFA
- medication/nephrotoxin exposure

The exact table names must be verified from `INFORMATION_SCHEMA.TABLES`; do not assume that a historical local database has the required schema.

## G0 stop conditions

Stop before G1 if:

- BigQuery authentication fails.
- Required derived tables are unavailable.
- Dependency imports fail.
- Python executable/path is not the intended environment.
- The environment cannot be reproduced from the committed dependency specification.
- Any patient-level data would need to be committed to proceed.
