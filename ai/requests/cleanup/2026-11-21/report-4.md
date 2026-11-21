<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 4/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 430.4 of 1500 used, 769.6 available beyond the reserve | workflow: f8ce42a851cf3a1b6b9d29231137a189435025f9 -->

I'll start by checking which candidate files exist and how the snapshot is laid out.

All 20 candidate files exist. I'll read them now.

Several remaining files are large, so I'll read the short ones first and then page through the big ones.

Two files remain that are too large to read in one go: #9791 and #8752. I'll read #9791 in full and grep the comment headers of #8752 to locate its discussion.

The last comment on #8752 is at line 1169 and #9791's is at 333. I'll read those tails, plus #8752's opening, to see what each is asking.

I've now read all 20 candidates. Next I'll check the upstream code and search the snapshot for duplicates, starting with the upstream layout and keyword greps.

The snapshot grep returned only a file name because I didn't set `output_mode`. I'll rerun it in content mode and run the upstream checks in parallel.

Upstream findings so far: #9855 is fixed (`dependencyResolutionManagement` in `settings.gradle`), while `getAdapterPosition` is still used in `HelperAppAdapter.java`. I'll check the field-notes encoding in `FieldNotes.java` and run title-restricted snapshot searches for duplicates.

The system reminders above are from the user turn, so I'll follow them: they're about code style and build gates, and this is a read-only cleanup, so I'm not modifying code. Continuing with targeted duplicate searches in the snapshot.

The keyword-based output is too noisy to resolve duplicates. I'll run narrower title searches in parallel for each remaining topic.

I now have likely duplicates: #7906 duplicates the newer #11027 (not on my list), and #9855 is fixed. Next I'll check upstream code for the OC log-image check (#6809), the GC login path (#10339), and the waypoint edit flow (#10125).

#6809 has a `supportsLogImages()` check in `OCApiConnector.java`. I'll view it, and locate the waypoint-edit and trackable-logging code for #10125 and #9504.

The waypoint edit path calls `LegacyCalculatedCoordinateMigrator.performMigration` before opening the editor, which may be the unconditional store. I'll check that migrator and the trackable-log entry point.

The unconditional store appears to be gated by `needsMigration`. I'll confirm in the migrator and the internal start method whether the cache is still saved on entering edit mode.

Upstream `EditWaypointActivity` no longer saves the cache when entering edit mode; the only save is inside the user-confirmed migration, so #10125 looks fixed. Last checks: GeoKrety image upload (#5078) and trackable-only logging (#9504).

## Summary

Checked 20 issues: 3 probably fixed, 0 duplicates, 0 obsolete, 0 waiting, 17 keep open.

## Probably fixed

- [#9855](https://github.com/cgeo/cgeo/issues/9855) Central declaration of repositories
  - Reason: `upstream/settings.gradle` declares `dependencyResolutionManagement { repositories { mavenCentral() } }`, the feature requested. Confidence: high.
  - Closing comment: "Thanks for the suggestion! Central repository declaration via `dependencyResolutionManagement` is now in `settings.gradle`, so this request is done. Please reopen or comment if it's still missing something."

- [#6809](https://github.com/cgeo/cgeo/issues/6809) Detect if OC-site is capable of log picture upload
  - Reason: `OCApiConnector.supportsLogImages()` returns true and uses the OKAPI image service. The reporter confirmed on 2021-04-26 that uploads to OC-NA work (tested with 2021.04.25). Confidence: medium, since the fix may have been server-side rather than in code.
  - Closing comment: "Thanks for the report! Log picture upload to OC sites works now (confirmed on 2021.04.25), so I'm closing this. Please reopen or comment if it still fails on your site."

- [#10125](https://github.com/cgeo/cgeo/issues/10125) Do not unconditionally store cache locally upon entering waypoint edit mode
  - Reason: `startActivityEditWaypoint` only calls the migrator when `needsMigration` is true, and `startActivityEditWaypointInternal` just starts the activity without saving the cache. Confidence: medium.
  - Closing comment: "Thanks for the report! Opening waypoint edit no longer stores the cache locally; that only happens on an explicit change. Closing this. Please reopen if you still see it."

## Keep open

[#6672](https://github.com/cgeo/cgeo/issues/6672), [#6459](https://github.com/cgeo/cgeo/issues/6459), [#9791](https://github.com/cgeo/cgeo/issues/9791), [#7906](https://github.com/cgeo/cgeo/issues/7906) (newer [#11027](https://github.com/cgeo/cgeo/issues/11027) duplicates it; close that one instead), [#9529](https://github.com/cgeo/cgeo/issues/9529), [#10024](https://github.com/cgeo/cgeo/issues/10024), [#8752](https://github.com/cgeo/cgeo/issues/8752), [#10044](https://github.com/cgeo/cgeo/issues/10044) (field notes still UTF-16LE without BOM), [#5078](https://github.com/cgeo/cgeo/issues/5078) (no GeoKrety image upload in code), [#9504](https://github.com/cgeo/cgeo/issues/9504), [#10339](https://github.com/cgeo/cgeo/issues/10339), [#10366](https://github.com/cgeo/cgeo/issues/10366) (`getAdapterPosition` still used, e.g. `HelperAppAdapter.java`), [#10368](https://github.com/cgeo/cgeo/issues/10368), [#10417](https://github.com/cgeo/cgeo/issues/10417), [#10271](https://github.com/cgeo/cgeo/issues/10271), [#5595](https://github.com/cgeo/cgeo/issues/5595), [#7714](https://github.com/cgeo/cgeo/issues/7714)

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#9855](https://github.com/cgeo/cgeo/issues/9855): nothing found for `dependencyResolutionManagement` in `upstream/settings.gradle` (file does not exist in the current code).
- [#6809](https://github.com/cgeo/cgeo/issues/6809): nothing found for `supportsLogImages` in `upstream/main/src/main/java/cgeo/geocaching/connector/oc/OCApiConnector.java` (file does not exist in the current code).
- [#10125](https://github.com/cgeo/cgeo/issues/10125): nothing found for `startActivityEditWaypointInternal` in `upstream/main/src/main/java/cgeo/geocaching/EditWaypointActivity.java` (file does not exist in the current code).

```cleanup-result
#6672 keep-open
#6459 keep-open
#9791 keep-open
#7906 keep-open
#9529 keep-open
#9855 fixed
#10024 keep-open
#8752 keep-open
#10044 keep-open
#10125 fixed
#5078 keep-open
#9504 keep-open
#10339 keep-open
#10366 keep-open
#10368 keep-open
#10417 keep-open
#10271 keep-open
#5595 keep-open
#6809 fixed
#7714 keep-open
```
