<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 3/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 518.6 of 1500 used, 981.4 available beyond the reserve | workflow: 707a4f36d3e52637b5c2b6d05f14cfba4ef13e01 -->

I'll start by reading the 20 candidate issue files and locating the snapshot entries.

All 20 candidate files exist. The snapshot grep returned nothing, so I'll check its format after reading the issues.

I've read all 20 issues. Next I'll check the snapshot's format and search it for duplicates, and look at the upstream tree for the code evidence I need.

The snapshot uses `#number |` lines. My keyword grep ran in file-list mode, so I'll re-run it with line output, plus the specific issue numbers.

#18703 is not in the snapshot, so #18704 has no open duplicate. Next I'll check the master code for the candidate fixes: the language-switch filter names (#18170), the date formatting (#18651), and the ProGuard rules (#18676). I'll also check the CI and log-loading code.

The Apache ProtocolVersion crash (#18676) may already be addressed: the manifest declares `org.apache.http.legacy` and ProGuard keeps `org.apache.http`. I'll read those spots, and also search the filter-name code for #18170.

The message above is a system reminder in the user turn, so I'll follow it. I'm only reading files for this report, so the build and style rules don't change the work. Next I'll locate the manifest and check the language-related code paths.

The filter-name path goes through the localized context, but I can't confirm from the tree which commit introduced that change. For #18651, `formatShortDateIncludingWeekday` appears to use the base context (system locale), so I'll check that and the cache-detail call site.

The date code still uses the system-locale base context for the weekday (`Formatter.java` ~L161, used at ~L332), so #18651 is still present in master even though GitHub shows it closed. Last checks: the manifest's Apache entry, any "load more logs" feature (#585), and whether CI still runs on Jenkins (#6587).

## Summary

- Checked: 20 issues
- Fixed: 0
- Duplicate: 0
- Obsolete: 0
- Waiting for information: 0
- Keep open: 20 (#18651 is already closed on GitHub; see the note below)

No issue can be closed with the evidence available.

## Keep open

[#18601](https://github.com/cgeo/cgeo/issues/18601), [#18610](https://github.com/cgeo/cgeo/issues/18610), [#18611](https://github.com/cgeo/cgeo/issues/18611), [#18170](https://github.com/cgeo/cgeo/issues/18170), [#18566](https://github.com/cgeo/cgeo/issues/18566), [#18612](https://github.com/cgeo/cgeo/issues/18612), [#18386](https://github.com/cgeo/cgeo/issues/18386), [#18651](https://github.com/cgeo/cgeo/issues/18651), [#18671](https://github.com/cgeo/cgeo/issues/18671), [#18676](https://github.com/cgeo/cgeo/issues/18676), [#585](https://github.com/cgeo/cgeo/issues/585), [#18690](https://github.com/cgeo/cgeo/issues/18690), [#18692](https://github.com/cgeo/cgeo/issues/18692), [#4216](https://github.com/cgeo/cgeo/issues/4216), [#6587](https://github.com/cgeo/cgeo/issues/6587), [#11660](https://github.com/cgeo/cgeo/issues/11660), [#18132](https://github.com/cgeo/cgeo/issues/18132), [#18698](https://github.com/cgeo/cgeo/issues/18698), [#18702](https://github.com/cgeo/cgeo/issues/18702), [#18704](https://github.com/cgeo/cgeo/issues/18704)

Notes where a later look is worthwhile:
- [#18170](https://github.com/cgeo/cgeo/issues/18170): the reporter says the fix works in the beta and release, and master's `getStringWithFallback` (`upstream/main/src/main/java/cgeo/geocaching/utils/LocalizationUtils.java`, ~L114) uses the app locale. I could not identify a commit-specific marker, so it is not in the fixed category. Close it once the maintainers confirm.
- [#18651](https://github.com/cgeo/cgeo/issues/18651): it is already closed on GitHub, but `formatShortDateIncludingWeekday` (`upstream/main/src/main/java/cgeo/geocaching/utils/Formatter.java`, ~L160) still uses the system-locale base context for the weekday. The bug looks present in master.
- [#18676](https://github.com/cgeo/cgeo/issues/18676): `org.apache.http.legacy` is already declared (`upstream/main/AndroidManifest.xml`, L66) and ProGuard keeps `org.apache.http`. Both look older than the report, so the crash may persist.
- [#18132](https://github.com/cgeo/cgeo/issues/18132): a maintainer comment leans towards "won't fix". That is a decision for maintainers, not a closing category.
- [#18566](https://github.com/cgeo/cgeo/issues/18566): the DT-marker hash point is already handled in `MapMarkerUtils.getCacheMarker()`. The LRU question is still open.

```cleanup-result
#18601 keep-open
#18610 keep-open
#18611 keep-open
#18170 keep-open
#18566 keep-open
#18612 keep-open
#18386 keep-open
#18651 keep-open
#18671 keep-open
#18676 keep-open
#585 keep-open
#18690 keep-open
#18692 keep-open
#4216 keep-open
#6587 keep-open
#11660 keep-open
#18132 keep-open
#18698 keep-open
#18702 keep-open
#18704 keep-open
```
