import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";

const siteSource = fs.readFileSync(new URL("../assets/site.js", import.meta.url), "utf8");
const analyticsPath = new URL("../assets/analytics.js", import.meta.url);
const analyticsSource = fs.existsSync(analyticsPath) ? fs.readFileSync(analyticsPath, "utf8") : "";
const measurementId = "G-HXBT0T7YQM";

function visit({ cookie = "", path = "/ru/", origin = "https://sleep2story.com", referrer = "", languages = ["en"] } = {}) {
  const address = new URL(path, origin);
  const cookies = new Map(cookie.split(";").filter(Boolean).map((part) => part.trim().split("=")));
  const writes = [];
  const scripts = [];
  let reloads = 0;
  let focused = "";
  let cleaned = "";
  const localeLink = {
    href: "/fr/",
    getAttribute(name) { return name === "data-locale" ? "fr" : this.href; },
    setAttribute(_, value) { this.href = value; },
    addEventListener(_, handler) { this.click = handler; },
  };
  const controls = Object.fromEntries(["analytics-notice", "analytics-title", "analytics-accept", "analytics-reject", "analytics-settings"].map((id) => [id, {
    hidden: true, listeners: {}, attributes: {},
    addEventListener(type, handler) { this.listeners[type] = handler; },
    setAttribute(name, value) { this.attributes[name] = value; },
    focus() { focused = id; },
  }]));
  const document = {
    referrer,
    get cookie() { return [...cookies].map(([key, value]) => `${key}=${value}`).join("; "); },
    set cookie(value) {
      writes.push(value);
      const [key, entry] = value.split(";")[0].split("=");
      if (/Max-Age=0(?:;|$)/.test(value)) cookies.delete(key);
      else cookies.set(key, entry);
    },
    querySelectorAll: () => [localeLink],
    getElementById: (id) => controls[id],
    createElement: (tagName) => ({ tagName }),
    head: { appendChild: (element) => scripts.push(element) },
  };
  const window = {
    location: {
      href: address.href, origin: address.origin, pathname: address.pathname,
      hostname: address.hostname, protocol: address.protocol, search: address.search, hash: address.hash,
      replace() {}, assign() {}, reload() { reloads += 1; },
    },
    history: { state: null, replaceState(_, __, url) { cleaned = url; } },
  };
  const context = vm.createContext({ document, window, URL, URLSearchParams, navigator: { languages, language: languages[0] } });
  vm.runInContext(siteSource, context);
  vm.runInContext(analyticsSource, context);
  return {
    window, controls, writes, scripts, cookies, cleaned,
    switchLocale() { localeLink.click(); return localeLink.href; },
    get reloads() { return reloads; }, get focused() { return focused; },
    click(id) { controls[id].listeners.click(); },
    repeat() { vm.runInContext(analyticsSource, context); },
    commands() { return Array.from(window.dataLayer || [], (command) => Array.from(command)); },
  };
}

const fresh = visit();
assert.equal(fresh.controls["analytics-notice"].hidden, false, "Unknown consent must show the notice");
assert.equal(fresh.controls["analytics-settings"].hidden, false);
assert.equal(fresh.scripts.length, 0, "No Google script before consent");
assert.equal(fresh.window.dataLayer, undefined);
assert.deepEqual(fresh.writes, [], "Unknown consent does not create analytics storage");
fresh.click("analytics-reject");
assert.equal(fresh.scripts.length, 0, "Reject must never load Google");
assert.equal(fresh.controls["analytics-notice"].hidden, true);
assert.equal(fresh.cookies.get("sleep2story_analytics"), "denied");
assert.equal(fresh.reloads, 0);
assert.equal(fresh.focused, "", "An initial decision does not move keyboard focus to the footer");
fresh.click("analytics-settings");
assert.equal(fresh.controls["analytics-notice"].hidden, false);
assert.equal(fresh.focused, "analytics-title");

for (const preference of ["denied", "invalid", "granted-extra"]) {
  const page = visit({ cookie: `sleep2story_analytics=${preference}` });
  assert.equal(page.scripts.length, 0, `Unrecognized or denied consent (${preference}) cannot load Google`);
  assert.equal(page.controls["analytics-notice"].hidden, preference === "denied");
}

const accepted = visit({ path: "/ru/?utm_source=Newsletter&utm_campaign=Sleep%20Well&utm_medium=email&email=private@example.com#secret", referrer: "https://search.example/private?token=secret" });
accepted.click("analytics-accept");
accepted.click("analytics-accept");
accepted.repeat();
assert.equal(accepted.scripts.length, 1, "Only one Google tag per document");
assert.equal(accepted.scripts[0].src, `https://www.googletagmanager.com/gtag/js?id=${measurementId}`);
assert.equal(accepted.scripts[0].async, true);
assert.equal(accepted.scripts[0].referrerPolicy, "origin");
assert.equal(accepted.cookies.get("sleep2story_analytics"), "granted");
assert.equal(accepted.window[`ga-disable-${measurementId}`], false);
assert.equal(accepted.controls["analytics-notice"].hidden, true);
const commands = accepted.commands();
const configs = commands.filter(([command]) => command === "config");
assert.equal(configs.length, 1, "Only one automatic page_view configuration per document");
assert.equal(commands.filter(([command]) => command === "event").length, 0, "No extra custom events");
assert.equal(configs[0][1], measurementId);
const config = configs[0][2];
assert.equal(config.page_location, "https://sleep2story.com/ru/?utm_source=Newsletter&utm_campaign=Sleep%20Well&utm_medium=email");
assert.equal(config.page_referrer, "https://search.example");
assert.equal(config.cookie_expires, 180 * 24 * 60 * 60);
assert.equal(config.cookie_update, false);
assert.equal(config.cookie_domain, "none");
assert.equal(config.cookie_path, "/");
assert.equal(config.cookie_flags, "SameSite=Lax;Secure");
assert.equal(config.allow_google_signals, false);
assert.equal(config.allow_ad_personalization_signals, false);
assert.equal(Object.hasOwn(config, "debug_mode"), false, "Production config must omit debug_mode entirely");
const consent = commands.find(([command]) => command === "consent");
assert.equal(consent[1], "default");
assert.equal(consent[2].analytics_storage, "granted");
for (const key of ["ad_storage", "ad_user_data", "ad_personalization"]) assert.equal(consent[2][key], "denied");
assert.ok(commands.indexOf(consent) < commands.indexOf(configs[0]), "Consent must precede configuration");
assert.ok(accepted.writes.every((value) => /Max-Age=15552000; Path=\/; SameSite=Lax; Secure$/.test(value)));

const returning = visit({ cookie: "sleep2story_analytics=granted; _ga=old; _ga_HXBT0T7YQM=session; _ga_OTHER=other; _gid=legacy; _gat=legacy-throttle; sleep2story_locale=ru", origin: "https://www.sleep2story.com" });
assert.equal(returning.scripts.length, 1, "A remembered yes initializes analytics");
assert.deepEqual(returning.writes, [], "A revisit must not extend the preference lifetime");
returning.click("analytics-settings");
returning.click("analytics-reject");
assert.equal(returning.focused, "analytics-settings", "A reopened notice returns focus to its settings trigger");
assert.equal(returning.window[`ga-disable-${measurementId}`], true);
assert.equal(returning.cookies.get("sleep2story_analytics"), "denied");
assert.equal(returning.cookies.get("sleep2story_locale"), "ru");
assert.ok(!returning.cookies.has("_ga") && !returning.cookies.has("_ga_HXBT0T7YQM"));
assert.equal(returning.cookies.get("_ga_OTHER"), "other");
assert.equal(returning.cookies.get("_gid"), "legacy");
assert.equal(returning.cookies.get("_gat"), "legacy-throttle");
assert.equal(returning.reloads, 1, "Withdrawal reloads to stop already loaded code");
assert.ok(returning.writes.some((value) => value.includes("Domain=.sleep2story.com")), "Withdrawal clears parent-domain GA cookies too");

const local = visit({ cookie: "sleep2story_analytics=granted", origin: "http://localhost:8765" });
assert.equal(local.commands().find(([command]) => command === "config")[2].debug_mode, true);
assert.equal(local.commands().find(([command]) => command === "config")[2].cookie_flags, "SameSite=Lax");
const redirected = visit({ cookie: "sleep2story_analytics=granted", path: "/", languages: ["ru"] });
assert.equal(redirected.scripts.length, 0, "The automatic locale redirect cannot send a source-root page_view");
const referral = visit({ cookie: "sleep2story_analytics=granted", path: "/ru/?s2s_referrer=https%3A%2F%2Fnews.example%2Fsecret%3Ftoken%3D123&utm_source=news", referrer: "https://sleep2story.com/" });
const referralConfig = referral.commands().find(([command]) => command === "config")[2];
assert.equal(referralConfig.page_referrer, "https://news.example");
assert.equal(referralConfig.page_location, "https://sleep2story.com/ru/?utm_source=news");

const referralSource = visit({ path: "/ru/?utm_campaign=Sleep%20Well&utm_content=a+b#privacy", referrer: "https://NEWS.example/private?token=secret" });
const changedLocale = visit({ path: referralSource.switchLocale(), cookie: "sleep2story_locale=fr", referrer: "https://sleep2story.com/ru/" });
assert.deepEqual([...referralSource.cookies.keys()], ["sleep2story_locale"], "Locale handoff uses no analytics storage before consent");
assert.equal(referralSource.scripts.length, 0);
assert.equal(changedLocale.scripts.length, 0);
assert.deepEqual(changedLocale.writes, []);
changedLocale.click("analytics-accept");
const changedConfig = changedLocale.commands().find(([command]) => command === "config")[2];
assert.equal(changedConfig.page_referrer, "https://news.example", "An external referrer survives changing locale before first consent");
assert.equal(changedConfig.page_location, "https://sleep2story.com/fr/?utm_campaign=Sleep%20Well&utm_content=a+b");
assert.equal(changedLocale.cleaned, "/fr/?utm_campaign=Sleep%20Well&utm_content=a+b#privacy", "Transient referrer is removed from the landing URL");

console.log("Analytics consent checks passed");
