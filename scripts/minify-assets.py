#!/usr/bin/env python3
"""Minify CSS and JS assets for production deploy."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def minify_css(css: str) -> str:
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)
    return css.strip()


def minify_js(js: str) -> str:
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    js = re.sub(r"(?m)^\s*//.*$", "", js)
    js = re.sub(r"\s+", " ", js)
    js = re.sub(r"\s*([{}();,:=+\-*/<>!&|?\[\]])\s*", r"\1", js)
    return js.strip()


def minify_file(path: Path, minifier) -> int:
    original = path.read_text(encoding="utf-8")
    minified = minifier(original)
    if minified == original:
        return 0
    path.write_text(minified + "\n", encoding="utf-8")
    saved = len(original) - len(minified)
    print(f"  {path.relative_to(ROOT)}: {len(original)} → {len(minified)} bytes (-{saved})")
    return saved


def main() -> None:
    total_saved = 0
    for css_path in sorted((ROOT / "css").glob("*.css")):
        total_saved += minify_file(css_path, minify_css)
    for js_path in sorted((ROOT / "js").glob("*.js")):
        total_saved += minify_file(js_path, minify_js)
    print(f"Total saved: {total_saved} bytes")


if __name__ == "__main__":
    main()
