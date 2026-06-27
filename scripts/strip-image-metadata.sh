#!/usr/bin/env bash
# Strip EXIF/metadata from all raster images under images/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Stripping metadata from JPEG files…"
if command -v convert >/dev/null 2>&1; then
  find "$ROOT/images" -type f \( -iname '*.jpg' -o -iname '*.jpeg' \) -print0 | while IFS= read -r -d '' f; do
    convert "$f" -strip "$f"
  done
elif command -v exiftool >/dev/null 2>&1; then
  find "$ROOT/images" -type f \( -iname '*.jpg' -o -iname '*.jpeg' \) -print0 \
    | xargs -0 -r exiftool -overwrite_original -all= -q
else
  echo "Neither convert nor exiftool found — skip JPEG metadata strip."
fi

if command -v exiftool >/dev/null 2>&1; then
  echo "Stripping metadata from WebP/AVIF via exiftool…"
  find "$ROOT/images" -type f \( -iname '*.webp' -o -iname '*.avif' \) -print0 \
    | xargs -0 -r exiftool -overwrite_original -all= -q
else
  echo "exiftool not found — JPEG stripped; WebP/AVIF rely on encoder flags during generation."
fi

echo "Done."
