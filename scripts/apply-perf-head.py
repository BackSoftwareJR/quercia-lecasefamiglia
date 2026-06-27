#!/usr/bin/env python3
"""Apply render-blocking optimizations to all HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRITICAL_CSS_PATH = ROOT / "css" / "critical.css"

RESOURCE_HINTS = """  <link rel="dns-prefetch" href="https://fonts.googleapis.com">
  <link rel="dns-prefetch" href="https://fonts.gstatic.com">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="dns-prefetch" href="https://maps.google.com">
  <link rel="preconnect" href="https://maps.google.com" crossorigin>"""

OLD_PRECONNECT_RE = re.compile(
    r"  <link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\">\n"
    r"  <link rel=\"preconnect\" href=\"https://fonts\.gstatic\.com\" crossorigin>\n",
    re.IGNORECASE,
)

BLOCKING_FONTS_RE = re.compile(
    r"^\s*<link (?:href=\"(https://fonts\.googleapis\.com/[^\"]+)\" rel=\"stylesheet\""
    r"|rel=\"stylesheet\" href=\"(https://fonts\.googleapis\.com/[^\"]+)\")\s*>\s*$",
    re.MULTILINE | re.IGNORECASE,
)

STYLESHEET_RE = re.compile(
    r"^  <link rel=\"stylesheet\" href=\"([^\"]+)\"\s*>$",
    re.MULTILINE | re.IGNORECASE,
)


def minify_css(css: str) -> str:
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)
    return css.strip()


def async_fonts_markup(url: str) -> str:
    return (
        f'  <link rel="preload" as="style" href="{url}" '
        f"onload=\"this.onload=null;this.rel='stylesheet'\">\n"
        f'  <noscript><link rel="stylesheet" href="{url}"></noscript>'
    )


def async_stylesheet_markup(href: str) -> str:
    return (
        f'  <link rel="stylesheet" href="{href}" media="print" onload="this.media=\'all\'">\n'
        f'  <noscript><link rel="stylesheet" href="{href}"></noscript>'
    )


def ensure_resource_hints(html: str) -> str:
    if 'rel="preconnect" href="https://maps.google.com"' in html:
        return html

    if OLD_PRECONNECT_RE.search(html):
        return OLD_PRECONNECT_RE.sub(RESOURCE_HINTS + "\n", html, count=1)

    critical_marker = '  <style id="critical-css">'
    if critical_marker in html:
        return html.replace(critical_marker, RESOURCE_HINTS + "\n" + critical_marker, 1)

    return html.replace("</head>", RESOURCE_HINTS + "\n</head>", 1)


def transform_blocking_fonts(html: str) -> str:
    def replace(match: re.Match[str]) -> str:
        url = match.group(1) or match.group(2)
        return async_fonts_markup(url)

    return BLOCKING_FONTS_RE.sub(replace, html)


def ensure_critical_css(html: str, critical_css: str) -> str:
    if 'id="critical-css"' in html:
        return html

    critical_block = f'  <style id="critical-css">{critical_css}</style>\n'
    marker = '  <link rel="preload" as="style" href="https://fonts.googleapis.com'
    if marker in html:
        return html.replace(marker, critical_block + marker, 1)

    hints_marker = '  <link rel="preconnect" href="https://maps.google.com" crossorigin>'
    if hints_marker in html:
        return html.replace(
            hints_marker,
            hints_marker + "\n" + critical_block.rstrip(),
            1,
        )

    return html.replace("</head>", critical_block + "</head>", 1)


def transform_stylesheets(html: str) -> str:
    return STYLESHEET_RE.sub(
        lambda match: async_stylesheet_markup(match.group(1)),
        html,
    )


def normalize_head_whitespace(html: str) -> str:
    html = re.sub(
        r'(type="image/avif">)\s+(<link rel="dns-prefetch")',
        r"\1\n  \2",
        html,
    )
    html = re.sub(
        r'(type="image/x-icon">)\s+(<link rel="dns-prefetch")',
        r"\1\n  \2",
        html,
    )
    return html


def transform_head(html: str, critical_css: str) -> tuple[str, bool]:
    updated = html
    updated = ensure_resource_hints(updated)
    updated = transform_blocking_fonts(updated)
    updated = ensure_critical_css(updated, critical_css)
    updated = transform_stylesheets(updated)
    updated = normalize_head_whitespace(updated)
    return updated, updated != html


def main() -> None:
    critical_css = minify_css(CRITICAL_CSS_PATH.read_text(encoding="utf-8"))
    changed = 0

    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        transformed, did_change = transform_head(original, critical_css)
        if did_change:
            path.write_text(transformed, encoding="utf-8")
            changed += 1
            print(f"updated: {path.relative_to(ROOT)}")

    print(f"Done. {changed} file(s) updated.")


if __name__ == "__main__":
    main()
