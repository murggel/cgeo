<!-- task: cleanup-issues | upstream: cgeo/cgeo@428a9dad765cf3c240eb11bbd92e32a50a059624 | issue snapshot: 2026-11-15 | provider: copilot 1.0.105 | workflow: a5c14a752cf5960eda490699f8be006d1ae9ea31 -->

## Summary
I checked 20 issues. None can be closed with enough evidence, so all 20 stay open. That means no fixed, duplicate, obsolete or waiting issues.

## Keep open
[#4839](https://github.com/cgeo/cgeo/issues/4839), [#4872](https://github.com/cgeo/cgeo/issues/4872), [#5009](https://github.com/cgeo/cgeo/issues/5009), [#5011](https://github.com/cgeo/cgeo/issues/5011), [#3273](https://github.com/cgeo/cgeo/issues/3273), [#5122](https://github.com/cgeo/cgeo/issues/5122), [#5154](https://github.com/cgeo/cgeo/issues/5154), [#5165](https://github.com/cgeo/cgeo/issues/5165), [#4822](https://github.com/cgeo/cgeo/issues/4822), [#5207](https://github.com/cgeo/cgeo/issues/5207), [#5176](https://github.com/cgeo/cgeo/issues/5176), [#5237](https://github.com/cgeo/cgeo/issues/5237), [#5341](https://github.com/cgeo/cgeo/issues/5341), [#5404](https://github.com/cgeo/cgeo/issues/5404), [#4672](https://github.com/cgeo/cgeo/issues/4672), [#5736](https://github.com/cgeo/cgeo/issues/5736), [#5856](https://github.com/cgeo/cgeo/issues/5856), [#5853](https://github.com/cgeo/cgeo/issues/5853), [#5894](https://github.com/cgeo/cgeo/issues/5894), [#5212](https://github.com/cgeo/cgeo/issues/5212)

Reasons for the ones that came closest to being closed:
- [#5736](https://github.com/cgeo/cgeo/issues/5736): `LogCacheActivity.java:188` still passes `null` for the time view. Only trackable logs have a time editor (`LogTrackableActivity.java:139`, `:276`). The newer [#12991](https://github.com/cgeo/cgeo/issues/12991) asks for a related feature, but it is newer than #5736, so it is not a reason to close #5736.
- [#5176](https://github.com/cgeo/cgeo/issues/5176): the newer [#7922](https://github.com/cgeo/cgeo/issues/7922) and [#4360](https://github.com/cgeo/cgeo/issues/4360) are related requests, not exact duplicates.
- [#5237](https://github.com/cgeo/cgeo/issues/5237): `CacheDetailActivity.java:1401-1409` shows only one name, the "placed by" name, and falls back to the owner's user ID only if that is blank. The request is still open.
- [#4839](https://github.com/cgeo/cgeo/issues/4839): `TrackableActivity.java:411` shows `trackable.getImages()`. `GCParser.java:1380` appears to fill that list only from the featured image pattern, so I could not confirm the gallery is covered.
- [#5122](https://github.com/cgeo/cgeo/issues/5122): `AndroidManifest.xml` has `allowBackup` and a custom `CentralBackupAgent`, but no `fullBackupContent` rules. It is unclear whether this meets the request.
- [#5011](https://github.com/cgeo/cgeo/issues/5011): the `ACTION_SEND_MULTIPLE` use I found (`CacheListActivity.java:1814`) is for pocket query downloads, not for sharing several cache codes.
- [#4822](https://github.com/cgeo/cgeo/issues/4822), [#4672](https://github.com/cgeo/cgeo/issues/4672), [#5341](https://github.com/cgeo/cgeo/issues/5341) and [#5894](https://github.com/cgeo/cgeo/issues/5894) carry the "Feedback required" label, which means developer feedback, so it does not make them "waiting". The last comment on each also dates from 2016 or earlier and asks no question of the reporter.

```cleanup-result
#4839 keep-open
#4872 keep-open
#5009 keep-open
#5011 keep-open
#3273 keep-open
#5122 keep-open
#5154 keep-open
#5165 keep-open
#4822 keep-open
#5207 keep-open
#5176 keep-open
#5237 keep-open
#5341 keep-open
#5404 keep-open
#4672 keep-open
#5736 keep-open
#5856 keep-open
#5853 keep-open
#5894 keep-open
#5212 keep-open
```
