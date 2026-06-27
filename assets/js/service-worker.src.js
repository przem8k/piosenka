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

// ---------------------------------------------------------------- runtime caches

// Song / artist / article / blog pages. Network-first so online visits
// are always fresh; once visited they keep working offline from cache.
// The network timeout is critical: an iOS standalone PWA does NOT always
// fail an offline fetch promptly, so without a cap a tap to an unvisited
// page (e.g. a search result) hangs forever with no way back. On timeout
// we serve the cached page if visited, else the catch handler's
// offline.html.
registerRoute(
  ({ request, url }) =>
    isSameOriginNavigation(request, url) && HTML_SECTIONS.test(url.pathname),
  new NetworkFirst({
    cacheName: "html-pages",
    networkTimeoutSeconds: 3,
    plugins: [CACHEABLE_OK, expire(500, 30)],
  })
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
setCatchHandler(async ({ request }) => {
  if (request.mode === "navigate") {
    return offlineFallback({ request });
  }
  return Response.error();
});
