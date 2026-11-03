from __future__ import annotations

from html import escape
import json
from types import MappingProxyType
from typing import Final, Mapping, Sequence


ARTICLE_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "ru": "/ru/guides/kak-zapisat-skazku-na-noch/",
    "en": "/guides/how-to-record-bedtime-stories/",
    "zh": "/zh/zhinan/shuiqian-gushi-luyin-fangfa/",
    "es": "/es/guias/grabar-cuentos-para-dormir/",
    "fr": "/fr/guides/enregistrer-une-histoire-du-soir/",
    "de": "/de/ratgeber/gute-nacht-geschichten-aufnehmen/",
    "it": "/it/guide/registrare-storie-della-buonanotte/",
    "pt": "/pt/guias/gravar-historias-para-dormir/",
    "ar": "/ar/dalil/tasjil-qisas-qabl-alnawm/",
    "hi": "/hi/guide/sone-se-pahle-kahani-record-kaise-karen/",
    "ja": "/ja/guide/oyasumi-mae-no-ohanashi-rokon/",
    "ko": "/ko/guide/jamjari-donghwa-nogeum-bangbeop/",
    "tr": "/tr/rehber/uyku-masali-nasil-kaydedilir/",
    "pl": "/pl/poradniki/jak-nagrac-bajke-na-dobranoc/",
})
GRANDPARENT_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "ru": "/ru/guides/babushka-dedushka-zapisat-skazku-dlya-vnukov/",
    "en": "/guides/grandparents-record-stories-for-grandchildren/",
    "zh": "/zh/zhinan/zufu-zumu-gei-sunbei-lu-gushi/",
    "es": "/es/guias/abuelos-grabar-cuentos-para-nietos/",
    "fr": "/fr/guides/grands-parents-enregistrer-histoire-petits-enfants/",
    "de": "/de/ratgeber/oma-opa-gute-nacht-geschichte-fuer-enkel-aufnehmen/",
    "it": "/it/guide/nonni-registrare-storie-per-nipoti/",
    "pt": "/pt/guias/avos-gravar-historias-para-netos/",
    "ar": "/ar/dalil/tasjil-qisas-alajdad-lilahfad/",
    "hi": "/hi/guide/dada-dadi-nana-nani-ki-record-ki-hui-kahaniyan/",
    "ja": "/ja/guide/sofu-sobo-mago-ni-ohanashi-o-rokon/",
    "ko": "/ko/guide/jobu-mo-sonju-jamjari-donghwa-nogeum/",
    "tr": "/tr/rehber/buyukanne-dede-torunlar-icin-masal-kaydetme/",
    "pl": "/pl/poradniki/babcia-dziadek-nagrac-bajke-dla-wnukow/",
})
BEDTIME_ROUTINE_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "ru": "/ru/guides/skazki-na-noch-dlya-detey-spokoinyy-ritual/",
    "en": "/guides/bedtime-stories-for-kids-calm-routine/",
    "zh": "/zh/zhinan/ertong-shuiqian-gushi-wan-shang-xiguan/",
    "es": "/es/guias/cuentos-para-dormir-ninos-rutina-nocturna/",
    "fr": "/fr/guides/histoires-du-soir-enfants-rituel-coucher/",
    "de": "/de/ratgeber/gute-nacht-geschichten-kinder-abendroutine/",
    "it": "/it/guide/storie-buonanotte-bambini-routine-serale/",
    "pt": "/pt/guias/historias-para-dormir-criancas-rotina-noturna/",
    "ar": "/ar/dalil/qisas-alatfal-wa-rutin-qabl-alnawm/",
    "hi": "/hi/guide/bachchon-ki-sone-se-pahle-kahani-ki-dincharya/",
    "ja": "/ja/guide/kodomo-no-oyasumi-ohanashi-shukan/",
    "ko": "/ko/guide/aideul-jamjari-donghwa-rutin/",
    "tr": "/tr/rehber/cocuklar-icin-uyku-masallari-aksam-rutini/",
    "pl": "/pl/poradniki/bajki-na-dobranoc-dla-dzieci-wieczorny-rytual/",
})
TIRED_PARENT_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "ru": "/ru/guides/net-sil-chitat-skazku-na-noch/",
    "en": "/guides/too-tired-to-read-bedtime-stories/",
    "zh": "/zh/zhinan/tai-lei-bu-xiang-jiang-shuiqian-gushi/",
    "es": "/es/guias/demasiado-cansado-para-leer-cuentos/",
    "fr": "/fr/guides/trop-fatigue-pour-lire-histoire-du-soir/",
    "de": "/de/ratgeber/zu-muede-zum-vorlesen/",
    "it": "/it/guide/troppo-stanchi-per-leggere-la-storia-della-buonanotte/",
    "pt": "/pt/guias/sem-energia-para-ler-historia-ao-deitar/",
    "ar": "/ar/dalil/indama-tataab-min-qiraat-qissat-alnawm/",
    "hi": "/hi/guide/bahut-thake-hain-kahani-kaise-sunaye/",
    "ja": "/ja/guide/yomikikase-ni-tsukareta-toki/",
    "ko": "/ko/guide/donghwa-ilgi-himdeun-nal/",
    "tr": "/tr/rehber/masal-okuyamayacak-kadar-yorgun-olmak/",
    "pl": "/pl/poradniki/brak-sily-na-czytanie-bajki/",
})
FAMILY_MEMORY_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "ru": "/ru/guides/kak-prevratit-vospominanie-v-skazku/",
    "en": "/guides/family-story-prompts-for-kids/",
    "zh": "/zh/zhinan/jiating-huiyi-bian-cheng-ertong-gushi/",
    "es": "/es/guias/recuerdos-familiares-en-cuentos-para-ninos/",
    "fr": "/fr/guides/souvenirs-de-famille-en-histoire-pour-enfants/",
    "de": "/de/ratgeber/familienerinnerungen-als-geschichte-fuer-kinder/",
    "it": "/it/guide/ricordi-di-famiglia-in-storie-per-bambini/",
    "pt": "/pt/guias/memorias-de-familia-em-historias-para-criancas/",
    "ar": "/ar/dalil/tahwil-dhikrayat-alusra-ila-qissa-lilatfal/",
    "hi": "/hi/guide/parivar-ki-yadon-se-bachchon-ki-kahani/",
    "ja": "/ja/guide/kazoku-no-omoide-kodomo-no-monogatari/",
    "ko": "/ko/guide/gajok-chueogeuro-aideul-iyagi/",
    "tr": "/tr/rehber/aile-anilarini-cocuklar-icin-masala-donusturme/",
    "pl": "/pl/poradniki/rodzinne-wspomnienia-w-bajce-dla-dziecka/",
})
PARENT_AWAY_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "ru": "/ru/guides/skazka-na-noch-kogda-roditel-v-otezde/",
    "en": "/guides/bedtime-stories-when-parent-is-away/",
    "zh": "/zh/zhinan/fumu-buzai-shenbian-shuiqian-gushi/",
    "es": "/es/guias/cuentos-para-dormir-cuando-un-padre-esta-lejos/",
    "fr": "/fr/guides/histoire-du-soir-quand-un-parent-est-absent/",
    "de": "/de/ratgeber/gute-nacht-geschichten-wenn-ein-elternteil-weg-ist/",
    "it": "/it/guide/storia-buonanotte-quando-un-genitore-e-lontano/",
    "pt": "/pt/guias/historia-de-embalar-quando-um-dos-pais-esta-longe/",
    "ar": "/ar/dalil/qissat-alnawm-ind-ghiyab-ahad-alwalidayn/",
    "hi": "/hi/guide/jab-mata-pita-door-hon-sone-ki-kahani/",
    "ja": "/ja/guide/oya-ga-rusuno-yoru-no-ohanashi/",
    "ko": "/ko/guide/bumoga-meolli-isseul-ttae-jamjari-donghwa/",
    "tr": "/tr/rehber/ebeveyn-uzaktayken-uyku-masali/",
    "pl": "/pl/poradniki/bajka-na-dobranoc-gdy-rodzic-wyjezdza/",
})
BILINGUAL_STORY_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "ru": "/ru/guides/skazki-na-noch-na-raznyh-yazykah/",
    "en": "/guides/bedtime-stories-in-different-languages/",
    "zh": "/zh/zhinan/butong-yuyan-de-shuiqian-gushi/",
    "es": "/es/guias/cuentos-para-dormir-en-varios-idiomas/",
    "fr": "/fr/guides/histoires-du-soir-en-plusieurs-langues/",
    "de": "/de/ratgeber/gute-nacht-geschichten-in-vielen-sprachen/",
    "it": "/it/guide/storie-della-buonanotte-in-piu-lingue/",
    "pt": "/pt/guias/historias-de-embalar-em-varias-linguas/",
    "ar": "/ar/dalil/qisas-qabl-alnawm-bilughat-mukhtalifa/",
    "hi": "/hi/guide/alag-bhashaon-mein-sone-ki-kahaniyan/",
    "ja": "/ja/guide/iroiro-na-gengo-de-oyasumi-ohanashi/",
    "ko": "/ko/guide/yeoreo-eoneoui-jamjari-donghwa/",
    "tr": "/tr/rehber/farkli-dillerde-uyku-masallari/",
    "pl": "/pl/poradniki/bajki-na-dobranoc-w-roznych-jezykach/",
})
BILINGUAL_STORY_OLD_PATHS: Final[Mapping[str, str]] = MappingProxyType({
    "ru": "/ru/guides/skazka-na-noch-na-dvuh-yazykah/",
    "en": "/guides/bilingual-bedtime-story-for-kids/",
    "es": "/es/guias/cuento-para-dormir-en-dos-idiomas/",
    "fr": "/fr/guides/histoire-du-soir-bilingue-enfant/",
    "de": "/de/ratgeber/zweisprachige-gute-nacht-geschichte-kinder/",
    "it": "/it/guide/storia-della-buonanotte-in-due-lingue/",
    "pt": "/pt/guias/historia-de-embalar-em-duas-linguas/",
    "tr": "/tr/rehber/iki-dilde-uyku-masali/",
    "pl": "/pl/poradniki/bajka-na-dobranoc-w-dwoch-jezykach/",
})
ARTICLE_CATALOG: Final[tuple[tuple[str, Mapping[str, str], str, str], ...]] = (
    ("article-locales", ARTICLE_PATHS, "2026-09-02", "how-to-record-bedtime-stories.html"),
    ("grandparent-article-locales", GRANDPARENT_PATHS, "2026-09-02", "how-to-record-bedtime-stories.html"),
    ("bedtime-routine-article-locales", BEDTIME_ROUTINE_PATHS, "2026-09-04", "how-to-record-bedtime-stories.html"),
    ("tired-parent-article-locales", TIRED_PARENT_PATHS, "2026-09-07", "tired-parents.html"),
    ("family-memory-article-locales", FAMILY_MEMORY_PATHS, "2026-09-14", "family-memories.html"),
    ("parent-away-article-locales", PARENT_AWAY_PATHS, "2026-09-19", "parent-away.html"),
    ("bilingual-story-article-locales", BILINGUAL_STORY_PATHS, "2026-09-30", "bilingual-story.html"),
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
            f'            <a href="{path}" lang="{locale}" dir="auto" data-locale="{locale}"'
            f"{current_attribute}>{escape(names[locale])}</a>"
        )
    return "\n".join(links)


def structured_data(
    site_url: str,
    locale: str,
    copy: Mapping[str, str],
    paths: Mapping[str, str],
    published_date: str,
) -> str:
    canonical = f"{site_url}{paths[locale]}"
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": copy["meta.og_title"],
        "description": copy["schema.description"],
        "image": copy.get("meta.image_url", f"{site_url}/assets/og-{locale}.jpg"),
        "datePublished": published_date,
        "dateModified": published_date,
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
    for paths in (SECTION_PATHS, *(paths for _, paths, _, _ in ARTICLE_CATALOG)):
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
