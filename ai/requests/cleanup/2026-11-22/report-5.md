<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 5/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 445.7 of 1500 used, 754.3 available beyond the reserve | workflow: 80e10c46acfc5ada8d2ff8809d23eb8d64f9209b -->

I'll start by reading the 20 candidate issue files in parallel.

Most files are read. Issue #11429 is too large to view whole, so I'll read it in ranges and also check the snapshot.

I still need the remaining comments on #11429 (22 in total). I'll read the rest of that file.

I've read all 20 issues. Next I'll check the upstream code for the claims that could resolve issues: language switch removal, GPX naming, the geochecker, activate-log dates, PQ filters, and the offline trackable loading.

The geochecker feature exists in `CheckerUtils.java`. Next I'll check the GPX export naming, the language setting, and the other code paths.

The GPX export code builds a filename from the list title, which looks like the #2724 fix. I'll look at that code, the app-language setting, the log-date handling, and the offline trackable loading.

Those reminders are repo style rules for code I'd write. This task is read-only, so I'm continuing the analysis. Next I'll check the remaining code paths: the trackable offline load, the language setting, the log-date handling, and the PQ filter.

Confirmed so far: GPX naming (#2724) and the geochecker (#4549) are present, while the app-language setting (#13387) and the trackable/PQ-filter paths still exist. A final batch checks the OC export type, the old map, and the favorites filter.

Two items still need a check: whether the old mapsforge v6 map still exists (for #8144), and the OC unknown-type export path (for #13374).

The old mapsforge v6 map files don't appear under `maps/`. I'll confirm whether that code was removed entirely, and check the mapsforge dependency for the unified map.

## Summary

Checked 20 issues: 2 probably fixed, 1 obsolete, 0 duplicates, 0 waiting for information, 17 keep open.

## Probably fixed

- [#2724](https://github.com/cgeo/cgeo/issues/2724) GPX export file naming
  - Reason: `calculateFileName` in `main/src/main/java/cgeo/geocaching/export/GpxExport.java` lines 56–71 names single-cache exports after the geocode and title, and list exports after the list title. Confidence: high.
  - Closing comment: "Thanks for the suggestion. GPX exports are now named after the cache (geocode and name) for single caches and after the list for list exports (see `GpxExport.calculateFileName`). Closing as implemented; please reopen or comment if the problem persists."

- [#4549](https://github.com/cgeo/cgeo/issues/4549) Checker for challenge caches
  - Reason: `main/src/main/java/cgeo/geocaching/utils/CheckerUtils.java` lines 22–31 define known geocheckers, and `main/src/main/java/cgeo/geocaching/CacheDetailActivity.java` lines 594–605 opens the checker for a cache. The reporter and maintainers agreed in 2020 that this is sufficient. Confidence: medium, because the requested project-gc API was not built.
  - Closing comment: "The cache detail page already offers a geochecker lookup for challenge checkers (`CheckerUtils`, menu "Open Geochecker"). Closing on this basis; feel free to reopen if a different check is needed."

## No longer applicable

- [#8144](https://github.com/cgeo/cgeo/issues/8144) Map tiles get repainted each time screen is turned on
  - Reason: The report points to `NewMap.java` in the mapsforge v6 map. That code no longer exists in upstream, and no `maps.mapsforge.v6` references remain. The maintainer noted in 2022 that the unified map replaces it. Confidence: medium.
  - Closing comment: "The mapsforge v6 map this report refers to has been removed and replaced by the unified map. Closing as obsolete; please reopen if the tile redraw still happens in the current nightly."

## Keep open

[#13308](https://github.com/cgeo/cgeo/issues/13308), [#13321](https://github.com/cgeo/cgeo/issues/13321), [#13336](https://github.com/cgeo/cgeo/issues/13336), [#13374](https://github.com/cgeo/cgeo/issues/13374), [#13359](https://github.com/cgeo/cgeo/issues/13359), [#13387](https://github.com/cgeo/cgeo/issues/13387), [#11429](https://github.com/cgeo/cgeo/issues/11429), [#13388](https://github.com/cgeo/cgeo/issues/13388), [#13444](https://github.com/cgeo/cgeo/issues/13444), [#3282](https://github.com/cgeo/cgeo/issues/3282), [#13492](https://github.com/cgeo/cgeo/issues/13492), [#13506](https://github.com/cgeo/cgeo/issues/13506), [#13559](https://github.com/cgeo/cgeo/issues/13559), [#13564](https://github.com/cgeo/cgeo/issues/13564), [#13552](https://github.com/cgeo/cgeo/issues/13552), [#13603](https://github.com/cgeo/cgeo/issues/13603), [#13614](https://github.com/cgeo/cgeo/issues/13614)

Notes:
- [#13387](https://github.com/cgeo/cgeo/issues/13387): The app-language setting still exists (`Settings.getUserLanguage`), so the report still applies.
- [#13614](https://github.com/cgeo/cgeo/issues/13614): The maintainer's own note shows the fix is still in progress.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#2724](https://github.com/cgeo/cgeo/issues/2724): commit [fa3d6a1497](https://github.com/cgeo/cgeo/commit/fa3d6a1497b081e503ab64b4415426de288d681c) of 2015-04-22 (no pull request), added `private void calculateFileName` in `main/src/main/java/cgeo/geocaching/export/GpxExport.java`.
- [#4549](https://github.com/cgeo/cgeo/issues/4549): [PR #12134](https://github.com/cgeo/cgeo/pull/12134) "pass current cache coordinates to geochecker", merged 2021-11-28, commit [ec5c9a3274](https://github.com/cgeo/cgeo/commit/ec5c9a3274da77dfdd3e681e028e237eb4826a4d) of 2021-11-28, added `GeoChecker[] CHECKERS` in `main/src/main/java/cgeo/geocaching/utils/CheckerUtils.java`.

```cleanup-result
#13308 keep-open
#13321 keep-open
#13336 keep-open
#13374 keep-open
#13359 keep-open
#4549 fixed
#13387 keep-open
#11429 keep-open
#13388 keep-open
#13444 keep-open
#3282 keep-open
#13492 keep-open
#13506 keep-open
#2724 fixed
#8144 obsolete
#13559 keep-open
#13564 keep-open
#13552 keep-open
#13603 keep-open
#13614 keep-open
```
