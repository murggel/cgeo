<!-- task: cleanup-issues | upstream: cgeo/cgeo@428a9dad765cf3c240eb11bbd92e32a50a059624 | issues: 20 | issue snapshot: 2026-11-15 | provider: copilot 1.0.105 | workflow: efb572f4037bc256268bcaaa02630707106df9e6 -->

Reading all of them.

## c:geo issue cleanup: 20 issues checked

1 can probably be closed: 1 fixed, 0 duplicates, 0 obsolete, 0 waiting. The remaining 19 stay open.

## Probably fixed

- https://github.com/cgeo/cgeo/issues/447 – caches should be sorted relative to search centre, not phone coords
  - Reason: Coordinate and address searches now pass the search centre to the list as `Intents.EXTRA_COORDS` (`CacheListActivity.java:385-386`, `:1752`, `:1769`). `CacheListActivity.java:417` sets it as `GeocacheSort.targetCoords`. `GeocacheSort.java:38` and `:207-208` then use `SortType.TARGET_DISTANCE` with `TargetDistanceComparator`. `CacheListAdapter.java:470-476` also shows distances relative to that centre. Confidence: medium.
  - Closing comment: "Thanks for the suggestion! Lists from coordinate and address searches are now sorted by distance to the search centre instead of your current position, and the distances shown are relative to that centre. Closing as implemented. Please reopen or comment if you still see different behaviour."

## Keep open

[#1710](https://github.com/cgeo/cgeo/issues/1710), [#1679](https://github.com/cgeo/cgeo/issues/1679), [#734](https://github.com/cgeo/cgeo/issues/734) (the nearby list now goes through `CoordsGeocacheListLoader`, so offline behaviour is worth a look), [#3102](https://github.com/cgeo/cgeo/issues/3102) (a mid-point sort is not implemented; only the target-distance sort from #447 exists), [#749](https://github.com/cgeo/cgeo/issues/749) (still no c:geo licence headers in the sources), [#3486](https://github.com/cgeo/cgeo/issues/3486) (the EC connector still exists), [#3542](https://github.com/cgeo/cgeo/issues/3542) (searches are still merged per connector, only limited by a distance filter), [#3671](https://github.com/cgeo/cgeo/issues/3671), [#3806](https://github.com/cgeo/cgeo/issues/3806), [#4182](https://github.com/cgeo/cgeo/issues/4182) (pocket queries are still GC-specific), [#335](https://github.com/cgeo/cgeo/issues/335), [#4280](https://github.com/cgeo/cgeo/issues/4280), [#4130](https://github.com/cgeo/cgeo/issues/4130) (`goMap()` in `CacheListActivity.java:1627-1638` still opens the whole list), [#2781](https://github.com/cgeo/cgeo/issues/2781), [#4532](https://github.com/cgeo/cgeo/issues/4532) (no calibration hint in the code), [#1627](https://github.com/cgeo/cgeo/issues/1627) (`configChanges` is still used throughout `AndroidManifest.xml`), [#4495](https://github.com/cgeo/cgeo/issues/4495), [#1631](https://github.com/cgeo/cgeo/issues/1631) (tests now use fixed mock HTML under `androidTest/res/raw/mock`, so this may be obsolete, but I'm not sure), [#4744](https://github.com/cgeo/cgeo/issues/4744)

```cleanup-result
#1710 keep-open
#1679 keep-open
#447 fixed
#734 keep-open
#3102 keep-open
#749 keep-open
#3486 keep-open
#3542 keep-open
#3671 keep-open
#3806 keep-open
#4182 keep-open
#335 keep-open
#4280 keep-open
#4130 keep-open
#2781 keep-open
#4532 keep-open
#1627 keep-open
#4495 keep-open
#1631 keep-open
#4744 keep-open
```
