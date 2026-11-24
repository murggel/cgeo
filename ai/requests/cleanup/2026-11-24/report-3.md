<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 3/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 481.8 of 1500 used, 718.2 available beyond the reserve | workflow: 82cc223d3f1a7bb66fe3741eb4cd0662da311006 -->

I'll start by locating the candidate issue files and the snapshot.

All 20 candidate files exist. Reading them now.

Now the snapshot, searched for duplicates of these issues, and a check that the upstream checkout exists.

The broad search matched too much. I'll search the snapshot for the specific issue numbers instead, since issues often cross-reference each other.

The snapshot shows several likely duplicates (e.g. #16951 vs #15924, #16187 vs #14329). Next I'll check the remaining cross-referenced numbers and the upstream code for each candidate.

Next, the upstream code checks. I'll run targeted greps for each candidate in parallel.

Several leads: a `HiddenGeocacheFilter`, an `ImportBookmarkLinks` class (relevant to #15802), and HTTP 429 handling in the live map only. I'll read those and check GeoKrety and the other candidates.

Those reminders are repo style rules for code I'd write; this task is read-only, so nothing changes for the report. Continuing the upstream checks.

Findings so far: GeoKrety has no 429 handling, the live map still reloads the whole list on cache change, and the date-range filter needs a closer look. Checking those files now, plus the log activity and watchlist code.

Watchlist failures still return `false` when the server says the state already matches, so #15979 is unfixed. Next, the SQL date filter (for #15867), the log activity focus, and the trackable colour and clear-target code.

The date filter still converts hidden dates with SQLite's UTC `date()` while the min/max bounds use local time, so #15867 is still present. Next I'll check the map idle-debounce code (possible #15977 fix), background image loading (#15934), and GPX import intent handling (#14329).

The map debounce logic exists but does not clearly stop reloads during gestures, so #15977 stays open. The background image still uses the same pattern, so #15934 is also still open. Next I'll check the GPX intent handling for #14329.

## Summary

Checked 20 issues. Probably closable: 3 duplicates, 0 fixed, 0 obsolete, 0 waiting. The other 17 stay open.

## Duplicates

- [#15388](https://github.com/cgeo/cgeo/issues/15388) GeoKrety 429 rate limit: duplicate of [#14657](https://github.com/cgeo/cgeo/issues/14657), which is older and covers the same problem. Confidence: high. The reporter's own comment says so, and the code has no GeoKrety-specific 429 handling (HttpRequest.java:169-171 only broadcasts for the live map).

  Closing comment: "Thanks for the report. This is the same problem as #14657, which is already tracked there, so we are closing this one in favour of it. Please comment on #14657 if the problem persists."

- [#15924](https://github.com/cgeo/cgeo/issues/15924) Projection from another waypoint: duplicate of [#16951](https://github.com/cgeo/cgeo/issues/16951), which requests the same feature and has more discussion. Confidence: medium. Projection logic exists (Waypoint.java:388-565, CacheArtefactParser.java:45-266), but no waypoint picker was found.

  Closing comment: "Thanks for the suggestion. It is the same request as #16951, which is already tracked there, so we are closing this one in favour of it. Please comment on #16951 if you have more to add."

- [#14329](https://github.com/cgeo/cgeo/issues/14329) Import tracks/routes via GPX open: duplicate of [#16187](https://github.com/cgeo/cgeo/issues/16187), which covers the same track-import problem and is already labelled Duplicate. Confidence: medium. Maintainer should confirm which one to keep.

  Closing comment: "Thanks for the report. The problem is the same as #16187, which is tracked there, so we are closing this one in favour of it. Please comment on #16187 if the problem persists."

## Keep open

[#15783](https://github.com/cgeo/cgeo/issues/15783), [#12910](https://github.com/cgeo/cgeo/issues/12910), [#15802](https://github.com/cgeo/cgeo/issues/15802), [#15673](https://github.com/cgeo/cgeo/issues/15673), [#11871](https://github.com/cgeo/cgeo/issues/11871), [#15840](https://github.com/cgeo/cgeo/issues/15840), [#15461](https://github.com/cgeo/cgeo/issues/15461), [#15867](https://github.com/cgeo/cgeo/issues/15867), [#15847](https://github.com/cgeo/cgeo/issues/15847), [#13415](https://github.com/cgeo/cgeo/issues/13415), [#15934](https://github.com/cgeo/cgeo/issues/15934), [#15977](https://github.com/cgeo/cgeo/issues/15977), [#15979](https://github.com/cgeo/cgeo/issues/15979), [#14227](https://github.com/cgeo/cgeo/issues/14227), [#14657](https://github.com/cgeo/cgeo/issues/14657), [#16017](https://github.com/cgeo/cgeo/issues/16017), [#16025](https://github.com/cgeo/cgeo/issues/16025)

Worth a later look: #15867 (DateFilter still mixes UTC and local time), #15977 (idle debounce exists but may not cover gestures), #15802 (behaviour is by design in ImportBookmarkLinks.java).

```cleanup-result
#15783 keep-open
#12910 keep-open
#15802 keep-open
#15673 keep-open
#11871 keep-open
#15840 keep-open
#15461 keep-open
#15867 keep-open
#15847 keep-open
#13415 keep-open
#14329 duplicate
#15924 duplicate
#15934 keep-open
#15977 keep-open
#15979 keep-open
#14227 keep-open
#14657 keep-open
#15388 duplicate
#16017 keep-open
#16025 keep-open
```
