# Tired-parent article: build and content QA

Audit date: 7 September 2026. Result: **PASS; no remaining build/content blockers found.** Read-only inspection covered the final `dist/` build and source files. Browser/visual QA belongs to the parent task.

## Rendering and localization

- All 14 locales (`en`, `ru`, `de`, `uk`, `pl`, `sr`, `fr`, `es`, `it`, `pt`, `nl`, `cs`, `ro`, `tr`) have the same 89 nonempty override keys. The existing loader reported no duplicate or missing keys.
- Every built article contains all 88 override values used directly by the new template. The remaining override, `schema.description`, matches the parsed Article JSON-LD description. No unresolved template tokens remain.
- The template consumes 103 copy keys: 88 article overrides and 15 shared localized values. The inherited values were inspected: navigation/accessibility labels, author, short-answer/FAQ labels, footer text, guide-index link label, brand OG-image alt, and product screenshot alt/caption. None contains inherited recording-guide instructions or article-specific headings. All article paragraphs, FAQ answers, metadata and new-illustration descriptions come from the new locale files.
- A first audit caught stale Polish `meta.description` and `answer.title` output. The parent rebuilt after localization settled. The complete subsequent pass found zero mismatches, including the final Russian and German product-heading edits.

## Structure and SEO

- All 14 new pages have one H1, unique element IDs and ten valid local fragment links each.
- Canonical URL, OG URL/locale/title/description, Article JSON-LD headline/description/language/canonical, and publication/modification date `2026-09-07` match their locale inputs.
- Each new article has the complete 14-language alternate set plus English `x-default`; language-switcher links remain within the same article.
- All 14 indexes show four guide cards. Independently parsed CollectionPage/ItemList graphs contain exactly four items and the four correct localized guide URLs.
- Each new article links to the three earlier guides; all 42 earlier localized articles link back to their localized new guide.
- Sitemap validation passes with exactly 84 entries and the appropriate complete alternate set for every page. Existing local-resource, favicon, manifest and redirect checks pass.

## Images

Native `sips` inspection confirmed these dimensions. SHA-256 comparison confirmed all 18 related image files in `dist/assets/` match the inspected source files.

| Asset | Dimensions |
| --- | --- |
| `tired-parent-story.webp` | 1200 × 800 |
| `tired-parent-story-640.webp` | 640 × 427 |
| `screens/tonight.webp` | 1170 × 2532 |
| `screens/tonight-520.webp` | 520 × 1126 |
| All 14 localized `og-*.jpg` files | 1200 × 630 |

The full-size image dimensions and responsive width descriptors match the HTML. Localized illustration alt/caption values render; screenshot labels identify the existing English product preview.

## Python review and checks

The diff is confined to catalog/routes, per-entry template selection, four raw cross-link paths, and structural checks. Every catalog consumer now unpacks four fields. The first three entries retain their previous template and locale merge behavior; the fourth selects `tired-parents.html`. No new dependency or abstraction was introduced.

Passed: `uv run scripts/check_site.py`, `node scripts/check_locale_redirect.mjs`, `git diff --check`, Python compilation, and the independent content/JSON-LD/index/image checks described above. The pre-integration structural check was observed failing because the old index had three guides.

Limitations: basedpyright/Biome are unavailable. The programming audit flags only the existing oversized `build.py`, now 257 versus 255 pure LOC; no broad refactor was attempted. This pass checks rendered input provenance and structure, not native-speaker certification, search demand or live deployment. The parent's temporary `dist/qa-frame.html` browser fixture is outside product source and must be removed before publishing.
