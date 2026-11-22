<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 3/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 445.7 of 1500 used, 754.3 available beyond the reserve | workflow: 80e10c46acfc5ada8d2ff8809d23eb8d64f9209b -->

I'll start by reading the 20 candidate issue files in parallel.

I've read all 20 issues. Next I'll check the snapshot for duplicates and search upstream code for the fixes or features.

The grep calls returned only file names, so I'll check the snapshot format directly.

The snapshot is large, so I'll confirm which of the 20 issues are still listed as open, and check the upstream layout.

All 20 are open in the snapshot. Now I'll check the upstream code for each topic, starting with the directly searchable ones.

Several results need follow-up: `live_map_button` isn't in the English strings, and the connector grep missed its files. I'll narrow those searches.

Key results so far: `live_map_button` is gone from the English strings, the Wear and WMS features are absent, and the GC web API now has `sa`/`fb`/`hb` parameters. Next I'll read the specific code paths.

I'm continuing the read-only analysis: no code changes are needed, so the coding rules don't apply here. Next I'll check the manifest, calculator, log time, gallery, and compass paths.

The date filter already has end-of-day handling, and the manifest has no `autoVerify`. I'll check the #12886 request text and the calculator start-point code.

## Summary

- Checked: 20 issues
- Probably fixed: 1 (#12886)
- Duplicates: 0
- Obsolete: 0
- Waiting for information: 0
- Keep open: 19

## Probably fixed

### [#12886](https://github.com/cgeo/cgeo/issues/12886) Map filter for events: Displays events for wrong day
- **Reason:** The date filter now truncates the maximum date to the end of the day (`truncateToEndOfDay`, `main/src/main/java/cgeo/geocaching/filters/core/DateFilter.java`, lines 52-58, used at line 153). A same-day range therefore includes the whole selected day. The reporter's time-zone question was never answered, so the "wrong day" symptom may have come from something else. Confidence: **medium**.
- **Closing comment:** Thanks for the report. The date range filter now includes the full selected end day, so a same-day range should show only events from that day. If you still see events from the wrong day, please reopen or comment with your time zone and c:geo version.

## Duplicates

None found.

## No longer applicable

None found.

## Waiting for information

None found. No reporter question is at least 6 months old and unanswered.

## Keep open

[#12672](https://github.com/cgeo/cgeo/issues/12672), [#12702](https://github.com/cgeo/cgeo/issues/12702), [#12725](https://github.com/cgeo/cgeo/issues/12725), [#12744](https://github.com/cgeo/cgeo/issues/12744), [#12750](https://github.com/cgeo/cgeo/issues/12750), [#11897](https://github.com/cgeo/cgeo/issues/11897), [#12714](https://github.com/cgeo/cgeo/issues/12714), [#12859](https://github.com/cgeo/cgeo/issues/12859), [#12877](https://github.com/cgeo/cgeo/issues/12877), [#12886](https://github.com/cgeo/cgeo/issues/12886) (see above), [#12907](https://github.com/cgeo/cgeo/issues/12907), [#12920](https://github.com/cgeo/cgeo/issues/12920), [#12937](https://github.com/cgeo/cgeo/issues/12937), [#12991](https://github.com/cgeo/cgeo/issues/12991), [#13013](https://github.com/cgeo/cgeo/issues/13013), [#13018](https://github.com/cgeo/cgeo/issues/13018), [#3954](https://github.com/cgeo/cgeo/issues/3954), [#13032](https://github.com/cgeo/cgeo/issues/13032), [#11960](https://github.com/cgeo/cgeo/issues/11960), [#12885](https://github.com/cgeo/cgeo/issues/12885)

Later looks worthwhile: #12725 (the `live_map_button` reference is gone, but removal alone gives no unique evidence string), #11960 (archived-cache search parameters look implemented), #12750 (the calculator falls back to the device location when no start point is given), #12920 (no Wear OS code found).

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#12886](https://github.com/cgeo/cgeo/issues/12886): [PR #17666](https://github.com/cgeo/cgeo/pull/17666) "fix \#17633: Normalize relative date filters to day boundaries", merged 2025-12-29, commit [f3e1a18dbe](https://github.com/cgeo/cgeo/commit/f3e1a18dbeb380492c5ec0f5b1c0b336fd884129) of 2025-12-27, added `truncateToEndOfDay` in `main/src/main/java/cgeo/geocaching/filters/core/DateFilter.java`.

```cleanup-result
#12672 keep-open
#12702 keep-open
#12725 keep-open
#12744 keep-open
#12750 keep-open
#11897 keep-open
#12714 keep-open
#12859 keep-open
#12877 keep-open
#12886 fixed
#12907 keep-open
#12920 keep-open
#12937 keep-open
#12991 keep-open
#13013 keep-open
#13018 keep-open
#3954 keep-open
#13032 keep-open
#11960 keep-open
#12885 keep-open
```
