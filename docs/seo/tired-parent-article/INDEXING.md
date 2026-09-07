# Отправка статьи в поисковые системы

Инструкция подготовлена 7 сентября 2026. Это действия владельца в кабинетах, а не подтверждение выполненной отправки или индексации.

## Google Search Console

1. Откройте [Google Search Console](https://search.google.com/search-console). Выберите существующий ресурс сайта. Если его ещё нет, добавьте доменный ресурс `sleep2story.com` и подтвердите владение DNS TXT-записью, которую выдаст Google. Скопируйте именно выданное значение. Оставьте запись после проверки. Отдельные ресурсы для 14 языков не нужны.
2. В разделе **Индексирование → Файлы Sitemap** отправьте `https://sleep2story.com/sitemap.xml`. Если поле уже содержит префикс сайта, впишите только `sitemap.xml`. Если этот адрес уже добавлен, второй экземпляр не нужен: Google будет перечитывать тот же файл.
3. Через верхнюю строку **Проверка URL** проверьте по очереди приоритетные адреса ниже. Нажмите **Проверить опубликованную страницу**, затем **Запросить индексирование**. Если интерфейс не позволяет отправить запрос, устраните указанную причину; после исчерпания квоты продолжите в другой день.
4. Сначала отправьте новую EN-статью, затем DE, FR, ES, IT, NL и PT. Остальные переводы доступны через sitemap и взаимные ссылки. Приоритет выбран по целевым рынкам, а не по измеренной частотности запросов. Английская страница одна для США и Великобритании.
5. Если сайт ещё совсем не индексировался, дополнительно проверьте `https://sleep2story.com/`, `https://sleep2story.com/guides/` и разделы нужных языков: `/de/ratgeber/`, `/fr/guides/`, `/es/guias/`, `/it/guide/`, `/nl/gidsen/`, `/pt/guias/`. Полные URL начинаются с `https://sleep2story.com`.

Документация: [ресурсы и основные задачи](https://support.google.com/webmasters/answer/10351509?hl=en), [отчёт Sitemap](https://support.google.com/webmasters/answer/7451001?hl=en), [проверка URL](https://support.google.com/webmasters/answer/9012289?hl=en).

## Яндекс Вебмастер

1. Откройте [Яндекс Вебмастер](https://webmaster.yandex.ru/). Выберите или добавьте сайт `https://sleep2story.com` и подтвердите права. DNS TXT позволяет сделать это без изменения HTML; используйте значение из кабинета.
2. В **Индексирование → Файлы Sitemap** добавьте `https://sleep2story.com/sitemap.xml`. Если файл уже добавлен, используйте действие отправки обновлённого sitemap на переобход в его строке.
3. В **Индексирование → Переобход страниц** отправьте следующие адреса, по одному на строку:

```text
https://sleep2story.com/ru/guides/net-sil-chitat-skazku-na-noch/
https://sleep2story.com/ru/guides/
https://sleep2story.com/ru/
```

4. При доступном лимите можно отправить и остальные переводы из списка ниже. Sitemap отправляйте через раздел Sitemap, а не через переобход HTML-страниц.
5. Добавьте русскую статью в **Мониторинг важных страниц**. В **Индексирование → Страницы в поиске** проверяйте появление страницы и причины исключения.

Документация: [подтверждение прав](https://yandex.ru/support/webmaster/ru/service/rights), [Sitemap](https://yandex.ru/support/webmaster/ru/indexing-options/sitemap), [переобход страниц](https://www.yandex.ru/support/webmaster/ru/robot-workings/site-reindex).

## Все 14 новых URL

```text
https://sleep2story.com/guides/too-tired-to-read-bedtime-stories/
https://sleep2story.com/de/ratgeber/zu-muede-zum-vorlesen/
https://sleep2story.com/fr/guides/trop-fatigue-pour-lire-histoire-du-soir/
https://sleep2story.com/es/guias/demasiado-cansado-para-leer-cuentos/
https://sleep2story.com/it/guide/troppo-stanchi-per-leggere-la-storia-della-buonanotte/
https://sleep2story.com/nl/gidsen/te-moe-om-voor-te-lezen/
https://sleep2story.com/pt/guias/sem-energia-para-ler-historia-ao-deitar/
https://sleep2story.com/ru/guides/net-sil-chitat-skazku-na-noch/
https://sleep2story.com/uk/porady/nemaie-syl-chytaty-kazku-na-nich/
https://sleep2story.com/pl/poradniki/brak-sily-na-czytanie-bajki/
https://sleep2story.com/sr/vodici/nema-snage-za-pricu-za-laku-noc/
https://sleep2story.com/cs/pruvodce/moc-unaveni-na-cteni-pohadky/
https://sleep2story.com/ro/ghiduri/prea-obosit-sa-citesti-povestea-de-seara/
https://sleep2story.com/tr/rehber/masal-okuyamayacak-kadar-yorgun-olmak/
```

## После отправки и при следующих публикациях

- Успешная отправка sitemap или заявка на обход не означает включения страниц в поиск. Проверяйте индексирование в кабинетах, а не только запросом `site:`.
- Раз в неделю смотрите GSC **Индексирование → Страницы** и **Эффективность → Результаты поиска**: страницы, запросы, страны, показы и клики. Данные будут появляться по мере обхода и поисковых показов. Проверьте выбранный Google canonical: для каждого перевода ожидается собственный URL, а не английский.
- В Яндексе статус **Заявка обработана** подтверждает посещение роботом, но сам по себе не подтверждает индексирование.
- При следующей статье обновляйте тот же sitemap, добавляйте ссылки из языковых разделов и связанных статей. Запрашивайте обход новых приоритетных страниц; заново отправлять все 84 адреса каждый раз не нужно.
- GA4 и Метрика могут дать статистику поведения на сайте, но их установка не является условием индексирования. Для начала достаточно Search Console и Вебмастера. Идентификаторы счётчиков и подтверждения прав выдаются в аккаунтах владельца; произвольные значения в код не добавляются.
- В sitemap нет необязательного `lastmod`. Не стоит подставлять дату каждой сборки: [Google использует только достоверные даты существенных изменений](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap). Это не препятствует отправке текущего sitemap.

Локальные проверки перед публикацией: `node scripts/check_locale_redirect.mjs`, `/opt/homebrew/bin/python3 scripts/build.py`, `/opt/homebrew/bin/python3 scripts/check_site.py dist` завершились успешно. Публикация и доступность на домене проверяются отдельно после отправки коммита.
