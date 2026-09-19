import csv
from pathlib import Path


def run(run_id: str) -> dict:
    file = Path(__file__).resolve().parents[2] / "sample_data" / "checks.csv"
    with file.open(newline="", encoding="utf-8") as source:
        matches = [row for row in csv.DictReader(source) if row["run_id"] == run_id]
    if not matches:
        raise ValueError("No checks found for this run")
    return {"run_id": run_id, "checks": matches, "failed": sum(row["status"] == "FAIL" for row in matches)}
