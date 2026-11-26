<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 2/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 505.7 of 1500 used, 994.3 available beyond the reserve | workflow: d7e87ee585e88ddebec71b578af2d2517c5fd54c -->

I'll start by checking which candidate files exist and how the snapshot is laid out.

Now I'll read the 20 candidate files to check.

All 20 candidates are read. Next I'll check the snapshot for duplicates and the upstream code for the fixes that are plausible.

The snapshot grep was too broad, so I'll narrow it per topic and check the upstream code in parallel.

Several upstream areas look relevant. I'll read the image-caption code, the GC box guard, and the artefact parser.

The upstream instructions appeared in a system message, not inside a tool result, so they're from the user side. This task is read-only analysis, so I'll keep going with the report. Next, I'll check the timestamp, artefact-parser, and image-check code.

Two possible fixes stand out: `CompassMiniView` for #13466 and the `{c:geo-start}` parser for #17801. I'll check where they're used, plus the image-content check and the GC date parser for #17291.

The timestamp code still uses the device-local offset (`LogUtils.java` line 67), so #17291 is not fixed. The image-check toast is still the generic `err_acquire_image_failed`. Last, I'll check the snapshot for duplicate titles and look for the home-screen and bookmark-list features.

## Summary

Checked 20 issues: 0 probably fixed, 2 duplicates, 0 obsolete, 1 waiting for information, 17 keep open.

## Duplicates

- [#15879](https://github.com/cgeo/cgeo/issues/15879) Allow placeholders in default caption for log images
  - Reason: The reporter's own comment says "See #13385", and both ask for placeholders such as [Name] in image captions. Master still uses the plain prefix (`LogUtils.java` line 81, `getLogImageTitle`). Confidence: high
  - Closing comment: "Thanks for the report. This is a duplicate of #13385, which covers the same placeholder request for image names and captions. We're closing this in favour of that issue. If you have additional details, please comment there."

- [#17242](https://github.com/cgeo/cgeo/issues/17242) Support [NAME] and other placeholders in default image caption setting
  - Reason: Same request as #13385 and #15879, which the reporter already linked. Master's caption code is unchanged. Confidence: high
  - Closing comment: "Thanks for the request. This is a duplicate of #13385, which tracks placeholders for image names and captions. We're closing this in favour of that issue. Feel free to comment there if you have more input."

## Waiting for information

- [#17739](https://github.com/cgeo/cgeo/issues/17739) Unexpected result when sorting a search result
  - Reason: semantosoph asked the reporter on 2026-02-10 whether the "223 caches" in the expected result is a typo. The reporter has not replied in the nine months since, so the question is more than 6 months old. Confidence: medium
  - Closing comment: "We're closing this for now because the question from 10 February 2026 (whether the expected count of 223 is a typo for 213) has not been answered. If the problem still happens, please reopen or comment with the answer and your steps, and we'll take another look."

## Keep open

[#17828](https://github.com/cgeo/cgeo/issues/17828), [#14038](https://github.com/cgeo/cgeo/issues/14038) (generic toast still used, `upstream/main/src/main/java/cgeo/geocaching/ui/ImageActivityHelper.java` 277-290), [#14302](https://github.com/cgeo/cgeo/issues/14302), [#17809](https://github.com/cgeo/cgeo/issues/17809), [#17583](https://github.com/cgeo/cgeo/issues/17583), [#17714](https://github.com/cgeo/cgeo/issues/17714) (safeguard in `GCWebAPI.java` 433-440, but reopened and root cause open), [#17853](https://github.com/cgeo/cgeo/issues/17853) (home screen still shows only "%d logged offline"), [#17857](https://github.com/cgeo/cgeo/issues/17857), [#17868](https://github.com/cgeo/cgeo/issues/17868), [#17872](https://github.com/cgeo/cgeo/issues/17872), [#17854](https://github.com/cgeo/cgeo/issues/17854), [#13385](https://github.com/cgeo/cgeo/issues/13385) (duplicate target), [#17291](https://github.com/cgeo/cgeo/issues/17291) (local-time offset still used in `LogUtils.java` 67; the fix PR #17430 is not in master), [#17801](https://github.com/cgeo/cgeo/issues/17801) (`CacheArtefactParser.java` has `{c:geo-start}` parsing, but the listing-scan request is open), [#16092](https://github.com/cgeo/cgeo/issues/16092), [#17107](https://github.com/cgeo/cgeo/issues/17107), [#13466](https://github.com/cgeo/cgeo/issues/13466) (`CompassMiniView` is only in list and detail views, not on the map)

```cleanup-result
#17828 keep-open
#14038 keep-open
#14302 keep-open
#17809 keep-open
#17583 keep-open
#17739 waiting
#17714 keep-open
#17853 keep-open
#17857 keep-open
#17868 keep-open
#17872 keep-open
#17854 keep-open
#13385 keep-open
#15879 duplicate
#17242 duplicate
#17291 keep-open
#17801 keep-open
#16092 keep-open
#17107 keep-open
#13466 keep-open
```
