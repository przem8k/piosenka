// Bundle the service worker source with esbuild, then run
// workbox-build's injectManifest on the bundled output to inject the
// precache list in place of `self.__WB_MANIFEST`.
//
// Why this shape:
//   - injectManifest (not generateSW): we want to own SW behavior —
//     a custom catch handler for offline fallback and per-route
//     runtime caches — which generateSW's config doesn't fully expose.
//   - esbuild before injectManifest: workbox-build v7 expects an
//     already-bundled SW; it inlines the precache manifest but won't
//     resolve Workbox imports for us.
//   - Workbox is bundled into the SW output (not loaded from a CDN)
//     so the PWA has no external runtime dependency — important for
//     offline-first.

const path = require("path");
const esbuild = require("esbuild");
const { injectManifest } = require("workbox-build");

const ROOT = path.resolve(__dirname, "..");
const SRC = path.join(ROOT, "assets", "js", "service-worker.src.js");
const BUNDLED = path.join(ROOT, "out", "_service-worker.bundled.js");
const OUT = path.join(ROOT, "out", "service-worker.js");

async function main() {
  await esbuild.build({
    entryPoints: [SRC],
    bundle: true,
    outfile: BUNDLED,
    format: "iife",
    target: "es2020",
    minify: true,
    sourcemap: false,
    logLevel: "warning",
  });

  const result = await injectManifest({
    swSrc: BUNDLED,
    swDest: OUT,
    globDirectory: path.join(ROOT, "out"),
    globPatterns: [
      // App shell: the django-compress bundles HTML actually loads.
      "static/CACHE/**/*.{js,css}",
      "static/css/install-prompt.css",
      // Third-party CSS/JS bundled into the same compress block.
      "static/third_party/bootstrap/css/bootstrap.min.css",
      "static/third_party/bootstrap/js/bootstrap.bundle.min.js",
      "static/third_party/glyphicons/**/*.{css,woff,woff2,ttf,eot,svg}",
      "static/third_party/luminous/luminous.min.js",
      "static/third_party/luminous/luminous-basic.min.css",
      // App icons + favicons.
      "static/images/icon-192.png",
      "static/images/icon-512.png",
      "static/images/icon-maskable-512.png",
      "static/images/apple-touch-icon.png",
      "static/images/favicon*.png",
      "static/images/feather*.png",
      // Search index — precached so search works offline from the
      // first visit (~200 KB today, the primary entry point for the site).
      "index/*.json",
      "manifest.webmanifest",
      "offline.html",
    ],
    globIgnores: [
      "**/node_modules/**",
      "**/*.map",
      "_service-worker.bundled.js",
      // Individual unbundled JS / per-feature CSS — django-compress
      // already bundled them into static/CACHE/*, which is what HTML loads.
      "static/js/**",
      "static/css/{comments,dark,lightbox,search,song,style,output}.css",
    ],
  });

  // Drop the intermediate bundled file so it doesn't get deployed.
  require("fs").unlinkSync(BUNDLED);

  console.log(
    `Service worker written to ${path.relative(ROOT, OUT)} ` +
      `(precaching ${result.count} URLs, ` +
      `${(result.size / 1024 / 1024).toFixed(2)} MB).`
  );
  if (result.warnings.length) {
    console.warn("Warnings:", result.warnings);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
