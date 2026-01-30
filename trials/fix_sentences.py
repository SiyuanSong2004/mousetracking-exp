#!/usr/bin/env python3
"""Tidy filler sentences:

- lowercase only the first letter
- strip sentence-final punctuation (e.g., '.', '!', '?', ';', ':', '…')
- keep internal punctuation intact
"""

from __future__ import annotations

import csv
from pathlib import Path
import re

# Characters to remove only at sentence end (plus trailing quotes/spaces).
END_PUNCT_PATTERN = re.compile(r"""[\s"'”’]*[\.!?;:…]+[\s"'”’]*$""")


def main() -> None:
    trials_dir = Path(__file__).resolve().parent
    filler_path = trials_dir / "filler.csv"

    if not filler_path.exists():
        raise FileNotFoundError(f"Cannot find {filler_path}")

    with filler_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    if not fieldnames:
        raise ValueError("No headers found in filler.csv")

    for row in rows:
        original = row.get("Sentence", "").strip()

        # Remove only the ending punctuation (keep internal commas etc.).
        no_end_punct = END_PUNCT_PATTERN.sub("", original)

        # Lowercase just the first alphabetic character if present.
        if no_end_punct:
            first_char = no_end_punct[0].lower()
            row["Sentence"] = first_char + no_end_punct[1:]
        else:
            row["Sentence"] = ""

    with filler_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)



if __name__ == "__main__":
    main()
