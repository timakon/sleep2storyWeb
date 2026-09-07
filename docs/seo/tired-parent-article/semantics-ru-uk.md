# Russian and Ukrainian wording evidence

Checked with live web searches on 7 September 2026. This is a narrow language and intent check, not keyword-volume research. Search results support natural wording, not the prevalence of a problem or the effectiveness of a product. Broad Wordstat figures in the main research must not be presented as volumes for these exact phrases.

## Russian

Primary phrase: **нет сил читать сказку на ночь**. The page addresses a parent who needs an easier option this evening; it does not target a collection of story texts.

Related wording: **не хочется читать детям**; **болит горло, а ребёнок просит сказку**; **короткая сказка на ночь**; **аудиосказка перед сном**.

Exact searches:

- `"нет сил" "читать сказку"`
- `"не хочется" "читать детям"`
- `"болит горло" "сказку"`
- `"болит горло" "читать" "сказку"`

Evidence:

- A [parent's Babyblog diary](https://www.babyblog.ru/user/aminavictory) appeared for the first query with the phrase «нет сил читать сказку» in a first-person account of asking the other parent to take over bedtime. This supports the fatigue wording and the handover situation; it is one personal account, not a representative sample.
- [MedAboutMe's article on reading to children](https://medaboutme.ru/articles/kak_pravilno_chitat_detyam/) appeared for the reluctance query and discusses reading when the adult does not feel like it. Used as adjacent wording evidence only, not as a medical or child-development authority for this article.
- The combined sore-throat queries mostly returned story texts in which a character has a sore throat. They did not establish a distinct search-demand cluster. The article still answers that situation because it is part of the requested parent need.

Editorial choices: direct «нет сил» in the title; «не хочется читать детям» once in the introduction; «болит горло» in the relevant section and FAQ. «Спокойной ночи», «запасная сказка» and «другой близкий взрослый» fit the site's family voice. Example speech avoids assuming the tired parent is the mother.

## Ukrainian

Primary phrase: **немає сил читати казку на ніч**. This is a natural editorial formulation for the immediate parent need; exact-query volume is unverified.

Related wording: **нема сил читати дитині**; **не хочеться читати дітям**; **болить горло, а дитина просить казку**; **аудіоказки на ніч**.

Exact searches:

- `"немає сил" "читати" "казку"`
- `"немає сил" "казку"`
- `"не хочеться" "читати дітям"`
- `"болить горло" "казку"`
- `"болить горло" "читати" "казку"`
- Follow-up: `"втомилися" "читати" "казки"`

Evidence:

- [A Ukrainian short-story collection](https://kazky-dlya-ditey.art/korotki-kazky/) appeared for the fatigue query and connects a short bedtime story with having little time or energy. This supports the local short-story framing, not demand estimates or developmental claims.
- [Baby Bear's Ukrainian bedtime-story page](https://baby-bear.org/uk/kazka-na-nich-dlya-divchinki-3-rokiv/) uses «немає сил читати» in its advice to parents. This is one publisher's wording. Its therapeutic and sleep-related marketing claims were not adopted.
- [Pepi's Ukrainian audio-story collection](https://pepi.com.ua/biblioteka/audiokazky) appeared in the follow-up search and uses «аудіоказки», «читати вголос» and parental tiredness together. Used only to check language and the audio alternative, not to endorse the service or its benefit claims.
- Exact reluctance and sore-throat combinations returned mostly unrelated discussions, educational materials or story texts. Sparse results do not prove that parents never search this way; they also do not justify a popularity claim.

Editorial choices: «на добраніч», «книжка», «роздивитися малюнки», «добірка», «програвач», «застосунок» and «озвучення». Syntax was rewritten for Ukrainian rather than copied from Russian. The page explicitly says that launch narration is planned in English and Russian; Ukrainian website text is not a promise of Ukrainian narration.

## Scope and validation

The local pages preserve every source paragraph and all five FAQ topics in substance. They distinguish tonight's available options from later preparation, require consent and the complete story text, describe narration as synthetic, and retain prelaunch status. They do not add store links, offline/export promises or sleep guarantees.

Voice-care wording was checked against the primary [NIDCD guidance](https://www.nidcd.nih.gov/health/taking-care-your-voice): rest a hoarse or tired voice and do not use whispering as the alternative. No diagnosis or treatment was added.

Both locale files have 89 keys in the English order after the coordinated removal of `meta.image_alt`; `figure.alt` remains localized. Node validation found no duplicate keys, empty values, inline HTML/Markdown or values copied unchanged from English. Both have five FAQ question/answer pairs. Counts use Unicode word tokens and keep apostrophes inside words:

| Locale | Article words | All property-value words |
| --- | ---: | ---: |
| Russian | 1,446 | 1,642 |
| Ukrainian | 1,444 | 1,640 |

Article counts exclude metadata, schema description, navigation, contents labels, byline and source labels; they include headings, the caption, examples and FAQ. Full site rendering and browser checks belong to the integration pass.
