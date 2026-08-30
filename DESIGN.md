# Sleep2Story Web Design System

## 1. Atmosphere & Identity

Sleep2Story Web feels like a warm family radio poster: candid, literary, and reassuring rather than technical. The signature is the contrast between oversized broadcast typography and tilted, real product screens in candlelight amber, muted moss, dusty rose, and paper.

## 2. Color

| Role | Token | Light | Dark | Usage |
|---|---|---|---|---|
| Paper | `--paper` | `#fff8f4` | `#211a13` | Page surface |
| Paper low | `--paper-low` | `#fff1e5` | `#2d2721` | Secondary surface |
| Paper mid | `--paper-mid` | `#faebde` | `#372f27` | Cards and bands |
| Paper high | `--paper-high` | `#f4e6d9` | `#443b33` | Elevated tonal surface |
| Ink | `--ink` | `#211a13` | `#fdeee1` | Primary text and outlines |
| Muted | `--muted` | `#524435` | `#d7c3af` | Secondary text |
| Line | `--line` | `#d7c3af` | `#574a40` | Dividers and focus support |
| Amber | `--amber` | `#845400` | `#ffb95a` | Primary interactive accent |
| Amber bright | `--amber-bright` | `#d9901c` | `#d9901c` | Poster field |
| Amber soft | `--amber-soft` | `#ffddb6` | `#643f00` | Warm field |
| Moss | `--moss` | `#4c644e` | `#b3ceb2` | Calm secondary field |
| Moss soft | `--moss-soft` | `#ceeacd` | `#354c37` | Calm background |
| Rose | `--rose` | `#795555` | `#eabbbb` | Consent accent |
| Rose soft | `--rose-soft` | `#c09595` | `#5f3e3f` | Consent background |
| Error | `--error` | `#ba1a1a` | `#ffdad6` | Validation only |

Accent colors carry product meaning and interaction. No generic purple/blue SaaS gradient is introduced.

## 3. Typography

| Level | Size | Weight | Line height | Usage |
|---|---|---|---|---|
| Poster display | `clamp(4.5rem, 10vw, 9rem)` | 900 | 0.78–0.9 | Hero only |
| Section display | `clamp(2.75rem, 7vw, 6rem)` | 800–900 | 0.9–1 | Major sections |
| Card title | `1.5rem` | 800 | 1.1 | Tiles and FAQ |
| Lead | `1.25rem` | 650 | 1.5 | Hero support copy |
| Body | `1rem` | 400–650 | 1.55 | Default text |
| Label | `0.75rem` | 800 | 1.3 | Uppercase broadcast labels |

- Functional and body type: Inter, system-ui, sans-serif.
- Product wordmark: Fraunces, Georgia, serif.
- Expressive Cyrillic/Latin italic: Georgia, Times New Roman, serif.
- Body text never falls below 14px. German labels may wrap; controls expand rather than clip.

## 4. Spacing & Layout

- Base unit: 4px; existing spacing follows an 8px rhythm.
- Content width: 1320px maximum with fluid side gutters.
- Breakpoints: 520px, 820px, 1100px.
- Desktop hero uses a two-column poster split; tablet and mobile reflow to one column.
- Touch targets are at least 44px. At 200% text size, navigation may wrap or collapse without horizontal overflow.

## 5. Components

### Site header

- Structure: brand link, primary section links, locale switcher, FAQ link.
- States: default, hover, active, visible keyboard focus.
- Accessibility: labelled navigation, decorative icon has empty alt, links remain reachable at 200% zoom.
- Layout: sticky cluster on desktop; compact cluster on mobile.

### Button link

- Structure: descriptive anchor text plus optional decorative arrow.
- Variants: ink primary, paper secondary.
- States: default, hover/focus translate, active reset.
- Accessibility: visible `:focus-visible`, at least 44px high, no icon-only action.
- Motion: transform only, disabled under reduced motion.

### Poster tile

- Structure: number, heading, body.
- Variants: amber, moss, rose.
- Accessibility: semantic ordered list; color never carries meaning alone.

### Product screen

- Structure: real screenshot, localized alt text, localized caption where present.
- Accessibility: fixed intrinsic dimensions prevent layout shift. Screenshot language is stated when it differs from page language.
- Layout: cropped phone frame; never used as a fake replacement for interactive controls.

### FAQ disclosure

- Structure: native `details` and `summary`.
- States: closed, open, hover, keyboard focus.
- Accessibility: native keyboard and screen-reader behavior; answer immediately follows its question.

### Locale switcher

- Structure: links to equivalent locale routes.
- States: current locale marked with `aria-current`, hover, focus.
- Accessibility: native language names and a localized group label.
- Behavior: selection is remembered locally; no automatic redirect is allowed.

## 6. Motion & Interaction

| Type | Duration | Easing | Usage |
|---|---|---|---|
| Micro | 180ms | ease | Link/button affordance |
| Ticker | 24s | linear | Broadcast strip only |

Only transform and opacity animate. `prefers-reduced-motion` disables smooth scrolling, ticker motion, and transitions.

## 7. Depth & Surface

Strategy: mixed tonal fields plus one strong ink outline. Product screens may use a soft shadow to read as physical devices; content tiles use flat poster fields and borders rather than generic floating cards.

## 8. Accessibility Constraints & Accepted Debt

### Constraints

- WCAG 2.2 AA target: 4.5:1 body contrast, 3:1 large text, visible focus, semantic landmarks, keyboard reachability, reduced-motion support.
- Validate at 375px, 768px, and 1280px; repeat at 200% text size.
- English, Russian, and German content must not clip, truncate, or create horizontal page overflow.
- System dark mode must preserve hierarchy and contrast.

### Accepted Debt

| Item | Location | Why accepted | Owner / Exit |
|---|---|---|---|
| Product screenshots are available only in English | Localized landing pages | Mobile currently supports English and Russian, not German; fabricating a German app UI would misrepresent the product | Add real locale screenshots after Mobile ships the matching locale |
| Formal legal documents and German Impressum are absent | Footer / legal routes | Backend contains URL contracts but no approved legal text or operator identity | Product owner supplies approved documents and legal entity details before public launch |
