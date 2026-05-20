// Service worker source. workbox-build's injectManifest replaces the
// __WB_MANIFEST placeholder with the precache list at build time.

import {
  precacheAndRoute,
  createHandlerBoundToURL,
  cleanupOutdatedCaches,
} from "workbox-precaching";
import { registerRoute, setCatchHandler } from "workbox-routing";
import { StaleWhileRevalidate, NetworkFirst } from "workbox-strategies";
import { ExpirationPlugin } from "workbox-expiration";
import { CacheableResponsePlugin } from "workbox-cacheable-response";

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

// Song / artist / article / blog pages. Once visited they keep working
// offline; Workbox refreshes them in the background on revisit.
registerRoute(
  ({ request, url }) =>
    isSameOriginNavigation(request, url) && HTML_SECTIONS.test(url.pathname),
  new StaleWhileRevalidate({
    cacheName: "html-pages",
    plugins: [CACHEABLE_OK, expire(500, 30)],
  })
);

// Homepage: changes more often than song pages, so prefer the network
// with a short timeout before falling back to the last cached copy.
registerRoute(
  ({ request, url }) =>
    isSameOriginNavigation(request, url) && url.pathname === "/",
  new NetworkFirst({
    cacheName: "homepage",
    networkTimeoutSeconds: 4,
    plugins: [CACHEABLE_OK, expire(1, 7)],
  })
);

// Cover images + score thumbs served from GCS.
registerRoute(
  ({ url }) =>
    url.origin === MEDIA_HOST && url.pathname.startsWith(MEDIA_PATH_PREFIX),
  new StaleWhileRevalidate({
    cacheName: "media-images",
    plugins: [CACHEABLE_OK, expire(300, 90)],
  })
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
setCatchHandler(async ({ request }) => {
  if (request.mode === "navigate") {
    return offlineFallback({ request });
  }
  return Response.error();
});
