<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 1/2 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 531.4 of 1500 used, 968.6 available beyond the reserve | workflow: 1110dd237fd88892ac4919eda5e1a4d19ad95956 -->

I'll start by checking which candidate files exist for the 20 issues and what the snapshot says about them.

All 20 candidate files exist. Reading them now.

Most candidates are read. Next I'll check upstream master for the fixes the comments mention (PR #18877, visiteddate handling, owned OC caches, waypoint filters, CI workflow, obfuscation, NetworkOnMainThread).

Upstream still has `-dontobfuscate`, the CI still gates on `ok-to-test`, and visiteddate logic is unchanged so far. Checking the offline-log visit-date callers, the owned-cache detection, the waypoint filter, and the DownloaderUtils download call.

Waypoint-tab filter is absent (keep-open). Next I'll check the "date logged" sort, owned-cache detection, and the offline-log delete path.

Upstream has a `HistoryComparator` that considers offline-log dates, which looks like the #18877 workaround. Checking that code, the offline-log delete path, and how a draft log for an uncached premium geocache is stored.

Continuing the audit. Next I'm checking whether deleting an offline log resets `visiteddate` (#18878), and how the history list handles draft logs for uncached premium geocaches (#12339).

Offline-log deletion calls `DataStore.clearLogOffline`. Checking whether that resets `visiteddate`, and how `saveLogOffline` handles it.

Confirmed: `clearLogOffline` never resets `visiteddate`, so #18878 is still present. Now checking whether offline logs for not-stored caches get persisted (relevant to #17819, #12339).

Offline logs for uncached geocaches are saved into the standard list before the visit date is set, which covers the #17819 scenario. Last check: how the history list renders its date, to judge #17030 and #7919.

The history date display (`CacheListAdapter.java:529`) now falls back to the offline-log date, which addresses #17030. Last, I'm checking owned-cache detection for OpenCaching (#4752) and the offline-log list marker (#15398).

## Summary

Checked 20 issues. 1 can probably be closed, 19 stay open.

- Fixed: 1
- Duplicate: 0
- Obsolete: 0
- Waiting for information: 0
- Keep open: 19

Five of the checked issues (#7919, #15398, #17030, #17819, #18853) already show as closed in their candidate files.

## Probably fixed

- [#17030](https://github.com/cgeo/cgeo/issues/17030) Caches shown without log date/time in history list
  - Reason: History entries now fall back to the offline-log date. `Geocache.getHistoryDate()` returns the newer of visited date and offline-log date (`main/src/main/java/cgeo/geocaching/models/Geocache.java`, ~lines 1134-1137), and `CacheListAdapter` shows the date when that value is positive (`main/src/main/java/cgeo/geocaching/ui/CacheListAdapter.java`, line 529). The sort uses `HistoryComparator` (`main/src/main/java/cgeo/geocaching/sorting/GeocacheSort.java`, line 211). Confidence: medium. The reporter's exact case is not re-tested, and a later comment says reproducible for non-stored caches.
  - Closing comment: "Thanks for the report! The history list now uses the offline log date when it is newer than the visited date (`getHistoryDate()`), so offline-logged caches get their date and sort correctly. If you still see caches without a date or at the bottom of the history list, please comment or reopen with the steps and version. Thank you!"

## Keep open

[#4752](https://github.com/cgeo/cgeo/issues/4752), [#7919](https://github.com/cgeo/cgeo/issues/7919), [#12339](https://github.com/cgeo/cgeo/issues/12339), [#15398](https://github.com/cgeo/cgeo/issues/15398), [#17252](https://github.com/cgeo/cgeo/issues/17252), [#17819](https://github.com/cgeo/cgeo/issues/17819), [#17904](https://github.com/cgeo/cgeo/issues/17904), [#18853](https://github.com/cgeo/cgeo/issues/18853), [#18863](https://github.com/cgeo/cgeo/issues/18863), [#18864](https://github.com/cgeo/cgeo/issues/18864), [#18865](https://github.com/cgeo/cgeo/issues/18865), [#18866](https://github.com/cgeo/cgeo/issues/18866), [#18867](https://github.com/cgeo/cgeo/issues/18867), [#18868](https://github.com/cgeo/cgeo/issues/18868), [#18869](https://github.com/cgeo/cgeo/issues/18869), [#18870](https://github.com/cgeo/cgeo/issues/18870), [#18871](https://github.com/cgeo/cgeo/issues/18871), [#18872](https://github.com/cgeo/cgeo/issues/18872), [#18878](https://github.com/cgeo/cgeo/issues/18878)

Notes where a later look is worthwhile:
- #18878: still present. `DataStore.clearLogOffline` does not reset `visiteddate`, while `saveVisitDate` sets it on save.
- #7919 and #18853: the stored-list "Date logged" sort still uses `visiteddate` only (`GeocacheSort.java` line 211).
- #17819: the not-stored case is now saved before the visit date is set, but the "missing until restart" symptom is unverified.
- #12339: maybe covered by the not-stored save path, but not verified.
- #4752: owner detection still depends on the live connector (`OCBaseConnector.isOwner` returns false).
- #17252: no waypoint filter exists.
- #18865: `-dontobfuscate` is still in `main/proguard-project.txt`.
- #17904: `tests.yml` still gates jobs on `ok-to-test`.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#17030](https://github.com/cgeo/cgeo/issues/17030): [PR #18877](https://github.com/cgeo/cgeo/pull/18877) "fix \#17030, fix \#18853, fix \#17819, fix \#7919 : Consider date of offline log", merged 2026-11-15, commit [1c05c19b8f](https://github.com/cgeo/cgeo/commit/1c05c19b8fc5b6868d933fb4c85f6f7d75eecdbe) of 2026-11-07, added `public long getHistoryDate()` in `main/src/main/java/cgeo/geocaching/models/Geocache.java`.

```cleanup-result
#4752 keep-open
#7919 keep-open
#12339 keep-open
#15398 keep-open
#17030 fixed
#17252 keep-open
#17819 keep-open
#17904 keep-open
#18853 keep-open
#18863 keep-open
#18864 keep-open
#18865 keep-open
#18866 keep-open
#18867 keep-open
#18868 keep-open
#18869 keep-open
#18870 keep-open
#18871 keep-open
#18872 keep-open
#18878 keep-open
```
