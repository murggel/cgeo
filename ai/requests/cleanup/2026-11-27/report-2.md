<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 2/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 518.6 of 1500 used, 981.4 available beyond the reserve | workflow: 707a4f36d3e52637b5c2b6d05f14cfba4ef13e01 -->

I'll start by checking which candidate issue files exist and how the snapshot is laid out.

All 20 candidate files exist. Next I'll read them, plus the snapshot header.

The remaining candidate, #9398, is too large for a single read, so I'll read it in ranges. I'll also check the snapshot's line format.

The snapshot has entries for all 20 issues. Next I'll search it for possible duplicates of each topic.

The snapshot search surfaces no clear duplicates yet. Next I'll check the upstream checkout's layout and how git history is available for the fix-evidence lookups.

The upstream checkout is a full tree. I'll grep it for the specific code paths each issue depends on.

Two early findings: upstream's `DocumentContentAccessor` has a subdirectory lock and case-insensitive comparison (relevant to #17995), while `DownloaderUtils` still uses `setDestinationInExternalPublicDir` (#18522). I'll read the relevant code for those and for #18411 and #18384.

The inserted system reminders sit in the user turn, so they are your instructions. They are coding conventions, and I'm not writing code for this read-only report, so they don't change the work. Continuing with the remaining code checks: #18411's toast path, #18384's stored-since filter, #18578's manifest, #17738's F-Droid changelogs, and #17199's sublist handling.

Confirmed so far: upstream has the #17995 fix, no opt-out property in the manifest (#18578), no F-Droid changelogs directory (#17738), and the #18411 toast path is still in place. A last batch checks averaging (#9398) and sublists on the map (#17199).

Averaging exists in upstream (`AveragedCoordsUtils`, used by `CoordinateInputDialog`), which may cover #9398. I'll verify that the waypoint editor uses that dialog.

The waypoint editor opens `CoordinateInputDialog`. I need to confirm the averaging action isn't limited to a different display mode.

Averaging is reachable from the waypoint editor's dialog (Normal/Waypoint modes), so #9398 looks fixed. Next I'll check the remaining three issues' snapshot entries.

## Summary
- Checked: 20
- Probably fixed: 2
- Duplicates: 0
- No longer applicable: 0
- Waiting for information: 0
- Keep open: 18

## Probably fixed

- [#17995](https://github.com/cgeo/cgeo/issues/17995) - Storage folder/file name issues with SAF
  - Reason: `DocumentContentAccessor` now has `findCreateSubdirectory` (synchronized) and a case-insensitive `findDocumentByName`, which addresses the reported duplicate/missing-folder problem (`main/src/main/java/cgeo/geocaching/storage/DocumentContentAccessor.java`, about lines 374-430). Confidence: medium.
  - Closing comment: "Thanks for the report. The current master code in `DocumentContentAccessor` (`findCreateSubdirectory` and `findDocumentByName`) handles this case, so we are closing this issue. If the problem persists in a current nightly, please comment or reopen and we will take a look."

- [#9398](https://github.com/cgeo/cgeo/issues/9398) - Average WP coords
  - Reason: The waypoint editor opens `CoordinateInputDialog` in Waypoint mode (`EditWaypointActivity.java:586`), and that dialog offers averaging through `AveragedCoordsUtils` on its "current location" button (`CoordinateInputDialog.java`, about lines 262-272). Confidence: medium.
  - Closing comment: "Thanks for the suggestion. Coordinate averaging is now available in the waypoint coordinate dialog (`AveragedCoordsUtils` in `CoordinateInputDialog`), so we are closing this issue. If you still need something beyond this, please comment or reopen."

## Keep open
[#17738](https://github.com/cgeo/cgeo/issues/17738), [#18469](https://github.com/cgeo/cgeo/issues/18469), [#18475](https://github.com/cgeo/cgeo/issues/18475), [#18407](https://github.com/cgeo/cgeo/issues/18407), [#18411](https://github.com/cgeo/cgeo/issues/18411), [#18384](https://github.com/cgeo/cgeo/issues/18384), [#17199](https://github.com/cgeo/cgeo/issues/17199), [#18381](https://github.com/cgeo/cgeo/issues/18381), [#18508](https://github.com/cgeo/cgeo/issues/18508), [#6153](https://github.com/cgeo/cgeo/issues/6153), [#18522](https://github.com/cgeo/cgeo/issues/18522), [#17195](https://github.com/cgeo/cgeo/issues/17195), [#18503](https://github.com/cgeo/cgeo/issues/18503), [#18536](https://github.com/cgeo/cgeo/issues/18536), [#12363](https://github.com/cgeo/cgeo/issues/12363), [#12552](https://github.com/cgeo/cgeo/issues/12552), [#18578](https://github.com/cgeo/cgeo/issues/18578), [#18581](https://github.com/cgeo/cgeo/issues/18581)

Notes:
- [#18411](https://github.com/cgeo/cgeo/issues/18411): `sendShowStatusToast` is still called (`Geocache.java:2176`, `2185`).
- [#18381](https://github.com/cgeo/cgeo/issues/18381): map legends exist, but not the auto-generated legend requested.
- [#6153](https://github.com/cgeo/cgeo/issues/6153): the oc.uk connector is still present.
- [#18522](https://github.com/cgeo/cgeo/issues/18522): still uses `setDestinationInExternalPublicDir` (`DownloaderUtils.java:292`).

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#17995](https://github.com/cgeo/cgeo/issues/17995): [PR #18001](https://github.com/cgeo/cgeo/pull/18001) "rel \#17995: serialize SAF subdir creation and use case-insensitive lookup", merged 2026-04-26, commit [f923464a27](https://github.com/cgeo/cgeo/commit/f923464a27687b401ae8f2c28bb6e1005c3f45a0) of 2026-04-26, added `findDocumentByName` in `main/src/main/java/cgeo/geocaching/storage/DocumentContentAccessor.java`.
- [#9398](https://github.com/cgeo/cgeo/issues/9398): [PR #18464](https://github.com/cgeo/cgeo/pull/18464) "Averaging coordinates in coordinate input/edit dialog (fix \#9398)", merged 2026-08-14, commit [8a2bc0fd55](https://github.com/cgeo/cgeo/commit/8a2bc0fd55babb4c76b74709b6e11b8c7c0e4573) of 2026-08-03, added `AveragedCoordsUtils` in `main/src/main/java/cgeo/geocaching/ui/dialog/CoordinateInputDialog.java`.

```cleanup-result
#17738 keep-open
#18469 keep-open
#18475 keep-open
#18407 keep-open
#18411 keep-open
#18384 keep-open
#17199 keep-open
#18381 keep-open
#18508 keep-open
#6153 keep-open
#18522 keep-open
#17195 keep-open
#17995 fixed
#18503 keep-open
#18536 keep-open
#9398 fixed
#12363 keep-open
#12552 keep-open
#18578 keep-open
#18581 keep-open
```
