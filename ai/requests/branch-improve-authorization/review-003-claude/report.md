<!-- task: review-branch | upstream: cgeo/cgeo@0edab2d977d2f9631cbef5d52f54e4f7abdefc13 | branch: murggel/cgeo:feature/improve-authorization@341fccd401d5b33589be9180c8f5271810c99b3a | base: master@2dc6a7075c980380907f6cb8d14232bfb80ea929 | issue snapshot: 2026-11-15 | preselected: 5 | instructions: yes | previous: review-002-claude | provider: claude | workflow: 959fc66474e3d6cac0677b47e3e3ddb09314db52 -->

**Status:** The branch head is still `341fccd`, the head the previous report was based on. I didn't build or run anything. Everything below comes from reading `branch-head/`, and I did not re-check translations beyond a count. I'm not repeating the unchanged details of the previous report.

## Status of the previous report

| # | Previous finding | Status | Reason |
|---|---|---|---|
| 1 | Stale login state and user name after revoke, then re-authorize | **Partly wrong, still open for OC/SU** | GC is not affected. `GCAuthorizationActivity.checkCredentials` (lines 27-41) calls `logout()` when the stored credentials are invalid, which is the case after a revoke, and then `login()`. OC and SU are still affected (D1). |
| 2 | Fragile `ocSite` extra, crash on a missing or invalid value | **Still open, low** | `PreferenceServiceOpencachingFragment.getSite()` still throws. `onPreferenceStartFragment` (`SettingsActivity.java:361-365`) still just forwards `pref.getExtras()`. |
| 3 | Translations out of sync | **Still open, low** | 32 locale files still contain `auth_unconnected` or `auth_explain_long`. I did not check which locale has which. The default `strings.xml` no longer defines `auth_unconnected`, so lint `ExtraTranslation` is likely. |
| 4 | SU secret key id fix at `OAuthPreference.java:33` is undocumented | **Still open** | It is a correct fix, but the PR description must mention it. |
| 5 | Offline handling: no defect | **Holds** | See the flow table below. |

## 1. Base and scope

- **Base:** `cgeo/cgeo:master`, merge base `2dc6a70`.
- **Size:** 10 commits and 28 changed files.
- **Base-side changes:** the context file says the base has 31 commits since the merge base. The previous report said none. I did not compare them against `upstream/`, so I can't confirm conflicts.

## 2. Findings: defects still open in the authorization area

### D1. OC and SU keep the old account's login state after revoke and re-authorize (medium)

- **Where:**
  - `OCApiLiveConnector.java:48,149-157,184-197` and `SuConnector.java:59,99-111,128-141`.
  - `OAuthAuthorizationActivity` has no login call.
  - `AbstractAuthorizationPreference.updateAuthorizationInfo` (new, lines 443-455) shows `getUserName()`.
  - `OAuthPreference.java:112-120` reads that name from the connector's cached `userInfo`.
- **Scenario:**
  1. The user is logged in to OC.de or SU as account A.
  2. They long-tap, revoke, and authorize as account B without restarting the app.
  3. The new guards (`supportsPersonalization()`) pass again, because tokens exist.
  4. `userInfo` still says `SUCCESSFUL` with A's name.
- **Impact:**
  - Settings show "Connected as A" and the main screen shows "logged in".
  - A's name and find count are used until the next `login()`, for example for owner checks (`SuConnector.java:178`).
  - After a restart the state is correct, because `userInfo` is in memory only.
  - The commit "Show correct login status after the authorization has been revoked" fixes only the revoke direction.
- **Solutions:**
  - **(a)** Clear the cached state in the connector, for example a `resetLoginStatus()` that sets `userInfo` to `NOT_RETRIEVED`. Call it from `OAuthPreference.revokeAuthorization`.
    - Pro: small and local.
    - Con: it adds a method to the connector API, and the status stays "not retrieved" until the next login.
  - **(b)** Trigger `login()` on a background thread after a successful authorization, in `OAuthAuthorizationActivity` or on return to the settings.
    - Pro: this also fills in the user name right after the first authorization.
    - Con: it needs thread and offline handling, and it is a larger change.
  - **(c)** Do both.
- **Recommendation:** (c). Fix it in this branch, because the branch claims correct status after revoke. (a) is small; (b) can be a follow-up if the branch should stay small.

### D2. GeoKrety counts as registered after a long-tap revoke (medium, pre-existing, but it is the revoke flow of this branch)

- **Where:**
  - `TokenPreference.java:75-77` revokes by writing `""`.
  - `Settings.java:1080-1081`: `isRegisteredForGeokretyLogging()` returns `getGeokretySecId() != null`.
  - `GeokretyConnector.java:346-347`: `isRegistered()` uses that function.
- **Scenario:** The user revokes GeoKrety. The preference shows "Not connected" (`isAuthorized` uses `isNotEmpty`), but `isRegistered()` is still true. GeoKrety logging stays offered and runs with an empty secid.
- **Impact:** The UI is inconsistent after the revoke, and the user can try logging with an empty secid.
- **Solutions:**
  - **(a)** Make `isRegisteredForGeokretyLogging()` return `hasGeokretyAuthorization()`. It is one line, and `hasGeokretyAuthorization()` already uses `isNotBlank`.
  - **(b)** Revoke by writing `null`. That removes the key, but the other callers of `setTokenSecret` still behave differently.
- **Recommendation:** (a). It is tiny and belongs in this branch. I did not check whether the old state was reachable another way. This does not cause a crash.

### D3. Missing or invalid `ocSite` extra crashes the OC settings screen (low, partly fixed)

- **Where:** `PreferenceServiceOpencachingFragment.java` (`getSite`, `onCreatePreferences`, `onResume`) and the `<extra>` entries in `preferences_services.xml`.
- **Scenario:** A future OC entry has no matching extra or a typo. It crashes when the screen opens (`IllegalStateException`, or `IllegalArgumentException` from `valueOf`).
- **Solutions:**
  - **(a)** In `onPreferenceStartFragment`, derive the site from the clicked preference key and build the arguments there. Remove the XML extras.
    - Pro: one source of truth.
    - Con: code is needed in `SettingsActivity`.
  - **(b)** Keep the extras and have `getSite()` fall back to a safe default or finish the screen.
    - Pro: avoids the crash.
    - Con: it hides the mistake.
- **Recommendation:** (a), in this branch, since it is the branch's own design.

### D4. `isAuthorized` uses different rules for Geokrety (low)

- **Where:** `TokenPreference.java:70-71` uses `isNotEmpty`, while `Settings.hasGeokretyAuthorization()` uses `isNotBlank`.
- **Scenario:** A blank-only secret counts as authorized in settings but not elsewhere.
- **Fix:** Use `Settings.hasGeokretyAuthorization()` in `TokenPreference`, together with D2.

### D5. Translations (low)

- **Where:** default and translated `strings.xml`.
- **Impact:**
  - Translated `auth_explain_long` and `auth_token_explain_long` still hard-code the old button name.
  - `auth_connected` text changed, but translations still read "Connected".
  - Orphan `auth_unconnected` entries are likely to trigger lint.
- **Fix:** Remove or mark the stale translations, as is usual in this project. Do it in this branch if CI lint fails; otherwise as a separate change.

### Flow check (GC, OC/SU, GeoKrety)

| Flow | GC | OC / SU | GeoKrety |
|---|---|---|---|
| Authorize | OK | OK, but the name stays blank until a login ("Connected." text) | OK |
| Re-authorize with another account | OK, login is forced | **D1** | OK |
| Long-tap revoke | OK, cookies and avatar cleared | OK, SU now clears the secret too | **D2** |
| App restart | OK | OK, cache is rebuilt | OK |
| No internet | Settings use local data only. The main screen still guards the GC error line with `Network.isConnected()`. | Offline login gives `FAILED`; settings still show "Connected" (correct, local data) | No network use |
| Main screen versus settings | Consistent | Main screen may lag behind settings until the next login (D1) | Main screen n/a |
| OC screens from the list | OK, via XML extra | OK | n/a |
| OC screens from search or deep link | OK, via `getByPrefScreenKey` and `newInstance` | OK | n/a |

I found no crash path for the deep-link and search routes. A restored fragment keeps its arguments.

## 3. Behavior changes

The previous report's grouping is unchanged and I confirm it. Items that are not yet in the commit messages and should go into the PR description:
- The SU revoke clears the secret key.
- The GC settings show the raw stored username.
- OC and SU login status now depends on stored tokens.
- The `auth_unconnected` string was removed.
- The `RegisterSend2CgeoPreference` change: it no longer has a long-tap action.

D1 and D2 are the unintended side effects; they are covered under Findings.

## 4. Issues fixed by the branch

No issue is referenced in the commit messages or the branch name. The snapshot's issue lines are mostly cut off by the tool, so I could only judge a few from the snapshot. I found no further candidates, apart from those below.

| Issue | Classification | Closure assessment |
|---|---|---|
| [#7537](https://github.com/cgeo/cgeo/issues/7537) "Show account name (and avatar) in settings for other connectors", **verified (full text)** | **Partly fixed**, confidence medium. The summary now shows "Connected as <name>" for OC, SU and GeoKrety through `AbstractAuthorizationPreference.updateAuthorizationInfo`. | Keep open. No avatar is added. The name is empty until a login for OC/SU, GeoKrety has no user name at all (`getUserName()` returns `null`), and D1 can show the wrong name. Verify: authorize OC.de, then open its settings screen. |
| [#5619](https://github.com/cgeo/cgeo/issues/5619) "`*AuthorizationActivity` need to be factorized", **verified (full text)** | **Related, not fixed**. The branch changes the preference classes, not the activity hierarchy. | Keep open. A maintainer might assume it is fixed, because both authorization activities got the same `setStartButtonText` helper. It is still duplicated. |
| [#10339](https://github.com/cgeo/cgeo/issues/10339) "Forbidden login at GCConnector", **verified (full text)** | Unrelated (network error handling). | Waiting for information or likely outdated: 2021, last comment 2021. Keep open if in doubt. |
| [#17700](https://github.com/cgeo/cgeo/issues/17700) "Redesign how c:geo opens files" | Unrelated. | Keep open. |
| [#17191](https://github.com/cgeo/cgeo/issues/17191) "Map crash when open map" | Unrelated. | Keep open; needs a log. |

Terms searched: authoriz*, OAuth, revoke, Geokrety, login status, account name, connected. Search hits for #264 ("Captcha during authoriz…") and #389 ("Is it possible to keep the logged in…") could not be read in full; I did not classify them. They are **to be verified** only as possible area issues.

## 5. Draft PR description

**Unify authorization status handling in settings**

- Rename `AbstractClickablePreference` to `AbstractAuthorizationPreference`. Title, summary and icon for GC, SU, GeoKrety and OC now come from one place, based on `isAuthorized()` and `getUserName()`. The summary mentions tap to update and long tap to remove.
- Fix a crash in the GC settings when credentials are not valid.
- Replace the six opencaching settings fragments with `PreferenceServiceOpencachingFragment`. The site comes from `OCPreferenceKeys`.
- `getLoginStatusString` and `isLoggedIn` for GC, OC and SU no longer report a cached state after credentials or tokens were removed.
- The authorization screens' explanation text names the current start button label (positional placeholders in `auth_explain_long` and `auth_token_explain_long`).
- SU revoke now clears the secret token as well.
- The send2cgeo registration is a plain preference with no long-tap action.

**User-visible changes:** settings titles, summaries and icons for all authorization entries, the "Connected" text, the authorization screens' explanation text, and the login status after a revoke.

**Test:**
1. For GC, SU, GeoKrety and each OC site, open the settings screen from the service list, from search and from a deep link. Check title, summary, icon and website link.
2. Long-tap to revoke each service. Check the main-screen status and that GeoKrety logging is no longer offered.
3. Re-authorize as another account without restarting. Check the name and status (known issue D1 for OC and SU).
4. Turn the network off. Open the settings and authorization screens.
5. Check that the explanation text follows the button label, including after an error.

No issue is referenced with "fixes #", since none is clearly fixed. #7537 is partly addressed; the author should decide whether to mention it.

## Recommended next steps

1. Fix D1: reset the OC and SU cached state on revoke, and optionally log in after authorization.
2. Fix D2 and D4: make `isRegisteredForGeokretyLogging()` use `hasGeokretyAuthorization()`.
3. Fix D3: derive the OC site from the clicked preference key and remove the XML extras.
4. Clean up the translations (D5) if lint fails.
5. Add the undocumented behavior changes to the PR description.
6. Optionally, show a GeoKrety user name and avatar as a follow-up for #7537.
