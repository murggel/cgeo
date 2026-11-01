#!/usr/bin/env python3
"""Strict validation for AI workflow request YAML files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


TASK_SCHEMAS = {
    "analyze-issue": {"issue"},
}
COMMON_KEYS = {"task", "provider"}
PROVIDERS = {"claude", "copilot"}
TASK_ID_PATTERN = re.compile(r"^issue-[1-9][0-9]*$")


def fail(message: str) -> None:
    print(f"Invalid request: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request_file", type=Path)
    args = parser.parse_args()

    try:
        request = yaml.safe_load(args.request_file.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        fail(f"cannot read valid YAML ({exc})")

    if not isinstance(request, dict):
        fail("top-level YAML value must be a mapping")

    task = request.get("task")
    if task not in TASK_SCHEMAS:
        fail(f"unsupported task {task!r}")

    provider = request.get("provider")
    if provider not in PROVIDERS:
        fail("provider must be 'claude' or 'copilot'")

    expected_keys = COMMON_KEYS | TASK_SCHEMAS[task]
    actual_keys = set(request)
    if actual_keys != expected_keys:
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys)
        fail(f"wrong keys (missing={missing}, unexpected={extra})")

    issue = request["issue"]
    if isinstance(issue, bool) or not isinstance(issue, int) or issue < 1:
        fail("issue must be a positive integer")

    task_id = args.request_file.parent.name
    if not TASK_ID_PATTERN.fullmatch(task_id) or task_id != f"issue-{issue}":
        fail("request directory must be named issue-<issue-number>")

    print(f"Valid request: task={task}, provider={provider}, issue={issue}")


if __name__ == "__main__":
    main()
