<!-- task: review-pr | upstream: cgeo/cgeo@2dc6a7075c980380907f6cb8d14232bfb80ea929 | PR: #18890 | PR head: e3113d43fc87cc12b3989b95491371ef2252bdec | instructions: yes | provider: claude | workflow: 844b60c9b6ef2a8994d97f0a15fc6825185fb756 -->

1. **Base branch**: `release` (at 239e17d). `upstream/` was not needed. I could not check the real GPS Status 11.x or 12.x manifests, so claims about their intent filters rest on the PR description.

2. **Findings**

**Medium: radar visibility is no longer tied to GPS Status, so other apps can trigger the "Radar" entry.**
- Location: `main/src/main/java/cgeo/geocaching/apps/navi/AbstractRadarApp.java:37-39`, which also applies to `PebbleApp`.
- Before the change, `isInstalled()` checked that the specific package (`com.eclipsim.gpsstatus2`) was launchable. Now `RadarApp.isInstalled()` falls back to `ProcessUtils.isIntentAvailable("com.google.android.radar.SHOW_RADAR")` with no package restriction.
- The legacy action is a generic, historically shared "Google radar" action. Any other app that registers it will now make "Radar" appear.
- On the legacy path, `createIntent` also sends an unrestricted implicit intent. This can open a chooser or a different app than GPS Status.
- Impact for older versions: GPS Status ≤11 still works, because the app is declared in `<queries>` and so is visible.
- The same unrestricted check now applies to `PebbleApp`. This is a small behavior change for a feature the PR doesn't mention.
- Suggested fix: restrict the legacy check to the package. For example, call `intent.setPackage(PACKAGE_NAME)` and use `ProcessUtils.isActivityAvailable`. Also call `setPackage` in `createIntent`. Pebble could use the same pattern, or keep the old package check combined with the new check.

**Low: older versions that match neither path lose the Radar entry.**
- `RadarApp.isInstalled()` is now `isRadarLinkSupported() || super.isInstalled()`.
- If a 12.x build, or a 11.x build with an unusual filter, has no `SHOW_RADAR` filter with `CATEGORY_DEFAULT` and no mobiwia link filter, the entry silently disappears.
- `queryIntentActivities` with `MATCH_DEFAULT_ONLY` mirrors what `startActivity` needs, so this is correct for working builds. Please confirm on an actual 11.x install, because the PR only says it was tested.

**Low: no tests were added.**
- The link building has several edge cases: names with `&`, `,`, `#`, `%`, non-ASCII characters, or only parentheses.
- `Uri.encode` and the bracket replacement look sound. I found no defect, and the coordinate format is locale-independent (`%.6f` with a null `Locale`).

**Backward-compatibility assessment for GPS Status 12.x and ≤11.x:**
- On 12.x, `isRadarLinkSupported()` is true, so the deep link is used. It is restricted to the GPS Status package, which is already listed in `<queries>`.
- On ≤11.x, the deep link intent doesn't resolve. The code falls back to the legacy intent with the extras unchanged, as float lat/lon.
- `ActivityNotFoundException` is now caught for all radar apps, which is a robustness gain.
- The manifest needs no change. The package is already in `<queries>`, and the existing broad `https` BROWSABLE `<intent>` entry is not needed because the intent is package-restricted.
- Only the unrestricted legacy-action check above is a risk, and it affects other apps rather than GPS Status itself.

3. **Behavior changes**

**Intended and documented**
- On GPS Status 12, radar uses the `https://mobiwia.com/radar?q=lat,lon(name)` deep link.
- The "Radar" entry is hidden when GPS Status can't handle either path.
- The cache or waypoint name is passed, with parentheses replaced by brackets. Plain coordinates have no name.
- A toast is shown instead of a crash when no activity is found.
- `ProcessUtils.isActivityAvailable` is new.

**Intended but undocumented**
- The `isInstalled()` change in `AbstractRadarApp` also affects `PebbleApp`. Please add this to the description.
- The description doesn't say that `Log.w` and the `err_application_no` toast now apply to Pebble too.
- This goes beyond a targeted fix for a release branch. The refactoring is small but touches shared code. The `createIntent` signature change is internal and low risk.

**Unintended or side effect**
- The unrestricted `SHOW_RADAR` check means third-party apps can make "Radar" appear. It can also send the legacy intent to a non-GPS-Status app (see Findings).

I found no reliance on master-only code.
