"""Validate every decision step file against data/schema.json.

Usage:
    python scripts/validate.py

Exits non-zero if any record fails validation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit(
        "jsonschema is required. Install it with:\n"
        "    pip install jsonschema"
    )

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "data" / "schema.json"
DATA_DIR = REPO_ROOT / "data" / "decision_steps"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    files = sorted(DATA_DIR.glob("P*.json"))
    if not files:
        print(f"No decision step files found in {DATA_DIR}", file=sys.stderr)
        return 1

    total_records = 0
    total_errors = 0

    for path in files:
        records = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            print(f"FAIL  {path.name}: top-level value is not a list", file=sys.stderr)
            total_errors += 1
            continue

        file_errors = 0
        prev_index = -1
        for i, record in enumerate(records):
            for err in validator.iter_errors(record):
                file_errors += 1
                loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
                print(
                    f"FAIL  {path.name}[{i}] {loc}: {err.message}",
                    file=sys.stderr,
                )
            # Cross-field consistency: step_index must be monotonically increasing from 0
            if isinstance(record, dict) and "step_index" in record:
                if record["step_index"] != prev_index + 1:
                    file_errors += 1
                    print(
                        f"FAIL  {path.name}[{i}]: step_index {record['step_index']} "
                        f"is not sequential (expected {prev_index + 1})",
                        file=sys.stderr,
                    )
                prev_index = record["step_index"]

        # Cross-field consistency: participant_id must match filename
        expected_pid = path.stem  # e.g. "P01"
        wrong_pid = [
            (i, r["participant_id"])
            for i, r in enumerate(records)
            if isinstance(r, dict) and r.get("participant_id") != expected_pid
        ]
        for i, pid in wrong_pid:
            file_errors += 1
            print(
                f"FAIL  {path.name}[{i}]: participant_id {pid!r} does not match filename",
                file=sys.stderr,
            )

        status = "OK  " if file_errors == 0 else "FAIL"
        print(f"{status}  {path.name}: {len(records)} records, {file_errors} errors")
        total_records += len(records)
        total_errors += file_errors

    print()
    print(f"Validated {len(files)} files / {total_records} records")
    if total_errors:
        print(f"FAILED with {total_errors} errors")
        return 1
    print("All records valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
