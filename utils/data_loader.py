"""Helpers for loading parametrized test data from the data/ directory."""

import csv
import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str) -> Any:
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def load_csv(filename: str) -> list[dict[str, str]]:
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
