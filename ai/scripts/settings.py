#!/usr/bin/env python3
"""Read ai/settings.yml and decide what the scheduled cleanup does.

Commands:
  tonight   for the scheduled task (no network): whether to push a snapshot
            and/or a cleanup request tonight, as "snapshot=yes|no" and
            "cleanup=yes|no" lines, and as "cleanup_extra=<provider>|no"
            whether to push an extra cleanup request with that provider.
  resolve   for the workflow: turns a cleanup request into concrete values.
            For "provider: auto" it picks the rule of the night and, for
            Copilot, checks the GitHub AI Credits of the current month
            (GitHub billing API, token in COPILOT_BILLING_TOKEN). It writes
            provider (empty: skip), count, batches, skip_days,
            waiting_months, model and credits to $GITHUB_OUTPUT.
  credits   for the workflow: only the AI Credits line for the report header
            of other Copilot runs (written as credits=...; empty if unknown).
"""

from __future__ import annotations

import argparse
import json
import os
import re
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
CREDITS_SKU = "Copilot AI Credits"
# The API reports "ai-credits" (checked 2026-11); "credits" is accepted as well.
CREDITS_UNITS = ("ai-credits", "credits")
MODEL_PATTERN = re.compile(r"[a-z0-9][a-z0-9.-]{0,63}")


class SettingsError(Exception):
    """Raised when the settings are invalid or the quota cannot be read."""


@dataclass(frozen=True)
class Rule:
    days: frozenset[int]
    weekdays: frozenset[int]
    provider: str
    count: int
    max_batches: int
    until: date | None = None

    def matches(self, day: date) -> bool:
        return (day.day in self.days and (not self.weekdays or day.weekday() in self.weekdays)
                and (self.until is None or day <= self.until))


@dataclass(frozen=True)
class Settings:
    timezone: ZoneInfo
    snapshot_days: frozenset[int]
    count: int
    skip_days: int
    waiting_months: int
    rules: tuple[Rule, ...]
    extra_rules: tuple[Rule, ...]
    monthly_credits: int
    cost_per_batch: int
    reserve: int
    cleanup_model: str

    def today(self) -> date:
        return datetime.now(self.timezone).date()

    def rule_for(self, day: date) -> Rule | None:
        return next((rule for rule in self.rules if rule.matches(day)), None)

    def extra_rule_for(self, day: date) -> Rule | None:
        return next((rule for rule in self.extra_rules if rule.matches(day)), None)


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


def _until(value: Any, name: str) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        raise SettingsError(f"{name} must be a date like 2026-11-30") from None


def _rules(items: Any, section: str, count: int) -> tuple[Rule, ...]:
    if not isinstance(items, list):
        raise SettingsError(f"{section} must be a list of rules")
    rules = []
    for index, item in enumerate(items, start=1):
        name = f"{section} rule {index}"
        rule = _mapping(item, name, {"days", "weekdays", "provider", "count", "max_batches", "until"})
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
                          _int(rule.get("count", count), f"{name}: count", 1, MAX_COUNT), batches,
                          _until(rule.get("until"), f"{name}: until")))
    return tuple(rules)


def parse(data: Any) -> Settings:
    root = _mapping(data, "settings", {"timezone", "snapshot", "cleanup", "copilot"})
    try:
        timezone = ZoneInfo(str(root.get("timezone", "Europe/Berlin")))
    except (ZoneInfoNotFoundError, ValueError):
        raise SettingsError("timezone must be a time zone name like Europe/Berlin") from None
    snapshot = _mapping(root.get("snapshot", {}), "snapshot", {"days"})
    cleanup = _mapping(root.get("cleanup", {}), "cleanup",
                       {"count", "skip_days", "waiting_months", "auto", "extra"})
    copilot = _mapping(root.get("copilot", {}), "copilot",
                       {"monthly_credits", "cost_per_batch", "reserve", "cleanup_model"})
    model = copilot.get("cleanup_model", "")
    if not isinstance(model, str) or (model and not MODEL_PATTERN.fullmatch(model)):
        raise SettingsError("copilot.cleanup_model must be a model name like claude-haiku-5.5 (or empty)")
    count = _int(cleanup.get("count", 20), "cleanup.count", 1, MAX_COUNT)

    rules = _rules(cleanup.get("auto", []), "cleanup.auto", count)
    extra_rules = _rules(cleanup.get("extra", []), "cleanup.extra", count)

    return Settings(
        timezone=timezone,
        snapshot_days=_days(snapshot.get("days", [1, 15]), "snapshot.days"),
        count=count,
        skip_days=_int(cleanup.get("skip_days", 183), "cleanup.skip_days", 0, 3650),
        waiting_months=_int(cleanup.get("waiting_months", 6), "cleanup.waiting_months", 1, 120),
        rules=rules,
        extra_rules=extra_rules,
        monthly_credits=_int(copilot.get("monthly_credits", 1500), "copilot.monthly_credits", 0, 1000000),
        cost_per_batch=_int(copilot.get("cost_per_batch", 100), "copilot.cost_per_batch", 0, 100000),
        reserve=_int(copilot.get("reserve", 300), "copilot.reserve", 0, 1000000),
        cleanup_model=model,
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


def used_ai_credits(fetch: Fetch, user: str, day: date) -> float:
    """GitHub AI Credits used in the month of ``day`` (all Copilot products and models).

    Raises SettingsError if the response has no usable credit entries, so that
    Copilot is skipped instead of being run on a wrong count of 0.
    """
    data = fetch(f"/users/{user}/settings/billing/ai_credit/usage?year={day.year}&month={day.month}")
    items = data.get("usageItems") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise SettingsError("unexpected billing API response: no usageItems")
    credits = [item for item in items if isinstance(item, dict)
               and item.get("sku") == CREDITS_SKU and item.get("unitType") in CREDITS_UNITS]
    if not credits:
        raise SettingsError(f"billing API response has no entries for {CREDITS_SKU!r}")
    # grossQuantity is the consumption; netQuantity only the part beyond the included credits.
    try:
        return round(sum(float(item.get("grossQuantity") or 0) for item in credits), 1)
    except (TypeError, ValueError):
        raise SettingsError("unexpected billing API response: grossQuantity is not a number") from None


def credits_line(settings: Settings, used: float) -> str:
    """The AI Credits state for the report header."""
    return (f"{used:g} of {settings.monthly_credits} used, "
            f"{settings.monthly_credits - settings.reserve - used:g} available beyond the reserve")


def check_credits(settings: Settings, fetch: Fetch | None, user: str, day: date) -> tuple[float | None, str]:
    """Return (used credits or None, reason if unknown)."""
    if fetch is None:
        return None, "secret COPILOT_BILLING_TOKEN missing"
    try:
        return used_ai_credits(fetch, user, day), ""
    except SettingsError as exc:
        # One line, as it goes into $GITHUB_OUTPUT and the run summary.
        return None, " ".join(str(exc).split())[:300]


def resolve(settings: Settings, provider: str, count: int, day: date,
            fetch: Fetch | None, user: str, extra: bool = False) -> tuple[dict[str, str], str]:
    """Return the outputs for a cleanup request and a one-line explanation.

    An extra request (``extra: true``, pushed by the scheduled task besides the
    "auto" one) runs only if a rule of cleanup.extra matches the night and names
    the same provider; it then takes count and batches from that rule.
    """
    outputs = {"skip_days": str(settings.skip_days), "waiting_months": str(settings.waiting_months),
               "batches": "1", "count": str(count or settings.count), "provider": provider,
               "model": settings.cleanup_model if provider in ("copilot", "auto") else "", "credits": ""}
    if extra:
        rule = settings.extra_rule_for(day)
        if rule is None or rule.provider != provider:
            outputs["provider"] = ""
            return outputs, (f"no rule of cleanup.extra for {provider} matches {day:%a %Y-%m-%d}; "
                             "nothing to do")
        return _apply_rule(settings, rule, outputs, count, day, fetch, user, "extra rule")
    if provider != "auto":
        if provider == "copilot":
            used, _ = check_credits(settings, fetch, user, day)
            if used is not None:
                outputs["credits"] = credits_line(settings, used)
        return outputs, f"provider {provider} given by the request"
    rule = settings.rule_for(day)
    if rule is None:
        outputs["provider"] = ""
        return outputs, f"no rule of cleanup.auto matches {day:%a %Y-%m-%d}; nothing to do"
    return _apply_rule(settings, rule, outputs, count, day, fetch, user, "rule")


def _apply_rule(settings: Settings, rule: Rule, outputs: dict[str, str], count: int, day: date,
                fetch: Fetch | None, user: str, kind: str) -> tuple[dict[str, str], str]:
    outputs["provider"] = rule.provider
    outputs["count"] = str(count or rule.count)
    if rule.provider == "claude":
        outputs["model"] = ""
        return outputs, f"{kind} for {day:%a %Y-%m-%d}: claude, {outputs['count']} issues"
    outputs["model"] = settings.cleanup_model
    used, reason = check_credits(settings, fetch, user, day)
    if used is None:
        outputs["provider"] = ""
        return outputs, f"Copilot AI Credits unknown ({reason}); skipped"
    outputs["credits"] = credits_line(settings, used)
    available = settings.monthly_credits - settings.reserve - used
    batches = rule.max_batches if settings.cost_per_batch == 0 else \
        min(rule.max_batches, int(available // settings.cost_per_batch))
    explanation = (f"Copilot AI Credits {settings.monthly_credits}, used {used:g}, reserve "
                   f"{settings.reserve}, {available:g} available, about {settings.cost_per_batch} per batch")
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
    res.add_argument("--extra", default="", help="'true' for an extra request (cleanup.extra)")
    res.add_argument("--user", required=True, help="GitHub user whose Copilot quota is checked")
    res.add_argument("--date", default="")
    res.add_argument("--github-output", type=Path)
    cred = sub.add_parser("credits")
    cred.add_argument("--user", required=True, help="GitHub user whose AI Credits are read")
    cred.add_argument("--date", default="")
    cred.add_argument("--github-output", type=Path)
    args = parser.parse_args(argv)

    try:
        settings = load(args.settings)
        day = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else settings.today()
        if args.command == "tonight":
            print(f"snapshot={'yes' if day.day in settings.snapshot_days else 'no'}")
            print(f"cleanup={'yes' if settings.rule_for(day) else 'no'}")
            extra = settings.extra_rule_for(day)
            print(f"cleanup_extra={extra.provider if extra else 'no'}")
            return 0
        token = os.environ.get("COPILOT_BILLING_TOKEN", "")
        fetch = billing_fetch(token) if token else None
        if args.command == "credits":
            used, reason = check_credits(settings, fetch, args.user, day)
            outputs = {"credits": credits_line(settings, used) if used is not None else ""}
            explanation = f"AI Credits: {outputs['credits']}" if used is not None else f"AI Credits unknown ({reason})"
        else:
            outputs, explanation = resolve(settings, args.provider, int(args.count or 0), day, fetch, args.user,
                                           args.extra == "true")
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
