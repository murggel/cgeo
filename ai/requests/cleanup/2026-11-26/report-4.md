<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 4/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 505.7 of 1500 used, 994.3 available beyond the reserve | workflow: d7e87ee585e88ddebec71b578af2d2517c5fd54c -->

I'll start by reading the 20 candidate issue files.

Most candidates are read. #18108 and #18228 were too large, so I'll read them in full alongside the first upstream checks.

#18108 is already closed upstream, and #18196's resume-reload path is still present. Next I'll check duplicates in the snapshot and the code paths for the remaining issues.

Key code findings: PMD is in `build.gradle` but not in any workflow; the deprecated actions from #18129 are gone; PebbleApp still hardcodes its package; `inventoryItems` still clamps on save. Now I'll check the snapshot for duplicates of the remaining topics.

**Summary**

- Checked: 20 issues
- Probably obsolete: 1
- Probably fixed: 0
- Duplicates: 0
- Waiting for information: 0
- Keep open: 19 (including #18108 and #18137, which are already closed upstream and need no action)

## No longer applicable

- [#18129](https://github.com/cgeo/cgeo/issues/18129): The report concerns deprecated GitHub Actions (`actions-ecosystem/action-add-labels`, `actions/github-script`). Neither appears in `upstream/.github` any more, and the workflows now use other jobs. Confidence: medium-high. The reporter (chrisdebian) already asked on 2026-06-07 whether it could be closed.

  Closing comment:
  > Thanks for the report. The deprecated actions mentioned here are no longer used in the workflows on master, so this issue no longer applies. Closing it for now. If the problem shows up again with the current workflows, please reopen or comment and we will take another look.

## Keep open

[#18114](https://github.com/cgeo/cgeo/issues/18114), [#18137](https://github.com/cgeo/cgeo/issues/18137) (already closed), [#17699](https://github.com/cgeo/cgeo/issues/17699) (PMD is configured in `build.gradle`, but no CI step runs it; worth a later look), [#18108](https://github.com/cgeo/cgeo/issues/18108) (already closed), [#18196](https://github.com/cgeo/cgeo/issues/18196) (reload-on-resume still present in `UnifiedMapActivity.java`), [#18167](https://github.com/cgeo/cgeo/issues/18167), [#17152](https://github.com/cgeo/cgeo/issues/17152), [#18233](https://github.com/cgeo/cgeo/issues/18233), [#18228](https://github.com/cgeo/cgeo/issues/18228), [#18289](https://github.com/cgeo/cgeo/issues/18289), [#18035](https://github.com/cgeo/cgeo/issues/18035), [#17969](https://github.com/cgeo/cgeo/issues/17969), [#4789](https://github.com/cgeo/cgeo/issues/4789), [#18120](https://github.com/cgeo/cgeo/issues/18120), [#18150](https://github.com/cgeo/cgeo/issues/18150), [#18342](https://github.com/cgeo/cgeo/issues/18342), [#18312](https://github.com/cgeo/cgeo/issues/18312) (`PebbleApp.java` still hardcodes the package), [#433](https://github.com/cgeo/cgeo/issues/433) (`DataStore.java` still clamps inventory to 0 on save), [#14881](https://github.com/cgeo/cgeo/issues/14881)

```cleanup-result
#18114 keep-open
#18137 keep-open
#17699 keep-open
#18108 keep-open
#18196 keep-open
#18129 obsolete
#18167 keep-open
#17152 keep-open
#18233 keep-open
#18228 keep-open
#18289 keep-open
#18035 keep-open
#17969 keep-open
#4789 keep-open
#18120 keep-open
#18150 keep-open
#18342 keep-open
#18312 keep-open
#433 keep-open
#14881 keep-open
```
