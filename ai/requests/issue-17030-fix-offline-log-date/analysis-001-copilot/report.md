<!-- upstream: cgeo/cgeo@08d806f589eb38f0346ba7edc4c208c9d964ed95 | issue: #17030 | cli: 1.0.105 -->

# Analysis of #17030: Caches shown without log date/time in history list

## 1. Issue summary
After quick offline logging from the map, some caches show no date/time in the history list. They sort to the bottom, below entries from 2024. The offline logs themselves exist, and the list view shows them. SammysHP says the 0:00 reset is old behaviour (#9653). The reporter says the date is now lost entirely, which is worse than before. Support tickets report the same, one of them as far back as 2025.04.

## 2. Relevant components (verified)
- `Geocache.storeLogOffline` (`models/Geocache.java:623-650`): saves the log with `DataStore.saveLogOffline`, then calls `DataStore.saveVisitDate(geocode, logEntry.date)` (line 638).
- `DataStore.saveVisitDate` and `setVisitDate` (`storage/DataStore.java:5805`, `5040-5062`): update `cg_caches.visiteddate` directly with SQL.
- `DataStore.storeIntoDatabase` (`DataStore.java:2730`): writes `cache.getVisitedDate()` into `visiteddate` on every full cache save.
- History list:
  - `HISTORY_COUNT` (`DataStore.java:5728`) and `ListIdGeocacheFilter.java:53` include caches where `visiteddate > 0 OR geocode IN offline logs`.
  - `VisitComparator` (`sorting/VisitComparator.java`) sorts on `visiteddate`.
  - `CacheListAdapter.java:529` shows the history date info only if `getVisitedDate() > 0`. Otherwise it shows the normal info line, which has no date.
- Other writers of `visitedDate`:
  - `LogUtils.adaptCacheCommonsAfterLogging` (`LogUtils.java:377,381`) sets it only for online found/DNF logs.
  - GPX parsers and `GCParser.java:1769`.
  - `DeleteCachesCommand` (`:242`, `:273`) restores it on undo.

## 3. Technical analysis
**Facts**
- Offline logs make a cache appear in history even when `visiteddate` is 0. These caches get no date text and sort last, which matches the symptoms.
- `storeLogOffline` never calls `setVisitedDate` on the in-memory `Geocache`. It only updates the DB row.
- `storeIntoDatabase` writes the in-memory `visitedDate` back to the DB.

**Hypothesis (not reproduced)**
- A later `DataStore.saveCache` on the same, still-cached `Geocache` object resets `visiteddate` to its stale in-memory value, which is usually 0. The 0 value is unconditional in `storeIntoDatabase`.
- Plausible triggers on the map:
  - the cache detail refresh or sheet loading;
  - the cache being added to a list;
  - a refresh from the server, which uses `SAVE_ALL`.
- In the issue's workflow, the cache info sheet on the map holds the object and the quick log is made on it. Other map or sheet activity can then save the cache again.
- This would explain "some but not all" caches and why the date is fully lost. The old 0:00 reset is a different mechanism, likely a date-only value being applied.
- I did not check the quick-log code path on the map or the `saveCache` merge logic. I also did not check git history for a regression around 2025.04.

## 4. Possible solution
- **Minimal:** in `Geocache.storeLogOffline`, call `setVisitedDate(logEntry.date)` on the instance as well as `saveVisitDate`. The in-memory and DB values then stay consistent. Alternatively, put the visit-date update into the same `saveCache` call.
- **Defensive alternative:** in `storeIntoDatabase`, don't overwrite a non-zero DB `visiteddate` with 0 (e.g. `MAX` semantics). This also protects against other stale writers, but it blocks intentional clearing. Intentional clears use `clearVisitDate`, which writes SQL directly, so this may be acceptable.
- **Display/sort fallback:** for caches that have an offline log but `visiteddate == 0`, use the offline log date in sorting and display. This is more invasive (SQL join in `VisitComparator`).
- Consider also covering the existing broken data by a one-time repair, though that is likely not worth it.

## 5. Risks and tests
**Risks**
- Setting the in-memory date also affects GPX export (`GpxSerializer.java:221`) and the "found" info shown in the details.
- Overwriting offline-log dates when a log is edited. Check what date an offline log should carry when it is changed or deleted.
- `DeleteCachesCommand` undo relies on the current visited date.

**Tests**
- A unit/instrumented test in `DataStoreTest` or `Geocache` tests:
  1. Store an offline log with a non-zero date.
  2. Call `saveCache(SAVE_ALL)` on the same cached instance.
  3. Assert that `visiteddate` is still non-zero when reloaded from the DB.
- A manual test: quick-log several caches from the map, then check the history list ordering and date text.

## 6. Open questions
- What exact action sequence in the reporter's flow triggers the stale write? A reproduction is needed, since the issue is labelled "Feedback required".
- Why did the problem worsen around 2025.04? Git history and logs from the support tickets are needed to answer this.

