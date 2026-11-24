<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 5/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 481.8 of 1500 used, 718.2 available beyond the reserve | workflow: 82cc223d3f1a7bb66fe3741eb4cd0662da311006 -->

I'll start by checking which candidate files exist, then read the issue texts.

Most candidates are read. Issue #11725 is too large for a single read, and #16731 is already closed. I'll read #11725 in ranges and check the snapshot for duplicates.

The snapshot grep only returned a file name, so I'll rerun it in content mode and read the rest of #11725.

I've read all candidates. Next I'll check the upstream code for the likely-fixed items: the corrected-coordinates share option (#13108), the Event date filter, the tilt setting (#15796), GPX track/route handling (#15827, #8626), and the image-scaling setting (#16539).

Initial hits: `FileTypeDetector` now reads a capped 64 KB header, and the GPX parser still has the "tracks take precedence" comment. Next I'll inspect the image title layout, the GPX parser, and the cache-share options.

These reminders arrived as part of the user turn, not inside a tool result, so I'll treat them as normal guidance. My task is read-only analysis, so I'm not changing any code. Next I'll check the remaining feature candidates in upstream.

No Project-GC VGPS connector exists, and no option to disable map tilt. Now I'll check the cache-share option for #13108 and the scale-down setting for #16539.

The cache menu has a "Share incl. user data" option shown when coordinates were corrected. I'll check what it actually shares, and also the event-date filter and the GPX parser's multi-track handling.

#13108 looks fixed: the "Share incl. user data" action now shares corrected coordinates and the personal note. Last checks: the GPX importer for #8626 and #15827, and the event-date filter for #16595/#16596.

The new `UnifiedGPXParser` keeps every `<rte>` and `<trk>` as separate routes/tracks, which may resolve #15827. I'll check whether the old `GPXTrackOrRouteParser` is still used for the "Load Track/Route" action.

The "Load Track/Route" action still uses the old `GPXTrackOrRouteImporter`, so #15827 remains open. Last, I'll check the snapshot for the issues referenced as duplicates or related: #1879, #9595, #15929, #15420, #13302.

### Summary
Checked 20 issues. 4 can probably be closed: 2 fixed and 2 duplicates. 0 obsolete, 0 waiting, 16 keep-open. #16731 is already closed, so it needs no action.

### Probably fixed
- [#13108](https://github.com/cgeo/cgeo/issues/13108) Share cache together with corrected coordinates
  - Reason: `CacheMenuHandler.java` (lines ~99–119) shares the corrected or final coordinates plus the personal note as text via "Share incl. user data". Matches the request; ztNFny linked PR #16481 for it. Confidence: medium.
  - Closing comment: "Thanks for the suggestion! The "Share incl. user data" action in the cache menu now includes the corrected coordinates and personal note. If that doesn't cover your use case, please reopen or comment."
- [#16731](https://github.com/cgeo/cgeo/issues/16731) OOM in detecting file type
  - Reason: already closed. `FileTypeDetector.java` (lines 29, 64–66) reads only a capped 64 KB header. Confidence: high. No closing comment needed.

### Duplicates
- [#14931](https://github.com/cgeo/cgeo/issues/14931) update only cache state: duplicate of [#9595](https://github.com/cgeo/cgeo/issues/9595) (open, 28 comments, same partial-update request). Confidence: high.
  - Closing comment: "Thanks! This is a duplicate of #9595, which covers the same partial/quick update request and has the fuller discussion. Please follow that issue or comment there."
- [#16516](https://github.com/cgeo/cgeo/issues/16516) GC.com: load images from "Image Gallery": duplicate of [#15420](https://github.com/cgeo/cgeo/issues/15420) (open, same gallery request, older). Confidence: high.
  - Closing comment: "Thanks! This is a duplicate of #15420, which covers the same gallery-image request. Please follow that issue or comment there."

### Waiting for information
None.

### Keep open
[#16442](https://github.com/cgeo/cgeo/issues/16442), [#16460](https://github.com/cgeo/cgeo/issues/16460) (only the QuickLaunch part is addressed by #16478), [#16517](https://github.com/cgeo/cgeo/issues/16517), [#16539](https://github.com/cgeo/cgeo/issues/16539), [#16541](https://github.com/cgeo/cgeo/issues/16541), [#12913](https://github.com/cgeo/cgeo/issues/12913), [#16479](https://github.com/cgeo/cgeo/issues/16479), [#15939](https://github.com/cgeo/cgeo/issues/15939) (only inventory count is covered, by #16498), [#16595](https://github.com/cgeo/cgeo/issues/16595), [#16606](https://github.com/cgeo/cgeo/issues/16606), [#16596](https://github.com/cgeo/cgeo/issues/16596), [#15796](https://github.com/cgeo/cgeo/issues/15796), [#16759](https://github.com/cgeo/cgeo/issues/16759), [#11725](https://github.com/cgeo/cgeo/issues/11725) (active, recent activity), [#8626](https://github.com/cgeo/cgeo/issues/8626), [#15827](https://github.com/cgeo/cgeo/issues/15827) (the "Load Track/Route" path still uses the old `GPXTrackOrRouteParser`, with `rte` precedence).

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#13108](https://github.com/cgeo/cgeo/issues/13108): [PR #16481](https://github.com/cgeo/cgeo/pull/16481) "option to share cache with user data (coords, PN)", merged 2025-01-02, commit [05927d2bb5](https://github.com/cgeo/cgeo/commit/05927d2bb586f629ea0e20f83f51c83a0b824d10) of 2025-01-01, added `menu_share_with_data` in `main/src/main/java/cgeo/geocaching/CacheMenuHandler.java`.
- [#16731](https://github.com/cgeo/cgeo/issues/16731): [PR #18912](https://github.com/cgeo/cgeo/pull/18912) "Fix \#16731: detect the file type from the first 64 KB only", merged 2026-11-20, commit [778ab4de75](https://github.com/cgeo/cgeo/commit/778ab4de75f7ab5e6849f4b2930fbe6e0bf1a7da) of 2026-11-15, added `MAX_HEADER_BYTES` in `main/src/main/java/cgeo/geocaching/files/FileTypeDetector.java`.

```cleanup-result
#16442 keep-open
#13108 fixed
#16460 keep-open
#14931 duplicate
#16517 keep-open
#16539 keep-open
#16541 keep-open
#12913 keep-open
#16479 keep-open
#15939 keep-open
#16595 keep-open
#16606 keep-open
#16596 keep-open
#15796 keep-open
#16516 duplicate
#16731 fixed
#16759 keep-open
#11725 keep-open
#8626 keep-open
#15827 keep-open
```
