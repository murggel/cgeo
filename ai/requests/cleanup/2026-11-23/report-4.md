<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 4/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 463.9 of 1500 used, 736.1 available beyond the reserve | workflow: 1d3a4543eb6f7e4963e3872cb0392abc1ae9da40 -->

I'll start by checking which candidate files exist, then read the issue texts.

I've read all 20 candidate issues. None has an unanswered question to the reporter, so "waiting" looks empty. Next I'll search the snapshot for duplicates and the upstream code for the reported behaviour.

The snapshot search was truncated, so I'll run narrower searches for the topics that matter.

The snapshot shows no clear duplicates. Now I'll check the upstream code for the main claims, starting with the features most likely to exist already.

Several leads: the 81er matrix filter and live gc.com fill appear to exist, and the download dialog may already check for new caches. I'll read those code paths and check the remaining claims.

I'll keep going with the analysis; the reminders about code style don't affect this read-only report, since I'm not writing or changing any files. Next I'm checking the GeoKrety coordinate handling, the Locus waypoint callers, the undo and drag-reorder code, and the GeoKrety log-text option.

Findings so far: the live-map "zoom in" partial-results message exists (likely closes #9340), and the GeoKrety log still sends coordinates only when known. I'll confirm the live-map usage, how history deletion is wired, and the favorite-point check.

The live-map partial-results message is wired in `UnifiedMapActivity`, so #9340 looks fixed. Last check: the favorite-points path for #13309 and the history delete path for #14823.

Summary: 20 issues checked. Probably fixed: 2 (#14579 high, #9340 medium). Duplicates: 0. No longer applicable: 0. Waiting for information: 0. Keep open: 18, including #14158, which is only partly addressed.

## Probably fixed

- [#14579](https://github.com/cgeo/cgeo/issues/14579) 81er matrix filter: the gc.com fill button and the matrix-to-online-search wiring exist (`main/src/main/java/cgeo/geocaching/filters/gui/DifficultyTerrainMatrixFilterViewHolder.java` lines 39-46; `GCWebAPI.java` `getNeededDifficultyTerrainCombisFor81Matrix`). Confidence: high.
  - Closing comment: "Thanks for the report. The 81er difficulty/terrain matrix filter now includes a 'Fill with gc.com' button and passes the matrix to the online search, so this request appears to be implemented. If the problem persists, please reopen or comment with details."
- [#9340](https://github.com/cgeo/cgeo/issues/9340) Live map limit notice: the partial-results message is shown in `main/src/main/java/cgeo/geocaching/unifiedmap/UnifiedMapActivity.java` (line 685), with the string in `main/src/main/res/values/strings.xml` (line 2837). Confidence: medium, because I did not fully verify the exact wording requested in the issue.
  - Closing comment: "Thanks for the suggestion. The live map now shows a status message telling you to zoom in when results are partial, which covers this request. If the problem persists, please reopen or comment."

## Duplicates

None found.

## No longer applicable

None.

## Waiting for information

None. No target issue has an unanswered question to the reporter that is at least six months old.

## Keep open

[#13309](https://github.com/cgeo/cgeo/issues/13309), [#14621](https://github.com/cgeo/cgeo/issues/14621), [#14643](https://github.com/cgeo/cgeo/issues/14643), [#14670](https://github.com/cgeo/cgeo/issues/14670), [#14674](https://github.com/cgeo/cgeo/issues/14674), [#6225](https://github.com/cgeo/cgeo/issues/6225), [#8996](https://github.com/cgeo/cgeo/issues/8996), [#9183](https://github.com/cgeo/cgeo/issues/9183), [#9399](https://github.com/cgeo/cgeo/issues/9399), [#14698](https://github.com/cgeo/cgeo/issues/14698), [#14719](https://github.com/cgeo/cgeo/issues/14719), [#12891](https://github.com/cgeo/cgeo/issues/12891), [#14745](https://github.com/cgeo/cgeo/issues/14745), [#14795](https://github.com/cgeo/cgeo/issues/14795), [#14816](https://github.com/cgeo/cgeo/issues/14816), [#14824](https://github.com/cgeo/cgeo/issues/14824), [#14158](https://github.com/cgeo/cgeo/issues/14158), [#14823](https://github.com/cgeo/cgeo/issues/14823)

Notes: #14158 is only partly fixed (scroll preserved, but the reporter's other asks are not addressed). #9183 is still present (`AbstractLocusCacheListApp.java` line 37).

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#14579](https://github.com/cgeo/cgeo/issues/14579): [PR #14587](https://github.com/cgeo/cgeo/pull/14587) "fix \#14579: add difficulty terrain matrix filter", merged 2023-09-10, commit [61685ddf17](https://github.com/cgeo/cgeo/commit/61685ddf176406b1bb4d53f9bb2db2134b838b5e) of 2023-09-10, added `cache_filter_difficulty_terrain_matrix_fill_with_gc_data` in `main/src/main/java/cgeo/geocaching/filters/gui/DifficultyTerrainMatrixFilterViewHolder.java`.
- [#9340](https://github.com/cgeo/cgeo/issues/9340): [PR #16508](https://github.com/cgeo/cgeo/pull/16508) "Live map status visuals", merged 2025-01-04, commit [102c22c357](https://github.com/cgeo/cgeo/commit/102c22c35782642a851c979e5c4aeba052cb8041) of 2025-01-04, added `live_map_status_partial` in `main/src/main/res/values/strings.xml`.

```cleanup-result
#13309 keep-open
#14621 keep-open
#14643 keep-open
#14670 keep-open
#14674 keep-open
#6225 keep-open
#8996 keep-open
#9183 keep-open
#9399 keep-open
#14698 keep-open
#9340 fixed
#14719 keep-open
#12891 keep-open
#14745 keep-open
#14579 fixed
#14795 keep-open
#14816 keep-open
#14824 keep-open
#14158 keep-open
#14823 keep-open
```
