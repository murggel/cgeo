#!/usr/bin/env python3
"""Strict validation for AI workflow request files.

This script is the single place that decides which tasks, providers,
repositories and directory names are allowed. The workflow only consumes
its outputs and does not repeat these rules.

Every request lives at ai/requests/<subject>/<request-id>/request.yml.
Branch reviews name a branch of the fork and a base branch of the upstream
repository. Analyses and reviews may carry free-text ``instructions`` that are added to
the prompt; the workflow passes them on unchanged.
"""

from __future__ import annotations

import argparse
import re
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


MAX_REQUEST_BYTES = 16_384
MAX_NUMBER = 999_999_999
MAX_INSTRUCTIONS_CHARS = 4_000
# Tabs and line breaks are fine; other control characters are not.
FORBIDDEN_CHARACTERS = re.compile("[\x00-\x08\x0b-\x1f\x7f]")
# review-branch: branch names of the fork, restricted to safe characters.
BRANCH_PATTERN = re.compile(r"[A-Za-z0-9_][A-Za-z0-9._/-]{0,199}")
ALLOWED_BASES = frozenset({"master", "release"})
DEFAULT_REPOSITORY = "cgeo/cgeo"
# Only smoke tests may choose a repository; all other tasks use the default.
ALLOWED_REPOSITORIES = frozenset({"cgeo/cgeo", "murggel/cgeo"})

NUMBER = r"(?P<number>[1-9][0-9]{0,8})"
DESCRIPTION = r"(?:-[A-Za-z0-9_-]+)?"
NAME = re.compile("[A-Za-z0-9_-]+")


@dataclass(frozen=True)
class TaskRule:
    providers: frozenset[str]
    required_keys: frozenset[str]
    optional_keys: frozenset[str]
    subject: re.Pattern[str]
    request_id: re.Pattern[str]
    layout: str


TASKS = {
    "analyze-issue": TaskRule(
        providers=frozenset({"claude", "copilot"}),
        required_keys=frozenset({"issue"}),
        optional_keys=frozenset({"instructions"}),
        subject=re.compile(rf"issue-{NUMBER}{DESCRIPTION}"),
        request_id=re.compile(rf"analysis-[0-9]{{3}}{DESCRIPTION}"),
        layout="ai/requests/issue-<number>[-description]/analysis-NNN[-description]/request.yml",
    ),
    "review-pr": TaskRule(
        providers=frozenset({"claude", "copilot"}),
        required_keys=frozenset({"pr"}),
        optional_keys=frozenset({"instructions"}),
        subject=re.compile(rf"(?:pr-{NUMBER}|issue-[1-9][0-9]{{0,8}}){DESCRIPTION}"),
        request_id=re.compile(rf"review(?:-pr)?-[0-9]{{3}}{DESCRIPTION}"),
        layout="ai/requests/(pr|issue)-<number>[-description]/review[-pr]-NNN[-description]/request.yml",
    ),
    "review-branch": TaskRule(
        providers=frozenset({"claude", "copilot"}),
        required_keys=frozenset({"branch", "base"}),
        optional_keys=frozenset({"instructions"}),
        subject=re.compile(rf"branch-[A-Za-z0-9_-]+"),
        request_id=re.compile(rf"review-[0-9]{{3}}{DESCRIPTION}"),
        layout="ai/requests/branch-<description>/review-NNN[-description]/request.yml",
    ),
    "smoke-test": TaskRule(
        providers=frozenset({"claude", "copilot"}),
        required_keys=frozenset(),
        optional_keys=frozenset({"issue", "repository"}),
        subject=re.compile("smoke-test"),
        request_id=NAME,
        layout="ai/requests/smoke-test/<name>/request.yml",
    ),
}


@dataclass(frozen=True)
class Request:
    path: PurePosixPath
    task: str
    provider: str
    number: int | None
    repository: str
    instructions: str = ""
    branch: str = ""
    base: str = ""

    def outputs(self) -> dict[str, str]:
        return {
            "request_dir": self.path.parent.as_posix(),
            "task": self.task,
            "provider": self.provider,
            "number": "" if self.number is None else str(self.number),
            "repository": self.repository,
            "instructions": self.instructions,
            "branch": self.branch,
            "base": self.base,
        }

    def summary(self) -> str:
        lines = [f"- Task: {self.task}", f"- Provider: {self.provider}"]
        if self.task == "review-pr":
            lines.append(f"- Pull request: {self.repository}#{self.number}")
        elif self.task == "review-branch":
            lines.append(f"- Branch: {self.branch} (base: {self.repository}:{self.base})")
        elif self.number is not None:
            lines.append(f"- Issue: {self.repository}#{self.number}")
        if self.instructions:
            lines.append(f"- Additional instructions: {len(self.instructions)} characters")
        lines.append(f"- Request: {self.path.as_posix()}")
        return "\n".join(lines)


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate keys, anchors and aliases."""

    def compose_node(self, parent, index):
        event = self.peek_event()
        if getattr(event, "anchor", None) is not None:
            raise yaml.constructor.ConstructorError(
                None, None, "YAML anchors and aliases are not allowed", event.start_mark
            )
        return super().compose_node(parent, index)


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                "all mapping keys must be strings", key_node.start_mark,
            )
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"duplicate key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def _split_path(request_path: str | PurePosixPath) -> tuple[str, str]:
    """Return subject and request id of ai/requests/<subject>/<request-id>/request.yml."""
    parts = PurePosixPath(request_path).parts
    if (
        len(parts) != 5
        or parts[:2] != ("ai", "requests")
        or parts[4] != "request.yml"
        or not all(NAME.fullmatch(part) for part in parts[2:4])
    ):
        raise ValueError(
            "request must be stored as ai/requests/<subject>/<request-id>/request.yml; "
            "directory names may only contain A-Z, a-z, 0-9, '_' and '-'"
        )
    return parts[2], parts[3]


def _read_yaml(root: Path, path: PurePosixPath) -> Any:
    parts = path.parts
    for depth in range(1, len(parts) + 1):
        if (root.joinpath(*parts[:depth])).is_symlink():
            raise ValueError(f"'{PurePosixPath(*parts[:depth])}' must not be a symbolic link")
    file = root.joinpath(*parts)
    if not file.is_file():
        raise ValueError("request file does not exist or is not a regular file")
    try:
        if file.stat().st_size > MAX_REQUEST_BYTES:
            raise ValueError(f"request file must not exceed {MAX_REQUEST_BYTES // 1024} KiB")
        return yaml.load(file.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, UnicodeError, yaml.YAMLError, RecursionError) as exc:
        raise ValueError(f"cannot read valid YAML ({exc})") from exc


def _number(request: dict[str, Any], key: str) -> int:
    value = request[key]
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_NUMBER:
        raise ValueError(f"{key} must be a positive integer up to {MAX_NUMBER}")
    return value


def _instructions(request: dict[str, Any]) -> str:
    if "instructions" not in request:
        return ""
    value = request["instructions"]
    if not isinstance(value, str):
        raise ValueError("instructions must be text (use a YAML block scalar 'instructions: |')")
    text = value.replace("\r\n", "\n").strip()
    if not text:
        raise ValueError("instructions must not be empty; remove the key instead")
    if len(text) > MAX_INSTRUCTIONS_CHARS:
        raise ValueError(f"instructions must not exceed {MAX_INSTRUCTIONS_CHARS} characters")
    if FORBIDDEN_CHARACTERS.search(text):
        raise ValueError("instructions must not contain control characters")
    return text


def _branch(request: dict[str, Any]) -> tuple[str, str]:
    if "branch" not in request:
        return "", ""
    branch, base = request["branch"], request["base"]
    if (
        not isinstance(branch, str)
        or not BRANCH_PATTERN.fullmatch(branch)
        or ".." in branch or "//" in branch or "/." in branch or "@{" in branch
        or branch.endswith(("/", ".", ".lock"))
    ):
        raise ValueError(
            "branch must be a branch name of up to 200 characters A-Z, a-z, 0-9, '.', '_', '-' and '/'. "
            "It must start with a letter, a digit or '_', must not contain '..', '//' or '/.' "
            "and must not end with '/', '.' or '.lock' (e.g. feature/issue-123-fix-map)"
        )
    if not isinstance(base, str) or base not in ALLOWED_BASES:
        raise ValueError(f"base must be one of: {', '.join(sorted(ALLOWED_BASES))}")
    return branch, base


def write_github_output(path: Path, outputs: dict[str, str]) -> None:
    """Append outputs to $GITHUB_OUTPUT; multi-line values use a random delimiter."""
    with path.open("a", encoding="utf-8") as stream:
        for name, value in outputs.items():
            if "\n" not in value:
                stream.write(f"{name}={value}\n")
                continue
            delimiter = f"EOF_{uuid.uuid4().hex}"
            if delimiter in value:  # practically impossible, but never ambiguous
                raise ValueError(f"cannot write output {name}")
            stream.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")


def validate_request(request_path: str | PurePosixPath, root: Path = Path(".")) -> Request:
    """Validate a request given relative to the repository root ``root``."""
    path = PurePosixPath(request_path)
    subject, request_id = _split_path(path)
    request = _read_yaml(root, path)

    if not isinstance(request, dict):
        raise ValueError("top-level YAML value must be a mapping")

    task = request.get("task")
    if not isinstance(task, str) or task not in TASKS:
        raise ValueError(f"task must be one of: {', '.join(sorted(TASKS))}")
    rule = TASKS[task]

    provider = request.get("provider")
    if not isinstance(provider, str) or provider not in rule.providers:
        raise ValueError(
            f"provider for task '{task}' must be one of: {', '.join(sorted(rule.providers))}"
        )

    required_keys = {"task", "provider"} | rule.required_keys
    allowed_keys = required_keys | rule.optional_keys
    missing = sorted(required_keys - request.keys())
    unexpected = sorted(request.keys() - allowed_keys)
    if missing or unexpected:
        raise ValueError(f"wrong keys (missing={missing}, unexpected={unexpected})")

    number_key = "pr" if task == "review-pr" else "issue"
    number = _number(request, number_key) if number_key in request else None

    if "repository" in request and number is None:
        raise ValueError("repository can only be specified together with an issue")
    repository = request.get("repository", DEFAULT_REPOSITORY)
    if not isinstance(repository, str) or repository not in ALLOWED_REPOSITORIES:
        raise ValueError(f"repository must be one of: {', '.join(sorted(ALLOWED_REPOSITORIES))}")

    subject_match = rule.subject.fullmatch(subject)
    if subject_match is None or rule.request_id.fullmatch(request_id) is None:
        raise ValueError(f"'{task}' requests must be stored as {rule.layout}")
    if "number" in rule.subject.groupindex and subject_match["number"] is not None \
            and int(subject_match["number"]) != number:
        raise ValueError(
            f"directory '{subject}' refers to {number_key} {subject_match['number']}, "
            f"but the request specifies {number_key} {number}"
        )

    branch, base = _branch(request)
    return Request(path, task, provider, number, repository, _instructions(request), branch, base)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request_file", help="path relative to the repository root")
    parser.add_argument(
        "--github-output", type=Path, help="append the workflow outputs to this file"
    )
    args = parser.parse_args(argv)

    try:
        request = validate_request(args.request_file)
    except ValueError as exc:
        print(f"Invalid request: {exc}", file=sys.stderr)
        return 1

    if args.github_output:
        write_github_output(args.github_output, request.outputs())
    print(request.summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())
