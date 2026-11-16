import unittest

from issue_snapshot import summarize


class SummarizeTest(unittest.TestCase):
    def issue(self, **extra):
        return {"number": 447, "title": "Sorting", "body": "Sort by target", "labels": [{"name": "Bug"}],
                "created_at": "2011-09-14T10:00:00Z", "updated_at": "2026-01-02T10:00:00Z", "comments": 3,
                **extra}

    def test_assignees(self):
        line = summarize(self.issue(assignees=[{"login": "moving-bits"}, {"login": "bad login"}, "x",
                                               {"login": "eddiemuc"}]))
        self.assertIn(" | comments: 3 | assignees: moving-bits, eddiemuc | title: Sorting", line)

    def test_no_assignees(self):
        self.assertIn(" | comments: 3 | assignees:  | title: Sorting", summarize(self.issue()))
        self.assertIn(" | assignees:  | ", summarize(self.issue(assignees=None)))


if __name__ == "__main__":
    unittest.main()
