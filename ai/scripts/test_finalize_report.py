import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from finalize_report import ReportError, build_report, find_secrets, main, read_claude_result


def claude_messages(result="Final report", subtype="success", is_error=False, num_turns=3):
    return [
        {"type": "system", "subtype": "init"},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "Let me look."}]}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": result}]}},
        {"type": "result", "subtype": subtype, "is_error": is_error, "result": result,
         "num_turns": num_turns},
    ]


class FinalizeReportTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.output = self.dir / "report.md"

    def write(self, name, content):
        path = self.dir / name
        path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
        return str(path)

    def run_main(self, *args, env=None):
        with mock.patch.dict(os.environ, env or {}), redirect_stderr(io.StringIO()) as stderr, \
                redirect_stdout(io.StringIO()):
            code = main([*args, "--output", str(self.output)])
        return code, stderr.getvalue()

    # Claude execution file

    def test_claude_uses_only_final_result(self):
        path = Path(self.write("exec.json", claude_messages("# Analysis\n\nDone.")))
        self.assertEqual(read_claude_result(path), ("# Analysis\n\nDone.", 3))

    def test_claude_max_turns_is_an_error(self):
        messages = claude_messages(subtype="error_max_turns", is_error=True)
        del messages[-1]["result"]
        with self.assertRaisesRegex(ReportError, "error_max_turns"):
            read_claude_result(Path(self.write("exec.json", messages)))

    def test_claude_without_result_message(self):
        with self.assertRaisesRegex(ReportError, "no final result"):
            read_claude_result(Path(self.write("exec.json", claude_messages()[:-1])))

    def test_claude_empty_result(self):
        with self.assertRaisesRegex(ReportError, "without producing"):
            read_claude_result(Path(self.write("exec.json", claude_messages(result="  "))))

    def test_claude_invalid_json(self):
        with self.assertRaisesRegex(ReportError, "cannot read"):
            read_claude_result(Path(self.write("exec.json", "{")))

    def test_claude_missing_file(self):
        with self.assertRaisesRegex(ReportError, "missing"):
            read_claude_result(self.dir / "missing.json")

    def test_main_marks_result_over_turn_limit(self):
        with redirect_stdout(io.StringIO()) as stdout, redirect_stderr(io.StringIO()):
            code = main([
                "--claude-execution-file", self.write("exec.json", claude_messages("Report", num_turns=18)),
                "--max-turns", "15", "--header", "provider: claude", "--output", str(self.output),
            ])
        self.assertEqual(code, 0)
        report = self.output.read_text(encoding="utf-8")
        self.assertTrue(report.startswith("<!-- provider: claude | status: exceeded-max-turns (18 of 15) -->\n\n"))
        self.assertIn("> **Note:** Claude needed 18 turns, more than the configured limit of 15.", report)
        self.assertTrue(report.endswith("\n\nReport\n"))
        self.assertIn("::warning::", stdout.getvalue())

    def test_main_within_turn_limit_is_unmarked(self):
        code, _ = self.run_main(
            "--claude-execution-file", self.write("exec.json", claude_messages("Report", num_turns=15)),
            "--max-turns", "15", "--header", "h",
        )
        self.assertEqual(code, 0)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "<!-- h -->\n\nReport\n")

    # Report building

    def test_build_report(self):
        self.assertEqual(
            build_report("provider: x", "\nBody\n", "Appendix\n"),
            "<!-- provider: x -->\n\nBody\n\n---\n\nAppendix\n",
        )
        self.assertEqual(build_report("h", "Body"), "<!-- h -->\n\nBody\n")

    def test_main_with_copilot_output_and_appendix(self):
        code, _ = self.run_main(
            "--copilot-output", self.write("out.md", "# Copilot smoke test\nStatus: successful\n"),
            "--append", self.write("issue.md", "## Issue\n\nText"),
            "--header", "provider: copilot",
        )
        self.assertEqual(code, 0)
        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            "<!-- provider: copilot -->\n\n# Copilot smoke test\nStatus: successful\n\n---\n\n## Issue\n\nText\n",
        )

    def test_main_with_claude_execution_file(self):
        code, _ = self.run_main(
            "--claude-execution-file", self.write("exec.json", claude_messages("Report")),
            "--header", "provider: claude",
        )
        self.assertEqual(code, 0)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "<!-- provider: claude -->\n\nReport\n")

    def test_main_empty_copilot_output(self):
        code, stderr = self.run_main("--copilot-output", self.write("out.md", "\n"), "--header", "h")
        self.assertEqual(code, 1)
        self.assertIn("without producing", stderr)
        self.assertFalse(self.output.exists())

    def test_main_rejects_oversized_report(self):
        code, stderr = self.run_main("--copilot-output", self.write("out.md", "x" * (512 * 1024)), "--header", "h")
        self.assertEqual(code, 1)
        self.assertIn("exceeds the 512 KiB limit", stderr)
        self.assertFalse(self.output.exists())

    # Secret scan

    def test_token_patterns(self):
        for token in (
            "sk-ant-oat01-abcdefghijklmnop",
            "sk-ant-api03-abcdefghijklmnop",
            "ghp_" + "a" * 36,
            "ghs_" + "A1" * 18,
            "github_pat_" + "a1_" * 20,
        ):
            with self.subTest(token=token):
                self.assertTrue(find_secrets(f"text {token} text", {}))

    def test_harmless_text_passes(self):
        text = "Use the GitHub token (ghp_...) and sk-ant- prefix as described in the README."
        self.assertEqual(find_secrets(text, {"EMPTY": "", "SHORT": "abc"}), [])

    def test_secret_value(self):
        self.assertEqual(find_secrets("x 1234567890abcdef x", {"MY_TOKEN": "1234567890abcdef"}), ["value of MY_TOKEN"])

    def test_main_refuses_report_with_secret_value(self):
        secret = "s3cr3t-value-without-known-prefix"
        code, stderr = self.run_main(
            "--copilot-output", self.write("out.md", f"leaked: {secret}"),
            "--header", "h", "--secret-env", "MY_TOKEN",
            env={"MY_TOKEN": secret},
        )
        self.assertEqual(code, 1)
        self.assertIn("value of MY_TOKEN", stderr)
        self.assertNotIn(secret, stderr)
        self.assertFalse(self.output.exists())

    def test_main_scans_appendix(self):
        code, stderr = self.run_main(
            "--copilot-output", self.write("out.md", "ok"),
            "--append", self.write("issue.md", "ghp_" + "b" * 36),
            "--header", "h",
        )
        self.assertEqual(code, 1)
        self.assertIn("GitHub token", stderr)


if __name__ == "__main__":
    unittest.main()
