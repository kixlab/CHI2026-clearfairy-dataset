"""Helpers for loading the ClearFairy Cognitive Decision Steps dataset.

Usage:
    from scripts.load import load_dataset, load_participant

    steps = load_dataset()                 # all 417 steps as a flat list
    p01   = load_participant("P01")        # one participant's steps
    lab   = load_dataset(task="lab_website")
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

# Resolve the data directory relative to this file so the helper works
# regardless of the caller's current working directory.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _REPO_ROOT / "data" / "decision_steps"

VALID_TASKS = {"lab_website", "shopping_site"}


def _iter_files() -> Iterable[Path]:
    return sorted(_DATA_DIR.glob("P*.json"))


def load_participant(participant_id: str) -> list[dict]:
    """Load all decision steps for a single participant (e.g. "P01")."""
    path = _DATA_DIR / f"{participant_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"No data file for participant {participant_id!r}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_dataset(task: str | None = None) -> list[dict]:
    """Load all decision steps as a single flat list.

    Args:
        task: Optional task filter. One of "lab_website" or "shopping_site".
    """
    if task is not None and task not in VALID_TASKS:
        raise ValueError(f"task must be one of {sorted(VALID_TASKS)} or None")

    steps: list[dict] = []
    for path in _iter_files():
        steps.extend(json.loads(path.read_text(encoding="utf-8")))

    if task is not None:
        steps = [s for s in steps if s["task_type"] == task]
    return steps


if __name__ == "__main__":
    all_steps = load_dataset()
    n_participants = len({s["participant_id"] for s in all_steps})
    print(f"{len(all_steps)} steps from {n_participants} participants")
    for task in sorted(VALID_TASKS):
        subset = load_dataset(task=task)
        n = len({s["participant_id"] for s in subset})
        print(f"  {task}: {len(subset)} steps from {n} participants")
