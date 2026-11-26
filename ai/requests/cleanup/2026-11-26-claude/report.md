<!-- task: cleanup-issues | upstream: cgeo/cgeo@eaf2f937998c638da1fb7975b15556012c4b7edf | issue snapshot: 2026-11-15 | provider: claude | workflow: 0bfa593922dc4190b9a934989334e64796b449bf -->

## Summary

30 issues checked, 4 can probably be closed:
- Probably fixed: 1
- Duplicates: 1
- No longer applicable: 0
- Waiting for information: 2
- Keep open: 26

## Probably fixed

**[#17488](https://github.com/cgeo/cgeo/issues/17488) Many ANR happening on c:geo startup**
- Both reported stack traces end in `Log.<clinit>` reading the log config file via SAF on the main thread. In master that work now runs in its own thread: `main/src/main/java/cgeo/geocaching/utils/Log.java:82-84` (`new Thread(Log::configureLogging).start()`). This is the change from PR #17521 mentioned in the issue.
- The issue also floated moving other SAF access off the main thread. That is a separate, general topic.
- Confidence: medium. Nobody has confirmed an improvement in the Play Store statistics.
- Closing comment: "The startup ANRs in the reported stack traces came from reading the logging configuration via SAF on the main thread. Since #17521 this runs in a separate thread (`Log.java`), and it is part of current releases. I'm closing this issue. If the Play Console still shows ANRs from the same code path, or other SAF-related ANRs, please reopen it or open a new issue with the new traces."

## Duplicates

**[#17744](https://github.com/cgeo/cgeo/issues/17744) Map shows all caches when no cache types are selected in filters**
- This is the same request as [#10963](https://github.com/cgeo/cgeo/issues/10963), "Hiding all caches on map viewer (quickly) is not possible". #10963 is older and has the longer discussion. A team member already pointed to it in the comments, and there is no implementation yet.
- Confidence: medium. #17744 also asks that the empty selection persist in the filter dialog, which fits the same concept.
- Closing comment: "Thanks for the report! This is the same topic as #10963 (hiding all caches via filter / how an empty cache type selection should behave). To keep the discussion in one place I'm closing this as a duplicate. Please add your points, including the persistence of the empty selection, to #10963."

## Waiting for information

**[#16744](https://github.com/cgeo/cgeo/issues/16744) No proximity alert for Final?**
- On 2025-12-20 the maintainer explained how the notifications work (general vs. specific, minimum intervals, suppression when moving away) and asked "Does that work for you?". There has been no reply in about 11 months. Nobody else could reproduce the problem.
- Confidence: medium.
- Closing comment: "We couldn't reproduce this, and we haven't heard back since our explanation of how general and specific proximity notifications work (last question on 2025-12-20). I'm closing this for now. If it still happens with a current version, please reopen it with your notification settings and the type of map you use."

**[#17739](https://github.com/cgeo/cgeo/issues/17739) Unexpected result when sorting a search result**
- On 2026-02-10 a team member asked the reporter whether "223 caches" in the expected result was a typo. The reporter has not replied in over 9 months, and the expected behaviour is still unclear.
- Confidence: medium-low.
- Closing comment: "We asked for clarification on the expected result (2026-02-10) and haven't received an answer, so I'm closing this for now. If you still see the result list change after sorting in a current version, please reopen it or comment with the exact steps and the number of caches before and after."

## Keep open

[#16797](https://github.com/cgeo/cgeo/issues/16797) (second part, converting a GPX route, is not implemented), [#16971](https://github.com/cgeo/cgeo/issues/16971), [#6575](https://github.com/cgeo/cgeo/issues/6575) (maintainers consider it unlikely, but it is not closed), [#15193](https://github.com/cgeo/cgeo/issues/15193), [#17541](https://github.com/cgeo/cgeo/issues/17541) (confirmed still present), [#9595](https://github.com/cgeo/cgeo/issues/9595), [#17322](https://github.com/cgeo/cgeo/issues/17322), [#17663](https://github.com/cgeo/cgeo/issues/17663), [#17283](https://github.com/cgeo/cgeo/issues/17283), [#17700](https://github.com/cgeo/cgeo/issues/17700) (no `activity-alias` in `main/AndroidManifest.xml` yet), [#17625](https://github.com/cgeo/cgeo/issues/17625), [#17579](https://github.com/cgeo/cgeo/issues/17579), [#17747](https://github.com/cgeo/cgeo/issues/17747), [#17737](https://github.com/cgeo/cgeo/issues/17737) (part 2 was fixed by #17728; part 1 is unresolved), [#17688](https://github.com/cgeo/cgeo/issues/17688) (the checkstyle.org firewall rule is open; worth a later look), [#17797](https://github.com/cgeo/cgeo/issues/17797), [#4875](https://github.com/cgeo/cgeo/issues/4875) (KML import is only a partial answer), [#17828](https://github.com/cgeo/cgeo/issues/17828), [#14038](https://github.com/cgeo/cgeo/issues/14038) (no HEIC conversion found in master), [#14302](https://github.com/cgeo/cgeo/issues/14302), [#17809](https://github.com/cgeo/cgeo/issues/17809) (`GeokretyConnector.java:420` still uses `cache.getCoords()`), [#17583](https://github.com/cgeo/cgeo/issues/17583), [#17714](https://github.com/cgeo/cgeo/issues/17714) (only a safeguard was added; the cause of the invalid coordinates is not analysed), [#17853](https://github.com/cgeo/cgeo/issues/17853), [#17857](https://github.com/cgeo/cgeo/issues/17857), [#17868](https://github.com/cgeo/cgeo/issues/17868) (GC-side problem, but c:geo could show a message instead)

## Pull requests of the probably fixed issues

Found by rules in the history of the code named above (the first commit that added it). A hint, not proof: check that the pull request really is the fix.

- [#17488](https://github.com/cgeo/cgeo/issues/17488): [PR #17521](https://github.com/cgeo/cgeo/pull/17521) "rel to \#17488: Log configuration on startup: avoid blocking main thread for file access", merged 2025-10-09, commit [7243b697e9](https://github.com/cgeo/cgeo/commit/7243b697e902f66bc015aa5e1e7780e819e5a5a8) of 2025-10-07, added `new Thread(Log::configureLogging).start()` in `main/src/main/java/cgeo/geocaching/utils/Log.java`.

```cleanup-result
#16744 waiting
#16797 keep-open
#16971 keep-open
#17488 fixed
#6575 keep-open
#15193 keep-open
#17541 keep-open
#9595 keep-open
#17322 keep-open
#17663 keep-open
#17283 keep-open
#17700 keep-open
#17625 keep-open
#17579 keep-open
#17744 duplicate
#17747 keep-open
#17737 keep-open
#17688 keep-open
#17797 keep-open
#4875 keep-open
#17828 keep-open
#14038 keep-open
#14302 keep-open
#17809 keep-open
#17583 keep-open
#17739 waiting
#17714 keep-open
#17853 keep-open
#17857 keep-open
#17868 keep-open
```
