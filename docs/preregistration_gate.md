# AKI Prediction Research — Preregistration & Recovery Gate

**Date:** 2026-10-07  
**Status:** Pre-registered protocol for clean rebuild

> This document is the operational source of truth for the recovery experiment. Historical numbers from prior runs are **unvalidated** unless reproduced under this protocol. No row-level patient data or patient identifiers belong in this repository, chat, or public artifacts.

## Locked decisions

1. **ICU length-of-stay cutoff:** ICU LOS **≥72 hours**.
   - Rationale: included patients have a fully observed 48-hour prediction/outcome window.
   - Because this cutoff can induce selection bias, report an included-vs-excluded table.

2. **Old Gate-1 pipeline:** **Skip it.**
   - The old data/mask artifacts are gone and rebuilding the buggy pipeline would be costly.
   - Run the active-learning gate once on clean features.
   - This is an explicit deviation from the original protocol §0.6 and must be stated as such.

3. **Gate label:** **Binary KDIGO AKI** for the active-learning gate.
   - Persistent AKI is reserved for the post-gate analysis if the gate passes.

4. **Active-learning evaluation window:** **600–1,500 labels**, pending confirmation that this region is unsaturated using a random-only learning curve on clean data. Freeze the final window before the AL comparison.

## G0 — Setup and provenance

- [ ] Fresh environment with pinned/import-clean dependencies.
- [ ] BigQuery access works.
- [ ] `INFORMATION_SCHEMA.TABLES` confirms all required derived tables.
- [ ] Old numbers are marked unvalidated.
- [ ] No row-level patient data in chat, docs, Git, or other shared artifacts.
- [ ] This preregistration file is committed **before** the AL run.
- [ ] Log Python executable/path to avoid PATH collisions.
- [ ] Log dependency versions, seeds, configs, and commit SHAs.

## G1 — Cohort and label

- [ ] Record a CONSORT-style count at every cohort filtering step.
- [ ] Flag any single step with >30% unexplained loss.
- [ ] ICD-10 filters use dot-free codes **and** `icd_version`.
- [ ] Verify each intended ICD filter returns >0 rows.
- [ ] Check diagnosis titles in `d_icd_diagnoses`.
- [ ] Apply ESRD, transplant, and RRT exclusions as specified.
- [ ] Inspect AKI-related events during hours 0–23 for exclusion.
- [ ] Do **not** exclude index admissions accidentally.
- [ ] Patients lacking KDIGO data are **not** automatically labeled 0; distinguish “no AKI” from “no KDIGO evidence.”
- [ ] Define baseline creatinine explicitly and report the fraction covered by each definition.
- [ ] Report final AKI prevalence and compare with matched published cohorts.
- [ ] Produce an included-vs-excluded table.

## G2 — Feature integrity

For every final feature column:

- [ ] Report min, max, median, and % null.
- [ ] GCS total is in the expected 3–15 range.
- [ ] Bicarbonate comes from `mimiciv_derived.chemistry.bicarbonate`, not a blood-gas proxy.
- [ ] AST is the actual AST variable, not ALP.
- [ ] Blood pressure uses `COALESCE(sbp, sbp_ni)`.
- [ ] Do not create an arterial-line-present feature.
- [ ] Missing values remain NaN/NULL; never encode missing as 0.
- [ ] Nephrotoxin classes are fixed and exclude diuretics.
- [ ] Cumulative dose is in validated fixed units; otherwise remove it.
- [ ] Implement vancomycin AUC or remove every claim/reference to AUC.
- [ ] Creatinine slopes/trajectory features are computed from observed measurements **before** imputation.
- [ ] Reject suspicious near-zero slope artifacts (e.g. values around 1e-17) caused by broken logic.
- [ ] Weight may be used to normalize urine output/kg but is dropped from the predictive matrix afterward.
- [ ] Leakage checker passes with no post-hour-24 features.

## G3 — Matrix and splits

- [ ] Final row count equals final cohort count.
- [ ] Final column count equals the sum of preregistered feature-block widths.
- [ ] No all-NaN or constant columns remain.
- [ ] Temporal split uses `anchor_year_group`, not sorting directly on `intime`.
- [ ] No patient overlap across train/calibration/test.
- [ ] Fresh test set is stored and untouched during model/AL development.
- [ ] Persist split manifest, seeds, and frozen config.

## G4 — Baselines and model lock

Run at minimum:

- Logistic regression baseline.
- Full-feature LightGBM baseline.
- SOFA baseline.

Model rules:

- [ ] **No class_weight**.
- [ ] Hyperparameters tuned by cross-validation within the training data only.
- [ ] Apply post-hoc calibration after model fitting.
- [ ] Calibration slope should be approximately 1 and intercept approximately 0.
- [ ] Brier score must beat the no-skill reference.
- [ ] Calibration-vs-test AUROC should be within ~0.03.
- [ ] AUROC >0.90 triggers a formal leakage audit.
- [ ] An AUROC around 0.70 while barely beating logistic regression is a debugging signal, not a success criterion.
- [ ] Write down the base-paper AUPRC used for task-matched benchmarking.

## G5 — Contribution-killer experiments

Before attaching any method to the headline:

### SHAP compression
- [ ] Compare the SHAP mask with the upper tail of ≥10 random feature subsets.
- [ ] Include gain-based importance as a second comparator.
- [ ] Cross-fit SHAP feature selection inside training folds only.
- [ ] Freeze the selected mask before evaluating compressed AL.

### Nephrotoxin trajectory contribution
- [ ] Primary comparison: time-series/trajectory features vs binary exposure flags.
- [ ] Run the preregistered 6-arm feature ablation table.

### Missingness
Use the corrected three-arm design:

- **A0:** original missingness behavior.
- **A1:** mask missingness explicitly.
- **A2:** remove missingness signal as far as the implementation permits.

- [ ] Quantify the care-process/missingness contribution rather than treating the mask-free arm as automatically fair.

## G6 — BADGE correctness

- [ ] Embedding uses the model’s hard predicted label in the gradient construction.
- [ ] Core selection uses genuine k-means++ / D² seeding, not full k-means followed by nearest-centroid assignment.
- [ ] Verify that BADGE selects a wider probability spread than random.
- [ ] If exact BADGE cannot be defended, rename the method as **BADGE-inspired** rather than BADGE.

## G7 — Active-learning gate

### Experimental setup

- [ ] Use the calibration split for AL selection; test remains untouched.
- [ ] Freeze the SHAP mask before AL.
- [ ] Use the same initial seed patients for all sampling arms within each seed.
- [ ] Use **10 paired seeds** for the primary gate.
- [ ] Arms:
  - Random sampling.
  - Stratified BADGE.
  - Uncertainty sampling.
- [ ] Start with **500 labeled** seed patients.
- [ ] Add **100 labels per iteration**.
- [ ] Continue to at most **2,500 labels**.
- [ ] Record learning curves for every seed and arm.

### Pre-gate saturation check

- [ ] First run a random-only learning curve on clean data.
- [ ] Confirm that 600–1,500 labels is not already saturated.
- [ ] Freeze the gate window W after this check.

### Primary statistic

For each seed, compute the average performance difference over the frozen window W:

**Δ_seed = mean(performance_BADGE(W) − performance_random(W))**

Across the 10 paired seeds:

- **SE = SD(Δ_seed) / sqrt(10)**
- **95% CI = mean(Δ) ± 2.262 × SE**
- Use the paired seed-level differences; do **not** confuse SD with SE.

### Decision rule

**PASS**
- Lower bound of the 95% CI > 0, **and**
- Mean Δ ≥ **0.01**.

**FAIL**
- Any result that does not meet PASS is not a headline active-learning win.
- Under Locked Decision #2, do **not** rebuild the old Gate-1 pipeline.
- If the CI excludes 0 but mean Δ <0.01 → FAIL headline.
- If CI includes 0 but mean Δ ≥0.01 → run 20 additional paired seeds before final classification.

### Diagnostic rule

If a diagnostic arm beats random but BADGE itself does not, investigate the BADGE implementation/selection logic before interpreting the AL result as a method failure.

## G8 — eICU external validation

Run in parallel with the MIMIC rebuild.

- [ ] Map identifiers and multiple ICU stays correctly for eICU.
- [ ] Respect 2014–2015 multi-hospital structure and site heterogeneity.
- [ ] Unavailable features remain NaN; never zero-fill them.
- [ ] Validate urine-output translation; if necessary, use and disclose a creatinine-only KDIGO fallback.
- [ ] Report AUROC.
- [ ] Report AUPRC together with prevalence.
- [ ] Report AUPRC lift over prevalence.
- [ ] Report per-hospital AUROC with hospital sample size.
- [ ] Report zero-shot transfer.
- [ ] Report recalibrated transfer.
- [ ] If prevalence is wildly different from MIMIC, investigate label construction before attributing differences to domain shift.

## G9 — Evaluation and reporting

- [ ] Decision-curve analysis (DCA).
- [ ] Alert burden / alerts per patient-time at the selected operating point.
- [ ] Subgroup analysis.
- [ ] Fairness analysis where appropriate and supportable.
- [ ] Sensitivity analyses.
- [ ] TRIPOD+AI reporting checklist.
- [ ] Test set is touched exactly once for the final held-out evaluation.
- [ ] If AUROC exceeds 0.90, include a leakage audit in the final report.

## G10 — Final consistency and release

Before writing or presenting any claim:

- [ ] Every number in the manuscript/slides points to a reproducible run.
- [ ] The task is described as **24-hour observation → 48-hour future AKI prediction**.
- [ ] Do not describe the study as providing a “12-hour warning” or other intervention window unless a separate analysis actually establishes that claim.
- [ ] SHAP hour-of-day patterns are interpretive only; they are not automatically intervention recommendations.
- [ ] Delete unsupported “mask-freezing” claims unless the experiment demonstrates them.
- [ ] Source or remove epidemiology claims.
- [ ] Merge the intended research branch into the chosen release branch.
- [ ] Pin dependencies.
- [ ] Log seeds.
- [ ] Attach the exact config to every reported result.
- [ ] Keep patient-level data and protected healthcare-derived artifacts outside Git.

## Rerun matrix

| Change | Re-run |
|---|---|
| Cohort/label or baseline-creatinine definition | Everything, including eICU comparison |
| Feature specification | Feature matrix, baselines, SHAP mask, G5, AL |
| Split or seeds | All models and all paired experiments |
| SHAP mask recomputed | Compression, compressed AL, eICU transfer |
| BADGE implementation | AL gate only |
| Hyperparameters/model settings | Every affected model result in every arm |
| eICU mapping | eICU only |

## Kill experiments first

Before attaching anything to the paper headline, run the three contribution-killers:

1. **SHAP vs random-k feature compression**
2. **Nephrotoxin trajectory vs binary exposure**
3. **Missingness A0/A1/A2**

The active-learning gate is then run once on the clean, frozen feature pipeline under G7.

## Decision tree

`Random-only curve saturated in W?`
- YES → choose a new unsaturated W and freeze it before AL.
- NO → run the preregistered AL gate.

`BADGE passes G7?`
- YES → retain AL as a headline contribution and complete supporting analyses.
- NO → do not sell AL as a positive headline result; retain the baseline/feature findings and report the negative AL result if scientifically useful.

`BADGE diagnostic arm beats random, but BADGE fails?`
- Audit BADGE implementation and rerun G7 after the implementation fix.

## Explicit deviation from the original protocol

The original protocol called for an earlier Gate-1 experiment before the main AL gate. Because the historical data/mask artifacts are unavailable and rebuilding the old buggy pipeline would create a large, low-value reproduction burden, this rebuild **skips the old Gate-1 run** and proceeds directly to the clean-feature AL gate. This deviation must remain visible in the preregistration and final paper methods.
