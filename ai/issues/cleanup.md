# Issue cleanup

Written by the workflow after every cleanup run and issue snapshot; do not edit by hand. The
reports are in the request folders `ai/requests/cleanup/<name>/` (`report.md`, further batches
of the same night `report-2.md`, ...). The AI closes nothing: check each issue in its report
before closing it.

## Contents

- [Issues that can probably be closed](#issues-that-can-probably-be-closed)
  - [Probably fixed (46)](#probably-fixed-46)
  - [Duplicates (20)](#duplicates-20)
  - [No longer applicable (11)](#no-longer-applicable-11)
  - [Waiting for information (10)](#waiting-for-information-10)
- [Reports (41)](#reports-41)

## Issues that can probably be closed

Issues whose latest result of at least one provider says they can be closed, by category;
a later run of the same provider that keeps an issue open removes it here. The columns show
the latest result of each provider with a link to its report.

### Probably fixed (46)

| Issue | Title | Copilot | Claude |
|---|---|---|---|
| [#447](https://github.com/cgeo/cgeo/issues/447) | caches should be sorted relative to search centre, not phone coords | [fixed](../requests/cleanup/2026-11-15/report.md) | – |
| [#1286](https://github.com/cgeo/cgeo/issues/1286) | Support of eniro maps | [fixed](../requests/cleanup/2026-11-21/report-5.md) | – |
| [#2724](https://github.com/cgeo/cgeo/issues/2724) | GPX eport file naming | [fixed](../requests/cleanup/2026-11-22/report-5.md) | – |
| [#2808](https://github.com/cgeo/cgeo/issues/2808) | Nearby search not supporting "load more" for OC | [fixed](../requests/cleanup/2026-11-21/report-2.md) | – |
| [#3509](https://github.com/cgeo/cgeo/issues/3509) | Requests to disabled/unused connectors | [fixed](../requests/cleanup/2026-11-21/report.md) | – |
| [#4549](https://github.com/cgeo/cgeo/issues/4549) | Implement checker for challenge caches | [fixed](../requests/cleanup/2026-11-22/report-5.md) | – |
| [#5206](https://github.com/cgeo/cgeo/issues/5206) | GK: Search by tracking code | [fixed](../requests/cleanup/2026-11-21/report-5.md) | – |
| [#6360](https://github.com/cgeo/cgeo/issues/6360) | Mass uploading personal notes should not be in Export menu | – | [fixed](../requests/cleanup/2026-11-20/report.md) |
| [#6391](https://github.com/cgeo/cgeo/issues/6391) | Support Geocaching Australia API | [fixed](../requests/cleanup/2026-11-21/report-2.md) | – |
| [#6511](https://github.com/cgeo/cgeo/issues/6511) | Add filter for gc friend that has found caches in your list | [fixed](../requests/cleanup/2026-11-17/report.md) | – |
| [#6809](https://github.com/cgeo/cgeo/issues/6809) | Detect if OC-site is capable of log picture upload | [fixed](../requests/cleanup/2026-11-21/report-4.md) | – |
| [#7464](https://github.com/cgeo/cgeo/issues/7464) | Make export functions cancellable | [fixed](../requests/cleanup/2026-11-21/report.md) | – |
| [#7990](https://github.com/cgeo/cgeo/issues/7990) | No way out if user permanently declined permission | [fixed](../requests/cleanup/2026-11-21/report-2.md) | – |
| [#8334](https://github.com/cgeo/cgeo/issues/8334) | Retracted cache listing not recognized | [fixed](../requests/cleanup/2026-11-21/report-2.md) | – |
| [#8351](https://github.com/cgeo/cgeo/issues/8351) | Update AVD on CI | [fixed](../requests/cleanup/2026-11-21/report-2.md) | – |
| [#9340](https://github.com/cgeo/cgeo/issues/9340) | Toast for "There may be more caches in this area" | [fixed](../requests/cleanup/2026-11-23/report-4.md) | – |
| [#9398](https://github.com/cgeo/cgeo/issues/9398) | Average WP coords | [fixed](../requests/cleanup/2026-11-27/report-2.md) | – |
| [#9855](https://github.com/cgeo/cgeo/issues/9855) | Central declaration of repositories | [fixed](../requests/cleanup/2026-11-21/report-4.md) | – |
| [#10125](https://github.com/cgeo/cgeo/issues/10125) | Do not unconditionally store cache locally upon entering waypoint edit mode | [fixed](../requests/cleanup/2026-11-21/report-4.md) | – |
| [#11023](https://github.com/cgeo/cgeo/issues/11023) | CI/Jenkins: make logcat output accessible for Test runs | [fixed](../requests/cleanup/2026-11-25/report-2.md) | – |
| [#11394](https://github.com/cgeo/cgeo/issues/11394) | Provide error message returned by connector to user | [fixed](../requests/cleanup/2026-11-24/report.md) | – |
| [#11849](https://github.com/cgeo/cgeo/issues/11849) | Avoid confirm dialog when waypoint is unchanged | [fixed](../requests/cleanup/2026-11-24/report-2.md) | – |
| [#12077](https://github.com/cgeo/cgeo/issues/12077) | Have some options when trying to save search results to a list | [fixed](../requests/cleanup/2026-11-25/report-4.md) | – |
| [#12241](https://github.com/cgeo/cgeo/issues/12241) | Calculated Waypoints refactoring: replace side-scrolling multi-column variable dialog with single l… | [fixed](../requests/cleanup/2026-11-22/report.md) | – |
| [#12503](https://github.com/cgeo/cgeo/issues/12503) | Explicit white background in cache description not readable in dark mode | [fixed](../requests/cleanup/2026-11-23/report.md) | – |
| [#12886](https://github.com/cgeo/cgeo/issues/12886) | Map filter for events: Displays events for wrong day | [fixed](../requests/cleanup/2026-11-22/report-3.md) | – |
| [#13108](https://github.com/cgeo/cgeo/issues/13108) | Share cache together with corrected coordinates | [fixed](../requests/cleanup/2026-11-24/report-5.md) | – |
| [#13640](https://github.com/cgeo/cgeo/issues/13640) | Lint: CustomSplashScreen | [fixed](../requests/cleanup/2026-11-23/report-2.md) | – |
| [#13781](https://github.com/cgeo/cgeo/issues/13781) | Failure to show error toast | [fixed](../requests/cleanup/2026-11-23/report-3.md) | – |
| [#13797](https://github.com/cgeo/cgeo/issues/13797) | ALC change of linear/random mode not detected | [fixed](../requests/cleanup/2026-11-23/report.md) | – |
| [#14189](https://github.com/cgeo/cgeo/issues/14189) | NullPointerException on long tap on geocache waypoint | [fixed](../requests/cleanup/2026-11-23/report-2.md) | – |
| [#14579](https://github.com/cgeo/cgeo/issues/14579) | Filter for missing T/D in 81er Matrix | [fixed](../requests/cleanup/2026-11-23/report-4.md) | – |
| [#14983](https://github.com/cgeo/cgeo/issues/14983) | Move batch uploading notes/coords to background with proper notification | [fixed](../requests/cleanup/2026-11-23/report-5.md) | – |
| [#14989](https://github.com/cgeo/cgeo/issues/14989) | No notification dot shown when directly launching into map | [fixed](../requests/cleanup/2026-11-23/report-5.md) | – |
| [#15071](https://github.com/cgeo/cgeo/issues/15071) | Hyperlink in personal note is not parsed correctly | [fixed](../requests/cleanup/2026-11-23/report-5.md) | – |
| [#16731](https://github.com/cgeo/cgeo/issues/16731) | OOM in detecting file type | [fixed](../requests/cleanup/2026-11-24/report-5.md) | – |
| [#16751](https://github.com/cgeo/cgeo/issues/16751) | Android 16 / targetSDK 36 | [keep-open](../requests/cleanup/2026-11-27/report.md) | [fixed](../requests/cleanup/2026-11-27-claude/report.md) |
| [#17041](https://github.com/cgeo/cgeo/issues/17041) | Beta version: IllegalStateException / missing context in DescriptionViewCreator | [fixed](../requests/cleanup/2026-11-25/report-3.md) | – |
| [#17093](https://github.com/cgeo/cgeo/issues/17093) | RuntimeException in WherigoGameService.onCreate | [fixed](../requests/cleanup/2026-11-25/report-2.md) | – |
| [#17105](https://github.com/cgeo/cgeo/issues/17105) | Ordered HTML list not displayed as such | [fixed](../requests/cleanup/2026-11-27/report.md) | [keep-open](../requests/cleanup/2026-11-27-claude/report.md) |
| [#17375](https://github.com/cgeo/cgeo/issues/17375) | Upgrade to SDK35: Edge-to-Edge | [fixed](../requests/cleanup/2026-11-25/report-4.md) | – |
| [#17485](https://github.com/cgeo/cgeo/issues/17485) | NPE in PersistableFolder.registerForIndirectChange | [fixed](../requests/cleanup/2026-11-25/report-5.md) | – |
| [#17488](https://github.com/cgeo/cgeo/issues/17488) | Many ANR happening on c:geo startup | [keep-open](../requests/cleanup/2026-11-26/report.md) | [fixed](../requests/cleanup/2026-11-26-claude/report.md) |
| [#17738](https://github.com/cgeo/cgeo/issues/17738) | Add "New in version" (What's New) info to F-Droid releases | [keep-open](../requests/cleanup/2026-11-27/report-2.md) | [fixed](../requests/cleanup/2026-11-27-claude/report.md) |
| [#17995](https://github.com/cgeo/cgeo/issues/17995) | \[Wherigo / SAF\] Downloading cartridge creates duplicate "wherigo (n)" folders instead of using exis… | [fixed](../requests/cleanup/2026-11-27/report-2.md) | – |
| [#18058](https://github.com/cgeo/cgeo/issues/18058) | Add a "cache placement" view to the map | [fixed](../requests/cleanup/2026-11-27/report.md) | [keep-open](../requests/cleanup/2026-11-27-claude/report.md) |

### Duplicates (20)

| Issue | Title | Copilot | Claude |
|---|---|---|---|
| [#7850](https://github.com/cgeo/cgeo/issues/7850) | Upload button for personal note missing | [duplicate](../requests/cleanup/2026-11-25/report-2.md) | – |
| [#11440](https://github.com/cgeo/cgeo/issues/11440) | Cleanup our DB | [duplicate](../requests/cleanup/2026-11-22/report.md) | – |
| [#11722](https://github.com/cgeo/cgeo/issues/11722) | Import GPX routes/trackes via click on file | [duplicate](../requests/cleanup/2026-11-22/report.md) | – |
| [#12459](https://github.com/cgeo/cgeo/issues/12459) | Heat Live map: Colors icon by Favorites | [duplicate](../requests/cleanup/2026-11-22/report-2.md) | – |
| [#14125](https://github.com/cgeo/cgeo/issues/14125) | Is it possible to keep the logged in session locally for a short time? | [duplicate](../requests/cleanup/2026-11-23/report-2.md) | – |
| [#14329](https://github.com/cgeo/cgeo/issues/14329) | Support importing GPX tracks/routes from external | [duplicate](../requests/cleanup/2026-11-24/report-3.md) | – |
| [#14909](https://github.com/cgeo/cgeo/issues/14909) | support field note upload for opencaching.de | [duplicate](../requests/cleanup/2026-11-27/report-4.md) | – |
| [#14931](https://github.com/cgeo/cgeo/issues/14931) | update only cache state | [duplicate](../requests/cleanup/2026-11-24/report-5.md) | – |
| [#15313](https://github.com/cgeo/cgeo/issues/15313) | wording of link to images (minor) | [duplicate](../requests/cleanup/2026-11-24/report.md) | – |
| [#15388](https://github.com/cgeo/cgeo/issues/15388) | Geokrety - support rate limiting system | [duplicate](../requests/cleanup/2026-11-24/report-3.md) | – |
| [#15879](https://github.com/cgeo/cgeo/issues/15879) | Allow placeholders in default caption for log images | [duplicate](../requests/cleanup/2026-11-26/report-2.md) | – |
| [#15924](https://github.com/cgeo/cgeo/issues/15924) | possibility to add waypoint for projection/offset | [duplicate](../requests/cleanup/2026-11-24/report-3.md) | – |
| [#16187](https://github.com/cgeo/cgeo/issues/16187) | Share Intent Receiver: track.gpx | [duplicate](../requests/cleanup/2026-11-24/report-4.md) | – |
| [#16516](https://github.com/cgeo/cgeo/issues/16516) | GC.com: load images from "Image Gallery" | [duplicate](../requests/cleanup/2026-11-24/report-5.md) | – |
| [#17215](https://github.com/cgeo/cgeo/issues/17215) | IllegalArgumentException and OutOfMemoryError in AbstractActivity.onStart | [duplicate](../requests/cleanup/2026-11-26/report-3.md) | – |
| [#17242](https://github.com/cgeo/cgeo/issues/17242) | Support \[NAME\] and other placeholders in default image caption setting | [duplicate](../requests/cleanup/2026-11-26/report-2.md) | – |
| [#17423](https://github.com/cgeo/cgeo/issues/17423) | Improve UI for loading tracks versus routes | [duplicate](../requests/cleanup/2026-11-25/report-5.md) | – |
| [#17541](https://github.com/cgeo/cgeo/issues/17541) | Audio and video calls using \`c:geo\` or \`c:geo GPX import\` apps | [duplicate](../requests/cleanup/2026-11-26/report.md) | [keep-open](../requests/cleanup/2026-11-26-claude/report.md) |
| [#17744](https://github.com/cgeo/cgeo/issues/17744) | Map shows all caches when no cache types are selected in filters | [duplicate](../requests/cleanup/2026-11-26/report.md) | [duplicate](../requests/cleanup/2026-11-26-claude/report.md) |
| [#17747](https://github.com/cgeo/cgeo/issues/17747) | Feature Request: Improve “Special” Cache Types in Filters | [duplicate](../requests/cleanup/2026-11-26/report.md) | [keep-open](../requests/cleanup/2026-11-26-claude/report.md) |

### No longer applicable (11)

| Issue | Title | Copilot | Claude |
|---|---|---|---|
| [#1863](https://github.com/cgeo/cgeo/issues/1863) | GCVote loading after gpx import | [obsolete](../requests/cleanup/2026-11-21/report.md) | – |
| [#3798](https://github.com/cgeo/cgeo/issues/3798) | Avoid database lookups for map JSON caches | [obsolete](../requests/cleanup/2026-11-21/report-3.md) | – |
| [#4248](https://github.com/cgeo/cgeo/issues/4248) | GCVote shown as "Active" although no password given | [obsolete](../requests/cleanup/2026-11-21/report.md) | – |
| [#4298](https://github.com/cgeo/cgeo/issues/4298) | Feature Request: Transmit .gpx file instead of URL via NFC | [obsolete](../requests/cleanup/2026-11-21/report.md) | – |
| [#6034](https://github.com/cgeo/cgeo/issues/6034) | Always show voting in log activity | [obsolete](../requests/cleanup/2026-11-21/report.md) | – |
| [#8144](https://github.com/cgeo/cgeo/issues/8144) | Map tiles get repainted each time screen is turned on | [obsolete](../requests/cleanup/2026-11-22/report-5.md) | – |
| [#8614](https://github.com/cgeo/cgeo/issues/8614) | Final flag lost on live map after opening popup | [obsolete](../requests/cleanup/2026-11-21/report-3.md) | – |
| [#10568](https://github.com/cgeo/cgeo/issues/10568) | Filtering for ALC fails after "Load more" in search results | [obsolete](../requests/cleanup/2026-11-21/report-5.md) | – |
| [#10656](https://github.com/cgeo/cgeo/issues/10656) | catch IllegalArgumentException for EC active without login information | [obsolete](../requests/cleanup/2026-11-21/report-5.md) | – |
| [#15358](https://github.com/cgeo/cgeo/issues/15358) | ToolbarWidgetWrapper: Progress display unsupported | [obsolete](../requests/cleanup/2026-11-24/report.md) | – |
| [#18129](https://github.com/cgeo/cgeo/issues/18129) | GH Workflow check-secrets - deprecation warning | [obsolete](../requests/cleanup/2026-11-26/report-4.md) | – |

### Waiting for information (10)

| Issue | Title | Copilot | Claude |
|---|---|---|---|
| [#10837](https://github.com/cgeo/cgeo/issues/10837) | Individual track and OC waypoints | [waiting](../requests/cleanup/2026-11-25/report-2.md) | – |
| [#11112](https://github.com/cgeo/cgeo/issues/11112) | "Search by XYZ" should have a progress spinner while loading caches | [waiting](../requests/cleanup/2026-11-23/report-3.md) | – |
| [#11927](https://github.com/cgeo/cgeo/issues/11927) | \[Nightly\] App Crash when leaving or rotating Live Map while it's still rendering | [waiting](../requests/cleanup/2026-11-23/report-5.md) | – |
| [#16191](https://github.com/cgeo/cgeo/issues/16191) | found status of ALC is not automatically set | [waiting](../requests/cleanup/2026-11-25/report-2.md) | – |
| [#16362](https://github.com/cgeo/cgeo/issues/16362) | Lines between tiles on Unified MF | [waiting](../requests/cleanup/2026-11-24/report-4.md) | – |
| [#16744](https://github.com/cgeo/cgeo/issues/16744) | No proximity alert for Final? | [waiting](../requests/cleanup/2026-11-26/report.md) | [waiting](../requests/cleanup/2026-11-26-claude/report.md) |
| [#16977](https://github.com/cgeo/cgeo/issues/16977) | Tests -\> request was not successful: message=Forbidden | [waiting](../requests/cleanup/2026-11-25/report-2.md) | – |
| [#17568](https://github.com/cgeo/cgeo/issues/17568) | \[Nightly\] Long distance routing behaves erratic | [waiting](../requests/cleanup/2026-11-25/report-5.md) | – |
| [#17737](https://github.com/cgeo/cgeo/issues/17737) | Problems with activity stack | [waiting](../requests/cleanup/2026-11-26/report.md) | [keep-open](../requests/cleanup/2026-11-26-claude/report.md) |
| [#17739](https://github.com/cgeo/cgeo/issues/17739) | Unexpected result when sorting a search result | [waiting](../requests/cleanup/2026-11-26/report-2.md) | [waiting](../requests/cleanup/2026-11-26-claude/report.md) |

## Reports (41)

| Report | Provider | Checked | Fixed | Duplicates | Obsolete | Waiting | Can probably be closed |
|---|---|---|---|---|---|---|---|
| [2026-11-27-claude](../requests/cleanup/2026-11-27-claude/report.md) | claude | 30 | 2 | 0 | 0 | 0 | [#16751](https://github.com/cgeo/cgeo/issues/16751) fixed, [#17738](https://github.com/cgeo/cgeo/issues/17738) fixed |
| [2026-11-27 (5)](../requests/cleanup/2026-11-27/report-5.md) | copilot | 20 | 0 | 0 | 0 | 0 | – |
| [2026-11-27 (4)](../requests/cleanup/2026-11-27/report-4.md) | copilot | 20 | 0 | 1 | 0 | 0 | [#14909](https://github.com/cgeo/cgeo/issues/14909) duplicate |
| [2026-11-27 (3)](../requests/cleanup/2026-11-27/report-3.md) | copilot | 20 | 0 | 0 | 0 | 0 | – |
| [2026-11-27 (2)](../requests/cleanup/2026-11-27/report-2.md) | copilot | 20 | 2 | 0 | 0 | 0 | [#17995](https://github.com/cgeo/cgeo/issues/17995) fixed, [#9398](https://github.com/cgeo/cgeo/issues/9398) fixed |
| [2026-11-27](../requests/cleanup/2026-11-27/report.md) | copilot | 20 | 2 | 0 | 0 | 0 | [#18058](https://github.com/cgeo/cgeo/issues/18058) fixed, [#17105](https://github.com/cgeo/cgeo/issues/17105) fixed |
| [2026-11-26-claude](../requests/cleanup/2026-11-26-claude/report.md) | claude | 30 | 1 | 1 | 0 | 2 | [#16744](https://github.com/cgeo/cgeo/issues/16744) waiting, [#17488](https://github.com/cgeo/cgeo/issues/17488) fixed, [#17744](https://github.com/cgeo/cgeo/issues/17744) duplicate, [#17739](https://github.com/cgeo/cgeo/issues/17739) waiting |
| [2026-11-26 (5)](../requests/cleanup/2026-11-26/report-5.md) | copilot | – | – | – | – | – | no result block |
| [2026-11-26 (4)](../requests/cleanup/2026-11-26/report-4.md) | copilot | 20 | 0 | 0 | 1 | 0 | [#18129](https://github.com/cgeo/cgeo/issues/18129) obsolete |
| [2026-11-26 (3)](../requests/cleanup/2026-11-26/report-3.md) | copilot | 20 | 0 | 1 | 0 | 0 | [#17215](https://github.com/cgeo/cgeo/issues/17215) duplicate |
| [2026-11-26 (2)](../requests/cleanup/2026-11-26/report-2.md) | copilot | 20 | 0 | 2 | 0 | 1 | [#17739](https://github.com/cgeo/cgeo/issues/17739) waiting, [#15879](https://github.com/cgeo/cgeo/issues/15879) duplicate, [#17242](https://github.com/cgeo/cgeo/issues/17242) duplicate |
| [2026-11-26](../requests/cleanup/2026-11-26/report.md) | copilot | 20 | 0 | 3 | 0 | 2 | [#16744](https://github.com/cgeo/cgeo/issues/16744) waiting, [#17541](https://github.com/cgeo/cgeo/issues/17541) duplicate, [#17744](https://github.com/cgeo/cgeo/issues/17744) duplicate, [#17747](https://github.com/cgeo/cgeo/issues/17747) duplicate, [#17737](https://github.com/cgeo/cgeo/issues/17737) waiting |
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
