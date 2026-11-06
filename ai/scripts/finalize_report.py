#!/usr/bin/env python3
"""Turn raw agent output into the report.md that the workflow publishes.

The report gets a one-line HTML comment header for reproducibility, an
optional appendix, a size limit, and a scan for credentials. A report that
looks like it contains a credential is not written at all.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


MAX_REPORT_BYTES = 512 * 1024
MIN_SECRET_LENGTH = 8
TOKEN_PATTERNS = (
    ("Anthropic API key or OAuth token", re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}")),
)


class ReportError(Exception):
    """Raised when no publishable report can be created."""


def read_copilot_output(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as exc:
        raise ReportError(f"cannot read Copilot output ({exc})") from exc
    if not text:
        raise ReportError("Copilot finished without producing a report")
    return text


def read_claude_result(path: Path) -> str:
    """Return only Claude's final answer, not the intermediate assistant messages."""
    if path.is_symlink() or not path.is_file():
        raise ReportError("Claude execution file is missing or not a regular file")
    try:
        messages = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise ReportError(f"cannot read Claude execution file ({exc})") from exc
    if not isinstance(messages, list):
        raise ReportError("Claude execution file does not contain a message list")

    results = [m for m in messages if isinstance(m, dict) and m.get("type") == "result"]
    if not results:
        raise ReportError("Claude execution file contains no final result")
    final = results[-1]
    if final.get("is_error") or final.get("subtype") != "success":
        raise ReportError(
            f"Claude did not finish successfully (subtype={final.get('subtype')!r}); "
            "for 'error_max_turns' raise --max-turns or narrow the request"
        )
    text = final.get("result")
    if not isinstance(text, str) or not text.strip():
        raise ReportError("Claude finished without producing a report")
    return text.strip()


def build_report(header: str, body: str, appendix: str | None = None) -> str:
    parts = [f"<!-- {header} -->", "", body.strip()]
    if appendix and appendix.strip():
        parts += ["", "---", "", appendix.strip()]
    return "\n".join(parts) + "\n"


def find_secrets(text: str, secret_values: dict[str, str]) -> list[str]:
    """Return a description of each credential found; never the credential itself."""
    findings = [name for name, pattern in TOKEN_PATTERNS if pattern.search(text)]
    findings += [
        f"value of {name}"
        for name, value in secret_values.items()
        if len(value) >= MIN_SECRET_LENGTH and value in text
    ]
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--copilot-output", type=Path, help="text printed by copilot -s")
    source.add_argument("--claude-execution-file", type=Path, help="execution_file of the Claude action")
    parser.add_argument("--header", required=True, help="text of the leading HTML comment")
    parser.add_argument("--append", type=Path, help="file appended below a separator")
    parser.add_argument(
        "--secret-env", action="append", default=[], metavar="NAME",
        help="environment variable whose value must not appear in the report",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        if args.copilot_output:
            body = read_copilot_output(args.copilot_output)
        else:
            body = read_claude_result(args.claude_execution_file)
        try:
            appendix = args.append.read_text(encoding="utf-8") if args.append else None
        except (OSError, UnicodeError) as exc:
            raise ReportError(f"cannot read appendix ({exc})") from exc

        report = build_report(args.header, body, appendix)
        secrets = {name: os.environ.get(name, "") for name in args.secret_env}
        findings = find_secrets(report, secrets)
        if findings:
            raise ReportError(
                "the report seems to contain a credential (" + ", ".join(findings)
                + "); it was not saved"
            )
        data = report.encode("utf-8")
        if len(data) > MAX_REPORT_BYTES:
            raise ReportError(
                f"report is {len(data)} bytes and exceeds the {MAX_REPORT_BYTES // 1024} KiB limit"
            )
    except ReportError as exc:
        print(f"Cannot create report: {exc}", file=sys.stderr)
        return 1

    args.output.write_bytes(data)
    print(f"Wrote {len(data)} bytes to {args.output}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
