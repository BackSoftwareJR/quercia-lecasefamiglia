#!/usr/bin/env bash
# Generate responsive AVIF, WebP, and JPEG variants for site images.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WIDTHS=(400 640 800 960 1200 1280 1920)
QUALITY_JPG=80
TMP="${TMPDIR:-/tmp}/cfq-responsive-$$"
mkdir -p "$TMP"

cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

generate_variants() {
  local src="$1"
  local dir base stem
  dir="$(dirname "$src")"
  base="$(basename "$src")"
  stem="${base%.avif}"

  echo "→ $base"
  avifdec "$src" "$TMP/src.png" >/dev/null

  for w in "${WIDTHS[@]}"; do
    local jpg="$dir/${stem}-${w}w.jpg"
    local webp="$dir/${stem}-${w}w.webp"
    local avif="$dir/${stem}-${w}w.avif"

    convert "$TMP/src.png" -resize "${w}x" -strip -quality "$QUALITY_JPG" "$jpg"
    cwebp -quiet -q "$QUALITY_JPG" "$jpg" -o "$webp"
    avifenc --min 20 --max 35 --speed 6 "$jpg" "$avif" >/dev/null
  done
}

shopt -s nullglob
for img in "$ROOT/images/Pinerolo - Casa Famiglia Quercia 1"/*.avif; do
  generate_variants "$img"
done

for img in "$ROOT/images"/*.avif; do
  generate_variants "$img"
done

echo "Done. Responsive variants written next to each source AVIF."
