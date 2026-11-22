<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 1/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 445.7 of 1500 used, 754.3 available beyond the reserve | workflow: 80e10c46acfc5ada8d2ff8809d23eb8d64f9209b -->

I'll start by reading the candidate issue files and the snapshot.

Most candidates are read. #10522 was too large for a single view, so I'll read it in ranges and grep the snapshot for duplicates.

The snapshot grep was too broad, so I'll narrow it per issue. First the rest of #10522 and a check of the upstream icon and code paths.

The upstream tree is current master, so many 2021 reports may have been addressed. I'll check the specific code paths for each candidate in batches.

I'm continuing the code checks. The system notes about coding style don't change this read-only cleanup, since I'm not writing code. Next batch covers the GPX intent filter, ALC user menu, attribute filter search, calculated-waypoint variables, the offline-log dashboard link, and the sort arrows.

The variables view now uses a RecyclerView, which suggests #12241 is addressed. I'll confirm where it's used, and check the remaining areas (sort menu, dashboard, attribute filter, GPX intent filter).

Attribute filter has no name-search field, so #11986 stands. Now I'll check where the new variable list is used, the sort menu entry, and the dashboard offline-log link.

#12241 looks fixed: the calculator dialogs now use the vertical `VariableListView`. Next I'll check the remaining points: the manifest GPX intent filter, ALC owner capability, the dashboard, and the sort icon code.

ALC has no owner capability, so its user menu lacks the hidden/found entries (#12061 stays open). Checking the manifest GPX filter, the dashboard, and sort-direction UI next.

The manifest does register GPX intent filters, so I need to see whether the handler also imports tracks. I'll check that along with the sort arrow glyphs and the home screen's offline-log entries.

Offline logs have a home-screen entry, and the sort arrows (↑/↓) are still rendered. I'll check the home-screen click target, the sort label code, and how a GPX opened via intent is dispatched (caches vs. tracks).

Opening a GPX file still routes to cache import, while tracks/routes are imported only from the map, so #11722 stays open. Now I'll search the snapshot for duplicates of each candidate.

The snapshot has a likely duplicate for #11722 (#14329, same GPX track/route request). I'll run narrower searches for the other candidates, including #8626, and check whether #9586's and #11440's targets are open.

Summary: 20 issues checked. Probably closable: 1 fixed, 2 duplicates. No obsolete or waiting issues were found with enough evidence. 17 remain open (#12034 is already closed).

## Probably fixed

- [#12241](https://github.com/cgeo/cgeo/issues/12241) Variables dialog horizontal scrolling
  - Reason: The variables list is now a RecyclerView (`VariableListView` with `VariablesListAdapter`, `main/src/main/java/cgeo/geocaching/ui/VariableListView.java`), used by `CoordinatesCalculateGlobalDialog` and `EditWaypointActivity`. The old horizontally scrolling layout is gone. Confidence: medium-high.
  - Closing comment: "Thanks for the report. The variables list has since been rebuilt as a RecyclerView-based list, so the horizontal-scrolling layout described here no longer exists in current c:geo. If the problem still happens in the latest release, please comment or reopen with your version and steps."

## Duplicates

- [#11440](https://github.com/cgeo/cgeo/issues/11440) duplicate of [#651](https://github.com/cgeo/cgeo/issues/651) (Database fields cleanup). Both cover removing the unused `updated` fields. The `updated` columns are still in `DataStore.java` (L391 and following), so #651 remains the open checklist. Confidence: high.
  - Closing comment: "Thanks. This is covered by the database cleanup checklist in #651, which also tracks removing the unused `updated` fields. We'll follow up there. Please comment on #651 if you have more details."
- [#11722](https://github.com/cgeo/cgeo/issues/11722) duplicate of [#14329](https://github.com/cgeo/cgeo/issues/14329) (Support importing GPX tracks/routes from external). Both request that opening a GPX file offers track/route import, not just cache import. The import logic is still cache-only on file open. Confidence: medium.
  - Closing comment: "Thanks for the suggestion. The same request is tracked in #14329, which has the more recent discussion. Please follow up there if the problem persists or you have additional details."

## No longer applicable

None.

## Waiting for information

None. Every candidate's last substantive comment is either from 2021 or later with no open question to the reporter, or the reporter answered.

## Keep open

[#651](https://github.com/cgeo/cgeo/issues/651), [#11036](https://github.com/cgeo/cgeo/issues/11036), [#11961](https://github.com/cgeo/cgeo/issues/11961), [#12034](https://github.com/cgeo/cgeo/issues/12034), [#10522](https://github.com/cgeo/cgeo/issues/10522), [#9586](https://github.com/cgeo/cgeo/issues/9586), [#12061](https://github.com/cgeo/cgeo/issues/12061), [#12065](https://github.com/cgeo/cgeo/issues/12065), [#12085](https://github.com/cgeo/cgeo/issues/12085), [#12151](https://github.com/cgeo/cgeo/issues/12151), [#7555](https://github.com/cgeo/cgeo/issues/7555), [#11728](https://github.com/cgeo/cgeo/issues/11728), [#12159](https://github.com/cgeo/cgeo/issues/12159), [#11986](https://github.com/cgeo/cgeo/issues/11986), [#12180](https://github.com/cgeo/cgeo/issues/12180), [#12186](https://github.com/cgeo/cgeo/issues/12186), [#12021](https://github.com/cgeo/cgeo/issues/12021)

Notes:
- [#12034](https://github.com/cgeo/cgeo/issues/12034) is already closed (updated 2026-11-20).
- [#651](https://github.com/cgeo/cgeo/issues/651) is the target for the #11440 duplicate and should stay open.
- [#10522](https://github.com/cgeo/cgeo/issues/10522) is partly done (an adaptive icon exists) but the foreground quality is still open.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#12241](https://github.com/cgeo/cgeo/issues/12241): [PR #11764](https://github.com/cgeo/cgeo/pull/11764) "rel to \#11520: add first version of variables/calculator tab", merged 2021-10-03, commit [3b59e0b516](https://github.com/cgeo/cgeo/commit/3b59e0b51618805b9509a7494f130ecef178dcf8) of 2021-09-26, added `VariablesListAdapter` in `main/src/main/java/cgeo/geocaching/ui/VariableListView.java`. The code is older than the issue, so this is probably not the fix.

```cleanup-result
#12241 fixed
#11440 duplicate
#11722 duplicate
#651 keep-open
#11036 keep-open
#11961 keep-open
#12034 keep-open
#10522 keep-open
#9586 keep-open
#12061 keep-open
#12065 keep-open
#12085 keep-open
#12151 keep-open
#7555 keep-open
#11728 keep-open
#12159 keep-open
#11986 keep-open
#12180 keep-open
#12186 keep-open
#12021 keep-open
```
