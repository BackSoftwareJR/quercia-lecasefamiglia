#!/usr/bin/env python3
"""Rebrand Casa Famiglia Quercia → Castelletto (commercial name), keeping Quercia in SEO/legal refs."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BRAND = "Casa Famiglia Castelletto"
BRAND_SHORT = "Casa Castelletto"
FORMER_BRAND = "Casa Famiglia Quercia"
FORMER_SHORT = "Casa Quercia"
SEO_KEYWORDS_EXTRA = "casa famiglia castelletto Pinerolo, casa famiglia quercia Pinerolo"

PROTECTED = [
    ("Quercia S.r.l.s.", "__LEGAL_QUERCIA_SRLS__"),
    ("casafamigliaquercia.it", "__DOMAIN_CFQ__"),
    ("info@casafamigliaquercia.it", "__EMAIL_CFQ__"),
    ("quercia.lecasefamiglia.it", "__DOMAIN_LEGACY__"),
    ("Pinerolo - Casa Famiglia Quercia 1", "__IMG_DIR_PLAIN__"),
    ("Pinerolo%20-%20Casa%20Famiglia%20Quercia%201", "__IMG_DIR_ENC__"),
    ("quercia_cookie_consent", "__COOKIE_KEY__"),
    ("QuerciaTokens", "__TOKENS_GLOBAL__"),
    ('"name": "casafamigliaquercia"', "__PKG_NAME__"),
]

SCAN_SUFFIXES = {".html", ".js", ".md", ".py", ".json", ".css", ".txt", ".xml"}
SKIP_DIRS = {".git", "node_modules", ".cursor"}
SKIP_FILES = {"rename-to-castelletto.py", "googled383cece6ecba048.html"}


def protect(text: str) -> str:
    for original, placeholder in PROTECTED:
        text = text.replace(original, placeholder)
    return text


def restore(text: str) -> str:
    for original, placeholder in reversed(PROTECTED):
        text = text.replace(placeholder, original)
    return text


def rebrand(text: str) -> str:
    text = protect(text)
    # Preserve former-name references before generic brand swap
    text = text.replace(f"(ex {FORMER_BRAND})", "__EX_FORMER_BRAND__")
    text = text.replace(FORMER_BRAND, BRAND)
    text = text.replace(FORMER_SHORT, BRAND_SHORT)
    text = text.replace("__EX_FORMER_BRAND__", f"(ex {FORMER_BRAND})")
    return restore(text)


def patch_json_ld(content: str) -> str:
    """Add alternateName to schema.org entities that use the commercial brand name."""

    def patch_block(match: re.Match[str]) -> str:
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)

        changed = False

        def visit(node):
            nonlocal changed
            if isinstance(node, dict):
                name = node.get("name")
                if name == BRAND and "alternateName" not in node:
                    node["alternateName"] = [FORMER_BRAND, FORMER_SHORT]
                    changed = True
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for item in node:
                    visit(item)

        visit(data)
        if not changed:
            return match.group(0)
        return (
            '<script type="application/ld+json">\n  '
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "\n  </script>"
        )

    pattern = re.compile(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
        re.DOTALL,
    )
    return pattern.sub(patch_block, content)


def enrich_home_keywords(content: str) -> str:
    """Ensure homepage keywords mention both castelletto and quercia."""
    if 'name="keywords"' not in content:
        return content
    return re.sub(
        r'(<meta name="keywords" content=")([^"]*)(">)',
        lambda m: (
            f'{m.group(1)}{SEO_KEYWORDS_EXTRA}, {m.group(2)}{m.group(3)}'
            if SEO_KEYWORDS_EXTRA.split(",")[0].strip() not in m.group(2)
            else m.group(0)
        ),
        content,
        count=1,
    )


def enrich_meta_description(content: str) -> str:
    """Add former name to meta/og descriptions when missing (SEO continuity)."""
    former_hint = f"(ex {FORMER_BRAND})"
    for attr in ('name="description"', 'property="og:description"'):
        pattern = rf'(<meta {attr} content=")([^"]*)((">)?)'
        match = re.search(pattern, content)
        if not match:
            continue
        body = match.group(2)
        if FORMER_BRAND.lower() in body.lower() or "ex " in body.lower():
            continue
        if body.startswith(BRAND):
            insert_at = len(BRAND)
            if body[insert_at : insert_at + 2] == " a":
                new_body = body[:insert_at] + f" {former_hint}" + body[insert_at:]
            else:
                new_body = f"{BRAND} {former_hint}: " + body[len(BRAND) + 2 :] if body.startswith(BRAND + ": ") else f"{body} — {former_hint}"
            content = content[: match.start(2)] + new_body + content[match.end(2) :]
    return content


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = rebrand(original)
    if path.suffix == ".html":
        updated = patch_json_ld(updated)
        if path.name == "index.html" and path.parent == ROOT:
            updated = enrich_home_keywords(updated)
        if "meta name=\"description\"" in updated or 'property="og:description"' in updated:
            updated = enrich_meta_description(updated)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        files.append(path)
    return sorted(files)


def main() -> None:
    changed = 0
    for path in iter_files():
        if process_file(path):
            print(f"OK {path.relative_to(ROOT)}")
            changed += 1
    print(f"Done. Updated {changed} file(s).")


if __name__ == "__main__":
    main()
