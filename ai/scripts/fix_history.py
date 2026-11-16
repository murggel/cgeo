#!/usr/bin/env python3
"""Find the pull request that probably fixed each "fixed" issue of a cleanup report.

The AI of cleanup-issues cannot see the history of cgeo/cgeo. For each issue it
calls fixed, it names the code that shows the fix in a block

    ```fix-evidence
    #447 main/src/main/java/cgeo/geocaching/sorting/GeocacheSort.java TARGET_DISTANCE
    ```

(issue, file, a literal piece of that code). This script runs without AI on
the full upstream clone:

- ``git log --follow -S`` gives the commit that introduced that code,
- the GitHub API gives the pull request that contains this commit,
- the block is replaced by a section that lists the result per issue,
- placeholders ``[fix-pr #<n>]`` of older prompts are removed: the closing
  comments do not name the pull request, the maintainer checks it first,
- the entry of each issue that could be closed gets its assignees from the
  issue snapshot ("assigned: @login" or "unassigned").

The first commit with the code is not always the fix (code can be older than
the issue, or be reworked later), so the result is a hint for the maintainer.
A commit older than the issue is marked as probably not the fix. The report is AI output and therefore untrusted: file, search text
and issue numbers are checked, and git is called without a shell.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable

import fetch_context
import issue_cleanup
from fetch_context import ContextError, Fetch


EVIDENCE_BLOCK = re.compile(r"^[ \t]*```fix-evidence[ \t]*\n(.*?)^[ \t]*```[ \t]*\n?", re.MULTILINE | re.DOTALL)
EVIDENCE_LINE = re.compile(r"^#([1-9][0-9]{0,8})\s+(\S+)\s+(.+?)\s*$")
SQUASH_SUBJECT = re.compile(r"^(.*?)\s*\(#([1-9][0-9]{0,8})\)\s*$")
PLACEHOLDER = re.compile(r"[ \t]?\[fix-pr #([1-9][0-9]{0,8})\]")
LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
MIN_NEEDLE = 4
MAX_NEEDLE = 120
MAX_TITLE = 100
SECTION_TITLE = "## Pull requests of the probably fixed issues"
SECTION_INTRO = ("Found by rules in the history of the code named above (the first commit that added it). "
                 "A hint, not proof: check that the pull request really is the fix.")

Git = Callable[[list[str]], str]


class HistoryError(Exception):
    """Raised when the history of one issue's evidence cannot be read."""


@dataclass
class Evidence:
    number: int
    path: str
    needle: str


@dataclass
class Finding:
    evidence: Evidence
    note: str = ""          # why nothing usable was found
    sha: str = ""
    commit_date: str = ""
    pr: int | None = None
    pr_title: str = ""
    merged: str = ""
    older_than_issue: bool = False


def run_git(upstream: Path) -> Git:
    def git(args: list[str]) -> str:
        try:
            result = subprocess.run(["git", "-C", str(upstream), *args], check=True,
                                    capture_output=True, text=True, timeout=600)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise HistoryError(f"git {args[0]} failed") from exc
        return result.stdout.strip()
    return git


def parse_evidence(report: str, fixed: set[int]) -> list[Evidence]:
    """Return the valid evidence lines for issues the report calls fixed, one per issue."""
    match = EVIDENCE_BLOCK.search(report)
    if not match:
        return []
    found: dict[int, Evidence] = {}
    for line in match.group(1).splitlines():
        parsed = EVIDENCE_LINE.match(line.strip())
        if not parsed:
            continue
        number, path, needle = int(parsed.group(1)), parsed.group(2), parsed.group(3).strip("`")
        if number in fixed and number not in found:
            found[number] = Evidence(number, path, needle)
    return list(found.values())


def check_evidence(evidence: Evidence) -> str:
    """Return why the evidence cannot be used, or an empty string."""
    path = PurePosixPath(evidence.path)
    if path.is_absolute() or ".." in path.parts or evidence.path.startswith("-") or "\\" in evidence.path:
        return "invalid file name"
    if not MIN_NEEDLE <= len(evidence.needle) <= MAX_NEEDLE or any(ord(char) < 32 for char in evidence.needle):
        return f"search text must be {MIN_NEEDLE} to {MAX_NEEDLE} characters on one line"
    return ""


def find_commit(git: Git, evidence: Evidence) -> tuple[str, str, str]:
    """Return (sha, date, subject) of the first commit that added the search text to the file."""
    try:
        git(["cat-file", "-e", f"HEAD:{evidence.path}"])
    except HistoryError:
        raise HistoryError("file does not exist in the current code") from None
    # git grep -F exits with 1 if the text is not found.
    try:
        git(["grep", "--quiet", "--fixed-strings", "-e", evidence.needle, "HEAD", "--", evidence.path])
    except HistoryError:
        raise HistoryError("search text is not in the current file") from None
    # Without a rename limit, --follow also keeps track of files moved in large commits.
    log = git(["-c", "diff.renameLimit=0", "log", "--follow", "--format=%H %as %s",
               f"-S{evidence.needle}", "HEAD", "--", evidence.path])
    lines = [line.split(" ", 2) for line in log.splitlines() if line.strip()]
    if not lines:
        raise HistoryError("no commit adds the search text")
    # git log lists newest first; --reverse does not combine reliably with --follow.
    sha, commit_date, *subject = lines[-1]
    return sha, commit_date, subject[0] if subject else ""


def find_pull_request(fetch: Fetch, repository: str, sha: str) -> tuple[int, str, str] | None:
    """Return (number, title, merge date) of the earliest merged PR containing the commit."""
    pulls = fetch(f"/repos/{repository}/commits/{sha}/pulls")
    if not isinstance(pulls, list):
        raise ContextError("unexpected response for the pull requests of a commit")
    merged = [pull for pull in pulls if isinstance(pull, dict) and pull.get("merged_at")
              and isinstance(pull.get("number"), int)]
    if not merged:
        return None
    pull = min(merged, key=lambda item: item["merged_at"])
    return pull["number"], str(pull.get("title") or ""), pull["merged_at"][:10]


def investigate(evidence: Evidence, git: Git, fetch: Fetch, repository: str, created: dict[int, str]) -> Finding:
    finding = Finding(evidence)
    finding.note = check_evidence(evidence)
    if finding.note:
        return finding
    try:
        finding.sha, finding.commit_date, subject = find_commit(git, evidence)
    except HistoryError as exc:
        finding.note = str(exc)
        return finding
    issue_created = created.get(evidence.number, "")
    finding.older_than_issue = bool(issue_created) and finding.commit_date < issue_created
    try:
        pull = find_pull_request(fetch, repository, finding.sha)
    except ContextError:
        pull = None
        print(f"::warning::Cannot look up the pull request of commit {finding.sha[:10]} for #{evidence.number}.")
    if pull:
        finding.pr, finding.pr_title, finding.merged = pull
    else:
        # GitHub ends the subject of a squash merge with the PR number, e.g. "... (#11937)".
        squash = SQUASH_SUBJECT.match(subject)
        if squash:
            finding.pr, finding.pr_title = int(squash.group(2)), squash.group(1)
    return finding


def plain(text: str) -> str:
    """One line of untrusted text, safe inside Markdown."""
    text = " ".join(text.split())[:MAX_TITLE]
    return re.sub(r"([\\`*_\[\]<>|#])", r"\\\1", text)


def code(text: str) -> str:
    return "`" + text.replace("`", "'") + "`"


def render_line(finding: Finding, repository: str) -> str:
    evidence = finding.evidence
    issue = f"[#{evidence.number}](https://github.com/{repository}/issues/{evidence.number})"
    where = f"{code(evidence.needle)} in {code(evidence.path)}"
    if finding.note:
        return f"- {issue}: nothing found for {where} ({finding.note})."
    commit = f"commit [{finding.sha[:10]}](https://github.com/{repository}/commit/{finding.sha}) of {finding.commit_date}"
    if finding.pr:
        merged = f", merged {finding.merged}" if finding.merged else ""
        change = (f"[PR #{finding.pr}](https://github.com/{repository}/pull/{finding.pr}) "
                  f"\"{plain(finding.pr_title)}\"{merged}, {commit}")
    else:
        change = f"{commit} (no pull request)"
    line = f"- {issue}: {change}, added {where}."
    if finding.older_than_issue:
        line += " The code is older than the issue, so this is probably not the fix."
    return line


def render_section(findings: list[Finding], repository: str) -> str:
    if not findings:
        return ""
    lines = [SECTION_TITLE, "", SECTION_INTRO, ""] + [render_line(item, repository) for item in findings]
    return "\n".join(lines) + "\n"


def link_fixes(report: str, git: Git, fetch: Fetch, repository: str, created: dict[int, str],
               checked: set[int]) -> tuple[str, list[Finding]]:
    """Return the report with the evidence block replaced and placeholders removed."""
    try:
        results = issue_cleanup.parse_results(report, checked)
    except issue_cleanup.CleanupError:
        results = {}
    fixed = {number for number, category in results.items() if category == "fixed"}
    findings = [investigate(item, git, fetch, repository, created) for item in parse_evidence(report, fixed)]
    section = render_section(findings, repository)
    # A function as replacement, so that untrusted text is never read as a regex template.
    report = EVIDENCE_BLOCK.sub(lambda _: section, report, count=1)
    report = EVIDENCE_BLOCK.sub("", report)
    report = PLACEHOLDER.sub("", report)
    return re.sub(r"\n{3,}", "\n\n", report), findings


def entry_line(number: int, repository: str) -> re.Pattern[str]:
    """The list entry of an issue in a category section: "- [#447](.../issues/447) title"."""
    link = re.escape(f"[#{number}](https://github.com/{repository}/issues/{number})")
    return re.compile(rf"^([ \t]*[-*][ \t]+(?:\*\*)?{link}.*?)[ \t]*$", re.MULTILINE)


def add_assignees(report: str, repository: str, assignees: dict[int, list[str]], checked: set[int]) -> str:
    """Name the assignees of each issue that could be closed, at the end of its entry line.

    Only issues of the result block with a category other than keep-open, and
    only those whose snapshot entry has the assignees field.
    """
    try:
        results = issue_cleanup.parse_results(report, checked)
    except issue_cleanup.CleanupError:
        return report
    for number, category in sorted(results.items()):
        if category == "keep-open" or number not in assignees:
            continue
        logins = assignees[number]
        note = "assigned: " + ", ".join(f"@{login}" for login in logins) if logins else "unassigned"
        report = entry_line(number, repository).sub(lambda match: f"{match.group(1)} — {note}", report, count=1)
    return report


def snapshot_entries(snapshot_dir: Path) -> list[dict]:
    try:
        return issue_cleanup.parse_entries(snapshot_dir)
    except issue_cleanup.CleanupError:
        return []


def created_dates(entries: list[dict]) -> dict[int, str]:
    return {entry["number"]: entry.get("created", "") for entry in entries}


def assignee_logins(entries: list[dict]) -> dict[int, list[str]]:
    """Assignees per issue; issues of an older snapshot without the field are left out."""
    return {entry["number"]: [login for login in (part.strip() for part in entry["assignees"].split(","))
                              if LOGIN.fullmatch(login)]
            for entry in entries if "assignees" in entry}


def main(argv: list[str] | None = None, fetch: Fetch | None = None, git: Git | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--report", type=Path, required=True, help="cleanup report, changed in place")
    parser.add_argument("--upstream", type=Path, required=True, help="clone of the repository with full history")
    parser.add_argument("--repository", default="cgeo/cgeo")
    parser.add_argument("--issues", type=Path, default=Path("ai/issues"), help="snapshot directory")
    parser.add_argument("--checked", required=True, help="comma-separated numbers of the checked issues")
    args = parser.parse_args(argv)

    if not fetch_context.REPOSITORY_PATTERN.fullmatch(args.repository):
        print(f"Invalid repository name {args.repository!r}", file=sys.stderr)
        return 1
    try:
        report = args.report.read_text(encoding="utf-8")
        checked = {int(part) for part in args.checked.split(",") if part}
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Cannot read the cleanup report: {exc}", file=sys.stderr)
        return 1
    fetch = fetch or fetch_context.github_fetch(os.environ.get("GH_API_TOKEN"))
    git = git or run_git(args.upstream)
    entries = snapshot_entries(args.issues)
    # Before link_fixes, whose section of pull requests also lists the fixed issues.
    report = add_assignees(report, args.repository, assignee_logins(entries), checked)
    report, findings = link_fixes(report, git, fetch, args.repository, created_dates(entries), checked)
    args.report.write_text(report, encoding="utf-8")
    found = sum(1 for item in findings if item.pr)
    print(f"{args.report.name}: {len(findings)} fixed issues with evidence, {found} with a pull request.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
