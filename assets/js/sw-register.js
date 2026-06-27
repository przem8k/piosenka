// Service worker registration. Everything else (precache, runtime
// caches, update flow) lives in service-worker.src.js.

(function () {
  if (!("serviceWorker" in navigator)) return;

  // Don't register on the Django dev server (port 8000): runserver
  // doesn't hash asset URLs, so the SW would cache unhashed files and
  // serve stale copies across restarts. To test the PWA locally, run
  // `bash build.sh && python -m http.server -d out 8001` instead.
  if (window.location.port === "8000") return;

  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/service-worker.js", { scope: "/" })
      .catch(function (err) {
        // SW failure shouldn't break the page; log + report (GA, already
        // loaded) so we hear about it without any extra dependency.
        console.warn("Service worker registration failed:", err);
        if (window.gtag) {
          gtag("event", "sw_register_failed", { description: String(err) });
        }
      });
  });
})();
