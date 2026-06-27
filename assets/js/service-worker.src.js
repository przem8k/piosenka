// Service worker source. workbox-build's injectManifest replaces the
// __WB_MANIFEST placeholder with the precache list at build time.

import {
  precacheAndRoute,
  createHandlerBoundToURL,
  cleanupOutdatedCaches,
} from "workbox-precaching";
import { registerRoute, setCatchHandler, NavigationRoute } from "workbox-routing";
import { StaleWhileRevalidate, NetworkFirst, NetworkOnly } from "workbox-strategies";
import { ExpirationPlugin } from "workbox-expiration";
import { CacheableResponsePlugin } from "workbox-cacheable-response";

// ---------------------------------------------------------------- known limitations
//
// Revisit when we next expand offline support (e.g. client-side song
// rendering) — the model may change enough that these dissolve.
//
//  1. App-shell skew after a deploy. Non-precached pages are cached as
//     you visit them (NetworkFirst) and reference hashed CSS/JS from the
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

// Song / artist / article / blog pages. A page you've already opened is
// served instantly from cache and refreshed in the background; a page you
// haven't opened tries the network with a hard 3s timeout, then falls
// back to the catch handler's offline.html. The timeout only ever fires
// on iOS standalone, where an offline fetch can hang instead of failing —
// elsewhere fetch rejects in milliseconds and the cap is never reached.
// (Cache-first read on top of NetworkFirst so saved pages stay instant
// offline; NetworkFirst alone would make every offline read wait 3s.)
const pageStrategy = new NetworkFirst({
  cacheName: "html-pages",
  networkTimeoutSeconds: 3,
  plugins: [CACHEABLE_OK, expire(500, 30)],
});
registerRoute(
  ({ request, url }) =>
    isSameOriginNavigation(request, url) && HTML_SECTIONS.test(url.pathname),
  async (params) => {
    const cache = await caches.open("html-pages");
    const cached = await cache.match(params.request);
    if (cached) {
      // Refresh in the background; the strategy's own timeout keeps this
      // bounded so it can't leak a hung fetch.
      params.event.waitUntil(pageStrategy.handle(params).catch(() => {}));
      return cached;
    }
    return pageStrategy.handle(params);
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
// for: hit the network, and when that fails offline the catch handler
// below serves offline.html. Without this, a navigation that matches no
// route bypasses Workbox entirely and the offline fallback never runs —
// on iOS that shows up as a dead tap (nothing happens) rather than the
// offline page. Registered last so the specific routes above win first.
registerRoute(new NavigationRoute(new NetworkOnly({ networkTimeoutSeconds: 3 })));

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
