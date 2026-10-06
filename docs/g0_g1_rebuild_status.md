# G0/G1 Rebuild Status

**Date:** 2026-10-07

## Current state

The clean rebuild has started from the preregistered protocol in docs/preregistration_gate.md.

### Confirmed

- The personal research repository is active.
- The preregistration was committed before any new AL run.
- Historical data/results are treated as unvalidated.
- No patient-level healthcare data are being copied into this repository.
- The source branch manasvi in the collaborator repository is available for code audit.

### Source-code audit findings

The old manasvi branch contains several settings that must **not** be carried forward unchanged:

1. MIN_ICU_LOS_HOURS = 24 — conflicts with locked decision: **≥72h**.
2. The old LightGBM training code uses class_weight="balanced" — conflicts with G4.
3. The old active-learning loop evaluates the held-out test set repeatedly during the AL loop — conflicts with the requirement that the test set remain untouched.
4. The old feature extraction code fills unresolved value features with 0.0 — conflicts with G2 missingness rules.
5. The old nephrotoxin specification includes diuretics — conflicts with G2.
6. The old trajectory code uses a hard-coded 70 kg fallback — this must not become an implicit predictive signal; weight may only be used for urine-output normalization and then dropped.
7. The old nephrotoxin code uses 0 for hours_since_first when there has been no exposure; this sentinel is ambiguous and must be replaced with a preregistered representation.
8. The old creatinine trajectory reconstruction reads imputed/wide feature values rather than rebuilding slopes directly from observed pre-imputation measurements; this must be corrected.
9. The old environment is pinned to Python 3.10 with older package versions, while recovery notes mention a different later environment. This discrepancy is **not silently resolved**; dependency resolution must be completed in G0 and committed.

## G0 blockers

- [ ] Confirm working BigQuery credentials/project.
- [ ] Confirm access to required MIMIC-IV derived tables through INFORMATION_SCHEMA.TABLES.
- [ ] Resolve and commit the exact Python/package environment.
- [ ] Verify executable path and imported package versions.
- [ ] Freeze the clean feature specification before AL.

## G1 next actions

1. Rebuild the cohort from MIMIC-IV derived tables using the **≥72h ICU LOS** rule.
2. Use dot-free ICD codes together with icd_version.
3. Verify diagnosis titles from d_icd_diagnoses.
4. Apply the preregistered ESRD/transplant/RRT/prior-AKI exclusions.
5. Explicitly distinguish missing KDIGO evidence from no AKI.
6. Define and quantify baseline-creatinine coverage.
7. Produce stepwise cohort counts and an included-vs-excluded table.
8. Do not proceed to the AL gate until G1 passes.

## Important

The old numerical results are not evidence that any gate passes. They are historical notes only until reproduced under this clean rebuild.
