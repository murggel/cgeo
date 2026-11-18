<!-- task: review-branch | upstream: cgeo/cgeo@81d6f67055136a9fc1dfde9d8cf045abe7f911aa | branch: murggel/cgeo:feature/improve-authorization@f44d29b154a9e0bafe5d84a2273e9fd5fbd79f0d | base: master@2dc6a7075c980380907f6cb8d14232bfb80ea929 | issue snapshot: 2026-11-15 | preselected: 5 | instructions: yes | previous: review-003-claude | provider: claude | workflow: de3391133fa01b5558a6d4e71660cbd58e767961 -->

# Branch review: murggel/cgeo `feature/improve-authorization`, follow-up (head f44d29b)

I read the code in `branch-head/` and did not build or run anything. I did not re-read the translated `strings.xml` files. The base has moved on (34 commits since the merge base), and I did not compare it against `upstream/`.

## Status of the previous report

| # | Previous finding | Status | Reason |
|---|---|---|---|
| D1 | OC/SU keep the old account's login state after revoke and re-authorize | **Fixed**, with one residual risk (N2) | `OAuthPreference.revokeAuthorization` (`OAuthPreference.java:108-110`) now resets the connector state. `OAuthAuthorizationActivity.changeToken` calls `loginWithNewTokens()` (`OAuthAuthorizationActivity.java:301,315-327`) after the tokens are stored. |
| D2 | GeoKrety still counts as registered after revoke | **Fixed** | `Settings.isRegisteredForGeokretyLogging()` now returns `hasGeokretyAuthorization()` (`Settings.java:1080-1083`). |
| D3 | Missing or invalid `ocSite` extra crashes the OC settings | **Mostly fixed** | The XML extras are gone. The site comes from `OCPreferenceKeys.getByAuthPrefKey(pref.getKey())` (`SettingsActivity.java:362-365`) and `getByPrefScreenKey` (`:255,286`). A small fallback remains (N3). |
| D4 | `TokenPreference` and `Settings` use different rules for "authorized" | **Fixed** | Both now use `isNotBlank` (`TokenPreference.java:72`). |
| D5 | Translations out of sync | **Still open** | The branch changes only the default `strings.xml`. The translated `auth_explain_long` and `auth_token_explain_long` have a single `%s`, and `auth_unconnected` is removed only from the default file. I did not re-check the locale files. |
| 4 | The SU secret-key fix is undocumented | **Still open** | See the behavior changes below. |
| 5 | Offline handling: no defect | **Holds** | Details are in the flow table. |

## 1. Base and scope

- **Base:** `cgeo/cgeo:master`, merge base `2dc6a70`.
- **Size:** 14 commits (the previous report covered 10) and 33 changed files.
- **Uncertainty:** the base has 34 newer commits that I did not compare, so I can't confirm conflicts.

## 2. Findings

No finding is severe. N1 to N3 are new. N4 to N6 are open points, some of them unchanged from the previous report.

### N1. The background-login counter can block later login attempts (low-medium, pre-existing, separate change)

- **Where:** `AbstractNavigationBarActivity.java:462-497`.
- **Why:** `LOGINS_IN_PROGRESS` is set to `loginConns.length`. It is decremented only for connectors that actually log in, because the `if (mustLogin || !conn.isLoggedIn())` check skips already-logged-in ones. It is also not decremented if `login()` throws.
- **Scenario:**
  1. GC is logged in, OC.de has just been authorized while offline, and its login failed.
  2. The next main-screen start runs `startBackgroundLogin`. It sets the counter to 2, and only OC decrements it.
  3. The counter stays at 1 for the rest of the process.
  4. Every later `startBackgroundLogin` returns immediately.
- **Impact:** the new code comment says a failed login "is retried by the next background login". That is true once at most. After that, a failing OC or SU login is not retried until the app restarts, so the main screen shows "login failed" even though the tokens are valid.
- **Solutions:**
  - **(a)** Count only the connectors that will actually log in, and decrement in a `finally`. It is small and safe, but it touches shared navigation code.
  - **(b)** Replace the counter by a per-connector "login running" flag. This is cleaner but a larger change.
- **Recommendation:** (a), in a separate change. The branch is not the cause, but the new comment relies on this behavior.

### N2. `resetLoginStatus()` can race with a running login, and the authorization dialog waits for the login (low)

- **Where:** `OCApiLiveConnector.java:48,171-174` and `SuConnector.java:120-122`. `userInfo` is a plain field. Also `OAuthAuthorizationActivity.java:299-307`.
- **Scenario:** a background `login()` with the old tokens is in flight while the user revokes or re-authorizes. It writes the old account's `userInfo` after the reset. Separately, `loginWithNewTokens()` runs before `changeTokensHandler.sendEmptyMessage(status)`, so "authorized" is reported only after the login network call returns.
- **Impact:** the race window is narrow and needs a login in flight, but the stale name could reappear. The delay is bounded by the network timeout, and the login failure is already caught.
- **Solutions:**
  - Make `userInfo` volatile. This is cheap and fixes only visibility.
  - Send the result message first and log in afterwards. This is better for the UI, but the settings screen may then read the state before the login finishes.
- **Recommendation:** make the field `volatile` in this branch. Leave the rest as it is.

### N3. A mismatched OC service key still crashes the OC settings (low)

- **Where:** `SettingsActivity.java:362-371` and `PreferenceServiceOpencachingFragment.java:1220-1226` (`getSite`).
- **Scenario:** a services-list entry that points to `PreferenceServiceOpencachingFragment` but has a key that is not in `OCPreferenceKeys` falls into the `else` branch. The fragment is created without arguments, and `requireArguments()` throws. This can only happen after a future XML edit.
- **Solutions:**
  - Add a unit test that every OC entry in `preferences_services.xml` resolves through `getByAuthPrefKey`.
  - Fail visibly with a clear log message.
  - Skip the screen with a toast.
- **Recommendation:** the test. It is cheap and belongs in this branch.

### N4. GC cached data stays visible after revoke (low)

- **Where:** `GCConnector.java:486-488,500-503,569`.
- **Why:** only `getLoginStatusString` and `isLoggedIn` are guarded by `getCredentials().isValid()`. `getUserName()`, `getCachesFound()` and line 569 still read the `GCLogin` cache.
- **Scenario:** after a GC revoke, GC code that does not use `isLoggedIn` (for example the found count or owner checks) can still use the old account until the next login or restart.
- **Impact:** low. The status display is correct.
- **Solutions:**
  - Guard those getters the same way.
  - Call `GCLogin.getInstance().logout()` in `CredentialsPreference.revokeAuthorization`. That is more thorough, but I did not check its side effects.
- **Recommendation:** `logout()` on revoke, as a separate change after checking `GCLogin.logout()`.

### N5. Translations (low, unchanged; previous D5)

- **Impact:**
  - Translated `auth_explain_long` and `auth_token_explain_long` have one `%s`. They will not show the button label, and they still hard-code the old button name.
  - The `auth_connected` text changed, but translations still read "Connected".
  - `auth_unconnected` is likely to trigger an `ExtraTranslation` lint warning.
- **Solutions:** remove or mark the stale translations as this project usually does (translations come from Crowdin), or leave them to the next translation sync.
- **Recommendation:** only change them if lint fails. Otherwise leave them to the translation workflow.

### N6. "Connected" means "credentials stored", not "login works" (low, by design)

- **Where:** `CredentialsPreference.java:129-131`, `OAuthPreference.java:94-100`.
- **Scenario:** the settings show "Connected as X" even if the last login failed, for example with a changed password or while offline. For GC the main screen then shows the failure.
- **Solution:** none needed in this branch. Mention it in the PR description.

### Flow check

| Flow | GC | OC / SU | GeoKrety |
|---|---|---|---|
| Authorize | OK | OK. The name appears after the login that now follows the authorization. | OK |
| Re-authorize as another account | OK. `GCAuthorizationActivity` forces a logout and then a login. | **Fixed.** Reset plus login. N2 is a narrow race. | OK |
| Long-tap revoke | OK. Cookies and avatar are cleared. N4. | OK. Tokens are cleared and state is reset. SU now clears its secret as well. | **Fixed (D2).** |
| App restart | OK | OK. The cache is rebuilt. | OK |
| No internet | The settings use local data. | The login after authorization fails quietly, the status shows "failed" while the settings show "Connected". The retry is limited by N1. | No network use |
| Main screen versus settings | Consistent | Consistent after a login. | n/a |
| OC screens from the list | n/a | OK, via the key of the clicked entry. | n/a |
| OC screens from search or deep link | n/a | OK, via `getByPrefScreenKey`. A restored fragment keeps its arguments. | n/a |

## 3. Behavior changes

**Intended and documented**
- Unified title, summary and icon for GC, SU, GeoKrety and OC. The summary mentions tap to update and long tap to remove.
- Fix for the GC settings crash when credentials are invalid.
- The six OC settings fragments are merged into one.
- Login status after a revoke (`getLoginStatusString`, `isLoggedIn`), now also for OC/SU after re-authorization.
- The explanation text names the actual start button label (`auth_explain_long`, `auth_token_explain_long`).
- GeoKrety is no longer registered for logging after a revoke. A blank token counts as not authorized.

**Intended but undocumented (mention in the PR description)**
- SU revoke now clears the secret token. The old mapping passed the public key id for both (`OAuthPreference.java:32`).
- A successful OC/SU authorization now performs a login in the background, so authorization takes as long as that login.
- GC settings show the raw stored user name (`getUsernameRaw()`).
- `RegisterSend2CgeoPreference` is now a plain `Preference` without a long-tap action.
- The `auth_unconnected` string is removed and the `auth_connected` text changed.
- `IOAuthCapability` has a new default method `resetLoginStatus()`, and `ConnectorFactory` has two new helpers.

**Unintended or side effect**
- None found beyond N1 to N4.

## 4. Issues fixed by the branch

No issue is referenced in the commit messages or the branch name.

| Issue | Classification | Closure assessment |
|---|---|---|
| [#7537](https://github.com/cgeo/cgeo/issues/7537) "Show account name (and avatar) in settings for other connectors" — **verified (full text)** | **Possibly partly fixed**, confidence medium. `AbstractAuthorizationPreference.updateAuthorizationInfo` shows "Connected as <name>" for OC/SU once a login has run (`OAuthPreference.getUserName`, `OAuthPreference.java:113-125`). GeoKrety has no user name, and no avatar is added. To verify: authorize OC.de and open its settings screen, then check the summary. | Keep open. The avatar is missing, and the author should decide whether the name alone is enough. |
| [#5619](https://github.com/cgeo/cgeo/issues/5619) "`*AuthorizationActivity` need to be factorized" — **verified (full text)** | **Related, not fixed.** The authorization activities are still duplicated. | Keep open. |
| [#16977](https://github.com/cgeo/cgeo/issues/16977) and [#13266](https://github.com/cgeo/cgeo/issues/13266) — **verified (full text)** | Unrelated. They are GC web API 403 and 400 errors. | #16977 is a CI test problem; keep it open. #13266 is old and has no activity; keep open if in doubt. |
| [#10339](https://github.com/cgeo/cgeo/issues/10339) | Unrelated by title (GC "Forbidden login"). I did not re-read the full text this time. | Keep open if in doubt. |

**Search terms** (the snapshot lines were only partly readable in the previous run): authoriz*, OAuth, revoke, GeoKrety, login status, account name, connected. I found no further issue that the branch fixes. The candidates #264 and #389 from the previous report were not read in full, so they stay **to be verified**.

## 5. Draft PR description

**Unify authorization status handling in settings**

- Rename `AbstractClickablePreference` to `AbstractAuthorizationPreference`. Title, summary and icon for GC, SU, GeoKrety and the OC sites now come from one place, based on `isAuthorized()` and `getUserName()`. The summary mentions tap to update and long tap to remove.
- Fix a crash in the GC settings when credentials are not valid.
- Replace the six opencaching settings fragments with `PreferenceServiceOpencachingFragment`. The site comes from the clicked service entry or from the screen key (`OCPreferenceKeys`).
- `getLoginStatusString` and `isLoggedIn` for GC, OC and SU no longer report cached state after credentials or tokens were removed.
- OC and SU: revoke resets the cached user info, and a successful authorization logs in again in the background, so the new account is shown.
- GeoKrety: a revoked or blank token no longer counts as authorized or as registered for logging.
- The authorization screens' explanation text names the current start button label (positional placeholders in `auth_explain_long` and `auth_token_explain_long`).
- SU revoke now clears the secret token as well.
- The send2cgeo registration is a plain preference without a long-tap action.

**User-visible changes:** settings titles, summaries and icons for the authorization entries, the "Connected" text, the authorization screens' explanation text, the login status after revoke and re-authorization, and the GeoKrety logging offer after a revoke.

**Test:**
1. For GC, SU, GeoKrety and each OC site, open the settings screen from the service list, from search and from a deep link. Check title, summary, icon and website link.
2. Long-tap to revoke each service. Check the settings summary and the main-screen status. For GeoKrety, check that logging is no longer offered.
3. Re-authorize OC or SU as another account without restarting the app. Check the name in the settings and the status on the main screen.
4. Turn the network off, authorize, and check that the authorization still succeeds with a "login failed" status.
5. Check that the explanation text follows the button label, including after an error.

No "fixes #" line: no issue is clearly fixed. #7537 is only partly addressed, and the author should decide whether to mention it.

## Recommended next steps

1. **In this branch:** make `userInfo` in `OCApiLiveConnector` and `SuConnector` `volatile` (N2).
2. **In this branch:** add a test that every OC services-list key resolves through `OCPreferenceKeys.getByAuthPrefKey` (N3).
3. **In this branch:** put the undocumented behavior changes into the PR description. These are the SU secret fix, the login after authorization, the raw GC user name, the send2cgeo change and the removed or changed strings.
4. **Check before the PR:** run lint and decide whether the stale translations (N5) need action.
5. **Separate change:** fix the `LOGINS_IN_PROGRESS` counter (N1), because the new "retried by the next background login" comment depends on it.
6. **Separate change:** call `GCLogin.logout()` on GC revoke after checking its side effects (N4).
7. **Optional follow-up for #7537:** a GeoKrety user name and avatars.
