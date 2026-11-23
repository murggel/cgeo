<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 3/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 463.9 of 1500 used, 736.1 available beyond the reserve | workflow: 1d3a4543eb6f7e4963e3872cb0392abc1ae9da40 -->

I'll start by reading the candidate issue files and checking the snapshot format.

I've read all 20 candidate files. Next I'll check the code in `upstream/` for the concrete claims: HtmlSpanner, the image scale list, GK missing, route updates, and the rest.

The broad grep is too noisy, so I'll run targeted checks per issue.

The scale list still has the old 512–1024 options, so #14559 is not fixed. Next I'll check the toast code, LogCacheActivity, GCLogin, and the GK connector.

The system reminders above are upstream repo guidance. They don't change this task, which is read-only analysis, so I'll keep going. Next I'm checking the toast helper, the GK connector, the log-type and calendar code, and the F-Droid screenshots.

Next I'm checking the toast helper, the GeoKrety missing/image support, the LogCacheActivity onCreate path, and the route and log-sort code.

Several items are narrowing down. I'm verifying the route-removal-on-log path, the toast threading, and whether waypoint "visited" also removes from the route.

Route removal on log exists but is opt-in, so #12387 is still open. Last, I'm reading the toast helper to see whether background-thread toasts are handled.

The toast helper now posts to the UI thread, so #13781 looks fixed. Before finalizing, I'll search the snapshot for duplicates of the open feature requests.

The snapshot shows a few related items (#4839, #18796). I'll run one narrower search for the remaining topics.

That search was too broad. I'll run one final targeted search on the image and trackable titles.

The compact output hides titles. I'll do one last narrow title search for trackable-log and upload items.

## Summary

Checked 20 issues. Probably closable: 2.

- **Probably fixed:** 1
- **Duplicates:** 0
- **No longer applicable:** 0
- **Waiting for information:** 1
- **Keep open:** 18

## Probably fixed

- [#13781](https://github.com/cgeo/cgeo/issues/13781) "Failure to show error toast"
  - Reason: `ViewUtils.showToast` now routes every toast through `runOnUiThread`, which posts to the UI thread when called from a background thread (`upstream/main/src/main/java/cgeo/geocaching/ui/ViewUtils.java` lines 552–565 and 592–594). The `Looper.prepare()` crash from `ContentStorage.reportProblem` (`ContentStorage.java` line 644) therefore no longer occurs. Confidence: medium.
  - Closing comment: "Thanks for the report! Toasts are now dispatched to the UI thread from any thread (`ViewUtils.showToast`), so the failed-export error message from `ContentStorage` should be shown instead of crashing with 'Can't toast on a thread that has not called Looper.prepare()'. If you still see this problem, please reopen or comment with the log."

## Waiting for information

- [#11112](https://github.com/cgeo/cgeo/issues/11112) "\"Search by XYZ\" should have a progress spinner while loading caches"
  - Reason: moving-bits asked on 2023-07-02 for the exact scenario in which the spinner is missing. No answer has come in over three years. The original report was posted by @MagpieFourtyTwo. Confidence: medium.
  - Closing comment: "Thanks for the suggestion! We asked on 2023-07-02 which exact scenario lacks the progress indicator, but have not heard back. Searches opened from the search list already show a progress spinner, so we are closing this for now. If the spinner is still missing in a specific case, please reopen or describe the steps."

## Keep open

[#14246](https://github.com/cgeo/cgeo/issues/14246), [#14286](https://github.com/cgeo/cgeo/issues/14286), [#14287](https://github.com/cgeo/cgeo/issues/14287), [#14289](https://github.com/cgeo/cgeo/issues/14289), [#14293](https://github.com/cgeo/cgeo/issues/14293), [#7064](https://github.com/cgeo/cgeo/issues/7064), [#14357](https://github.com/cgeo/cgeo/issues/14357), [#14276](https://github.com/cgeo/cgeo/issues/14276), [#12387](https://github.com/cgeo/cgeo/issues/12387), [#14374](https://github.com/cgeo/cgeo/issues/14374), [#4360](https://github.com/cgeo/cgeo/issues/4360), [#14306](https://github.com/cgeo/cgeo/issues/14306), [#14457](https://github.com/cgeo/cgeo/issues/14457), [#14486](https://github.com/cgeo/cgeo/issues/14486), [#5097](https://github.com/cgeo/cgeo/issues/5097), [#14559](https://github.com/cgeo/cgeo/issues/14559), [#4867](https://github.com/cgeo/cgeo/issues/4867), [#5848](https://github.com/cgeo/cgeo/issues/5848)

Worth a later look:
- #14293: a null guard now exists at `LogCacheActivity.java` lines 215–219, so this may be fixed.
- #14246: HtmlSpanner is not used; the `<a><p>` link problem is probably still there.
- #14559: the scaling list is still 512–1024.
- #12387: route removal on log is opt-in (`Geocache.java` line 645).
- #4360: multiple logging templates may cover the request.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#13781](https://github.com/cgeo/cgeo/issues/13781): [PR #15767](https://github.com/cgeo/cgeo/pull/15767) "Refactor: unify usage of Toasts across c:geo", merged 2024-06-09, commit [326121ae1b](https://github.com/cgeo/cgeo/commit/326121ae1bff3987d2e4afe656e9843e728fc2fb) of 2024-06-08, added `currentThreadIsUiThread` in `main/src/main/java/cgeo/geocaching/ui/ViewUtils.java`.

```cleanup-result
#14246 keep-open
#14286 keep-open
#14287 keep-open
#14289 keep-open
#14293 keep-open
#7064 keep-open
#14357 keep-open
#14276 keep-open
#12387 keep-open
#14374 keep-open
#4360 keep-open
#11112 waiting
#14306 keep-open
#13781 fixed
#14457 keep-open
#14486 keep-open
#5097 keep-open
#14559 keep-open
#4867 keep-open
#5848 keep-open
```
