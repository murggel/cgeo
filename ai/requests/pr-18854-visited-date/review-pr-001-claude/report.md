<!-- task: review-pr | upstream: cgeo/cgeo@f26cfc0f009b4bbbd83409fb01e5236359631ff8 | PR: #18854 | PR head: 8840be35fecd17c7d7f6109b50586f6e25224f05 | provider: claude | workflow: 740eda0d8ac7fb26ceae5398b9033db834c691f6 -->

1. **Base branch:** The base is the `release` branch (`5b92630…`), not master. I only compared against `pr-head/`. I did not check whether `DataStore.saveVisitDate`, `OfflineLogEntry.Builder` and the other APIs the PR uses match the release base. They are plain calls and probably exist there.

2. **Findings**

   **1. The change broadcast is lost after a background log upload** (medium)
   - Location: `main/src/main/java/cgeo/geocaching/service/LogPostingService.java:147-155`, using `Geocache.clearOfflineLog` at `main/src/main/java/cgeo/geocaching/models/Geocache.java:687-691`.
   - Before the PR, the service called `cache.clearOfflineLog(null)` and then `cache.notifyChange()`. The no-arg `notifyChange()` uses the application context (`Geocache.java:229`) and sends `GeocacheChangedBroadcastReceiver.sendBroadcast`.
   - The PR removes that call. `clearOfflineLog(null)` ends in `notifyChange(null)`, and that only sends the broadcast when the context is non-null (`Geocache.java:237`).
   - Scenario: an offline log is uploaded by the service while a cache list or detail screen is open. The screen may not get the "geocache changed" broadcast, so the "has offline log" marker can stay stale until the screen reloads.
   - Fix: pass `CgeoApplication.getInstance()` to `clearOfflineLog`, or keep the `notifyChange()` call.

   **2. Deleting an offline log leaves the visited date it set** (low, unclear if intended)
   - Location: `main/src/main/java/cgeo/geocaching/models/Geocache.java:632-647` and `:687`.
   - `storeLogOffline` now overwrites the visited date, with a found or DNF log or when the date is 0. `clearOfflineLog` does not restore the previous value. The new test `clearOfflineLogKeepsVisitedDate` confirms this.
   - Scenario: a user saves a Found/DNF offline log and then deletes it. The cache keeps a "visited" date for a visit that was discarded. The old date is also lost.
   - Whether this is deliberate is unclear. If it is, the description should say so.

3. **Behavior changes**

   **Intended and documented**
   - The visited date is now set on the in-memory cache object when an offline log is stored. This matches the description ("don't rely on db"), though the description is very brief.

   **Intended but undocumented** (please add these to the description)
   - A note or other non-visit offline log no longer overwrites an existing visited date. It only sets the date when it is 0. Previously any offline log overwrote it in the DB.
   - `LogType.isVisitLog()` is new. In `LogUtils`, the visited date is now set for every visit-log type. This is the same set of types as before, so there is no change in practice.
   - `OkapiClient.getCacheFoundDate` now also accepts `WEBCAM_PHOTO_TAKEN` logs, because `isFoundLog()` includes that type. Previously only FOUND_IT, ATTENDED and DNF counted.
   - `CacheLogsViewCreator` now deletes an offline log through `cache.clearOfflineLog(activity)`. That also resets the in-memory `hasLogOffline` flag, which the old code did not.
   - `LogPostingService` now skips the clear when the cache is null. Before, it would have thrown a NullPointerException.

   **Unintended or side effect**
   - The lost broadcast after background upload (Finding 1).
   - Deleting an offline log keeps the visited date it set (Finding 2).

   **Release-branch risk:** These are small, targeted changes, and I found no new preferences, strings, dependencies or database changes. The new `isVisitLog()` method and the added test are mild extras. The `OkapiClient` change goes slightly beyond a targeted fix.
