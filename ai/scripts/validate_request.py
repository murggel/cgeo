#!/usr/bin/env python3
"""Strict validation for AI workflow request YAML files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


TASK_SCHEMAS = {
    "analyze-issue": {"issue"},
    "smoke-test": set(),
}
COMMON_KEYS = {"task", "provider"}
PROVIDERS = {"claude", "copilot"}
ISSUE_TASK_ID_PATTERN = re.compile(r"^issue-([1-9][0-9]*)(?:-.+)?$")
SMOKE_TEST_TASK_ID_PATTERN = re.compile(r"^smoke-test(?:-[a-z0-9]+)*$")


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "unhashable mapping key",
                key_node.start_mark,
            )
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def validate_request(request_file: Path) -> tuple[str, str, int | None]:
    if request_file.name != "request.yml":
        raise ValueError("request file must be named request.yml")
    if request_file.parent.parent.name != "requests":
        raise ValueError("request file must be inside ai/requests/<task-id>/")

    try:
        if request_file.stat().st_size > 16_384:
            raise ValueError("request file must not exceed 16 KiB")
        request = yaml.load(
            request_file.read_text(encoding="utf-8"), Loader=UniqueKeyLoader
        )
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read valid YAML ({exc})") from exc

    if not isinstance(request, dict):
        raise ValueError("top-level YAML value must be a mapping")
    if any(not isinstance(key, str) for key in request):
        raise ValueError("all mapping keys must be strings")

    task = request.get("task")
    if not isinstance(task, str) or task not in TASK_SCHEMAS:
        raise ValueError(f"unsupported task {task!r}")

    provider = request.get("provider")
    if not isinstance(provider, str) or provider not in PROVIDERS:
        raise ValueError("provider must be 'claude' or 'copilot'")

    expected_keys = COMMON_KEYS | TASK_SCHEMAS[task]
    actual_keys = set(request)
    if actual_keys != expected_keys:
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys)
        raise ValueError(
            f"wrong keys (missing={missing}, unexpected={extra})"
        )

    issue = request.get("issue")
    if task == "analyze-issue":
        if isinstance(issue, bool) or not isinstance(issue, int) or issue < 1:
            raise ValueError("issue must be a positive integer")

    task_id = request_file.parent.name
    if task == "analyze-issue":
        task_id_match = ISSUE_TASK_ID_PATTERN.fullmatch(task_id)
        if task_id_match is None:
            raise ValueError(
                f"request directory '{task_id}' must match 'issue-{issue}[-description]'"
            )
        directory_issue = int(task_id_match.group(1))
        if directory_issue != issue:
            raise ValueError(
                f"request directory '{task_id}' refers to issue {directory_issue}, "
                f"but request specifies issue {issue}"
            )
    elif SMOKE_TEST_TASK_ID_PATTERN.fullmatch(task_id) is None:
        raise ValueError(
            f"request directory '{task_id}' must match 'smoke-test[-description]'"
        )

    return task, provider, issue if task == "analyze-issue" else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request_file", type=Path)
    args = parser.parse_args()

    try:
        task, provider, issue = validate_request(args.request_file)
    except ValueError as exc:
        print(f"Invalid request: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    issue_text = str(issue) if issue is not None else "none"
    print(f"Valid request: task={task}, provider={provider}, issue={issue_text}")


if __name__ == "__main__":
    main()
