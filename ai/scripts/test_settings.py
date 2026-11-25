import tempfile
import unittest
from datetime import date
from pathlib import Path

import settings
from settings import SettingsError, parse, resolve, used_ai_credits


BASE = {
    "cleanup": {"count": 20, "auto": [
        {"days": "1-20", "weekdays": ["fri"], "provider": "claude"},
        {"days": "21-31", "provider": "copilot", "max_batches": 5},
    ]},
    "copilot": {"monthly_credits": 1500, "cost_per_batch": 100, "reserve": 300,
                "cleanup_model": "claude-haiku-5.5"},
}
LATE = date(2026, 11, 25)


def usage(*items):
    return {"usageItems": list(items)}


def credit(quantity, sku="Copilot AI Credits", unit="ai-credits"):
    return {"sku": sku, "unitType": unit, "grossQuantity": quantity}


class Api:
    def __init__(self, response=None, error=None):
        self.response, self.error, self.paths = response, error, []

    def __call__(self, path):
        self.paths.append(path)
        if self.error:
            raise SettingsError(self.error)
        return self.response


class ParseTest(unittest.TestCase):
    def test_values(self):
        result = parse(BASE)
        self.assertEqual((result.monthly_credits, result.cost_per_batch, result.reserve, result.cleanup_model),
                         (1500, 100, 300, "claude-haiku-5.5"))
        self.assertEqual(result.rules[1].max_batches, 5)

    def test_old_keys_are_rejected(self):
        with self.assertRaisesRegex(SettingsError, "unknown keys"):
            parse({"copilot": {"monthly_requests": 300}})

    def test_invalid_model(self):
        for model in ("Claude Haiku", "a;b", 5):
            with self.assertRaisesRegex(SettingsError, "cleanup_model"):
                parse({"copilot": {"cleanup_model": model}})

    def test_repository_settings_are_valid(self):
        settings.load()


class CreditsTest(unittest.TestCase):
    def test_only_ai_credit_items_count(self):
        api = Api(usage(credit(120.5), credit(30), credit(999, sku="Copilot Premium Request"),
                        credit(999, unit="requests"), credit(1, unit="credits"), "junk"))
        self.assertEqual(used_ai_credits(api, "murggel", LATE), 151.5)
        self.assertEqual(api.paths, ["/users/murggel/settings/billing/ai_credit/usage?year=2026&month=11"])

    def test_missing_data(self):
        for response in ({}, [], usage(), usage(credit(5, sku="other")), usage(credit("many"))):
            with self.assertRaises(SettingsError):
                used_ai_credits(Api(response), "murggel", LATE)


    def test_real_response(self):
        """Shape of the answer of 2026-11-16, one entry per model."""
        items = [{"product": "Copilot", "sku": "Copilot AI Credits", "model": model, "unitType": "ai-credits",
                  "pricePerUnit": 0.01, "grossQuantity": quantity, "discountQuantity": quantity,
                  "netQuantity": 0.0, "netAmount": 0.0}
                 for model, quantity in (("Auto: GPT-6 Luna", 0.10859715), ("Claude Haiku 5.5", 0.00487),
                                         ("Claude Sonnet 5.5", 427.6994),
                                         ("Fusion (Standard): GPT-6 Luna", 0.14949725))]
        response = {"timePeriod": {"year": 2026, "month": 11}, "user": "murggel", "usageItems": items}
        self.assertEqual(used_ai_credits(Api(response), "murggel", LATE), 428.0)


class ResolveTest(unittest.TestCase):
    def resolve(self, api, provider="auto", day=LATE):
        return resolve(parse(BASE), provider, 0, day, api, "murggel")

    def test_batches_limited_by_credits(self):
        outputs, explanation = self.resolve(Api(usage(credit(950))))
        self.assertEqual((outputs["provider"], outputs["batches"], outputs["model"]),
                         ("copilot", "2", "claude-haiku-5.5"))
        self.assertEqual(outputs["credits"], "950 of 1500 used, 250 available beyond the reserve")
        self.assertIn("2 batch(es)", explanation)

    def test_batches_limited_by_rule(self):
        outputs, _ = self.resolve(Api(usage(credit(0))))
        self.assertEqual(outputs["batches"], "5")

    def test_not_enough_credits(self):
        outputs, explanation = self.resolve(Api(usage(credit(1150))))
        self.assertEqual(outputs["provider"], "")
        self.assertIn("not enough", explanation)

    def test_errors_skip_copilot(self):
        for api in (None, Api(error="billing API returned HTTP 404:\nNot Found"), Api(usage())):
            outputs, explanation = self.resolve(api)
            self.assertEqual(outputs["provider"], "")
            self.assertIn("skipped", explanation)
            self.assertNotIn("\n", explanation)

    def test_claude_rule_needs_no_credits(self):
        api = Api(error="must not be called")
        outputs, _ = self.resolve(api, day=date(2026, 11, 20))
        self.assertEqual((outputs["provider"], outputs["model"], outputs["credits"]), ("claude", "", ""))
        self.assertEqual(api.paths, [])

    def test_explicit_copilot_shows_credits_but_never_skips(self):
        outputs, _ = self.resolve(Api(usage(credit(10))), provider="copilot")
        self.assertEqual((outputs["provider"], outputs["model"]), ("copilot", "claude-haiku-5.5"))
        self.assertIn("10 of 1500", outputs["credits"])
        outputs, _ = self.resolve(Api(error="HTTP 500"), provider="copilot")
        self.assertEqual((outputs["provider"], outputs["credits"]), ("copilot", ""))

    def test_explicit_claude(self):
        outputs, _ = self.resolve(None, provider="claude")
        self.assertEqual((outputs["provider"], outputs["model"]), ("claude", ""))


class ExtraTest(unittest.TestCase):
    SETTINGS = {**BASE, "cleanup": {**BASE["cleanup"], "extra": [
        {"days": "26-30", "until": "2026-11-30", "provider": "claude", "count": 30}]}}

    def test_extra_rule_with_until(self):
        settings = parse(self.SETTINGS)
        self.assertEqual(settings.extra_rule_for(date(2026, 11, 27)).provider, "claude")
        self.assertIsNone(settings.extra_rule_for(date(2026, 12, 27)))
        self.assertIsNone(settings.extra_rule_for(date(2026, 11, 25)))

    def test_resolve_extra(self):
        api = Api(error="must not be called")
        outputs, explanation = resolve(parse(self.SETTINGS), "claude", 0, date(2026, 11, 27), api, "murggel", True)
        self.assertEqual((outputs["provider"], outputs["count"], outputs["model"]), ("claude", "30", ""))
        self.assertIn("extra rule", explanation)
        outputs, explanation = resolve(parse(self.SETTINGS), "copilot", 0, date(2026, 11, 27), api, "murggel", True)
        self.assertEqual(outputs["provider"], "")
        outputs, _ = resolve(parse(self.SETTINGS), "claude", 0, date(2026, 12, 27), api, "murggel", True)
        self.assertEqual(outputs["provider"], "")

    def test_invalid_until(self):
        bad = {**BASE, "cleanup": {**BASE["cleanup"], "extra": [{"provider": "claude", "until": "30.11."}]}}
        with self.assertRaises(SettingsError):
            parse(bad)


class MainTest(unittest.TestCase):
    def test_credits_command_without_token(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "out"
            self.assertEqual(settings.main(["credits", "--user", "murggel", "--github-output", str(output)]), 0)
            self.assertIn("credits=\n", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
