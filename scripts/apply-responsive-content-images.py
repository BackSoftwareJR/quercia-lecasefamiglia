#!/usr/bin/env python3
"""Convert bare AVIF <img> tags and JPG-only responsive imgs to full <picture> markup."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CARD_WIDTHS = [400, 640, 800, 1200]
FEATURE_WIDTHS = [640, 960, 1200, 1280]
SPLIT_WIDTHS = [400, 640, 800, 1200]

IMG_AVIF_RE = re.compile(
    r"<img(?P<attrs>(?:(?!>).)*?)src=\"(?P<base>/images/[^\"]+?)\.avif\"(?P<rest>(?:(?!>).)*?)>",
    re.IGNORECASE,
)

IMG_JPG_ONLY_RE = re.compile(
    r"<img(?P<attrs>(?:(?!>).)*?)src=\"(?P<base>/images/[^\"]+?)-(?P<fb>\d+)w\.jpg\""
    r"(?P<srcset>\s+srcset=\"[^\"]+\")(?P<rest>(?:(?!>).)*?)>",
    re.IGNORECASE,
)


def is_inside_picture(content: str, start: int) -> bool:
    before = content[:start]
    return before.count("<picture") > before.count("</picture>")


def attr_value(attrs: str, name: str) -> str | None:
    match = re.search(rf'{name}="([^"]*)"', attrs, re.IGNORECASE)
    return match.group(1) if match else None


def srcset(base: str, widths: list[int], ext: str) -> str:
    return ", ".join(f"{base}-{w}w.{ext} {w}w" for w in widths)


def pick_layout(display_w: int, css_class: str, loading: str) -> tuple[list[int], str, int]:
    if "blog-featured" in css_class or (loading == "eager" and display_w >= 1200):
        return FEATURE_WIDTHS, "(max-width: 1024px) 100vw, 1200px", 1200
    if "blog-card" in css_class or display_w <= 400:
        return CARD_WIDTHS, "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 400px", 800
    if display_w >= 800:
        return SPLIT_WIDTHS, "(max-width: 1024px) 100vw, 800px", 800
    if display_w >= 600:
        return [400, 640, 800], "(max-width: 1024px) 100vw, 600px", 640
    return [400, 640, 800], "(max-width: 1024px) 100vw, 640px", 640


def build_img_attrs(
    alt: str,
    width: str | None,
    height: str | None,
    css_class: str | None,
    style: str | None,
    loading: str,
    fetchpriority: str | None,
    img_id: str | None,
) -> str:
    parts: list[str] = []
    if img_id:
        parts.append(f'id="{img_id}"')
    if css_class:
        parts.append(f'class="{css_class}"')
    if width:
        parts.append(f'width="{width}"')
    if height:
        parts.append(f'height="{height}"')
    parts.append(f'loading="{loading}"')
    if fetchpriority:
        parts.append(f'fetchpriority="{fetchpriority}"')
    if loading != "eager":
        parts.append('decoding="async"')
    else:
        parts.append('decoding="async"')
    if style:
        parts.append(f'style="{style}"')
    parts.append(f'alt="{alt}"')
    return " ".join(parts)


def picture_for_avif(match: re.Match[str]) -> str:
    base = match.group("base")
    if re.search(r"-\d+w$", base):
        return match.group(0)

    attrs = match.group("attrs") + match.group("rest")
    alt = attr_value(attrs, "alt") or ""
    width = attr_value(attrs, "width")
    height = attr_value(attrs, "height")
    css_class = attr_value(attrs, "class")
    style = attr_value(attrs, "style")
    loading = attr_value(attrs, "loading") or "lazy"
    fetchpriority = attr_value(attrs, "fetchpriority")
    img_id = attr_value(attrs, "id")
    if loading == "eager" and not fetchpriority:
        fetchpriority = "high"

    display_w = int(width) if width and width.isdigit() else 640
    widths, sizes, fallback = pick_layout(display_w, css_class or "", loading)
    img_attrs = build_img_attrs(
        alt, width, height, css_class, style, loading, fetchpriority, img_id
    )

    return (
        f"<picture>\n"
        f'          <source type="image/avif" srcset="{srcset(base, widths, "avif")}" sizes="{sizes}">\n'
        f'          <source type="image/webp" srcset="{srcset(base, widths, "webp")}" sizes="{sizes}">\n'
        f'          <img {img_attrs} src="{base}-{fallback}w.jpg" '
        f'srcset="{srcset(base, widths, "jpg")}" sizes="{sizes}">\n'
        f"        </picture>"
    )


def picture_for_jpg(match: re.Match[str]) -> str:
    attrs = match.group("attrs") + match.group("rest")
    base = match.group("base")
    fallback = match.group("fb")
    alt = attr_value(attrs, "alt") or ""
    width = attr_value(attrs, "width")
    height = attr_value(attrs, "height")
    css_class = attr_value(attrs, "class")
    style = attr_value(attrs, "style")
    loading = attr_value(attrs, "loading") or "lazy"
    fetchpriority = attr_value(attrs, "fetchpriority")
    img_id = attr_value(attrs, "id")

    display_w = int(width) if width and width.isdigit() else int(fallback)
    widths, sizes, fb = pick_layout(display_w, css_class or "", loading)
    if int(fallback) not in widths:
        fb = int(fallback)
    img_attrs = build_img_attrs(
        alt, width, height, css_class, style, loading, fetchpriority, img_id
    )

    return (
        f"<picture>\n"
        f'          <source type="image/avif" srcset="{srcset(base, widths, "avif")}" sizes="{sizes}">\n'
        f'          <source type="image/webp" srcset="{srcset(base, widths, "webp")}" sizes="{sizes}">\n'
        f'          <img {img_attrs} src="{base}-{fb}w.jpg" '
        f'srcset="{srcset(base, widths, "jpg")}" sizes="{sizes}">\n'
        f"        </picture>"
    )


def process_content(content: str) -> str:
    def replace_avif(match: re.Match[str]) -> str:
        if is_inside_picture(content, match.start()):
            return match.group(0)
        return picture_for_avif(match)

    def replace_jpg(match: re.Match[str], source: str) -> str:
        if is_inside_picture(source, match.start()):
            return match.group(0)
        return picture_for_jpg(match)

    updated = IMG_AVIF_RE.sub(replace_avif, content)

    def jpg_sub(match: re.Match[str]) -> str:
        return replace_jpg(match, updated)

    updated = IMG_JPG_ONLY_RE.sub(jpg_sub, updated)
    return updated


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = process_content(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        print(f"OK {path.relative_to(ROOT)}")
        return True
    return False


def main() -> None:
    changed = 0
    for html in sorted(ROOT.rglob("*.html")):
        if "node_modules" in html.parts:
            continue
        if process_file(html):
            changed += 1
    print(f"Updated {changed} HTML file(s).")


if __name__ == "__main__":
    main()
