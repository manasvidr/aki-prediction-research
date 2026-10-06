"""Locked experiment configuration for the clean AKI rebuild.

Do not put credentials or patient-level data in this file.
Environment variables provide the BigQuery project identifiers.
"""

import os

# Data locations
DATA_DIR = os.getenv("AKI_DATA_DIR", "data")
RESULTS_DIR = os.getenv("AKI_RESULTS_DIR", "results")

# BigQuery
GCP_PROJECT = os.environ.get("AKI_GCP_PROJECT", "")
PHYSIONET_PROJECT = os.getenv("AKI_PHYSIONET_PROJECT", "physionet-data")

# Cohort — preregistered
MIN_AGE = 18
MIN_ICU_LOS_HOURS = 72
OBS_WINDOW_HOURS = 24
OUTCOME_WINDOW_HOURS = 48

# KDIGO — gate label is binary AKI
CREAT_RISE_48H = 0.3
CREAT_RISE_7D_FACTOR = 1.5
UO_OLIGURIC = 0.5

# Feature matrix
N_HOURS = 24

# Temporal split — must be implemented with anchor_year_group
TRAIN_FRAC = 0.60
CALIB_FRAC = 0.20
TEST_FRAC = 0.20

# SHAP mask
MASK_PERCENTILE = 85
JACCARD_THRESHOLD = 0.95
JACCARD_WINDOW = 3

# Active learning — preregistered
SEED_SIZE = 500
QUERY_SIZE = 100
MAX_LABELED = 2500
AL_SEEDS = 10
AL_MIN_LABELS = 600
AL_MAX_LABELS = 1500
AL_DELTA_THRESHOLD = 0.01
AL_EXTRA_SEEDS_IF_AMBIGUOUS = 20

# Reproducibility
RANDOM_SEED = 42

# Model policy
USE_CLASS_WEIGHT = False

# Hyperparameters are intentionally not locked here until G0 dependency
# resolution is completed. They must be tuned by CV inside train.
