<!-- task: review-pr | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | PR: #18952 | PR head: f4dbefefe17f9ef3feaf81cd1fcf71d256f2c4b3 | issue snapshot: 2026-11-15 | provider: claude | workflow: e79e0e579a8c67a9ecdeb4d3b6498636f3784252 -->

## 1. Base branch
The base is the **release branch** (`release @ f3cc3f1`). The PR says `FieldNotes` is identical on release and master. The patch doesn't use any master-only code. `GCConnector.getInstance().canHandle(...)` is long-standing and I didn't check it against the release branch. I couldn't compare `upstream/` against the release base, so that part is unverified.

## 2. Findings
No actionable findings identified.

- **Ordering:** GC records are now written to `gcRecords` and all others to `otherRecords`. `getContent()` concatenates them with GC first, and order within each group is kept (`FieldNotes.java:45-66`).
- **Report-problem record:** The extra record created for a "report problem" log recurses through `add(...)` with the same cache. It lands in the same group right after its parent record, and `size` is incremented as before.
- **Checks:** `writeToFolder` uses `getContent()`, so the written file is consistent. The multi-line test is valid.

**Release-risk check:** The change is small and targeted. It adds no new preferences, strings, dependencies, database changes or features, and it uses no master-only code.

**Remaining limitations** (the PR says the first of these is unchanged):
- A file with no GC record is still rejected by geocaching.com.
- If `canHandle` ever returned false for a valid GC code, that record would be sorted into the other group. `GCConnector`'s geocode matching decides this, and I didn't verify it.

## 3. Behavior changes
- **Intended and documented:** In the exported field notes file, GC records now come first and other platforms' records follow. Each group keeps its order and no record is dropped. This matches the description.
- **Intended but undocumented:** None.
- **Unintended or side effect:** The record order in the file now differs from the list order for mixed-platform exports. This affects every consumer of `FieldNotes`, including the saved file, and not only the geocaching.com upload. The description says "the same file is written", but the order is different. The change is deliberate and minor.

## 4. Issues fixed by this PR

**Referenced issues**
- https://github.com/cgeo/cgeo/issues/14935 "Fieldnotes export with upload to geocaching.com fails in a multi platform use case" (to be verified)
  - **Classification:** likely fixed. **Confidence:** medium.
  - **Reasoning:** The title matches the described cause: a mixed-platform export fails to upload. The change in `FieldNotes.java:45-66` puts the GC records first. The entry is from 2023-12 with 0 comments, and I could only read its title.
  - **How to verify:** Log offline for one GC and one OC cache, with the OC log most recent. Export from History with upload. The upload should succeed.
- #18947 is not in the snapshot, so it is either newer than the snapshot or closed. Going by the PR description, the same scenario applies and the change plausibly fixes it. I can't verify this from the snapshot.

**Further fixed issues**
No further fixed issues identified. Search terms used: field note, fieldnotes, upload, export, multi platform, geocaching.com 400.

**Related but not fixed** (a maintainer might otherwise assume these are covered)
- https://github.com/cgeo/cgeo/issues/12702 "Fieldnotes upload behaves weird" (to be verified): same area, but I couldn't read the summary, so the cause is unknown. Low confidence.
- https://github.com/cgeo/cgeo/issues/14908 and https://github.com/cgeo/cgeo/issues/14909: upload of field notes to opencaching.de is a feature request. This PR does not provide it.

**Recommendation:** The description should reference `fixes #14935`, and `fixes #18947` once that issue is confirmed.
