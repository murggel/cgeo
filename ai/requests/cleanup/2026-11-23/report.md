<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 1/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 463.9 of 1500 used, 736.1 available beyond the reserve | workflow: 1d3a4543eb6f7e4963e3872cb0392abc1ae9da40 -->

I'll start by reading the 20 candidate issue files.

Two candidate files are too large to read whole. I'll read #8402 in full and check the structure of #13736, and also look at the snapshot and upstream layout.

The #13736 grep returned only a filename, so I'll read that file in ranges and gather the snapshot lines for the candidates.

The snapshot gives me duplicate candidates for most issues. Next I need the discussion part of #13736 and the comment headers, which will show where the discussion starts.

I've now read all 20 candidates. Next I'll check the upstream code for each claim, starting with the strings, backup, filter, search and routing features.

Several results matter: #13649 (`MAX_AUTO_BACKUPS = 4` still hardcoded), #13669 (both exports still share `export_exportedto`), and #13560 (`ALApi` archived flag handling). Next I'll check the remaining features and the snapshot for #12660.

The system reminders above are project instructions for writing code. This task is read-only, so I'll continue the analysis. Next I'll check the search, filter, GPX, formula and BRouter code paths.

The #13878 out-of-sync button exists for the cache note, so I need to check whether it also covers waypoint notes. I'll check the remaining features and the waypoint activity together.

Key findings so far: the FAQ link in `err_unknown` still exists (#13676 is still live), the "Load all remaining caches" button still exists (#13707), and #13649's auto-backup cap is still hardcoded. Last, I'll check the Adventure Lab handling for #13560 and #13797.

`ALApi` reads `IsLinear` on detail parsing, which may cover #13797. I'll view that block to confirm it's saved on refresh.

The detail import now sets the ALC mode from `IsLinear` and saves it on every refresh, so #13797 looks fixed. Last, I'll check the snapshot for the possible duplicate targets mentioned in the issues.

I've lost the earlier per-issue notes, so I'll re-read the 20 candidate files before writing the report.

Two candidate files were too large to read in full: #13736 and #8402. I'll read their first sections now.

I now have all 20 candidate texts. Next I'll check the code for the likely fixes: ALC linear mode, the "load all" button, large status icon graying, auto-backup count, and the waypoint scan.

Early checks: #13649 still has `MAX_AUTO_BACKUPS = 4`, so it stays open. #13797 has `IsLinear` read in ALApi. Next I'll grep for the remaining feature candidates.

Code evidence so far: #12503 has `addColorContrast` in HtmlUtils, and #13797 reads `IsLinear` in ALApi. Last, I'll check the snapshot for duplicate targets and the fix-evidence text of #13797.

**Summary**

Checked 20 issues. Probably closable: 2 fixed, 0 duplicate, 0 obsolete, 0 waiting. 18 stay open. [#13755](https://github.com/cgeo/cgeo/issues/13755) is already closed on GitHub, so it is listed under keep-open with no action needed.

## Probably fixed

- [#13797](https://github.com/cgeo/cgeo/issues/13797) ALC change of linear/random mode not detected
  Reason: `ALApi.java` (lines 404–412) reads `IsLinear` from the Adventure Lab API on each detail refresh, sets the ALC mode and saves it, so the stale "Linear" state no longer persists. Confidence: medium.
  Closing comment: "Thanks for the report! The current code reads the linear/random mode from the Adventure Lab API on every refresh and saves it (`main/src/main/java/cgeo/geocaching/connector/al/ALApi.java`), so this should be resolved. If the mode still doesn't update, please reopen or comment with the cache code and the c:geo version."

- [#12503](https://github.com/cgeo/cgeo/issues/12503) Explicit white background in cache description not readable in dark mode
  Reason: `HtmlStyle` applies `HtmlUtils.addColorContrast` (`main/src/main/java/cgeo/geocaching/utils/html/HtmlUtils.java`, lines 208–215) to description text, recolouring spans whose contrast with the app background is too low. It does not check the span's own background colour. Confidence: medium.
  Closing comment: "Thanks for the report! Description text is now checked for contrast against the app background and recoloured when it is too low (`main/src/main/java/cgeo/geocaching/utils/html/HtmlUtils.java`). If a listing is still unreadable in dark mode, please reopen or comment with the cache code."

## Duplicates

None found.

## No longer applicable

None.

## Waiting for information

None.

## Keep open

[#8402](https://github.com/cgeo/cgeo/issues/8402), [#13669](https://github.com/cgeo/cgeo/issues/13669), [#13676](https://github.com/cgeo/cgeo/issues/13676), [#13690](https://github.com/cgeo/cgeo/issues/13690), [#13707](https://github.com/cgeo/cgeo/issues/13707), [#13560](https://github.com/cgeo/cgeo/issues/13560), [#13717](https://github.com/cgeo/cgeo/issues/13717), [#13649](https://github.com/cgeo/cgeo/issues/13649), [#13755](https://github.com/cgeo/cgeo/issues/13755), [#13493](https://github.com/cgeo/cgeo/issues/13493), [#13813](https://github.com/cgeo/cgeo/issues/13813), [#13829](https://github.com/cgeo/cgeo/issues/13829), [#13835](https://github.com/cgeo/cgeo/issues/13835), [#13878](https://github.com/cgeo/cgeo/issues/13878), [#13736](https://github.com/cgeo/cgeo/issues/13736), [#13895](https://github.com/cgeo/cgeo/issues/13895), [#13698](https://github.com/cgeo/cgeo/issues/13698), [#13031](https://github.com/cgeo/cgeo/issues/13031)

Worth a later look:
- [#13649](https://github.com/cgeo/cgeo/issues/13649): `MAX_AUTO_BACKUPS = 4` is still hard-coded in `main/src/main/java/cgeo/geocaching/utils/BackupUtils.java`.
- [#13676](https://github.com/cgeo/cgeo/issues/13676): a maintainer decision on the FAQ link is pending.
- [#13755](https://github.com/cgeo/cgeo/issues/13755): already closed on GitHub.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#13797](https://github.com/cgeo/cgeo/issues/13797): [PR #13303](https://github.com/cgeo/cgeo/pull/13303) "alcIsLinear", merged 2022-08-06, commit [fdb0ada6ce](https://github.com/cgeo/cgeo/commit/fdb0ada6ce36f10114f4a3f9abf4e37249f34e74) of 2022-08-03, added `response.get("IsLinear")` in `main/src/main/java/cgeo/geocaching/connector/al/ALApi.java`. The code is older than the issue, so this is probably not the fix.
- [#12503](https://github.com/cgeo/cgeo/issues/12503): [PR #15806](https://github.com/cgeo/cgeo/pull/15806) "rel to \#12910: refactor html rendering, add description styles", merged 2024-06-23, commit [4b8261eeb0](https://github.com/cgeo/cgeo/commit/4b8261eeb0390bb4b765881839df4127217c0071) of 2024-06-22, added `addColorContrast` in `main/src/main/java/cgeo/geocaching/utils/html/HtmlUtils.java`.

```cleanup-result
#8402 keep-open
#13669 keep-open
#13676 keep-open
#13690 keep-open
#13707 keep-open
#13560 keep-open
#13717 keep-open
#13649 keep-open
#13755 keep-open
#13493 keep-open
#13813 keep-open
#13829 keep-open
#13835 keep-open
#13797 fixed
#13878 keep-open
#12503 fixed
#13736 keep-open
#13895 keep-open
#13698 keep-open
#13031 keep-open
```
