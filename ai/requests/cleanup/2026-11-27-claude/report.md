<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | provider: claude | workflow: aee9d7d5a10c41a55e21353a131b82e5a38b97bd -->

## Summary

I checked 30 issues. Two can probably be closed, both as fixed. The other 28 stay open. I found no duplicates, no obsolete issues and no waiting issues.

| Category | Count |
|---|---|
| Probably fixed | 2 |
| Duplicates | 0 |
| No longer applicable | 0 |
| Waiting for information | 0 |
| Keep open | 28 |

## Probably fixed

**[#16751](https://github.com/cgeo/cgeo/issues/16751): Android 16 / targetSDK 36**
- This is a tracking issue for the move to targetSDK 36. Master already has `compileSdk = 36` (`upstream/main/build.gradle:34`) and `targetSdk = 36` (`upstream/main/build.gradle:47`). That meets the Play requirement bekuno quoted for 2026-08-31.
- The issue lists changes that "may hit us" and has no checklist, so a regression from a single item such as predictive back or large-screen resizing could still be tracked separately.
- Confidence: medium.
- Suggested comment:
  > c:geo on master now targets API 36 (`targetSdk = 36`), so the Google Play requirement is met. Closing this tracking issue. If a specific Android 16 behaviour change causes a problem, please open a separate issue for it, or reopen this one.

**[#17738](https://github.com/cgeo/cgeo/issues/17738): Add "New in version" (What's New) info to F-Droid releases**
- The original request was fastlane changelogs in `fastlane/metadata/android/<locale>/changelogs/<versionCode>.txt`. Master has them for en-US and de, for example `upstream/fastlane/metadata/android/en-US/changelogs/202611222.txt`. The thread has since drifted to APK size and the IzzyOnDroid limit, which is a separate topic.
- Confidence: medium. It is high for the original request, but the maintainers may want to keep the size discussion open somewhere else.
- Suggested comment:
  > Release notes for F-Droid are now provided via `fastlane/metadata/android/*/changelogs/`, so users see what's new when an update arrives. Closing this as implemented. The APK size and packaging questions discussed later in the thread can continue in a dedicated issue. Please reopen if anything is still missing.

## Keep open

[#17837](https://github.com/cgeo/cgeo/issues/17837), [#17866](https://github.com/cgeo/cgeo/issues/17866) (thank-you post, not a bug or request; the maintainers may simply want to close it), [#17979](https://github.com/cgeo/cgeo/issues/17979), [#18352](https://github.com/cgeo/cgeo/issues/18352) (Galician is not in master: no `values-gl`), [#18353](https://github.com/cgeo/cgeo/issues/18353) (master still has `values-in` and `values-iw`), [#16956](https://github.com/cgeo/cgeo/issues/16956) (only the code part is done; docs and wiki are open; later look worthwhile), [#18058](https://github.com/cgeo/cgeo/issues/18058) (the unpublished-caches PR is still open), [#18295](https://github.com/cgeo/cgeo/issues/18295) (master `InstallWizardActivity.java` still requests the notification permission), [#18362](https://github.com/cgeo/cgeo/issues/18362), [#18378](https://github.com/cgeo/cgeo/issues/18378), [#18282](https://github.com/cgeo/cgeo/issues/18282), [#18402](https://github.com/cgeo/cgeo/issues/18402), [#17156](https://github.com/cgeo/cgeo/issues/17156) (no question to the reporter, so not waiting), [#16265](https://github.com/cgeo/cgeo/issues/16265) (assigned; a related crash on truncated pages is still possible, as `GCParser.java:577` shows), [#18333](https://github.com/cgeo/cgeo/issues/18333), [#14360](https://github.com/cgeo/cgeo/issues/14360) (the question to developers on older Android versions is only from 2026-08-06), [#4688](https://github.com/cgeo/cgeo/issues/4688) (`[DATETIME]` follows the system format, but the custom-format wish is open and a maintainer decision is pending), [#17105](https://github.com/cgeo/cgeo/issues/17105) (fix PR #18454 not yet merged), [#18457](https://github.com/cgeo/cgeo/issues/18457), [#18469](https://github.com/cgeo/cgeo/issues/18469), [#18475](https://github.com/cgeo/cgeo/issues/18475), [#18407](https://github.com/cgeo/cgeo/issues/18407) (PR #18430 is not confirmed as merged), [#18411](https://github.com/cgeo/cgeo/issues/18411), [#18384](https://github.com/cgeo/cgeo/issues/18384) (the reporter says it no longer occurs, but there is no code evidence, so a later look is worthwhile), [#17199](https://github.com/cgeo/cgeo/issues/17199), [#18381](https://github.com/cgeo/cgeo/issues/18381), [#18508](https://github.com/cgeo/cgeo/issues/18508), [#6153](https://github.com/cgeo/cgeo/issues/6153) (reproduced again on 2026-08-25)

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#16751](https://github.com/cgeo/cgeo/issues/16751): [PR #18571](https://github.com/cgeo/cgeo/pull/18571) "Quick fix to raise targetSDK to 36", merged 2026-09-05, commit [b1dbefdddc](https://github.com/cgeo/cgeo/commit/b1dbefdddcf4acde7f04947c8b5db2526942b1fc) of 2026-09-05, added `targetSdk = 36` in `main/build.gradle`.
- [#17738](https://github.com/cgeo/cgeo/issues/17738): commit [b452a0dd7f](https://github.com/cgeo/cgeo/commit/b452a0dd7fbda9e4a11981bb94ff70190850f54e) of 2026-11-22 (no pull request), added `changelog_bugfix.md` in `fastlane/metadata/android/en-US/changelogs/202611222.txt`.

```cleanup-result
#17837 keep-open
#17866 keep-open
#17979 keep-open
#18352 keep-open
#18353 keep-open
#16956 keep-open
#18058 keep-open
#18295 keep-open
#18362 keep-open
#18378 keep-open
#18282 keep-open
#18402 keep-open
#17156 keep-open
#16265 keep-open
#18333 keep-open
#14360 keep-open
#4688 keep-open
#16751 fixed
#17105 keep-open
#18457 keep-open
#17738 fixed
#18469 keep-open
#18475 keep-open
#18407 keep-open
#18411 keep-open
#18384 keep-open
#17199 keep-open
#18381 keep-open
#18508 keep-open
#6153 keep-open
```
