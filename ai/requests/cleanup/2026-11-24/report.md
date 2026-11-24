<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 1/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 481.8 of 1500 used, 718.2 available beyond the reserve | workflow: 82cc223d3f1a7bb66fe3741eb4cd0662da311006 -->

I'll start by checking which candidate files exist and how the snapshot is laid out.

All 20 candidate files exist. I'll read them in parallel.

I've read all 20 issues. Next I'll check the upstream code for each feature or bug, starting with the most likely fixed or removed items.

Early findings: `NavigateAnyPointActivity` and `MissingQuantity` (still disabled) remain, and `ToolbarWidgetWrapper` appears nowhere. I'll check the remaining candidates next.

Several candidates need a closer look at the specific code. I'll check the OKAPI error path, GC archived detection, the owner popup, GPX import, and the spoiler and shortcut strings.

The OKAPI error text is passed into `LogResult`, so I need to confirm it reaches the user. I'll also check the AL owner actions and the GC archived logic.

Those two system reminders arrived in the user turn, so they are your instructions and I'll follow them. This task is read-only, so the build and checkstyle gates don't apply. Next I'll check how the OKAPI error reaches the user, the AL owner actions, and whether county is shown anywhere.

The OKAPI message is carried through `StatusResult.getErrorString()` into the error notification. I'll confirm `LogResult` stores it as the server message, and check whether caches (not just the current position) get an address with county.

The OKAPI message does reach the user through the error notification, so 11394 looks fixed. Last, I'll search the snapshot for duplicates and check the log-type special case and the long-tap code.

Long-tap now uses a global setting, but not the two-stage tap requested in 14323. I'll run one narrower snapshot search for duplicates, since the last one was truncated.

That search was too broad. I'll run one tight duplicate search on the specific topics.

## Summary

I checked 20 issues. 3 can probably be closed, 0 are waiting for information, and 17 stay open.

- **Probably fixed:** 1
- **Duplicates:** 1
- **Obsolete:** 1
- **Waiting for information:** 0
- **Keep open:** 17

## Probably fixed

- [#11394](https://github.com/cgeo/cgeo/issues/11394) Provide error message returned by connector to user
  - Reason: OKAPI's `message` is now passed as the server message in `upstream/main/src/main/java/cgeo/geocaching/connector/oc/OkapiClient.java` (around lines 672–676). `LogResult` and `StatusResult.getErrorString()` (`connector/StatusResult.java`) append it, and `LogPostingService.java` line 155 shows it in the error notification. Confidence: medium. I did not confirm the commit that introduced it.
  - Closing comment: "Thanks for the report! c:geo now shows the server's error message (for OKAPI-based services) when a log post fails, so reasons like 'you cannot attend an event before it takes place' are visible. Closing as fixed. If you still see an unhelpful error, please comment or reopen."

## Duplicates

- [#15313](https://github.com/cgeo/cgeo/issues/15313) wording of link to images (minor)
  - Duplicate of [#17091](https://github.com/cgeo/cgeo/issues/17091) "Rename 'spoiler images'", which has the better discussion. Both ask for the same rename, and the German string is still singular ("Hinweisbild", `values-de/strings.xml`). Confidence: high.
  - Closing comment: "Thanks for the report! This is the same request as #17091 (renaming 'spoiler images'), which has more discussion, so I'm closing this one as a duplicate. Please continue the discussion there."

## No longer applicable

- [#15358](https://github.com/cgeo/cgeo/issues/15358) ToolbarWidgetWrapper: Progress display unsupported
  - Reason: `ToolbarWidgetWrapper` and the "Progress display unsupported" message no longer exist anywhere in `upstream/`. The log line comes from code that has been removed. Confidence: medium-high.
  - Closing comment: "Thanks for the report! The toolbar widget wrapper that logged this message no longer exists in the current code, so I'm closing this as no longer applicable. Please reopen if you still see the message in a current version."

## Keep open

[#14048](https://github.com/cgeo/cgeo/issues/14048), [#8561](https://github.com/cgeo/cgeo/issues/8561), [#15266](https://github.com/cgeo/cgeo/issues/15266), [#9187](https://github.com/cgeo/cgeo/issues/9187), [#13704](https://github.com/cgeo/cgeo/issues/13704), [#10914](https://github.com/cgeo/cgeo/issues/10914), [#11321](https://github.com/cgeo/cgeo/issues/11321), [#11334](https://github.com/cgeo/cgeo/issues/11334), [#14323](https://github.com/cgeo/cgeo/issues/14323), [#9126](https://github.com/cgeo/cgeo/issues/9126), [#15339](https://github.com/cgeo/cgeo/issues/15339), [#15350](https://github.com/cgeo/cgeo/issues/15350), [#15288](https://github.com/cgeo/cgeo/issues/15288), [#15367](https://github.com/cgeo/cgeo/issues/15367), [#15364](https://github.com/cgeo/cgeo/issues/15364), [#15373](https://github.com/cgeo/cgeo/issues/15373), [#15374](https://github.com/cgeo/cgeo/issues/15374)

Worth a later look:
- [#15350](https://github.com/cgeo/cgeo/issues/15350): `NavigateAnyPointActivity` is still present, so the removal work is not done.
- [#14323](https://github.com/cgeo/cgeo/issues/14323): only a global long-tap menu setting exists, not the two-stage tap requested.
- [#15373](https://github.com/cgeo/cgeo/issues/15373): overlaps with [#7797](https://github.com/cgeo/cgeo/issues/7797) (favorite percentage).
- [#13704](https://github.com/cgeo/cgeo/issues/13704): `MissingQuantity` is still disabled in `main/build.gradle` and `main/lint.xml`.

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#11394](https://github.com/cgeo/cgeo/issues/11394): [PR #15010](https://github.com/cgeo/cgeo/pull/15010) "rel to \#2012: connect to new logging api and refactor", merged 2023-12-14, commit [85605d02a7](https://github.com/cgeo/cgeo/commit/85605d02a7424e0f85b5a8f394e37256068e5087) of 2023-12-14, added `LOG_POST_ERROR, data.get("message").asText()` in `main/src/main/java/cgeo/geocaching/connector/oc/OkapiClient.java`.

```cleanup-result
#14048 keep-open
#8561 keep-open
#15266 keep-open
#9187 keep-open
#13704 keep-open
#10914 keep-open
#11321 keep-open
#11334 keep-open
#11394 fixed
#14323 keep-open
#15313 duplicate
#9126 keep-open
#15339 keep-open
#15350 keep-open
#15358 obsolete
#15288 keep-open
#15367 keep-open
#15364 keep-open
#15373 keep-open
#15374 keep-open
```
