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
OPTIONAL_KEYS = {
    "analyze-issue": set(),
    "smoke-test": {"issue", "repository"},
}
COMMON_KEYS = {"task", "provider"}
PROVIDERS = {"claude", "copilot"}
ALLOWED_ISSUE_REPOSITORIES = {"cgeo/cgeo", "murggel/cgeo"}
DEFAULT_ISSUE_REPOSITORY = "cgeo/cgeo"
MAX_ISSUE_NUMBER = 999_999_999
ISSUE_TASK_ID_PATTERN = re.compile(r"^issue-([1-9][0-9]*)(?:-[A-Za-z0-9._-]+)?$")
SMOKE_TEST_TASK_ID_PATTERN = re.compile(r"^smoke-test(?:-[a-z0-9]+)*$")


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate keys, anchors and aliases."""

    def compose_node(self, parent, index):
        event = self.peek_event()
        if getattr(event, "anchor", None) is not None:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                "YAML anchors and aliases are not allowed",
                event.start_mark,
            )
        return super().compose_node(parent, index)


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


def validate_request(request_file: Path) -> tuple[str, str, int | None, str]:
    if request_file.name != "request.yml":
        raise ValueError("request file must be named request.yml")
    requests_dir = request_file.parent.parent
    if requests_dir.name != "requests" or requests_dir.parent.name != "ai":
        raise ValueError("request file must be inside ai/requests/<task-id>/")
    if request_file.is_symlink():
        raise ValueError("request file must not be a symbolic link")

    try:
        if request_file.stat().st_size > 16_384:
            raise ValueError("request file must not exceed 16 KiB")
        request = yaml.load(
            request_file.read_text(encoding="utf-8"), Loader=UniqueKeyLoader
        )
    except (OSError, UnicodeError, yaml.YAMLError, RecursionError) as exc:
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
    if task == "smoke-test" and provider != "copilot":
        raise ValueError("smoke-test is currently supported only with provider 'copilot'")

    required_keys = COMMON_KEYS | TASK_SCHEMAS[task]
    allowed_keys = required_keys | OPTIONAL_KEYS[task]
    actual_keys = set(request)
    if not required_keys.issubset(actual_keys) or not actual_keys.issubset(allowed_keys):
        missing = sorted(required_keys - actual_keys)
        extra = sorted(actual_keys - allowed_keys)
        raise ValueError(
            f"wrong keys (missing={missing}, unexpected={extra})"
        )

    issue = request.get("issue")
    if task == "analyze-issue" or "issue" in request:
        if (
            isinstance(issue, bool)
            or not isinstance(issue, int)
            or not 1 <= issue <= MAX_ISSUE_NUMBER
        ):
            raise ValueError(
                f"issue must be a positive integer up to {MAX_ISSUE_NUMBER}"
            )

    repository = request.get("repository", DEFAULT_ISSUE_REPOSITORY)
    if not isinstance(repository, str) or repository not in ALLOWED_ISSUE_REPOSITORIES:
        raise ValueError(
            "repository must be one of: " + ", ".join(sorted(ALLOWED_ISSUE_REPOSITORIES))
        )
    if task == "smoke-test" and "repository" in request and issue is None:
        raise ValueError("repository can only be specified when an issue is provided")

    task_id = request_file.parent.name
    if task == "analyze-issue":
        task_id_match = ISSUE_TASK_ID_PATTERN.fullmatch(task_id)
        if task_id_match is None:
            raise ValueError(
                f"request directory '{task_id}' must match 'issue-{issue}[-description]' "
                "(description: letters, digits, '.', '_' and '-')"
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

    return task, provider, issue, repository


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request_file", type=Path)
    args = parser.parse_args()

    try:
        task, provider, issue, repository = validate_request(args.request_file)
    except ValueError as exc:
        print(f"Invalid request: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    issue_text = str(issue) if issue is not None else "none"
    print(
        f"Valid request: task={task}, provider={provider}, "
        f"issue={issue_text}, repository={repository}"
    )


if __name__ == "__main__":
    main()