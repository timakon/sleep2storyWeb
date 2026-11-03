"""Render social preview cards for the newly added site languages.

Run with the system Python that has Playwright installed, for example:
    python3 scripts/render_locale_og.py zh ar hi ja ko
"""

from __future__ import annotations

import argparse
import base64
from html import escape
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
NEW_LOCALES = ("zh", "ar", "hi", "ja", "ko")


def copy_for(locale: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in (ROOT / "site" / "locales" / f"{locale}.properties").read_text(encoding="utf-8").splitlines():
        if line:
            key, value = line.split("=", 1)
            values[key] = value.replace(r"\n", "\n")
    return values


def data_url(path: Path, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def markup(locale: str, copy: dict[str, str], icon_url: str, screen_url: str) -> str:
    lines = "<br>".join(
        escape(copy[f"hero.line{number}"]) if number < 3
        else f'<span class="last">{escape(copy[f"hero.line{number}"])}</span>'
        for number in (1, 2, 3)
    )
    direction = "rtl" if locale == "ar" else "ltr"
    return f"""<!doctype html>
<html lang="{locale}" dir="{direction}"><head><meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ width: 1200px; height: 630px; margin: 0; }}
body {{ color: #211a13; background: #fff8f4; font-family: system-ui, sans-serif; }}
.card {{ display: grid; grid-template-columns: 705px 495px; width: 1200px; height: 630px; border: 3px solid #211a13; overflow: hidden; }}
.copy {{ display: flex; flex-direction: column; padding: 54px 55px 46px; background: #ffddb6; }}
.brand {{ display: flex; align-items: center; gap: 13px; direction: ltr; width: fit-content; font: 700 25px Georgia, serif; }}
.brand img {{ width: 44px; height: 44px; border-radius: 10px; }}
.eyebrow {{ margin: 74px 0 16px; font-size: 18px; font-weight: 750; }}
h1 {{ margin: 0; font-size: 57px; line-height: 1.21; font-weight: 800; letter-spacing: 0; }}
h1 .last {{ color: #4c644e; }}
.lead {{ max-width: 590px; margin: auto 0 0; font-size: 19px; line-height: 1.5; }}
.art {{ position: relative; overflow: hidden; border-inline-start: 3px solid #211a13; background: #ceeacd; }}
.halo {{ position: absolute; width: 490px; height: 490px; top: 74px; left: 1px; border: 3px solid #211a13; border-radius: 50%; background: #faebde; }}
.phone {{ position: absolute; top: 31px; left: 145px; height: 565px; aspect-ratio: 1170 / 2532; padding: 7px; border: 6px solid #211a13; border-radius: 35px; background: #211a13; box-shadow: 15px 15px 0 #845400; transform: rotate(5deg); }}
.phone img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 20px; }}
.stamp {{ position: absolute; left: 25px; bottom: 38px; width: 153px; height: 153px; padding: 20px; display: grid; place-items: center; border: 3px solid #211a13; border-radius: 50%; background: #e1c0bf; text-align: center; font-size: 17px; font-weight: 800; line-height: 1.25; transform: rotate(-8deg); }}
html[dir="rtl"] .card {{ grid-template-columns: 495px 705px; }}
html[dir="rtl"] .copy {{ grid-column: 2; grid-row: 1; }}
html[dir="rtl"] .art {{ grid-column: 1; grid-row: 1; }}
html[dir="rtl"] .brand {{ align-self: end; }}
html[dir="rtl"] .eyebrow {{ margin-top: 62px; }}
html[dir="rtl"] h1 {{ font-size: 60px; line-height: 1.32; }}
html[dir="rtl"] .phone {{ transform: rotate(-5deg); }}
html[dir="rtl"] .art {{ border-inline-start: 0; border-inline-end: 3px solid #211a13; }}
</style></head>
<body><main class="card"><section class="copy">
<div class="brand"><img src="{icon_url}" alt="">Sleep2Story</div>
<p class="eyebrow">{escape(copy['hero.eyebrow'])}</p>
<h1>{lines}</h1>
<p class="lead">{escape(copy['hero.lead'])}</p>
</section><div class="art"><div class="halo"></div>
<div class="phone"><img src="{screen_url}" alt=""></div>
<div class="stamp">{escape(copy['stage.sticker']).replace(chr(10), '<br>')}</div>
</div></main></body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("locales", nargs="+", choices=NEW_LOCALES)
    locales = parser.parse_args().locales
    icon = data_url(ROOT / "assets" / "app-icon-512.png", "image/png")
    screen = data_url(ROOT / "assets" / "screens" / "tonight.webp", "image/webp")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for locale in locales:
            page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
            page.set_content(markup(locale, copy_for(locale), icon, screen))
            page.evaluate("document.fonts.ready")
            target = ROOT / "assets" / f"og-{locale}.jpg"
            page.screenshot(path=str(target), type="jpeg", quality=88)
            page.close()
            print(target)
        browser.close()


if __name__ == "__main__":
    main()
