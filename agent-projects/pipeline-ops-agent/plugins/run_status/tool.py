import csv
from pathlib import Path


def run(run_id: str) -> dict:
    file = Path(__file__).resolve().parents[2] / "sample_data" / "runs.csv"
    with file.open(newline="", encoding="utf-8") as source:
        matches = [row for row in csv.DictReader(source) if row["run_id"] == run_id]
    if len(matches) != 1:
        raise ValueError("Run ID not found or ambiguous")
    return matches[0]
