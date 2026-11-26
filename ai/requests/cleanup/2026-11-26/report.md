<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 1/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 505.7 of 1500 used, 994.3 available beyond the reserve | workflow: d7e87ee585e88ddebec71b578af2d2517c5fd54c -->

I'll start by reading the 20 candidate issue files.

Several files are too large for a default read, so I'll read the rest with the force flag.

I've read all 20 issues. Next I'll check the snapshot for duplicates and the upstream code for the fixes the comments mention.

The snapshot grep was too broad. I'll narrow it to the specific issue numbers and search the upstream code more precisely.

The upstream tree already has a KML track parser, which may bear on #4875. I'll check how it's wired into track import, and look at the Android scroll and cache-type code for the other candidates.

Those system reminders are coding-style guidance for code I write. This task is a read-only report, so I'm not changing any files and will carry on with the checks. Next: the GC keyword-search path (for #16971) and the favorites filter (for #17283).

## Summary

- Checked: 20 issues
- Probably fixed: 0
- Duplicates: 3
- No longer applicable: 0
- Waiting for information: 2
- Keep open: 15

## Duplicates

- [#17744](https://github.com/cgeo/cgeo/issues/17744) "Hide all caches" / no types selected: duplicate of [#10963](https://github.com/cgeo/cgeo/issues/10963), which is open and has more discussion (40 comments). Confidence: medium-high.
  - Closing comment: "Thanks for the report. This is the same problem as #10963, which has more discussion, so we are closing this one in favour of it. Please follow #10963 for updates, or comment here if your case differs."
- [#17541](https://github.com/cgeo/cgeo/issues/17541) APK "open with" intent filters too broad: duplicate of [#17501](https://github.com/cgeo/cgeo/issues/17501), an open bug with the same root cause (see also [#17700](https://github.com/cgeo/cgeo/issues/17700)). Confidence: medium-high.
  - Closing comment: "Thanks for the report. The root cause is the same as #17501, which is open and tracks this, so we are closing this one as a duplicate. Please follow #17501, or comment here if the problem differs."
- [#17747](https://github.com/cgeo/cgeo/issues/17747) "Show all cache types" in advanced filter: duplicate of [#11923](https://github.com/cgeo/cgeo/issues/11923), which is open. Confidence: medium.
  - Closing comment: "Thanks for the suggestion. This is already tracked in #11923, which is open, so we are closing this one as a duplicate. Please follow #11923, or comment here if you have a different request."

## Waiting for information

- [#16744](https://github.com/cgeo/cgeo/issues/16744): a maintainer asked "Does that work for you?" on 2025-12-20, and the reporter has not replied since 2025-03-14. Confidence: medium.
  - Closing comment: "Thanks for the report. We asked on 2025-12-20 whether the change works for you and have not heard back. We are closing this for now. Please reopen or comment if the problem persists."
- [#17737](https://github.com/cgeo/cgeo/issues/17737): a maintainer asked on 2026-01-12 whether the steps match the release behaviour, with no reply since. Part 2 was reportedly fixed by #17728, which I could not verify in master. Confidence: medium.
  - Closing comment: "Thanks for the report. We asked on 2026-01-12 whether the steps match the release behaviour and have not heard back, so we are closing this for now. If the problem persists, please reopen or comment with the details."

## Keep open

[#16797](https://github.com/cgeo/cgeo/issues/16797), [#16971](https://github.com/cgeo/cgeo/issues/16971) (PR #17636 is not visible in master; keyword search is still sent in `GCMap.java:141`), [#17488](https://github.com/cgeo/cgeo/issues/17488) (ANR reports continue), [#6575](https://github.com/cgeo/cgeo/issues/6575), [#15193](https://github.com/cgeo/cgeo/issues/15193), [#9595](https://github.com/cgeo/cgeo/issues/9595), [#17322](https://github.com/cgeo/cgeo/issues/17322), [#17663](https://github.com/cgeo/cgeo/issues/17663), [#17283](https://github.com/cgeo/cgeo/issues/17283), [#17700](https://github.com/cgeo/cgeo/issues/17700), [#17625](https://github.com/cgeo/cgeo/issues/17625) (the reporter said it still fails after PR #17701), [#17579](https://github.com/cgeo/cgeo/issues/17579), [#17688](https://github.com/cgeo/cgeo/issues/17688), [#17797](https://github.com/cgeo/cgeo/issues/17797), [#4875](https://github.com/cgeo/cgeo/issues/4875) (KML track import exists in `GPXTrackOrRouteImporter.java:82-85`, but the integrated map request is unclear; low-medium confidence, worth a later look)

```cleanup-result
#16744 waiting
#16797 keep-open
#16971 keep-open
#17488 keep-open
#6575 keep-open
#15193 keep-open
#17541 duplicate
#9595 keep-open
#17322 keep-open
#17663 keep-open
#17283 keep-open
#17700 keep-open
#17625 keep-open
#17579 keep-open
#17744 duplicate
#17747 duplicate
#17737 waiting
#17688 keep-open
#17797 keep-open
#4875 keep-open
```
