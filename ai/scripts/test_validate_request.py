import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path, PurePosixPath

from validate_request import Request, main, validate_request


ISSUE_PATH = "ai/requests/issue-17573/analysis-001/request.yml"
PR_PATH = "ai/requests/pr-11067/review-001/request.yml"
SMOKE_PATH = "ai/requests/smoke-test/copilot/request.yml"
BRANCH_PATH = "ai/requests/branch-map-fix/review-001/request.yml"


class ValidateRequestTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def write(self, relative: str, text: str) -> str:
        file = self.root / relative
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")
        return relative

    def validate(self, relative: str, text: str) -> Request:
        return validate_request(self.write(relative, text), self.root)

    def assertInvalid(self, relative: str, text: str, message: str):
        with self.assertRaisesRegex(ValueError, message):
            self.validate(relative, text)

    def symlink(self, target: Path, link: Path):
        try:
            os.symlink(target, link, target_is_directory=target.is_dir())
        except (OSError, NotImplementedError):
            self.skipTest("symbolic links are not supported on this system")

    # Valid requests

    def test_issue_analysis_with_both_providers(self):
        for provider in ("claude", "copilot"):
            with self.subTest(provider=provider):
                request = self.validate(
                    ISSUE_PATH, f"task: analyze-issue\nprovider: {provider}\nissue: 17573\n"
                )
                self.assertEqual(
                    request,
                    Request(PurePosixPath(ISSUE_PATH), "analyze-issue", provider, 17573, "cgeo/cgeo"),
                )

    def test_descriptions_in_directory_names(self):
        request = self.validate(
            "ai/requests/issue-17573-map_crash/analysis-002-follow-up/request.yml",
            "task: analyze-issue\nprovider: claude\nissue: 17573\n",
        )
        self.assertEqual(request.number, 17573)

    def test_pr_review_with_both_providers(self):
        for provider in ("claude", "copilot"):
            with self.subTest(provider=provider):
                request = self.validate(PR_PATH, f"task: review-pr\nprovider: {provider}\npr: 11067\n")
                self.assertEqual(
                    request, Request(PurePosixPath(PR_PATH), "review-pr", provider, 11067, "cgeo/cgeo")
                )

    def test_smoke_test_without_issue(self):
        request = self.validate(SMOKE_PATH, "task: smoke-test\nprovider: copilot\n")
        self.assertEqual(request.number, None)
        self.assertEqual(request.outputs()["number"], "")

    def test_smoke_test_with_issue_and_repository(self):
        request = self.validate(
            "ai/requests/smoke-test/claude-issue-42/request.yml",
            "task: smoke-test\nprovider: claude\nissue: 42\nrepository: murggel/cgeo\n",
        )
        self.assertEqual((request.number, request.repository), (42, "murggel/cgeo"))

    def test_comments_are_allowed(self):
        request = self.validate(SMOKE_PATH, "# test\ntask: smoke-test  # inline\nprovider: claude\n")
        self.assertEqual(request.provider, "claude")

    def test_outputs(self):
        request = self.validate(PR_PATH, "task: review-pr\nprovider: claude\npr: 11067\n")
        self.assertEqual(
            request.outputs(),
            {
                "request_dir": "ai/requests/pr-11067/review-001",
                "task": "review-pr",
                "provider": "claude",
                "number": "11067",
                "repository": "cgeo/cgeo",
                "instructions": "",
                "branch": "",
                "base": "",
                "previous_report": "",
            },
        )

    def test_instructions_for_analysis_and_review(self):
        text = "instructions: |\n  Focus on the map.\n  Answer in German.\n"
        request = self.validate(ISSUE_PATH, "task: analyze-issue\nprovider: claude\nissue: 17573\n" + text)
        self.assertEqual(request.instructions, "Focus on the map.\nAnswer in German.")
        self.assertIn("Additional instructions: 35 characters", request.summary())
        request = self.validate(PR_PATH, "task: review-pr\nprovider: copilot\npr: 11067\n" + text)
        self.assertEqual(request.outputs()["instructions"], "Focus on the map.\nAnswer in German.")

    def test_review_branch(self):
        request = self.validate(
            BRANCH_PATH,
            "task: review-branch\nprovider: claude\nbranch: feature/issue-1-fix.map_2\nbase: release\n"
            "instructions: |\n  Focus on threading.\n",
        )
        self.assertEqual((request.number, request.repository), (None, "cgeo/cgeo"))
        self.assertEqual(request.outputs()["branch"], "feature/issue-1-fix.map_2")
        self.assertEqual(request.outputs()["base"], "release")
        self.assertEqual(request.outputs()["number"], "")
        self.assertIn("- Branch: feature/issue-1-fix.map_2 (base: cgeo/cgeo:release)", request.summary())

    def test_review_branch_keys(self):
        base = "task: review-branch\nprovider: copilot\n"
        self.assertInvalid(BRANCH_PATH, base + "branch: a\n", r"missing=\['base'\]")
        self.assertInvalid(BRANCH_PATH, base + "base: master\n", r"missing=\['branch'\]")
        self.assertInvalid(BRANCH_PATH, base + "branch: a\nbase: master\nissue: 1\n", r"unexpected=\['issue'\]")
        self.assertInvalid(BRANCH_PATH, base + "branch: a\nbase: develop\n", "base must be one of")
        self.assertInvalid(BRANCH_PATH, base + "branch: a\nbase: 1\n", "base must be one of")

    def test_branch_name_may_start_with_underscore(self):
        request = self.validate(
            BRANCH_PATH,
            "task: review-branch\nprovider: claude\nbranch: _draft/ai/improve-authorization\nbase: master\n",
        )
        self.assertEqual(request.branch, "_draft/ai/improve-authorization")

    def test_invalid_branch_names(self):
        for branch in ("-x", "a..b", "a//b", "a/.b", "a/", "a.", "a.lock", "a b", "a~1", "a:b",
                       "a@{1}", "'$(id)'", "12", "x" * 201, "[a]"):
            with self.subTest(branch=branch):
                self.assertInvalid(
                    BRANCH_PATH,
                    f"task: review-branch\nprovider: claude\nbranch: {branch}\nbase: master\n",
                    "branch must be a branch name",
                )

    def test_review_branch_directory_names(self):
        text = "task: review-branch\nprovider: claude\nbranch: a\nbase: master\n"
        self.assertEqual(self.validate("ai/requests/branch-a/review-002-second/request.yml", text).branch, "a")
        for path in ("ai/requests/branch/review-001/request.yml",
                     "ai/requests/pr-1/review-001/request.yml",
                     "ai/requests/branch-a/analysis-001/request.yml"):
            with self.subTest(path=path):
                self.assertInvalid(path, text, "must be stored as")

    def test_instructions_not_allowed_for_smoke_test(self):
        self.assertInvalid(SMOKE_PATH, "task: smoke-test\nprovider: claude\ninstructions: hi\n",
                           r"unexpected=\['instructions'\]")

    def test_invalid_instructions(self):
        base = "task: analyze-issue\nprovider: claude\nissue: 17573\n"
        cases = {
            "instructions: 5\n": "must be text",
            "instructions: [a, b]\n": "must be text",
            "instructions: '  '\n": "must not be empty",
            "instructions:\n": "must be text",
            f"instructions: {'x' * 4001}\n": "must not exceed 4000",
            'instructions: "a\\x07b"\n': "control characters",
        }
        for text, message in cases.items():
            with self.subTest(text=text[:30]):
                self.assertInvalid(ISSUE_PATH, base + text, message)

    # Previous report

    def test_previous_report_for_all_follow_up_tasks(self):
        cases = {
            "ai/requests/issue-17573/analysis-002/request.yml": "task: analyze-issue\nprovider: claude\nissue: 17573\n",
            "ai/requests/pr-11067/review-002/request.yml": "task: review-pr\nprovider: copilot\npr: 11067\n",
            "ai/requests/branch-map-fix/review-002/request.yml":
                "task: review-branch\nprovider: claude\nbranch: a\nbase: master\n",
        }
        for relative, text in cases.items():
            with self.subTest(path=relative):
                directory = PurePosixPath(relative).parent.parent
                expected = (directory / "first-001" / "report.md").as_posix()
                self.write(expected, "old report\n")
                request = self.validate(relative, text + "previous: first-001\n")
                self.assertEqual(request.previous_report, expected)
                self.assertEqual(request.outputs()["previous_report"], expected)
                self.assertIn(f"- Previous report: {expected}", request.summary())

    def test_previous_report_must_exist(self):
        self.assertInvalid(PR_PATH, "task: review-pr\nprovider: claude\npr: 11067\nprevious: review-000\n",
                           "does not exist in this commit")

    def test_invalid_previous(self):
        base = "task: review-pr\nprovider: claude\npr: 11067\n"
        for value in ("1", "../review-000", "a/b", "''", "[a]"):
            with self.subTest(value=value):
                self.assertInvalid(PR_PATH, base + f"previous: {value}\n", "previous must be the folder name")
        self.assertInvalid(PR_PATH, base + "previous: review-001\n", "must not name the request itself")

    def test_previous_not_allowed_for_smoke_test(self):
        self.assertInvalid(SMOKE_PATH, "task: smoke-test\nprovider: claude\nprevious: other\n",
                           r"unexpected=\['previous'\]")

    def test_symlinked_previous_report(self):
        real = self.root / "real.md"
        real.write_text("x", encoding="utf-8")
        link = self.root / "ai/requests/pr-11067/review-000/report.md"
        link.parent.mkdir(parents=True)
        self.symlink(real, link)
        self.assertInvalid(PR_PATH, "task: review-pr\nprovider: claude\npr: 11067\nprevious: review-000\n",
                           "must not be a symbolic link")

    # Task, provider and keys

    def test_unknown_task(self):
        self.assertInvalid(ISSUE_PATH, "task: fix-issue\nprovider: claude\nissue: 1\n", "task must be one of")

    def test_task_must_be_a_string(self):
        self.assertInvalid(ISSUE_PATH, "task: [analyze-issue]\nprovider: claude\nissue: 1\n", "task must be one of")

    def test_unknown_provider(self):
        self.assertInvalid(ISSUE_PATH, "task: analyze-issue\nprovider: gemini\nissue: 17573\n", "provider")

    def test_provider_is_case_sensitive(self):
        self.assertInvalid(ISSUE_PATH, "task: analyze-issue\nprovider: Claude\nissue: 17573\n", "provider")

    def test_missing_issue(self):
        self.assertInvalid(ISSUE_PATH, "task: analyze-issue\nprovider: claude\n", r"missing=\['issue'\]")

    def test_extra_key(self):
        self.assertInvalid(
            ISSUE_PATH, "task: analyze-issue\nprovider: claude\nissue: 17573\nmodel: x\n", r"unexpected=\['model'\]"
        )

    def test_repository_not_allowed_for_issue_analysis(self):
        self.assertInvalid(
            ISSUE_PATH,
            "task: analyze-issue\nprovider: claude\nissue: 17573\nrepository: cgeo/cgeo\n",
            r"unexpected=\['repository'\]",
        )

    def test_pr_key_not_allowed_for_issue_analysis(self):
        self.assertInvalid(ISSUE_PATH, "task: analyze-issue\nprovider: claude\nissue: 17573\npr: 1\n", "unexpected")

    def test_smoke_test_repository_requires_issue(self):
        self.assertInvalid(
            SMOKE_PATH, "task: smoke-test\nprovider: copilot\nrepository: cgeo/cgeo\n", "together with an issue"
        )

    def test_smoke_test_rejects_unapproved_repository(self):
        self.assertInvalid(
            SMOKE_PATH, "task: smoke-test\nprovider: copilot\nissue: 1\nrepository: other/cgeo\n", "repository must be"
        )

    # Numbers

    def test_invalid_numbers(self):
        for value in ("true", "'17573'", "0", "-1", "1.5", "1000000000", "null"):
            with self.subTest(value=value):
                self.assertInvalid(
                    "ai/requests/issue-1/analysis-001/request.yml",
                    f"task: analyze-issue\nprovider: claude\nissue: {value}\n",
                    "issue must be a positive integer",
                )

    def test_invalid_pr_number(self):
        self.assertInvalid(PR_PATH, "task: review-pr\nprovider: claude\npr: yes\n", "pr must be a positive integer")

    def test_issue_number_must_match_directory(self):
        self.assertInvalid(ISSUE_PATH, "task: analyze-issue\nprovider: claude\nissue: 1\n", "refers to issue 17573")

    def test_review_pr_in_issue_directory(self):
        request = self.validate(
            "ai/requests/issue-17573-rtl/review-001/request.yml",
            "task: review-pr\nprovider: claude\npr: 11067\n",
        )
        self.assertEqual(request.number, 11067)

    def test_review_pr_directory_name(self):
        for relative in (
            "ai/requests/pr-11067/review-pr-001/request.yml",
            "ai/requests/issue-17573/review-pr-002-follow-up/request.yml",
        ):
            with self.subTest(path=relative):
                self.validate(relative, "task: review-pr\nprovider: claude\npr: 11067\n")

    def test_pr_number_must_match_directory(self):
        self.assertInvalid(PR_PATH, "task: review-pr\nprovider: claude\npr: 1\n", "refers to pr 11067")

    # Directory layout

    def test_wrong_directory_names(self):
        issue = "task: analyze-issue\nprovider: claude\nissue: 17573\n"
        cases = {
            "ai/requests/issue-17573/review-001/request.yml": issue,
            "ai/requests/issue-17573/analysis-1/request.yml": issue,
            "ai/requests/issue-17573/analysis-copilot/request.yml": issue,
            "ai/requests/issue-017573/analysis-001/request.yml": issue,
            "ai/requests/bug-17573/analysis-001/request.yml": issue,
            "ai/requests/issue-11067/analysis-001/request.yml":
                "task: review-pr\nprovider: claude\npr: 11067\n",
            "ai/requests/smoke-test-copilot/run/request.yml": "task: smoke-test\nprovider: copilot\n",
        }
        for relative, text in cases.items():
            with self.subTest(path=relative):
                self.assertInvalid(relative, text, "requests must be stored as")

    def test_wrong_depth_or_location(self):
        text = "task: smoke-test\nprovider: copilot\n"
        for relative in (
            "ai/requests/smoke-test-copilot/request.yml",
            "ai/requests/smoke-test/a/b/request.yml",
            "requests/smoke-test/copilot/request.yml",
            "other/requests/smoke-test/copilot/request.yml",
            "ai/requests/smoke-test/copilot/request.yaml",
            "ai/requests/smoke-test/../smoke-test/request.yml",
            "ai/requests/smoke-test/a.b/request.yml",
            "ai/requests/issue-17573/analysis-001-a.b/request.yml",
            "ai/requests/smoke-test/run 1/request.yml",
        ):
            with self.subTest(path=relative):
                with self.assertRaisesRegex(ValueError, "ai/requests/<subject>/<request-id>/request.yml"):
                    validate_request(relative, self.root)

    def test_missing_file(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            validate_request(SMOKE_PATH, self.root)

    # YAML strictness

    def test_duplicate_key(self):
        self.assertInvalid(SMOKE_PATH, "task: smoke-test\nprovider: copilot\nprovider: claude\n", "duplicate key")

    def test_anchor_and_alias(self):
        self.assertInvalid(SMOKE_PATH, "task: &t smoke-test\nprovider: copilot\nx: *t\n", "anchors and aliases")

    def test_non_string_key(self):
        self.assertInvalid(SMOKE_PATH, "task: smoke-test\nprovider: copilot\n1: x\n", "keys must be strings")

    def test_non_mapping_top_level(self):
        self.assertInvalid(SMOKE_PATH, "- task: smoke-test\n", "must be a mapping")

    def test_invalid_yaml(self):
        self.assertInvalid(SMOKE_PATH, "task: [smoke-test\n", "cannot read valid YAML")

    def test_deeply_nested_yaml(self):
        self.assertInvalid(SMOKE_PATH, "[" * 5_000 + "]" * 5_000 + "\n", "cannot read valid YAML|must be a mapping")

    def test_oversized_file(self):
        text = "task: smoke-test\nprovider: copilot\n" + "#" * 17_000 + "\n"
        self.assertInvalid(SMOKE_PATH, text, "must not exceed 16 KiB")

    # Symbolic links

    def test_symlinked_request_file(self):
        real = self.root / "real.yml"
        real.write_text("task: smoke-test\nprovider: copilot\n", encoding="utf-8")
        link = self.root / SMOKE_PATH
        link.parent.mkdir(parents=True)
        self.symlink(real, link)
        with self.assertRaisesRegex(ValueError, "must not be a symbolic link"):
            validate_request(SMOKE_PATH, self.root)

    def test_symlinked_directory(self):
        real = self.root / "elsewhere" / "copilot"
        real.mkdir(parents=True)
        (real / "request.yml").write_text("task: smoke-test\nprovider: copilot\n", encoding="utf-8")
        (self.root / "ai" / "requests").mkdir(parents=True)
        self.symlink(real.parent, self.root / "ai" / "requests" / "smoke-test")
        with self.assertRaisesRegex(ValueError, "'ai/requests/smoke-test' must not be a symbolic link"):
            validate_request(SMOKE_PATH, self.root)

    # Command line

    def test_main_writes_github_output(self):
        self.write(SMOKE_PATH, "task: smoke-test\nprovider: claude\nissue: 18739\n")
        output = self.root / "github-output"
        cwd = os.getcwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)
        with redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(main([SMOKE_PATH, "--github-output", str(output)]), 0)
        self.assertIn("- Issue: cgeo/cgeo#18739", stdout.getvalue())
        self.assertEqual(
            output.read_text(encoding="utf-8"),
            "request_dir=ai/requests/smoke-test/copilot\ntask=smoke-test\nprovider=claude\n"
            "number=18739\nrepository=cgeo/cgeo\ninstructions=\nbranch=\nbase=\nprevious_report=\n",
        )

    def test_main_writes_multiline_instructions(self):
        self.write(ISSUE_PATH, "task: analyze-issue\nprovider: claude\nissue: 17573\n"
                               "instructions: |\n  line one\n  line two\n")
        output = self.root / "github-output"
        cwd = os.getcwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main([ISSUE_PATH, "--github-output", str(output)]), 0)
        lines = output.read_text(encoding="utf-8").splitlines()
        start = next(i for i, line in enumerate(lines) if line.startswith("instructions<<"))
        delimiter = lines[start].split("<<", 1)[1]
        self.assertRegex(delimiter, "^EOF_[0-9a-f]{32}$")
        self.assertEqual(lines[start + 1:start + 4], ["line one", "line two", delimiter])
        self.assertEqual(lines[start + 4:], ["branch=", "base=", "previous_report="])

    def test_main_rejects_invalid_request(self):
        self.write(SMOKE_PATH, "task: smoke-test\n")
        cwd = os.getcwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)
        with redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(main([SMOKE_PATH]), 1)
        self.assertIn("Invalid request: provider", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
