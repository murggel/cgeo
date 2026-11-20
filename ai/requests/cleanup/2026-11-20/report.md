<!-- task: cleanup-issues | upstream: cgeo/cgeo@81d6f67055136a9fc1dfde9d8cf045abe7f911aa | issue snapshot: 2026-11-15 | provider: claude | workflow: 6720cef2b038ed68e37780b676e143711f186d84 -->

## Summary

I checked 20 issues. One can probably be closed as fixed. I found no duplicates, no obsolete issues and no waiting issues. The other 19 stay open.

| Category | Count |
|---|---|
| Probably fixed | 1 |
| Duplicates | 0 |
| No longer applicable | 0 |
| Waiting for information | 0 |
| Keep open | 19 |

## Probably fixed

**[#6360](https://github.com/cgeo/cgeo/issues/6360) – Mass uploading personal notes should not be in Export menu**
- **Reason:** The issue asked to rename the entry or make clear that it uploads. The label is now "Upload personal notes" (`upstream/main/src/main/res/values/strings.xml:2394`, `export_persnotes`). Lineflyer already noted "Renamed accordingly" in February 2017. `PersonalNoteExport` now starts a `PersonalNoteUploadService` batch upload (`main/src/main/java/cgeo/geocaching/export/PersonalNoteExport.java:24-28`). The menu id is still `menu_export_persnotes`, but the user-visible label no longer suggests a file export.
- **Confidence:** medium. The code still names the menu item "export", so I couldn't check where it sits in the menu hierarchy.
- **Suggested comment:** "The menu entry is now labelled 'Upload personal notes', so it is clear that the notes are uploaded to the server and not exported to a file. I'm closing this as done. Please reopen or comment if you still find it confusing."

## Keep open

Reasons are given where a later look seems worthwhile.

- [#1806](https://github.com/cgeo/cgeo/issues/1806): general refactoring request, still relevant per the maintainers in 2017.
- [#4802](https://github.com/cgeo/cgeo/issues/4802): GeoKrety are probably still not counted in the list. The code was never merged.
- [#3049](https://github.com/cgeo/cgeo/issues/3049)
- [#6901](https://github.com/cgeo/cgeo/issues/6901)
- [#6590](https://github.com/cgeo/cgeo/issues/6590): `PersonalNote.java` now has a `fromProvider` flag and an entry-by-entry merge. This is partly the dirty-flag idea, but a changed server note is still appended to the local one. A closer look at the current behaviour may be worthwhile.
- [#6910](https://github.com/cgeo/cgeo/issues/6910)
- [#6949](https://github.com/cgeo/cgeo/issues/6949): I found no OC contact code in `upstream`, so I can't say whether the related features #6931 and #6932 still exist.
- [#4899](https://github.com/cgeo/cgeo/issues/4899): pstorch asked for opinions in 2018, but that is a question to the maintainers, not the reporter.
- [#6970](https://github.com/cgeo/cgeo/issues/6970)
- [#6994](https://github.com/cgeo/cgeo/issues/6994): I found no stage count in the cache details code.
- [#7090](https://github.com/cgeo/cgeo/issues/7090)
- [#7096](https://github.com/cgeo/cgeo/issues/7096): the "Feedback required" label means developer feedback. Lineflyer voted for a confirmation dialog, and I did not check whether one exists now.
- [#4457](https://github.com/cgeo/cgeo/issues/4457)
- [#7117](https://github.com/cgeo/cgeo/issues/7117)
- [#7173](https://github.com/cgeo/cgeo/issues/7173): `needs_maintenance` appears only when posting logs (`OkapiClient.java:647`), not as a displayed state.
- [#5004](https://github.com/cgeo/cgeo/issues/5004): `OkapiClient.java:1061-1062` still maps "Ready to search" to `ENABLE_LISTING`, which is the problem following5 described in 2018.
- [#6162](https://github.com/cgeo/cgeo/issues/6162)
- [#7215](https://github.com/cgeo/cgeo/issues/7215): the maintainers decided against background sync in 2018. That is not a reason to close it on its own.
- [#7283](https://github.com/cgeo/cgeo/issues/7283): still present. `LogCacheActivity.updateLogPasswordBox` (`main/src/main/java/cgeo/geocaching/log/LogCacheActivity.java:461-467`) shows the password field only for `FOUND_IT`, so `ATTENDED` event logs get no password prompt.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#6360](https://github.com/cgeo/cgeo/issues/6360): [PR #16935](https://github.com/cgeo/cgeo/pull/16935) "Fix \#16625: Move upload entries and update labels", merged 2025-05-16, commit [9223a00a22](https://github.com/cgeo/cgeo/commit/9223a00a227d379cd077fc210c6036ca78e5a1b4) of 2025-05-10, added `Upload personal notes` in `main/src/main/res/values/strings.xml`.

```cleanup-result
#1806 keep-open
#4802 keep-open
#3049 keep-open
#6901 keep-open
#6590 keep-open
#6910 keep-open
#6949 keep-open
#4899 keep-open
#6970 keep-open
#6994 keep-open
#6360 fixed
#7090 keep-open
#7096 keep-open
#4457 keep-open
#7117 keep-open
#7173 keep-open
#5004 keep-open
#6162 keep-open
#7215 keep-open
#7283 keep-open
```
