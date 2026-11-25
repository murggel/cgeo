<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 3/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 494.6 of 1500 used, 705.4 available beyond the reserve | workflow: 8c6dd3a0e6a5bb2ce4f7f91644e7cd6a3ab23cf2 -->

I'll start by checking which candidate issue files exist and locating the snapshot entries.

The snapshot has all 20 issues. Next I'll read the 20 candidate files in parallel.

I've read all 20 issues. Several need code checks in `upstream/`, so I'll verify the relevant code paths next.

The `google.navigation:q=` change from #15978 is already in upstream, and `nojit` still exists in `build.gradle`. Next I'll check the remaining code paths.

Findings so far: the `q=` navigation fix is in code, OkapiClient still uses a fixed 200 km radius, and no treasure or latitude filter exists. Next I'll check the remaining specifics: the translation fix, the advanced type filter, the map circle code, and the lab/captcha/driving-mode paths.

The translation crash path now uses `LocalizationUtils`, and the advanced type filter still omits MEGA/GIGA. I'll check those enum values and the remaining map, lab, and routing threading code.

Driving mode exists for VTM and Mapsforge but not Google Maps, and `IndividualRoute` still calls routing without a thread switch. Last, I'll check the type filter display values and the lab-linear and waypoint-visited code.

Mega and giga are still grouped under "Specials" in the type filter. I'll check the #11915 overlap with #17150, plus the hit-area commit, captcha manual-login, and waypoint quick-filter code.

## Summary

- Checked: 20 issues
- Probably fixed: 1 ([#17041](https://github.com/cgeo/cgeo/issues/17041))
- Duplicates: 0
- No longer applicable: 0
- Waiting for information: 0
- Keep open: 19

## Probably fixed

- [#17041](https://github.com/cgeo/cgeo/issues/17041) Beta version: IllegalStateException / missing context in DescriptionViewCreator
  - Reason: The reporter's crash came from `Fragment.getString` in a translation callback. The description-rendering path now uses `LocalizationUtils.getString(...)` (`main/src/main/java/cgeo/geocaching/CacheDetailActivity.java`, ~line 2005), and a commenter says the fix is #17113. I could not verify that PR from the checkout.
  - Confidence: medium
  - Closing comment: "Thanks for the report! The crash in the description view should be resolved by #17113, which no longer depends on the fragment context for these translations. If you still see this IllegalStateException in a current build, please comment here and we will reopen."

## Waiting for information

None.

## Keep open

[#15960](https://github.com/cgeo/cgeo/issues/15960), [#17076](https://github.com/cgeo/cgeo/issues/17076), [#15257](https://github.com/cgeo/cgeo/issues/15257), [#17137](https://github.com/cgeo/cgeo/issues/17137), [#15493](https://github.com/cgeo/cgeo/issues/15493), [#17150](https://github.com/cgeo/cgeo/issues/17150), [#17172](https://github.com/cgeo/cgeo/issues/17172), [#15978](https://github.com/cgeo/cgeo/issues/15978), [#17171](https://github.com/cgeo/cgeo/issues/17171), [#17179](https://github.com/cgeo/cgeo/issues/17179), [#17187](https://github.com/cgeo/cgeo/issues/17187), [#7279](https://github.com/cgeo/cgeo/issues/7279), [#11923](https://github.com/cgeo/cgeo/issues/11923), [#12017](https://github.com/cgeo/cgeo/issues/12017), [#15880](https://github.com/cgeo/cgeo/issues/15880), [#16060](https://github.com/cgeo/cgeo/issues/16060), [#17180](https://github.com/cgeo/cgeo/issues/17180), [#17201](https://github.com/cgeo/cgeo/issues/17201), [#17212](https://github.com/cgeo/cgeo/issues/17212)

Notes where a later look seems worthwhile:
- [#15978](https://github.com/cgeo/cgeo/issues/15978): `GoogleNavigationApp` now uses `q=`, but the Waze destination problem remains.
- [#11923](https://github.com/cgeo/cgeo/issues/11923): MEGA and GIGA are still grouped under "Specials" in `TypeGeocacheFilter`.
- [#17180](https://github.com/cgeo/cgeo/issues/17180): The reporter cites commit 85c102a0 as a hit-area increase, but I found no matching code. Confirm it.
- [#17179](https://github.com/cgeo/cgeo/issues/17179) and [#15880](https://github.com/cgeo/cgeo/issues/15880): Already closed on GitHub.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#17041](https://github.com/cgeo/cgeo/issues/17041): [PR #16910](https://github.com/cgeo/cgeo/pull/16910) "WIP: Make offline translation preserve HTML", merged 2025-05-04, commit [4631df147f](https://github.com/cgeo/cgeo/commit/4631df147f712bfece5b5be3c5bd55e6f635565c) of 2025-05-04, added `cache_description_translating_and_rendering` in `main/src/main/java/cgeo/geocaching/CacheDetailActivity.java`. The code is older than the issue, so this is probably not the fix.

```cleanup-result
#15960 keep-open
#17076 keep-open
#17041 fixed
#15257 keep-open
#17137 keep-open
#15493 keep-open
#17150 keep-open
#17172 keep-open
#15978 keep-open
#17171 keep-open
#17179 keep-open
#17187 keep-open
#7279 keep-open
#11923 keep-open
#12017 keep-open
#15880 keep-open
#16060 keep-open
#17180 keep-open
#17201 keep-open
#17212 keep-open
```
