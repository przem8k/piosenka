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
      // App shell: django-compress concatenates every CSS/JS the HTML
      // links (third-party + per-feature) into these hashed bundles, so
      // the individual source files are never requested in production.
      "static/CACHE/**/*.{js,css}",
      // Glyphicons fonts are pulled by url() from the bundled CSS, so
      // they are NOT inside the CACHE bundle. Modern browsers load woff;
      // ttf is the fallback (eot/svg only matter to engines that can't
      // run a service worker anyway).
      "static/third_party/glyphicons/**/*.{woff,ttf}",
      // Icons the pages actually reference: navbar logo, favicon, PWA.
      "static/images/icon-192.png",
      "static/images/icon-512.png",
      "static/images/icon-maskable-512.png",
      "static/images/apple-touch-icon.png",
      "static/images/favicon.ico",
      "static/images/feather_40.png",
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
    ],
  });

  // Drop the intermediate bundled file so it doesn't get deployed.
  require("fs").unlinkSync(BUNDLED);

  // injectManifest only WARNS (and still exits 0) when a globPattern
  // matches no files. That would silently ship a service worker missing
  // a precache entry, so fail the build instead and let CI catch it.
  if (result.warnings.length) {
    console.error("Service worker precache warnings:\n" + result.warnings.join("\n"));
    throw new Error(
      `injectManifest produced ${result.warnings.length} warning(s) ` +
        `(likely a globPattern that matched no files). Failing the build.`
    );
  }

  console.log(
    `Service worker written to ${path.relative(ROOT, OUT)} ` +
      `(precaching ${result.count} URLs, ` +
      `${(result.size / 1024 / 1024).toFixed(2)} MB).`
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
