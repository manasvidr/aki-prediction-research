-- G0 metadata-only check. Do not SELECT patient rows here.
-- Replace PROJECT_ID with the authorized project containing MIMIC-IV.

SELECT
  table_schema,
  table_name
FROM `PROJECT_ID`.physionet-data.INFORMATION_SCHEMA.TABLES
WHERE table_schema IN ("mimiciv_derived", "mimiciv_hosp", "mimiciv_icu")
ORDER BY table_schema, table_name;
