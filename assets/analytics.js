(() => {
  if (window.sleep2storyRedirecting || window.sleep2storyAnalyticsInitialized) return;
  window.sleep2storyAnalyticsInitialized = true;

  const measurementId = "G-HXBT0T7YQM";
  const lifetime = 180 * 24 * 60 * 60;
  const secure = window.location.protocol === "https:";
  const notice = document.getElementById("analytics-notice");
  const settings = document.getElementById("analytics-settings");
  const preference = document.cookie.split(";").map((part) => part.trim())
    .find((part) => part.startsWith("sleep2story_analytics="))?.split("=")[1];
  let started = false;
  let openedFromSettings = false;

  function startAnalytics() {
    if (started) return;
    started = true;
    window[`ga-disable-${measurementId}`] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("consent", "default", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
    window.gtag("set", "ads_data_redaction", true);
    window.gtag("js", new Date());
    window.gtag("config", measurementId, {
      page_location: window.sleep2storyPageLocation,
      page_referrer: window.sleep2storyReferrer,
      cookie_domain: "none",
      cookie_path: "/",
      cookie_expires: lifetime,
      cookie_update: false,
      cookie_flags: `SameSite=Lax${secure ? ";Secure" : ""}`,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      ...(["localhost", "127.0.0.1", "[::1]"].includes(window.location.hostname) ? { debug_mode: true } : {}),
    });
    const script = document.createElement("script");
    script.async = true;
    script.referrerPolicy = "origin";
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    document.head.appendChild(script);
  }

  function choose(preference) {
    document.cookie = `sleep2story_analytics=${preference}; Max-Age=${lifetime}; Path=/; SameSite=Lax${secure ? "; Secure" : ""}`;
    notice.hidden = true;
    settings.setAttribute("aria-expanded", "false");
    if (openedFromSettings) settings.focus({ preventScroll: true });
    if (preference === "granted") {
      startAnalytics();
      return;
    }
    window[`ga-disable-${measurementId}`] = true;
    const domains = [""];
    const labels = window.location.hostname.split(".");
    for (let index = 0; index < labels.length - 1; index += 1) {
      domains.push(`; Domain=.${labels.slice(index).join(".")}`);
    }
    document.cookie.split(";").map((part) => part.trim().split("=")[0])
      .filter((name) => name === "_ga" || name === `_ga_${measurementId.slice(2)}`)
      .forEach((name) => {
        domains.forEach((domain) => {
          document.cookie = `${name}=; Max-Age=0; Path=/${domain}; SameSite=Lax${secure ? "; Secure" : ""}`;
        });
      });
    if (started) window.location.reload();
  }

  settings.hidden = false;
  notice.hidden = preference === "granted" || preference === "denied";
  settings.setAttribute("aria-expanded", String(!notice.hidden));
  settings.addEventListener("click", () => {
    openedFromSettings = true;
    notice.hidden = false;
    settings.setAttribute("aria-expanded", "true");
    document.getElementById("analytics-title").focus({ preventScroll: true });
  });
  document.getElementById("analytics-accept").addEventListener("click", () => choose("granted"));
  document.getElementById("analytics-reject").addEventListener("click", () => choose("denied"));
  window[`ga-disable-${measurementId}`] = preference !== "granted";
  if (preference === "granted") startAnalytics();
})();
