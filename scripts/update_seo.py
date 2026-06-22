#!/usr/bin/env python3
"""Update SEO meta tags, canonical URLs, OG tags, and schema.org for Casa Famiglia Quercia."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://casafamigliaquercia.it"
OG_IMAGE = f"{BASE}/images/map-placeholder.jpg"
PINEROLO_OG_IMAGE = f"{BASE}/images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/Sala%20da%20Pranzo%20%2B%20persone%201.avif"

LODGING_SCHEMA = {
    "@context": "https://schema.org",
    "@type": ["LodgingBusiness", "LocalBusiness"],
    "name": "Casa Famiglia Quercia",
    "description": "Casa famiglia per anziani autosufficienti a Pinerolo (TO). Assistenza 24h, ambienti familiari, Pinerolese.",
    "url": f"{BASE}/",
    "telephone": "+39 376 203 1211",
    "email": "info@casafamigliaquercia.it",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Stradale Poirino, 152",
        "addressLocality": "Pinerolo",
        "addressRegion": "TO",
        "postalCode": "10064",
        "addressCountry": "IT",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 44.8235, "longitude": 7.3307},
    "priceRange": "€€",
}

PAGE_SEO = {
    "index.html": {
        "title": "Casa Famiglia Quercia | Residenza per Anziani a Pinerolo (TO)",
        "description": "Casa Famiglia Quercia a Pinerolo: residenza per anziani autosufficienti a 40 minuti da Torino. Max 8 ospiti, assistenza 24h, ambiente familiare. Prenota una visita gratuita.",
        "keywords": "casa famiglia anziani Pinerolo, residenza anziani Pinerolo Torino, casa famiglia Pinerolese, anziani autosufficienti Pinerolo",
        "path": "/",
        "og_type": "website",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "servizi/index.html": {
        "title": "Servizi | Casa Famiglia Quercia – Pinerolo",
        "description": "Assistenza 24h, pasti freschi, camere private, giardino, attività ricreative: scopri tutti i servizi inclusi a Casa Famiglia Quercia a Pinerolo.",
        "path": "/servizi/",
        "og_type": "website",
    },
    "contatti/index.html": {
        "title": "Contatti | Casa Famiglia Quercia – Pinerolo (TO)",
        "description": "Contatta Casa Famiglia Quercia a Pinerolo. Telefono, WhatsApp, email. Prenota una visita gratuita senza impegno. Stradale Poirino 152, Pinerolo.",
        "path": "/contatti/",
        "og_type": "website",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "rette-e-ammissione/index.html": {
        "title": "Rette e Ammissione | Casa Famiglia Quercia – Pinerolo",
        "description": "Scopri cosa include la retta di Casa Famiglia Quercia a Pinerolo. Trasparenza completa su costi e servizi. Nessun extra nascosto. Contattaci per un preventivo.",
        "path": "/rette-e-ammissione/",
        "og_type": "website",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "la-giornata/index.html": {
        "title": "La Giornata Tipo | Casa Famiglia Quercia – Pinerolo",
        "description": "Com'è una giornata a Casa Famiglia Quercia? Scopri i ritmi, le attività e la vita quotidiana della nostra residenza per anziani a Pinerolo.",
        "path": "/la-giornata/",
        "og_type": "website",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "chi-siamo/index.html": {
        "title": "Chi siamo | Casa Famiglia Quercia – Pinerolo",
        "description": "Scopri Casa Famiglia Quercia a Pinerolo: una seconda casa per anziani autosufficienti nel Pinerolese. Ambiente familiare, non una RSA.",
        "path": "/chi-siamo/",
        "og_type": "website",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "storia/index.html": {
        "title": "La nostra storia | Casa Famiglia Quercia – Pinerolo",
        "description": "La storia di Casa Famiglia Quercia a Pinerolo: una casa familiare nel verde del Pinerolese, pensata per anziani autosufficienti.",
        "path": "/storia/",
        "og_type": "website",
    },
    "la-struttura/index.html": {
        "title": "La struttura | Casa Famiglia Quercia – Pinerolo",
        "description": "Camere luminose, salotti condivisi e giardino a Pinerolo. Scopri gli spazi di Casa Famiglia Quercia in Stradale Poirino 152.",
        "path": "/la-struttura/",
        "og_type": "website",
    },
    "galleria/index.html": {
        "title": "Galleria foto | Casa Famiglia Quercia – Pinerolo",
        "description": "Esplora in foto camere, salotti, cucina e giardino di Casa Famiglia Quercia a Pinerolo. Ambienti familiari per anziani autosufficienti.",
        "path": "/galleria/",
        "og_type": "website",
    },
    "requisiti-autosufficienza/index.html": {
        "title": "Requisiti autosufficienza | Casa Famiglia Quercia – Pinerolo",
        "description": "Chi può entrare a Casa Famiglia Quercia a Pinerolo? Requisiti per anziani autosufficienti over 65: autonomia, salute e processo di ammissione.",
        "path": "/requisiti-autosufficienza/",
        "og_type": "website",
    },
    "casa-famiglia-pinerolo/index.html": {
        "title": "Casa famiglia anziani Pinerolo | Casa Famiglia Quercia",
        "description": "Casa famiglia per anziani autosufficienti a Pinerolo. Max 8 ospiti, assistenza 24h, ambiente familiare vicino Torino. Prenota una visita gratuita.",
        "path": "/casa-famiglia-pinerolo/",
        "og_type": "website",
    },
    "casa-famiglia-coazze/index.html": {
        "title": "Casa famiglia anziani Pinerolese | Casa Famiglia Quercia",
        "description": "Casa famiglia per anziani autosufficienti nel Pinerolese. Casa Famiglia Quercia a Pinerolo: assistenza 24h, pasti di casa. Prenota una visita gratuita.",
        "path": "/casa-famiglia-coazze/",
        "og_type": "website",
    },
    "casa-famiglia-valle-di-susa/index.html": {
        "title": "Casa famiglia Pinerolese | Anziani autosufficienti",
        "description": "Casa famiglia per anziani autosufficienti nel Pinerolese. Pinerolo, natura, assistenza 24h e vita di comunità. Casa Famiglia Quercia.",
        "path": "/casa-famiglia-valle-di-susa/",
        "og_type": "website",
    },
    "casa-famiglia-giaveno/index.html": {
        "title": "Casa famiglia anziani vicino Giaveno | Casa Famiglia Quercia",
        "description": "Cerchi una casa famiglia per genitori autosufficienti vicino Giaveno? Casa Famiglia Quercia a Pinerolo è facilmente raggiungibile. Visita gratuita.",
        "path": "/casa-famiglia-giaveno/",
        "og_type": "website",
    },
    "casa-famiglia-avigliana/index.html": {
        "title": "Casa famiglia anziani vicino Avigliana | Casa Famiglia Quercia",
        "description": "Casa famiglia per anziani autosufficienti vicino Avigliana. Casa Famiglia Quercia a Pinerolo nel Pinerolese. Ambiente familiare, visita gratuita.",
        "path": "/casa-famiglia-avigliana/",
        "og_type": "website",
    },
    "blog/index.html": {
        "title": "Blog | Casa Famiglia Quercia – Pinerolo",
        "description": "Guide e articoli per famiglie: scegliere una casa famiglia, autonomia degli anziani e vita quotidiana serena a Pinerolo.",
        "path": "/blog/",
        "og_type": "website",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/casa-famiglia-vs-rsa-differenze/index.html": {
        "title": "Casa Famiglia o RSA? Le differenze vere (e come scegliere quella giusta)",
        "description": "RSA o casa famiglia per il tuo caro? Scopri le differenze reali: costi, assistenza, libertà, atmosfera. Una guida onesta per famiglie in cerca della scelta giusta.",
        "path": "/blog/casa-famiglia-vs-rsa-differenze/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/costi-retta-casa-famiglia-piemonte/index.html": {
        "title": "Cosa include la retta di una casa famiglia? Tutto quello che devi sapere",
        "description": "Cosa copre la retta mensile di una casa famiglia? Pasti, assistenza, terapie, pulizie: ecco cosa è incluso (e cosa non lo è). Guida chiara per famiglie.",
        "path": "/blog/costi-retta-casa-famiglia-piemonte/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/visite-familiari-casa-famiglia/index.html": {
        "title": "Visite familiari in casa famiglia: guida pratica",
        "description": "Orari, nipoti, equilibrio emotivo e distanza: come gestire visite familiari utili in casa famiglia a Pinerolo.",
        "path": "/blog/visite-familiari-casa-famiglia/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/valle-di-susa-vita-anziani/index.html": {
        "title": "Pinerolese e qualità della vita in terza età",
        "description": "Natura, comunità e casa troppo grande: perché nel Pinerolese una casa famiglia può migliorare la vita dell'ospite e dei figli.",
        "path": "/blog/valle-di-susa-vita-anziani/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/coazze-giaveno-pinerolo-servizi/index.html": {
        "title": "Pinerolo, Giaveno e Pinerolese: servizi e distanze",
        "description": "Distanze, collegamenti e servizi tra Pinerolo, Giaveno e il Pinerolese: guida pratica per scegliere una casa famiglia sostenibile.",
        "path": "/blog/coazze-giaveno-pinerolo-servizi/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/scegliere-casa-famiglia-genitori/index.html": {
        "title": "Come scegliere casa famiglia per i genitori",
        "description": "Checklist visita, errori dei figli e dialogo con il genitore: guida pratica per scegliere casa famiglia a Pinerolo senza fretta.",
        "path": "/blog/scegliere-casa-famiglia-genitori/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/autonomia-dignita-terza-eta/index.html": {
        "title": "Autonomia e dignità nella terza età: guida pratica",
        "description": "Autonomia non è solitudine: linguaggio, scelte quotidiane e assistenza discreta per preservare dignità in casa famiglia a Pinerolo.",
        "path": "/blog/autonomia-dignita-terza-eta/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/domande-figli-casa-famiglia/index.html": {
        "title": "Le domande dei figli prima della casa famiglia",
        "description": "FAQ emotive e pratiche dei figli: momento giusto, costi, visite e qualità della casa famiglia a Pinerolo.",
        "path": "/blog/domande-figli-casa-famiglia/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/inserimento-nuovo-ospite/index.html": {
        "title": "Inserimento nuovo ospite: guida ai primi 30 giorni",
        "description": "Ambientamento, oggetti personali e primo mese in casa famiglia: percorso pratico per inserire un nuovo ospite con serenità a Pinerolo.",
        "path": "/blog/inserimento-nuovo-ospite/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "blog/anziani-autosufficienti-coazze/index.html": {
        "title": "Anziani autosufficienti a Pinerolo: guida utile",
        "description": "Autosufficienza non significa assenza di bisogno: territorio, solitudine e figli lontani nella scelta di una casa famiglia a Pinerolo.",
        "path": "/blog/anziani-autosufficienti-coazze/",
        "og_type": "article",
        "og_image": PINEROLO_OG_IMAGE,
    },
    "privacy-policy/index.html": {
        "title": "Informativa privacy GDPR | Casa Famiglia Quercia – Pinerolo",
        "description": "Informativa privacy ai sensi del Reg. UE 2016/679. Titolare: Quercia & Gramsci S.r.l.s., P.IVA IT13206680012, Pinerolo (TO). Trattamento dati da telefono, WhatsApp ed email.",
        "path": "/privacy-policy/",
        "og_type": "website",
    },
    "cookie-policy/index.html": {
        "title": "Cookie Policy | Casa Famiglia Quercia – Pinerolo",
        "description": "Informativa sui cookie del sito Casa Famiglia Quercia a Pinerolo. Cookie tecnici e analitici, gestione del consenso.",
        "path": "/cookie-policy/",
        "og_type": "website",
    },
    "termini-e-condizioni/index.html": {
        "title": "Termini e condizioni d'uso | Casa Famiglia Quercia – Pinerolo",
        "description": "Termini di utilizzo del sito informativo Casa Famiglia Quercia. Quercia & Gramsci S.r.l.s., P.IVA IT13206680012, Pinerolo (TO). Legge italiana, foro di Torino.",
        "path": "/termini-e-condizioni/",
        "og_type": "website",
    },
    "404.html": {
        "title": "404 | Casa Famiglia Quercia",
        "description": "Pagina non trovata. Torna alla home di Casa Famiglia Quercia o contattaci.",
        "path": None,
        "og_type": None,
    },
}

REPLACEMENTS = [
    ("https://gramsci.lecasefamiglia.it", BASE),
    ("https://quercia.lecasefamiglia.it", BASE),
    ("gramsci.lecasefamiglia.it", "casafamigliaquercia.it"),
    ("quercia.lecasefamiglia.it", "casafamigliaquercia.it"),
    ("info@gramsci.lecasefamiglia.it", "info@casafamigliaquercia.it"),
    ("Casa Famiglia Gramsci", "Casa Famiglia Quercia"),
    ("Casa Gramsci", "Casa Famiglia Quercia"),
    ("Villa Gramsci", "Casa Famiglia Quercia"),
    ("Piazza Gramsci, 17", "Stradale Poirino, 152"),
    ("Piazza Gramsci 17", "Stradale Poirino 152"),
    ('"addressLocality":"Coazze"', '"addressLocality":"Pinerolo"'),
    ('"addressLocality": "Coazze"', '"addressLocality": "Pinerolo"'),
    ('"postalCode":"10050"', '"postalCode":"10064"'),
    ('"postalCode": "10050"', '"postalCode": "10064"'),
    ("10050 Coazze", "10064 Pinerolo"),
    ("Coazze (TO)", "Pinerolo (TO)"),
    ("a Coazze", "a Pinerolo"),
    ("a Coazze,", "a Pinerolo,"),
    ("in Coazze", "a Pinerolo"),
    ("di Coazze", "di Pinerolo"),
    ("| Gramsci", "| Casa Famiglia Quercia"),
    ("Gramsci Coazze", "Casa Famiglia Quercia – Pinerolo"),
    ("Gramsci Valle Susa", "Casa Famiglia Quercia – Pinerolo"),
    ("Valle di Susa", "Pinerolese"),
    ("Valle Susa", "Pinerolese"),
    ("45.05175", "44.8235"),
    ("7.29549", "7.3307"),
    (
        "images/Coazze%20-%20Casa%20Famiglia%20Gramsci/",
        "images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/",
    ),
]


def replace_tag(content: str, tag: str, value: str, attr: str = "content") -> str:
    pattern = rf'<{tag}[^>]*{attr}="[^"]*"[^>]*>'
    replacement = f'<{tag} name="{tag.split()[0]}" {attr}="{value}">' if tag.startswith("meta") else f'<{tag}>{value}</title>'
    if tag == "title":
        return re.sub(r"<title>[^<]*</title>", f"<title>{value}</title>", content, count=1)
    if tag == "meta description":
        return re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{value}">',
            content,
            count=1,
        )
    if tag == "meta keywords":
        if 'name="keywords"' in content:
            return re.sub(
                r'<meta name="keywords" content="[^"]*">',
                f'<meta name="keywords" content="{value}">',
                content,
                count=1,
            )
        desc = re.search(r'<meta name="description" content="[^"]*">', content)
        if desc:
            insert = f'\n  <meta name="keywords" content="{value}">'
            return content[: desc.end()] + insert + content[desc.end() :]
        return content
    if tag == "canonical":
        if 'rel="canonical"' in content:
            return re.sub(
                r'<link rel="canonical" href="[^"]*">',
                f'<link rel="canonical" href="{value}">',
                content,
                count=1,
            )
        robots = re.search(r'<meta name="robots"[^>]*>', content)
        insert = f'\n  <link rel="canonical" href="{value}">'
        if robots:
            return content[: robots.end()] + insert + content[robots.end() :]
        return content
    if tag.startswith("og:"):
        prop = tag
        if f'property="{prop}"' in content:
            return re.sub(
                rf'<meta property="{prop}" content="[^"]*">',
                f'<meta property="{prop}" content="{value}">',
                content,
                count=1,
            )
        og_block = re.search(r'<meta property="og:[^"]+" content="[^"]*">', content)
        insert = f'\n  <meta property="{prop}" content="{value}">'
        if og_block:
            return content[: og_block.end()] + insert + content[og_block.end() :]
        canonical = re.search(r'<link rel="canonical"[^>]*>', content)
        if canonical:
            return content[: canonical.end()] + insert + content[canonical.end() :]
        return content
    return content


def apply_global_replacements(content: str) -> str:
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    return content


def update_schema_urls(content: str, page_path) -> str:
    """Normalize LodgingBusiness blocks and breadcrumb/home URLs."""
    content = apply_global_replacements(content)

    if page_path:
        page_url = f"{BASE}{page_path}"
        content = replace_tag(content, "canonical", page_url)

    return content


def process_file(rel_path: str, seo: dict) -> None:
    path = ROOT / rel_path
    if not path.exists():
        print(f"SKIP missing: {rel_path}")
        return

    content = path.read_text(encoding="utf-8")
    content = apply_global_replacements(content)

    content = replace_tag(content, "title", seo["title"])
    content = replace_tag(content, "meta description", seo["description"])

    if seo.get("keywords"):
        content = replace_tag(content, "meta keywords", seo["keywords"])

    page_path = seo.get("path")
    if page_path:
        page_url = f"{BASE}{page_path}"
        content = replace_tag(content, "canonical", page_url)

        og_type = seo.get("og_type", "website")
        content = replace_tag(content, "og:type", og_type)
        content = replace_tag(content, "og:url", page_url)
        content = replace_tag(content, "og:title", seo["title"])
        content = replace_tag(content, "og:description", seo["description"])
        og_image = seo.get("og_image", OG_IMAGE)
        content = replace_tag(content, "og:image", og_image)

        if 'property="og:locale"' not in content and og_type:
            canonical = re.search(r'<meta property="og:image"[^>]*>', content)
            if canonical:
                insert = '\n  <meta property="og:locale" content="it_IT">'
                content = content[: canonical.end()] + insert + content[canonical.end() :]

        if 'rel="alternate" hreflang' in content:
            content = re.sub(
                r'<link rel="alternate" hreflang="it" href="[^"]*">',
                f'<link rel="alternate" hreflang="it" href="{page_url}">',
                content,
                count=1,
            )

    path.write_text(content, encoding="utf-8")
    print(f"OK {rel_path}")


def process_all_html_globally() -> None:
    for html_file in ROOT.rglob("*.html"):
        if "googled" in html_file.name:
            continue
        rel = str(html_file.relative_to(ROOT))
        if rel in PAGE_SEO:
            continue
        content = html_file.read_text(encoding="utf-8")
        updated = apply_global_replacements(content)
        if updated != content:
            html_file.write_text(updated, encoding="utf-8")
            print(f"GLOBAL {rel}")


def main() -> None:
    for rel_path, seo in PAGE_SEO.items():
        process_file(rel_path, seo)
    process_all_html_globally()
    print("Done.")


if __name__ == "__main__":
    main()
