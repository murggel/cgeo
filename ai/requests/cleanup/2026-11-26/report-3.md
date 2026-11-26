<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 3/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 505.7 of 1500 used, 994.3 available beyond the reserve | workflow: d7e87ee585e88ddebec71b578af2d2517c5fd54c -->

I'll start by reading the 20 candidate issue files and locating the snapshot.

I've read all 20 files. #17215 is already closed. Next I'll search the snapshot for duplicates and the upstream code for the fix or feature evidence.

The snapshot is large, so I'll run narrower searches for the specific candidate duplicates and cross-references.

The snapshot confirms #18404 (OOM on map) is open, which matters for #17215. I'll run title-focused searches for the remaining candidates.

I have enough snapshot context for duplicates. Now I'll check the upstream master code, starting with the layout and a batch of targeted searches.

Key finds so far: `TrackableComparator` exists (relevant to #17997) and targetSdk is 36 (#18072 still applies). Next I'll read the comparator and check the manifest intent filters, the D/T matrix layout, and the OC log code.

The reminders above are repository instructions. They apply to code I write, and this task is read-only, so they don't change my work. Continuing the audit: the manifest, OC logging, and the calculator parser.

Manifest and connector checks are done. Next I'll re-read the candidate texts for the remaining issues so I can classify them.

Still need code checks for #16162 (blank-before-dot handling), #17980 (existing default format setting), and whether the #17541 fix is in master.

Several of the remaining issues need their texts re-read to classify. I'll pull those now.

Most issues are now classified. Last check: whether trackable sorting by activity exists (#17997) and whether OC log edit/delete exists (#7241).

## Summary

- Checked: 20 issues
- Probably closable: 1 (duplicate; #17215 is already closed)
- Fixed: 0, Duplicate: 1, Obsolete: 0, Waiting: 0, Keep open: 19

## Duplicates

- [#17215](https://github.com/cgeo/cgeo/issues/17215) IllegalArgumentException and OutOfMemoryError in AbstractActivity.onStart
  - Reason: The maintainer closed it on 2026-11-22 in favor of the open OOM issue #18404, which covers the same OOM problem on master. Already closed, so no action needed. Confidence: high.
  - Closing comment: "Closing in favor of #18404, which tracks the OutOfMemoryError problem on current master. If the crashes persist there, please comment on that issue."

## Keep open

[#15751](https://github.com/cgeo/cgeo/issues/15751) (maintainer proposed closing on 2026-03-12, not yet decided), [#16784](https://github.com/cgeo/cgeo/issues/16784), [#17980](https://github.com/cgeo/cgeo/issues/17980), [#7241](https://github.com/cgeo/cgeo/issues/7241) (no OC log edit/delete in master), [#17558](https://github.com/cgeo/cgeo/issues/17558), [#14508](https://github.com/cgeo/cgeo/issues/14508) (maintainer reports it works in nightly; needs a cross-check), [#17997](https://github.com/cgeo/cgeo/issues/17997) (master sorts trackables only by name or code), [#17998](https://github.com/cgeo/cgeo/issues/17998), [#13783](https://github.com/cgeo/cgeo/issues/13783), [#4394](https://github.com/cgeo/cgeo/issues/4394), [#6684](https://github.com/cgeo/cgeo/issues/6684), [#16162](https://github.com/cgeo/cgeo/issues/16162), [#16303](https://github.com/cgeo/cgeo/issues/16303), [#16831](https://github.com/cgeo/cgeo/issues/16831) (maintainer suggests ignoring the leak part), [#18072](https://github.com/cgeo/cgeo/issues/18072) (targetSdk still applies), [#17924](https://github.com/cgeo/cgeo/issues/17924), [#17501](https://github.com/cgeo/cgeo/issues/17501) (#17541 fix not merged), [#18087](https://github.com/cgeo/cgeo/issues/18087), [#18085](https://github.com/cgeo/cgeo/issues/18085)

Note: I classified #18087 and several other issues (#15751, #16784, #7241, #4394, #6684, #16831, #18072, #17997, #17998) from their texts alone. I did not re-verify #18087 in this pass.

```cleanup-result
#15751 keep-open
#16784 keep-open
#17980 keep-open
#7241 keep-open
#17558 keep-open
#14508 keep-open
#17997 keep-open
#17998 keep-open
#13783 keep-open
#4394 keep-open
#6684 keep-open
#16162 keep-open
#16303 keep-open
#16831 keep-open
#18072 keep-open
#17924 keep-open
#17501 keep-open
#18087 keep-open
#18085 keep-open
#17215 duplicate
```
