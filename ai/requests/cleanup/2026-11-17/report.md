<!-- task: cleanup-issues | upstream: cgeo/cgeo@0edab2d977d2f9631cbef5d52f54e4f7abdefc13 | issue snapshot: 2026-11-15 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 428 of 1500 used, 772 available beyond the reserve | workflow: e9eac61e16e6ab3ac9e0a9bf2c7b3b2ec305c56a -->

I'll start by checking which candidate files exist and how the snapshot is laid out.

All 20 candidate files exist. I'll read them now.

I've read all 20 issues. Several claims depend on current code, so I'll check the upstream tree for each feature and string in parallel.

Key results so far: `customListIdOffset` still exists (so #6289 and #6227 stay open), and a favorites-percentage filter exists. I'll read the relevant code sections.

Continuing the audit. The remaining checks are the description fastscroll, the field-note export, the backup format, the description WebView, and the Play Services settings dialog.

The fastscroll exists only for the waypoint list, and the field-note dialog still has the global "only new" timestamp, so both remain open. A last batch covers backup format, the Send2cgeo downloader, OKAPI language, and the home-location fallback.

Most remaining issues are still applicable. I'll run one last check for the friend-log filter, contacts-based friends, and the package refactor.

Two findings change the picture: a log-entry "found by" filter now exists (relevant to #6511), and `ContactsHelper` exists (relevant to #5852). I need to confirm both are wired up in the UI and not just present.

The "Found by" log-entry filter is wired into the UI (`GeocacheFilterType.LOG_ENTRY`), so #6511 is fixed. `ContactsHelper` is only used for the owner contact card, so #5852 stays open. Last step: search the snapshot for duplicates of the remaining issues.

The snapshot search turned up related-but-distinct items (#4672, #3273). I'll run targeted title-level checks for the remaining topics to confirm there are no clear duplicates.

The title-level search found no clear duplicates. One more check: whether the cache-details delete action now goes through the undo-capable `DeleteCachesCommand` (#6489).

## Summary

Checked 20 issues: **1 probably fixed**, 0 duplicates, 0 obsolete, 0 waiting, **19 keep open**.

## Probably fixed

- [#6511](https://github.com/cgeo/cgeo/issues/6511) Add filter for gc friend that has found caches in your list
  - Reason: A "Found by" log-entry filter now exists. It is registered as `LOG_ENTRY` (`main/src/main/java/cgeo/geocaching/filters/core/GeocacheFilterType.java` line 37), with the UI in `main/src/main/java/cgeo/geocaching/filters/gui/LogEntryFilterViewHolder.java` line 36 and matching on log authors in `main/src/main/java/cgeo/geocaching/filters/core/LogEntryGeocacheFilter.java` lines 37–62. The limit (only logs already loaded) was accepted by the reporter.
  - Confidence: medium-high
  - Closing comment: "Thanks for the suggestion! c:geo now has a 'Found by' log-entry filter (Filter → Details → Found by), which lists caches where a given user appears in the loaded logs, including friend logs. Please comment or reopen if it doesn't cover your use case."

## Keep open

[#3891](https://github.com/cgeo/cgeo/issues/3891) (rename not done; "Recently viewed" exists separately), [#5077](https://github.com/cgeo/cgeo/issues/5077) (description still native, WebView only for login), [#6005](https://github.com/cgeo/cgeo/issues/6005) (refactoring still ongoing), [#5852](https://github.com/cgeo/cgeo/issues/5852) (ContactsHelper only used for owner card), [#6143](https://github.com/cgeo/cgeo/issues/6143) (maintainer declined; could be closed as won't-fix), [#4751](https://github.com/cgeo/cgeo/issues/4751) (no settings-dialog code), [#6274](https://github.com/cgeo/cgeo/issues/6274) (send2cgeo is single-cache only), [#6227](https://github.com/cgeo/cgeo/issues/6227), [#6289](https://github.com/cgeo/cgeo/issues/6289) (`customListIdOffset` still present), [#4405](https://github.com/cgeo/cgeo/issues/4405) (sort still exists; percentage filter only partly addresses it), [#3123](https://github.com/cgeo/cgeo/issues/3123), [#4258](https://github.com/cgeo/cgeo/issues/4258) (field-note export still list-based, no counts), [#6348](https://github.com/cgeo/cgeo/issues/6348), [#6489](https://github.com/cgeo/cgeo/issues/6489) (details page doesn't use `DeleteCachesCommand`), [#6409](https://github.com/cgeo/cgeo/issues/6409) (preferred-language list only, no per-cache switch), [#5791](https://github.com/cgeo/cgeo/issues/5791), [#6638](https://github.com/cgeo/cgeo/issues/6638) (fastscroll only in waypoint list), [#6650](https://github.com/cgeo/cgeo/issues/6650), [#2380](https://github.com/cgeo/cgeo/issues/2380) (backup still copies SQLite file)

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#6511](https://github.com/cgeo/cgeo/issues/6511): [PR #10767](https://github.com/cgeo/cgeo/pull/10767) "fix \#10635: added filters for log entry, last found and log counts", merged 2021-05-27, commit [ab254eb5e6](https://github.com/cgeo/cgeo/commit/ab254eb5e61136533b0215a7270eefc5d6d5647d) of 2021-05-27, added `cache_filter_log_entry_foundby` in `main/src/main/java/cgeo/geocaching/filters/gui/LogEntryFilterViewHolder.java`.

```cleanup-result
#3891 keep-open
#5077 keep-open
#6005 keep-open
#5852 keep-open
#6143 keep-open
#4751 keep-open
#6274 keep-open
#6227 keep-open
#6289 keep-open
#4405 keep-open
#3123 keep-open
#4258 keep-open
#6348 keep-open
#6489 keep-open
#6409 keep-open
#6511 fixed
#5791 keep-open
#6638 keep-open
#6650 keep-open
#2380 keep-open
```
