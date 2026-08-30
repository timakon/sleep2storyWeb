import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";

const source = fs.readFileSync(new URL("../assets/site.js", import.meta.url), "utf8");

function redirectFor({ languages, cookie = "", pathname = "/", hash = "" }) {
  let redirect = "";
  const location = {
    pathname,
    hash,
    replace(url) {
      redirect = url;
    },
    assign() {},
  };
  vm.runInNewContext(source, {
    document: { cookie, querySelectorAll: () => [] },
    navigator: { languages, language: languages[0] },
    window: { location },
  });
  return redirect;
}

assert.equal(redirectFor({ languages: ["ru-RU", "en-US"] }), "/ru/");
assert.equal(redirectFor({ languages: ["sr-Latn-RS"], hash: "#inside" }), "/sr/#inside");
assert.equal(redirectFor({ languages: ["ja-JP"] }), "");
assert.equal(redirectFor({ languages: ["ru-RU"], cookie: "sleep2story_locale=en" }), "");
assert.equal(
  redirectFor({ languages: ["ru-RU"], cookie: "sleep2story_locale=de" }),
  "/de/",
);
assert.equal(redirectFor({ languages: ["ru-RU"], pathname: "/fr/" }), "");

console.log("Locale redirect checks passed");
