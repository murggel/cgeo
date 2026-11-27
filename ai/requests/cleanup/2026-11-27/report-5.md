<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 5/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 518.6 of 1500 used, 981.4 available beyond the reserve | workflow: 707a4f36d3e52637b5c2b6d05f14cfba4ef13e01 -->

I'll start by checking which candidate files exist and what the snapshot says about these 20 issues.

The snapshot gives one line per issue. Next I'll read the 20 full candidate files in parallel.

Several are feature requests or proposals that need code checks. Reading the remaining candidate files, including the large 18823 in chunks.

Most candidates are read. The large files (18404, 10963) need their comment headers and last comments, so I'll grep for comment dates first.

I have all the issue text now. Next I'll check the code in `upstream/` for the claimed fixes and features, using grep only.

Some greps returned nothing, so I'll view the exact code locations directly and widen the filter and export searches.

Several claims are now checked: the image-size "Unchanged" option, the Rating filter, the AsyncTask base class, and the missing GPX offline-log and filter export code all still exist. A few more code checks remain for the personal-note keyboard fix, trackable visit default, waypoint translation, and map hide-all.

Waypoint translation is only the external-app action, so the offline version is still missing. One more check on the keyboard handling for the personal-note fix.

## Summary

- Checked: 20 issues
- Probably fixed: 0
- Duplicates: 0
- No longer applicable: 0
- Waiting for information: 0
- Keep open: 20

## Keep open

[#18796](https://github.com/cgeo/cgeo/issues/18796), [#18812](https://github.com/cgeo/cgeo/issues/18812), [#17842](https://github.com/cgeo/cgeo/issues/17842), [#18818](https://github.com/cgeo/cgeo/issues/18818), [#18819](https://github.com/cgeo/cgeo/issues/18819), [#18804](https://github.com/cgeo/cgeo/issues/18804), [#18826](https://github.com/cgeo/cgeo/issues/18826), [#18404](https://github.com/cgeo/cgeo/issues/18404), [#18799](https://github.com/cgeo/cgeo/issues/18799), [#18820](https://github.com/cgeo/cgeo/issues/18820), [#6054](https://github.com/cgeo/cgeo/issues/6054), [#18670](https://github.com/cgeo/cgeo/issues/18670), [#18823](https://github.com/cgeo/cgeo/issues/18823), [#18837](https://github.com/cgeo/cgeo/issues/18837), [#10963](https://github.com/cgeo/cgeo/issues/10963), [#18401](https://github.com/cgeo/cgeo/issues/18401), [#18732](https://github.com/cgeo/cgeo/issues/18732), [#18829](https://github.com/cgeo/cgeo/issues/18829), [#18852](https://github.com/cgeo/cgeo/issues/18852), [#18856](https://github.com/cgeo/cgeo/issues/18856)

Notes worth a later look:
- [#17842](https://github.com/cgeo/cgeo/issues/17842): a maintainer says PR #18086 fixed it, but the issue is still open and October reports persist. Master has IME inset handling in `upstream/main/src/main/java/cgeo/geocaching/activity/AbstractActivity.java:72`, but I could not confirm it addresses the personal-note case. Verify on a device.
- [#6054](https://github.com/cgeo/cgeo/issues/6054): a maintainer proposed closing it as roughly ten years old. Age alone is not evidence, so the maintainer should decide.
- [#18812](https://github.com/cgeo/cgeo/issues/18812): may be superseded by #17586, which I did not verify.

```cleanup-result
#18796 keep-open
#18812 keep-open
#17842 keep-open
#18818 keep-open
#18819 keep-open
#18804 keep-open
#18826 keep-open
#18404 keep-open
#18799 keep-open
#18820 keep-open
#6054 keep-open
#18670 keep-open
#18823 keep-open
#18837 keep-open
#10963 keep-open
#18401 keep-open
#18732 keep-open
#18829 keep-open
#18852 keep-open
#18856 keep-open
```
