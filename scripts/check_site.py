#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run scripts/check_site.py [OUTPUT_DIR]
# 3. Or make executable and run:
#      chmod +x scripts/check_site.py && ./scripts/check_site.py [OUTPUT_DIR]
# ──────────────────

from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


LOCALES = (
    "en",
    "ru",
    "de",
    "uk",
    "pl",
    "sr",
    "fr",
    "es",
    "it",
    "pt",
    "nl",
    "cs",
    "ro",
    "tr",
)
SITE_URL = "https://sleep2story.com"
ARTICLE_PATHS = {
    "en": "/guides/how-to-record-bedtime-stories/",
    "ru": "/ru/guides/kak-zapisat-skazku-na-noch/",
    "de": "/de/ratgeber/gute-nacht-geschichten-aufnehmen/",
    "uk": "/uk/porady/yak-zapysaty-kazku-na-nich/",
    "pl": "/pl/poradniki/jak-nagrac-bajke-na-dobranoc/",
    "sr": "/sr/vodici/kako-snimiti-pricu-za-laku-noc/",
    "fr": "/fr/guides/enregistrer-une-histoire-du-soir/",
    "es": "/es/guias/grabar-cuentos-para-dormir/",
    "it": "/it/guide/registrare-storie-della-buonanotte/",
    "pt": "/pt/guias/gravar-historias-para-dormir/",
    "nl": "/nl/gidsen/verhaaltje-voor-het-slapengaan-opnemen/",
    "cs": "/cs/pruvodce/jak-nahrat-pohadku-na-dobrou-noc/",
    "ro": "/ro/ghiduri/inregistrare-povesti-de-seara/",
    "tr": "/tr/rehber/uyku-masali-nasil-kaydedilir/",
}


def locale_path(locale: str) -> str:
    return "/" if locale == "en" else f"/{locale}/"


@dataclass(slots=True)  # noqa: MUTABLE_OK
class PageFacts:
    """Mutable accumulator populated by the streaming HTML parser."""

    language: str = ""
    title: str = ""
    description: str = ""
    canonical: str = ""
    og_image: str = ""
    hreflang: dict[str, str] = field(default_factory=dict)
    links: list[tuple[str, str]] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)
    _in_title: bool = False


class FactsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.facts = PageFacts()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.facts.language = values.get("lang", "")
        if tag == "title":
            self.facts._in_title = True
        if tag == "meta" and values.get("name") == "description":
            self.facts.description = values.get("content", "")
        if tag == "meta" and values.get("property") == "og:image":
            self.facts.og_image = values.get("content", "")
        if tag == "link" and values.get("rel") == "canonical":
            self.facts.canonical = values.get("href", "")
        if tag == "link" and values.get("rel") == "alternate" and values.get("hreflang"):
            self.facts.hreflang[values["hreflang"]] = values.get("href", "")
        if tag == "a" and values.get("href"):
            self.facts.links.append((values["href"], values.get("data-locale", "")))
        if tag in {"img", "script"} and values.get("src"):
            self.facts.resources.append(values["src"])
        if tag == "img" and values.get("srcset"):
            self.facts.resources.extend(
                candidate.strip().split()[0]
                for candidate in values["srcset"].split(",")
            )
        if tag == "link" and values.get("rel") in {"icon", "apple-touch-icon", "manifest", "preload"}:
            self.facts.resources.append(values.get("href", ""))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.facts._in_title = False

    def handle_data(self, data: str) -> None:
        if self.facts._in_title:
            self.facts.title += data


def parse_page(path: Path) -> PageFacts:
    parser = FactsParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.facts


def local_path(output: Path, url: str) -> Path | None:
    parts = urlsplit(url)
    if parts.netloc and parts.netloc != "sleep2story.com":
        return None
    path = parts.path
    if not path.startswith("/"):
        return None
    target = output / path.lstrip("/")
    return target / "index.html" if path.endswith("/") else target


def assert_local_targets(output: Path, facts: PageFacts) -> None:
    for url in [*(href for href, _ in facts.links), *facts.resources, facts.og_image]:
        target = local_path(output, url)
        if target is not None:
            assert target.is_file(), f"Broken local target: {url}"


def check(output: Path) -> None:
    expected_alternates = {
        **{locale: f"{SITE_URL}{locale_path(locale)}" for locale in LOCALES},
        "x-default": f"{SITE_URL}/",
    }
    expected_locale_links = {locale: locale_path(locale) for locale in LOCALES}

    for locale in LOCALES:
        route = locale_path(locale)
        page_path = output / "index.html" if locale == "en" else output / locale / "index.html"
        assert page_path.is_file(), f"Missing route {route}"
        source = page_path.read_text(encoding="utf-8")
        assert "{{" not in source, f"Unresolved template token in {route}"
        assert source.count('class="ticker__group"') == 2, f"Ticker loop is not duplicated in {route}"
        assert source.count('class="ticker__item"') == 8, f"Ticker does not fill wide screens in {route}"

        facts = parse_page(page_path)
        assert facts.language == locale
        assert facts.title.strip()
        assert facts.description.strip()
        assert facts.canonical == f"{SITE_URL}{route}"
        assert facts.og_image == f"{SITE_URL}/assets/og-{locale}.jpg"
        assert facts.hreflang == expected_alternates
        assert {
            switched_locale: href
            for href, switched_locale in facts.links
            if switched_locale
        } == expected_locale_links
        assert (f"{route}#how", "") in facts.links
        assert (ARTICLE_PATHS[locale], "") in facts.links
        assert all(
            href == ARTICLE_PATHS[locale] or href.startswith(f"{route}#")
            for href, switched_locale in facts.links
            if href.startswith("/") and not switched_locale
        )
        assert_local_targets(output, facts)

    english_redirect = (output / "en" / "index.html").read_text(encoding="utf-8")
    assert 'name="robots" content="noindex"' in english_redirect
    assert 'rel="canonical" href="https://sleep2story.com/"' in english_redirect

    article_alternates = {
        **{locale: f"{SITE_URL}{path}" for locale, path in ARTICLE_PATHS.items()},
        "x-default": f"{SITE_URL}{ARTICLE_PATHS['en']}",
    }
    article_titles: set[str] = set()
    for locale, route in ARTICLE_PATHS.items():
        article_path = output / route.lstrip("/") / "index.html"
        assert article_path.is_file(), f"Missing route {route}"
        article_source = article_path.read_text(encoding="utf-8")
        article_facts = parse_page(article_path)
        assert "{{" not in article_source
        assert article_facts.language == locale
        assert article_facts.title.strip()
        assert article_facts.title not in article_titles, f"Untranslated article title in {locale}"
        article_titles.add(article_facts.title)
        assert article_facts.description.strip()
        assert article_facts.canonical == f"{SITE_URL}{route}"
        assert article_facts.hreflang == article_alternates
        assert article_facts.og_image == f"{SITE_URL}/assets/og-{locale}.jpg"
        assert {
            switched_locale: href
            for href, switched_locale in article_facts.links
            if switched_locale
        } == ARTICLE_PATHS
        assert '"@type": "Article"' in article_source
        assert f'"inLanguage": "{locale}"' in article_source
        assert '"datePublished": "2026-09-02"' in article_source
        assert (f"{locale_path(locale)}#how", "") in article_facts.links
        assert_local_targets(output, article_facts)

    sitemap = ET.parse(output / "sitemap.xml").getroot()
    namespace = {
        "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "xhtml": "http://www.w3.org/1999/xhtml",
    }
    urls = {node.text for node in sitemap.findall("s:url/s:loc", namespace)}
    assert urls == {
        *(f"{SITE_URL}{locale_path(locale)}" for locale in LOCALES),
        *(f"{SITE_URL}{route}" for route in ARTICLE_PATHS.values()),
    }
    for entry in sitemap.findall("s:url", namespace):
        location = entry.find("s:loc", namespace)
        assert location is not None
        alternates = {
            link.attrib["hreflang"]: link.attrib["href"]
            for link in entry.findall("xhtml:link", namespace)
        }
        expected = article_alternates if location.text in article_alternates.values() else expected_alternates
        assert alternates == expected

    for locale in LOCALES:
        manifest = output / f"site-{locale}.webmanifest"
        assert manifest.is_file(), f"Missing localized manifest for {locale}"


def main() -> None:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
    check(output)
    print(f"Site checks passed: {output}")


if __name__ == "__main__":
    main()
