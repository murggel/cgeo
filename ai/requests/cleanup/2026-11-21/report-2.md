<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 2/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 430.4 of 1500 used, 769.6 available beyond the reserve | workflow: f8ce42a851cf3a1b6b9d29231137a189435025f9 -->

I'll start by checking which candidate files exist and what the snapshot contains.

All 20 candidate files exist. Next I'll read them in parallel.

I've read all 20 issue files. Now I'll check the snapshot for duplicates and the format of its lines.

The snapshot has useful lines for most issues. Next I'll search it for possible duplicates by topic and check that `upstream/` exists.

Two early findings: `upstream/` has `connector/ga/GeocachingAustraliaConnector.java`, which points to #6391 being fixed. I'll fix my snapshot regex (the lines start with `#`, not spaces) and grep upstream for the other features.

The snapshot finds no near-duplicates so far, and several upstream features look present (max image upload size, a Geocaching Australia connector, a permission context). I'll check each candidate feature directly in upstream code.

Clear leads now: OC implements `ISearchByNextPage` (#2808), `PermissionAction` opens app settings (#7990), and `CacheDetailActivity` special-cases `CACHE_NOT_FOUND` (#8334). Geocaching.hu has no hits. Next I'll read the relevant code paths and CI config.

The custom instructions in that reminder are repository coding conventions. I'm only auditing and writing a report, so they don't change my task. Next I'll check the remaining code paths: image size limit, owner list, the GK inventory loader, and CI lint/AVD config.

The GK URL-encoding crash is fixed, but the connector still searches trackables for every cache, so #4929 stays open. Next I'll check the OC upload-size override, the nightly/release CI workflows, and the anchor handling.

OC doesn't override the upload-size limit, and lint runs only in `tests.yml`. I'll read the base logging manager's default and check the link handling for anchors.

`AnchorAwareLinkMovementMethod` looks like the anchor fix for #7515. I'll read it and run one last targeted check for waypoint sorting (#2677).

The anchor class only swallows exceptions; it doesn't stop fragment-only links from opening. I'll check how `HtmlUtils` resolves relative URLs before deciding #7515.

## Summary

Checked 20 issues: 5 probably fixed, 0 duplicates, 0 obsolete, 0 waiting for information, 15 keep open.

## Probably fixed

- [#2808](https://github.com/cgeo/cgeo/issues/2808) Nearby search not supporting "load more" for OC
  - Reason: `OCApiLiveConnector` implements `ISearchByNextPage` (`main/src/main/java/cgeo/geocaching/connector/oc/OCApiLiveConnector.java` lines 40, 215-216), backed by `getCachesByNextPage` and `SEARCH_LOAD_NEXTPAGE` in `OkapiClient.java` (lines 108, 344-357). Confidence: medium-high.
  - Closing comment: "Thanks for the report! OC connectors now support loading more results via `ISearchByNextPage` (see `OkapiClient.getCachesByNextPage`), so this should be resolved. Please reopen or comment if the problem persists."

- [#6391](https://github.com/cgeo/cgeo/issues/6391) Support Geocaching Australia API
  - Reason: a dedicated connector exists at `main/src/main/java/cgeo/geocaching/connector/ga/GeocachingAustraliaConnector.java`. Confidence: high.
  - Closing comment: "Thanks for the request! Geocaching Australia is now supported by a dedicated connector (`connector/ga`). Please reopen or comment if anything is still missing."

- [#7990](https://github.com/cgeo/cgeo/issues/7990) No way out if user permanently declined permission
  - Reason: after a denied permission, the dialog now offers "goto app details" (`main/src/main/java/cgeo/geocaching/permission/PermissionAction.java` lines 103-134, `openApplicationSettings()`), which opens the system app settings. Confidence: high.
  - Closing comment: "Thanks for the report! The permission dialog now offers a button to open the app's system settings when permissions were denied. Please reopen if this doesn't resolve the situation."

- [#8334](https://github.com/cgeo/cgeo/issues/8334) Retracted cache listing not recognized
  - Reason: `CacheDetailActivity.java` lines 953-972 show an error toast with the status (e.g. `CACHE_NOT_FOUND`) when a refresh fails, instead of silently finishing. The 404 maps to `CACHE_NOT_FOUND` in `connector/gc/GCParser.java` line 221. I did not verify the exact refresh path for retracted listings. Confidence: medium.
  - Closing comment: "Thanks for the report! Refreshing a cache that no longer exists now shows an error message ('cache not found') instead of failing silently. Please reopen if you still see no feedback for a retracted listing."

- [#8351](https://github.com/cgeo/cgeo/issues/8351) Update AVD on CI
  - Reason: CI now runs on API levels 26, 30 and 34 (`.github/workflows/tests.yml` line 350); the Android 6.0 AVD from the report is gone. Confidence: medium-high.
  - Closing comment: "Thanks for the suggestion! CI now runs instrumented tests on API 26, 30 and 34, so the old Android 6.0 AVD is no longer used. Please reopen if you want a different target."

## Duplicates

None found.

## No longer applicable

None.

## Waiting for information

None. No issue has an unanswered question to the reporter that is at least 6 months old.

## Keep open

[#7139](https://github.com/cgeo/cgeo/issues/7139), [#7145](https://github.com/cgeo/cgeo/issues/7145), [#5259](https://github.com/cgeo/cgeo/issues/5259), [#7819](https://github.com/cgeo/cgeo/issues/7819), [#7894](https://github.com/cgeo/cgeo/issues/7894), [#7922](https://github.com/cgeo/cgeo/issues/7922), [#4929](https://github.com/cgeo/cgeo/issues/4929), [#7999](https://github.com/cgeo/cgeo/issues/7999), [#7181](https://github.com/cgeo/cgeo/issues/7181), [#7515](https://github.com/cgeo/cgeo/issues/7515), [#8222](https://github.com/cgeo/cgeo/issues/8222), [#8121](https://github.com/cgeo/cgeo/issues/8121), [#2677](https://github.com/cgeo/cgeo/issues/2677), [#3971](https://github.com/cgeo/cgeo/issues/3971), [#7075](https://github.com/cgeo/cgeo/issues/7075)

Worth a later look:
- #4929: the URL-encoding crash is fixed, but the connector still looks up trackables for every cache.
- #7515: `HtmlUtils.fixRelativeLinks` still turns `#...` links into external URLs.
- #7145: the OC connector does not override `getMaxImageUploadSize()`, so the 500 kB limit is not applied.
- #8222: lint runs only in the PR workflow, not nightly or release.
- #5259: no direct GSAK `.db3` import exists.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#2808](https://github.com/cgeo/cgeo/issues/2808): [PR #12188](https://github.com/cgeo/cgeo/pull/12188) "fix \#11941: allow loading more caches for new gc search and oc", merged 2021-11-29, commit [d837ca5f4e](https://github.com/cgeo/cgeo/commit/d837ca5f4e83e00b0651f40e4ed1a7cd0c855333) of 2021-11-29, added `SEARCH_LOAD_NEXTPAGE` in `main/src/main/java/cgeo/geocaching/connector/oc/OkapiClient.java`.
- [#6391](https://github.com/cgeo/cgeo/issues/6391): commit [862a05d3cf](https://github.com/cgeo/cgeo/commit/862a05d3cf1e67d9e4e581b02e9818c41639a79d) of 2011-10-12 (no pull request), added `GeocachingAustraliaConnector` in `main/src/main/java/cgeo/geocaching/connector/ga/GeocachingAustraliaConnector.java`. The code is older than the issue, so this is probably not the fix.
- [#7990](https://github.com/cgeo/cgeo/issues/7990): [PR #13800](https://github.com/cgeo/cgeo/pull/13800) "rel to \#13777: integrate Contacts Plugin into c:geo, add PermissionAction + ActivitySavedState", merged 2022-12-30, commit [ab5737c3e9](https://github.com/cgeo/cgeo/commit/ab5737c3e93195a6baaf690c0e24934267a289ab) of 2022-12-30, added `openApplicationSettings` in `main/src/main/java/cgeo/geocaching/permission/PermissionAction.java`.
- [#8334](https://github.com/cgeo/cgeo/issues/8334): [PR #5504](https://github.com/cgeo/cgeo/pull/5504) "Fix tests", merged 2016-03-05, commit [ef3d32677e](https://github.com/cgeo/cgeo/commit/ef3d32677eb9c3225f41bba987946d9b17a27997) of 2016-03-05, added `Cache not found is not a download error` in `main/src/main/java/cgeo/geocaching/CacheDetailActivity.java`. The code is older than the issue, so this is probably not the fix.
- [#8351](https://github.com/cgeo/cgeo/issues/8351): [PR #16848](https://github.com/cgeo/cgeo/pull/16848) "Ci adjust", merged 2025-04-14, commit [0a0b551912](https://github.com/cgeo/cgeo/commit/0a0b5519126a1a0a9fbf977bd52e56aad423641d) of 2025-04-14, added `api-level: [26, 30, 34]` in `.github/workflows/tests.yml`.

```cleanup-result
#7139 keep-open
#7145 keep-open
#5259 keep-open
#7819 keep-open
#7894 keep-open
#7922 keep-open
#4929 keep-open
#7990 fixed
#7999 keep-open
#7181 keep-open
#7515 keep-open
#8222 keep-open
#8121 keep-open
#2808 fixed
#3971 keep-open
#2677 keep-open
#8334 fixed
#8351 fixed
#6391 fixed
#7075 keep-open
```
