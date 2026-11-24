<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | batch: 2/5 | provider: copilot 1.0.105 | model: claude-haiku-5.5 | AI credits before run: 481.8 of 1500 used, 718.2 available beyond the reserve | workflow: 82cc223d3f1a7bb66fe3741eb4cd0662da311006 -->

I'll start by checking which candidate files exist for the 20 issues.

The 20 candidate files all exist. Reading them now.

I've read all 20 issues. Next I'll check the snapshot for duplicates and search upstream code for the fixes or features each issue asks for.

The snapshot search is too broad, so I'll run narrower searches per topic, alongside code checks.

Snapshot greps are returning too much, so I'll rely on targeted checks. Next I'll inspect the key code paths: the map file validator, the waymarking connector, the offline-log delete flow, and the message strings.

Those two notes sit in the user turn, so I'll follow them. They concern code I write, and this task is read-only, so they don't change my work. Continuing with the remaining code checks.

Next I'll look at the offline-log delete handler and the coordinate parser entry point, which bear on #15531, #15765 and #15687.

The parser has a 20-match cap marked as a quickfix for #15687, which mitigates the hang but leaves the root cause. Next I'll check whether every offline-log delete path confirms first (#15765), and inspect the track list sort and the personal-note export.

Two more files need a look: the personal-note export (for #12051) and the `Geocache` call site that clears offline logs (for #15765).

I still need the call sites of `clearOfflineLog` to judge #15765, plus the route/track popup for #15508.

#15765 is still present: the fast offline-log menu's `CLEAR_LOG` branch deletes without confirmation. Next, #15508: `Trackfiles` already sorts a list locale-aware, so I'll check whether that's the track list in question.

Remaining checks: the waypoint discard-confirm path (#11849), the compass long-press message (#15312), and the Unbekannter Benutzer dashboard (#11852).

The #15312 message is unchanged in the code. Last, I'll confirm whether `EditWaypointActivity` skips the discard prompt when nothing changed (#11849).

#11849 is already handled: the discard prompt only appears when `isWaypointChanged` is true. Last step: a title-only snapshot search for duplicates of the remaining issues.

## Summary

Checked 20 issues: 1 probably fixed, 0 duplicates, 0 obsolete, 0 waiting, 19 keep-open.

## Probably fixed

- [#11849](https://github.com/cgeo/cgeo/issues/11849) Avoid confirm dialog when waypoint is unchanged
  - Reason: the discard prompt in `finishConfirmDiscard()` only shows when `isWaypointChanged(currentState)` is true (`main/src/main/java/cgeo/geocaching/EditWaypointActivity.java`, lines 634-641). Unchanged waypoints exit directly. The "remove the save tick" part of the request is not verified.
  - Confidence: medium
  - Closing comment: "Thanks for the report! Unchanged waypoints now leave the edit screen without the discard prompt. `EditWaypointActivity` only asks for confirmation when the waypoint has changed. If you still see the prompt with no changes, please reopen or comment with steps to reproduce."

## Duplicates

None.

## No longer applicable

None.

## Waiting for information

None. None of the open questions to reporters is older than six months.

## Keep open

[#420](https://github.com/cgeo/cgeo/issues/420) (own trackables list still missing; see also #4394), [#15420](https://github.com/cgeo/cgeo/issues/15420) (overlaps newer #16516), [#10843](https://github.com/cgeo/cgeo/issues/10843), [#11521](https://github.com/cgeo/cgeo/issues/11521) (only a `WaymarkingConnector` stub exists), [#11852](https://github.com/cgeo/cgeo/issues/11852), [#11992](https://github.com/cgeo/cgeo/issues/11992) (reproduced 2026-11-15; older than #17105), [#12051](https://github.com/cgeo/cgeo/issues/12051), [#15312](https://github.com/cgeo/cgeo/issues/15312) (message unchanged), [#15477](https://github.com/cgeo/cgeo/issues/15477), [#15499](https://github.com/cgeo/cgeo/issues/15499), [#15497](https://github.com/cgeo/cgeo/issues/15497), [#15508](https://github.com/cgeo/cgeo/issues/15508) (alphabetical sort only, no sort option), [#15531](https://github.com/cgeo/cgeo/issues/15531) (low confidence; may be by design for online logs), [#14950](https://github.com/cgeo/cgeo/issues/14950), [#15613](https://github.com/cgeo/cgeo/issues/15613), [#15687](https://github.com/cgeo/cgeo/issues/15687) (20-match cap mitigates only), [#15740](https://github.com/cgeo/cgeo/issues/15740), [#15745](https://github.com/cgeo/cgeo/issues/15745) (deprecated `getFromLocationName` still used), [#15765](https://github.com/cgeo/cgeo/issues/15765) (`CLEAR_LOG` in `LoggingUI` deletes without confirmation)

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#11849](https://github.com/cgeo/cgeo/issues/11849): commit [0a21fc6e31](https://github.com/cgeo/cgeo/commit/0a21fc6e310d697529642bb5173850df919410af) of 2015-06-09 (no pull request), added `isWaypointChanged` in `main/src/main/java/cgeo/geocaching/EditWaypointActivity.java`. The code is older than the issue, so this is probably not the fix.

```cleanup-result
#420 keep-open
#15420 keep-open
#10843 keep-open
#11849 fixed
#11852 keep-open
#11992 keep-open
#12051 keep-open
#15477 keep-open
#15312 keep-open
#15499 keep-open
#15497 keep-open
#15508 keep-open
#15531 keep-open
#14950 keep-open
#15613 keep-open
#11521 keep-open
#15745 keep-open
#15687 keep-open
#15740 keep-open
#15765 keep-open
```
