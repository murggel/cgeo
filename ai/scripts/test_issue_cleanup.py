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
        self.index = root / "ai" / "issues" / "cleanup.md"

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
                if line.startswith("| [2026")]
        self.assertEqual(3, len(rows))
        self.assertTrue(rows[0].startswith(
            "| [2026-11-21 (2)](../requests/cleanup/2026-11-21/report-2.md) | copilot | 2 | 0 | 0 | 1 | 1 |"))
        self.assertIn("[#13](https://github.com/cgeo/cgeo/issues/13) waiting", rows[0])
        self.assertTrue(rows[1].startswith("| [2026-11-21](../requests/cleanup/2026-11-21/report.md) |"))
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
        text = self.index.read_text(encoding="utf-8")
        self.assertTrue(text.endswith("|---|---|---|---|---|---|---|---|\n"))
        self.assertIn("### Probably fixed (0)\n\nNone.", text)

    def snapshot(self, *entries: str) -> Path:
        directory = self.index.parent
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "issues.md").write_text("# Open issues\n" + "".join(e + "\n" for e in entries),
                                             encoding="utf-8")
        (directory / "snapshot.json").write_text('{"created_at": "2026-12-01T08:00:00Z"}', encoding="utf-8")
        return directory

    def test_status_tables_latest_result_and_closed_left_out(self):
        self.write("2026-11-20", "report.md", report("claude", "#11 fixed\n#12 fixed\n#13 waiting\n#15 fixed\n"))
        self.write("2026-11-21", "report.md", report("copilot", "#12 keep-open\n#14 duplicate\n#13 obsolete\n"))
        snapshot = self.snapshot(
            "#11 | labels: Bug | created: 2020-01-01 | updated: 2020-01-02 | title: Crash [map] | x | summary: s",
            "#12 | labels: | title: Twelve | summary: s",
            "#13 | labels: | title: Thirteen | summary: s",
            "#14 | labels: | title: Fourteen | summary: s")
        issue_cleanup.write_index(self.requests, self.index, snapshot)
        text = self.index.read_text(encoding="utf-8")
        self.assertLess(text.index("## Issues that can probably be closed"), text.index("## Reports"))
        self.assertIn("Left out: 1 issues that are no longer open in the issue snapshot of 2026-12-01.", text)
        fixed = text[text.index("### Probably fixed (1)"):text.index("### Duplicates (1)")]
        self.assertIn("| [#11](https://github.com/cgeo/cgeo/issues/11) | Crash \\[map\\] | "
                      "[2026-11-20](../requests/cleanup/2026-11-20/report.md) |", fixed)
        self.assertNotIn("#12", fixed)
        self.assertNotIn("#15", fixed)
        self.assertIn("### No longer applicable (1)", text)
        self.assertIn("| [#13](https://github.com/cgeo/cgeo/issues/13) | Thirteen | [2026-11-21]", text)
        self.assertIn("### Waiting for information (0)\n\nNone.", text)

    def test_status_without_snapshot_keeps_all(self):
        self.write("2026-11-20", "report.md", report("claude", "#15 fixed\n"))
        issue_cleanup.write_index(self.requests, self.index, self.index.parent / "missing")
        self.assertIn("| [#15](https://github.com/cgeo/cgeo/issues/15) | – | [2026-11-20]",
                      self.index.read_text(encoding="utf-8"))

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
