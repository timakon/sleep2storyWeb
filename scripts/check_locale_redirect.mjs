import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";

const source = fs.readFileSync(new URL("../assets/site.js", import.meta.url), "utf8");

function visit({ languages = ["en"], cookie = "", path = "/", referrer = "" } = {}) {
  let redirect = "";
  let cleaned = "";
  const address = new URL(path, "https://sleep2story.com");
  const makeLink = (locale) => ({
    href: locale === "en" ? "/" : `/${locale}/`,
    getAttribute(name) { return name === "data-locale" ? locale : this.href; },
    setAttribute(_, value) { this.href = value; },
    addEventListener(_, handler) { this.click = handler; },
    cloneNode() { return makeLink(locale); },
  });
  const links = ["en", "ru", "de", "fr", "zh", "ar", "hi", "ja", "ko"].map(makeLink);
  const suggestion = {
    hidden: true,
    appendChild(link) { this.link = link; },
  };
  const document = { cookie, referrer, querySelectorAll: () => links, querySelector: () => suggestion };
  const window = {
    location: {
      href: address.href, origin: address.origin, pathname: address.pathname,
      search: address.search, hash: address.hash,
      replace: (url) => { redirect = url; },
      assign() {},
    },
    history: { state: null, replaceState: (_, __, url) => { cleaned = url; } },
  };
  vm.runInNewContext(source, { URL, URLSearchParams, document, window, navigator: { languages, language: languages[0] } });
  return {
    redirect, cleaned, window, document, suggestion,
    switchLocale(link = links.find((entry) => entry.getAttribute("data-locale") === "fr")) {
      link.click({ preventDefault() { assert.fail("Locale links must retain native navigation"); } });
      return link.href;
    },
  };
}

for (const locale of ["ru", "ja", "zh", "ar", "hi", "ko"]) {
  const page = visit({ languages: [`${locale}-XX`, "en-US"] });
  assert.equal(page.redirect, "");
  assert.equal(page.document.cookie, "", "A suggestion must not save a language until clicked");
  assert.equal(page.suggestion.hidden, false);
  assert.equal(page.suggestion.link.href, `/${locale}/`);
}
for (const retired of ["sr-Latn-RS", "uk-UA", "nl-NL", "cs-CZ", "ro-RO"]) {
  assert.equal(visit({ languages: [retired] }).suggestion.hidden, true);
}
assert.equal(visit({ languages: ["ru-RU"], cookie: "sleep2story_locale=uk" }).suggestion.link.href, "/ru/");
assert.equal(visit({ languages: ["ru-RU"], cookie: "sleep2story_locale=en" }).suggestion.hidden, true);
assert.equal(visit({ languages: ["ru-RU"], cookie: "sleep2story_locale=de" }).suggestion.link.href, "/de/");
assert.equal(visit({ languages: ["ru-RU"], path: "/fr/" }).suggestion.hidden, true);

const campaign = "utm_source=Newsletter&utm_medium=email&utm_campaign=Sleep%20Well&utm_content=a+b&utm_id=7&utm_term=bedtime&utm_source_platform=mail&utm_creative_format=banner&utm_marketing_tactic=prospecting";
const suggested = visit({ languages: ["ru"], path: `/?${campaign}&email=private@example.com#privacy`, referrer: "https://NEWS.example/path?secret=yes#token" });
assert.equal(suggested.redirect, "");
assert.equal(suggested.switchLocale(suggested.suggestion.link), `/ru/?${campaign}&s2s_referrer=https%3A%2F%2Fnews.example#privacy`);
assert.match(suggested.document.cookie, /^sleep2story_locale=ru;/);
assert.equal(visit({ languages: ["ru"], referrer: "https://sleep2story.com/blog/" }).suggestion.link.href, "/ru/");
assert.equal(visit({ languages: ["ru"], referrer: "javascript:alert(1)" }).suggestion.link.href, "/ru/");

const landed = visit({ path: `/ru/?${campaign}&s2s_referrer=https%3A%2F%2Fnews.example%2Fprivate%3Ftoken%3D123&secret=hidden#privacy`, referrer: "https://sleep2story.com/" });
assert.equal(landed.cleaned, `/ru/?${campaign}&secret=hidden#privacy`);
assert.equal(landed.window.sleep2storyReferrer, "https://news.example");
assert.equal(landed.window.sleep2storyPageLocation, `https://sleep2story.com/ru/?${campaign}`);
assert.equal(landed.document.cookie, "");
assert.equal(landed.switchLocale(), `/fr/?${campaign}&s2s_referrer=https%3A%2F%2Fnews.example#privacy`);
landed.window.location.hash = "#faq";
assert.equal(landed.switchLocale(), `/fr/?${campaign}&s2s_referrer=https%3A%2F%2Fnews.example#faq`);
assert.equal(visit({ path: `/?${campaign}` }).switchLocale(), `/fr/?${campaign}`);
assert.equal(visit({ path: "/?private=secret#unrecognized" }).switchLocale(), "/fr/");
assert.equal(visit({ path: "/ru/?s2s_referrer=javascript%3Aalert(1)" }).window.sleep2storyReferrer, "");
assert.equal(visit({ path: "/ru/?s2s_referrer=https%3A%2F%2Fsleep2story.com%2Fprivate" }).window.sleep2storyReferrer, "");
assert.equal(visit({ path: "/ru/", referrer: "https://search.example/private?term=secret" }).window.sleep2storyReferrer, "https://search.example");

console.log("Locale navigation checks passed");
