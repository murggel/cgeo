(Nattliga endast: Tar tillfälligt bort "nattlig" banner från logotypen medan finjustering av designen pågår)

### UnifiedMap roadmap & "old" maps deprecation notice
c:geo has an all-new map implementation called "UnifiedMap" since some time, which will ultimately replace the old implementations of Google Maps and Mapsforge (OpenStreetMap). This is a deprecation notice to inform you about the further roadmap.

UnifiedMap got published about a year ago. It still supports Google Maps and OpenStreetMap (online + offline), but in a completely reworked technical way, and with a lot of exciting new features that the "old" maps do not support, some of which are
- Map rotation for OpenStreetMap based maps (online + offline)
- Cluster popup for Google Maps
- Hide map sources you don't need
- Elevation chart for routes and tracks
- Switch between lists directly from map
- "Driving mode" for OpenStreetMap based maps

UnfiedMap has proven to be stable since quite some time, thus we will remove the old map implementations to reduce the efforts for maintaining c:geo.

Roadmap:
- "Old" maps are in deprecation mode now - we won't fix bugs for it anymore.
- UnifiedMap will be made default for all users in fall of 2025.
- "Old" map implementations will be removed in spring 2026.

Until then, you can switch between the different implementations in settings => map sources.

### Karta
- New: Show geofences for lab stages (UnifiedMap) - enable "Circles" in map quick settings to show them
- New: Option to set circles with individual radius to waypoints ("geofence" context menu option)
- Fix: Map view not updated when removing cache from currently shown list
- Fix: Number of cache in list chooser not updated on changing list contents
- Change: Keep current viewport on mapping a list, if all caches fit into current viewport
- New: Follow my location in elevation chart (UnifiedMap)
- New: Enable "move to" / "copy to" actions for "show as list"
- New: Support Elevate Winter theme in map downloader
- New: Adaptive hillshading, optional high quality mode (UnifiedMap Mapsforge)
- New: Redesigned routes/tracks quick settings dialog
- New: Long tap on map selection icon to select previous tile provider (UnifiedMap)
- New: Allow setting display name for offline maps in companion file (UnifiedMap)
- New: Long tap on "enable live button" to load offline caches
- New: Offline hillshading for UnifiedMap (VTM variant)
- New: Support for background maps (UnifiedMap)
- Fix: Compact icons not returning to large icons on zooming in in auto mode (UnifiedMap)
- Nytt: Åtgärder för långtryck på cache-infosida: GC-kod, cachetitel, koordinater, personlig anteckning/ledtråd
- Ändring: Byter cache infosida långtryck för emoji-väljare till kort tryck för att lösa kollisionen

### Cachedetaljer
- Nyhet: Offline-översättning av notering, text och loggar (experimentell)
- Nyhet: Alternativ för att dela cache med användardata (koordinater, personlig anteckning)
- Fix: Talservice avbryts vid skärmrotation
- Fix: Cache details: Lists for cache not updated after tapping on list name an removing that cache from that list
- Fix: Användaranteckning tappas när du laddar upp ett lab adventure
- Ändra: Loggdatum-relaterade platshållare kommer att använda valt datum istället för aktuellt datum
- New: Collapse long log entries per default

### Wherigo player
- Nytt: Integrerad Wherigo-spelarkontroll kontrollerar saknade inloggningsuppgifter
- Change: Removed Wherigo bug report (as errors are mostly cartridge-related, need to be fixed by cartridge owner)
- New: Ability to navigate to a zone using compass
- New: Ability to copy zone center coordinates to clipboard
- New: Set zone center as target when opening map (to get routing and distance info for it)
- Nyhet: Stöd för att öppna lokala Wherigo-filer
- Change: Long-tap on a zone on map is no longer recognized. This allows users to do other stuff in map zone area available on long-tap, eg: create user-defined cache
- New: Display warning if wherigo.com reports missing EULA (which leads to failing download of cartridge)

### Allmänt
- New: Redesigned search page
- Nytt: Filter för antal i inventariet
- Nytt: Stöd för koordinater i DD,DDDDDDD-format
- Nytt: Visa senast använda filternamn i filterdialogen
- Nytt: Koordinatkalkylator: Funktion för att ersätta "x" med multiplikationssymbol
- Fix: Felaktig höjd (använder inte höjd över havsmedelnivån)
- Fix: Avståndsgränsen i närheten fungerar inte korrekt för små värden
- Fix: Sorting of cache lists by distance descending not working correctly
- Fix: Lab-cacher exkluderade av D/T-filter även med aktiva "inkludera osäkerhet"
- Fix: Färg-problem med menyikoner i ljust läge
- Nyhet: Lägg till "Ta bort tidigare händelser" för att lista "alla"
- Nyhet: Visa koppling för "användardefinierade cacher" som aktiv i källfiltret
- New: GPX export: exporting logs / trackables made optional
- New: Added button to delete log templates
- Fix: Import av lokal kartfil får slumpmässigt kartnamn
- Fix: Map downloader offering broken (0 bytes) files for download
- Nytt: Lade till mappningar för vissa saknade OC-cache-typer
- Nytt: Flytta "nyligen använda"-listorna i dialogrutan för val av lista till toppen när du trycker på "nyligen använda"-knappen
- Nyhet: Dela en lista med geocoder från cachelistan
