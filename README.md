# Sleep2Story marketing site

Статический SEO-лендинг на английском, русском и немецком без runtime-зависимостей.
Английский — основной язык; `/` остаётся индексируемой страницей выбора языка без
принудительного редиректа.

## Локальный запуск

```sh
uv run scripts/build.py
uv run scripts/check_site.py
python3 -m http.server 4174 --directory dist
```

Открыть `http://localhost:4174/`, `/en/`, `/ru/` или `/de/`.

Исходники:

- `site/home.template.html` — общий шаблон локализованной страницы;
- `site/locales/*.properties` — переводы с обязательным равенством ключей;
- `variants/variants.css` — дизайн-система и адаптивные стили;
- `scripts/build.py` — production-сборка в `dist/`;
- `scripts/check_site.py` — маршруты, SEO, локаль ссылок, sitemap и ресурсы.

## Публикация

Сборка не использует публичные переменные окружения и не содержит секретов.
Минимальный вариант при существующем GitHub-репозитории — GitHub Pages с артефактом
`dist/`, custom domain `sleep2story.app` и HTTPS. До включения публикации нужны:

1. подтверждение платформы и доступа к DNS домена;
2. утверждённые Privacy Policy, Terms и немецкий Impressum с данными оператора;
3. реальные App Store / Google Play URL после релиза;
4. публичный Backend URL и CORS-контракт до подключения waitlist или analytics.

Форма сбора данных и аналитика намеренно не подключены: без утверждённых legal-текстов
и API origin они создавали бы неработающий или юридически рискованный сценарий.
