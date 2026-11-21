<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 5/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 430.4 of 1500 used, 769.6 available beyond the reserve | workflow: f8ce42a851cf3a1b6b9d29231137a189435025f9 -->

I'll start by checking which candidate files exist and how large they are.

All 20 requested candidate files exist. Reading them now.

I've read all 20 candidates. Next I'll search the snapshot for duplicates and check the upstream code for each feature or bug.

The snapshot shows #3954 (custom WMS/map sources) overlapping #1286. Now I'll look at the upstream tree layout and the relevant code paths.

Key finding: `res/layout` is still flat, but `userdefined_tileprovider_preference_dialog.xml` exists, suggesting custom tile providers (relevant to #1286). The `viewpagerindicator` folder is gone. Now I'll grep the upstream code for each feature and bug.

Confirmed so far: custom tile providers exist (#1286 fixed), GK tracking-code lookup exists (#5206 fixed), and `FastScrollListener` still ships. Next I'll check the EC null-login path, the ignore-list UI, batch found-state, the NM/NA log restriction, and a few others.

The last two messages are user-turn instructions about coding style and build commands. My task is a read-only report, so they don't change what I'm doing; I'll continue the analysis. Next: the EC connector (ECApi looks much shorter than expected), the ignore capability, and the remaining checks.

Several results are now clear: the EC search code was removed (#10656), and the ignore-removal method exists but has no UI caller (#11439). Batch found-state and the flat layout folder are still missing. I'll check the last few: repo top level, waypoint-type defaults, and the ALC load-more path.

ALConnector no longer implements `ISearchByNextPage`, so the "Load more" path in #10568 is gone. Last step: check the snapshot for duplicates of the remaining candidates.

That search was too broad. I'll narrow it to the specific referenced issue numbers and a few exact phrases.

## Summary

Checked 20 issues. Probably closeable: 4.
- Fixed: 2
- Duplicate: 0
- Obsolete: 2
- Waiting for information: 0
- Keep open: 16

## Probably fixed

- [#1286](https://github.com/cgeo/cgeo/issues/1286) Support of eniro maps
  - Reason: Custom tile-based online map sources are now supported. Users can add any tile URL via `PrefUserDefinedTileProvider` (`main/src/main/java/cgeo/geocaching/unifiedmap/tileproviders/PrefUserDefinedTileProvider.java`, lines 19–34). `TileProviderFactory.java` (lines 102–135) builds map sources from them, and a settings dialog exists (`settings/UserDefinedTileProviderPreference.java`). Eniro's tile URL can be entered there. Confidence: medium.
  - Closing comment: "Thanks for the request! c:geo now lets you add custom tile-based online map sources in the map sources settings, so Eniro tiles can be configured by URL. Closing as fixed. If it doesn't work for you, please reopen or comment."

- [#5206](https://github.com/cgeo/cgeo/issues/5206) GK: Search by tracking code
  - Reason: The GeoKrety connector now looks up trackables by tracking code via the GK export API (`main/src/main/java/cgeo/geocaching/connector/trackable/GeokretyConnector.java`, lines 135–140 and 302–316, `getGeocodeFromTrackingCode`). Confidence: high.
  - Closing comment: "Searching GeoKrety by tracking code is now supported in the GK connector (`GeokretyConnector`). Closing as fixed. Please reopen or comment if it still fails for a specific code."

## No longer applicable

- [#10656](https://github.com/cgeo/cgeo/issues/10656) catch IllegalArgumentException for EC active without login information
  - Reason: The EC search code that threw this exception was removed. `main/src/main/java/cgeo/geocaching/connector/ec/ECApi.java` now only contains `getIdFromGeocode`, and `ECConnector` no longer implements a viewport search. The reported code path does not exist. Confidence: high.
  - Closing comment: "The EC connector no longer performs the viewport search that produced this exception, so the report no longer applies. Closing. Please reopen if you still see it with a current version."

- [#10568](https://github.com/cgeo/cgeo/issues/10568) Filtering for ALC fails after "Load more" in search results
  - Reason: `ALConnector` no longer implements paging (`ISearchByNextPage`; declaration at `main/src/main/java/cgeo/geocaching/connector/al/ALConnector.java`, line 31), so there is no "Load more" path. The Adventure Lab type filter is now applied in the filter chain (`ALApi.java`, lines 237–248). Confidence: medium.
  - Closing comment: "The Adventure Lab connector has been reworked. Its search no longer uses the 'Load more' paging described here, and the type filter is applied in the filter chain. Closing as no longer applicable. Please reopen if the filter is still lost with a current version."

## Keep open

[#10547](https://github.com/cgeo/cgeo/issues/10547), [#10375](https://github.com/cgeo/cgeo/issues/10375), [#10642](https://github.com/cgeo/cgeo/issues/10642), [#10686](https://github.com/cgeo/cgeo/issues/10686), [#11027](https://github.com/cgeo/cgeo/issues/11027), [#10980](https://github.com/cgeo/cgeo/issues/10980), [#9699](https://github.com/cgeo/cgeo/issues/9699), [#11377](https://github.com/cgeo/cgeo/issues/11377), [#11413](https://github.com/cgeo/cgeo/issues/11413), [#11439](https://github.com/cgeo/cgeo/issues/11439), [#11469](https://github.com/cgeo/cgeo/issues/11469), [#11518](https://github.com/cgeo/cgeo/issues/11518), [#11579](https://github.com/cgeo/cgeo/issues/11579), [#2226](https://github.com/cgeo/cgeo/issues/2226), [#7333](https://github.com/cgeo/cgeo/issues/7333), [#11497](https://github.com/cgeo/cgeo/issues/11497)

Worth a later look:
- #11497: the newer [#18837](https://github.com/cgeo/cgeo/issues/18837) (logbook scrolling) covers the same area.
- #11439: `removeFromIgnorelist` exists in the connectors but has no UI caller.
- #10547: found-state only exists for single caches (`CacheMenuHandler.java`).
- #10686: the `project/` folder is absent upstream, but I could not confirm the outdated images were removed.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#1286](https://github.com/cgeo/cgeo/issues/1286): [PR #18586](https://github.com/cgeo/cgeo/pull/18586) "Support multiple user-defined tile providers", merged 2026-09-11, commit [1df6f9ea24](https://github.com/cgeo/cgeo/commit/1df6f9ea24d8b351e5ecd8205ed48060bbf784b2) of 2026-09-11, added `public class PrefUserDefinedTileProvider` in `main/src/main/java/cgeo/geocaching/unifiedmap/tileproviders/PrefUserDefinedTileProvider.java`.
- [#5206](https://github.com/cgeo/cgeo/issues/5206): [PR #5368](https://github.com/cgeo/cgeo/pull/5368) "Support links encoded in some GeoKrety QRCode", merged 2016-01-19, commit [157a3d16bc](https://github.com/cgeo/cgeo/commit/157a3d16bcec7a5d214d440d51bdd3901f3c6d65) of 2015-08-30, added `getGeocodeFromTrackingCode` in `main/src/main/java/cgeo/geocaching/connector/trackable/GeokretyConnector.java`. The code is older than the issue, so this is probably not the fix.

```cleanup-result
#10568 obsolete
#10547 keep-open
#10375 keep-open
#10642 keep-open
#10656 obsolete
#10686 keep-open
#11027 keep-open
#10980 keep-open
#9699 keep-open
#11377 keep-open
#11413 keep-open
#11439 keep-open
#11469 keep-open
#11518 keep-open
#1286 fixed
#11579 keep-open
#2226 keep-open
#5206 fixed
#7333 keep-open
#11497 keep-open
```
