#!/usr/bin/env python3
"""Rejects commit messages that GitHub would link to an issue or pull request.

GitHub links a commit message that contains ``#<number>``, ``GH-<number>``,
``<owner>/<repo>#<number>`` or an issue or pull request URL to that issue or pull
request in cgeo/cgeo, even from this fork, and everyone sees the link there.
Commit messages on dev/ai-workflows name the subject folder instead, for example
``pr-18952`` or ``issue-12345``.

Used by the commit-msg hook (``--file``), by the cgeo-ai-request skill before
every commit and by the workflow for the pushed commits and its own report commit.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# "&#<number>" is an HTML character reference, not an issue reference.
REFERENCE = re.compile(
    r"(?<!&)#[0-9]+"
    r"|\bGH-[0-9]+"
    r"|github\.com/[^\s/]+/[^\s/]+/(?:issues|pull|discussions)/[0-9]+",
    re.IGNORECASE,
)
# "git commit --verbose" appends the diff below this line; git does not keep it.
SCISSORS = re.compile(r"^\S+ -+ >8 -+$")


def find_references(message: str) -> list[str]:
    """Returns the references in the message, each once, in order of appearance."""
    return list(dict.fromkeys(match.group(0) for match in REFERENCE.finditer(message)))


def read_message_file(path: Path) -> str:
    """Reads a commit message file as git passes it to the commit-msg hook.

    Comment lines stay in: with ``git commit -m`` git keeps lines that start
    with "#", and the comments git adds itself contain no references.
    """
    lines = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if SCISSORS.match(line):
            break
        lines.append(line)
    return "\n".join(lines)


def check(message: str) -> str | None:
    """Returns an error text for a message with references, otherwise None."""
    references = find_references(message)
    if not references:
        return None
    stripped = message.strip()
    subject = stripped.splitlines()[0] if stripped else ""
    return (f"'{subject}' contains {', '.join(references)}; GitHub would link it to the issue "
            "or pull request in cgeo/cgeo. Name the subject folder instead, e.g. pr-18952.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("messages", nargs="*", metavar="MESSAGE",
                        help="commit message to check; put -- before messages that start with -")
    parser.add_argument("--file", type=Path, action="append", default=[],
                        help="commit message file, as git passes it to the commit-msg hook")
    args = parser.parse_args(argv)
    if not args.messages and not args.file:
        parser.error("give at least one message or --file")

    messages = list(args.messages)
    for path in args.file:
        try:
            messages.append(read_message_file(path))
        except OSError as exc:
            print(f"Cannot read commit message: {exc}", file=sys.stderr)
            return 2
    errors = [error for error in map(check, messages) if error]
    for error in errors:
        print(f"Invalid commit message: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"Commit message{'s' if len(messages) > 1 else ''} OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
