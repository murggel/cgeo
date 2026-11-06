#!/usr/bin/env python3
"""Fetch issue or pull-request context from the GitHub API for the AI workflow.

All fetched text is untrusted user content. Nothing is truncated silently:
lists are read page by page, and the script fails if the result would be
larger than MAX_CONTEXT_BYTES or a list has more than MAX_PAGES pages.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable


API_ROOT = "https://api.github.com"
MAX_CONTEXT_BYTES = 512 * 1024
PER_PAGE = 100
MAX_PAGES = 30
REPOSITORY_PATTERN = re.compile(r"[A-Za-z0-9-]+/[A-Za-z0-9_-][A-Za-z0-9_.-]*")

Fetch = Callable[[str], Any]


class ContextError(Exception):
    """Raised when the context cannot be fetched completely."""


def github_fetch(token: str | None) -> Fetch:
    """Return a function that GETs an API path and returns the decoded JSON."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "murggel-cgeo-ai-workflow",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    def fetch(path: str) -> Any:
        url = API_ROOT + path
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read(500).decode("utf-8", errors="replace")
            raise ContextError(f"GitHub API returned HTTP {exc.code} for {url}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            raise ContextError(f"GitHub API request failed for {url}: {exc}") from exc

    return fetch


def fetch_all(fetch: Fetch, path: str) -> list[dict[str, Any]]:
    """Read every page of a list endpoint."""
    items: list[dict[str, Any]] = []
    for page in range(1, MAX_PAGES + 1):
        batch = fetch(f"{path}?per_page={PER_PAGE}&page={page}")
        if not isinstance(batch, list):
            raise ContextError(f"unexpected response for {path}: expected a list")
        items.extend(batch)
        if len(batch) < PER_PAGE:
            return items
    raise ContextError(
        f"{path} has more than {MAX_PAGES * PER_PAGE} entries; refusing to truncate"
    )


def _login(item: dict[str, Any]) -> str:
    return (item.get("user") or {}).get("login") or "unknown"


def _comment_section(title: str, comments: list[dict[str, Any]]) -> list[str]:
    lines = [f"## {title} (untrusted user-provided content)", ""]
    for index, comment in enumerate(comments, start=1):
        lines += [
            f"### Comment {index} by {_login(comment)} ({comment.get('created_at', '')})",
            "",
            comment.get("body") or "_Empty comment._",
            "",
        ]
    if not comments:
        lines += ["_None._", ""]
    return lines


def issue_context(fetch: Fetch, repository: str, number: int, with_comments: bool) -> str:
    issue = fetch(f"/repos/{repository}/issues/{number}")
    if "pull_request" in issue:
        raise ContextError(f"{repository}#{number} is a pull request, not an issue")

    labels = ", ".join(label.get("name", "") for label in issue.get("labels", []))
    lines = [
        f"# Issue {repository}#{number}: {issue.get('title', '')}",
        "",
        f"- URL: {issue.get('html_url', '')}",
        f"- State: {issue.get('state', '')}",
        f"- Author: {_login(issue)}",
        f"- Created: {issue.get('created_at', '')}",
        f"- Updated: {issue.get('updated_at', '')}",
        f"- Labels: {labels}",
        "",
        "## Issue description (untrusted user-provided content)",
        "",
        issue.get("body") or "_No description provided._",
        "",
    ]
    if with_comments:
        comments = fetch_all(fetch, f"/repos/{repository}/issues/{number}/comments")
        lines += _comment_section("Discussion comments", comments)
    return "\n".join(lines)


def pr_context(fetch: Fetch, repository: str, number: int) -> str:
    root = f"/repos/{repository}/pulls/{number}"
    pr = fetch(root)
    files = fetch_all(fetch, f"{root}/files")
    reviews = fetch_all(fetch, f"{root}/reviews")
    inline_comments = fetch_all(fetch, f"{root}/comments")
    discussion = fetch_all(fetch, f"/repos/{repository}/issues/{number}/comments")

    base = pr.get("base") or {}
    head = pr.get("head") or {}
    lines = [
        f"# Pull request {repository}#{number}: {pr.get('title', '')}",
        "",
        f"- URL: {pr.get('html_url', '')}",
        f"- State: {pr.get('state', '')}",
        f"- Author: {_login(pr)}",
        f"- Base: {base.get('ref', '')} @ {base.get('sha', '')}",
        f"- Head: {head.get('sha', '')}",
        f"- Changed files: {len(files)}",
        "",
        "## Description (untrusted user-provided content)",
        "",
        pr.get("body") or "_No description provided._",
        "",
        "## Changed files and patches (untrusted user-provided content)",
        "",
    ]
    for changed in files:
        lines += [
            f"### {changed.get('filename', '')} ({changed.get('status', '')}, "
            f"+{changed.get('additions', 0)}/-{changed.get('deletions', 0)})",
            "",
            changed.get("patch")
            or "_GitHub provides no patch for this file (binary or too large); inspect it in pr-head/._",
            "",
        ]

    lines += ["## Reviews (untrusted user-provided content)", ""]
    for review in reviews:
        lines += [
            f"### Review by {_login(review)} ({review.get('state', '')}, {review.get('submitted_at', '')})",
            "",
            review.get("body") or "_No review text._",
            "",
        ]
    if not reviews:
        lines += ["_None._", ""]

    lines += ["## Inline review comments (untrusted user-provided content)", ""]
    for comment in inline_comments:
        line = comment.get("line") or comment.get("original_line") or "?"
        lines += [
            f"### {_login(comment)} on {comment.get('path', '')}:{line}",
            "",
            comment.get("body") or "_Empty comment._",
            "",
        ]
    if not inline_comments:
        lines += ["_None._", ""]

    lines += _comment_section("Discussion comments", discussion)
    return "\n".join(lines)


def bounded(text: str) -> bytes:
    data = text.encode("utf-8")
    if len(data) > MAX_CONTEXT_BYTES:
        raise ContextError(
            f"context is {len(data)} bytes and exceeds the {MAX_CONTEXT_BYTES // 1024} KiB limit"
        )
    return data


def main(argv: list[str] | None = None, fetch: Fetch | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("issue", "pr"))
    parser.add_argument("--repository", default="cgeo/cgeo")
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--no-comments", action="store_true", help="issue only: omit the discussion"
    )
    args = parser.parse_args(argv)

    fetch = fetch or github_fetch(os.environ.get("GH_API_TOKEN"))
    try:
        if not REPOSITORY_PATTERN.fullmatch(args.repository):
            raise ContextError(f"invalid repository name {args.repository!r}")
        if args.number < 1:
            raise ContextError("number must be positive")
        if args.kind == "issue":
            text = issue_context(fetch, args.repository, args.number, not args.no_comments)
        else:
            text = pr_context(fetch, args.repository, args.number)
        data = bounded(text)
    except ContextError as exc:
        print(f"Cannot fetch context: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(f"Wrote {len(data)} bytes of {args.kind} context for {args.repository}#{args.number}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
