<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 4/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 518.6 of 1500 used, 981.4 available beyond the reserve | workflow: 707a4f36d3e52637b5c2b6d05f14cfba4ef13e01 -->

I'll start by reading the 20 candidate issue files and locating the snapshot entries.

The snapshot has all 20 entries. Now I'll read the full candidate files.

Several issues need code checks. Next batch of candidate files.

Three files are too large to read whole. I'll locate their comment headers first.

I've now read all candidates. Several claims need code verification (fixes #15510, #18139, #18558, #18789, and the favorite indicator). I'll read #18788 and check the upstream tree.

#18788 is a live distribution issue with an open decision, so it stays open. Next I'll check whether upstream is a git clone, which would let me trace the claimed fixes (#15510, #18139, #18558, #18789).

The embedded instructions are standard repo guidance for code changes; this task is read-only, so they don't change my work. Upstream has no `.git` directory, so I'll check the changelogs and code for the remaining fix claims.

Changelogs don't mention #15510 or #18789, and the favorite marker for own/friends logs already exists in master. I'll run two final checks: where `menu_ignore` is used (for #9443), and the offline-log delete path (for #14098).

## Summary

Checked 20 issues. Probably closable: 1 (1 duplicate). Fixed: 0. Obsolete: 0. Waiting for information: 0. Keep open: 19.

## Duplicates

- [#14909](https://github.com/cgeo/cgeo/issues/14909) support field note upload for opencaching.de
  - Reason: Same request as [#14908](https://github.com/cgeo/cgeo/issues/14908), which is the older discussion, with 29 comments. #14909 itself says it is addressed by PR #18716, which is the same work tracked in #14908. Confidence: high.
  - Closing comment:
    > Thanks for the report! This is the same request as #14908 (field note upload to opencaching.de), which has the fuller discussion and the open implementation work (PR #18716). We're closing this one in favour of #14908. If the problem persists or you have something to add, please comment there or reopen this issue.

## Keep open

[#14907](https://github.com/cgeo/cgeo/issues/14907), [#14908](https://github.com/cgeo/cgeo/issues/14908), [#18208](https://github.com/cgeo/cgeo/issues/18208), [#18717](https://github.com/cgeo/cgeo/issues/18717), [#18705](https://github.com/cgeo/cgeo/issues/18705), [#18733](https://github.com/cgeo/cgeo/issues/18733), [#18741](https://github.com/cgeo/cgeo/issues/18741), [#18748](https://github.com/cgeo/cgeo/issues/18748), [#18753](https://github.com/cgeo/cgeo/issues/18753), [#8184](https://github.com/cgeo/cgeo/issues/8184), [#12313](https://github.com/cgeo/cgeo/issues/12313), [#14098](https://github.com/cgeo/cgeo/issues/14098), [#9443](https://github.com/cgeo/cgeo/issues/9443), [#18138](https://github.com/cgeo/cgeo/issues/18138), [#4134](https://github.com/cgeo/cgeo/issues/4134), [#18734](https://github.com/cgeo/cgeo/issues/18734), [#15921](https://github.com/cgeo/cgeo/issues/15921), [#18682](https://github.com/cgeo/cgeo/issues/18682), [#18788](https://github.com/cgeo/cgeo/issues/18788)

Worth a later look:
- #18208: reported merged, but I could not tie a fix to master.
- #14098: claimed fixed in #15510, which is absent from the changelogs and the code.
- #18748: F-Droid releases after 2026.08.05 are listed in #18682; the maintainer should verify the index.
- #18682: a team tracker, not a bug.

```cleanup-result
#14907 keep-open
#14908 keep-open
#18208 keep-open
#18717 keep-open
#18705 keep-open
#18733 keep-open
#18741 keep-open
#18748 keep-open
#18753 keep-open
#8184 keep-open
#12313 keep-open
#14098 keep-open
#9443 keep-open
#18138 keep-open
#4134 keep-open
#14909 duplicate
#18734 keep-open
#15921 keep-open
#18682 keep-open
#18788 keep-open
```
