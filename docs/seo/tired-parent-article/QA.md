# Article 04 verification

Pre-publication verification snapshot, 7 September 2026. Source fingerprints: `.omo/evidence/tired-parent-article/verified/source-sha256.json`. The checks below preceded the publication commit. Search-engine submission instructions are in INDEXING.md.

## Build and SEO

- `uv run scripts/build.py`: exit 0.
- `uv run scripts/check_site.py`: exit 0 after final French punctuation edit.
- `node scripts/check_locale_redirect.mjs`: exit 0; product JavaScript unchanged.
- `git diff --check`: exit 0.
- 14 complete localized files, exactly 89 keys each. Article structure contains five FAQ pairs; metadata, illustration caption and alt localized. No English fallback for new article-specific copy.
- Four cards per language index, reciprocal localized article links, 84 sitemap URLs, canonical and hreflang/Article JSON-LD validated. See BUILD-CONTENT-QA.md for the independent source-to-render audit.
- Biome/basedpyright LSP verification unavailable: language servers are not installed and prior installation was declined. No installation performed.

## Browser surface

`verified/captures.json` enumerates all 210 affected route/width cases: 14 new articles, 14 indexes, 42 existing article source/link blocks, each at 375/768/1280 CSS pixels. New article and index content captured with overlapping scroll positions; existing articles captured at the changed link block. Every case has zero horizontal page overflow. Full actual text rendering checked across Latin and Cyrillic scripts; no CJK locales are present.

Native CUA browser captures are JPEG, with correctly encoded PNG crops for review. Screenshots use the real same-origin generated page inside an iframe whose width determines its actual responsive layout. The 1280 layout is visually scaled to fit the native browser capture; it retains a 1280 CSS-pixel layout viewport. Files ending `-review.png` are stitched reading aids. Raw JPEGs and per-frame PNG crops are authoritative; stitched sheets may retain repeated sticky-header/TOC strips at joins.

Browser screenshot tooling initially produced partial scaled composites and smooth-scroll stitching artifacts. Those stale attempts are outside `verified/` and were not used for the final approval. The replacement capture method checks settled scroll position and uses 100px frame overlap. A mass-navigation tab crashed once; captures resumed in a fresh tab with completed records preserved.

Direct-page interaction evidence in `verified/interactions.json`:

- All 14 language-menu transitions retained the corresponding article and correct html language.
- All five FAQs opened by click; Enter closed and reopened a disclosure.
- TOC voice link reached the intended fragment.
- Fourth index card opened the new article.
- Recording-guide link and reciprocal return link worked.
- Product CTA reached the local homepage #how section.

Fresh direct-page console check returned no errors/warnings on a script-free control and on the new article after a language switch (`console-fresh-tab.json`). Earlier mass-navigation observer errors without source URLs are preserved in `console.json`; product scripts contain no MutationObserver. Their exact tooling source is unconfirmed, and no website JavaScript fix is claimed.

## Independent review

Pass A approved real semantic DOM, design tokens, responsive guide primitives, native controls, illustration handling and all 210 cases. Initial Pass B found one French mobile punctuation wrap: a question mark could begin a new line. French question/exclamation/semicolon spacing now uses narrow nonbreaking spaces, with nonbreaking colon/guillemet spacing. All 15 affected French route/width cases were recaptured after the correction; other 195 cases correspond to unchanged rendered sources.

Final independent visual verdict: PASS, high confidence, no blocking findings. Reviewer `article_final_visual_review` inspected all 15 overview sheets, all 14 complete mobile articles, relevant tablet/desktop frames, final French punctuation, interaction evidence and applicable source freshness. Pass A reviewer: `article_design_review`, PASS. Initial Pass B reviewer: `article_visual_review`, REVISE for French punctuation; this finding is resolved in the final pass. These verdicts cover the source fingerprints recorded above.

## Scope limits

These captures cover the current system dark theme at the three named widths. Alternate OS theme, 200% text resizing, Lighthouse/Core Web Vitals and external Google indexing were not measured. An unchanged old Dutch recording-guide hero has an intrinsic heading-width flag (351px inside 339px) without page overflow; this task's changed source-link block is clear. No full audit or fix of unrelated existing hero typography is claimed. Native-speaker certification and Google regional keyword volumes are not claimed.

Temporary QA frame/control pages are excluded from the production source and removed from dist before handoff. The local preview server remains available for reviewing the article.
