<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | provider: claude | workflow: 2353adc863eabdcc0cdc1e09715084aa4e8600a5 -->

## Summary

I checked 28 issues. I found none that I can recommend closing now: 0 fixed, 0 duplicates, 0 obsolete, 0 waiting. All 28 stay in keep-open.

- **Already closed on GitHub (9):** [#7919](https://github.com/cgeo/cgeo/issues/7919), [#15398](https://github.com/cgeo/cgeo/issues/15398), [#17030](https://github.com/cgeo/cgeo/issues/17030), [#17819](https://github.com/cgeo/cgeo/issues/17819), [#18853](https://github.com/cgeo/cgeo/issues/18853), [#18855](https://github.com/cgeo/cgeo/issues/18855), [#18895](https://github.com/cgeo/cgeo/issues/18895), [#18901](https://github.com/cgeo/cgeo/issues/18901) and [#18229](https://github.com/cgeo/cgeo/issues/18229). Their state is already `closed` in the downloaded text, so there is nothing to close. I did not list them as "fixed", because that category is for issues that should be closed.
- **Open and recent:** no open issue has an unanswered question to the reporter that is 6 months old or more. The only question to a reporter is on [#4752](https://github.com/cgeo/cgeo/issues/4752), dated 2026-11-05.
- **No duplicates among the open issues:** the ANR issues #18867–#18871 are examples collected under the meta issue #18866. The four sorting/history issues #17030, #17819, #18853 and #7919 overlap, but they are all already closed.

## Keep open

[#4752](https://github.com/cgeo/cgeo/issues/4752) (Detecting own opencaching caches fails when not online), [#12339](https://github.com/cgeo/cgeo/issues/12339) (Premium-only draft logs not shown in History list), [#17252](https://github.com/cgeo/cgeo/issues/17252) (Filter for waypoints in waypoint-tab), [#17904](https://github.com/cgeo/cgeo/issues/17904) (CI tests not running without ok-to-test), [#18863](https://github.com/cgeo/cgeo/issues/18863) (NetworkOnMainThreadException), [#18864](https://github.com/cgeo/cgeo/issues/18864) (Play Store: bitmap memory), [#18865](https://github.com/cgeo/cgeo/issues/18865) (Play Store: missing obfuscation), [#18866](https://github.com/cgeo/cgeo/issues/18866) (Play Store: ANR meta issue), [#18867](https://github.com/cgeo/cgeo/issues/18867), [#18868](https://github.com/cgeo/cgeo/issues/18868), [#18869](https://github.com/cgeo/cgeo/issues/18869), [#18870](https://github.com/cgeo/cgeo/issues/18870), [#18871](https://github.com/cgeo/cgeo/issues/18871) (ANR reports), [#18872](https://github.com/cgeo/cgeo/issues/18872) ("Missing resource" errors), [#18878](https://github.com/cgeo/cgeo/issues/18878) (Deleting offline log does not update visitedDate), [#18883](https://github.com/cgeo/cgeo/issues/18883) (Handling of UDC created from cache list), [#18891](https://github.com/cgeo/cgeo/issues/18891) (Images in personal notes), [#18908](https://github.com/cgeo/cgeo/issues/18908) (Routing should take linear labs into account), [#18909](https://github.com/cgeo/cgeo/issues/18909) (OutOfMemory Exception).

Reasons where a later look seems worthwhile:
- **#4752:** murggel asked Lineflyer on 2026-11-05 whether it still happens. If there is no answer in about 6 months, it can go to "waiting".
- **#12339:** murggel wrote "maybe fixed with PR #18877". Upstream/ has the history-date change (`getHistoryDate()` in `main/src/main/java/cgeo/geocaching/models/Geocache.java:1134`, used by `HistoryComparator`). That change affects sorting only. Nothing in upstream/ shows that premium-only caches with only a draft log now appear in the list. Someone should test it before closing.
- **#18878:** this is the open follow-up to #7919 for the visitedDate problem when an offline log is deleted.
- **#18901 (already closed):** `ShareUtils.openCustomTab` (`main/src/main/java/cgeo/geocaching/utils/ShareUtils.java:250-264`) still has no `ActivityNotFoundException` handling. If the crash with malformed `http:/…` links should be fixed, the closed issue may need a re-check.

```cleanup-result
#4752 keep-open
#7919 keep-open
#15398 keep-open
#17030 keep-open
#17819 keep-open
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
#12339 keep-open
#17252 keep-open
#17904 keep-open
#18883 keep-open
#18891 keep-open
#18901 keep-open
#18908 keep-open
#18229 keep-open
#18855 keep-open
#18895 keep-open
#18909 keep-open
```
