// One-off utility: regenerate PWA icons from the 512px feather source.
// Not part of build.sh — run manually with `npm run build:icons` whenever
// the source image changes. Output PNGs are committed to assets/images.
const sharp = require("sharp");
const path = require("path");

const SRC = path.resolve(__dirname, "..", "assets", "images", "feather_512.png");
const OUT_DIR = path.resolve(__dirname, "..", "assets", "images");

// feather_512.png is opaque with a black background already baked in, so we
// keep the same background when we need to add safe-zone padding.
const BG = { r: 0, g: 0, b: 0, alpha: 1 };

// padRatio = how much of the canvas the source occupies. 1.0 uses the source
// as-is (it already carries its own margin); < 1.0 shrinks it onto a black
// canvas to create the safe zone maskable icons need.
async function buildIcon(size, padRatio, filename, { alpha = true } = {}) {
  const inner = Math.round(size * padRatio);
  const offset = Math.round((size - inner) / 2);

  const featherBuffer = await sharp(SRC)
    .resize(inner, inner, { fit: "contain", kernel: "lanczos3" })
    .toBuffer();

  await sharp({
    create: { width: size, height: size, channels: 4, background: BG },
  })
    .composite([{ input: featherBuffer, left: offset, top: offset }])
    .png({ compressionLevel: 9 })
    .toFile(path.join(OUT_DIR, filename))
    .then(() => console.log(`Wrote ${filename} (${size}x${size}, inner ${inner}px)`));
}

async function main() {
  await buildIcon(192, 1.0, "icon-192.png");          // any
  await buildIcon(512, 1.0, "icon-512.png");          // any
  await buildIcon(512, 0.72, "icon-maskable-512.png"); // maskable safe zone
  await buildIcon(180, 1.0, "apple-touch-icon.png");  // iOS home screen
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
