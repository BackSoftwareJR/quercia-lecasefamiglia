#!/usr/bin/env python3
"""Upgrade blog article hero images to responsive picture elements."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIDTHS = [640, 960, 1200, 1280]
PIN = "/images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/"
DINING_STEM = "Sala%20da%20Pranzo%20%2B%20persone%201"

BLOG_HERO_RE = re.compile(
    r'<img\s+src="(/images/(?:Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/img\d+|Sala%20da%20Pranzo%20%2B%20persone%201))\.avif"\s+'
    r'alt="([^"]*)"\s+width="1200"\s+height="630"\s+loading="eager"\s+fetchpriority="high">'
)


def srcset(base: str, ext: str) -> str:
    return ", ".join(f"{base}-{w}w.{ext} {w}w" for w in WIDTHS)


def picture_for(base: str, alt: str) -> str:
    return f"""<picture>
        <source type="image/avif" srcset="{srcset(base, 'avif')}" sizes="(max-width: 1024px) 100vw, 1200px">
        <source type="image/webp" srcset="{srcset(base, 'webp')}" sizes="(max-width: 1024px) 100vw, 1200px">
        <img src="{base}-1200w.jpg" srcset="{srcset(base, 'jpg')}" sizes="(max-width: 1024px) 100vw, 1200px" alt="{alt}" width="1200" height="630" loading="eager" fetchpriority="high" decoding="async">
      </picture>"""


def preload_for(base: str) -> str:
    return (
        f'  <link rel="preload" as="image" href="{base}-1200w.avif" '
        f'imagesrcset="{srcset(base, "avif")}" '
        f'imagesizes="(max-width: 1024px) 100vw, 1200px" fetchpriority="high" type="image/avif">'
    )


def process(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    match = BLOG_HERO_RE.search(content)
    if not match:
        return False

    base, alt = match.group(1), match.group(2)
    updated = BLOG_HERO_RE.sub(picture_for(base, alt), content, count=1)
    link = preload_for(base)
    if link not in updated:
        marker = '<link rel="preconnect" href="https://fonts.googleapis.com">'
        updated = updated.replace(marker, link + "\n  " + marker, 1)

    if updated != content:
        path.write_text(updated, encoding="utf-8")
        print(f"OK {path.relative_to(ROOT)}")
        return True
    return False


def main() -> None:
    changed = sum(process(p) for p in ROOT.glob("blog/**/index.html"))
    print(f"Updated {changed} blog articles.")


if __name__ == "__main__":
    main()
