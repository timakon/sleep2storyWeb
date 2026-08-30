(() => {
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
