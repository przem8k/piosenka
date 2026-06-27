// "Add to home screen" prompt. Markup lives in the
// #pzt-install-banner-tpl <template> in base.html so we keep HTML in
// HTML; this file clones the template and wires up the two install
// paths the platforms give us:
//
//   - Chrome / Edge / Android Chrome: the browser fires a
//     `beforeinstallprompt` event when the site meets PWA install
//     criteria. We preventDefault() to suppress the browser's own
//     mini-infobar, show our banner instead, then call deferredPrompt
//     .prompt() on click to bring up the native install dialog.
//   - iOS Safari: no programmatic install API exists, so we show an
//     instructional banner pointing at Share → Add to Home Screen.

(function () {
  var STORAGE_KEY = "pzt_install_prompt_dismissed";
  var DISMISS_DAYS = 30;
  var BANNER_ID = "pzt-install-banner";

  function track(name, params) {
    if (window.gtag) window.gtag("event", name, params || {});
  }

  function dismissedRecently() {
    try {
      var ts = parseInt(localStorage.getItem(STORAGE_KEY) || "", 10);
      if (!Number.isFinite(ts)) return false;
      // age < 0 means a future-dated timestamp (clock moved back, or a
      // corrupt value) — treat as not-dismissed so the banner can show.
      var age = Date.now() - ts;
      return age >= 0 && age < DISMISS_DAYS * 86400000;
    } catch (e) {
      return false;
    }
  }

  function recordDismiss() {
    try { localStorage.setItem(STORAGE_KEY, String(Date.now())); } catch (e) {}
  }

  function isStandalone() {
    return (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches)
      || window.navigator.standalone === true;
  }

  function isIosSafari() {
    var ua = window.navigator.userAgent;
    // iPadOS 13+ Safari reports a "Macintosh" desktop UA; a touch point
    // count > 1 distinguishes it from a real Mac. Then exclude the
    // non-Safari iOS browsers, which tag themselves (CriOS/FxiOS/EdgiOS).
    var isIos = /iPhone|iPad|iPod/.test(ua)
      || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
    return isIos
      && /WebKit/.test(ua)
      && !/CriOS|FxiOS|EdgiOS/.test(ua);
  }

  // Touch devices (phones / tablets). Desktop Chrome already offers an
  // address-bar install icon, so we skip the banner there.
  function isTouchDevice() {
    return !!(window.matchMedia && window.matchMedia("(pointer: coarse)").matches);
  }

  // Clone the install-banner template, reveal the text variant for this
  // platform and the optional action button, wire up close, append to
  // the page. All copy lives in the template (base.html), not here.
  function showBanner(opts) {
    if (document.getElementById(BANNER_ID)) return;
    var tpl = document.getElementById("pzt-install-banner-tpl");
    if (!tpl) return;
    var banner = tpl.content.cloneNode(true).firstElementChild;
    var text = banner.querySelector(".pzt-install-text-" + opts.variant);
    if (text) text.hidden = false;

    var action = banner.querySelector(".pzt-install-action");
    if (opts.onAction) {
      action.hidden = false;
      action.addEventListener("click", function () { opts.onAction(banner); });
    }

    banner.querySelector(".pzt-install-close").addEventListener("click", function () {
      recordDismiss();
      banner.remove();
    });

    document.body.appendChild(banner);
    return banner;
  }

  if (isStandalone()) track("pwa_launch_standalone");
  if (isStandalone() || dismissedRecently()) return;

  // Fired when the user completes installation (platforms that support
  // it) — lets us measure real installs, not just prompts shown.
  window.addEventListener("appinstalled", function () {
    track("pwa_installed");
  });

  // ---- native (Chrome / Edge / Android Chrome) ----
  var deferredPrompt = null;
  window.addEventListener("beforeinstallprompt", function (e) {
    if (isStandalone() || dismissedRecently()) return;
    if (!isTouchDevice()) return;
    e.preventDefault();
    deferredPrompt = e;
    showBanner({
      variant: "native",
      onAction: function (banner) {
        if (!deferredPrompt) { banner.remove(); return; }
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function (choice) {
          var outcome = choice && choice.outcome;
          track(outcome === "accepted" ? "pwa_install_accepted"
                                       : "pwa_install_dismissed");
          // Only suppress future banners if the user declined. On accept
          // the app becomes standalone (isStandalone() hides the banner);
          // recording a dismissal would also keep it hidden for 30 days
          // if they later uninstall.
          if (outcome === "dismissed") recordDismiss();
        }).finally(function () {
          deferredPrompt = null;
          banner.remove();
        });
      },
    });
    track("pwa_install_prompt_shown");
  });

  // ---- iOS Safari (no programmatic install API) ----
  if (isIosSafari()) {
    var scheduleIosBanner = function () {
      setTimeout(function () {
        showBanner({ variant: "ios" });
      }, 1200);
    };
    if (document.readyState === "complete") scheduleIosBanner();
    else window.addEventListener("load", scheduleIosBanner);
  }
})();
