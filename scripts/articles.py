from __future__ import annotations

from html import escape
import json
from types import MappingProxyType
from typing import Final, Mapping, Sequence


ARTICLE_PATHS: Final[Mapping[str, str]] = MappingProxyType({
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
})
GRANDPARENT_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "en": "/guides/grandparents-record-stories-for-grandchildren/",
    "ru": "/ru/guides/babushka-dedushka-zapisat-skazku-dlya-vnukov/",
    "de": "/de/ratgeber/oma-opa-gute-nacht-geschichte-fuer-enkel-aufnehmen/",
    "uk": "/uk/porady/babusia-didus-zapysaty-kazku-dlia-onukiv/",
    "pl": "/pl/poradniki/babcia-dziadek-nagrac-bajke-dla-wnukow/",
    "sr": "/sr/vodici/baka-deka-snimiti-pricu-za-unuke/",
    "fr": "/fr/guides/grands-parents-enregistrer-histoire-petits-enfants/",
    "es": "/es/guias/abuelos-grabar-cuentos-para-nietos/",
    "it": "/it/guide/nonni-registrare-storie-per-nipoti/",
    "pt": "/pt/guias/avos-gravar-historias-para-netos/",
    "nl": "/nl/gidsen/opa-oma-verhaaltje-voor-kleinkind-opnemen/",
    "cs": "/cs/pruvodce/babicka-dedecek-nahrat-pohadku-pro-vnoucata/",
    "ro": "/ro/ghiduri/bunici-inregistreze-povesti-pentru-nepoti/",
    "tr": "/tr/rehber/buyukanne-dede-torunlar-icin-masal-kaydetme/",
})
ARTICLE_CATALOG: Final[tuple[tuple[str, Mapping[str, str]], ...]] = (
    ("article-locales", ARTICLE_PATHS),
    ("grandparent-article-locales", GRANDPARENT_PATHS),
)
SECTION_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    locale: path.rsplit("/", 2)[0] + "/" for locale, path in ARTICLE_PATHS.items()
})


def alternate_urls(
    site_url: str, paths: Mapping[str, str] = ARTICLE_PATHS,
) -> Mapping[str, str]:
    return MappingProxyType({
        **{locale: f"{site_url}{path}" for locale, path in paths.items()},
        "x-default": f"{site_url}{paths['en']}",
    })


def hreflang_links(site_url: str, paths: Mapping[str, str] = ARTICLE_PATHS) -> str:
    return "\n".join(
        f'    <link rel="alternate" hreflang="{locale}" href="{url}" />'
        for locale, url in alternate_urls(site_url, paths).items()
    )


def locale_links(
    current: str, names: Mapping[str, str], paths: Mapping[str, str] = ARTICLE_PATHS,
) -> str:
    links: list[str] = []
    for locale, path in paths.items():
        current_attribute = ' aria-current="page"' if locale == current else ""
        links.append(
            f'            <a href="{path}" lang="{locale}" data-locale="{locale}"'
            f"{current_attribute}>{escape(names[locale])}</a>"
        )
    return "\n".join(links)


def structured_data(
    site_url: str, locale: str, copy: Mapping[str, str], paths: Mapping[str, str],
) -> str:
    canonical = f"{site_url}{paths[locale]}"
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": copy["meta.og_title"],
        "description": copy["schema.description"],
        "image": f"{site_url}/assets/og-{locale}.jpg",
        "datePublished": "2026-09-02",
        "dateModified": "2026-09-02",
        "inLanguage": locale,
        "mainEntityOfPage": canonical,
        "author": {"@type": "Organization", "name": copy["byline.author"]},
        "publisher": {
            "@type": "Organization",
            "name": "Sleep2Story",
            "logo": {"@type": "ImageObject", "url": f"{site_url}/assets/app-icon-512.png"},
        },
    }
    return json.dumps(article, ensure_ascii=False, indent=6)


def section_structured_data(
    site_url: str,
    locale: str,
    copy: Mapping[str, str],
    articles: Sequence[tuple[Mapping[str, str], Mapping[str, str]]],
) -> str:
    canonical = f"{site_url}{SECTION_PATHS[locale]}"
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": copy["index.meta_title"],
        "description": copy["index.meta_description"],
        "url": canonical,
        "inLanguage": locale,
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(articles),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": position,
                    "url": f"{site_url}{paths[locale]}",
                    "name": article_copy["meta.og_title"],
                }
                for position, (article_copy, paths) in enumerate(articles, start=1)
            ],
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=6)


def sitemap_entries(site_url: str) -> str:
    entries: list[str] = []
    for paths in (SECTION_PATHS, *(paths for _, paths in ARTICLE_CATALOG)):
        alternates = "\n".join(
            f'    <xhtml:link rel="alternate" hreflang="{locale}" href="{url}" />'
            for locale, url in alternate_urls(site_url, paths).items()
        )
        entries.extend(
            f"  <url>\n    <loc>{site_url}{path}</loc>\n{alternates}\n  </url>"
            for path in paths.values()
        )
    return "\n".join(entries)


def section_cards(
    locale: str,
    articles: Sequence[tuple[Mapping[str, str], Mapping[str, str]]],
    read_more: str,
) -> str:
    cards: list[str] = []
    for position, (copy, paths) in enumerate(articles, start=1):
        cards.append(
            f'        <a class="guide-index__card" href="{paths[locale]}">\n'
            f'          <span class="guide-index__number" aria-hidden="true">{position:02}</span>\n'
            '          <span class="guide-index__copy">\n'
            f'            <span class="broadcast-label">{escape(copy["hero.eyebrow"])}</span>\n'
            f'            <span class="guide-index__title">{escape(copy["meta.og_title"])}</span>\n'
            f'            <span class="guide-index__summary">{escape(copy["meta.description"])}</span>\n'
            '          </span>\n'
            f'          <span class="guide-index__cta">{escape(read_more)} '
            '<span aria-hidden="true">→</span></span>\n'
            '        </a>'
        )
    return "\n".join(cards)
