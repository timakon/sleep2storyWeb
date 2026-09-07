# Tired-parent article illustration

Generated on 2026-09-07 using the built-in `image_gen` tool, in the `illustration-story` category. One image was generated; no fallback API, additional dependency, or generation script was used.

## Deliverables

| Asset | Intrinsic dimensions | File size |
|---|---|---|
| `assets/tired-parent-story.webp` | 1200 × 800 | 151,724 bytes |
| `assets/tired-parent-story-640.webp` | 640 × 427 | 48,346 bytes |

The original 1536 × 1024 PNG remains at:
`/Users/mac/.codex/generated_images/01a0791e-6baf-70c2-8e38-c8dcf9187b56/exec-2e74d05e-1a06-4e08-93ac-ca0e449172ff.png`.

## Prompt

```text
Use case: illustration-story.
Asset type: one editorial illustration for a tired-parent bedtime article on Sleep2Story, landscape 3:2, intended final size 1200 by 800 pixels.
Primary request: a quiet, ordinary parent sits beside a child about five years old tucked into bed, sharing an open book. A small bedside lamp gives a gentle candlelight glow. The parent looks softly tired but present, and the child is comfortable and restful. Make this a sympathetic, reassuring family moment.
Style/medium: warm literary family radio poster aesthetic, hand-drawn editorial printmaking / screenprint, flat warm colour shapes, expressive dark ink linework, modest detail and subtle paper/print texture. Natural, appealing anatomy and an uncluttered bedroom.
Composition/framing: landscape 3:2; give the figures, bed, open book and lamp room to breathe. The scene is the complete picture, not a user-interface or poster mockup. No border, no surrounding device, no title space that looks like missing lettering.
Color palette: warm paper #fff8f4, dark brown ink #211a13, muted moss #4c644e, candlelight amber #ffddb6, dusty rose #c09595; small accents in warm timber tones. Warm, calm and restrained, no cool blue or purple gradient.
Constraints: no text, lettering, typography, logos or watermarks anywhere, including the book. No medical symbols. No device held by the child. No dramatic exhaustion or distress, no glossy 3D rendering, no photorealism. Create exactly one image.
```

## Encoding and verification

Read `DESIGN.md` for the palette and literary family-radio style. Encoded the original directly into each WebP using the existing `cwebp` tool, quality 82, method 6, and `-resize 1200 0` / `-resize 640 0`. A zero height preserves aspect ratio, with the smaller output rounded to 427 pixels. No crop or stretch was applied.

Verified intrinsic dimensions with `sips` and file sizes with `stat`. Visually inspected the original and final 1200-pixel WebP: a calm parent and child with an open book and bedside lamp; warm moss, rose and amber print texture; legible composition at reduced size; no lettering, logo, medical symbol, or child-held device. The generated palette is predominantly amber-lit rather than an exact flat paper background.

Suggested alt text: “A parent sits beside a child in bed with an open book in the warm light of a bedside lamp.”
