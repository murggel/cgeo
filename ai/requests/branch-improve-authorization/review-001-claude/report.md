<!-- task: review-branch | upstream: cgeo/cgeo@2dc6a7075c980380907f6cb8d14232bfb80ea929 | branch: murggel/cgeo:feature/improve-authorization@d4f56b0e707caf7ece86cfe415f668ad01eaa2f5 | base: master@f26cfc0f009b4bbbd83409fb01e5236359631ff8 | instructions: yes | provider: claude | workflow: 8440728fb105f1950f639970582add6ac0999ee1 -->

## 1. Base and scope

- **Base:** `cgeo/cgeo:master`, merge base `f26cfc0`, head `d4f56b0`.
- **Size:** 10 commits, 28 changed files.
- **Base movement:** the base has one newer commit since the merge base. I didn't find anything in `upstream/` that I could confirm conflicts with this branch.
- **Not verified:** I didn't build or run the app. All findings come from reading the code.

## 2. Findings

I found no crash or data-loss defect. I also found no single bug that breaks the login flow. These are the issues I could confirm, most severe first.

### 1. Stale connector state after revoke and re-authorization (medium)

**Where:** `GCConnector.java` `getLoginStatusString` / `isLoggedIn`; the same pattern in `OCApiLiveConnector.java` and `SuConnector.java`. The changed lines are about 504–517 in GC and 184–197 in OC.

**What the branch does.** Commit `8e0a6aa` fixes the stale status only for the revoked state. It adds a guard (`getCredentials().isValid()` for GC, `supportsPersonalization()` for OC and SU) that overrides the cached state. The cache itself is never reset.
- `GCLogin.actualLoginStatus` stays `true`.
- `OCApiLiveConnector.userInfo` and `SuConnector.userInfo` stay `SUCCESSFUL` with the old name.

**Scenario.** The user long-taps to remove the authorization, then authorizes again, possibly as a different account. The guard now passes again. `isLoggedIn()` and the status string report the previous account's "logged in" state until the next `login()` completes. `AbstractAuthorizationPreference.updateAuthorizationInfo` also shows the old user name from `getUserName()`, because `OAuthPreference.getUserName` reads `userInfo.getName()`. The OC and SU `login()` methods rebuild `userInfo` and the GC login refreshes its state, but nothing triggers them after revoke.

**Suggested fix.** In the revoke path, reset the connector cache (a "not logged in" `UserInfo` for OC/SU, `GCLogin` state for GC). Alternatively, trigger `login()` after a successful authorization. I did not trace whether the authorization activities already do this.

**Other callers.** Code that calls `GCLogin.getInstance().isActualLoginStatus()` directly, instead of going through `GCConnector.isLoggedIn()`, still sees the stale value. I did not check how many callers do this.

### 2. Unrelated token-key fix, not in the commit messages (low, behavior change)

**Where:** `OAuthPreference.java:33`.

The SU mapping used `getTokenPublicPrefKeyId()` for both the public and the secret key. It now uses `getTokenSecretPrefKeyId()`. This is a correct fix.
- **Before:** "revoke" cleared only the public token and left the secret in place.
- **After:** both tokens are cleared.
- **Documentation:** no commit mentions it.

### 3. Fragile "ocSite" extra, duplicated in XML and code (low)

`PreferenceServiceOpencachingFragment` documents that the `"ocSite"` extra must match `preferences_services.xml`. `SettingsActivity.onPreferenceStartFragment` passes `pref.getExtras()` to the fragment. Two entry paths now exist:
- `newInstance(...)` via `openRequestedFragment`.
- The XML `<extra>`.

A typo in an XML value, or a new OC site added without an `<extra>`, makes `getSite()` throw `IllegalStateException` or `IllegalArgumentException` when the settings screen opens. Commit history shows the author switched between approaches (`5eabc3b` removed the extras, `a183c5c` re-added them). The `OCPreferenceKeys.valueOf` call would be safer if it resolved the site from the clicked preference's key, as `5eabc3b` intended.

### 4. Translations out of sync (low)

- **`auth_connected`:** it now contains the "tap to update / long tap to remove" hint, but existing translations still read "Connected".
- **`auth_unconnected`:** it was removed from the default strings while all translated files still define it. This may trigger lint's `ExtraTranslation` check.
- **`auth_explain_long` / `auth_token_explain_long`:** the source strings switched to `%1$s` / `%2$s`. Existing translations use a single `%s` plus a hard-coded button name such as "Starte Autorisierung". They still format correctly. They will not follow the actual button label until they are retranslated.

### Offline behavior

Loss of connectivity is handled gracefully by this branch, and I found no defect.
- The new authorization summary and title depend only on local data: credentials, tokens, and cached user name.
- `getLoginStatusString` / `isLoggedIn` add no network calls.
- The authorization activities' error handlers still reset the button, and the explanation text now follows it.
- `MainActivity` still guards the GC error line with `Network.isConnected()`.
- Minor cost: OC and SU `isLoggedIn()` now read SharedPreferences on every call through `getSupportedAuthLevel()`. I don't expect this to matter.

### On "the problem with the login flow"

The only login-flow problem I can substantiate is finding 1. The status is now correct after revoke. After re-authorization, the connectors rely on a cache that is never invalidated at the moment the account changes. The fix is in the suggestion under finding 1.

## 3. Behavior changes

### Intended and documented
- **Unified authorization preference display.** Title, summary and icon now come from `isAuthorized()` and `getUserName()`, and the summary mentions tap and long tap.
  - GC, SU, Geokrety and OC all use it.
  - The implementation goes slightly further: the "Connected" summary for OAuth and token services now also carries the hint text.
- **GC settings crash fix.** The `assert`/null path is replaced by `updateAuthorizationPreference`, which logs an error and returns.
- **OC fragments merged into one.** `PreferenceServiceOpencachingFragment` replaces six classes.
- **Correct login status after revoke.** This is implemented for GC, OC and SU, but only partly (see finding 1).
- **Positional placeholders in `auth_explain_long`.**
- **Explanation text follows the button label.** This also applies to the token activity.
- **Missing authorization preference is logged** instead of silently ignored.
- **`RegisterSend2CgeoPreference` is a plain `Preference`.** It no longer carries the long-click removal behavior.

### Intended but undocumented
- **The SU secret key id fix** (finding 2).
- **The OAuth and token activities now set the explanation text late.** `auth2` is set after the button text, and `TokenAuthorizationActivity.getAuthExplainLong` has a new signature.
- **The "Connected" summary for Geokrety and OAuth now has the long-tap hint.** Before, they showed just "Connected". Mention this in the PR.
- **GC settings** show the raw stored user name from `getUsernameRaw()` rather than `credentials.getUserName()`.
- **`auth_unconnected` was removed.** The Not connected summary is now "Not connected yet - tap here to authorize" for SU and GC in the XML defaults.

### Unintended or side effects
- **Stale cache after re-authorization** is described in finding 1.
- **Hard failure on a bad site extra.** It is described in finding 3.

## 4. Draft PR description

**Improve authorization handling in settings**

This PR changes how authorization is shown and handled in the settings screens.

- `AbstractClickablePreference` is renamed to `AbstractAuthorizationPreference`. It now sets title, summary and icon in one place from `isAuthorized()` and `getUserName()`. The summary mentions tap to update and long tap to remove.
- The GC, SU, Geokrety and OC settings fragments use this shared update. This also fixes a crash in the GC settings when credentials are not valid.
- The six opencaching settings fragment classes are merged into one `PreferenceServiceOpencachingFragment`. The site comes from `OCPreferenceKeys`.
- `getLoginStatusString` and `isLoggedIn` for GC, OC and SU no longer report a cached "logged in" state after credentials or tokens have been removed.
- The authorization activities keep the explanation text in sync with the start button label. The `auth_explain_long` strings use positional placeholders.
- Fixed SU revoke so that the secret token is cleared as well. Previously the public key id was used for both tokens.
- The send2cgeo registration is no longer an authorization preference.

**User-visible changes:** authorization summaries and titles in settings, the explanation text on the authorization screens, and the login status shown after revoking an authorization.

**How to test:**
1. For GC, SU, Geokrety and each OC site, open the settings screen. Check title, summary and icon for the authorized and unauthorized states.
2. Long-tap to remove the authorization. Confirm the entry and the main-screen login status change to "not logged in".
3. Re-authorize, ideally as a different account. Confirm the user name and status update.
4. Repeat with the network off. The settings screens must still render, and the authorization screens must show their error toast and reset the button.
5. Open the authorization screens and check that the explanation text names the current button label.
6. Open each OC site's settings from the service list. Confirm title, website link and authorization entry are correct for that site.
