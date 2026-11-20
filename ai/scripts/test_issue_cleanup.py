import os
import tempfile
import unittest
from pathlib import Path

import issue_cleanup


def report(provider: str, results: str) -> str:
    header = f"<!-- task: cleanup-issues | provider: {provider} | workflow: abc -->\n\nText.\n\n"
    return header + (f"```cleanup-result\n{results}```\n" if results else "")


class IndexTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.requests = root / "ai" / "requests" / "cleanup"
        self.index = root / "ai" / "issues" / "cleanup" / "index.md"

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name: str, file: str, text: str) -> None:
        folder = self.requests / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / file).write_text(text, encoding="utf-8")

    def test_rows_newest_first_with_batches(self):
        self.write("2026-11-20", "report.md", report("claude", "#10 keep-open\n#11 fixed\n"))
        self.write("2026-11-21", "report.md", report("copilot 1.0.105", "#12 duplicate\n"))
        self.write("2026-11-21", "report-2.md", report("copilot 1.0.105", "#13 waiting\n#14 obsolete\n"))
        self.write("2026-11-21", "request.yml", "task: cleanup-issues\n")
        issue_cleanup.write_index(self.requests, self.index)
        rows = [line for line in self.index.read_text(encoding="utf-8").splitlines()
                if line.startswith("| [")]
        self.assertEqual(3, len(rows))
        self.assertTrue(rows[0].startswith(
            "| [2026-11-21 (2)](../../requests/cleanup/2026-11-21/report-2.md) | copilot | 2 | 0 | 0 | 1 | 1 |"))
        self.assertIn("[#13](https://github.com/cgeo/cgeo/issues/13) waiting", rows[0])
        self.assertTrue(rows[1].startswith("| [2026-11-21](../../requests/cleanup/2026-11-21/report.md) |"))
        self.assertTrue(rows[2].startswith("| [2026-11-20]("))
        self.assertIn("| claude | 2 | 1 | 0 | 0 | 0 | [#11]", rows[2])
        self.assertNotIn("#10", rows[2])

    def test_report_without_result_block(self):
        self.write("2026-11-20", "report.md", report("claude", ""))
        issue_cleanup.write_index(self.requests, self.index)
        self.assertIn("| claude | – | – | – | – | – | no result block |",
                      self.index.read_text(encoding="utf-8"))

    def test_unknown_provider_and_other_files_ignored(self):
        self.write("2026-11-20", "report.md", report("other", "#1 keep-open\n"))
        self.write("2026-11-20", "notes.md", report("claude", "#2 fixed\n"))
        issue_cleanup.write_index(self.requests, self.index)
        text = self.index.read_text(encoding="utf-8")
        self.assertIn("| ? | 1 | 0 | 0 | 0 | 0 | – |", text)
        self.assertNotIn("#2", text)

    def test_no_reports(self):
        issue_cleanup.write_index(self.requests, self.index)
        self.assertTrue(self.index.read_text(encoding="utf-8").endswith("|---|---|---|---|---|---|---|---|\n"))

    @unittest.skipUnless(hasattr(os, "symlink"), "symbolic links not available")
    def test_symlinks_skipped_and_refused(self):
        self.write("2026-11-20", "report.md", report("claude", "#1 fixed\n"))
        outside = Path(self.tmp.name) / "outside.md"
        outside.write_text(report("claude", "#99 fixed\n"), encoding="utf-8")
        try:
            os.symlink(outside, self.requests / "2026-11-20" / "report-2.md")
            os.symlink(self.requests / "2026-11-20", self.requests / "2026-11-21")
        except OSError:
            self.skipTest("symbolic links not allowed")
        issue_cleanup.write_index(self.requests, self.index)
        text = self.index.read_text(encoding="utf-8")
        self.assertNotIn("#99", text)
        self.assertNotIn("2026-11-21", text)
        self.index.unlink()
        os.symlink(outside, self.index)
        with self.assertRaises(issue_cleanup.CleanupError):
            issue_cleanup.write_index(self.requests, self.index)


if __name__ == "__main__":
    unittest.main()
