import tempfile
import unittest
from pathlib import Path

from validate_request import validate_request


class ValidateRequestTest(unittest.TestCase):
    def write_request(self, text: str, directory: str = "issue-17573") -> Path:
        root = Path(tempfile.mkdtemp()) / directory
        root.mkdir()
        request = root / "request.yml"
        request.write_text(text, encoding="utf-8")
        return request

    def test_valid_claude_request(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n"
        )
        self.assertEqual(validate_request(path), ("analyze-issue", "claude", 17573))

    def test_valid_copilot_request(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: copilot\nissue: 17573\n"
        )
        self.assertEqual(validate_request(path), ("analyze-issue", "copilot", 17573))

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

    def test_extra_key_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\nrepo: attacker/repo\n"
        )
        with self.assertRaisesRegex(ValueError, "wrong keys"):
            validate_request(path)

    def test_mismatched_directory_is_rejected(self):
        path = self.write_request(
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            directory="issue-42",
        )
        with self.assertRaisesRegex(ValueError, "directory"):
            validate_request(path)


if __name__ == "__main__":
    unittest.main()
