# Sleep2Story marketing site

Статический SEO-лендинг без сборщика и runtime-зависимостей. Основная страница
использует выбранное направление «Семейный эфир».

```sh
python3 -m http.server 4173 --directory website
```

Открыть `http://localhost:4173/`.

## Три новых направления

Страница сравнения: `http://localhost:4173/variants/`

- `variants/01-book-spread.html` — литературный книжный разворот.
- `variants/02-voice-studio.html` — тёмный product-first / voice studio.
- `variants/03-family-broadcast.html` — яркий семейный аудиобренд.
- `reference-research.md` — выводы по официальным референсам.
- `index-editorial-v1.html` — архив первой редакционной версии (`noindex`).

Варианты помечены `noindex`: это дизайн-кандидаты, а не три конкурирующие SEO-страницы. После выбора направление нужно перенести в основной `index.html`, сохранить единственный canonical и обновить Open Graph-обложку.

Перед публикацией:

1. Подтвердить домен `sleep2story.app` или заменить canonical, Open Graph URL, sitemap и robots.
2. Добавить реальные App Store / Google Play URL после релиза.
3. Подключить утверждённые юридические страницы.
4. При необходимости конвертировать TTF в WOFF2 и проверить лицензии шрифтов.
