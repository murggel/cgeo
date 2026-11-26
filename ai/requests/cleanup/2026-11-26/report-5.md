<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 5/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 505.7 of 1500 used, 994.3 available beyond the reserve | workflow: d7e87ee585e88ddebec71b578af2d2517c5fd54c -->

I'll start by reading the 20 candidate issue files and checking which exist.

I've read all 20 candidates. Next I'll search the snapshot for duplicates and check the upstream master code for the fix-candidate issues.

The snapshot search was truncated, so I'll run narrower topic searches for each candidate, along with checks on the upstream code.

Snapshot duplicates look sparse so far. Now I'll check the upstream master code for the key fix candidates.

Several promising leads: the `showCircles` setting, `PermissionContext.NOTIFICATIONS`, the `ol` handling and `DATETIME` template. I'll inspect those code paths.

Continuing the checks. The GCParser null-safe comparison at line 234 and the `</table>` guard at 577-579 look relevant to #16265, and the `ol` handling in `UnknownTagsHandler` is relevant to #17105.

Circles of 528 ft around caches and waypoints exist in `CacheCirclesLayer.java`, which resolves #18058. One last check on the long-tap "remove from list" option for #17837.

1. **Summary:** 20 issues checked. Probably closable: 1 fixed, 0 duplicate, 0 obsolete, 0 waiting. 19 keep open.

2. **Probably fixed**

- [#18058](https://github.com/cgeo/cgeo/issues/18058) Add a "cache placement" view to the map
  - Reason: The requested 528 ft circles around caches and waypoints are drawn on the live map when "show circles" is enabled (`CacheCirclesLayer.java`, radius line 23, draws for caches and waypoints at lines 37 and 56). The reporter confirmed the circle view was "almost exactly" the request. Follow-up ideas (challenge circles, unpublished caches, which an open PR touches) are separate scope. Confidence: medium.
  - Closing comment: "Thanks for the report! The map's circle overlay (Show circles, 528 ft around caches and waypoints) covers this request, so I'm closing it as implemented. If it doesn't cover your case, please reopen or comment with details, and feel free to open separate issues for the extra ideas."

3. **Keep open:** [#17837](https://github.com/cgeo/cgeo/issues/17837) (long-tap "remove from list" may suffice; reporter agreed, so a later look is worthwhile), [#17866](https://github.com/cgeo/cgeo/issues/17866) (thank-you note, not actionable), [#17979](https://github.com/cgeo/cgeo/issues/17979), [#18352](https://github.com/cgeo/cgeo/issues/18352) (`gl` not in locales), [#18353](https://github.com/cgeo/cgeo/issues/18353) (`in`/`iw` still used), [#16956](https://github.com/cgeo/cgeo/issues/16956) (old-map code removed on master, checklist still open), [#18295](https://github.com/cgeo/cgeo/issues/18295) (permission still requested in `InstallWizardActivity`), [#18362](https://github.com/cgeo/cgeo/issues/18362) (PR #18361 open), [#18378](https://github.com/cgeo/cgeo/issues/18378), [#18282](https://github.com/cgeo/cgeo/issues/18282) (icon still being revised), [#18402](https://github.com/cgeo/cgeo/issues/18402), [#17156](https://github.com/cgeo/cgeo/issues/17156), [#16265](https://github.com/cgeo/cgeo/issues/16265) (unchecked `substring` in `parseWaypoints` remains, assigned), [#18333](https://github.com/cgeo/cgeo/issues/18333), [#14360](https://github.com/cgeo/cgeo/issues/14360) (not reproducible on API 35, needs older-device check), [#4688](https://github.com/cgeo/cgeo/issues/4688) (`[DATETIME]` now uses locale formatting, but strftime request remains; worth splitting), [#16751](https://github.com/cgeo/cgeo/issues/16751) (tracker; targetSdk 36 set, predictive back partial), [#17105](https://github.com/cgeo/cgeo/issues/17105) (ordered-list code exists, but the listing fix PR #18454 is unverified), [#18457](https://github.com/cgeo/cgeo/issues/18457)

4. ```fix-evidence
#18058 main/src/main/java/cgeo/geocaching/unifiedmap/layers/CacheCirclesLayer.java 528.0 * IConversion.FEET_TO_KILOMETER
```

5. ```cleanup-result
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
#17105 keep-open
#18457 keep-open
```
