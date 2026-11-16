import io
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import fix_history
from fetch_context import ContextError
from fix_history import Evidence, add_assignees, assignee_logins, link_fixes, parse_evidence, run_git


def report(evidence, results, comment='"Sorted by the search centre now.[fix-pr #447] Closing."'):
    return (
        "## Probably fixed\n\n"
        f"- [#447](https://github.com/cgeo/cgeo/issues/447) – sorting\n  - Closing comment: {comment}\n\n"
        f"```fix-evidence\n{evidence}```\n\n"
        f"```cleanup-result\n{results}```\n"
    )


class Api:
    """Answers /commits/<sha>/pulls; records the requests."""

    def __init__(self, pulls=None, fail=False):
        self.pulls = pulls if pulls is not None else []
        self.fail = fail
        self.paths = []

    def __call__(self, path):
        self.paths.append(path)
        if self.fail:
            raise ContextError("HTTP 403")
        return self.pulls


class FixHistoryTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.git("init", "--quiet", "--initial-branch=master")
        self.commit("src/Sort.java", "class Sort {}\n", "Initial version", "2011-01-01")
        self.commit("src/Sort.java", "class Sort { int TARGET_DISTANCE; }\n",
                    "fix #8981: sort by target (#11937)", "2021-10-26")
        # A later move must not hide the commit that added the code.
        (self.repo / "app").mkdir()
        self.git("mv", "src/Sort.java", "app/Sort.java")
        self.git("commit", "--quiet", "-m", "move files", env_date="2022-12-23")
        self.sha = self.git("log", "--format=%H", "-S", "TARGET_DISTANCE").split()[-1]

    def git(self, *args, env_date=None):
        env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.org", "GIT_COMMITTER_NAME": "t",
               "GIT_COMMITTER_EMAIL": "t@example.org", "PATH": "/usr/bin:/bin:/usr/local/bin"}
        if env_date:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"{env_date}T12:00:00"
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True,
                              text=True, env=env).stdout.strip()

    def commit(self, path, content, message, day):
        file = self.repo / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")
        self.git("add", path)
        self.git("commit", "--quiet", "-m", message, env_date=day)

    def link(self, text, api=None, created=None, checked=frozenset({447})):
        with redirect_stdout(io.StringIO()):
            return link_fixes(text, run_git(self.repo), api or Api(), "cgeo/cgeo",
                              created if created is not None else {447: "2011-09-14"}, set(checked))

    def test_names_pull_request_from_api(self):
        api = Api([{"number": 11937, "title": "Sort by `target` [x]", "merged_at": "2021-10-27T10:00:00Z"},
                   {"number": 9, "title": "unmerged", "merged_at": None}])
        text, findings = self.link(report("#447 app/Sort.java TARGET_DISTANCE\n", "#447 fixed\n"), api)
        self.assertEqual(api.paths, [f"/repos/cgeo/cgeo/commits/{self.sha}/pulls"])
        # The closing comment never names the PR; the maintainer checks it first.
        self.assertIn('centre now. Closing."', text)
        self.assertIn("[PR #11937](https://github.com/cgeo/cgeo/pull/11937) "
                      '"Sort by \\`target\\` \\[x\\]", merged 2021-10-27', text)
        self.assertIn(f"commit [{self.sha[:10]}]", text)
        self.assertIn("of 2021-10-26", text)
        self.assertNotIn("fix-evidence", text)
        self.assertIn("```cleanup-result\n#447 fixed\n```", text)
        self.assertEqual(findings[0].pr, 11937)

    def test_squash_subject_when_api_fails(self):
        text, _ = self.link(report("#447 app/Sort.java TARGET_DISTANCE\n", "#447 fixed\n"), Api(fail=True))
        self.assertIn("[PR #11937](https://github.com/cgeo/cgeo/pull/11937)", text)
        self.assertIn('"fix \\#8981: sort by target", commit', text)

    def test_commit_older_than_issue_is_not_in_comment(self):
        text, _ = self.link(report("#447 app/Sort.java TARGET_DISTANCE\n", "#447 fixed\n"),
                            created={447: "2022-01-01"})
        self.assertIn('centre now. Closing."', text)
        self.assertIn("older than the issue", text)

    def test_unusable_evidence(self):
        cases = {
            "app/Missing.java TARGET_DISTANCE": "file does not exist",
            "app/Sort.java NOT_IN_FILE": "search text is not in the current file",
            "../etc/passwd TARGET_DISTANCE": "invalid file name",
            "-p TARGET_DISTANCE": "invalid file name",
            "app/Sort.java abc": "search text must be",
        }
        for evidence, note in cases.items():
            with self.subTest(evidence=evidence):
                text, findings = self.link(report(f"#447 {evidence}\n", "#447 fixed\n"))
                self.assertIn(note, findings[0].note)
                self.assertIn("nothing found for", text)
                self.assertIn('centre now. Closing."', text)

    def test_only_checked_fixed_issues(self):
        evidence = "#447 app/Sort.java TARGET_DISTANCE\n#448 app/Sort.java TARGET_DISTANCE\n#5 x y\n"
        results = "#447 keep-open\n#448 fixed\n"
        text, findings = self.link(report(evidence, results), checked={447})
        self.assertEqual(findings, [])
        self.assertNotIn("fix-evidence", text)
        self.assertNotIn("Pull requests of the probably fixed issues", text)
        self.assertNotIn("[fix-pr", text)

    def test_no_evidence_block_removes_placeholders(self):
        text = "Closing comment: \"Done.[fix-pr #447] Bye.\"\n\n```cleanup-result\n#447 fixed\n```\n"
        linked, _ = self.link(text)
        self.assertIn('"Done. Bye."', linked)

    def test_parse_evidence(self):
        text = "  ```fix-evidence\n  #447 a/B.java `x(y) z`\n  #447 a/C.java other\nnot a line\n  ```\n"
        self.assertEqual(parse_evidence(text, {447}), [Evidence(447, "a/B.java", "x(y) z")])

    def test_main_writes_report(self):
        path = self.repo / "report.md"
        path.write_text(report("#447 app/Sort.java TARGET_DISTANCE\n", "#447 fixed\n"), encoding="utf-8")
        with redirect_stdout(io.StringIO()) as out:
            code = fix_history.main(["--report", str(path), "--upstream", str(self.repo),
                                     "--issues", str(self.repo / "missing"), "--checked", "447"],
                                    fetch=Api(fail=True))
        self.assertEqual(code, 0)
        self.assertIn("1 with a pull request", out.getvalue())
        self.assertIn("[PR #11937]", path.read_text(encoding="utf-8"))


class AssigneeTest(unittest.TestCase):
    REPORT = (
        "## Probably fixed\n\n"
        "- [#447](https://github.com/cgeo/cgeo/issues/447) – sorting  \n  - Closing comment: \"Done.\"\n"
        "- [#448](https://github.com/cgeo/cgeo/issues/448) – map\n\n"
        "## Duplicates\n\n- **[#449](https://github.com/cgeo/cgeo/issues/449)** – list\n\n"
        "## Keep open\n\n[#450](https://github.com/cgeo/cgeo/issues/450), "
        "[#451](https://github.com/cgeo/cgeo/issues/451)\n\n"
        "- [#451](https://github.com/cgeo/cgeo/issues/451) – kept\n\n"
        "```cleanup-result\n#447 fixed\n#448 fixed\n#449 duplicate\n#450 keep-open\n#451 keep-open\n```\n"
    )

    def test_only_issues_to_close(self):
        assignees = {447: ["moving-bits"], 448: [], 449: ["a", "b"], 450: ["x"], 451: ["y"]}
        result = add_assignees(self.REPORT, "cgeo/cgeo", assignees, {447, 448, 449, 450, 451})
        self.assertIn("issues/447) – sorting — assigned: @moving-bits\n", result)
        self.assertIn("issues/448) – map — unassigned\n", result)
        self.assertIn("issues/449)** – list — assigned: @a, @b\n", result)
        self.assertNotIn("@x", result)
        self.assertNotIn("@y", result)
        self.assertEqual(result.count("assigned"), 3)

    def test_unknown_issue_or_unchecked_stays(self):
        result = add_assignees(self.REPORT, "cgeo/cgeo", {448: ["z"]}, {447})
        self.assertEqual(result, self.REPORT)

    def test_logins_from_snapshot(self):
        entries = [{"number": 1, "assignees": "a, b-c, bad name, "}, {"number": 2, "assignees": ""},
                   {"number": 3}]
        self.assertEqual(assignee_logins(entries), {1: ["a", "b-c"], 2: []})


if __name__ == "__main__":
    unittest.main()
