#!/usr/bin/env python3
"""Merge trial CSV files into a simplified format.

This script collects all `list_*.csv` files and the `filler.csv` file from the
`trials` directory and writes a combined CSV called `combined_trials.csv` with
the columns `item_id`, `condition_id`, and `text`.

Usage:
    python scripts/merge_trials.py
"""

from __future__ import annotations

import csv
from pathlib import Path


def build_condition_id(row: dict[str, str]) -> str:
    """Construct the condition identifier following the App.vue logic."""

    return (
        f"{row['verb_condition']}"
        f"_{row['subject_condition']}"
        f"_{row['context_condition']}"
        f"_{row['predicate_condition']}"
    )


def row_to_output(row: dict[str, str]) -> tuple[str, str, str]:
    """Convert an experimental row into the simplified schema."""

    item_id = (
        f"{row['Item']}"
        f"_{row['verb_condition']}"
        f"_{row['subject_condition']}"
        f"_{row['context_condition']}"
        f"_{row['predicate_condition']}"
    )
    condition_id = build_condition_id(row)
    text = row['sentence']
    return item_id, condition_id, text


def row_to_filler(row: dict[str, str]) -> tuple[str, str, str]:
    """Convert a filler row into the simplified schema."""

    filler_condition = "filler"
    item_id = f"{row['Item']}_{filler_condition}"
    condition_id = filler_condition
    text = row['Sentence']
    return item_id, condition_id, text


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    """Load all rows from a CSV file into dictionaries."""

    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    trials_dir = repo_root / "trials"

    output_path = trials_dir / "combined_trials.csv"

    list_files = sorted(trials_dir.glob("list_*.csv"))
    filler_file = trials_dir / "filler.csv"

    merged_rows: list[tuple[str, str, str]] = []

    for csv_path in list_files:
        for row in load_csv_rows(csv_path):
            merged_rows.append(row_to_output(row))

    if filler_file.exists():
        for row in load_csv_rows(filler_file):
            merged_rows.append(row_to_filler(row))

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["item_id", "condition_id", "text"])
        writer.writerows(merged_rows)

    print(f"Wrote {len(merged_rows)} rows to {output_path}")


if __name__ == "__main__":
    main()


