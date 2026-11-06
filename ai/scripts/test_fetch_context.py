import io
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import fetch_context
from fetch_context import ContextError, fetch_all, github_fetch, issue_context, main, pr_context


class FakeApi:
    """Serves canned responses; list endpoints are split into pages of PER_PAGE."""

    def __init__(self, objects=None, lists=None):
        self.objects = objects or {}
        self.lists = lists or {}
        self.requested = []

    def __call__(self, path):
        self.requested.append(path)
        base, _, query = path.partition("?")
        if not query:
            return self.objects[base]
        params = dict(item.split("=") for item in query.split("&"))
        size, page = int(params["per_page"]), int(params["page"])
        return self.lists.get(base, [])[(page - 1) * size:page * size]


def comment(login, body, created="2026-01-01"):
    return {"user": {"login": login}, "body": body, "created_at": created}


ISSUE = {
    "title": "Map crashes",
    "html_url": "https://github.com/cgeo/cgeo/issues/1",
    "state": "open",
    "user": {"login": "reporter"},
    "labels": [{"name": "Bug"}, {"name": "Map"}],
    "body": "Steps to reproduce",
}


class FetchAllTest(unittest.TestCase):
    def test_reads_all_pages(self):
        api = FakeApi(lists={"/x": [{"n": i} for i in range(250)]})
        self.assertEqual(len(fetch_all(api, "/x")), 250)
        self.assertEqual(len(api.requested), 3)

    def test_stops_after_exactly_full_page(self):
        api = FakeApi(lists={"/x": [{"n": i} for i in range(100)]})
        self.assertEqual(len(fetch_all(api, "/x")), 100)
        self.assertEqual(len(api.requested), 2)

    def test_refuses_to_truncate(self):
        api = FakeApi(lists={"/x": [{}] * (fetch_context.MAX_PAGES * fetch_context.PER_PAGE)})
        with self.assertRaisesRegex(ContextError, "refusing to truncate"):
            fetch_all(api, "/x")

    def test_rejects_non_list(self):
        with self.assertRaisesRegex(ContextError, "expected a list"):
            fetch_all(lambda path: {"message": "x"}, "/x")


class IssueContextTest(unittest.TestCase):
    def api(self, comments):
        return FakeApi(
            objects={"/repos/cgeo/cgeo/issues/1": ISSUE},
            lists={"/repos/cgeo/cgeo/issues/1/comments": comments},
        )

    def test_issue_with_all_comments(self):
        comments = [comment(f"user{i}", f"text {i}") for i in range(150)]
        text = issue_context(self.api(comments), "cgeo/cgeo", 1, with_comments=True)
        self.assertIn("# Issue cgeo/cgeo#1: Map crashes", text)
        self.assertIn("- Labels: Bug, Map", text)
        self.assertIn("Steps to reproduce", text)
        self.assertIn("### Comment 150 by user149", text)
        self.assertIn("untrusted user-provided content", text)

    def test_issue_without_comments(self):
        api = self.api([comment("a", "b")])
        text = issue_context(api, "cgeo/cgeo", 1, with_comments=False)
        self.assertNotIn("Discussion", text)
        self.assertEqual(api.requested, ["/repos/cgeo/cgeo/issues/1"])

    def test_empty_body_and_missing_user(self):
        api = FakeApi(
            objects={"/repos/cgeo/cgeo/issues/1": {"title": "t", "body": None, "user": None}},
            lists={"/repos/cgeo/cgeo/issues/1/comments": [{"body": ""}]},
        )
        text = issue_context(api, "cgeo/cgeo", 1, with_comments=True)
        self.assertIn("_No description provided._", text)
        self.assertIn("### Comment 1 by unknown", text)
        self.assertIn("_Empty comment._", text)

    def test_pull_request_is_rejected(self):
        api = FakeApi(objects={"/repos/cgeo/cgeo/issues/1": {**ISSUE, "pull_request": {}}})
        with self.assertRaisesRegex(ContextError, "is a pull request"):
            issue_context(api, "cgeo/cgeo", 1, with_comments=True)


class PrContextTest(unittest.TestCase):
    def test_pr_context_contains_all_parts(self):
        root = "/repos/cgeo/cgeo/pulls/7"
        api = FakeApi(
            objects={
                root: {
                    "title": "Fix map",
                    "state": "open",
                    "user": {"login": "author"},
                    "base": {"ref": "master", "sha": "b" * 40},
                    "head": {"sha": "h" * 40},
                    "body": "Fixes #1",
                }
            },
            lists={
                f"{root}/files": [
                    {"filename": f"src/F{i}.java", "status": "modified", "additions": 1,
                     "deletions": 2, "patch": f"@@ patch {i}"}
                    for i in range(120)
                ] + [{"filename": "big.bin", "status": "added"}],
                f"{root}/reviews": [{"user": {"login": "rev"}, "state": "APPROVED", "body": ""}],
                f"{root}/comments": [{"user": {"login": "rev"}, "path": "src/F1.java",
                                      "line": 12, "body": "nit"}],
                "/repos/cgeo/cgeo/issues/7/comments": [comment("author", "thanks")],
            },
        )
        text = pr_context(api, "cgeo/cgeo", 7)
        self.assertIn("# Pull request cgeo/cgeo#7: Fix map", text)
        self.assertIn("- Changed files: 121", text)
        self.assertIn("@@ patch 119", text)
        self.assertIn("GitHub provides no patch for this file", text)
        self.assertIn("### Review by rev (APPROVED", text)
        self.assertIn("_No review text._", text)
        self.assertIn("### rev on src/F1.java:12", text)
        self.assertIn("thanks", text)


class GithubFetchTest(unittest.TestCase):
    def test_http_error_is_reported(self):
        error = urllib.error.HTTPError(
            "https://api.github.com/x", 404, "Not Found", {}, io.BytesIO(b'{"message":"Not Found"}')
        )
        self.addCleanup(error.close)
        with mock.patch("urllib.request.urlopen", side_effect=error):
            with self.assertRaisesRegex(ContextError, "HTTP 404 .*Not Found"):
                github_fetch("token")("/x")

    def test_network_error_is_reported(self):
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("offline")):
            with self.assertRaisesRegex(ContextError, "request failed"):
                github_fetch(None)("/x")

    def test_token_is_sent(self):
        response = mock.MagicMock()
        response.__enter__.return_value = io.BytesIO(b"[]")
        with mock.patch("urllib.request.urlopen", return_value=response) as urlopen:
            self.assertEqual(github_fetch("secret")("/x"), [])
        self.assertEqual(urlopen.call_args.args[0].get_header("Authorization"), "Bearer secret")


class MainTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.output = Path(temp.name) / "ctx" / "issue.md"
        self.api = FakeApi(
            objects={"/repos/murggel/cgeo/issues/3": ISSUE},
            lists={"/repos/murggel/cgeo/issues/3/comments": []},
        )

    def run_main(self, *args):
        with redirect_stderr(io.StringIO()) as stderr, redirect_stdout(io.StringIO()):
            code = main(list(args), fetch=self.api)
        return code, stderr.getvalue()

    def test_writes_output(self):
        code, _ = self.run_main("issue", "--repository", "murggel/cgeo", "--number", "3",
                                "--output", str(self.output))
        self.assertEqual(code, 0)
        self.assertIn("Map crashes", self.output.read_text(encoding="utf-8"))

    def test_oversized_context_fails_without_output(self):
        self.api.objects["/repos/murggel/cgeo/issues/3"] = {**ISSUE, "body": "x" * (512 * 1024)}
        code, stderr = self.run_main("issue", "--repository", "murggel/cgeo", "--number", "3",
                                     "--output", str(self.output))
        self.assertEqual(code, 1)
        self.assertIn("exceeds the 512 KiB limit", stderr)
        self.assertFalse(self.output.exists())

    def test_invalid_repository(self):
        code, stderr = self.run_main("issue", "--repository", "../x", "--number", "3",
                                     "--output", str(self.output))
        self.assertEqual(code, 1)
        self.assertIn("invalid repository", stderr)


if __name__ == "__main__":
    unittest.main()
