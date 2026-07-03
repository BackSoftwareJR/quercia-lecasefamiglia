#!/usr/bin/env python3
"""Inject WebMCP agent discovery annotations into all HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WEBMCP_MARKER = 'name="webmcp:version"'

WEBMCP_HEAD = """  <!-- WebMCP Agent Discovery -->
  <meta name="webmcp:version" content="1.0">
  <meta name="webmcp:endpoint" content="https://quercia.lecasefamiglia.it/.well-known/webmcp">
  <link rel="webmcp" href="https://quercia.lecasefamiglia.it/.well-known/webmcp">
  <script type="application/ld+json" id="webmcp-tools">
{
  "@context": "https://schema.org",
  "@type": "WebAPI",
  "name": "Quercia WebMCP API",
  "description": "Machine-readable interface for AI agents to interact with Quercia elderly care services",
  "documentation": "https://quercia.lecasefamiglia.it/.well-known/webmcp",
  "endpointUrl": "https://quercia.lecasefamiglia.it/wp-json/wp/v2",
  "conformsTo": "https://webmcp.org/spec/1.0"
}
  </script>
"""

WEBSITE_SCHEMA = """  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"WebSite","name":"Quercia - Casa Famiglia per Anziani","url":"https://quercia.lecasefamiglia.it/","description":"Residenza assistita per anziani con cure specializzate per demenza e Alzheimer. Assistenza sanitaria h24 in ambiente familiare.","potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":"https://quercia.lecasefamiglia.it/?s={search_term_string}"},"query-input":"required name=search_term_string"},"publisher":{"@type":"Organization","name":"Le Case Famiglia","url":"https://www.lecasefamiglia.it/","logo":{"@type":"ImageObject","url":"https://quercia.lecasefamiglia.it/wp-content/uploads/logo.png"}}}
  </script>"""

OLD_WEBSITE_RE = re.compile(
    r'  <script type="application/ld\+json">\n'
    r'  \{"@context":"https://schema\.org","@type":"WebSite","name":"Casa Famiglia Castelletto".*?\n'
    r'  </script>\n',
    re.DOTALL,
)


def html_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if "partials" in path.parts or path.name == "googled383cece6ecba048.html":
            continue
        files.append(path)
    return files


def inject_webmcp(html: str) -> str:
    if WEBMCP_MARKER in html:
        return html
    return html.replace("</head>", WEBMCP_HEAD + "</head>", 1)


def update_homepage_schema(html: str) -> str:
    if '"@type":"WebSite","name":"Quercia - Casa Famiglia per Anziani"' in html:
        return html
    updated, count = OLD_WEBSITE_RE.subn(WEBSITE_SCHEMA + "\n", html, count=1)
    return updated if count else html


def main() -> None:
    updated = 0
    for path in html_files():
        original = path.read_text(encoding="utf-8")
        html = inject_webmcp(original)
        if path == ROOT / "index.html":
            html = update_homepage_schema(html)
        if html != original:
            path.write_text(html, encoding="utf-8")
            updated += 1
            print(f"updated: {path.relative_to(ROOT)}")
    print(f"done: {updated} file(s) updated")


if __name__ == "__main__":
    main()
