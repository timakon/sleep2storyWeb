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


LOCALES = ("en", "ru", "de")
SITE_URL = "https://sleep2story.app"


@dataclass(slots=True)
class PageFacts:
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
    if parts.netloc and parts.netloc != "sleep2story.app":
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
        **{locale: f"{SITE_URL}/{locale}/" for locale in LOCALES},
        "x-default": f"{SITE_URL}/",
    }

    for locale in LOCALES:
        page_path = output / locale / "index.html"
        assert page_path.is_file(), f"Missing route /{locale}/"
        source = page_path.read_text(encoding="utf-8")
        assert "{{" not in source, f"Unresolved template token in /{locale}/"

        facts = parse_page(page_path)
        assert facts.language == locale
        assert facts.title.strip()
        assert facts.description.strip()
        assert facts.canonical == f"{SITE_URL}/{locale}/"
        assert facts.og_image == f"{SITE_URL}/assets/og-{locale}.jpg"
        assert facts.hreflang == expected_alternates
        assert (f"/{locale}/#how", "") in facts.links
        assert all(
            not href.startswith(f"/{other}/")
            for other in LOCALES
            if other != locale
            for href, switched_locale in facts.links
            if not switched_locale
        )
        assert_local_targets(output, facts)

    root_facts = parse_page(output / "index.html")
    assert root_facts.canonical == f"{SITE_URL}/"
    assert root_facts.hreflang == expected_alternates
    assert_local_targets(output, root_facts)

    sitemap = ET.parse(output / "sitemap.xml").getroot()
    namespace = {
        "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "xhtml": "http://www.w3.org/1999/xhtml",
    }
    urls = {node.text for node in sitemap.findall("s:url/s:loc", namespace)}
    assert urls == {f"{SITE_URL}/{locale}/" for locale in LOCALES}
    for entry in sitemap.findall("s:url", namespace):
        alternates = {
            link.attrib["hreflang"]: link.attrib["href"]
            for link in entry.findall("xhtml:link", namespace)
        }
        assert alternates == expected_alternates

    for locale in LOCALES:
        manifest = output / f"site-{locale}.webmanifest"
        assert manifest.is_file(), f"Missing localized manifest for {locale}"


def main() -> None:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
    check(output)
    print(f"Site checks passed: {output}")


if __name__ == "__main__":
    main()
