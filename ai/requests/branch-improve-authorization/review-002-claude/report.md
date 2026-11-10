<!-- task: review-branch | upstream: cgeo/cgeo@2dc6a7075c980380907f6cb8d14232bfb80ea929 | branch: murggel/cgeo:feature/improve-authorization@341fccd401d5b33589be9180c8f5271810c99b3a | base: master@2dc6a7075c980380907f6cb8d14232bfb80ea929 | instructions: yes | previous: review-001-claude | provider: claude | workflow: a7b2ecb528a67dede5bec90a06ed796748503f4c -->

## Status of the previous report

The previous report was based on head `d4f56b0`, and the branch has since been rebased or extended. The current head is `341fccd`, with 10 commits. I checked each item against `branch-head/`.

| # | Previous item | Status | Reason |
|---|---|---|---|
| 1 | Stale connector state after revoke and re-authorization | **Still open** | The guards (`getCredentials().isValid()`, `supportsPersonalization()`) are unchanged. `GCLogin` state and `SuConnector.userInfo` (`SuConnector.java:59,98-116`) are never reset on revoke. `OAuthAuthorizationActivity` has no `login()` call. |
| 2 | SU secret key id fix in `OAuthPreference.java:33`, not in the commit messages | **Still present, still undocumented** | It is a correct fix and not a defect. It still needs a mention in the PR description. |
| 3 | Fragile `ocSite` extra duplicated in XML and code | **Partly fixed** | `SettingsActivity` now resolves the site via `OCPreferenceKeys.getByPrefScreenKey` and `newInstance` for search and deep links. The XML `<extra>` path in `onPreferenceStartFragment` (`SettingsActivity.java:361`) is back (`afa0fc6`). A missing or mistyped extra still crashes in `getSite()` (`requireArguments()`, `IllegalStateException`, `valueOf`). |
| 4 | Translations out of sync | **Still open** | `auth_unconnected` is removed from the default `strings.xml`, but translated `values-*/strings.xml` files still define it, which can trigger lint `ExtraTranslation`. Translations of `auth_connected` and the `*_explain_long` strings still use the old text. They still format correctly. |
| – | Offline handling: no defect | **Still holds** | See "Offline and authorization review" below. |

## 1. Base and scope

- **Base:** `cgeo/cgeo:master`, merge base `2dc6a70`, head `341fccd`.
- **Size:** 10 commits and 28 changed files. The base has no commits since the merge base, so I see no base-side conflicts.
- **Not verified:** I didn't build or run the app. All findings come from reading the code.

## 2. Findings

### 1. Stale login state and user name after revoke, then re-authorize (medium, still open)

- **Where:** `GCConnector.java:504-518`, `OCApiLiveConnector.java:184-198`, `SuConnector.java:128-142`, and `OAuthPreference.getUserName` (`OAuthPreference.java:112-120`).
- **Scenario:** The user long-taps to revoke, then authorizes again, possibly as a different account.
  - The new guards pass again, because credentials or tokens exist.
  - The cache from the old account was never cleared. `userInfo` is still `SUCCESSFUL` with the old name, and `GCLogin.actualLoginStatus` is still true.
- **Impact:**
  - Main screen and settings show "logged in", and `AbstractAuthorizationPreference.updateAuthorizationInfo` shows "Connected as <old user>" until the next `login()`.
  - Nothing in the revoke or authorization path triggers `login()`.
  - Callers of `GCLogin.isActualLoginStatus()` that bypass `GCConnector` stay stale.
- **Cause:** The branch fixes the symptom with guards. It doesn't reset the cache when the authorization changes.
- **Suggested fix:** Reset the connector's cached state in `revokeAuthorization()`, or call `login()` after a successful authorization.

### 2. Fragment crashes on a missing or invalid `ocSite` extra (low, partly fixed)

- **Where:** `PreferenceServiceOpencachingFragment.java` (`getSite`, `onCreatePreferences`, `onResume`) and the `<extra>` entries in `preferences_services.xml`.
- **Impact:** Any OC entry added without a matching `<extra>`, or with a typo, crashes when the screen opens.
- **Fix:** The site is already derivable from the clicked preference key. Resolve it in `onPreferenceStartFragment` via `OCPreferenceKeys.getByAuthId(...)`, which removes the duplicate source of truth.

### 3. Translation and lint inconsistencies (low, still open)

- `auth_unconnected` is removed from the default strings but still exists in the translations.
- The `auth_connected` text changed meaning, but translations still read "Connected".
- Translated `auth_explain_long` and `auth_token_explain_long` hard-code the old button name. They won't follow the dynamic button label until they are retranslated.

### Offline and authorization review

I found no new defect in either area.

- **Offline:**
  - The preference summary and title, the revoke path and the new `isLoggedIn` guards use only local data (SharedPreferences, credentials, cached `userInfo`) and make no network calls.
  - The authorization activities' error handlers still reset the start button, and the explanation text now follows it.
  - `MainActivity` still guards the GC error line with `Network.isConnected()`.
- **Authorization:**
  - Revoke still clears credentials (GC also clears cookies and avatar), tokens (SU now clears both) and the Geokrety secret.
  - `isAuthorized()` is derived from stored credentials and tokens, not from a network result.
  - `OAuthPreference` resolves the OC token ids through `OCPreferenceKeys.getByAuthId`, so the OC mappings (`-1,-1`) are still handled correctly.
- **Offline gap tied to finding 1:** the status shown offline reflects the last cached login result, not current validity, because nothing re-checks it.

## 3. Behavior changes

### Intended and documented

- **Unified authorization preference display (`be78bad`):** Title, summary and icon are set in one place for GC, SU, Geokrety and OC.
  - The implementation goes further than the message. The "Connected" summary for OAuth and token services (which previously read plain "Connected") now carries the tap and long-tap hint, and the not-connected summary changed.
- **GC settings crash fix:** The `assert` and null path is replaced by a logged error (`aeb905a`).
- **OC settings fragments merged into one (`d4a523b`, `7e8b34e`, `afa0fc6`):** The commit messages describe changing approaches. The final state is a mix of XML extras and `getByPrefScreenKey`, which is more than a single approach (see finding 2).
- **Login status after revoke (`af95934`):** Only partly effective (finding 1).
- **Positional placeholders in `auth_explain_long`, and the explanation text following the button label (`ef235e2`, `4cd0d62`, `c5996f2`):** This also applies to the token activity and `auth_token_explain_long`.
- **Missing authorization preference is logged (`aeb905a`)** instead of silently ignored.
- **send2cgeo registration is no longer an authorization preference (`341fccd`):** It no longer has the long-click behavior.

### Intended but undocumented

- **SU revoke now clears the secret token as well (`OAuthPreference.java:33`):** Previously the public key id was used for both.
- **GC settings show the raw stored user name** (`getUsernameRaw()`) instead of `credentials.getUserName()`.
- **`auth_unconnected` removed:** The GC and SU XML defaults now use `auth_unconnected_tap_here`.
- **OC login status:** OC and SU `getLoginStatusString` and `isLoggedIn` now depend on stored tokens (`supportsPersonalization()`).
- **Authorization screens set `auth2` text after the button text:** The `TokenAuthorizationActivity.getAuthExplainLong` signature changed.

### Unintended or side effects

- **Stale cache after re-authorization:** See finding 1.
- **Hard failure on a bad site extra:** See finding 2.

## 4. Draft PR description

**Improve authorization handling in settings**

- Rename `AbstractClickablePreference` to `AbstractAuthorizationPreference`.
  - It sets title, summary and icon in one place from `isAuthorized()` and `getUserName()`.
  - The summary mentions tap to update and long tap to remove.
- GC, SU, Geokrety and OC settings use the shared update. This also fixes a crash in the GC settings when credentials are not valid.
- Merge the six opencaching settings fragments into `PreferenceServiceOpencachingFragment`. The site comes from `OCPreferenceKeys` and from a preference extra.
- `getLoginStatusString` and `isLoggedIn` for GC, OC and SU no longer report a cached "logged in" state after credentials or tokens have been removed.
- The explanation text on the authorization screens now names the current start button label. `auth_explain_long` and `auth_token_explain_long` use positional placeholders.
- SU revoke now clears the secret token too. Previously the public key id was used for both.
- The send2cgeo registration is a plain preference, not an authorization preference.

**User-visible changes:**
- Authorization titles, summaries and icons in settings.
- The "Connected" text for OAuth and token services.
- The explanation text on the authorization screens.
- The login status shown after revoking an authorization.

**How to test:**
1. For GC, SU, Geokrety and each OC site, open the settings screen. Check title, summary and icon in the authorized and unauthorized states.
2. Long-tap to remove the authorization. Confirm the entry and the main-screen login status change to "not logged in".
3. Re-authorize, ideally as a different account. Confirm the user name and status update. The branch may still show the old account here.
4. With the network off, open the settings and authorization screens. The settings must render, and the authorization screens must show an error toast and reset the button.
5. Check that the explanation text names the current button label, including after an error.
6. Open each OC site from the service list, and also via settings search. Confirm title, website link and authorization entry are correct for that site.
