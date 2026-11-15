#!/usr/bin/env python3
"""Issue cleanup: select candidates from the issue snapshot and record the results.

The task cleanup-issues lets the AI check open issues of the upstream
repository and recommend which ones can be closed. This module holds the
parts that run without AI:

- select(): picks the issues to check from ai/issues/issues.md, longest
  inactive first, optionally only issues with one of the given labels.
  Issues checked within the last SKIP_DAYS days are skipped unless they have
  had activity since.
- apply (command line): reads the machine-readable result block of a cleanup
  report and records category and date per issue in ai/issues/cleanup.json.
  The next snapshot shows these results in its entries.

The result block is AI output and therefore untrusted: only lines of the form
``#<number> <category>`` for issues that the run actually checked are used.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


ISSUES_FILE = "issues.md"
STATE_FILE = "cleanup.json"
REPORTS_DIR = "cleanup"
SKIP_DAYS = 183
DEFAULT_COUNT = 20
MAX_COUNT = 30
# Category keys of the result block and their wording in the snapshot.
CATEGORIES = {
    "fixed": "probably fixed",
    "duplicate": "duplicate",
    "obsolete": "no longer applicable",
    "waiting": "waiting for information",
    "keep-open": "keep open",
}
ENTRY = re.compile(r"^#([1-9][0-9]*) \| (.*)$")
FIELD = re.compile(r"^([a-z]+): ?(.*)$")
RESULT_BLOCK = re.compile(r"^```cleanup-result[ \t]*\n(.*?)^```", re.MULTILINE | re.DOTALL)
RESULT_LINE = re.compile(r"^#([1-9][0-9]{0,8})\s+(" + "|".join(map(re.escape, CATEGORIES)) + r")\s*$")


class CleanupError(Exception):
    """Raised when candidates cannot be selected or results cannot be recorded."""


def parse_entries(directory: Path) -> list[dict[str, Any]]:
    """Read the entries of issues.md as dicts with number, labels, created, updated, ..."""
    try:
        lines = (directory / ISSUES_FILE).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise CleanupError(f"cannot read the issue snapshot ({exc})") from exc
    entries = []
    for line in lines:
        match = ENTRY.match(line)
        if not match:
            continue
        entry: dict[str, Any] = {"number": int(match.group(1))}
        # The summary is the last field and may itself contain " | ".
        head, _, summary = match.group(2).partition(" | summary: ")
        for part in head.split(" | "):
            field = FIELD.match(part)
            if field:
                entry[field.group(1)] = field.group(2).strip()
        entry["summary"] = summary
        entry["labels"] = [label.strip() for label in entry.get("labels", "").split(",") if label.strip()]
        entries.append(entry)
    return entries


def load_state(path: Path) -> dict[str, dict[str, str]]:
    """Return {number: {"category": ..., "date": ...}}; an unreadable file counts as empty."""
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(state, dict):
        return {}
    return {number: value for number, value in state.items()
            if number.isdigit() and isinstance(value, dict)
            and value.get("category") in CATEGORIES and isinstance(value.get("date"), str)}


def select(directory: Path, state: dict[str, dict[str, str]], count: int,
           labels: list[str], today: date) -> list[int]:
    """Pick the issues to check: longest inactive first, recently checked ones skipped."""
    wanted = {label.lower() for label in labels}
    candidates = []
    for entry in parse_entries(directory):
        if wanted and not wanted & {label.lower() for label in entry["labels"]}:
            continue
        checked = state.get(str(entry["number"]))
        updated = entry.get("updated", "")
        if checked:
            recent = checked["date"] >= (today - timedelta(days=SKIP_DAYS)).isoformat()
            # Activity after the check makes the issue eligible again.
            if recent and updated <= checked["date"]:
                continue
        candidates.append((updated, entry.get("created", ""), entry["number"]))
    candidates.sort()
    return [number for _, _, number in candidates[:count]]


def parse_results(report: str, checked: set[int]) -> dict[int, str]:
    """Return {number: category} from the result block, limited to the checked issues."""
    match = RESULT_BLOCK.search(report)
    if not match:
        raise CleanupError("the report has no ```cleanup-result block")
    results: dict[int, str] = {}
    for line in match.group(1).splitlines():
        result = RESULT_LINE.match(line.strip())
        if result and int(result.group(1)) in checked:
            results[int(result.group(1))] = result.group(2)
    return results


def apply(report_path: Path, state_path: Path, snapshot_dir: Path, checked: set[int],
          today: date) -> str:
    """Record the results of a cleanup report and drop entries of closed issues."""
    try:
        report = report_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise CleanupError(f"cannot read the cleanup report ({exc})") from exc
    results = parse_results(report, checked)
    state = load_state(state_path)
    for number, category in results.items():
        state[str(number)] = {"category": category, "date": today.isoformat()}
    open_issues = {str(entry["number"]) for entry in parse_entries(snapshot_dir)}
    removed = [number for number in state if number not in open_issues and int(number) not in results]
    for number in removed:
        del state[number]
    state_path.write_text(json.dumps(dict(sorted(state.items(), key=lambda item: int(item[0]))),
                                     indent=1) + "\n", encoding="utf-8")
    missing = sorted(checked - set(results))
    summary = f"recorded {len(results)} of {len(checked)} checked issues, removed {len(removed)} closed"
    if missing:
        summary += "; no result for " + ", ".join(f"#{number}" for number in missing)
    return summary


def snapshot_field(state: dict[str, dict[str, str]], number: int) -> str:
    """The cleanup field of a snapshot entry, or an empty string."""
    entry = state.get(str(number))
    if not entry:
        return ""
    return f"cleanup: {CATEGORIES[entry['category']]} ({entry['date']})"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    apply_parser = sub.add_parser("apply", help="record the results of a cleanup report")
    apply_parser.add_argument("--report", type=Path, required=True)
    apply_parser.add_argument("--issues", type=Path, default=Path("ai/issues"),
                              help="snapshot directory holding issues.md and cleanup.json")
    apply_parser.add_argument("--checked", required=True,
                              help="comma-separated numbers of the issues the run checked")
    apply_parser.add_argument("--date", default="", help="date of the run (YYYY-MM-DD), default today")
    args = parser.parse_args(argv)

    try:
        checked = {int(part) for part in args.checked.split(",") if part}
        today = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
        print(apply(args.report, args.issues / STATE_FILE, args.issues, checked, today))
    except (CleanupError, ValueError, OSError) as exc:
        print(f"Cannot record cleanup results: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
