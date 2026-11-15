#!/usr/bin/env python3
"""Read ai/settings.yml and decide what the scheduled cleanup does.

Commands:
  tonight   for the scheduled task (no network): whether to push a snapshot
            and/or a cleanup request tonight, as "snapshot=yes|no" and
            "cleanup=yes|no" lines.
  resolve   for the workflow: turns a cleanup request into concrete values.
            For "provider: auto" it picks the rule of the night and, for
            Copilot, checks the premium-request quota of the current month
            (GitHub billing API, token in COPILOT_BILLING_TOKEN). It writes
            provider (empty: skip), count, batches, skip_days and
            waiting_months to $GITHUB_OUTPUT.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml


DEFAULT_PATH = Path(__file__).resolve().parent.parent / "settings.yml"
WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
PROVIDERS = ("claude", "copilot")
MAX_COUNT = 30
MAX_BATCHES = 10
API_ROOT = "https://api.github.com"


class SettingsError(Exception):
    """Raised when the settings are invalid or the quota cannot be read."""


@dataclass(frozen=True)
class Rule:
    days: frozenset[int]
    weekdays: frozenset[int]
    provider: str
    count: int
    max_batches: int

    def matches(self, day: date) -> bool:
        return day.day in self.days and (not self.weekdays or day.weekday() in self.weekdays)


@dataclass(frozen=True)
class Settings:
    timezone: ZoneInfo
    snapshot_days: frozenset[int]
    count: int
    skip_days: int
    waiting_months: int
    rules: tuple[Rule, ...]
    monthly_requests: int
    cost_per_run: int
    reserve: int

    def today(self) -> date:
        return datetime.now(self.timezone).date()

    def rule_for(self, day: date) -> Rule | None:
        return next((rule for rule in self.rules if rule.matches(day)), None)


def _int(value: Any, name: str, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise SettingsError(f"{name} must be a number from {low} to {high}")
    return value


def _days(value: Any, name: str) -> frozenset[int]:
    if isinstance(value, str) and "-" in value:
        first, _, last = value.partition("-")
        try:
            low, high = int(first), int(last)
        except ValueError:
            raise SettingsError(f"{name} must be a range like 1-20 or a list of days") from None
        if not 1 <= low <= high <= 31:
            raise SettingsError(f"{name}: the range must lie within 1-31")
        return frozenset(range(low, high + 1))
    if isinstance(value, list) and value:
        return frozenset(_int(item, name, 1, 31) for item in value)
    raise SettingsError(f"{name} must be a range like 1-20 or a list of days")


def _mapping(value: Any, name: str, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SettingsError(f"{name} must be a mapping")
    unknown = sorted(set(value) - keys)
    if unknown:
        raise SettingsError(f"{name}: unknown keys {unknown}")
    return value


def parse(data: Any) -> Settings:
    root = _mapping(data, "settings", {"timezone", "snapshot", "cleanup", "copilot"})
    try:
        timezone = ZoneInfo(str(root.get("timezone", "Europe/Berlin")))
    except (ZoneInfoNotFoundError, ValueError):
        raise SettingsError("timezone must be a time zone name like Europe/Berlin") from None
    snapshot = _mapping(root.get("snapshot", {}), "snapshot", {"days"})
    cleanup = _mapping(root.get("cleanup", {}), "cleanup",
                       {"count", "skip_days", "waiting_months", "auto"})
    copilot = _mapping(root.get("copilot", {}), "copilot", {"monthly_requests", "cost_per_run", "reserve"})
    count = _int(cleanup.get("count", 20), "cleanup.count", 1, MAX_COUNT)

    rules = []
    auto = cleanup.get("auto", [])
    if not isinstance(auto, list):
        raise SettingsError("cleanup.auto must be a list of rules")
    for index, item in enumerate(auto, start=1):
        name = f"cleanup.auto rule {index}"
        rule = _mapping(item, name, {"days", "weekdays", "provider", "count", "max_batches"})
        provider = rule.get("provider")
        if provider not in PROVIDERS:
            raise SettingsError(f"{name}: provider must be one of {', '.join(PROVIDERS)}")
        weekdays = rule.get("weekdays", [])
        if not isinstance(weekdays, list) or any(day not in WEEKDAYS for day in weekdays):
            raise SettingsError(f"{name}: weekdays must be a list of {', '.join(WEEKDAYS)}")
        batches = _int(rule.get("max_batches", 1), f"{name}: max_batches", 1, MAX_BATCHES)
        if batches > 1 and provider != "copilot":
            raise SettingsError(f"{name}: max_batches is only possible with copilot")
        rules.append(Rule(_days(rule.get("days", "1-31"), f"{name}: days"),
                          frozenset(WEEKDAYS.index(day) for day in weekdays), provider,
                          _int(rule.get("count", count), f"{name}: count", 1, MAX_COUNT), batches))

    return Settings(
        timezone=timezone,
        snapshot_days=_days(snapshot.get("days", [1, 15]), "snapshot.days"),
        count=count,
        skip_days=_int(cleanup.get("skip_days", 183), "cleanup.skip_days", 0, 3650),
        waiting_months=_int(cleanup.get("waiting_months", 6), "cleanup.waiting_months", 1, 120),
        rules=tuple(rules),
        monthly_requests=_int(copilot.get("monthly_requests", 300), "copilot.monthly_requests", 0, 100000),
        cost_per_run=_int(copilot.get("cost_per_run", 1), "copilot.cost_per_run", 0, 1000),
        reserve=_int(copilot.get("reserve", 30), "copilot.reserve", 0, 100000),
    )


def load(path: Path = DEFAULT_PATH) -> Settings:
    try:
        return parse(yaml.safe_load(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise SettingsError(f"cannot read {path} ({exc})") from exc


Fetch = Callable[[str], Any]


def billing_fetch(token: str) -> Fetch:
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}",
               "User-Agent": "cgeo-ai-workflow", "X-GitHub-Api-Version": "2022-11-28"}

    def fetch(path: str) -> Any:
        request = urllib.request.Request(API_ROOT + path, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            raise SettingsError(f"billing API returned HTTP {exc.code}: {exc.read(300).decode('utf-8', 'replace')}") from exc
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            raise SettingsError(f"billing API request failed: {exc}") from exc

    return fetch


def used_premium_requests(fetch: Fetch, user: str, day: date) -> float:
    """Premium requests used in the month of ``day`` (all products and models)."""
    data = fetch(f"/users/{user}/settings/billing/premium_request/usage?year={day.year}&month={day.month}")
    items = data.get("usageItems") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise SettingsError("unexpected billing API response: no usageItems")
    return sum(float(item.get("grossQuantity") or 0) for item in items if isinstance(item, dict))


def resolve(settings: Settings, provider: str, count: int, day: date,
            fetch: Fetch | None, user: str) -> tuple[dict[str, str], str]:
    """Return the outputs for a cleanup request and a one-line explanation."""
    outputs = {"skip_days": str(settings.skip_days), "waiting_months": str(settings.waiting_months),
               "batches": "1", "count": str(count or settings.count), "provider": provider}
    if provider != "auto":
        return outputs, f"provider {provider} given by the request"
    rule = settings.rule_for(day)
    if rule is None:
        outputs["provider"] = ""
        return outputs, f"no rule of cleanup.auto matches {day:%a %Y-%m-%d}; nothing to do"
    outputs["provider"] = rule.provider
    outputs["count"] = str(count or rule.count)
    if rule.provider == "claude":
        return outputs, f"rule for {day:%a %Y-%m-%d}: claude"
    if fetch is None:
        outputs["provider"] = ""
        return outputs, "Copilot quota unknown (secret COPILOT_BILLING_TOKEN missing); skipped"
    used = used_premium_requests(fetch, user, day)
    available = settings.monthly_requests - settings.reserve - used
    batches = rule.max_batches if settings.cost_per_run == 0 else \
        min(rule.max_batches, int(available // settings.cost_per_run))
    explanation = (f"Copilot quota {settings.monthly_requests}, used {used:g}, reserve "
                   f"{settings.reserve}, {available:g} available")
    if batches < 1:
        outputs["provider"] = ""
        return outputs, explanation + "; not enough for a run, skipped"
    outputs["batches"] = str(batches)
    return outputs, explanation + f"; {batches} batch(es) of {outputs['count']} issues"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--settings", type=Path, default=DEFAULT_PATH)
    sub = parser.add_subparsers(dest="command", required=True)
    tonight = sub.add_parser("tonight")
    tonight.add_argument("--date", default="")
    res = sub.add_parser("resolve")
    res.add_argument("--provider", required=True)
    res.add_argument("--count", default="")
    res.add_argument("--user", required=True, help="GitHub user whose Copilot quota is checked")
    res.add_argument("--date", default="")
    res.add_argument("--github-output", type=Path)
    args = parser.parse_args(argv)

    try:
        settings = load(args.settings)
        day = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else settings.today()
        if args.command == "tonight":
            print(f"snapshot={'yes' if day.day in settings.snapshot_days else 'no'}")
            print(f"cleanup={'yes' if settings.rule_for(day) else 'no'}")
            return 0
        token = os.environ.get("COPILOT_BILLING_TOKEN", "")
        outputs, explanation = resolve(settings, args.provider, int(args.count or 0), day,
                                       billing_fetch(token) if token else None, args.user)
    except (SettingsError, ValueError) as exc:
        print(f"Settings error: {exc}", file=sys.stderr)
        return 1
    print(explanation)
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as stream:
            for name, value in outputs.items():
                stream.write(f"{name}={value}\n")
            stream.write(f"explanation={explanation}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
