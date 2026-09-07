# Italian and Portuguese (Portugal): tired-parent article

Research and translation date: 2026-09-07. Scope: the 89 article keys in the English tired-parent article, translated in full into `it.properties` and `pt.properties`. The existing localized OG brand-image description is inherited; `figure.alt` describes the article illustration. Existing recording and bedtime-routine guides supplied the site's tone; `.seo-cache/site-meta.json` confirmed the prerelease product and the distinction between website languages and planned EN/RU narration.

## Italian

Primary editorial target: **storia della buonanotte quando si è stanchi**. H1: **Non hai energie per la storia della buonanotte?** The tired-parent wording is an editorial intent hypothesis, not a measured search term. The established bedtime vocabulary is supported by the sources below.

Related phrases:

| Phrase | Evidence and intended use |
| --- | --- |
| storie della buonanotte | The provincial Bookstart family booklet uses the singular form for a familiar parent–child moment; the article uses this broad term for stories of any kind. [Bookstart, Provincia di Bolzano](https://www.provinz.bz.it/famiglia-sociale-comunita/famiglia/downloads/FA_Bookstart_1_165x204_IT_2022_web.pdf) |
| fiabe della buonanotte | Established Italian category wording visible in a publisher's own product page; treated as a related category, not forced into every heading. [Readmio](https://www.readmio.com/it/home) |
| leggere ad alta voce | Used in both the Bookstart booklet and Readmio's Italian description. This is the article's natural name for reading aloud. [Readmio](https://www.readmio.com/it/home) |
| storie brevi | Readmio's Italian App Store description uses this formulation; it matches the short-reading option. [Readmio's Italian listing](https://apps.apple.com/it/app/readmio-libri-per-bambini/id1473021827) |

Live queries: `favola della buonanotte genitori stanchi leggere`; `fiabe della buonanotte voce dei genitori leggere ad alta voce`; `storie della buonanotte audiolibri bambini voce rauca`.

Editorial choices: familiar `tu`, `stasera`, `figure`, `ora della nanna`, and `storie di scorta`; no literal translation of “reading voice” or “let the pictures carry the story.” Source labels are Italian and explicitly say `in inglese`. The third query was an exploration of the sore-voice intent; it did not establish demand or provide medical evidence.

## Portuguese: Portugal (pt_PT)

Primary editorial target: **sem energia para ler uma história ao deitar**. H1: **Sem energia para ler uma história ao deitar?** The full tired-parent phrase is an editorial intent hypothesis. The `ao deitar` vocabulary is attested by Portuguese publishers and libraries; `histórias para dormir` remains a useful related wording already present on this site.

Related phrases:

| Phrase | Evidence and intended use |
| --- | --- |
| histórias ao deitar | A Portuguese publisher used this expression for family recordings, and the municipal library has a category with the same name. [LeYa announcement](https://news.cision.com/pt/leya/r/leya-historias-ao-deitar--a-partir-de-amanha%2Cc637208987000000000), [Biblioteca Municipal de Viana do Castelo](https://biblioteca.cm-viana-castelo.pt/Atividades/Galerias-Multimedia/emodule/587/ecategory/10) |
| histórias para dormir | Exact title of a programme from Portugal's public broadcaster. Used as a related topic phrase, without repeating its promotional sleep claims. [RTP Zig Zag](https://www.rtp.pt/play/zigzag/p14188/e814753/historias-para-dormir) |
| ler em voz alta | Standard action wording used in the translation; the targeted query returned mixed and weak evidence for this article's specific intent. Kept for linguistic clarity, with no claim of measured demand. |
| histórias em áudio para crianças | Editorial description of the listening option. RTP offers children's stories to listen to, but this full phrase is a related wording, not a verified exact-match query. [RTP: Histórias](https://media.rtp.pt/zigzag/historias-2/) |

Useful live formulations: `histórias ao deitar Portugal pais`; `RTP histórias áudio crianças Zig Zag`; `"histórias ao deitar" Portugal`. Additional attempts were `ler crianças voz alta hora de deitar Portugal` and `"ler em voz alta" "pais" Portugal`. The initial three queries using `site:.pt` returned no results in this tool: `histórias ao deitar pais cansados ler site:.pt`; `histórias para adormecer ler voz alta pais site:.pt`; `histórias áudio crianças hora de deitar site:.pt`. That tool outcome is not evidence of no demand.

Editorial choices: polite third-person address consistent with the existing site, `telemóvel`, `ecrã`, `ficheiro`, `candeeiro`, `percetíveis`, `estar a + infinitive`, and `boas-noites`; the parent speaks to the child with `tu` in example dialogue. No Brazilian-default `celular`, `tela` or `arquivo`. Source labels are Portuguese and explicitly say `em inglês`.

## Limits and verification

This was qualitative live search for local language and intent, not location-controlled rank tracking, Google Search Console research or keyword-volume measurement. Search results contain mixed document types; the cited publishers, broadcaster and public institutions establish wording and context only. No volumes, ranks, traffic estimates or sleep outcomes are inferred. Neither Italian nor Portuguese narration is promised: both translations retain prerelease status, planned English/Russian narration, speaker consent, the complete story text as input and synthetic narration as output. Voice-rest guidance and the instruction not to whisper are translated from the English source, without expanding them into treatment advice.

Verified 89/89 ordered article keys after the agreed removal of the inherited OG-image alt override: no duplicate keys, no empty values, one physical line per key and no HTML/Markdown in either properties file. Word counts are Italian 2,030 and Portuguese 2,068. These whole-value counts include metadata, captions and labels; they are not body-only reading lengths.

Run from the repository root:

```sh
ruby -e 'base="site/tired-parent-article-locales/"; keys=File.readlines(base+"en.properties",chomp:true).map{|line| line.split("=",2).first}; %w[it pt].each do |locale|; lines=File.readlines(base+locale+".properties",chomp:true); actual=lines.map{|line| line.split("=",2).first}; abort "key mismatch #{locale}" unless keys==actual; abort "duplicate #{locale}" unless actual.uniq.size==actual.size; abort "blank #{locale}" unless lines.all?{|line| line.include?("=") && !line.split("=",2).last.to_s.empty?}; abort "markup #{locale}" if lines.any?{|line| line.match?(/<[^>]+>|\]\(/)}; words=lines.sum{|line| line.split("=",2).last.split.size}; puts "#{locale}: #{lines.size}/#{keys.size} ordered keys; #{words} words; no empty values or markup"; end'
```
