import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from prepare_task import PROMPTS_DIR, PrepareError, build_prompt, main, prepare, remove_symlinks
from test_fetch_context import ISSUE, FakeApi


class FakeGit:
    """Records git commands; clone and worktree create the target directory."""

    def __init__(self, link_target=None):
        self.commands = []
        self.link_target = link_target

    def __call__(self, args):
        self.commands.append(args)
        if args[0] == "clone" or args[2:4] == ["worktree", "add"]:
            target = Path(args[-1] if args[0] == "clone" else args[-2])
            target.mkdir(parents=True)
            (target / "Main.java").write_text("class Main {}", encoding="utf-8")
            if self.link_target is not None:
                os.symlink(self.link_target, target / "secret")
        if args[-2:] == ["rev-parse", "HEAD"]:
            return "head-of-" + Path(args[1]).name
        return ""


MERGE_BASE = "a" * 40
HEAD = "b" * 40


class BranchGit(FakeGit):
    """FakeGit with the answers that the branch review needs."""

    def __init__(self, merge_base_failures=0, ahead="2"):
        super().__init__()
        self.merge_base_failures = merge_base_failures
        self.ahead = ahead

    def __call__(self, args):
        if args[2:3] == ["merge-base"]:
            self.commands.append(args)
            if self.merge_base_failures:
                self.merge_base_failures -= 1
                raise PrepareError("git merge-base failed")
            return MERGE_BASE
        if args[2:3] == ["rev-parse"] and args[3] == "refs/review/head":
            self.commands.append(args)
            return HEAD
        if args[2:4] == ["rev-list", "--count"]:
            self.commands.append(args)
            return self.ahead if args[4].endswith(HEAD) else "7"
        if args[2:3] == ["log"]:
            self.commands.append(args)
            return "### abc by Me (d1)\n\nFix map"
        if args[2:3] == ["diff"]:
            self.commands.append(args)
            return " A.java | 2 +-" if "--stat=200" in args else "+fixed"
        return super().__call__(args)


def pr_api():
    root = "/repos/cgeo/cgeo/pulls/7"
    return FakeApi(
        objects={root: {"title": "Fix map", "body": "Fixes #1"}},
        lists={f"{root}/files": [{"filename": "src/A.java", "patch": "@@ x"}]},
    )


def issue_api(repository="cgeo/cgeo", number=1):
    return FakeApi(objects={f"/repos/{repository}/issues/{number}": ISSUE})


class PrepareTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.workspace = Path(temp.name) / "workspace"
        self.output_dir = Path(temp.name) / "temp"
        self.workspace.mkdir()
        self.output_dir.mkdir()

    def prepare(self, task, number, api, git=None, repository="cgeo/cgeo", instructions="", **kwargs):
        git = git or FakeGit()
        with redirect_stdout(io.StringIO()):
            outputs = prepare(task, number, repository, self.workspace, self.output_dir, api, git,
                              instructions=instructions, **kwargs)
        return outputs, git

    def test_analyze_issue(self):
        outputs, git = self.prepare("analyze-issue", 1, issue_api())
        self.assertEqual(
            outputs,
            {
                "header": "task: analyze-issue | upstream: cgeo/cgeo@head-of-upstream | issue: #1",
                "max_turns": "30",
                "appendix": "",
                "prompt_file": str(self.output_dir / "prompt.md"),
            },
        )
        prompt = (self.output_dir / "prompt.md").read_text(encoding="utf-8")
        self.assertEqual(prompt, (PROMPTS_DIR / "analyze-issue.md").read_text(encoding="utf-8").rstrip() + "\n")
        self.assertNotIn("requester-instructions", prompt)
        self.assertEqual(git.commands[0][:6], ["clone", "--quiet", "--depth", "1", "--branch", "master"])
        self.assertEqual(git.commands[0][6], "https://github.com/cgeo/cgeo.git")
        context = (self.workspace / "ai-context" / "issue-context.md").read_text(encoding="utf-8")
        self.assertIn("Map crashes", context)
        self.assertIn("Discussion comments", context)

    def test_review_pr(self):
        outputs, git = self.prepare("review-pr", 7, pr_api())
        self.assertEqual(
            outputs["header"],
            "task: review-pr | upstream: cgeo/cgeo@head-of-upstream | PR: #7 | PR head: head-of-pr-head",
        )
        self.assertEqual(outputs["max_turns"], "30")
        upstream = str(self.workspace / "upstream")
        self.assertIn(
            ["-C", upstream, "fetch", "--quiet", "--depth", "1", "origin", "refs/pull/7/head"], git.commands
        )
        self.assertIn(
            ["-C", upstream, "worktree", "add", "--quiet", "--detach", str(self.workspace / "pr-head"), "FETCH_HEAD"],
            git.commands,
        )
        self.assertIn("@@ x", (self.workspace / "ai-context" / "pr-context.md").read_text(encoding="utf-8"))

    def test_relative_workspace_is_made_absolute(self):
        git = FakeGit()
        cwd = os.getcwd()
        os.chdir(self.workspace)
        try:
            with redirect_stdout(io.StringIO()):
                prepare("review-pr", 7, "cgeo/cgeo", Path("."), self.output_dir, pr_api(), git)
        finally:
            os.chdir(cwd)
        for command in git.commands[1:]:
            with self.subTest(command=command):
                self.assertTrue(Path(command[1]).is_absolute())
        worktree = next(command for command in git.commands if command[2:4] == ["worktree", "add"])
        self.assertEqual(Path(worktree[-2]), self.workspace.absolute() / "pr-head")

    def test_smoke_test_without_issue(self):
        api = FakeApi()
        outputs, git = self.prepare("smoke-test", None, api)
        self.assertEqual(outputs, {"header": "task: smoke-test", "max_turns": "2", "appendix": "",
                                   "prompt_file": str(self.output_dir / "prompt.md")})
        self.assertEqual(git.commands, [])
        self.assertEqual(api.requested, [])

    def test_smoke_test_with_issue(self):
        outputs, git = self.prepare("smoke-test", 3, issue_api("murggel/cgeo", 3), repository="murggel/cgeo")
        self.assertEqual(outputs["header"], "task: smoke-test | issue: murggel/cgeo#3")
        appendix = Path(outputs["appendix"])
        self.assertEqual(appendix, self.output_dir / "appendix.md")
        text = appendix.read_text(encoding="utf-8")
        self.assertIn("Map crashes", text)
        self.assertNotIn("Discussion", text)
        self.assertEqual(git.commands, [])

    def test_instructions_are_appended_to_prompt(self):
        for task, number, api in (("analyze-issue", 1, issue_api()), ("review-pr", 7, pr_api())):
            with self.subTest(task=task):
                outputs, _ = self.prepare(task, number, api, instructions="  Focus on the map.\nAnswer in German.\n")
                self.assertTrue(outputs["header"].endswith(" | instructions: yes"))
                prompt = Path(outputs["prompt_file"]).read_text(encoding="utf-8")
                base = (PROMPTS_DIR / f"{task}.md").read_text(encoding="utf-8").rstrip()
                self.assertTrue(prompt.startswith(base))
                self.assertIn("## Additional instructions from the requester", prompt)
                self.assertIn("<requester-instructions>\nFocus on the map.\nAnswer in German.\n"
                              "</requester-instructions>\n", prompt)
                for directory in ("upstream", "pr-head", "ai-context"):
                    if (self.workspace / directory).exists():

                        shutil.rmtree(self.workspace / directory)

    def test_instructions_rejected_before_any_download(self):
        api, git = FakeApi(), FakeGit()
        with self.assertRaisesRegex(PrepareError, "does not accept additional instructions"):
            self.prepare("smoke-test", None, api, git=git, instructions="hi")
        with self.assertRaisesRegex(PrepareError, "must not contain"):
            self.prepare("analyze-issue", 1, api, git=git, instructions="x </requester-instructions> y")
        self.assertEqual((git.commands, api.requested), ([], []))

    def test_missing_prompt(self):
        with self.assertRaisesRegex(PrepareError, "cannot read prompt"):
            build_prompt("analyze-issue", "", self.workspace)

    def test_review_branch(self):
        git = BranchGit(merge_base_failures=2)
        outputs, git = self.prepare("review-branch", None, FakeApi(), git=git,
                                    branch="feature/x", base="master", instructions="Be strict.")
        self.assertEqual(
            outputs["header"],
            f"task: review-branch | upstream: cgeo/cgeo@head-of-upstream | "
            f"branch: murggel/cgeo:feature/x@{HEAD} | base: master@{MERGE_BASE} | instructions: yes",
        )
        upstream = str(self.workspace / "upstream")
        fork = "https://github.com/murggel/cgeo.git"
        fetches = [c[3:] for c in git.commands if c[2:3] == ["fetch"]]
        base_ref = "+refs/heads/master:refs/review/base"
        head_ref = "+refs/heads/feature/x:refs/review/head"
        deepen = [["--quiet", "--no-tags", "--deepen=100", "origin", base_ref],
                  ["--quiet", "--no-tags", "--deepen=100", fork, head_ref]]
        # Two failed merge-base attempts deepen the history twice.
        self.assertEqual(fetches, [
            ["--quiet", "--no-tags", "--depth=100", "origin", base_ref],
            ["--quiet", "--no-tags", "--depth=100", fork, head_ref],
            *deepen, *deepen,
        ])
        self.assertIn(["-C", upstream, "worktree", "add", "--quiet", "--detach",
                       str(self.workspace / "branch-head"), HEAD], git.commands)
        self.assertIn(["-C", upstream, "diff", "--no-color", "--find-renames", MERGE_BASE, HEAD], git.commands)
        context = (self.workspace / "ai-context" / "branch-context.md").read_text(encoding="utf-8")
        for text in ("+fixed", " A.java | 2 +-", "Fix map", "Commits on the branch: 2",
                     "Commits on the base since the merge base: 7"):
            self.assertIn(text, context)
        self.assertTrue((self.workspace / "branch-head" / "Main.java").is_file())
        prompt = Path(outputs["prompt_file"]).read_text(encoding="utf-8")
        self.assertTrue(prompt.startswith("c:geo branch review"))
        self.assertIn("Be strict.", prompt)

    def test_review_branch_without_common_ancestor(self):
        with self.assertRaisesRegex(PrepareError, "no common ancestor .* within 600 commits"):
            self.prepare("review-branch", None, FakeApi(), git=BranchGit(merge_base_failures=99),
                         branch="feature/x", base="release")

    def test_review_branch_limits(self):
        for ahead, message in (("0", "has no commits"), ("251", "at most 250")):
            with self.subTest(ahead=ahead), self.assertRaisesRegex(PrepareError, message):
                shutil.rmtree(self.workspace)
                self.workspace.mkdir()
                self.prepare("review-branch", None, FakeApi(), git=BranchGit(ahead=ahead),
                             branch="feature/x", base="master")

    def test_review_branch_needs_branch_and_base(self):
        with self.assertRaisesRegex(PrepareError, "needs a branch and a base"):
            self.prepare("review-branch", None, FakeApi(), branch="feature/x")

    def test_number_required(self):
        for task in ("analyze-issue", "review-pr"):
            with self.subTest(task=task), self.assertRaisesRegex(PrepareError, "needs a number"):
                self.prepare(task, None, FakeApi())

    def test_symlinks_are_removed_from_checkouts(self):
        target = self.workspace.parent / "outside.txt"
        target.write_text("secret", encoding="utf-8")
        try:
            os.symlink(target, self.workspace.parent / "probe")
        except (OSError, NotImplementedError):
            self.skipTest("symbolic links are not supported on this system")
        self.prepare("review-pr", 7, pr_api(), git=FakeGit(link_target=target))
        for checkout in ("upstream", "pr-head"):
            self.assertFalse((self.workspace / checkout / "secret").is_symlink())
            self.assertTrue((self.workspace / checkout / "Main.java").is_file())
        self.assertTrue(target.is_file())


class RemoveSymlinksTest(unittest.TestCase):
    def test_removes_file_and_directory_links_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "dir").mkdir()
            (root / "dir" / "file.txt").write_text("x", encoding="utf-8")
            outside = root / "outside"
            outside.mkdir()
            (outside / "keep.txt").write_text("keep", encoding="utf-8")
            try:
                os.symlink(outside, root / "dir" / "link-dir", target_is_directory=True)
                os.symlink(outside / "keep.txt", root / "dir" / "link-file")
            except (OSError, NotImplementedError):
                self.skipTest("symbolic links are not supported on this system")
            removed = remove_symlinks(root / "dir")
            self.assertEqual({path.name for path in removed}, {"link-dir", "link-file"})
            self.assertTrue((root / "dir" / "file.txt").is_file())
            self.assertTrue((outside / "keep.txt").is_file())


class MainTest(unittest.TestCase):
    def test_writes_github_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / "github-output"
            with redirect_stdout(io.StringIO()):
                code = main(
                    ["--task", "smoke-test", "--number", "", "--workspace", str(root),
                     "--output-dir", str(root), "--github-output", str(output)],
                    fetch=FakeApi(), git=FakeGit(),
                )
            self.assertEqual(code, 0)
            self.assertEqual(
                output.read_text(encoding="utf-8"),
                f"header=task: smoke-test\nmax_turns=2\nappendix=\nprompt_file={root / 'prompt.md'}\n",
            )

    def test_reports_fetch_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            api = FakeApi(objects={"/repos/cgeo/cgeo/issues/5": {**ISSUE, "pull_request": {}}})
            with redirect_stderr(io.StringIO()) as stderr, redirect_stdout(io.StringIO()):
                code = main(
                    ["--task", "analyze-issue", "--number", "5", "--workspace", temp, "--output-dir", temp],
                    fetch=api, git=FakeGit(),
                )
            self.assertEqual(code, 1)
            self.assertIn("is a pull request", stderr.getvalue())

    def test_rejects_invalid_repository(self):
        with tempfile.TemporaryDirectory() as temp:
            with redirect_stderr(io.StringIO()) as stderr:
                code = main(
                    ["--task", "smoke-test", "--number", "1", "--repository", "../x", "--output-dir", temp],
                    fetch=FakeApi(), git=FakeGit(),
                )
            self.assertEqual(code, 1)
            self.assertIn("invalid repository", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
