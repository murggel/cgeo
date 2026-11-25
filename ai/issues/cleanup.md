# Issue cleanup

Written by the workflow after every cleanup run and issue snapshot; do not edit by hand. The
reports are in the request folders `ai/requests/cleanup/<name>/` (`report.md`, further batches
of the same night `report-2.md`, ...). The AI closes nothing: check each issue in its report
before closing it.

## Contents

- [Issues that can probably be closed](#issues-that-can-probably-be-closed)
  - [Probably fixed (39)](#probably-fixed-39)
  - [Duplicates (13)](#duplicates-13)
  - [No longer applicable (10)](#no-longer-applicable-10)
  - [Waiting for information (7)](#waiting-for-information-7)
- [Reports (29)](#reports-29)

## Issues that can probably be closed

The latest result per issue, by category; a later run that keeps an issue open removes it here.

### Probably fixed (39)

| Issue | Title | Report |
|---|---|---|
| [#447](https://github.com/cgeo/cgeo/issues/447) | caches should be sorted relative to search centre, not phone coords | [2026-11-15](../requests/cleanup/2026-11-15/report.md) |
| [#1286](https://github.com/cgeo/cgeo/issues/1286) | Support of eniro maps | [2026-11-21 (5)](../requests/cleanup/2026-11-21/report-5.md) |
| [#2724](https://github.com/cgeo/cgeo/issues/2724) | GPX eport file naming | [2026-11-22 (5)](../requests/cleanup/2026-11-22/report-5.md) |
| [#2808](https://github.com/cgeo/cgeo/issues/2808) | Nearby search not supporting "load more" for OC | [2026-11-21 (2)](../requests/cleanup/2026-11-21/report-2.md) |
| [#3509](https://github.com/cgeo/cgeo/issues/3509) | Requests to disabled/unused connectors | [2026-11-21](../requests/cleanup/2026-11-21/report.md) |
| [#4549](https://github.com/cgeo/cgeo/issues/4549) | Implement checker for challenge caches | [2026-11-22 (5)](../requests/cleanup/2026-11-22/report-5.md) |
| [#5206](https://github.com/cgeo/cgeo/issues/5206) | GK: Search by tracking code | [2026-11-21 (5)](../requests/cleanup/2026-11-21/report-5.md) |
| [#6360](https://github.com/cgeo/cgeo/issues/6360) | Mass uploading personal notes should not be in Export menu | [2026-11-20](../requests/cleanup/2026-11-20/report.md) |
| [#6391](https://github.com/cgeo/cgeo/issues/6391) | Support Geocaching Australia API | [2026-11-21 (2)](../requests/cleanup/2026-11-21/report-2.md) |
| [#6511](https://github.com/cgeo/cgeo/issues/6511) | Add filter for gc friend that has found caches in your list | [2026-11-17](../requests/cleanup/2026-11-17/report.md) |
| [#6809](https://github.com/cgeo/cgeo/issues/6809) | Detect if OC-site is capable of log picture upload | [2026-11-21 (4)](../requests/cleanup/2026-11-21/report-4.md) |
| [#7464](https://github.com/cgeo/cgeo/issues/7464) | Make export functions cancellable | [2026-11-21](../requests/cleanup/2026-11-21/report.md) |
| [#7990](https://github.com/cgeo/cgeo/issues/7990) | No way out if user permanently declined permission | [2026-11-21 (2)](../requests/cleanup/2026-11-21/report-2.md) |
| [#8334](https://github.com/cgeo/cgeo/issues/8334) | Retracted cache listing not recognized | [2026-11-21 (2)](../requests/cleanup/2026-11-21/report-2.md) |
| [#8351](https://github.com/cgeo/cgeo/issues/8351) | Update AVD on CI | [2026-11-21 (2)](../requests/cleanup/2026-11-21/report-2.md) |
| [#9340](https://github.com/cgeo/cgeo/issues/9340) | Toast for "There may be more caches in this area" | [2026-11-23 (4)](../requests/cleanup/2026-11-23/report-4.md) |
| [#9855](https://github.com/cgeo/cgeo/issues/9855) | Central declaration of repositories | [2026-11-21 (4)](../requests/cleanup/2026-11-21/report-4.md) |
| [#10125](https://github.com/cgeo/cgeo/issues/10125) | Do not unconditionally store cache locally upon entering waypoint edit mode | [2026-11-21 (4)](../requests/cleanup/2026-11-21/report-4.md) |
| [#11023](https://github.com/cgeo/cgeo/issues/11023) | CI/Jenkins: make logcat output accessible for Test runs | [2026-11-25 (2)](../requests/cleanup/2026-11-25/report-2.md) |
| [#11394](https://github.com/cgeo/cgeo/issues/11394) | Provide error message returned by connector to user | [2026-11-24](../requests/cleanup/2026-11-24/report.md) |
| [#11849](https://github.com/cgeo/cgeo/issues/11849) | Avoid confirm dialog when waypoint is unchanged | [2026-11-24 (2)](../requests/cleanup/2026-11-24/report-2.md) |
| [#12077](https://github.com/cgeo/cgeo/issues/12077) | Have some options when trying to save search results to a list | [2026-11-25 (4)](../requests/cleanup/2026-11-25/report-4.md) |
| [#12241](https://github.com/cgeo/cgeo/issues/12241) | Calculated Waypoints refactoring: replace side-scrolling multi-column variable dialog with single l… | [2026-11-22](../requests/cleanup/2026-11-22/report.md) |
| [#12503](https://github.com/cgeo/cgeo/issues/12503) | Explicit white background in cache description not readable in dark mode | [2026-11-23](../requests/cleanup/2026-11-23/report.md) |
| [#12886](https://github.com/cgeo/cgeo/issues/12886) | Map filter for events: Displays events for wrong day | [2026-11-22 (3)](../requests/cleanup/2026-11-22/report-3.md) |
| [#13108](https://github.com/cgeo/cgeo/issues/13108) | Share cache together with corrected coordinates | [2026-11-24 (5)](../requests/cleanup/2026-11-24/report-5.md) |
| [#13640](https://github.com/cgeo/cgeo/issues/13640) | Lint: CustomSplashScreen | [2026-11-23 (2)](../requests/cleanup/2026-11-23/report-2.md) |
| [#13781](https://github.com/cgeo/cgeo/issues/13781) | Failure to show error toast | [2026-11-23 (3)](../requests/cleanup/2026-11-23/report-3.md) |
| [#13797](https://github.com/cgeo/cgeo/issues/13797) | ALC change of linear/random mode not detected | [2026-11-23](../requests/cleanup/2026-11-23/report.md) |
| [#14189](https://github.com/cgeo/cgeo/issues/14189) | NullPointerException on long tap on geocache waypoint | [2026-11-23 (2)](../requests/cleanup/2026-11-23/report-2.md) |
| [#14579](https://github.com/cgeo/cgeo/issues/14579) | Filter for missing T/D in 81er Matrix | [2026-11-23 (4)](../requests/cleanup/2026-11-23/report-4.md) |
| [#14983](https://github.com/cgeo/cgeo/issues/14983) | Move batch uploading notes/coords to background with proper notification | [2026-11-23 (5)](../requests/cleanup/2026-11-23/report-5.md) |
| [#14989](https://github.com/cgeo/cgeo/issues/14989) | No notification dot shown when directly launching into map | [2026-11-23 (5)](../requests/cleanup/2026-11-23/report-5.md) |
| [#15071](https://github.com/cgeo/cgeo/issues/15071) | Hyperlink in personal note is not parsed correctly | [2026-11-23 (5)](../requests/cleanup/2026-11-23/report-5.md) |
| [#16731](https://github.com/cgeo/cgeo/issues/16731) | OOM in detecting file type | [2026-11-24 (5)](../requests/cleanup/2026-11-24/report-5.md) |
| [#17041](https://github.com/cgeo/cgeo/issues/17041) | Beta version: IllegalStateException / missing context in DescriptionViewCreator | [2026-11-25 (3)](../requests/cleanup/2026-11-25/report-3.md) |
| [#17093](https://github.com/cgeo/cgeo/issues/17093) | RuntimeException in WherigoGameService.onCreate | [2026-11-25 (2)](../requests/cleanup/2026-11-25/report-2.md) |
| [#17375](https://github.com/cgeo/cgeo/issues/17375) | Upgrade to SDK35: Edge-to-Edge | [2026-11-25 (4)](../requests/cleanup/2026-11-25/report-4.md) |
| [#17485](https://github.com/cgeo/cgeo/issues/17485) | NPE in PersistableFolder.registerForIndirectChange | [2026-11-25 (5)](../requests/cleanup/2026-11-25/report-5.md) |

### Duplicates (13)

| Issue | Title | Report |
|---|---|---|
| [#7850](https://github.com/cgeo/cgeo/issues/7850) | Upload button for personal note missing | [2026-11-25 (2)](../requests/cleanup/2026-11-25/report-2.md) |
| [#11440](https://github.com/cgeo/cgeo/issues/11440) | Cleanup our DB | [2026-11-22](../requests/cleanup/2026-11-22/report.md) |
| [#11722](https://github.com/cgeo/cgeo/issues/11722) | Import GPX routes/trackes via click on file | [2026-11-22](../requests/cleanup/2026-11-22/report.md) |
| [#12459](https://github.com/cgeo/cgeo/issues/12459) | Heat Live map: Colors icon by Favorites | [2026-11-22 (2)](../requests/cleanup/2026-11-22/report-2.md) |
| [#14125](https://github.com/cgeo/cgeo/issues/14125) | Is it possible to keep the logged in session locally for a short time? | [2026-11-23 (2)](../requests/cleanup/2026-11-23/report-2.md) |
| [#14329](https://github.com/cgeo/cgeo/issues/14329) | Support importing GPX tracks/routes from external | [2026-11-24 (3)](../requests/cleanup/2026-11-24/report-3.md) |
| [#14931](https://github.com/cgeo/cgeo/issues/14931) | update only cache state | [2026-11-24 (5)](../requests/cleanup/2026-11-24/report-5.md) |
| [#15313](https://github.com/cgeo/cgeo/issues/15313) | wording of link to images (minor) | [2026-11-24](../requests/cleanup/2026-11-24/report.md) |
| [#15388](https://github.com/cgeo/cgeo/issues/15388) | Geokrety - support rate limiting system | [2026-11-24 (3)](../requests/cleanup/2026-11-24/report-3.md) |
| [#15924](https://github.com/cgeo/cgeo/issues/15924) | possibility to add waypoint for projection/offset | [2026-11-24 (3)](../requests/cleanup/2026-11-24/report-3.md) |
| [#16187](https://github.com/cgeo/cgeo/issues/16187) | Share Intent Receiver: track.gpx | [2026-11-24 (4)](../requests/cleanup/2026-11-24/report-4.md) |
| [#16516](https://github.com/cgeo/cgeo/issues/16516) | GC.com: load images from "Image Gallery" | [2026-11-24 (5)](../requests/cleanup/2026-11-24/report-5.md) |
| [#17423](https://github.com/cgeo/cgeo/issues/17423) | Improve UI for loading tracks versus routes | [2026-11-25 (5)](../requests/cleanup/2026-11-25/report-5.md) |

### No longer applicable (10)

| Issue | Title | Report |
|---|---|---|
| [#1863](https://github.com/cgeo/cgeo/issues/1863) | GCVote loading after gpx import | [2026-11-21](../requests/cleanup/2026-11-21/report.md) |
| [#3798](https://github.com/cgeo/cgeo/issues/3798) | Avoid database lookups for map JSON caches | [2026-11-21 (3)](../requests/cleanup/2026-11-21/report-3.md) |
| [#4248](https://github.com/cgeo/cgeo/issues/4248) | GCVote shown as "Active" although no password given | [2026-11-21](../requests/cleanup/2026-11-21/report.md) |
| [#4298](https://github.com/cgeo/cgeo/issues/4298) | Feature Request: Transmit .gpx file instead of URL via NFC | [2026-11-21](../requests/cleanup/2026-11-21/report.md) |
| [#6034](https://github.com/cgeo/cgeo/issues/6034) | Always show voting in log activity | [2026-11-21](../requests/cleanup/2026-11-21/report.md) |
| [#8144](https://github.com/cgeo/cgeo/issues/8144) | Map tiles get repainted each time screen is turned on | [2026-11-22 (5)](../requests/cleanup/2026-11-22/report-5.md) |
| [#8614](https://github.com/cgeo/cgeo/issues/8614) | Final flag lost on live map after opening popup | [2026-11-21 (3)](../requests/cleanup/2026-11-21/report-3.md) |
| [#10568](https://github.com/cgeo/cgeo/issues/10568) | Filtering for ALC fails after "Load more" in search results | [2026-11-21 (5)](../requests/cleanup/2026-11-21/report-5.md) |
| [#10656](https://github.com/cgeo/cgeo/issues/10656) | catch IllegalArgumentException for EC active without login information | [2026-11-21 (5)](../requests/cleanup/2026-11-21/report-5.md) |
| [#15358](https://github.com/cgeo/cgeo/issues/15358) | ToolbarWidgetWrapper: Progress display unsupported | [2026-11-24](../requests/cleanup/2026-11-24/report.md) |

### Waiting for information (7)

| Issue | Title | Report |
|---|---|---|
| [#10837](https://github.com/cgeo/cgeo/issues/10837) | Individual track and OC waypoints | [2026-11-25 (2)](../requests/cleanup/2026-11-25/report-2.md) |
| [#11112](https://github.com/cgeo/cgeo/issues/11112) | "Search by XYZ" should have a progress spinner while loading caches | [2026-11-23 (3)](../requests/cleanup/2026-11-23/report-3.md) |
| [#11927](https://github.com/cgeo/cgeo/issues/11927) | \[Nightly\] App Crash when leaving or rotating Live Map while it's still rendering | [2026-11-23 (5)](../requests/cleanup/2026-11-23/report-5.md) |
| [#16191](https://github.com/cgeo/cgeo/issues/16191) | found status of ALC is not automatically set | [2026-11-25 (2)](../requests/cleanup/2026-11-25/report-2.md) |
| [#16362](https://github.com/cgeo/cgeo/issues/16362) | Lines between tiles on Unified MF | [2026-11-24 (4)](../requests/cleanup/2026-11-24/report-4.md) |
| [#16977](https://github.com/cgeo/cgeo/issues/16977) | Tests -\> request was not successful: message=Forbidden | [2026-11-25 (2)](../requests/cleanup/2026-11-25/report-2.md) |
| [#17568](https://github.com/cgeo/cgeo/issues/17568) | \[Nightly\] Long distance routing behaves erratic | [2026-11-25 (5)](../requests/cleanup/2026-11-25/report-5.md) |

## Reports (29)

| Report | Provider | Checked | Fixed | Duplicates | Obsolete | Waiting | Can probably be closed |
|---|---|---|---|---|---|---|---|
| [2026-11-25 (5)](../requests/cleanup/2026-11-25/report-5.md) | copilot | 20 | 1 | 1 | 0 | 1 | [#17423](https://github.com/cgeo/cgeo/issues/17423) duplicate, [#17485](https://github.com/cgeo/cgeo/issues/17485) fixed, [#17568](https://github.com/cgeo/cgeo/issues/17568) waiting |
| [2026-11-25 (4)](../requests/cleanup/2026-11-25/report-4.md) | copilot | 20 | 2 | 0 | 0 | 0 | [#12077](https://github.com/cgeo/cgeo/issues/12077) fixed, [#17375](https://github.com/cgeo/cgeo/issues/17375) fixed |
| [2026-11-25 (3)](../requests/cleanup/2026-11-25/report-3.md) | copilot | 20 | 1 | 0 | 0 | 0 | [#17041](https://github.com/cgeo/cgeo/issues/17041) fixed |
| [2026-11-25 (2)](../requests/cleanup/2026-11-25/report-2.md) | copilot | 20 | 2 | 1 | 0 | 3 | [#10837](https://github.com/cgeo/cgeo/issues/10837) waiting, [#16191](https://github.com/cgeo/cgeo/issues/16191) waiting, [#16977](https://github.com/cgeo/cgeo/issues/16977) waiting, [#7850](https://github.com/cgeo/cgeo/issues/7850) duplicate, [#11023](https://github.com/cgeo/cgeo/issues/11023) fixed, [#17093](https://github.com/cgeo/cgeo/issues/17093) fixed |
| [2026-11-25](../requests/cleanup/2026-11-25/report.md) | copilot | 20 | 0 | 0 | 0 | 0 | – |
| [2026-11-24 (5)](../requests/cleanup/2026-11-24/report-5.md) | copilot | 20 | 2 | 2 | 0 | 0 | [#13108](https://github.com/cgeo/cgeo/issues/13108) fixed, [#14931](https://github.com/cgeo/cgeo/issues/14931) duplicate, [#16516](https://github.com/cgeo/cgeo/issues/16516) duplicate, [#16731](https://github.com/cgeo/cgeo/issues/16731) fixed |
| [2026-11-24 (4)](../requests/cleanup/2026-11-24/report-4.md) | copilot | 20 | 0 | 1 | 0 | 1 | [#16187](https://github.com/cgeo/cgeo/issues/16187) duplicate, [#16362](https://github.com/cgeo/cgeo/issues/16362) waiting |
| [2026-11-24 (3)](../requests/cleanup/2026-11-24/report-3.md) | copilot | 20 | 0 | 3 | 0 | 0 | [#14329](https://github.com/cgeo/cgeo/issues/14329) duplicate, [#15924](https://github.com/cgeo/cgeo/issues/15924) duplicate, [#15388](https://github.com/cgeo/cgeo/issues/15388) duplicate |
| [2026-11-24 (2)](../requests/cleanup/2026-11-24/report-2.md) | copilot | 20 | 1 | 0 | 0 | 0 | [#11849](https://github.com/cgeo/cgeo/issues/11849) fixed |
| [2026-11-24](../requests/cleanup/2026-11-24/report.md) | copilot | 20 | 1 | 1 | 1 | 0 | [#11394](https://github.com/cgeo/cgeo/issues/11394) fixed, [#15313](https://github.com/cgeo/cgeo/issues/15313) duplicate, [#15358](https://github.com/cgeo/cgeo/issues/15358) obsolete |
| [2026-11-23 (5)](../requests/cleanup/2026-11-23/report-5.md) | copilot | 20 | 3 | 0 | 0 | 1 | [#15071](https://github.com/cgeo/cgeo/issues/15071) fixed, [#14989](https://github.com/cgeo/cgeo/issues/14989) fixed, [#14983](https://github.com/cgeo/cgeo/issues/14983) fixed, [#11927](https://github.com/cgeo/cgeo/issues/11927) waiting |
| [2026-11-23 (4)](../requests/cleanup/2026-11-23/report-4.md) | copilot | 20 | 2 | 0 | 0 | 0 | [#9340](https://github.com/cgeo/cgeo/issues/9340) fixed, [#14579](https://github.com/cgeo/cgeo/issues/14579) fixed |
| [2026-11-23 (3)](../requests/cleanup/2026-11-23/report-3.md) | copilot | 20 | 1 | 0 | 0 | 1 | [#11112](https://github.com/cgeo/cgeo/issues/11112) waiting, [#13781](https://github.com/cgeo/cgeo/issues/13781) fixed |
| [2026-11-23 (2)](../requests/cleanup/2026-11-23/report-2.md) | copilot | 20 | 2 | 1 | 0 | 0 | [#13640](https://github.com/cgeo/cgeo/issues/13640) fixed, [#14125](https://github.com/cgeo/cgeo/issues/14125) duplicate, [#14189](https://github.com/cgeo/cgeo/issues/14189) fixed |
| [2026-11-23](../requests/cleanup/2026-11-23/report.md) | copilot | 20 | 2 | 0 | 0 | 0 | [#13797](https://github.com/cgeo/cgeo/issues/13797) fixed, [#12503](https://github.com/cgeo/cgeo/issues/12503) fixed |
| [2026-11-22 (5)](../requests/cleanup/2026-11-22/report-5.md) | copilot | 20 | 2 | 0 | 1 | 0 | [#4549](https://github.com/cgeo/cgeo/issues/4549) fixed, [#2724](https://github.com/cgeo/cgeo/issues/2724) fixed, [#8144](https://github.com/cgeo/cgeo/issues/8144) obsolete |
| [2026-11-22 (4)](../requests/cleanup/2026-11-22/report-4.md) | copilot | 20 | 0 | 0 | 0 | 0 | – |
| [2026-11-22 (3)](../requests/cleanup/2026-11-22/report-3.md) | copilot | 20 | 1 | 0 | 0 | 0 | [#12886](https://github.com/cgeo/cgeo/issues/12886) fixed |
| [2026-11-22 (2)](../requests/cleanup/2026-11-22/report-2.md) | copilot | 20 | 0 | 1 | 0 | 0 | [#12459](https://github.com/cgeo/cgeo/issues/12459) duplicate |
| [2026-11-22](../requests/cleanup/2026-11-22/report.md) | copilot | 20 | 1 | 2 | 0 | 0 | [#12241](https://github.com/cgeo/cgeo/issues/12241) fixed, [#11440](https://github.com/cgeo/cgeo/issues/11440) duplicate, [#11722](https://github.com/cgeo/cgeo/issues/11722) duplicate |
| [2026-11-21 (5)](../requests/cleanup/2026-11-21/report-5.md) | copilot | 20 | 2 | 0 | 2 | 0 | [#10568](https://github.com/cgeo/cgeo/issues/10568) obsolete, [#10656](https://github.com/cgeo/cgeo/issues/10656) obsolete, [#1286](https://github.com/cgeo/cgeo/issues/1286) fixed, [#5206](https://github.com/cgeo/cgeo/issues/5206) fixed |
| [2026-11-21 (4)](../requests/cleanup/2026-11-21/report-4.md) | copilot | 20 | 3 | 0 | 0 | 0 | [#9855](https://github.com/cgeo/cgeo/issues/9855) fixed, [#10125](https://github.com/cgeo/cgeo/issues/10125) fixed, [#6809](https://github.com/cgeo/cgeo/issues/6809) fixed |
| [2026-11-21 (3)](../requests/cleanup/2026-11-21/report-3.md) | copilot | 20 | 0 | 0 | 2 | 0 | [#8614](https://github.com/cgeo/cgeo/issues/8614) obsolete, [#3798](https://github.com/cgeo/cgeo/issues/3798) obsolete |
| [2026-11-21 (2)](../requests/cleanup/2026-11-21/report-2.md) | copilot | 20 | 5 | 0 | 0 | 0 | [#7990](https://github.com/cgeo/cgeo/issues/7990) fixed, [#2808](https://github.com/cgeo/cgeo/issues/2808) fixed, [#8334](https://github.com/cgeo/cgeo/issues/8334) fixed, [#8351](https://github.com/cgeo/cgeo/issues/8351) fixed, [#6391](https://github.com/cgeo/cgeo/issues/6391) fixed |
| [2026-11-21](../requests/cleanup/2026-11-21/report.md) | copilot | 20 | 2 | 0 | 4 | 0 | [#1863](https://github.com/cgeo/cgeo/issues/1863) obsolete, [#4248](https://github.com/cgeo/cgeo/issues/4248) obsolete, [#6034](https://github.com/cgeo/cgeo/issues/6034) obsolete, [#7464](https://github.com/cgeo/cgeo/issues/7464) fixed, [#3509](https://github.com/cgeo/cgeo/issues/3509) fixed, [#4298](https://github.com/cgeo/cgeo/issues/4298) obsolete |
| [2026-11-20](../requests/cleanup/2026-11-20/report.md) | claude | 20 | 1 | 0 | 0 | 0 | [#6360](https://github.com/cgeo/cgeo/issues/6360) fixed |
| [2026-11-17](../requests/cleanup/2026-11-17/report.md) | copilot | 20 | 1 | 0 | 0 | 0 | [#6511](https://github.com/cgeo/cgeo/issues/6511) fixed |
| [2026-11-15-test](../requests/cleanup/2026-11-15-test/report.md) | copilot | 20 | 0 | 0 | 0 | 0 | – |
| [2026-11-15](../requests/cleanup/2026-11-15/report.md) | copilot | 20 | 1 | 0 | 0 | 0 | [#447](https://github.com/cgeo/cgeo/issues/447) fixed |
