#!/usr/bin/env python3
"""Apply LCP picture + preload markup to hero images across HTML pages."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
HERO_WIDTHS = [640, 960, 1280, 1920]
PIN_DIR = "/images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/"
DINING = "/images/Sala%20da%20Pranzo%20%2B%20persone%201"


def encode_stem(stem: str) -> str:
    return quote(stem, safe="")


def srcset(dir_url: str, stem_enc: str, ext: str) -> str:
    return ", ".join(f"{dir_url}{stem_enc}-{w}w.{ext} {w}w" for w in HERO_WIDTHS)


def picture_markup(dir_url: str, stem_enc: str, alt: str, img_class: str = "hero-clean__fallback", img_id: str | None = None) -> str:
    id_attr = f' id="{img_id}"' if img_id else ""
    return f"""<picture>
          <source type="image/avif" srcset="{srcset(dir_url, stem_enc, "avif")}" sizes="100vw">
          <source type="image/webp" srcset="{srcset(dir_url, stem_enc, "webp")}" sizes="100vw">
          <img{id_attr} class="{img_class}" src="{dir_url}{stem_enc}-1280w.jpg" srcset="{srcset(dir_url, stem_enc, "jpg")}" sizes="100vw" alt="{alt}" width="1920" height="1080" loading="eager" fetchpriority="high" decoding="async">
        </picture>"""


def page_hero_picture(dir_url: str, stem_enc: str, alt: str) -> str:
    return f"""<picture>
          <source type="image/avif" srcset="{srcset(dir_url, stem_enc, "avif")}" sizes="(max-width: 1024px) 100vw, 1200px">
          <source type="image/webp" srcset="{srcset(dir_url, stem_enc, "webp")}" sizes="(max-width: 1024px) 100vw, 1200px">
          <img src="{dir_url}{stem_enc}-1280w.jpg" srcset="{srcset(dir_url, stem_enc, "jpg")}" sizes="(max-width: 1024px) 100vw, 1200px" alt="{alt}" width="1200" height="514" loading="eager" fetchpriority="high" decoding="async">
        </picture>"""


def preload_link(dir_url: str, stem_enc: str) -> str:
    return (
        f'  <link rel="preload" as="image" href="{dir_url}{stem_enc}-1280w.avif" '
        f'imagesrcset="{srcset(dir_url, stem_enc, "avif")}" imagesizes="100vw" '
        f'fetchpriority="high" type="image/avif">'
    )


def insert_preload(head: str, link: str) -> str:
    if link.strip() in head:
        return head
    marker = '<link rel="preconnect" href="https://fonts.googleapis.com">'
    if marker in head:
        return head.replace(marker, link + "\n  " + marker, 1)
    return head.replace("</head>", link + "\n</head>", 1)


HERO_IMG1 = (
    PIN_DIR,
    "img1",
    "Sala luminosa e accogliente di Casa Famiglia Castelletto a Pinerolo, residenza per anziani autosufficienti",
)
HERO_DINING = (
    "/images/",
    "Sala%20da%20Pranzo%20%2B%20persone%201",
    "Pasto conviviale in sala da pranzo — vita quotidiana a Casa Famiglia Castelletto, Pinerolo",
)

PAGE_HERO_UPDATES = {
    "servizi/index.html": HERO_IMG1,
    "rette-e-ammissione/index.html": (PIN_DIR, "img7", "Camera confortevole di Casa Famiglia Castelletto a Pinerolo — retta trasparente e ambiente familiare"),
    "contatti/index.html": (PIN_DIR, "img9", "Giardino e dintorni verdi di Casa Famiglia Castelletto — Stradale Poirino 152, Pinerolo"),
    "la-giornata/index.html": HERO_DINING,
    "chi-siamo/index.html": (PIN_DIR, "img12", "Esterno di Casa Famiglia Castelletto nel verde del Pinerolese"),
    "la-struttura/index.html": (PIN_DIR, "img1", "Salone luminoso di Casa Famiglia Castelletto a Pinerolo"),
}

HERO_IMG_RE = re.compile(
    r'<img(?:\s+id="heroFallback")?\s+class="hero-clean__fallback"\s+src="([^"]+)"\s+alt="([^"]*)"\s+width="1920"\s+height="1080"\s+loading="eager"\s+fetchpriority="high">',
    re.MULTILINE,
)

PAGE_HERO_IMG_RE = re.compile(
    r'<img\s+src="(/images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/img\d+)\.avif"\s+alt="([^"]*)"\s+width="1200"\s+height="514"\s+loading="eager"\s+fetchpriority="high">',
)


def process_hero_clean(rel: str, dir_url: str, stem_enc: str, alt: str) -> bool:
    path = ROOT / rel
    content = path.read_text(encoding="utf-8")
    original = content

    pic = picture_markup(dir_url, stem_enc, alt)
    content = HERO_IMG_RE.sub(pic, content, count=1)

    preload = preload_link(dir_url, stem_enc)
    content = insert_preload(content, preload)

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"OK hero-clean {rel}")
        return True
    return False


def process_page_hero(rel: str, dir_url: str, stem_enc: str, alt: str) -> bool:
    path = ROOT / rel
    content = path.read_text(encoding="utf-8")
    original = content

    def repl(match: re.Match[str]) -> str:
        return page_hero_picture(dir_url, stem_enc, alt)

    content = PAGE_HERO_IMG_RE.sub(repl, content, count=1)
    preload = preload_link(dir_url, stem_enc).replace('imagesizes="100vw"', 'imagesizes="(max-width: 1024px) 100vw, 1200px"')
    content = insert_preload(content, preload)

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"OK page-hero {rel}")
        return True
    return False


def main() -> None:
    changed = 0
    for rel, (dir_url, stem, alt) in PAGE_HERO_UPDATES.items():
        stem_enc = stem if "%" in stem else stem
        if rel in ("chi-siamo/index.html", "la-struttura/index.html"):
            if process_page_hero(rel, dir_url, stem_enc, alt):
                changed += 1
        elif process_hero_clean(rel, dir_url, stem_enc, alt):
            changed += 1
    print(f"Updated {changed} pages.")


if __name__ == "__main__":
    main()
