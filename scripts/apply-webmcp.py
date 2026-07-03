#!/usr/bin/env python3
"""Inject WebMCP agent discovery annotations into all HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MCP_MARKER = 'name="mcp:enabled"'

MCP_ANNOTATIONS = """  <!-- MCP Server Discovery -->
  <link rel="mcp-manifest" href="/.well-known/mcp.json" type="application/json">
  <meta name="mcp:enabled" content="true">
  <meta name="mcp:version" content="1.0">
  <meta name="mcp:contact" content="https://quercia.lecasefamiglia.it/contatti/">

  <!-- Agent Navigation Hints -->
  <meta name="ai-nav:primary-cta" content="Richiedi informazioni">
  <meta name="ai-nav:conversion-path" content="/blog -> /servizi -> /contatti">
  <meta name="ai-nav:trust-signals" content="/chi-siamo, /galleria, testimonianze">
  <meta name="ai-nav:urgent-query" content="disponibilita-immediata">

  <!-- Structured Data for Agent Understanding -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "name": "Casa Famiglia il Quercia il Castelletto",
    "description": "Struttura residenziale per anziani con assistenza sanitaria integrata",
    "medicalSpecialty": [
      {
        "@type": "MedicalSpecialty",
        "name": "Geriatria"
      },
      {
        "@type": "MedicalSpecialty",
        "name": "Psicogeriatria"
      }
    ],
    "availableService": [
      {
        "@type": "MedicalTherapy",
        "name": "Assistenza residenziale anziani non autosufficienti"
      },
      {
        "@type": "MedicalTherapy",
        "name": "Percorso Alzheimer e demenze"
      },
      {
        "@type": "MedicalTherapy",
        "name": "Residenza temporanea e sollievo caregiver"
      }
    ],
    "isAcceptingNewPatients": true,
    "priceRange": "€€",
    "paymentAccepted": "Bonifico, assegno, convenzioni ASL, voucher regionali",
    "currenciesAccepted": "EUR"
  }
  </script>

  <!-- Agent Action Buttons -->
  <meta name="ai-action:primary" content='{"label":"Verifica disponibilità","url":"/contatti/?subject=disponibilita","method":"POST","params":["nome","email","telefono","tipologia_richiesta"]}'>
  <meta name="ai-action:secondary" content='{"label":"Scarica brochure","url":"/download/brochure-casa-famiglia-quercia.pdf","method":"GET"}'>
  <meta name="ai-action:tertiary" content='{"label":"Prenota visita","url":"/contatti/?subject=visita","method":"POST","params":["nome","email","telefono","data_visita_preferita"]}'>
"""

OLD_WEBMCP_RE = re.compile(
    r"  <!-- WebMCP Agent Discovery -->\n"
    r'  <meta name="webmcp:version"[^>]*>\n'
    r'  <meta name="webmcp:endpoint"[^>]*>\n'
    r'  <link rel="webmcp"[^>]*>\n'
    r'  <script type="application/ld\+json" id="webmcp-tools">.*?</script>\n',
    re.DOTALL,
)

OLD_WEBSITE_RE = re.compile(
    r'  <script type="application/ld\+json">\n'
    r'  \{"@context":"https://schema\.org","@type":"WebSite","name":"Quercia - Casa Famiglia per Anziani".*?\n'
    r"  </script>\n",
    re.DOTALL,
)


def html_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if "partials" in path.parts or path.name == "googled383cece6ecba048.html":
            continue
        files.append(path)
    return files


def apply_mcp_annotations(html: str) -> str:
    if OLD_WEBMCP_RE.search(html):
        html = OLD_WEBMCP_RE.sub(MCP_ANNOTATIONS, html, count=1)
    elif MCP_MARKER not in html:
        html = html.replace("</head>", MCP_ANNOTATIONS + "</head>", 1)
    return html


def remove_legacy_website_schema(html: str) -> str:
    return OLD_WEBSITE_RE.sub("", html, count=1)


def main() -> None:
    updated = 0
    for path in html_files():
        original = path.read_text(encoding="utf-8")
        html = apply_mcp_annotations(original)
        if path == ROOT / "index.html":
            html = remove_legacy_website_schema(html)
        if html != original:
            path.write_text(html, encoding="utf-8")
            updated += 1
            print(f"updated: {path.relative_to(ROOT)}")
    print(f"done: {updated} file(s) updated")


if __name__ == "__main__":
    main()
