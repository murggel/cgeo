<!-- upstream: cgeo/cgeo@1175ec20ac9ed1cd6f6f672315cd597b5685b730 | issue: #18837 | cli: 1.0.105 -->

# Analysis: #18837 — Logbook tab doesn't stop at top when scrolling up

## 1. Issue summary
In the cache Logbook tab, a fast, uninterrupted scroll from bottom to top doesn't stop at the top. It keeps scrolling through the logs. Per the comments:
- It's reproducible with GC3DMN4 (every time for UniQP) and GCAGXKA (moving-bits, on the 2026.10.18 release).
- It doesn't occur if the scroll is slow or paused, if all logs are expanded first, or if the last element is collapsed.
- The last element, which spans more than a page, must be unfolded.
- Log line limit is 15 and the cache is saved in a list.
- moving-bits couldn't reproduce it on one device.

## 2. Relevant components (verified)
- `main/src/main/java/cgeo/geocaching/log/LogsViewCreator.java`
  - `setContent()` (~l.88) sets a `LinearLayoutManager` and `LogEntryAdapter`.
  - `fillViewHolder()` calls `holder.binding.log.setExpanded(...)` and then `setText(...)`.
- `main/src/main/java/cgeo/geocaching/ui/ExpandableTextView.java`
  - `onTextChanged()` does `post(() -> { lineCount = getLineCount(); isCollapsible=...; setCollapse(...) })`.
  - `setCollapse()` changes `maxLines`.
- `main/src/main/res/layout/logs_page.xml`: `RecyclerViewWithHeader` with `layout_height="fill_parent"`, `fastScrollEnabled=false`, `nestedScrollingEnabled=true`. The `LinearLayout` parent uses `wrap_content` height.
- `main/src/main/res/layout/logs_item.xml`: item root is `wrap_content`, and the `ExpandableTextView` is `wrap_content`.
- `main/src/main/java/cgeo/geocaching/ui/recyclerview/RecyclerViewWithHeader.java`: header-wrapping adapter. I found nothing suspicious in it.
- `CacheDetailActivity` instantiates `CacheLogsViewCreator` at ~l.2759.

## 3. Technical analysis
**Facts**
- Each item is first bound with the text at `maxLines = Integer.MAX_VALUE` (constructor default) or with a stale value from a recycled holder.
- Collapsing happens later, in a `post()` after text change, once the line count is known. So item heights change after layout and after the item has already been scrolled into view.
- `expandedByLog` is keyed by log identity. `setExpanded()` is applied before `setText`, so the state itself looks consistent.
- Fast scroll is disabled, so the reported symptom isn't the old fast-scroll bug (#18653/#18657) from the comments. I did not verify those issues.

**Hypothesis (unverified, I can't run it)**
- During a fling upward, items entering from the top are measured at full, uncollapsed height. They then shrink on the posted collapse. RecyclerView's scroll offsets and fling are computed against changing item heights, and a very tall expanded item (more than a page) amplifies this.
- Result: the fling's scroll extent is never consumed at position 0 and appears to run on, or the content shifts under the fling.
- This fits the observations: slow scrolling lets layout settle, collapsed last item avoids the tall item, and "expand all" removes the post-bind height change.
- The "last element" mention suggests the tall expanded item is the one at the bottom, whose scroll-from-bottom start state is unusual.
- Another candidate is the nested scrolling flag (`nestedScrollingEnabled=true`) combined with a `wrap_content` parent and a `fill_parent` RecyclerView, in a ViewPager inside a collapsing/scrolling activity. The fling may be handed to a nested parent. This is a weaker guess and untested.
- A device-specific component (not all devices reproduce it) points to overscroll and fling handling.

## 4. Possible solution
Minimal approach, in order of preference:
1. Make the collapse decision synchronous and deterministic during bind. Avoid height changes after layout, for example:
   - Compute collapsibility during bind and set `maxLines` immediately from `expandedByLog`.
   - Or use a layout-pre-draw/`ViewTreeObserver` step before the first draw rather than a `post`.
   - Set the initial `maxLines` to the line limit (collapsed) when not expanded, so the first measure uses the final height.
2. If that is insufficient, set `setOverScrollMode(OVER_SCROLL_NEVER)` and/or disable nested scrolling on the logs RecyclerView. Also consider a `RecyclerView` fling guard that stops at position 0 (`canScrollVertically(-1)`).
3. Alternatives: use `notifyItemChanged` on collapse state changes, or add `setHasFixedSize`/stable IDs. Neither addresses the late measurement.

## 5. Risks and tests
**Risks**
- Collapse/expand state could regress for recycled holders and for translation (`fillViewHolder` is re-called).
- The `getLineCount()` calculation requires layout, so a synchronous version must measure with a `StaticLayout` or pre-draw.
- Visual jumps when expanding.
- Trackable logs share `LogsViewCreator`.

**Tests**
- Instrumented/manual: a cache with several logs where the last one is tall and expanded, with line limit 15. Fling from bottom to top repeatedly and confirm it stops at the top. Also compare line limit 0.
- Check that expand state persists across scroll, translation and delete.
- Run on at least two devices, including one that reproduces it (GC3DMN4 or GCAGXKA).
- A pure unit test isn't practical for the layout behavior. A Robolectric/instrumented test of `ExpandableTextView` collapse state could be added.

## 6. Open questions
- What are the device models and Android versions that reproduce it? Is it vendor-specific?
- Does the issue reproduce in the release build as well as nightly? Comment 8 says yes (2026.10.18), but a regression point is unknown (git history not inspected).
- Does disabling `nestedScrollingEnabled` change the behavior? This needs experiment.

