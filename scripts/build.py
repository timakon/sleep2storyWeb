#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run scripts/build.py [OUTPUT_DIR]
# 3. Or make executable and run:
#      chmod +x scripts/build.py && ./scripts/build.py [OUTPUT_DIR]
# ──────────────────

from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
import shutil
import sys
from typing import Final


ROOT: Final = Path(__file__).resolve().parent.parent
SITE_URL: Final = "https://sleep2story.com"
LOCALES: Final = (
    "en", "ru", "de", "uk", "pl", "sr", "fr", "es", "it", "pt", "nl", "cs", "ro", "tr",
)
LOCALE_NAMES: Final = {
    "en": "English", "ru": "Русский", "de": "Deutsch", "uk": "Українська",
    "pl": "Polski", "sr": "Srpski", "fr": "Français", "es": "Español",
    "it": "Italiano", "pt": "Português", "nl": "Nederlands", "cs": "Čeština",
    "ro": "Română", "tr": "Türkçe",
}
OG_LOCALES: Final = {
    "en": "en_US", "ru": "ru_RU", "de": "de_DE", "uk": "uk_UA", "pl": "pl_PL",
    "sr": "sr_RS", "fr": "fr_FR", "es": "es_ES", "it": "it_IT", "pt": "pt_PT",
    "nl": "nl_NL", "cs": "cs_CZ", "ro": "ro_RO", "tr": "tr_TR",
}
NAV_LABELS: Final = {
    "en": "Primary navigation", "ru": "Основная навигация", "de": "Hauptnavigation",
    "uk": "Основна навігація", "pl": "Główna nawigacja", "sr": "Glavna navigacija",
    "fr": "Navigation principale", "es": "Navegación principal", "it": "Navigazione principale",
    "pt": "Navegação principal", "nl": "Hoofdnavigatie", "cs": "Hlavní navigace",
    "ro": "Navigare principală", "tr": "Ana gezinme",
}
TOKEN_PATTERN: Final = re.compile(r"{{([a-z0-9_.-]+)}}")


class BuildError(RuntimeError):
    pass


def load_copy(locale: str) -> dict[str, str]:
    values: dict[str, str] = {}
    path = ROOT / "site" / "locales" / f"{locale}.properties"
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        key, separator, value = line.partition("=")
        if not separator or not key:
            raise BuildError(f"Invalid translation at {path}:{line_number}")
        if key in values:
            raise BuildError(f"Duplicate translation key {key!r} at {path}:{line_number}")
        values[key] = value.replace(r"\n", "\n")
    return values


def locale_path(locale: str) -> str:
    return "/" if locale == "en" else f"/{locale}/"


def alternate_urls() -> dict[str, str]:
    return {
        **{locale: f"{SITE_URL}{locale_path(locale)}" for locale in LOCALES},
        "x-default": f"{SITE_URL}/",
    }


def hreflang_links() -> str:
    return "\n".join(
        f'    <link rel="alternate" hreflang="{language}" href="{url}" />'
        for language, url in alternate_urls().items()
    )


def locale_links(current: str) -> str:
    links: list[str] = []
    for locale in LOCALES:
        current_attribute = ' aria-current="page"' if locale == current else ""
        links.append(
            f'            <a href="{locale_path(locale)}" lang="{locale}" data-locale="{locale}"'
            f"{current_attribute}>{LOCALE_NAMES[locale]}</a>"
        )
    return "\n".join(links)


def structured_data(locale: str, copy: dict[str, str]) -> str:
    page_url = f"{SITE_URL}{locale_path(locale)}"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{page_url}#website",
                "url": page_url,
                "name": "Sleep2Story",
                "inLanguage": locale,
            },
            {
                "@type": "MobileApplication",
                "@id": f"{SITE_URL}/#app",
                "name": "Sleep2Story",
                "url": page_url,
                "applicationCategory": "LifestyleApplication",
                "operatingSystem": "iOS, Android",
                "inLanguage": ["en", "ru"],
                "description": copy["meta.og_description"],
            },
            {
                "@type": "FAQPage",
                "@id": f"{page_url}#faq",
                "inLanguage": locale,
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": copy[f"faq.{index}.question"],
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": copy[f"faq.{index}.answer"],
                        },
                    }
                    for index in range(1, 5)
                ],
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, indent=6)


def render(template: str, copy: dict[str, str], raw_values: dict[str, str]) -> str:
    rendered = template
    for key, value in raw_values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)

    missing: set[str] = set()

    def replace_token(match: re.Match[str]) -> str:
        key = match.group(1)
        value = copy.get(key)
        if value is None:
            missing.add(key)
            return match.group(0)
        return escape(value, quote=True)

    rendered = TOKEN_PATTERN.sub(replace_token, rendered)
    if missing:
        raise BuildError(f"Missing template keys: {', '.join(sorted(missing))}")
    return rendered


def write_sitemap(output: Path) -> None:
    alternates = "\n".join(
        f'    <xhtml:link rel="alternate" hreflang="{language}" href="{url}" />'
        for language, url in alternate_urls().items()
    )
    entries = "\n".join(
        f"  <url>\n    <loc>{SITE_URL}{locale_path(locale)}</loc>\n{alternates}\n  </url>"
        for locale in LOCALES
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
    (output / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def build(output: Path) -> None:
    copies = {locale: load_copy(locale) for locale in LOCALES}
    english_keys = set(copies["en"])
    for locale, copy in copies.items():
        if set(copy) != english_keys:
            missing = sorted(english_keys - set(copy))
            extra = sorted(set(copy) - english_keys)
            raise BuildError(f"Translation parity failed for {locale}: missing={missing}, extra={extra}")

    shutil.rmtree(output, ignore_errors=True)
    output.mkdir(parents=True)
    shutil.copytree(ROOT / "assets", output / "assets", dirs_exist_ok=True)
    shutil.copy2(ROOT / "favicon.ico", output / "favicon.ico")
    shutil.copy2(ROOT / "assets" / "site.js", output / "assets" / "site.js")
    for font_name in ("Inter.ttf", "Fraunces.ttf"):
        (output / "assets" / "fonts" / font_name).unlink(missing_ok=True)
    legacy_css = ROOT / "variants" / "variants.css"
    css_source = legacy_css.read_text(encoding="utf-8")
    css = css_source[: css_source.index("/* ─────────────────────────────\n   01 · BOOK SPREAD")]
    css += css_source[
        css_source.index("/* ─────────────────────────────\n   03 · FAMILY BROADCAST") :
        css_source.index("/* ─────────────────────────────\n   COMPARISON HUB")
    ]
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,])\s*", r"\1", css)
    css = css.strip()

    template = (ROOT / "site" / "home.template.html").read_text(encoding="utf-8")
    alternates = hreflang_links()
    for locale, copy in copies.items():
        route = locale_path(locale)
        locale_dir = output if locale == "en" else output / locale
        locale_dir.mkdir(parents=True, exist_ok=True)
        page = render(
            template,
            copy,
            {
                "locale": locale,
                "locale_path": route,
                "canonical_url": f"{SITE_URL}{route}",
                "hreflang_links": alternates,
                "locale_links": locale_links(locale),
                "locale_code": locale.upper(),
                "og_locale": OG_LOCALES[locale],
                "nav_label": NAV_LABELS[locale],
                "stage_sticker": escape(copy["stage.sticker"]).replace("\n", "<br />"),
                "styles": css,
                "structured_data": structured_data(locale, copy),
            },
        )
        (locale_dir / "index.html").write_text(page, encoding="utf-8")
        manifest = {
            "name": "Sleep2Story",
            "short_name": "Sleep2Story",
            "description": copy["manifest.description"],
            "lang": locale,
            "start_url": route,
            "display": "standalone",
            "background_color": "#fff8f4",
            "theme_color": "#fff8f4",
            "icons": [
                {
                    "src": "/assets/app-icon-512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                }
            ],
        }
        (output / f"site-{locale}.webmanifest").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    english_redirect = output / "en"
    english_redirect.mkdir()
    (english_redirect / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="robots" content="noindex"><link rel="canonical" href="https://sleep2story.com/">'
        '<meta http-equiv="refresh" content="0;url=/"><title>Sleep2Story</title></head>'
        '<body><a href="/">Continue to Sleep2Story</a></body></html>\n',
        encoding="utf-8",
    )
    (output / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )
    write_sitemap(output)


def main() -> None:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    build(output.resolve())
    print(f"Built localized site: {output}")


if __name__ == "__main__":
    main()
