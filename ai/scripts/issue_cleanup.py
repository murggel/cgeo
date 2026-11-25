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
- index (command line): writes ai/issues/cleanup.md, an overview of all
  cleanup reports, and ai/issues/cleanup-compare.md, Copilot and Claude side
  by side for the issues both have checked. The reports themselves are in the request folders,
  ai/requests/cleanup/<name>/report.md and report-2.md, ... for further batches.

The result block is AI output and therefore untrusted: only lines of the form
``#<number> <category>`` for issues that the run actually checked are used.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


ISSUES_FILE = "issues.md"
STATE_FILE = "cleanup.json"
INDEX_FILE = "cleanup.md"
COMPARE_FILE = "cleanup-compare.md"
REPORT_FILE = re.compile(r"^report(?:-([2-9]|[1-9][0-9]))?\.md$")
UPSTREAM_ISSUES = "https://github.com/cgeo/cgeo/issues/"
PROVIDER = re.compile(r"\| provider: (claude|copilot)\b")
# Categories that mean "can probably be closed", in the order of the index columns.
CLOSABLE = ("fixed", "duplicate", "obsolete", "waiting")
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
           labels: list[str], today: date, skip_days: int = SKIP_DAYS) -> list[int]:
    """Pick the issues to check: longest inactive first, recently checked ones skipped."""
    wanted = {label.lower() for label in labels}
    candidates = []
    for entry in parse_entries(directory):
        if wanted and not wanted & {label.lower() for label in entry["labels"]}:
            continue
        checked = state.get(str(entry["number"]))
        updated = entry.get("updated", "")
        if checked:
            recent = checked["date"] >= (today - timedelta(days=skip_days)).isoformat()
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


def report_paths(requests_dir: Path) -> list[tuple[str, int, Path]]:
    """All cleanup reports as (request name, batch, path), newest first."""
    reports = []
    if not requests_dir.is_dir() or requests_dir.is_symlink():
        return reports
    for folder in requests_dir.iterdir():
        if folder.is_symlink() or not folder.is_dir():
            continue
        for path in folder.iterdir():
            match = REPORT_FILE.match(path.name)
            if match and path.is_file() and not path.is_symlink():
                reports.append((folder.name, int(match.group(1) or 1), path))
    reports.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return reports


CLOSABLE_HEADINGS = {
    "fixed": "Probably fixed",
    "duplicate": "Duplicates",
    "obsolete": "No longer applicable",
    "waiting": "Waiting for information",
}
MARKDOWN_SPECIAL = re.compile(r"([\\`*_\[\]<>|#])")
MAX_TITLE = 100


def _plain(text: str) -> str:
    """Untrusted text as plain Markdown: one line, special characters escaped, shortened."""
    text = " ".join(text.split())
    if len(text) > MAX_TITLE:
        text = text[:MAX_TITLE - 1].rstrip() + "…"
    return MARKDOWN_SPECIAL.sub(r"\\\1", text)


def read_reports(requests_dir: Path, index_dir: Path) -> list[dict[str, Any]]:
    """All cleanup reports, newest first: title, link, provider and results (None: no block)."""
    reports = []
    for name, batch, path in report_paths(requests_dir):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        provider = PROVIDER.search(text.split("\n", 1)[0])
        block = RESULT_BLOCK.search(text)
        results: dict[int, str] | None = None
        if block:
            results = {}
            for line in block.group(1).splitlines():
                result = RESULT_LINE.match(line.strip())
                if result:
                    results[int(result.group(1))] = result.group(2)
        reports.append({
            "title": name if batch == 1 else f"{name} ({batch})",
            "link": Path(os.path.relpath(path, index_dir)).as_posix(),
            "provider": provider.group(1) if provider else "?",
            "results": results,
        })
    return reports


def _snapshot(snapshot_dir: Path | None) -> tuple[dict[int, dict[str, Any]] | None, str]:
    """Open issues of the snapshot by number and the snapshot date; None if there is none."""
    if snapshot_dir is None:
        return None, ""
    try:
        entries = {entry["number"]: entry for entry in parse_entries(snapshot_dir)}
    except CleanupError:
        return None, ""
    try:
        created = json.loads((snapshot_dir / "snapshot.json").read_text(encoding="utf-8")).get("created_at", "")
    except (OSError, ValueError, AttributeError):
        created = ""
    return entries, str(created)[:10]


def _anchor(heading: str) -> str:
    """The anchor GitHub gives a heading: lower case, punctuation removed, spaces as hyphens."""
    return re.sub(r"[^a-z0-9 _-]", "", heading.lower()).replace(" ", "-")


def table_of_contents(lines: list[str]) -> list[str]:
    """Links to the ## and ### headings of the overview."""
    toc = ["## Contents", ""]
    for line in lines:
        level, _, heading = line.partition(" ")
        if level in ("##", "###"):
            indent = "  " if level == "###" else ""
            toc.append(f"{indent}- [{heading}](#{_anchor(heading)})")
    return toc + [""]


PROVIDER_NAMES = (("copilot", "Copilot"), ("claude", "Claude"))


def latest_results(reports: list[dict[str, Any]]) -> dict[int, dict[str, tuple[str, dict[str, Any]]]]:
    """{number: {provider: (category, report)}}: the latest result of each provider per issue."""
    latest: dict[int, dict[str, tuple[str, dict[str, Any]]]] = {}
    for report in reports:  # newest first
        for number, category in (report["results"] or {}).items():
            latest.setdefault(number, {}).setdefault(report["provider"], (category, report))
    return latest


def _result_cell(results: dict[str, tuple[str, dict[str, Any]]], provider: str) -> str:
    if provider not in results:
        return "–"
    category, report = results[provider]
    return f"[{category}]({report['link']})"


def _title(entries: dict[int, dict[str, Any]] | None, number: int) -> str:
    return (_plain(str(entries.get(number, {}).get("title", ""))) if entries else "") or "–"


def _issue_rows(numbers: list[int], latest: dict[int, dict[str, tuple[str, dict[str, Any]]]],
                entries: dict[int, dict[str, Any]] | None) -> list[str]:
    lines = ["| Issue | Title | " + " | ".join(name for _, name in PROVIDER_NAMES) + " |",
             "|---|---|" + "---|" * len(PROVIDER_NAMES)]
    for number in numbers:
        cells = [_result_cell(latest[number], key) for key, _ in PROVIDER_NAMES]
        lines.append(f"| [#{number}]({UPSTREAM_ISSUES}{number}) | {_title(entries, number)} | "
                     + " | ".join(cells) + " |")
    return lines


def status_lines(reports: list[dict[str, Any]], snapshot_dir: Path | None) -> list[str]:
    """The issues that can probably be closed, by category, from the latest result per provider."""
    latest = latest_results(reports)
    entries, created = _snapshot(snapshot_dir)
    # The category of an issue: the newest result that can close it (reports are newest first).
    category_of: dict[int, str] = {}
    for report in reports:
        for number, category in (report["results"] or {}).items():
            if category in CLOSABLE and number not in category_of \
                    and latest[number].get(report["provider"], ("",))[0] == category:
                category_of[number] = category
    closed = sorted(number for number in category_of if entries is not None and number not in entries)
    lines = [
        "## Issues that can probably be closed",
        "",
        "Issues whose latest result of at least one provider says they can be closed, by category;",
        "a later run of the same provider that keeps an issue open removes it here. The columns show",
        "the latest result of each provider with a link to its report.",
    ]
    if closed:
        lines += ["", f"Left out: {len(closed)} issues that are no longer open in the issue snapshot"
                  f"{' of ' + created if created else ''}."]
    for key in CLOSABLE:
        rows = sorted(number for number, category in category_of.items()
                      if category == key and number not in closed)
        lines += ["", f"### {CLOSABLE_HEADINGS[key]} ({len(rows)})", ""]
        lines += _issue_rows(rows, latest, entries) if rows else ["None."]
    return lines


def compare_markdown(requests_dir: Path, index_dir: Path, snapshot_dir: Path | None = None) -> str:
    """Copilot and Claude side by side for the issues both have checked."""
    reports = read_reports(requests_dir, index_dir)
    latest = latest_results(reports)
    entries, _ = _snapshot(snapshot_dir)
    both = sorted(number for number, results in latest.items()
                  if all(key in results for key, _ in PROVIDER_NAMES))
    same = [number for number in both if len({latest[number][key][0] for key, _ in PROVIDER_NAMES}) == 1]
    different = [number for number in both if number not in same]
    keys = list(CATEGORIES)
    body = [
        f"## Summary ({len(both)})",
        "",
        f"Issues checked by both: {len(both)}; same result: {len(same)}"
        + (f" ({round(100 * len(same) / len(both))} %)" if both else "")
        + f"; different result: {len(different)}.",
        "",
        "Number of issues per pair of results (rows: Copilot, columns: Claude):",
        "",
        "| Copilot \\ Claude | " + " | ".join(keys) + " |",
        "|---|" + "---|" * len(keys),
    ]
    for row in keys:
        counts = [sum(1 for number in both if latest[number]["copilot"][0] == row
                      and latest[number]["claude"][0] == column) for column in keys]
        body.append(f"| {row} | " + " | ".join(str(count) if count else "·" for count in counts) + " |")
    body += ["", f"## Different results ({len(different)})", ""]
    body += _issue_rows(different, latest, entries) if different else ["None."]
    body += ["", f"## Same result ({len(same)})", ""]
    body += _issue_rows(same, latest, entries) if same else ["None."]
    lines = [
        "# Issue cleanup: Copilot and Claude compared",
        "",
        "Written by the workflow together with [cleanup.md](cleanup.md); do not edit by hand. Only issues",
        "that both providers have checked, each with its latest result and a link to the report.",
        "",
    ]
    return "\n".join(lines + table_of_contents(body) + body) + "\n"


def index_markdown(requests_dir: Path, index_dir: Path, snapshot_dir: Path | None = None) -> str:
    """The overview: issues that can probably be closed, then all cleanup reports, newest first."""
    reports = read_reports(requests_dir, index_dir)
    lines = [
        "# Issue cleanup",
        "",
        "Written by the workflow after every cleanup run and issue snapshot; do not edit by hand. The",
        "reports are in the request folders `ai/requests/cleanup/<name>/` (`report.md`, further batches",
        "of the same night `report-2.md`, ...). The AI closes nothing: check each issue in its report",
        "before closing it.",
        "",
    ]
    body = status_lines(reports, snapshot_dir)
    body += [
        "",
        f"## Reports ({len(reports)})",
        "",
        "| Report | Provider | Checked | Fixed | Duplicates | Obsolete | Waiting | Can probably be closed |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for report in reports:
        row = [f"[{report['title']}]({report['link']})", report["provider"]]
        results = report["results"]
        if results is None:
            body.append("| " + " | ".join(row + ["–"] * 5 + ["no result block"]) + " |")
            continue
        row.append(str(len(results)))
        row += [str(sum(1 for category in results.values() if category == key)) for key in CLOSABLE]
        closable = [f"[#{number}]({UPSTREAM_ISSUES}{number}) {category}"
                    for number, category in results.items() if category in CLOSABLE]
        row.append(", ".join(closable) or "–")
        body.append("| " + " | ".join(row) + " |")
    return "\n".join(lines + table_of_contents(body) + body) + "\n"


def write_index(requests_dir: Path, index_path: Path, snapshot_dir: Path | None = None,
                compare_path: Path | None = None) -> str:
    """Write the overview (and the comparison) of all cleanup reports; return a one-line summary."""
    for path in (index_path, compare_path):
        if path is not None and path.is_symlink():
            raise CleanupError(f"{path} is a symbolic link")
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(index_markdown(requests_dir, index_path.parent, snapshot_dir), encoding="utf-8")
    summary = f"wrote {index_path} with {len(report_paths(requests_dir))} reports"
    if compare_path is not None:
        compare_path.parent.mkdir(parents=True, exist_ok=True)
        compare_path.write_text(compare_markdown(requests_dir, compare_path.parent, snapshot_dir),
                                encoding="utf-8")
        summary += f" and {compare_path}"
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
    index_parser = sub.add_parser("index", help="write the overview of all cleanup reports")
    index_parser.add_argument("--requests", type=Path, default=Path("ai/requests/cleanup"),
                              help="folder holding the cleanup requests and their reports")
    index_parser.add_argument("--index", type=Path,
                              default=Path("ai/issues") / INDEX_FILE)
    index_parser.add_argument("--compare", type=Path,
                              default=Path("ai/issues") / COMPARE_FILE)
    index_parser.add_argument("--issues", type=Path, default=Path("ai/issues"),
                              help="snapshot directory, for titles and to leave out closed issues")
    args = parser.parse_args(argv)

    if args.command == "index":
        try:
            print(write_index(args.requests, args.index, args.issues, args.compare))
        except (CleanupError, OSError) as exc:
            print(f"Cannot write the cleanup index: {exc}", file=sys.stderr)
            return 1
        return 0
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
