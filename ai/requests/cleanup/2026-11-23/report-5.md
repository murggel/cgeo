<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 5/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 463.9 of 1500 used, 736.1 available beyond the reserve | workflow: 1d3a4543eb6f7e4963e3872cb0392abc1ae9da40 -->

I'll start by checking which candidate files exist and what the snapshot looks like.

All 20 candidate files are present. Reading them now.

Ten read so far. The rest are next, including #11927, which needs the large-file flag.

#14706 is the only file still unread; it's over the size limit, so I'll force-read it. #15071 shows as already closed upstream, which I'll note.

I've read all 20 candidates. Next I'll check the snapshot for duplicates, using targeted keywords and the referenced issue numbers.

That was too broad. I'll run narrower searches for the specific topics and cross-referenced numbers.

The combined pattern matched too much. I'll run several narrow searches in parallel instead.

Results are still too noisy. I'll check the specific cross-referenced numbers by exact line prefix.

The anchored search found nothing, including for candidate numbers themselves, so I'll check the snapshot format directly for a few candidates.

The snapshot confirms #7279, #7831, #13515 and #16370 are still open, which helps the duplicate check. Next I'll check the current code for the reported behaviours, starting with the relevant connector, marker, notification and export code.

The code shows a link-correction helper in `TextUtils` that may cover #15071. I'll read it alongside the personal-note link code and check the other specific features.

The personal-note link path now has a dedicated end-of-link correction (`TextUtils.getWebLinkEnd` / `ViewUtils`), which likely covers #15071. Next I'll check the field-note export, notification dot, log templates and OC nearby radius.

I'll read the notification-badge code, the link-end correction, and the field-note export to check the upload logic.

These reminders arrived as user-turn messages, not inside a tool result, so I'll follow them. This task is read-only, so they change nothing here. Next I'll check the field-note upload filter and the OC nearby radius.

My earlier notes cover only some of the 20 issues, and the details of the rest are gone from context. I'll re-read the candidate files so the report is accurate.

I have the text of all 20 issues. Next I'll read the two large files and check the code for the remaining feature and bug requests.

Next I'll read the two large files via targeted grep and check the code for the feature requests.

Most issues look like keep-open or feature requests. Several still need a check: #11927's last comments, #14983's background upload, #15071/#14989 code locations, #4594's OC distance code, and #10580's hemisphere handling.

The #14983 fix is confirmed, and #11927 has an unanswered question to the reporter from 2024-02-02. Last, I'll search the snapshot for duplicates of the open feature requests.

No clear duplicates in that list. One last targeted snapshot search for #10580 and #14266 before writing the report.

## Summary

- Checked: 20 issues
- Probably fixed: 3
- Duplicates: 0
- No longer applicable: 0
- Waiting for information: 1
- Keep open: 16

## Probably fixed

- [#15071](https://github.com/cgeo/cgeo/issues/15071) Hyperlink in personal note is not parsed correctly. Already closed upstream. The link-end correction exists in `main/src/main/java/cgeo/geocaching/ui/ViewUtils.java` (lines 824–860, `fixWebLinkEnds` with `TextUtils.getWebLinkEnd`) and is applied to the personal note in `main/src/main/java/cgeo/geocaching/CacheDetailActivity.java` line 3021. Confidence: medium. No action needed, since it is already closed.
  - Closing comment: "Closing as fixed: web link ends in personal notes are now corrected (`ViewUtils.fixWebLinkEnds`). Please reopen or comment if the link still opens with the trailing bracket."
- [#14989](https://github.com/cgeo/cgeo/issues/14989) No notification dot shown when directly launching into map. Message-center notifications now update the home badge via `MessageCenterUtils.setReceiver(this, intent -> updateHomeBadge(1))` in `main/src/main/java/cgeo/geocaching/activity/AbstractNavigationBarActivity.java` (line 219). The reporter's comment says this works since 2023.12.11. Confidence: medium.
  - Closing comment: "Closing as fixed: message-center notifications now show the badge in the bottom navigation, including when c:geo starts in map mode. Please reopen or comment if the dot is still missing."
- [#14983](https://github.com/cgeo/cgeo/issues/14983) Move batch uploading notes/coords to background with proper notification. `main/src/main/java/cgeo/geocaching/service/UploadCoordinatesBatchService.java` runs the upload as a background batch with a completion notification (`getCompletedText`, `getInterruptedText`). Confidence: high.
  - Closing comment: "Closing as fixed: coordinate uploads now run as a background batch service with a completion notification. Please reopen or comment if the result is still not shown."

## Duplicates

None found in the snapshot.

## Waiting for information

- [#11927](https://github.com/cgeo/cgeo/issues/11927) [Nightly] App Crash when leaving or rotating Live Map while it's still rendering. The last question, from moving-bits on 2024-02-02, asks whether this also happens with UnifiedMap. The reporter has not answered in more than 6 months. Confidence: medium.
  - Closing comment: "Closing for lack of feedback: the question from 2024-02-02 about UnifiedMap is still unanswered. Please reopen with your result and the logcat if the crash still happens on a current version."

## Keep open

[#10580](https://github.com/cgeo/cgeo/issues/10580), [#10676](https://github.com/cgeo/cgeo/issues/10676), [#10712](https://github.com/cgeo/cgeo/issues/10712), [#4671](https://github.com/cgeo/cgeo/issues/4671), [#14935](https://github.com/cgeo/cgeo/issues/14935), [#14955](https://github.com/cgeo/cgeo/issues/14955), [#14266](https://github.com/cgeo/cgeo/issues/14266), [#15119](https://github.com/cgeo/cgeo/issues/15119), [#15196](https://github.com/cgeo/cgeo/issues/15196), [#4594](https://github.com/cgeo/cgeo/issues/4594), [#10358](https://github.com/cgeo/cgeo/issues/10358), [#13540](https://github.com/cgeo/cgeo/issues/13540), [#14706](https://github.com/cgeo/cgeo/issues/14706), [#15246](https://github.com/cgeo/cgeo/issues/15246), [#15252](https://github.com/cgeo/cgeo/issues/15252), [#14010](https://github.com/cgeo/cgeo/issues/14010)

Worth a later look:
- [#14935](https://github.com/cgeo/cgeo/issues/14935): `main/src/main/java/cgeo/geocaching/export/FieldNoteExportTask.java` (lines 168–176) still sends the whole file to every connector.
- [#4594](https://github.com/cgeo/cgeo/issues/4594): `DEFAULT_RADIUS = "200"` in `main/src/main/java/cgeo/geocaching/connector/oc/OkapiClient.java` (line 211) is still in place.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#15071](https://github.com/cgeo/cgeo/issues/15071): [PR #18894](https://github.com/cgeo/cgeo/pull/18894) "Fix \#15071: correct the end of links in the personal note", merged 2026-11-15, commit [2ef71b5603](https://github.com/cgeo/cgeo/commit/2ef71b560305bfca3e5ff70607913a59207ecde2) of 2026-11-11, added `fixWebLinkEnds` in `main/src/main/java/cgeo/geocaching/ui/ViewUtils.java`.
- [#14989](https://github.com/cgeo/cgeo/issues/14989): [PR #14889](https://github.com/cgeo/cgeo/pull/14889) "Fixes for Message Center notifications", merged 2023-11-27, commit [0f1bd4259c](https://github.com/cgeo/cgeo/commit/0f1bd4259cc941f4d39c2c4603bf15994d37f9ca) of 2023-11-25, added `MessageCenterUtils.setReceiver(this, intent -> updateHomeBadge(1))` in `main/src/main/java/cgeo/geocaching/activity/AbstractNavigationBarActivity.java`. The code is older than the issue, so this is probably not the fix.
- [#14983](https://github.com/cgeo/cgeo/issues/14983): [PR #18596](https://github.com/cgeo/cgeo/pull/18596) "Abstract progress handler for batch-processing", merged 2026-10-11, commit [d6410eac66](https://github.com/cgeo/cgeo/commit/d6410eac66cf7dad985688817d84d2ca064235c6) of 2026-10-11, added `export_modifiedcoords_background_result` in `main/src/main/java/cgeo/geocaching/service/UploadCoordinatesBatchService.java`.

```cleanup-result
#15071 fixed
#14989 fixed
#14983 fixed
#11927 waiting
#10580 keep-open
#10676 keep-open
#10712 keep-open
#4671 keep-open
#14935 keep-open
#14955 keep-open
#14266 keep-open
#15119 keep-open
#15196 keep-open
#4594 keep-open
#10358 keep-open
#13540 keep-open
#14706 keep-open
#15246 keep-open
#15252 keep-open
#14010 keep-open
```
