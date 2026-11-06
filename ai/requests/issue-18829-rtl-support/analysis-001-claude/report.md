<!-- task: analyze-issue | upstream: cgeo/cgeo@fead335324331ba1e6a11d4c9a32396e54ebff02 | issue: #18829 | provider: claude | workflow: 46642f1656b8d9dd0518f31a50e625be92f1e666 -->

# Issue #18829: RTL layout support (list-selection dialog invisible with he_IL)

## 1. Issue summary
- On a Samsung A33 with Android 16 and system language Hebrew (`he_IL`), the "Pick a list" dialog shows no list names. Only the selection circles are visible at the left edge, with a large dark area and tall rows.
- The reporter says the rest of the app looks normal. Their AI-assisted analysis (comments 1–3) generalises this to "RTL support is incomplete", and also suspects wrong "system locale" detection. They raise a policy question: for an unsupported RTL system language, keep the system layout direction or force English.
- JakeDot (comment 4) asks whether `dir="rtl"` is supported in listing content. I haven't investigated that.
- I couldn't view the screenshot, so the visual symptoms come from the text only.

## 2. Relevant c:geo components
- **Dialog entry point:** `StoredList.UserInterface.promptForListSelection(...)` in `main/src/main/java/cgeo/geocaching/list/StoredList.java:164`. It builds a `SimpleDialog.ItemSelectModel` with `SINGLE_PLAIN` or `SINGLE_HIGHLIGHT` choice mode, and `configureListDisplay` (line 192) supplies text, icon and grouping. The title is `R.string.list_title` ("Pick a list", `values/strings.xml:640`). Hebrew has a translation, `values-iw/strings.xml:278`.
- **Row layout:** `main/src/main/res/layout/simpleitemlist_item_view.xml`. This is the likely culprit (see section 3).
- **Locale handling:**
  - `Settings.getApplicationLocale()` (`Settings.java:2279`) returns `new Locale(lang, "")` if the user picked a language. Otherwise it returns `Locale.getDefault()`.
  - `AbstractActivity.attachBaseContext` (`AbstractActivity.java:148-155`) applies that locale with `configuration.setLocale(locale)`.
  - `MainActivity.java:500-501` compares the resources' locale with the desired one.
- **Manifest:** `android:supportsRtl="true"` (`AndroidManifest.xml:58`). RTL mirroring is therefore active.
- **Wider scale:** a grep for `Left|Right|paddingStart|marginStart|layout_alignParent|layout_toLeftOf|layout_toRightOf` finds 580 matches across 107 layout files. Most layouts use absolute left/right attributes, not start/end.

## 3. Technical analysis
**Facts (verified in source):**
- `supportsRtl=true` is set.
- `simpleitemlist_item_view.xml` is a `RelativeLayout` built entirely from absolute `Left`/`Right` attributes:
  - `alignParentLeft`, `toRightOf`, `toLeftOf`, `alignParentRight`, `marginRight`.
  - `gravity="left|center_vertical"` on the content anchor (line 73).
- The content anchor (`item_view_anchor`, lines 65-82) is `wrap_content`. It is positioned `toRightOf item_icon` and `toLeftOf item_action`. `item_action` is `toLeftOf item_groupToggle`, which is `toLeftOf item_rightAnchor`.
- `getApplicationLocale()` falls back to `Locale.getDefault()`. It does not check whether the app has translations for that locale.

**Hypotheses (not verified, since I can't run the app):**
- Under RTL, the `RelativeLayout` rules and the mixed absolute/relative attributes resolve inconsistently. The item content could be squeezed to zero width or pushed off-screen, leaving only the checker visible. That would match "only circles at the left edge", though that placement is odd for an RTL layout. The extra row height may come from the content view being laid out against the wrong anchors. I haven't confirmed the exact mechanism.
- Where the list names are rendered (`item_view_anchor` is a `LinearLayout` that receives an inflated view) is not traced. The failure could be in that code, or in the Hebrew text direction and alignment of the `TextParam`.
- A second possibility is that the failure comes from the mix of `Left` and `Right` in the nested `RelativeLayout`s, not from locale detection. The reporter's "wrong locale / deprecated API" claim is **not supported by the code I read**. `Locale.getDefault()` is a normal API, and the Hebrew string exists (`values-iw`). The locale concern looks separate from the visible bug.
- Android reports Hebrew as `he`, but the resource folder is `values-iw`. `Locale(...)` mapping of `he`↔`iw` is a possible area to check, but I haven't confirmed any problem there.

## 4. Possible solution
**Minimal fix for the reported bug:**
1. Convert `simpleitemlist_item_view.xml` to start/end attributes:
   - `alignParentStart`/`alignParentEnd`
   - `toEndOf`/`toStartOf`
   - `marginEnd`
   - `gravity="start|center_vertical"`
2. Alternatively, replace the `RelativeLayout` chain with a horizontal `LinearLayout` or `ConstraintLayout`. The "anchor so GONE visibility works" comments at lines 11 and 121 exist because of `RelativeLayout`.
3. Verify with a Hebrew or Arabic locale, or with the developer option "Force RTL layout direction". The latter reproduces this without changing the system language.

**Broader RTL consistency (the issue title):**
- Run an Android Lint pass with the `RtlHardcoded` and `RtlSymmetry` checks enabled.
- Migrate the other layouts gradually, starting with the commonly seen ones, such as `cacheslist_item.xml`, `logs_item.xml` and `cachedetail_details_page.xml`.

**Locale policy (open decision):**
- Option A: keep the system locale and layout direction, with a fallback to English strings. Android already falls back to default resources.
- Option B: force English plus LTR when the system language is unsupported.
- Option A needs no code change beyond layout fixes. B would need the locale to be validated in `Settings.getApplicationLocale()`.
- The Android per-app language APIs (`AppCompatDelegate.setApplicationLocales`, `LocaleListCompat`) are an alternative to the manual `attachBaseContext` configuration. They are a larger change and not needed for this bug.

## 5. Risks and tests
**Risks:**
- Changing attributes in a shared dialog row affects every `SimpleDialog` list in the app. In LTR, start/end are equivalent to left/right, so the risk is low, but visual regressions in groups, icons or action buttons are possible.
- The icons `expand_less` and `expand_more`, and directional drawables, may need `autoMirrored`.
- HTML or WebView listing content has its own direction handling (comment 4). It is out of scope for this fix.

**Tests:**
- **Manual:**
  - Open each dialog that uses `SimpleItemListModel`: list selection, multi-select with checkboxes, grouped lists with expand/collapse, and rows with an action button.
  - Run each in LTR, forced RTL, and with Hebrew and Arabic locales.
  - Test with different font and display sizes.
- **Automated:** there is no obvious unit-test target for XML layout. An instrumented or Robolectric inflate test with a forced layout direction could check that the content view has a non-zero width. I haven't checked whether such tests exist in the repo.

## 6. Open questions
- Which of the two locale policies (keep the system RTL direction, or force English) do the maintainers want? That is a product decision.
- The screenshot isn't visible to me. Does the failure show the list names missing everywhere in the dialog, or only for certain rows (for example grouped ones)? This would confirm the layout hypothesis.
- Is `dir="rtl"` for listing content in scope for this issue, or should it be tracked separately?
