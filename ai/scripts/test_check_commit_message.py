import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from check_commit_message import check, find_references, main


class CheckCommitMessageTest(unittest.TestCase):
    def run_main(self, argv):
        with redirect_stdout(io.StringIO()) as stdout, redirect_stderr(io.StringIO()) as stderr:
            code = main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def write(self, text: str) -> str:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "COMMIT_EDITMSG"
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_message_without_reference_is_accepted(self):
        for message in ("AI request: review-pr pr-18952",
                        "Add Claude analysis report for issue-12345",
                        "Add Copilot review report for branch fix/map-18947",
                        "Fix &#123; entity\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n"
                        "Claude-Session: https://claude.ai/code/session_01ABC",
                        "See https://github.com/cgeo/cgeo/blob/master/README.md"):
            with self.subTest(message=message):
                self.assertIsNone(check(message))

    def test_message_with_reference_is_rejected(self):
        for message, reference in (("AI request: review PR #18952", "#18952"),
                                   ("Review\n\nSee cgeo/cgeo#123 for details", "#123"),
                                   ("Fixes PR#42", "#42"),
                                   ("Relates to gh-77", "gh-77"),
                                   ("See https://github.com/cgeo/cgeo/issues/447", "issues/447"),
                                   ("See github.com/cgeo/cgeo/pull/18952", "pull/18952")):
            with self.subTest(message=message):
                self.assertIn(reference, check(message))

    def test_references_are_listed_once(self):
        self.assertEqual(find_references("#1 and #2, again #1"), ["#1", "#2"])

    def test_main_checks_messages(self):
        self.assertEqual(self.run_main(["AI request: review-pr pr-18952"])[:2], (0, "Commit message OK.\n"))
        code, _, stderr = self.run_main(["ok", "PR #1", "--", "-x #2"])
        self.assertEqual(code, 1)
        self.assertIn("Invalid commit message: 'PR #1' contains #1", stderr)
        self.assertIn("'-x #2' contains #2", stderr)

    def test_main_checks_message_file(self):
        ok = self.write("AI request: review-pr pr-18952\n\n# Please enter the commit message.\n"
                        "# ------------------------ >8 ------------------------\n"
                        "+ diff line with #18952\n")
        self.assertEqual(self.run_main(["--file", ok])[0], 0)
        bad = self.write("AI request: review PR #18952\n")
        self.assertEqual(self.run_main(["--file", bad])[0], 1)

    def test_main_reports_unreadable_file(self):
        code, _, stderr = self.run_main(["--file", str(Path(self.write("x")).parent / "missing")])
        self.assertEqual(code, 2)
        self.assertIn("Cannot read commit message", stderr)

    def test_main_needs_input(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            main([])


if __name__ == "__main__":
    unittest.main()
