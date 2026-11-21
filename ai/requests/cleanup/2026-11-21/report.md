<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 1/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 430.4 of 1500 used, 769.6 available beyond the reserve | workflow: f8ce42a851cf3a1b6b9d29231137a189435025f9 -->

I'll start by reading the 20 candidate issue files and locating the snapshot and upstream code.

I've read all 20 issue files. Next I'll check the snapshot for duplicates and look at the upstream code for the feature-related issues.

The snapshot gives me the one-line summaries I need. Now I'll check the upstream code for the feature and bug claims.

Key finding: the changelog says Android Beam was removed (relevant to #4298) and GCVote was disabled (relevant to #6034, #4248, #1863). I'll check those and the other connector and UI claims more precisely.

The source tree is under `upstream/main/src/main/java/cgeo/geocaching`. I'll re-run the connector and map checks with the correct paths.

GCVote is still present (`CacheVotingBar`, `GCLoggingManager`). Next I'll check the GK lookup, the search-result save, and the voting-bar visibility.

Those reminders came from the user turn, so I'll apply them. This task is read-only analysis, so no code changes or builds are needed. Continuing with the remaining checks: voting bar visibility, GCVote settings status, export cancel, and main-menu list actions.

The voting bar is gated by `supportsVoting` and `canVote`. I'll check those implementations and the GCVote services settings summary, plus the main-menu list actions.

GC has no `supportsVoting` implementation, so GCVote is gone from the code. I'll confirm the GCVote and Beam removals in the changelog and check the main menu.

Confirmed: GCVote was removed (changelog line 89) and Android Beam was removed (line 814). Main menu has no list import/export, so #4948 stays open. Last checks: export cancellation (#7464), disabled-connector search (#3509), and the show-on-map limit (#7521).

Search filtering (`conn.isActive()`) addresses #3509. I still need to confirm that export cancellation is user-facing and check the CI setup for #4276.

## Summary

Checked 20 issues. Probably closable: 6 (2 fixed, 4 obsolete). No duplicates and no waiting-for-information cases. 14 stay open.

## Probably fixed

- [#3509](https://github.com/cgeo/cgeo/issues/3509): Requests to disabled/unused connectors. Search now skips inactive connectors (`conn.isActive() ? func.apply(conn) : null`, `main/src/main/java/cgeo/geocaching/SearchResult.java` lines 404–415). The issue's second example was already marked as no longer valid. Confidence: medium.
  - Closing comment: "Thanks for the report! Searches now only use active connectors (see `SearchResult.java`), so disabled connectors are no longer queried. Closing as fixed. Please reopen or comment if you still see requests to inactive services."

- [#7464](https://github.com/cgeo/cgeo/issues/7464): Make export functions cancellable. Export tasks now run with a `cancelFlag` (`main/src/main/java/cgeo/geocaching/export/GpxExportTask.java` line 83). Background export services report a cancelled state (`UploadCoordinatesBatchService.java` line 75). Confidence: medium.
  - Closing comment: "Export tasks now support cancellation via the `cancelFlag` in `GpxExportTask.java`, and the background upload services report cancelled runs. Closing as fixed. Please reopen if a specific export can't be cancelled."

## No longer applicable

- [#4298](https://github.com/cgeo/cgeo/issues/4298): Transmit .gpx file instead of URL via NFC. Android Beam was removed (`main/src/main/res/raw/changelog_full.md` line 814). Confidence: high.
  - Closing comment: "Android Beam support was removed from c:geo because the platform no longer supports it, so this NFC request no longer applies. Closing. Please reopen if you want to discuss an alternative sharing method."

- [#4248](https://github.com/cgeo/cgeo/issues/4248): GCVote shown as "Active" although no password given. GCVote was removed (`changelog_full.md` line 89, "Remove GCVote (service discontinued)"). Confidence: high.
  - Closing comment: "GCVote has been removed from c:geo since the service was discontinued, so this settings issue no longer applies. Closing. Please reopen if you still see this with a current version."

- [#6034](https://github.com/cgeo/cgeo/issues/6034): Always show voting in log activity. GCVote is gone, and the Geocaching connector has no voting capability. Voting remains only for OC and SU (`CacheVotingBar.java`). Confidence: high.
  - Closing comment: "Since GCVote was removed, geocaching.com caches have no voting bar to show in the log screen, so this request no longer applies. Closing. Please reopen if you want this for another connector."

- [#1863](https://github.com/cgeo/cgeo/issues/1863): GCVote loading after GPX import. The GCVote service was removed (`changelog_full.md` line 89), so batch-loading its ratings no longer applies. Confidence: high.
  - Closing comment: "GCVote support has been removed from c:geo, so batch-loading GCVote ratings after import no longer applies. Closing. Please reopen if you have a request for another rating source."

## Keep open

[#5936](https://github.com/cgeo/cgeo/issues/5936), [#7397](https://github.com/cgeo/cgeo/issues/7397) (no block handling in the SU parser), [#4779](https://github.com/cgeo/cgeo/issues/4779) (GK lookup still happens on load in `CacheDetailActivity.java` ~line 408), [#4994](https://github.com/cgeo/cgeo/issues/4994), [#4276](https://github.com/cgeo/cgeo/issues/4276) (a Jenkinsfile still exists, so CI status is unclear), [#5619](https://github.com/cgeo/cgeo/issues/5619) (no `AbstractAuthorizationActivity` exists yet), [#7521](https://github.com/cgeo/cgeo/issues/7521), [#6853](https://github.com/cgeo/cgeo/issues/6853) (`SearchResult.java` 350–353 still saves only the CACHE flag), [#7537](https://github.com/cgeo/cgeo/issues/7537) (account name only shown for geocaching.com), [#7600](https://github.com/cgeo/cgeo/issues/7600), [#7613](https://github.com/cgeo/cgeo/issues/7613), [#3777](https://github.com/cgeo/cgeo/issues/3777) (the GC3XX5J workaround is still in `GCParserTest.java`), [#4948](https://github.com/cgeo/cgeo/issues/4948) (no list import/export in the main menu), [#5088](https://github.com/cgeo/cgeo/issues/5088)

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#3509](https://github.com/cgeo/cgeo/issues/3509): [PR #16555](https://github.com/cgeo/cgeo/pull/16555) "fix \#16499: enhance live map status info and algorithm", merged 2025-01-13, commit [2339f5386f](https://github.com/cgeo/cgeo/commit/2339f5386f4358903a7ff0705200097eca12295e) of 2025-01-11, added `conn.isActive() ? func.apply(conn) : null` in `main/src/main/java/cgeo/geocaching/SearchResult.java`.
- [#7464](https://github.com/cgeo/cgeo/issues/7464): [PR #18850](https://github.com/cgeo/cgeo/pull/18850) "Move GpxExportTask onto WorkerTask (rel. to \#18799)", merged 2026-11-04, commit [fead335324](https://github.com/cgeo/cgeo/commit/fead335324331ba1e6a11d4c9a32396e54ebff02) of 2026-10-24, added `cancelFlag) -> new Pair<>(input.name, export(input, progress))` in `main/src/main/java/cgeo/geocaching/export/GpxExportTask.java`.

```cleanup-result
#5936 keep-open
#7397 keep-open
#1863 obsolete
#4248 obsolete
#4779 keep-open
#4994 keep-open
#6034 obsolete
#4276 keep-open
#5619 keep-open
#7464 fixed
#3777 keep-open
#7521 keep-open
#6853 keep-open
#7537 keep-open
#7600 keep-open
#7613 keep-open
#3509 fixed
#4948 keep-open
#5088 keep-open
#4298 obsolete
```
