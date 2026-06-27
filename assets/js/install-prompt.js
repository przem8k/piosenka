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

  function dismissedRecently() {
    try {
      var ts = parseInt(localStorage.getItem(STORAGE_KEY) || "", 10);
      return ts && Date.now() - ts < DISMISS_DAYS * 86400000;
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
    return /iPhone|iPad|iPod/.test(ua)
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

  if (isStandalone() || dismissedRecently()) return;

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
        deferredPrompt.userChoice.finally(function () {
          deferredPrompt = null;
          banner.remove();
          recordDismiss();
        });
      },
    });
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
