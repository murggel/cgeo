<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 4/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 481.8 of 1500 used, 718.2 available beyond the reserve | workflow: 82cc223d3f1a7bb66fe3741eb4cd0662da311006 -->

I'll start by checking which candidate files exist and how the snapshot is laid out.

I'll read the 20 candidate files in parallel.

I've read all 20 issues. Next I'll check the snapshot for duplicates and the upstream code for the feature-related claims.

Snapshot confirms duplicates for 16187 (older related issues #11722, #8626, #14329). Now I'll check the upstream code for the fix/feature claims.

The broad grep is too noisy, so I'll run narrower checks on the specific claims.

The upstream instructions in that message are coding-style guidance for code I write. This task is a read-only report, so I'm not writing code and it doesn't change the work. Continuing with the remaining code checks.

Checked 20 issues: 0 fixed, 1 duplicate, 0 obsolete, 1 waiting, 18 keep-open. Probably closable: 2.

## Duplicates

- [#16187](https://github.com/cgeo/cgeo/issues/16187) Share Intent Receiver: track.gpx
  - Reason: the issue requests that a GPX track or route opened from a file is not treated as a cache list. [#11722](https://github.com/cgeo/cgeo/issues/11722) (2021) asks for exactly this, and the reporter's own duplicate list also names [#14329](https://github.com/cgeo/cgeo/issues/14329) and [#8626](https://github.com/cgeo/cgeo/issues/8626). It is already labeled Duplicate. Confidence: high.
  - Closing comment: "Thanks for the report! This is a duplicate of #11722, which tracks the same request to import GPX tracks and routes when opening a file. We're closing this one in favour of it. If the problem persists or you have something to add, feel free to comment on #11722 or reopen this issue."

## Waiting for information

- [#16362](https://github.com/cgeo/cgeo/issues/16362) Lines between tiles on Unified MF
  - Reason: on 2024-11-18 a maintainer (devemux86) asked whether the artifact also appears in Android or desktop Cruiser, to tell a known map-writer grid artifact from something else. The reporter has not replied in over two years. Confidence: medium.
  - Closing comment: "Thanks for the report! Our last question was whether this also shows in Android or desktop Cruiser, which would show whether it is the known map-writer grid artifact. As we have not heard back, we are closing this for now. Please comment or reopen with that test result if the problem still occurs."

## Keep open

[#16038](https://github.com/cgeo/cgeo/issues/16038), [#16010](https://github.com/cgeo/cgeo/issues/16010), [#16040](https://github.com/cgeo/cgeo/issues/16040), [#16030](https://github.com/cgeo/cgeo/issues/16030), [#16066](https://github.com/cgeo/cgeo/issues/16066), [#15723](https://github.com/cgeo/cgeo/issues/15723), [#16133](https://github.com/cgeo/cgeo/issues/16133), [#16143](https://github.com/cgeo/cgeo/issues/16143), [#15999](https://github.com/cgeo/cgeo/issues/15999), [#16174](https://github.com/cgeo/cgeo/issues/16174), [#9967](https://github.com/cgeo/cgeo/issues/9967), [#15641](https://github.com/cgeo/cgeo/issues/15641), [#16145](https://github.com/cgeo/cgeo/issues/16145), [#15615](https://github.com/cgeo/cgeo/issues/15615), [#15901](https://github.com/cgeo/cgeo/issues/15901), [#16326](https://github.com/cgeo/cgeo/issues/16326), [#16124](https://github.com/cgeo/cgeo/issues/16124), [#16370](https://github.com/cgeo/cgeo/issues/16370)

Notes where a later look may help:
- #16038: the GC code substring filter exists (`GeocodeGeocacheFilter`, "Contains"), but the coordinate range filter does not.
- #16030: the maintainer's 2026-11-22 comment asks to remove the highlight, but `coordinate_input_dialog.xml` line 29 still applies `border_active`.
- #16040: the 2024 dev meeting chose to keep the current solution, so this may be declined rather than open.
- #16145: maintainers lean against the option.

```cleanup-result
#16038 keep-open
#16010 keep-open
#16040 keep-open
#16030 keep-open
#16066 keep-open
#15723 keep-open
#16133 keep-open
#16143 keep-open
#15999 keep-open
#16174 keep-open
#16187 duplicate
#9967 keep-open
#15641 keep-open
#16145 keep-open
#15615 keep-open
#15901 keep-open
#16326 keep-open
#16124 keep-open
#16370 keep-open
#16362 waiting
```
