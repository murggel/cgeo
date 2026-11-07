#!/usr/bin/env python3
"""Prepare the workspace for one AI task, independent of the provider.

analyze-issue: upstream/ checkout and ai-context/issue-context.md
review-pr:     upstream/ and pr-head/ checkouts and ai-context/pr-context.md
smoke-test:    optional issue description, appended to the report later

Symbolic links are removed from all checkouts: untrusted code could use
them to point the agent at files outside the workspace.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Callable

import fetch_context
from fetch_context import ContextError, Fetch


# Upper limit of agent turns per task (used by Claude).
MAX_TURNS = {"analyze-issue": 30, "review-pr": 30, "smoke-test": 2}

Git = Callable[[list[str]], str]


class PrepareError(Exception):
    """Raised when the workspace cannot be prepared."""


def run_git(args: list[str]) -> str:
    try:
        result = subprocess.run(["git", *args], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise PrepareError(f"git {' '.join(args)} failed: {exc.stderr.strip()}") from exc
    return result.stdout.strip()


def remove_symlinks(directory: Path) -> list[Path]:
    removed = []
    for root, dirs, files in os.walk(directory):
        for name in dirs + files:
            path = Path(root, name)
            if path.is_symlink():
                path.unlink()
                removed.append(path)
        dirs[:] = [name for name in dirs if Path(root, name).is_dir()]
    return removed


def write_bounded(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(fetch_context.bounded(text))


def clone_upstream(git: Git, repository: str, target: Path) -> str:
    git(["clone", "--quiet", "--depth", "1", "--branch", "master",
         f"https://github.com/{repository}.git", str(target)])
    return git(["-C", str(target), "rev-parse", "HEAD"])


def prepare(
    task: str,
    number: int | None,
    repository: str,
    workspace: Path,
    output_dir: Path,
    fetch: Fetch,
    git: Git = run_git,
) -> dict[str, str]:
    """Prepare the workspace and return the step outputs."""
    # git -C resolves relative paths against the -C directory, not the current one.
    workspace = workspace.absolute()
    upstream = workspace / "upstream"
    pr_head = workspace / "pr-head"
    context = workspace / "ai-context"
    appendix = ""

    if task in ("analyze-issue", "review-pr") and number is None:
        raise PrepareError(f"task '{task}' needs a number")

    if task == "analyze-issue":
        sha = clone_upstream(git, repository, upstream)
        write_bounded(context / "issue-context.md",
                      fetch_context.issue_context(fetch, repository, number, with_comments=True))
        header = f"task: analyze-issue | upstream: {repository}@{sha} | issue: #{number}"
    elif task == "review-pr":
        sha = clone_upstream(git, repository, upstream)
        git(["-C", str(upstream), "fetch", "--quiet", "--depth", "1", "origin",
             f"refs/pull/{number}/head"])
        git(["-C", str(upstream), "worktree", "add", "--quiet", "--detach", str(pr_head), "FETCH_HEAD"])
        head = git(["-C", str(pr_head), "rev-parse", "HEAD"])
        write_bounded(context / "pr-context.md", fetch_context.pr_context(fetch, repository, number))
        header = f"task: review-pr | upstream: {repository}@{sha} | PR: #{number} | PR head: {head}"
    elif task == "smoke-test":
        header = "task: smoke-test"
        if number is not None:
            path = output_dir / "appendix.md"
            write_bounded(path, fetch_context.issue_context(fetch, repository, number, with_comments=False))
            appendix = str(path)
            header += f" | issue: {repository}#{number}"
    else:
        raise PrepareError(f"unknown task {task!r}")

    for directory in (upstream, pr_head):
        if directory.is_dir():
            for path in remove_symlinks(directory):
                print(f"Removed symbolic link {path.relative_to(workspace).as_posix()}")

    return {"header": header, "max_turns": str(MAX_TURNS[task]), "appendix": appendix}


def optional_number(text: str) -> int | None:
    return int(text) if text else None


def main(argv: list[str] | None = None, fetch: Fetch | None = None, git: Git = run_git) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(MAX_TURNS))
    parser.add_argument("--number", type=optional_number, default=None,
                        help="issue or PR number; empty for a smoke test without issue")
    parser.add_argument("--repository", default="cgeo/cgeo")
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--github-output", type=Path, help="append the step outputs to this file")
    args = parser.parse_args(argv)

    fetch = fetch or fetch_context.github_fetch(os.environ.get("GH_API_TOKEN"))
    try:
        if not fetch_context.REPOSITORY_PATTERN.fullmatch(args.repository):
            raise PrepareError(f"invalid repository name {args.repository!r}")
        outputs = prepare(args.task, args.number, args.repository, args.workspace,
                          args.output_dir, fetch, git)
    except (PrepareError, ContextError) as exc:
        print(f"Cannot prepare task: {exc}", file=sys.stderr)
        return 1

    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as stream:
            for name, value in outputs.items():
                stream.write(f"{name}={value}\n")
    print(f"Prepared {args.task}: {outputs['header']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
