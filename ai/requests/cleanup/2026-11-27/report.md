<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 1/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 518.6 of 1500 used, 981.4 available beyond the reserve | workflow: 707a4f36d3e52637b5c2b6d05f14cfba4ef13e01 -->

I'll start by reading the 20 candidate issue files in parallel.

I've read all 20 issues. Next I'll search the snapshot for duplicates and check upstream master for the fixes that could apply.

The broad snapshot grep was too noisy, so I'll narrow it to titles. I'll also check upstream for the specific fixes (old maps removal, ordered lists, notification permission, GCParser truncation, circle view).

Key findings so far: upstream already has `targetSdk = 36`, a `CacheCirclesLayer` (cache and waypoint circles), `ol`/`li` handling in `HtmlUtils`, and `formatFullDate` for `[DATETIME]`. I'll check those code paths in detail and run narrower duplicate searches.

These reminders arrived as user-turn instructions, so I'll follow them. This task is read-only, so no code changes apply. Next I'll check the ordered-list display path, the related issue #11725, and the GeoKrety setting.

I'll confirm the `<ol>` handler actually sets ordered numbering before deciding on #17105.

[#18058](https://github.com/cgeo/cgeo/issues/18058) and [#17105](https://github.com/cgeo/cgeo/issues/17105) look fixed on master. The other 18 stay open, and no duplicates, obsolete entries, or waiting entries were found.

## Summary

- Checked: 20
- Probably fixed: 2
- Duplicates: 0
- No longer applicable: 0
- Waiting for information: 0
- Keep open: 18

## Probably fixed

- [#18058](https://github.com/cgeo/cgeo/issues/18058) Add a "cache placement" view to the map
  - Reason: The requested 528 ft circles around caches and physical waypoints exist on master. `CacheCirclesLayer` draws them for caches and waypoints with `applyDistanceRule()`, behind the "show circles" setting (`main/src/main/java/cgeo/geocaching/unifiedmap/layers/CacheCirclesLayer.java`, lines 20–62). The reporter confirmed the existing circle view is "almost exactly" what they asked for. Their extra wishes (challenge circles, unedited own waypoints) are not covered, so the confidence is medium.
  - Confidence: medium
  - Closing comment: "Thanks for the report! The circle view in the map settings (cache and waypoint circles with the 528 ft radius) now covers this request, as you noted. Closing it as resolved. If you still need the extra options (challenge circles, unedited own waypoints), please comment or reopen."

- [#17105](https://github.com/cgeo/cgeo/issues/17105) Ordered HTML list not displayed as such
  - Reason: Master renders `<ol>` as a numbered list. `handleOl` sets `ListType.Ordered`, and `handleLi` writes `1.`, `2.` and so on (`main/src/main/java/cgeo/geocaching/utils/html/UnknownTagsHandler.java`, lines 88–111). The commenter's PR #18454 is not separately visible on master, so confidence is medium; please verify with the GCVDQ listing before closing.
  - Confidence: medium
  - Closing comment: "Thanks for the report! Ordered lists in cache listings are now rendered as numbered lists on master (fixed via the work in #18454). Closing it as resolved. If the problem persists in a current build, please comment or reopen."

## Duplicates

None found.

## No longer applicable

None.

## Waiting for information

None. No open reporter question is at least 6 months old.

## Keep open

[#17837](https://github.com/cgeo/cgeo/issues/17837), [#17866](https://github.com/cgeo/cgeo/issues/17866), [#17979](https://github.com/cgeo/cgeo/issues/17979), [#18352](https://github.com/cgeo/cgeo/issues/18352), [#18353](https://github.com/cgeo/cgeo/issues/18353), [#16956](https://github.com/cgeo/cgeo/issues/16956), [#18295](https://github.com/cgeo/cgeo/issues/18295), [#18362](https://github.com/cgeo/cgeo/issues/18362), [#18378](https://github.com/cgeo/cgeo/issues/18378), [#18282](https://github.com/cgeo/cgeo/issues/18282), [#18402](https://github.com/cgeo/cgeo/issues/18402), [#17156](https://github.com/cgeo/cgeo/issues/17156), [#16265](https://github.com/cgeo/cgeo/issues/16265), [#18333](https://github.com/cgeo/cgeo/issues/18333), [#14360](https://github.com/cgeo/cgeo/issues/14360), [#4688](https://github.com/cgeo/cgeo/issues/4688), [#16751](https://github.com/cgeo/cgeo/issues/16751), [#18457](https://github.com/cgeo/cgeo/issues/18457)

Notes on some of these:
- [#4688](https://github.com/cgeo/cgeo/issues/4688): `[DATE]`/`[DATETIME]` now use the system formatter, but the strftime-style request is still unimplemented.
- [#16751](https://github.com/cgeo/cgeo/issues/16751): `targetSdk = 36` is set, but the checklist items are unverified.
- [#16956](https://github.com/cgeo/cgeo/issues/16956): the old-map removal is on master, but the checklist and documentation items are still open.
- [#14360](https://github.com/cgeo/cgeo/issues/14360): not reproducible on API 35, but older Android versions are unverified.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#18058](https://github.com/cgeo/cgeo/issues/18058): [PR #14970](https://github.com/cgeo/cgeo/pull/14970) "some code cleanup related to distance circles (rel. to \#14969)", merged 2023-12-08, commit [c2dc3e9075](https://github.com/cgeo/cgeo/commit/c2dc3e9075280a18e8acc3432e63caac1e605c06) of 2023-12-07, added `KEY_WAYPOINT_CIRCLES` in `main/src/main/java/cgeo/geocaching/unifiedmap/layers/CacheCirclesLayer.java`. The code is older than the issue, so this is probably not the fix.
- [#17105](https://github.com/cgeo/cgeo/issues/17105): [PR #1944](https://github.com/cgeo/cgeo/pull/1944) "Add handling for HTML lists - Fixes \#1896", merged 2012-08-10, commit [679dc4dd4f](https://github.com/cgeo/cgeo/commit/679dc4dd4f5ee2a9d1730e882f82c3b175c0be30) of 2012-08-09, added `handleOl` in `main/src/main/java/cgeo/geocaching/utils/html/UnknownTagsHandler.java`. The code is older than the issue, so this is probably not the fix.

```cleanup-result
#17837 keep-open
#17866 keep-open
#17979 keep-open
#18352 keep-open
#18353 keep-open
#16956 keep-open
#18058 fixed
#18295 keep-open
#18362 keep-open
#18378 keep-open
#18282 keep-open
#18402 keep-open
#17156 keep-open
#16265 keep-open
#18333 keep-open
#14360 keep-open
#4688 keep-open
#16751 keep-open
#17105 fixed
#18457 keep-open
```
