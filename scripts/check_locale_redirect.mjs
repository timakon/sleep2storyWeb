import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";

const source = fs.readFileSync(new URL("../assets/site.js", import.meta.url), "utf8");

function visit({ languages = ["en"], cookie = "", path = "/", referrer = "" } = {}) {
  let redirect = "";
  let href = "/fr/";
  let prevented = false;
  let cleaned = "";
  let click;
  const address = new URL(path, "https://sleep2story.com");
  const link = {
    getAttribute: (name) => name === "data-locale" ? "fr" : href,
    setAttribute: (_, value) => { href = value; },
    addEventListener: (_, handler) => { click = handler; },
  };
  const document = { cookie, referrer, querySelectorAll: () => [link] };
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
  return { redirect, cleaned, window, document, get prevented() { return prevented; }, switchLocale() { click({ preventDefault() { prevented = true; } }); return href; } };
}

assert.equal(visit({ languages: ["ru-RU", "en-US"] }).redirect, "/ru/");
assert.equal(visit({ languages: ["sr-Latn-RS"], path: "/#inside" }).redirect, "/sr/#inside");
assert.equal(visit({ languages: ["ja-JP"] }).redirect, "");
assert.equal(visit({ languages: ["ru-RU"], cookie: "sleep2story_locale=en" }).redirect, "");
assert.equal(visit({ languages: ["ru-RU"], cookie: "sleep2story_locale=de" }).redirect, "/de/");
assert.equal(visit({ languages: ["ru-RU"], path: "/fr/" }).redirect, "");

const campaign = "utm_source=Newsletter&utm_medium=email&utm_campaign=Sleep%20Well&utm_content=a+b&utm_id=7&utm_term=bedtime&utm_source_platform=mail&utm_creative_format=banner&utm_marketing_tactic=prospecting";
const redirected = visit({ languages: ["ru"], path: `/?${campaign}&email=private@example.com#privacy`, referrer: "https://NEWS.example/path?secret=yes#token" });
assert.equal(redirected.redirect, `/ru/?${campaign}&s2s_referrer=https%3A%2F%2Fnews.example#privacy`);
assert.equal(redirected.window.sleep2storyRedirecting, true);
assert.equal(visit({ languages: ["ru"], referrer: "https://sleep2story.com/blog/" }).redirect, "/ru/");
assert.equal(visit({ languages: ["ru"], referrer: "javascript:alert(1)" }).redirect, "/ru/");

const landed = visit({ path: `/ru/?${campaign}&s2s_referrer=https%3A%2F%2Fnews.example%2Fprivate%3Ftoken%3D123&secret=hidden#privacy`, referrer: "https://sleep2story.com/" });
assert.equal(landed.cleaned, `/ru/?${campaign}&secret=hidden#privacy`);
assert.equal(landed.window.sleep2storyReferrer, "https://news.example");
assert.equal(landed.window.sleep2storyPageLocation, `https://sleep2story.com/ru/?${campaign}`);
assert.equal(landed.document.cookie, "");
assert.equal(landed.switchLocale(), `/fr/?${campaign}&s2s_referrer=https%3A%2F%2Fnews.example#privacy`);
assert.equal(landed.prevented, false, "Locale links retain native modified-click behavior");
landed.window.location.hash = "#faq";
assert.equal(landed.switchLocale(), `/fr/?${campaign}&s2s_referrer=https%3A%2F%2Fnews.example#faq`);
assert.equal(visit({ path: `/?${campaign}` }).switchLocale(), `/fr/?${campaign}`);
assert.equal(visit({ path: "/?private=secret#unrecognized" }).switchLocale(), "/fr/");
assert.equal(visit({ path: "/ru/?s2s_referrer=javascript%3Aalert(1)" }).window.sleep2storyReferrer, "");
assert.equal(visit({ path: "/ru/?s2s_referrer=https%3A%2F%2Fsleep2story.com%2Fprivate" }).window.sleep2storyReferrer, "");
assert.equal(visit({ path: "/ru/", referrer: "https://search.example/private?term=secret" }).window.sleep2storyReferrer, "https://search.example");

console.log("Locale redirect checks passed");
