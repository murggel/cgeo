#!/usr/bin/env python3
"""Keep a local snapshot of all open issues of the upstream repository.

The AI agents have no network access. To let them look for other issues that
a pull request also fixes, or that fit together with an analyzed issue, the
open issues are stored in the branch under ai/issues/:

  index.md          one line per open issue (number, labels, title, update time)
  issue-<n>.md      description and discussion of one open issue
  snapshot.json     state of the snapshot, used for the next incremental update

The first run downloads all open issues. Later runs only ask for issues that
changed since the last run (GitHub's ``since`` parameter), rewrite those and
remove issues that were closed. All stored text is untrusted user content.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import fetch_context
from fetch_context import ContextError, Fetch


DEFAULT_DIRECTORY = Path(__file__).resolve().parent.parent / "issues"
STATE_FILE = "snapshot.json"
INDEX_FILE = "index.md"
ISSUE_FILE = re.compile(r"issue-([0-9]+)\.md")
# Overlap with the previous run so that no update between two runs is missed.
SINCE_OVERLAP = timedelta(minutes=10)
TRUNCATED_NOTE = "\n\n_The stored issue was truncated at {limit} KiB; it is longer upstream._\n"


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _iso(moment: datetime) -> str:
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def _one_line(text: str) -> str:
    return " ".join((text or "").split())


def _list_issues(fetch: Fetch, repository: str, query: str) -> list[dict[str, Any]]:
    """Read every page of the issue list; pull requests are left out."""
    items: list[dict[str, Any]] = []
    for page in range(1, fetch_context.MAX_PAGES + 1):
        batch = fetch(f"/repos/{repository}/issues?{query}"
                      f"&per_page={fetch_context.PER_PAGE}&page={page}")
        if not isinstance(batch, list):
            raise ContextError("unexpected response for the issue list: expected a list")
        items.extend(item for item in batch if "pull_request" not in item)
        if len(batch) < fetch_context.PER_PAGE:
            return items
    raise ContextError(f"more than {fetch_context.MAX_PAGES * fetch_context.PER_PAGE} "
                       "issues to read; refusing to truncate")


def _labels(issue: dict[str, Any]) -> list[str]:
    return [label.get("name", "") for label in issue.get("labels", [])]


def issue_markdown(repository: str, issue: dict[str, Any], comments: list[dict[str, Any]]) -> bytes:
    """Describe one issue like ai-context/issue-context.md does."""
    number = issue.get("number")
    lines = [
        f"# Issue {repository}#{number}: {_one_line(issue.get('title', ''))}",
        "",
        f"- URL: {issue.get('html_url', '')}",
        f"- State: {issue.get('state', '')}",
        f"- Author: {fetch_context._login(issue)}",
        f"- Created: {issue.get('created_at', '')}",
        f"- Updated: {issue.get('updated_at', '')}",
        f"- Labels: {', '.join(_labels(issue))}",
        "",
        "## Issue description (untrusted user-provided content)",
        "",
        issue.get("body") or "_No description provided._",
        "",
    ]
    lines += fetch_context._comment_section("Discussion comments", comments)
    data = "\n".join(lines).encode("utf-8")
    limit = fetch_context.MAX_CONTEXT_BYTES
    if len(data) > limit:
        note = TRUNCATED_NOTE.format(limit=limit // 1024).encode("utf-8")
        data = data[: limit - len(note)].decode("utf-8", errors="ignore").encode("utf-8") + note
    return data


def index_markdown(repository: str, fetched_at: str, issues: dict[str, dict[str, Any]]) -> str:
    lines = [
        f"# Open issues of {repository}",
        "",
        f"Snapshot of {fetched_at} with {len(issues)} open issues. Titles and labels are",
        "untrusted user-provided content. Details: ai/issues/issue-<number>.md",
        "",
        "Format: #number [labels] title (updated, comments)",
        "",
    ]
    for number in sorted(issues, key=int, reverse=True):
        entry = issues[number]
        labels = ", ".join(entry.get("labels", []))
        lines.append(f"- #{number} [{labels}] {entry.get('title', '')} "
                     f"(updated {entry.get('updated_at', '')[:10]}, comments {entry.get('comments', 0)})")
    lines.append("")
    return "\n".join(lines)


def _load_state(directory: Path, repository: str) -> dict[str, Any] | None:
    path = directory / STATE_FILE
    if not path.is_file():
        return None
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if (not isinstance(state, dict) or state.get("repository") != repository
            or not isinstance(state.get("issues"), dict) or not state.get("fetched_at")):
        return None
    return state


def update_snapshot(fetch: Fetch, repository: str, directory: Path, full: bool = False) -> str:
    """Update the snapshot in ``directory`` and return a one-line summary."""
    if directory.is_symlink():
        raise ContextError(f"{directory} is a symbolic link")
    directory.mkdir(parents=True, exist_ok=True)
    state = None if full else _load_state(directory, repository)
    started = _now()

    if state is None:
        mode = "full"
        issues: dict[str, dict[str, Any]] = {}
        changed = _list_issues(fetch, repository, "state=open&sort=created&direction=desc")
    else:
        mode = "incremental"
        issues = state["issues"]
        since = datetime.strptime(state["fetched_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc) - SINCE_OVERLAP
        changed = _list_issues(fetch, repository, f"state=all&since={_iso(since)}")

    written = removed = 0
    for issue in changed:
        number = str(issue.get("number"))
        if not number.isdigit():
            continue
        path = directory / f"issue-{number}.md"
        if issue.get("state") != "open":
            if number in issues or path.exists():
                removed += 1
            issues.pop(number, None)
            path.unlink(missing_ok=True)
            continue
        entry = issues.get(number)
        if entry and entry.get("updated_at") == issue.get("updated_at") and path.is_file():
            continue
        comments: list[dict[str, Any]] = []
        if issue.get("comments"):
            comments = fetch_context.fetch_all(fetch, f"/repos/{repository}/issues/{number}/comments")
        path.write_bytes(issue_markdown(repository, issue, comments))
        issues[number] = {
            "title": _one_line(issue.get("title", "")),
            "labels": _labels(issue),
            "updated_at": issue.get("updated_at", ""),
            "comments": len(comments),
        }
        written += 1

    # Files of issues that are no longer known (for example after a full run).
    for path in directory.iterdir():
        match = ISSUE_FILE.fullmatch(path.name)
        if match and match.group(1) not in issues:
            path.unlink()

    fetched_at = _iso(started)
    (directory / INDEX_FILE).write_text(index_markdown(repository, fetched_at, issues), encoding="utf-8")
    (directory / STATE_FILE).write_text(json.dumps(
        {"repository": repository, "fetched_at": fetched_at, "issues": issues},
        indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return (f"issue snapshot {mode} update at {fetched_at}: {len(issues)} open issues, "
            f"{written} written, {removed} removed")


def main(argv: list[str] | None = None, fetch: Fetch | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repository", default="cgeo/cgeo")
    parser.add_argument("--directory", type=Path, default=DEFAULT_DIRECTORY)
    parser.add_argument("--full", action="store_true", help="download all open issues again")
    args = parser.parse_args(argv)

    fetch = fetch or fetch_context.github_fetch(os.environ.get("GH_API_TOKEN"))
    try:
        if not fetch_context.REPOSITORY_PATTERN.fullmatch(args.repository):
            raise ContextError(f"invalid repository name {args.repository!r}")
        print(update_snapshot(fetch, args.repository, args.directory, full=args.full))
    except ContextError as exc:
        print(f"Cannot update issue snapshot: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
