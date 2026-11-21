<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 3/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 430.4 of 1500 used, 769.6 available beyond the reserve | workflow: f8ce42a851cf3a1b6b9d29231137a189435025f9 -->

I'll start by checking which candidate files exist and what the snapshot looks like.

All 20 candidate files exist. Reading them now.

Eleven read. Next batch, plus the large file #2093 read in ranges.

Most issues are read. #167 and the rest of #2093 are too large for a single read, so I'll read them in ranges.

I've read all 20 issues. Next I'll check the snapshot for duplicates and search upstream code for the fixes the issues describe.

The snapshot uses newer numbers, so I'll match duplicates by keyword. Now targeted code searches in upstream for each issue's subject.

Several leads: #7818 is still present (`UserClickListener.java:57` uses `userName`), and #8895 has downgrade-version handling in `DataStore`. Checking more code paths and existence of old live-map and EC logging classes.

Those two system reminders are in the user turn, so they're not tool-result injections. They govern code I'd write, and this task is read-only, so I'll keep going with the analysis. Next: checking whether the EC connector and the old mapsforge live map still exist.

The EC connector still exists, so #7188 needs a closer look. Checking how the log post button is enabled now, and how the old live map is wired.

`LogCacheActivity` has been refactored to a `readyToPost` flag. Checking whether a loading state can still block posting for EC caches.

The post button is gated by a loader lifecycle now, with `showProgress(false)` called on load finish, so the old `enablePostButton(false)` bug looks gone. One last duplicate sweep in the snapshot for the remaining topics.

**Summary:** 20 issues checked. Probably closable: 2 (obsolete: 2, fixed: 0, duplicate: 0, waiting: 0). Keep open: 18.

## No longer applicable

- [#3798](https://github.com/cgeo/cgeo/issues/3798) (title: see the issue): the old mapsforge `CachesOverlay` is gone from upstream. Only `unifiedmap/` remains, so the reported code path no longer exists. Confidence: medium.
  - Closing comment: "Thanks for the report. The mapsforge live map code this refers to has been replaced by the unified map, so this issue no longer applies. If the problem still occurs on the unified map, please comment or open a new issue with steps to reproduce."

- [#8614](https://github.com/cgeo/cgeo/issues/8614) (title: see the issue): the old `NewMap` implementation is no longer in upstream, and the map now lives in `unifiedmap/`. Confidence: medium.
  - Closing comment: "Thanks for the report. The map implementation this refers to has been reworked into the unified map, so this issue no longer applies. If it still happens there, please comment or open a new issue."

## Keep open

[#7797](https://github.com/cgeo/cgeo/issues/7797), [#7818](https://github.com/cgeo/cgeo/issues/7818), [#7403](https://github.com/cgeo/cgeo/issues/7403), [#7125](https://github.com/cgeo/cgeo/issues/7125), [#2093](https://github.com/cgeo/cgeo/issues/2093), [#8895](https://github.com/cgeo/cgeo/issues/8895), [#8658](https://github.com/cgeo/cgeo/issues/8658), [#9012](https://github.com/cgeo/cgeo/issues/9012), [#9027](https://github.com/cgeo/cgeo/issues/9027), [#9052](https://github.com/cgeo/cgeo/issues/9052), [#9190](https://github.com/cgeo/cgeo/issues/9190), [#9209](https://github.com/cgeo/cgeo/issues/9209), [#7188](https://github.com/cgeo/cgeo/issues/7188), [#7782](https://github.com/cgeo/cgeo/issues/7782), [#8323](https://github.com/cgeo/cgeo/issues/8323), [#167](https://github.com/cgeo/cgeo/issues/167), [#9738](https://github.com/cgeo/cgeo/issues/9738)

Later looks worthwhile: [#9027](https://github.com/cgeo/cgeo/issues/9027) (its old toggling path is gone, so it may be obsolete), [#7188](https://github.com/cgeo/cgeo/issues/7188) (the old post-button disable is gone, but EC posting was not fully verified), [#8895](https://github.com/cgeo/cgeo/issues/8895) (part 2 unclear).

```cleanup-result
#7797 keep-open
#8614 obsolete
#3798 obsolete
#6935 keep-open
#7403 keep-open
#7125 keep-open
#7818 keep-open
#2093 keep-open
#8895 keep-open
#8658 keep-open
#9012 keep-open
#9027 keep-open
#9052 keep-open
#9190 keep-open
#9209 keep-open
#7188 keep-open
#7782 keep-open
#8323 keep-open
#167 keep-open
#9738 keep-open
```
