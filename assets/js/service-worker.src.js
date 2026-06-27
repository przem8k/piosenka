// Service worker source. workbox-build's injectManifest replaces the
// __WB_MANIFEST placeholder with the precache list at build time.

import {
  precacheAndRoute,
  createHandlerBoundToURL,
  cleanupOutdatedCaches,
} from "workbox-precaching";
import { registerRoute, setCatchHandler } from "workbox-routing";
import { StaleWhileRevalidate } from "workbox-strategies";
import { ExpirationPlugin } from "workbox-expiration";
import { CacheableResponsePlugin } from "workbox-cacheable-response";

// ---------------------------------------------------------------- known limitations
//
// Revisit when we next expand offline support (e.g. client-side song
// rendering) — the model may change enough that these dissolve.
//
//  1. App-shell skew after a deploy. Non-precached pages are cached as
//     you visit them (cache-first) and reference hashed CSS/JS from the
//     precache. A deploy installs new hashes and evicts the old ones, so a
//     page still in the html-pages cache points at an old hash. Viewed
//     OFFLINE after a deploy it can render unstyled (the subresource
//     404s; only navigations get the offline fallback). Online it
//     refetches fresh, so it self-heals.
//  2. Django values mirrored by hand. HTML_SECTIONS and MEDIA_HOST /
//     MEDIA_PATH_PREFIX below duplicate gen.py's URL sections and
//     settings.py's GCS location. This SW is a static esbuild bundle and
//     can't read Django settings, so a change there silently desyncs it
//     (a new section isn't runtime-cached; a moved bucket isn't cached)
//     with no build error. Fix when needed by emitting a generated config
//     from gen.py, or guard with a test.
//
// (Icons are likewise produced by a manual script CI doesn't run — see
// scripts/generate-icons.js.)

// ---------------------------------------------------------------- config

const DAY = 60 * 60 * 24;

// TEMP (squash before merge): build id stamped in by esbuild, reported to
// the page so the footer can show whether this SW is the latest build.
const BUILD_ID = typeof __BUILD_ID__ === "string" ? __BUILD_ID__ : "dev";

// Top-level URL prefixes that own HTML pages. Mirrors the directories
// gen.py writes under out/. Add a section here when gen.py grows a
// new top-level URL space.
const HTML_SECTIONS = /^\/(opracowanie|spiewnik|artykuly|blog|szukaj|o-stronie)(\/|$)/;

// Cover images, score thumbs etc. live on GCS — see settings.py
// (MEDIA_URL / GS_BUCKET_NAME). Mirroring those values here is the
// price of running on the SW side, where we can't read Django settings.
const MEDIA_HOST = "https://storage.googleapis.com";
const MEDIA_PATH_PREFIX = "/piosenka-media/";

const CACHEABLE_OK = new CacheableResponsePlugin({ statuses: [0, 200] });

function expire(maxEntries, days) {
  return new ExpirationPlugin({
    maxEntries,
    maxAgeSeconds: DAY * days,
    purgeOnQuotaError: true,
  });
}

const isSameOriginNavigation = (request, url) =>
  request.mode === "navigate" && url.origin === self.location.origin;

const HTML_CACHE = "html-pages";
const NET_TIMEOUT_MS = 3000;

// Bound a fetch with our own timer. iOS standalone PWAs don't reject a
// dead fetch promptly, and Workbox's networkTimeoutSeconds did not
// reliably fire there — so an offline navigation to an uncached page hung
// instead of falling through to offline.html. Racing fetch against an
// explicit setTimeout fixes it (and is a no-op where fetch already fails
// fast, i.e. every other browser).
function fetchWithTimeout(request, ms) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("network timeout")), ms);
    fetch(request).then(
      (resp) => { clearTimeout(timer); resolve(resp); },
      (err) => { clearTimeout(timer); reject(err); }
    );
  });
}

// FIFO-trim a runtime cache to a max entry count (we manage html-pages by
// hand now rather than through ExpirationPlugin).
async function trimCache(cacheName, maxEntries) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  for (const key of keys.slice(0, keys.length - maxEntries)) {
    await cache.delete(key);
  }
}

// ---------------------------------------------------------------- precache

cleanupOutdatedCaches();
precacheAndRoute(self.__WB_MANIFEST);

// TEMP (squash before merge): expose this SW's build via a fetch so the
// footer can read it reliably (iOS WebKit is flaky delivering postMessage
// replies from a service worker). An old SW without this route lets the
// request fall through to a 404, which is itself the "stale SW" signal.
registerRoute(
  ({ url }) => url.pathname === "/__sw-build__",
  () => new Response(BUILD_ID, { headers: { "content-type": "text/plain" } })
);

// ---------------------------------------------------------------- runtime caches

// Song / artist / article / blog pages. Cache-first: a page you've opened
// loads instantly from cache (refreshed in the background); a page you
// haven't opened tries the network with our hard timeout, then falls
// through to the catch handler's offline.html. The explicit timeout is
// what keeps an offline tap from hanging on iOS standalone.
registerRoute(
  ({ request, url }) =>
    isSameOriginNavigation(request, url) && HTML_SECTIONS.test(url.pathname),
  async ({ request, event }) => {
    const cache = await caches.open(HTML_CACHE);
    const cached = await cache.match(request);
    if (cached) {
      event.waitUntil(
        fetchWithTimeout(request, NET_TIMEOUT_MS)
          .then((resp) => {
            if (resp && resp.ok) {
              return cache
                .put(request, resp.clone())
                .then(() => trimCache(HTML_CACHE, 500));
            }
          })
          .catch(() => {})
      );
      return cached;
    }
    // Cache miss: bounded network. If it rejects (offline / timeout) the
    // catch handler serves offline.html.
    const resp = await fetchWithTimeout(request, NET_TIMEOUT_MS);
    if (resp && resp.ok) {
      event.waitUntil(
        cache.put(request, resp.clone()).then(() => trimCache(HTML_CACHE, 500))
      );
    }
    return resp;
  }
);

// The homepage and the other index pages are in the precache (see the
// navigation shell in build-sw.js), so they are served from there and
// the installed app launches offline. Individual song / artist / article
// / blog pages fall through to the StaleWhileRevalidate route above.

// Cover images + score thumbs served from GCS.
registerRoute(
  ({ url }) =>
    url.origin === MEDIA_HOST && url.pathname.startsWith(MEDIA_PATH_PREFIX),
  new StaleWhileRevalidate({
    cacheName: "media-images",
    plugins: [CACHEABLE_OK, expire(300, 90)],
  })
);

// Catch-all for any other same-origin navigation we have no specific rule
// for (a path outside HTML_SECTIONS): bounded network, then the catch
// handler's offline.html. Without this, a navigation that matches no route
// bypasses Workbox and the offline fallback never runs. Registered last so
// the specific routes above win first.
registerRoute(
  ({ request, url }) => isSameOriginNavigation(request, url),
  async ({ request }) => fetchWithTimeout(request, NET_TIMEOUT_MS)
);

// ---------------------------------------------------------------- update flow

// Activate a fresh SW as soon as it's installed and have it claim any
// open clients (browser tabs + installed PWA window). The site is a
// multi-page static — every link click is a full navigation — so the
// next navigation served by the new SW just delivers fresh content,
// with no UI ceremony around the update.
self.skipWaiting();
self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});


// ---------------------------------------------------------------- offline fallback

// When a navigation request fails and no cache entry exists, serve the
// precached offline page instead of the browser's default offline error.
const offlineFallback = createHandlerBoundToURL("/offline.html");
setCatchHandler(async (options) => {
  // Pass the full handler options (including `event`) — the precache
  // handler needs them to serve offline.html. Passing only { request }
  // left it unable to respond, so a failed navigation rendered blank
  // instead of the offline page.
  if (options.request.mode === "navigate") {
    return offlineFallback(options);
  }
  return Response.error();
});
