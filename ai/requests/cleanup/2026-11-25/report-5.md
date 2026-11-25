<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 5/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 494.6 of 1500 used, 705.4 available beyond the reserve | workflow: 8c6dd3a0e6a5bb2ce4f7f91644e7cd6a3ab23cf2 -->

I'll read the 20 candidate issue files first.

Most candidates are read. #14570 is too large, so I'll read its header first.

#14570 is still on MaterialComponents, so it stays open. Next I'll check the code and the snapshot for the remaining candidates.

`minSdk` is now 26, which matters for #13734. Next I'll read the image categories, `getImages()`, `PersistableFolder`, and check the altitude graph and cache-limit code.

Continuing the read-only review. The `PersistableFolder` null check exists but I still need to confirm `Folder.fromFile` and the root-folder lookup handle null. Next I'll check those, the altitude chart distance formatting, the remaining API-level guards, and the README for a signing hash.

Findings so far: the altitude axis uses `Units.getDistanceFromKilometers`, `CgeoApplication` still has a `VERSION_CODES.O` guard, and the README has no signing hash. Last checks: the null path in `Folder.fromFile` and `Units`' negative-distance handling.

The null handling in `Folder.fromFile` and `PersistableFolder` covers the reported NPE path. Last step: check the snapshot for duplicates of #17423, #17586, #17505, #11915 and #14570.

## Summary

Checked 20 issues: **1 probably fixed**, **1 duplicate**, **0 obsolete**, **1 waiting for information**, **17 keep open**.

## Probably fixed

- [#17485](https://github.com/cgeo/cgeo/issues/17485): NPE in PersistableFolder.registerForIndirectChange
  - Reason: The reported NPE path is now guarded. `registerForIndirectChange` uses `folder == null ? null : folder.getRootPersistableFolder()` (`main/src/main/java/cgeo/geocaching/storage/PersistableFolder.java`, around lines 96–101), and `Folder.fromFile` returns null for a null file (`main/src/main/java/cgeo/geocaching/storage/Folder.java`, lines 176–180). Residual risk: `getExternalMediaDirs()[0]` is still unguarded at line 39.
  - Confidence: medium
  - Closing comment: "Thanks for the report! The null handling for the BACKGROUND_MAPS folder (PersistableFolder / Folder) appears to address this NPE. If the crash still happens in a current release, please reopen or comment with the stack trace and version."

## Duplicates

- [#17423](https://github.com/cgeo/cgeo/issues/17423) duplicates [#11722](https://github.com/cgeo/cgeo/issues/11722) (open since 2021, "Import GPX routes/tracks via click on file"). Both ask for GPX route/track files to be handled without the user choosing the type.
  - Confidence: medium
  - Closing comment: "Thanks for the suggestion! This is covered by the older request #11722 (GPX route/track import on file open), so we're continuing the discussion there. Please comment there if you have new input."

## Waiting for information

- [#17568](https://github.com/cgeo/cgeo/issues/17568): [Nightly] Long distance routing behaves erratic
  - Reason: On 2025-12-01 moving-bits asked the reporter where the observed routing change comes from. No reply since, about 12 months later.
  - Confidence: medium
  - Closing comment: "Thanks for the report. We asked on 2025-12-01 where the routing change you observed comes from, but have had no reply. Could you check whether the problem still happens in the current release? If it does, please reopen or comment with the details we asked for."

## Keep open

[#17344](https://github.com/cgeo/cgeo/issues/17344), [#15608](https://github.com/cgeo/cgeo/issues/15608), [#17191](https://github.com/cgeo/cgeo/issues/17191), [#17445](https://github.com/cgeo/cgeo/issues/17445) (negative km scaling is fixed in `Units.java`, but the circle and grid issues remain), [#1419](https://github.com/cgeo/cgeo/issues/1419), [#16777](https://github.com/cgeo/cgeo/issues/16777), [#13734](https://github.com/cgeo/cgeo/issues/13734) (`CgeoApplication.java` still has a `VERSION_CODES.O` guard), [#17483](https://github.com/cgeo/cgeo/issues/17483), [#17484](https://github.com/cgeo/cgeo/issues/17484), [#17482](https://github.com/cgeo/cgeo/issues/17482), [#17491](https://github.com/cgeo/cgeo/issues/17491), [#17505](https://github.com/cgeo/cgeo/issues/17505), [#11915](https://github.com/cgeo/cgeo/issues/11915), [#17586](https://github.com/cgeo/cgeo/issues/17586) (related: [#18812](https://github.com/cgeo/cgeo/issues/18812)), [#14570](https://github.com/cgeo/cgeo/issues/14570), [#17493](https://github.com/cgeo/cgeo/issues/17493), [#17065](https://github.com/cgeo/cgeo/issues/17065) (waypoint images are not in `Geocache.getImages()` yet)

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#17485](https://github.com/cgeo/cgeo/issues/17485): [PR #17523](https://github.com/cgeo/cgeo/pull/17523) "rel to \#17485: persistablefolder-prevent-npe-on-null-defaultfolder", merged 2025-10-09, commit [d8d04d6aed](https://github.com/cgeo/cgeo/commit/d8d04d6aed503b5a91dc44bb05347b0205304c8c) of 2025-10-07, added `folder == null ? null : folder.getRootPersistableFolder()` in `main/src/main/java/cgeo/geocaching/storage/PersistableFolder.java`.

```cleanup-result
#17344 keep-open
#15608 keep-open
#17423 duplicate
#17191 keep-open
#17445 keep-open
#1419 keep-open
#16777 keep-open
#13734 keep-open
#17483 keep-open
#17484 keep-open
#17482 keep-open
#17491 keep-open
#17485 fixed
#17505 keep-open
#11915 keep-open
#17586 keep-open
#17568 waiting
#14570 keep-open
#17493 keep-open
#17065 keep-open
```
