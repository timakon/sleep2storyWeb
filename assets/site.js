(() => {
  const supportedLocales = new Set([
    "en", "ru", "de", "uk", "pl", "sr", "fr", "es", "it", "pt", "nl", "cs", "ro", "tr",
  ]);
  const normalizeLocale = (value) => value?.toLowerCase().split(/[-_]/)[0] || "";
  const savedLocale = normalizeLocale(
    document.cookie
      .split(";")
      .map((item) => item.trim())
      .find((item) => item.startsWith("sleep2story_locale="))
      ?.split("=")[1],
  );
  const browserLocale = (navigator.languages || [navigator.language])
    .map(normalizeLocale)
    .find((locale) => supportedLocales.has(locale));
  const preferredLocale = supportedLocales.has(savedLocale) ? savedLocale : browserLocale || "en";
  const isRoot = window.location.pathname === "/" || window.location.pathname === "/index.html";

  if (isRoot && preferredLocale !== "en") {
    const hash = /^#(?:top|how|inside|privacy|faq)$/.test(window.location.hash)
      ? window.location.hash
      : "";
    if (!savedLocale) {
      document.cookie = `sleep2story_locale=${preferredLocale}; Max-Age=31536000; Path=/; SameSite=Lax`;
    }
    window.location.replace(`/${preferredLocale}/${hash}`);
    return;
  }

  const localeLinks = document.querySelectorAll("a[data-locale]");

  localeLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      const locale = link.getAttribute("data-locale");
      if (locale) {
        document.cookie = `sleep2story_locale=${locale}; Max-Age=31536000; Path=/; SameSite=Lax`;
        if (/^#(?:top|how|inside|privacy|faq)$/.test(window.location.hash)) {
          event.preventDefault();
          window.location.assign(`${link.getAttribute("href")}${window.location.hash}`);
        }
      }
    });
  });

})();
