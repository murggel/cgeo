import os
import tempfile
import unittest
from pathlib import Path

from validate_request import validate_request


class ValidateRequestTest(unittest.TestCase):
    def write_request(
        self,
        text: str,
        directory: str = "issue-17573",
        parent: str = "ai/requests",
    ) -> Path:
        root = Path(tempfile.mkdtemp()) / parent / directory
        root.mkdir(parents=True)
        request = root / "request.yml"
        request.write_text(text, encoding="utf-8")
        return request

    # --- gültige Requests ---

    def test_valid_claude_request(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n"
        )
        self.assertEqual(validate_request(path), ("analyze-issue", "claude", 17573, "cgeo/cgeo"))

    def test_valid_copilot_request(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: copilot\nissue: 17573\n"
        )
        self.assertEqual(validate_request(path), ("analyze-issue", "copilot", 17573, "cgeo/cgeo"))

    def test_valid_smoke_test_request(self):
        path = self.write_request(
            "task: smoke-test\nprovider: copilot\n",
            directory="smoke-test-copilot",
        )
        self.assertEqual(validate_request(path), ("smoke-test", "copilot", None, "cgeo/cgeo"))

    def test_directory_with_descriptive_suffix_is_valid(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            directory="issue-17573-rtl-layout",
        )
        self.assertEqual(validate_request(path), ("analyze-issue", "claude", 17573, "cgeo/cgeo"))

    # --- smoke-test ---

    def test_smoke_test_accepts_issue_with_default_repository(self):
        path = self.write_request(
            "task: smoke-test\nprovider: copilot\nissue: 17573\n",
            directory="smoke-test-copilot",
        )
        self.assertEqual(
            validate_request(path), ("smoke-test", "copilot", 17573, "cgeo/cgeo")
        )

    def test_smoke_test_accepts_issue_in_fork_repository(self):
        path = self.write_request(
            "task: smoke-test\nprovider: copilot\nissue: 42\nrepository: murggel/cgeo\n",
            directory="smoke-test-copilot",
        )
        self.assertEqual(
            validate_request(path), ("smoke-test", "copilot", 42, "murggel/cgeo")
        )

    def test_smoke_test_rejects_repository_without_issue(self):
        path = self.write_request(
            "task: smoke-test\nprovider: copilot\nrepository: murggel/cgeo\n",
            directory="smoke-test-copilot",
        )
        with self.assertRaisesRegex(ValueError, "only be specified when an issue"):
            validate_request(path)

    def test_smoke_test_rejects_unapproved_repository(self):
        path = self.write_request(
            "task: smoke-test\nprovider: copilot\nissue: 42\nrepository: attacker/repo\n",
            directory="smoke-test-copilot",
        )
        with self.assertRaisesRegex(ValueError, "repository must be one of"):
            validate_request(path)

    def test_smoke_test_requires_matching_directory(self):
        path = self.write_request(
            "task: smoke-test\nprovider: copilot\n",
            directory="issue-17573",
        )
        with self.assertRaisesRegex(ValueError, "smoke-test"):
            validate_request(path)

    def test_smoke_test_requires_copilot_provider(self):
        path = self.write_request(
            "task: smoke-test\nprovider: claude\n",
            directory="smoke-test-claude",
        )
        with self.assertRaisesRegex(ValueError, "only with provider 'copilot'"):
            validate_request(path)

    # --- Schlüssel und Werte ---

    def test_duplicate_key_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\ntask: analyze-issue\nprovider: claude\nissue: 17573\n"
        )
        with self.assertRaisesRegex(ValueError, "cannot read valid YAML"):
            validate_request(path)

    def test_boolean_issue_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: true\n",
            directory="issue-1",
        )
        with self.assertRaisesRegex(ValueError, "positive integer"):
            validate_request(path)

    def test_string_issue_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: '17573'\n"
        )
        with self.assertRaisesRegex(ValueError, "positive integer"):
            validate_request(path)

    def test_issue_above_maximum_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 1000000000\n",
            directory="issue-1000000000",
        )
        with self.assertRaisesRegex(ValueError, "positive integer up to"):
            validate_request(path)

    def test_extra_key_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\nrepo: attacker/repo\n"
        )
        with self.assertRaisesRegex(ValueError, "wrong keys"):
            validate_request(path)

    # --- Verzeichnisname ---

    def test_directory_with_wrong_issue_prefix_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            directory="issue-17574-rtl-layout",
        )
        with self.assertRaisesRegex(
            ValueError,
            r"issue-17574-rtl-layout.*issue 17574.*issue 17573",
        ):
            validate_request(path)

    def test_mismatched_directory_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            directory="issue-42",
        )
        with self.assertRaisesRegex(
            ValueError, r"issue-42.*issue 42.*issue 17573"
        ):
            validate_request(path)

    def test_directory_description_with_unsafe_characters_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            directory="issue-17573-rtl layout",
        )
        with self.assertRaisesRegex(ValueError, "must match"):
            validate_request(path)

    # --- Pfadstruktur ---

    def test_request_outside_requests_directory_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            parent="other",
        )
        with self.assertRaisesRegex(ValueError, "inside ai/requests"):
            validate_request(path)

    def test_request_without_ai_directory_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            parent="requests",
        )
        with self.assertRaisesRegex(ValueError, "inside ai/requests"):
            validate_request(path)

    def test_request_in_wrong_parent_of_requests_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            parent="docs/requests",
        )
        with self.assertRaisesRegex(ValueError, "inside ai/requests"):
            validate_request(path)

    def test_wrong_file_name_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n"
        )
        renamed = path.with_name("other.yml")
        path.rename(renamed)
        with self.assertRaisesRegex(ValueError, "named request.yml"):
            validate_request(renamed)

    # --- Härtung ---

    def test_yaml_anchor_and_alias_are_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: &p claude\nissue: 17573\nextra: *p\n"
        )
        with self.assertRaisesRegex(ValueError, "anchors and aliases"):
            validate_request(path)

    def test_symlinked_request_file_is_rejected(self):
        real = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            parent="elsewhere",
        )
        link_dir = Path(tempfile.mkdtemp()) / "ai" / "requests" / "issue-17573"
        link_dir.mkdir(parents=True)
        link = link_dir / "request.yml"
        try:
            os.symlink(real, link)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are not supported on this platform")
        with self.assertRaisesRegex(ValueError, "symbolic link"):
            validate_request(link)

    def test_oversized_file_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n" + "#" * 20_000
        )
        with self.assertRaisesRegex(ValueError, "16 KiB"):
            validate_request(path)

    def test_deeply_nested_yaml_is_rejected_cleanly(self):
        path = self.write_request("task: " + "[" * 5_000 + "]" * 5_000 + "\n")
        with self.assertRaisesRegex(ValueError, "cannot read valid YAML"):
            validate_request(path)

    def test_non_mapping_top_level_is_rejected(self):
        path = self.write_request("- task\n- provider\n")
        with self.assertRaisesRegex(ValueError, "must be a mapping"):
            validate_request(path)


if __name__ == "__main__":
    unittest.main()