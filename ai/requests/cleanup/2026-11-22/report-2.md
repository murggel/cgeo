<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 2/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 445.7 of 1500 used, 754.3 available beyond the reserve | workflow: 80e10c46acfc5ada8d2ff8809d23eb8d64f9209b -->

I'll read the 20 candidate issue files first, then check the snapshot and upstream code for each.

I've read all 20 candidates. Next I'll search the snapshot for duplicates and check the relevant upstream code paths.

The snapshot search was too broad. I'll look up specific issue numbers and topic terms, and in parallel check the upstream code for the remaining candidates.

Several candidates have possible duplicates or fixes: #12459 vs #12363, #12545 vs #15979. I'll check the upstream code for the coordinate parser, watchlist error handling, GeoKret date, Travel Bug map, co-owners, EXIF location, and Sonar config.

Upstream parses GeoKret dates explicitly in UTC, which looks like it may be the #8884 fix. I'll verify that along with the watchlist response handling, the coordinate parser, and the waypoint list-marker code.

Continuing the checks. The custom instructions you sent concern code I'm not writing here, so they don't change this read-only report. I'll finish by checking whether the DMS parser accepts a trailing hemisphere (#12504).

# Summary

Checked 20 issues. Probably closeable: 1 (1 duplicate). 0 fixed, 0 obsolete, 0 waiting, 19 keep open.

## Duplicates

- [#12459](https://github.com/cgeo/cgeo/issues/12459) Heat Live map: Colors icon by Favorites
  - Reason: The reporter's wish for favorite-based cache coloring is covered by the broader, still-open [#12363](https://github.com/cgeo/cgeo/issues/12363) (fully customizable cache icons/markers), which a maintainer pointed to in the thread. Confidence: medium. I did not verify the full text of #12363 for favorites, so please check that first.
  - Closing comment:
    > Thanks for the idea! This is covered by the more general request #12363 (fully customizable cache icons/markers), so we're closing this one as a duplicate and continuing the discussion there. If you feel something specific to favorites is missing, please comment on #12363 or reopen this issue.

## Keep open

[#4319](https://github.com/cgeo/cgeo/issues/4319) (2021 maintainer suggestion to split into dedicated issues; closing is a maintainer decision), [#5986](https://github.com/cgeo/cgeo/issues/5986) (online webview exists, offline one still requested), [#6272](https://github.com/cgeo/cgeo/issues/6272) (`metadata-extractor` is still used for GPS location, `main/src/main/java/cgeo/geocaching/utils/MetadataUtils.java` 70-77), [#6855](https://github.com/cgeo/cgeo/issues/6855) (disputed design question), [#8286](https://github.com/cgeo/cgeo/issues/8286), [#8805](https://github.com/cgeo/cgeo/issues/8805), [#8884](https://github.com/cgeo/cgeo/issues/8884) (GeoKret date now parsed as UTC in `GeokretyParser.java` 47, but not verified against the original bug), [#12389](https://github.com/cgeo/cgeo/issues/12389), [#12428](https://github.com/cgeo/cgeo/issues/12428), [#12498](https://github.com/cgeo/cgeo/issues/12498) (reporter and maintainer say more optimization is possible), [#11926](https://github.com/cgeo/cgeo/issues/11926), [#12504](https://github.com/cgeo/cgeo/issues/12504) (trailing-hemisphere parser exists only for decimal degrees, `main/src/main/java/cgeo/geocaching/location/GeopointParser.java` 387), [#12527](https://github.com/cgeo/cgeo/issues/12527) (reproduced on `release` on 2026-11-15), [#12545](https://github.com/cgeo/cgeo/issues/12545) (`main/src/main/java/cgeo/geocaching/connector/gc/GCParser.java` 1069-1095 still reports a generic error; the newer #15979 duplicates this report), [#12560](https://github.com/cgeo/cgeo/issues/12560), [#12622](https://github.com/cgeo/cgeo/issues/12622) (`CreateShortcutActivity.java` 97 still offers "Go to"), [#12628](https://github.com/cgeo/cgeo/issues/12628) (only `.codacy.yml` exists), [#12645](https://github.com/cgeo/cgeo/issues/12645), [#12650](https://github.com/cgeo/cgeo/issues/12650) (infrastructure task, not verifiable in code).

```cleanup-result
#4319 keep-open
#5986 keep-open
#6272 keep-open
#6855 keep-open
#8286 keep-open
#8805 keep-open
#8884 keep-open
#12389 keep-open
#12428 keep-open
#12459 duplicate
#12504 keep-open
#12498 keep-open
#11926 keep-open
#12560 keep-open
#12545 keep-open
#12527 keep-open
#12622 keep-open
#12628 keep-open
#12645 keep-open
#12650 keep-open
```
