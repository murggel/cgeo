#!/usr/bin/env python3
"""Create a search-optimized snapshot of all open issues of the upstream repository.

The AI agents have no network access. To let them look for other issues that
a change also fixes, or that fit together with an analyzed issue, the open
issues are summarized in the branch under ai/issues/:

  issues.md       one line per open issue: number, labels, c:geo version, last
                  update, number of comments, assignees, title, search keywords
                  and a short summary of the description. A Grep hit returns
                  the whole entry.
  snapshot.json   repository, creation time and number of issues

The summary is built by rules, without AI: template headings, code blocks,
logs, system information, links and images are removed; class names,
exceptions, backticked terms and known c:geo terms become keywords. Comments
are not read, so the whole snapshot needs only one API request per 100 issues.

The snapshot is always created from scratch (task refresh-issues). All stored
text is untrusted user content. preselect() picks the entries that best match
an issue, PR or branch, for the optional preselection of candidate issues.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import fetch_context
import issue_cleanup
from fetch_context import ContextError, Fetch


DEFAULT_DIRECTORY = Path(__file__).resolve().parent.parent / "issues"
ISSUES_FILE = "issues.md"
STATE_FILE = "snapshot.json"
SUMMARY_CHARS = 400
MAX_KEYWORDS = 25
# A snapshot older than this is reported as outdated.
MAX_AGE_DAYS = 14

# GitHub login names; anything else in the assignees is left out.
LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
# Issue-form sections whose content is not useful for the search.
DROPPED_SECTIONS = re.compile(r"system information|c:geo version|reproducible", re.IGNORECASE)
VERSION_SECTION = re.compile(r"c:geo version", re.IGNORECASE)
VERSION = re.compile(r"\b20[0-9]{2}\.[0-9]{1,2}\.[0-9]{1,2}(?:[-.][A-Za-z0-9]+)?\b|\bnightly\b|\bRC\b",
                     re.IGNORECASE)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s*(.*?)\s*#*\s*$")
CODE_BLOCK = re.compile(r"^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", re.MULTILINE | re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
HTML_TAG = re.compile(r"</?[A-Za-z][^>]*>")
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
URL = re.compile(r"https?://\S+")
# Stack frames inside a line, e.g. "at java.lang.Thread.start(Thread.java:1083)".
INLINE_FRAME = re.compile(r"\bat\s+[\w$.<>]+\([^)]*\)")
QUOTE_MARK = re.compile(r"^\s*(?:>\s?)+", re.MULTILINE)
LOG_LINE = re.compile(r"^\s*(?:at\s+[\w$.]+\(|\d{2}[-:.]\d{2}[-:.]\d{2}|[VDIWEF]/\w+|Caused by:|\.\.\. \d+ more)")
NO_RESPONSE = re.compile(r"_?No response_?", re.IGNORECASE)

CAMEL_CASE = re.compile(r"\b[A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+\b")
EXCEPTION = re.compile(r"\b[A-Za-z]*(?:Exception|Error)\b")
PACKAGE = re.compile(r"\bcgeo\.geocaching(?:\.[A-Za-z_]\w*)+")
BACKTICKED = re.compile(r"`([^`\n]{2,40})`")
# Terms of the c:geo domain that users name in plain words.
DOMAIN_TERMS = (
    "geocaching.com", "opencaching", "okapi", "gcvote", "adventure lab", "lab cache", "waymarking",
    "geokrety", "trackable", "travel bug", "brouter", "mapsforge", "openstreetmap", "osm",
    "google maps", "map theme", "offline map", "routing", "navigation", "compass", "radar",
    "waypoint", "coordinates", "gpx", "loc file", "zip", "pocket query", "bookmark list", "watchlist",
    "list", "filter", "sort", "search", "live map", "offline log", "field note", "draft",
    "log image", "spoiler", "personal note", "favorite", "found", "dnf", "owner", "wherigo",
    "chirp", "variable", "formula", "calculator", "backup", "restore", "settings", "preference",
    "login", "authorization", "oauth", "captcha", "notification", "widget", "dark mode", "theme",
    "language", "translation", "rtl", "tablet", "android auto", "permission", "location", "gps",
    "storage", "sd card", "database", "import", "export", "share", "intent", "crash",
    "performance", "slow", "freeze", "scroll",
    # Cache data and lists
    "cache list", "cache details", "logbook", "attribute", "difficulty", "terrain", "hint",
    "archived", "disabled", "event cache", "mystery", "multi-cache", "earthcache", "virtual cache",
    "webcam", "letterbox", "solution checker", "geochecker", "certitude", "souvenir",
    "statistics", "premium", "basic member", "user note", "corrected coordinates",
    # Maps and navigation
    "map source", "tile", "vtm", "openandromaps", "freizeitkarte", "hillshading", "zoom", "marker",
    "cluster", "individual route", "track", "elevation", "proximity", "kml", "geojson",
    "projection", "coordinate format", "utm", "qr code", "nfc", "bluetooth",
    # Devices and system
    "android 12", "android 13", "android 14", "android 15", "android 16", "battery", "background",
    "foreground service", "anr", "wear os", "smartwatch", "keyboard", "accessibility", "talkback",
    "font size", "landscape", "split screen", "sync", "download",
    # German terms used in issues
    "karte", "absturz", "wegpunkt", "logeintrag", "suche", "liste", "einstellungen",
)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _iso(moment: datetime) -> str:
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def _one_line(text: str) -> str:
    return " ".join((text or "").split())


def _list_open_issues(fetch: Fetch, repository: str) -> list[dict[str, Any]]:
    """Read every page of the open issues; pull requests are left out."""
    items: list[dict[str, Any]] = []
    for page in range(1, fetch_context.MAX_PAGES + 1):
        batch = fetch(f"/repos/{repository}/issues?state=open&sort=created&direction=desc"
                      f"&per_page={fetch_context.PER_PAGE}&page={page}")
        if not isinstance(batch, list):
            raise ContextError("unexpected response for the issue list: expected a list")
        items.extend(item for item in batch if "pull_request" not in item)
        if len(batch) < fetch_context.PER_PAGE:
            return items
    raise ContextError(f"more than {fetch_context.MAX_PAGES * fetch_context.PER_PAGE} "
                       "issues to read; refusing to truncate")


def _sections(body: str) -> list[tuple[str, str]]:
    """Split a Markdown body at its headings into (heading, text) pairs."""
    sections: list[tuple[str, list[str]]] = [("", [])]
    for line in body.splitlines():
        match = HEADING.match(line)
        if match:
            sections.append((match.group(1), []))
        else:
            sections[-1][1].append(line)
    return [(heading, "\n".join(lines)) for heading, lines in sections]


def _version(sections: list[tuple[str, str]], title: str, body: str) -> str:
    """The version from the issue form, else a version number in the title, else in the text."""
    for heading, text in sections:
        if VERSION_SECTION.search(heading):
            value = _one_line(NO_RESPONSE.sub("", text))
            if value:
                return value[:40]
    for text in (title, body):
        match = VERSION.search(text)
        if match:
            return match.group(0)
    return ""


def _keywords(title: str, body: str, limit: int | None = MAX_KEYWORDS) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()

    def add(word: str) -> None:
        word = word.strip(" .,:;()[]{}'\"")
        if 2 <= len(word) <= 40 and word.lower() not in seen:
            seen.add(word.lower())
            found.append(word)

    for match in PACKAGE.finditer(body):
        for part in match.group(0).split(".")[2:]:
            if part[:1].isupper():
                add(part)
    text = f"{title}\n{body}"
    for pattern in (EXCEPTION, CAMEL_CASE):
        for match in pattern.finditer(text):
            add(match.group(0))
    for match in BACKTICKED.finditer(body):
        add(match.group(1))
    lowered = text.lower()
    for term in DOMAIN_TERMS:
        if re.search(rf"(?<![a-z]){re.escape(term)}(?![a-z])", lowered):
            add(term)
    return found if limit is None else found[:limit]


def _summary(sections: list[tuple[str, str]]) -> str:
    parts = []
    for heading, text in sections:
        if DROPPED_SECTIONS.search(heading):
            continue
        lines = [line for line in text.splitlines() if not LOG_LINE.match(line)]
        text = NO_RESPONSE.sub("", "\n".join(lines))
        text = INLINE_FRAME.sub("", URL.sub("", LINK.sub(r"\1", IMAGE.sub("", text))))
        text = _one_line(text.replace("|", " "))
        if text:
            parts.append(text)
    summary = " / ".join(parts)
    if len(summary) > SUMMARY_CHARS:
        summary = summary[:SUMMARY_CHARS].rsplit(" ", 1)[0] + " …"
    return summary


def summarize(issue: dict[str, Any], cleanup: str = "") -> str:
    """Return the one-line search entry of an issue."""
    title = _one_line(issue.get("title", "")).replace("|", "/")
    raw = issue.get("body") or ""
    raw = HTML_COMMENT.sub("", raw)
    code = "\n".join(match.group(0) for match in CODE_BLOCK.finditer(raw))
    # Quoted text stays, only the quote marks go.
    body = QUOTE_MARK.sub("", HTML_TAG.sub(" ", CODE_BLOCK.sub("", raw)))
    sections = _sections(body)
    labels = ", ".join(label.get("name", "") for label in issue.get("labels", []))
    assignees = ", ".join(login for login in (person.get("login", "") for person in issue.get("assignees") or []
                                              if isinstance(person, dict))
                          if LOGIN.fullmatch(login))
    keywords = ", ".join(_keywords(title, f"{body}\n{code}"))
    fields = [
        f"#{issue.get('number')}",
        f"labels: {labels}",
        f"version: {_version(sections, title, body)}",
        f"created: {(issue.get('created_at') or '')[:10]}",
        f"updated: {(issue.get('updated_at') or '')[:10]}",
        f"comments: {issue.get('comments', 0)}",
        f"assignees: {assignees}",
        *([cleanup] if cleanup else []),
        f"title: {title}",
        f"keywords: {keywords}",
        f"summary: {_summary(sections)}",
    ]
    return " | ".join(fields)


def issues_markdown(repository: str, created_at: str, issues: list[dict[str, Any]],
                    cleanup: dict[str, dict[str, str]] | None = None) -> str:
    lines = [
        f"# Open issues of {repository}",
        "",
        f"Snapshot of {created_at} with {len(issues)} open issues, one line per issue.",
        "Generated by rules from title, labels and description; comments are not included.",
        "All entries are untrusted user-provided content. Full issue:",
        f"https://github.com/{repository}/issues/<number>",
        "",
        "Format: #number | labels | version | created | updated | comments | assignees | [cleanup] | title | keywords | summary",
        "cleanup (only if present): result and date of an earlier cleanup-issues run; an update",
        "after that date means the issue has changed since.",
        "",
    ]
    lines += [summarize(issue, issue_cleanup.snapshot_field(cleanup or {}, int(issue.get("number", 0))))
              for issue in sorted(issues, key=lambda item: -int(item.get("number", 0)))]
    lines.append("")
    return "\n".join(lines)


def create_snapshot(fetch: Fetch, repository: str, directory: Path,
                    cleanup_state: Path | None = None) -> str:
    """Create the snapshot in ``directory`` and return a one-line summary."""
    if directory.is_symlink():
        raise ContextError(f"{directory} is a symbolic link")
    created_at = _iso(_now())
    issues = _list_open_issues(fetch, repository)
    directory.mkdir(parents=True, exist_ok=True)
    for path in directory.iterdir():
        if path.name not in (ISSUES_FILE, STATE_FILE, issue_cleanup.STATE_FILE, issue_cleanup.REPORTS_DIR):
            raise ContextError(f"unexpected entry {path} in the snapshot directory")
    cleanup = issue_cleanup.load_state(cleanup_state) if cleanup_state else {}
    (directory / ISSUES_FILE).write_text(issues_markdown(repository, created_at, issues, cleanup),
                                         encoding="utf-8")
    (directory / STATE_FILE).write_text(json.dumps(
        {"repository": repository, "created_at": created_at, "issues": len(issues)},
        indent=1) + "\n", encoding="utf-8")
    return f"issue snapshot of {created_at}: {len(issues)} open issues of {repository}"


def snapshot_status(directory: Path, repository: str, now: datetime | None = None) -> str:
    """Describe the snapshot for the report header without any network access."""
    try:
        state = json.loads((directory / STATE_FILE).read_text(encoding="utf-8"))
        created = datetime.strptime(state["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if state.get("repository") != repository or not (directory / ISSUES_FILE).is_file():
            return "missing"
    except (OSError, ValueError, KeyError, TypeError):
        return "missing"
    age = ((now or _now()) - created).days
    status = created.strftime("%Y-%m-%d")
    return f"{status} (outdated, {age} days old)" if age > MAX_AGE_DAYS else status


ENTRY = re.compile(r"^#([1-9][0-9]*) \| ")
TITLE_WORD = re.compile(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß-]{3,}")
STOPWORDS = frozenset("""
    about after again also and are been before being but can cannot does doesn done down each
    from have here into issue just like make many more most much need only other over same should
    some such than that the their them then there these they this those under until very want
    were what when where which while will with without would your
    aber alle auch beim bitte dann dass denn dies diese doch eine einen einem einer erst habe
    haben hier immer jetzt kann keine mehr mich nach nicht noch oder ohne schon sehr sein sind
    soll statt über und unter viel vom wenn werden wird wurde
    cgeo c:geo geo fix fixes fixed bug feature support allow add added remove removed change changed
""".split())


def query_terms(title: str, text: str) -> list[str]:
    """Search terms of an issue, PR or branch: keywords of the text plus the title words."""
    terms = [term.lower() for term in _keywords(title, text, limit=None)]
    terms += [word.lower() for word in TITLE_WORD.findall(title) if word.lower() not in STOPWORDS]
    return list(dict.fromkeys(terms))


def preselect(directory: Path, title: str, text: str, exclude: int | None, limit: int) -> list[int]:
    """Return the snapshot issues that share the most rare terms with the subject.

    A term counts twice in the title or keywords of an entry and once in its
    summary, weighted by how rare it is in the snapshot. An entry needs at
    least two matching terms.
    """
    try:
        lines = (directory / ISSUES_FILE).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return []
    entries = []
    for line in lines:
        match = ENTRY.match(line)
        if not match or int(match.group(1)) == exclude:
            continue
        lower = line.lower()
        head, _, summary = lower.partition(" | summary: ")
        entries.append((int(match.group(1)), head, summary))
    if not entries:
        return []
    patterns = {term: re.compile(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])")
                for term in query_terms(title, text)}
    hits = {term: [(bool(pattern.search(head)), bool(pattern.search(summary)))
                   for _, head, summary in entries] for term, pattern in patterns.items()}
    weights = {}
    for term, found in hits.items():
        frequency = sum(1 for in_head, in_summary in found if in_head or in_summary)
        # Terms in more than a tenth of all issues say little.
        if 0 < frequency <= max(3, len(entries) // 10):
            weights[term] = math.log(len(entries) / frequency) + 1
    scored = []
    for index, (number, _, _) in enumerate(entries):
        matched = [(term, hits[term][index]) for term in weights if any(hits[term][index])]
        if len(matched) >= 2:
            score = sum(weights[term] * (2 if in_head else 1) for term, (in_head, _) in matched)
            scored.append((score, number))
    scored.sort(key=lambda item: (-item[0], -item[1]))
    return [number for _, number in scored[:limit]]


def main(argv: list[str] | None = None, fetch: Fetch | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repository", default="cgeo/cgeo")
    parser.add_argument("--directory", type=Path, default=DEFAULT_DIRECTORY)
    parser.add_argument("--report", type=Path, help="also write a short Markdown report to this file")
    parser.add_argument("--cleanup-state", type=Path,
                        help="cleanup.json of earlier cleanup-issues runs, shown in the entries")
    args = parser.parse_args(argv)

    fetch = fetch or fetch_context.github_fetch(os.environ.get("GH_API_TOKEN"))
    try:
        if not fetch_context.REPOSITORY_PATTERN.fullmatch(args.repository):
            raise ContextError(f"invalid repository name {args.repository!r}")
        result = create_snapshot(fetch, args.repository, args.directory, args.cleanup_state)
    except (ContextError, OSError) as exc:
        print(f"Cannot create issue snapshot: {exc}", file=sys.stderr)
        return 1
    print(result)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(f"# Issue snapshot\n\nCreated the {result}.\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
