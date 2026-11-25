<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 1/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 494.6 of 1500 used, 705.4 available beyond the reserve | workflow: 8c6dd3a0e6a5bb2ce4f7f91644e7cd6a3ab23cf2 -->

I'll start by checking which candidate files exist and what the snapshot looks like.

All 20 candidate files exist. Reading them now, in parallel.

I've read all 20 candidate texts. Now I'll check the code and snapshot for the claims that could settle them: highlights, leak and log-date handling, PN upload visibility, last-selection, and duplicates.

The leak and HashMap lines still look unchanged, and the PN button code is present. I'll inspect the specific code sections next.

Continuing the review. The tool results so far show the PN upload button is still present and no PCN log macro or projection-waypoint generation exists. Next I'm checking the OC highlight code, the PN button visibility logic, the event-date restriction, and the image edit dialog.

# Issue cleanup report

**Summary:** 20 issues checked. Probably closable: 0 fixed, 0 duplicate, 0 obsolete, 0 waiting. The other 20 stay open.

## Keep open

[#16791](https://github.com/cgeo/cgeo/issues/16791), [#5182](https://github.com/cgeo/cgeo/issues/5182), [#16802](https://github.com/cgeo/cgeo/issues/16802), [#16552](https://github.com/cgeo/cgeo/issues/16552), [#16832](https://github.com/cgeo/cgeo/issues/16832), [#15894](https://github.com/cgeo/cgeo/issues/15894), [#16903](https://github.com/cgeo/cgeo/issues/16903), [#16428](https://github.com/cgeo/cgeo/issues/16428), [#13746](https://github.com/cgeo/cgeo/issues/13746), [#16941](https://github.com/cgeo/cgeo/issues/16941), [#16952](https://github.com/cgeo/cgeo/issues/16952), [#16820](https://github.com/cgeo/cgeo/issues/16820), [#12196](https://github.com/cgeo/cgeo/issues/12196), [#16018](https://github.com/cgeo/cgeo/issues/16018), [#16986](https://github.com/cgeo/cgeo/issues/16986), [#16997](https://github.com/cgeo/cgeo/issues/16997), [#14547](https://github.com/cgeo/cgeo/issues/14547), [#15482](https://github.com/cgeo/cgeo/issues/15482), [#16825](https://github.com/cgeo/cgeo/issues/16825), [#10925](https://github.com/cgeo/cgeo/issues/10925)

Reasons for the more notable ones:
- [#16802](https://github.com/cgeo/cgeo/issues/16802): `MapMarkerUtils.addHighlighting` (`upstream/main/src/main/java/cgeo/geocaching/utils/MapMarkerUtils.java`, lines 947–962) still uses the single GC highlight drawable for all caches.
- [#15482](https://github.com/cgeo/cgeo/issues/15482): the PN upload button is still hidden unless `canAddPersonalNote` (`CacheDetailActivity.java`, ~lines 1785–1795). The "always show" change is not in upstream.
- [#16820](https://github.com/cgeo/cgeo/issues/16820): no personal-note log macro exists in the code.
- [#16952](https://github.com/cgeo/cgeo/issues/16952): no projection support in waypoint generation was found.
- [#10925](https://github.com/cgeo/cgeo/issues/10925): #17007 only covers list ordering. The "last selection" shortcut in the move dialog is not implemented.
- [#12196](https://github.com/cgeo/cgeo/issues/12196): found state is fixed by PR #14318, but no found date is available from the APIs (comment by ztNFny, 2025-05-22).
- [#16428](https://github.com/cgeo/cgeo/issues/16428): already labelled "Won't Fix" by the maintainers, so the maintainers should decide whether to close it.

```cleanup-result
#16791 keep-open
#5182 keep-open
#16802 keep-open
#16552 keep-open
#16832 keep-open
#15894 keep-open
#16903 keep-open
#16428 keep-open
#13746 keep-open
#16941 keep-open
#16952 keep-open
#16820 keep-open
#12196 keep-open
#16018 keep-open
#16986 keep-open
#16997 keep-open
#14547 keep-open
#15482 keep-open
#16825 keep-open
#10925 keep-open
```
