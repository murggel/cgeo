<!-- task: cleanup-issues | upstream: cgeo/cgeo@a2017cbd86d01a8f274852bcd0ec2ddce990aed3 | issue snapshot: 2026-11-15 | batch: 4/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 445.7 of 1500 used, 754.3 available beyond the reserve | workflow: 80e10c46acfc5ada8d2ff8809d23eb8d64f9209b -->

I'll start by checking which candidate files exist and how the snapshot is laid out.

The snapshot has all 20 entries. Now I'll read the candidate files in parallel.

I've read all 20 candidates. Next I'll check the snapshot for the issues they reference as duplicates, and search it for related keywords.

That keyword search was too broad. I'll narrow it to the specific referenced numbers and the most relevant keywords.

The referenced issues #6889, #10004, #11045, #10002, #8928, #13126 and #13152 aren't in the open snapshot, so they aren't open duplicates. Now I'll check the upstream code for the fix/feature candidates.

Several leads to check: the downloader service, the empty-list prompt in `CacheListActivity`, and the PMO/locked logging paths.

Continuing the analysis. Next I'll check where the empty-list prompt is triggered (for #12004), and how the downloader handles a missing download type (for #13113).

That search was too broad. I'll narrow it to the specific symbols.

The service has moved (it now delegates to `ReceiveDownload`), so I'll check the null handling there, and the CHECK_IF_EMPTY logic in `CacheListActivity`.

Found the #13113 null check (`ReceiveDownload.java` ~line 70), but the root cause is still unexplained, so I'll treat that as a doubt case. Next, the #12004 empty-list prompt path.

The empty-list check still runs for list refreshes. I need to see whether the PQ import path triggers it, so I'll check the import callback and `refreshListAtLastPosition` callers.

The PQ import goes through `importGpxAttachementFinishedHandler`, so I'll check what that handler does after the import finishes.

Found the #12004 mechanism: `onResume` (`CacheListActivity.java` ~533-537) runs the empty-list check on return from the PQ picker, possibly before the async import completes. That's still present, so #12004 stays open. Next I'll check the locked-cache message (#13196), the variable-view scrolling (#13253), and the image date (#11026).

The variable view has a `MINIMALISTIC` display type that already exists, relevant to #13251. I'll check that, plus the add-variable path (#13253), and look for the log-error strings (#13196) under a different wording.

The variable list already has a MINIMALISTIC display type, and the add path (line 382-387) sorts the new variable position, which is relevant to #13251/#13253. I'll confirm the candidate texts for those two and check the viewport clamp for #13266.

## Summary

- Checked: 20 issues
- Probably fixed: 0
- Duplicates: 0
- No longer applicable: 0
- Waiting for information: 0
- Keep open: 20

## Keep open

[#11055](https://github.com/cgeo/cgeo/issues/11055), [#13062](https://github.com/cgeo/cgeo/issues/13062), [#12729](https://github.com/cgeo/cgeo/issues/12729), [#13113](https://github.com/cgeo/cgeo/issues/13113), [#13139](https://github.com/cgeo/cgeo/issues/13139), [#13146](https://github.com/cgeo/cgeo/issues/13146), [#13153](https://github.com/cgeo/cgeo/issues/13153), [#12788](https://github.com/cgeo/cgeo/issues/12788), [#13151](https://github.com/cgeo/cgeo/issues/13151), [#13208](https://github.com/cgeo/cgeo/issues/13208), [#12951](https://github.com/cgeo/cgeo/issues/12951), [#13227](https://github.com/cgeo/cgeo/issues/13227), [#13165](https://github.com/cgeo/cgeo/issues/13165), [#13251](https://github.com/cgeo/cgeo/issues/13251), [#13252](https://github.com/cgeo/cgeo/issues/13252), [#13253](https://github.com/cgeo/cgeo/issues/13253), [#13196](https://github.com/cgeo/cgeo/issues/13196), [#13266](https://github.com/cgeo/cgeo/issues/13266), [#12004](https://github.com/cgeo/cgeo/issues/12004), [#11026](https://github.com/cgeo/cgeo/issues/11026)

Notes where a later look is worthwhile:
- [#12004](https://github.com/cgeo/cgeo/issues/12004): the empty-list prompt can appear before the asynchronous import finishes (`CacheListActivity.java`, `onResume`). The bug appears to remain.
- [#13266](https://github.com/cgeo/cgeo/issues/13266): no viewport size limit in `GCMap.searchByViewport`, so the 400 errors are still possible.
- [#13113](https://github.com/cgeo/cgeo/issues/13113): a null guard now exists in `ReceiveDownload.java`, but the root cause is not explained.
- [#12951](https://github.com/cgeo/cgeo/issues/12951): the requested integration is not in upstream code.
- [#13251](https://github.com/cgeo/cgeo/issues/13251): the maintainer comment leans toward dropping the request, so it could be closed as a feature-request decision.

```cleanup-result
#11055 keep-open
#13062 keep-open
#12729 keep-open
#13113 keep-open
#13139 keep-open
#13146 keep-open
#13153 keep-open
#12788 keep-open
#13151 keep-open
#13208 keep-open
#12951 keep-open
#13227 keep-open
#13165 keep-open
#13251 keep-open
#13252 keep-open
#13253 keep-open
#13196 keep-open
#13266 keep-open
#12004 keep-open
#11026 keep-open
```
