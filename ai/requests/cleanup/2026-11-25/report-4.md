<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 4/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 494.6 of 1500 used, 705.4 available beyond the reserve | workflow: 8c6dd3a0e6a5bb2ce4f7f91644e7cd6a3ab23cf2 -->

I'll start by checking which candidate files exist and how the snapshot is laid out.

The snapshot has all 20 entries. Next I'll read the 20 candidate files in parallel.

I've read all 20 candidates. Now I'll check the upstream code for the claims that can be verified: GCParser short-description delimiter, the select-mode "next" feature, the launch mode, target SDK, GeoKrety batching, and the map code behind #10927.

Several claims are now verifiable. Next I'll read the GCParser short-description code, the manifest entries that handle external links, and the GeoKrety logging code.

The system reminders in that message are repository coding guidelines. I'm only writing the report and not changing code, so they don't change my work. Next I'll check the short-description regex, the manifest's singleTop activities, and the live-state code path for #10927.

The short-description regex still ends at `</span>\s*</div>`, so #17224 is not fixed. Next I'll check the manifest's external-link handler for #17314, and search the tree for references to PR #17357 and to the three numbers in the issues to check.

`CacheDetailActivity` (the handler for geocache links) has no `launchMode`, so #17314 is still present in code. I'll now search the snapshot for possible duplicates of the open items.

The keyword grep is too broad. I'll narrow it to the GeoKrety bulk-logging reference and a few specific keywords.

## Summary

Checked 20 issues. Probably closable: 2 (fixed). Duplicates, obsolete, and waiting: 0 each. Keep open: 18.

## Probably fixed

- [#12077](https://github.com/cgeo/cgeo/issues/12077) Have some options when trying to save search results to a list
  - Reason: Select mode now has "Select next 20 / next 100 caches" (`selectNextCaches`, `upstream/main/src/main/java/cgeo/geocaching/ui/CacheListAdapter.java` 289-290; menu items in `upstream/main/res/menu/cache_list_options.xml`), which is the approach the maintainers agreed on in the thread. The distance-based option was not implemented. Confidence: medium-high.
  - Closing comment: "Thanks for the discussion. Select mode now offers 'Select next 20 / next 100 caches', the approach suggested here, which covers selecting the first N caches. The distance-based option was not implemented. If you still need it, please reopen or comment."

- [#17375](https://github.com/cgeo/cgeo/issues/17375) Upgrade to SDK35: Edge-to-Edge
  - Reason: The upgrade is in place: `targetSdk = 36` (`upstream/main/build.gradle` 47) and `WindowCompat.enableEdgeToEdge` with inset handling in `upstream/main/src/main/java/cgeo/geocaching/activity/AbstractActivity.java` 196-202. Map-specific ideas remain in [#17356](https://github.com/cgeo/cgeo/issues/17356). Confidence: medium.
  - Closing comment: "The edge-to-edge upgrade is in place (targetSdk 36, edge-to-edge in the base activity). Remaining map ideas are tracked in #17356. If edge-to-edge still causes problems on your device, please reopen or comment with details."

## Duplicates

None found.

## No longer applicable

None.

## Waiting for information

None. No open issue has an unanswered question to the reporter that is at least 6 months old.

## Keep open

[#17223](https://github.com/cgeo/cgeo/issues/17223), [#17224](https://github.com/cgeo/cgeo/issues/17224) (still present: `PATTERN_SHORTDESC` ends at `</span>\s*</div>`, `GCConstants.java` line 35), [#17188](https://github.com/cgeo/cgeo/issues/17188), [#17208](https://github.com/cgeo/cgeo/issues/17208) (contact note only, could be closed by the maintainer), [#17154](https://github.com/cgeo/cgeo/issues/17154), [#17258](https://github.com/cgeo/cgeo/issues/17258), [#17277](https://github.com/cgeo/cgeo/issues/17277), [#17278](https://github.com/cgeo/cgeo/issues/17278), [#17207](https://github.com/cgeo/cgeo/issues/17207), [#16915](https://github.com/cgeo/cgeo/issues/16915), [#17314](https://github.com/cgeo/cgeo/issues/17314) (still present: `CacheDetailActivity` has no `launchMode`, `upstream/main/AndroidManifest.xml` 488), [#7831](https://github.com/cgeo/cgeo/issues/7831), [#10927](https://github.com/cgeo/cgeo/issues/10927) (PR #17357 not verifiable in this tree), [#17102](https://github.com/cgeo/cgeo/issues/17102), [#17356](https://github.com/cgeo/cgeo/issues/17356), [#16020](https://github.com/cgeo/cgeo/issues/16020), [#16021](https://github.com/cgeo/cgeo/issues/16021), [#17394](https://github.com/cgeo/cgeo/issues/17394) (no GeoKrety batch logging in `GeokretyConnector`/`GeokretyLoggingManager`)

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#12077](https://github.com/cgeo/cgeo/issues/12077): [PR #12139](https://github.com/cgeo/cgeo/pull/12139) "add 'selext next 20 caches' to cache list (rel. to \#12077)", merged 2021-11-22, commit [013449db19](https://github.com/cgeo/cgeo/commit/013449db198d120330651eb7e5f1f89bf0cf78a4) of 2021-11-20, added `selectNextCaches` in `main/src/main/java/cgeo/geocaching/ui/CacheListAdapter.java`.
- [#17375](https://github.com/cgeo/cgeo/issues/17375): [PR #17355](https://github.com/cgeo/cgeo/pull/17355) "Adapt c:geo to edge2edge enforcement of target API 35", merged 2025-09-02, commit [3ca497fc7a](https://github.com/cgeo/cgeo/commit/3ca497fc7a21763f4e19708b0cf10a30a9604fd4) of 2025-09-02, added `WindowCompat.enableEdgeToEdge(currentWindow)` in `main/src/main/java/cgeo/geocaching/activity/AbstractActivity.java`.

```cleanup-result
#17223 keep-open
#17224 keep-open
#17188 keep-open
#17208 keep-open
#17154 keep-open
#17258 keep-open
#17277 keep-open
#17278 keep-open
#12077 fixed
#17207 keep-open
#16915 keep-open
#17314 keep-open
#7831 keep-open
#10927 keep-open
#17102 keep-open
#17356 keep-open
#16020 keep-open
#16021 keep-open
#17394 keep-open
#17375 fixed
```
