<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 2/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 494.6 of 1500 used, 705.4 available beyond the reserve | workflow: 8c6dd3a0e6a5bb2ce4f7f91644e7cd6a3ab23cf2 -->

I'll start by reading the 20 candidate issue files.

I've read all 20 files. Next I'll check the snapshot for duplicates and search the upstream code for each fix or feature.

The snapshot grep was too broad. I'll run narrower searches and check the upstream code in parallel.

Found the logcat capture in upstream's `tests.yml` (for #11023). Now I'll read the specific code regions for the Wherigo service, log-image storage, offline check, and the coordinates/track code.

The reminders in that message came from the user turn, so I'll follow them. I'm not writing any code in this read-only task, so they don't change the report. Next I'll check the remaining feature and string items.

Key finding: "Spoiler images" is still the English label (#17091 not fixed), and the search hint still reads "Search caches/trackables". Next I'll check navigation zoom and the coordinates dialog for #17097 and #16951.

Upstream still has only the cache-coordinates button, so #16951 is open. One last targeted snapshot search for duplicates.

The snapshot doesn't show a clear duplicate for the remaining items. I'll check the issue numbers that the discussions link to, since they may be open duplicates.

I haven't read #15425 yet; its file was too large for the first call. I'll read it in ranges.

## Summary

20 issues checked: 2 probably fixed, 1 duplicate, 0 obsolete, 3 waiting for information, 14 keep open.

## Probably fixed

- [#11023](https://github.com/cgeo/cgeo/issues/11023) CI/Jenkins: make logcat output accessible for Test runs
  - Reason: The GitHub test workflow now captures logcat during the emulator run and uploads it as an artifact (`.github/workflows/tests.yml`, lines 486–503). The Jenkins part of the request is no longer relevant, because CI runs on GitHub. Confidence: medium.
  - Closing comment: "Thanks for the request. Test runs now capture logcat output and attach it to the test results artifacts (`.github/workflows/tests.yml`). If the logs are still missing for your use case, please comment or reopen."

- [#17093](https://github.com/cgeo/cgeo/issues/17093) RuntimeException in WherigoGameService.onCreate
  - Reason: `WherigoGameService.onCreate()` wraps `startForeground(...)` in a `try` and catches `IllegalStateException | SecurityException`, which covers `ForegroundServiceStartNotAllowedException` and the `SecurityException` from the second trace (`main/src/main/java/cgeo/geocaching/wherigo/WherigoGameService.java`, roughly lines 49–62). Confidence: high.
  - Closing comment: "The foreground-service start in `WherigoGameService.onCreate` is now guarded against `ForegroundServiceStartNotAllowedException`/`SecurityException`, so the crash should be gone in current builds. If it still happens with a current version, please comment or reopen."

## Duplicates

- [#7850](https://github.com/cgeo/cgeo/issues/7850) Upload button for personal note missing
  - Duplicate of [#15482](https://github.com/cgeo/cgeo/issues/15482) (open, "Always show personal note upload button"). Both are about the upload button being hidden or missing when the connector state is unclear. #15482 is the open tracker for this behaviour, and the discussion here already links it. Confidence: high.
  - Closing comment: "This is covered by #15482 ("Always show personal note upload button"), which tracks the same missing-button behaviour. Please follow that issue or comment there if the problem persists."

## Waiting for information

- [#10837](https://github.com/cgeo/cgeo/issues/10837) Individual track and OC waypoints
  - Last substantive comment by bekuno on 2025-06-08 asks for a GPX export or GMX file to analyse. No reply since. Confidence: medium-high.
  - Closing comment: "We need the GMX/GPX file or the OC waypoint code to investigate this. The question from 2025-06-08 is still unanswered, so we are closing for now. Please reopen with the requested data if it still happens."

- [#16191](https://github.com/cgeo/cgeo/issues/16191) found status of ALC is not automatically set
  - Last substantive comment by murggel on 2025-06-10 asks for test data or test labs to reproduce. No reply since. Related to #15916 (upper-casing of codes). Confidence: medium.
  - Closing comment: "We still need test data or test labs for the ALC cases to reproduce this, and the question from 2025-06-10 is unanswered. Please reopen with the codes or steps if the status still isn't set automatically."

- [#16977](https://github.com/cgeo/cgeo/issues/16977) Tests -> request was not successful: message=Forbidden
  - Last substantive comment by kumy on 2025-06-11 asks bekuno to confirm whether concurrent test runs cause the 403 errors. No reply since. Confidence: medium.
  - Closing comment: "The question on 2025-06-11 about whether concurrent CI runs cause these 403 errors is still unanswered. Please reopen with confirmation or new CI logs if the failures continue."

## Keep open

[#1786](https://github.com/cgeo/cgeo/issues/1786), [#8825](https://github.com/cgeo/cgeo/issues/8825) (logbook format setting exists, but the long-date dot is still missing), [#9084](https://github.com/cgeo/cgeo/issues/9084) (related: #12729, #15901), [#17024](https://github.com/cgeo/cgeo/issues/17024), [#17035](https://github.com/cgeo/cgeo/issues/17035), [#17042](https://github.com/cgeo/cgeo/issues/17042), [#16951](https://github.com/cgeo/cgeo/issues/16951) (overlaps with #15924; the coordinate dialog still only offers cache coordinates), [#16778](https://github.com/cgeo/cgeo/issues/16778) (open design question on gallery images), [#16173](https://github.com/cgeo/cgeo/issues/16173), [#15425](https://github.com/cgeo/cgeo/issues/15425), [#17091](https://github.com/cgeo/cgeo/issues/17091) ("Spoiler images" is still the English string), [#17097](https://github.com/cgeo/cgeo/issues/17097), [#17098](https://github.com/cgeo/cgeo/issues/17098), [#15315](https://github.com/cgeo/cgeo/issues/15315)

## Evidence

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#11023](https://github.com/cgeo/cgeo/issues/11023): [PR #17068](https://github.com/cgeo/cgeo/pull/17068) "Ci watchdog", merged 2025-06-19, commit [e77629d270](https://github.com/cgeo/cgeo/commit/e77629d2709f240704cf891be096e542e09a5164) of 2025-06-19, added `adb logcat > /tmp/cgeo-apk-api` in `.github/workflows/tests.yml`.
- [#17093](https://github.com/cgeo/cgeo/issues/17093): [PR #18688](https://github.com/cgeo/cgeo/pull/18688) "Fix SecurityException on startForeground (fix \#18675)", merged 2026-10-03, commit [9aa87aa274](https://github.com/cgeo/cgeo/commit/9aa87aa274b7fcad116b01052a87355eb14b76a4) of 2026-10-03, added `catch (IllegalStateException | SecurityException re)` in `main/src/main/java/cgeo/geocaching/wherigo/WherigoGameService.java`.

## Result

```cleanup-result
#1786 keep-open
#10837 waiting
#8825 keep-open
#9084 keep-open
#17024 keep-open
#16191 waiting
#17035 keep-open
#16977 waiting
#17042 keep-open
#7850 duplicate
#16951 keep-open
#11023 fixed
#16778 keep-open
#16173 keep-open
#15425 keep-open
#17091 keep-open
#17093 fixed
#17097 keep-open
#17098 keep-open
#15315 keep-open
```
