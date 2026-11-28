<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 2/2 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 531.4 of 1500 used, 968.6 available beyond the reserve | workflow: 1110dd237fd88892ac4919eda5e1a4d19ad95956 -->

I'll start by reading the eight candidate issue files.

Most of these are recent, and none has a maintainer question to the reporter. Next I'll check the snapshot for duplicates and search upstream for the relevant code.

The broad grep was too noisy. I'll run targeted searches for the specific features and code paths, plus snapshot duplicates.

Key findings so far: monospace notes (#18895) and the geochecker link fix appear in master, and the Wherigo fix (#18855) needs checking. Next I'll read the relevant code and search the snapshot for duplicates.

Note: the two system reminders in this turn are ordinary instructions for code I write. This task is read-only reporting, so they don't change my work. Next I'll confirm when the Wherigo state-saving and geochecker-scheme fixes entered master.

Two more checks: whether the geochecker crash path has a fallback in master, and the Wherigo state-saving code.

## Summary

- Checked: 8 issues
- Probably fixed: 4 ([#18895](https://github.com/cgeo/cgeo/issues/18895), [#18901](https://github.com/cgeo/cgeo/issues/18901), [#18855](https://github.com/cgeo/cgeo/issues/18855), [#18229](https://github.com/cgeo/cgeo/issues/18229)). All four are already closed on GitHub, so only the record needs confirming.
- Duplicates: 0
- No longer applicable: 0
- Waiting for information: 0
- Keep open: 4

## Probably fixed

- [#18895](https://github.com/cgeo/cgeo/issues/18895) Option: monospace font for notes
  - Reason: The "Monospace font for notes" setting exists (`main/src/main/res/xml/preferences_cachedetails.xml`). `setNoteFont()` applies it in `main/src/main/java/cgeo/geocaching/ui/ViewUtils.java` (lines 1026–1036). Already closed.
  - Confidence: high
  - Closing comment: "Thanks for the request! This is now available as the 'Monospace font for notes' option under Settings → Cache details → Personal note. Please reopen or comment if it doesn't work as expected."

- [#18901](https://github.com/cgeo/cgeo/issues/18901) Activity for geochecker.com not found (2026.10.08)
  - Reason: `StartWebviewActivity` now catches `ActivityNotFoundException` (`main/src/main/java/cgeo/geocaching/settings/StartWebviewActivity.java`, lines 35–42). `CheckerUtils.ensureScheme()` (`main/src/main/java/cgeo/geocaching/utils/CheckerUtils.java`, lines 80–84) adds a missing scheme to schemeless links. Already closed. The malformed `http:/` link in the report was not separately verified.
  - Confidence: medium
  - Closing comment: "Thanks for reporting this. c:geo no longer crashes when no app can open the link, and links without a scheme are fixed. Please reopen if you still see the crash."

- [#18855](https://github.com/cgeo/cgeo/issues/18855) Wherigo text input problem
  - Reason: The maintainer comment says it was fixed in PR #18910. Master saves and restores the typed text in `WherigoInputDialogProvider` (`main/src/main/java/cgeo/geocaching/wherigo/WherigoInputDialogProvider.java`, lines 33, 94–96, 165–166). Already closed.
  - Confidence: medium
  - Closing comment: "Thanks for the report. Typed text in Wherigo input dialogs is now kept when switching apps (fixed in #18910). Please reopen if it still happens."

- [#18229](https://github.com/cgeo/cgeo/issues/18229) LOC file import hangs silently
  - Reason: `LocParser.parse()` reports progress before each cache is stored (`main/src/main/java/cgeo/geocaching/files/LocParser.java`, lines 127–144). Already closed.
  - Confidence: medium
  - Closing comment: "Thanks for the report. LOC imports now update the progress dialog for each cache. Please reopen if the import still hangs."

## Keep open

[#18883](https://github.com/cgeo/cgeo/issues/18883), [#18891](https://github.com/cgeo/cgeo/issues/18891), [#18908](https://github.com/cgeo/cgeo/issues/18908), [#18909](https://github.com/cgeo/cgeo/issues/18909)

- #18891 is a feature request. No code in master uses the personal-note image API.
- #18908 is a feature request. No linear-lab ordering exists in the routing code.
- #18909 is a system-level OOM from a support ticket with no app-specific trace.
- #18883 has no evidence either way; not verified in the cache-list code.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#18895](https://github.com/cgeo/cgeo/issues/18895): [PR #18896](https://github.com/cgeo/cgeo/pull/18896) "Add option to show notes in a monospace font", merged 2026-11-22, commit [fba61d1b7d](https://github.com/cgeo/cgeo/commit/fba61d1b7d85778b990cfbfed6a2e8e6f9f4136b) of 2026-11-14, added `public static void setNoteFont(` in `main/src/main/java/cgeo/geocaching/ui/ViewUtils.java`.
- [#18901](https://github.com/cgeo/cgeo/issues/18901): [PR #18902](https://github.com/cgeo/cgeo/pull/18902) "fix \#18901: don't crash on mal formatted urls", merged 2026-11-15, commit [3c4946f133](https://github.com/cgeo/cgeo/commit/3c4946f133b7b2d92ea0c58af167769cee43e7b4) of 2026-11-12, added `Never let an ActivityNotFoundException crash this activity` in `main/src/main/java/cgeo/geocaching/settings/StartWebviewActivity.java`.
- [#18855](https://github.com/cgeo/cgeo/issues/18855): [PR #18910](https://github.com/cgeo/cgeo/pull/18910) "fix \#18855: Wherigo: retain text input also on forced dialog reopening", merged 2026-11-15, commit [1138350d29](https://github.com/cgeo/cgeo/commit/1138350d295194cc46d84bf61d8d5801c6cd5b5d) of 2026-11-14, added `private static final String STATE_TEXT` in `main/src/main/java/cgeo/geocaching/wherigo/WherigoInputDialogProvider.java`.
- [#18229](https://github.com/cgeo/cgeo/issues/18229): [PR #18906](https://github.com/cgeo/cgeo/pull/18906) "Fix \#18229: show progress of the LOC import and let it be canceled", merged 2026-11-20, commit [3f5f4eb057](https://github.com/cgeo/cgeo/commit/3f5f4eb0579fca1a5707bb93ca348aae53f2e08b) of 2026-11-13, added `PROGRESS_MAX * done / coords.size()` in `main/src/main/java/cgeo/geocaching/files/LocParser.java`.

```cleanup-result
#18883 keep-open
#18891 keep-open
#18901 fixed
#18908 keep-open
#18909 keep-open
#18229 fixed
#18855 fixed
#18895 fixed
```
