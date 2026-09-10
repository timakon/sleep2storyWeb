(() => {
  const address = new URL(window.location.href);
  const campaignKeys = new Set([
    "utm_source", "utm_medium", "utm_campaign", "utm_id", "utm_term", "utm_content",
    "utm_source_platform", "utm_creative_format", "utm_marketing_tactic",
  ]);
  const queryParts = address.search.slice(1).split("&").filter(Boolean);
  const campaign = queryParts
    .filter((part) => campaignKeys.has(new URLSearchParams(part).keys().next().value))
    .join("&");
  const externalOrigin = (value) => {
    try {
      const url = new URL(value);
      return /^https?:$/.test(url.protocol) && url.origin !== address.origin ? url.origin : "";
    } catch {
      return "";
    }
  };
  window.sleep2storyReferrer = externalOrigin(address.searchParams.get("s2s_referrer") || document.referrer);
  window.sleep2storyPageLocation = `${address.origin}${address.pathname}${campaign ? `?${campaign}` : ""}`;
  if (address.searchParams.has("s2s_referrer")) {
    const remaining = queryParts.filter((part) => !new URLSearchParams(part).has("s2s_referrer")).join("&");
    window.history.replaceState(window.history.state, "", `${address.pathname}${remaining ? `?${remaining}` : ""}${address.hash}`);
  }

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
  const isRoot = address.pathname === "/" || address.pathname === "/index.html";
  const hash = /^#(?:top|how|inside|privacy|faq)$/.test(address.hash) ? address.hash : "";

  const referrer = window.sleep2storyReferrer;
  const query = [campaign, referrer ? `s2s_referrer=${encodeURIComponent(referrer)}` : ""].filter(Boolean).join("&");

  if (isRoot && preferredLocale !== "en") {
    if (!savedLocale) {
      document.cookie = `sleep2story_locale=${preferredLocale}; Max-Age=31536000; Path=/; SameSite=Lax`;
    }
    window.sleep2storyRedirecting = true;
    window.location.replace(`/${preferredLocale}/${query ? `?${query}` : ""}${hash}`);
    return;
  }

  document.querySelectorAll("a[data-locale]").forEach((link) => {
    const destination = `${link.getAttribute("href")}${query ? `?${query}` : ""}`;
    link.setAttribute("href", `${destination}${hash}`);
    link.addEventListener("click", () => {
      const locale = link.getAttribute("data-locale");
      if (locale) {
        document.cookie = `sleep2story_locale=${locale}; Max-Age=31536000; Path=/; SameSite=Lax`;
        const currentHash = /^#(?:top|how|inside|privacy|faq)$/.test(window.location.hash) ? window.location.hash : "";
        link.setAttribute("href", `${destination}${currentHash}`);
      }
    });
  });
})();
