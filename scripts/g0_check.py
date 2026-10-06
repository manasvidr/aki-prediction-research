"""G0 environment and MIMIC-IV access checks.

Run this locally in the clean research environment. It reports metadata only;
it never prints patient-level rows.
"""
import importlib
import os
import platform
import sys

REQUIRED_PACKAGES = ["pandas", "numpy", "scikit-learn", "lightgbm", "shap", "google-cloud-bigquery"]

def main():
    print("=== G0 environment ===")
    print("python_executable:", sys.executable)
    print("python_version:", platform.python_version())
    print("platform:", platform.platform())
    print("GCP project configured:", bool(os.getenv("AKI_GCP_PROJECT")))
    print("PhysioNet project:", os.getenv("AKI_PHYSIONET_PROJECT", "physionet-data"))
    print("\n=== package versions ===")
    for package in REQUIRED_PACKAGES:
        module = package.replace("-", "_")
        try:
            m = importlib.import_module(module)
            print(f"{package}: {getattr(m, "__version__", "installed; version unavailable")} ")
        except Exception as exc:
            print(f"{package}: IMPORT FAILED — {exc}")
    print("\n=== BigQuery ===")
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=os.getenv("AKI_GCP_PROJECT") or None)
        print("authenticated:", True)
        print("client_project:", client.project)
        print("BigQuery client creation: PASS")
    except Exception as exc:
        print("authenticated: UNKNOWN/FAILED")
        print("BigQuery client creation: FAIL")
        print(type(exc).__name__ + ":", exc)

if __name__ == "__main__":
    main()
