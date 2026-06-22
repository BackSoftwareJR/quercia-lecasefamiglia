#!/usr/bin/env python3
"""Generate magazine-style blog HTML + markdown from blog_articles_data.py"""
import json
import os
import re
import html as html_lib
from urllib.parse import quote, unquote

from blog_articles_data import ARTICLES, ARTICLE_INDEX, OG_IMAGE, IMG_BASE

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE, "content", "blog")
BLOG_DIR = os.path.join(BASE, "blog")
SITE = "https://casafamigliaquercia.it"

PROMO_BOXES = {
    "galleria": {
        "href": "/galleria/",
        "title": "Vedi la galleria",
        "text": "Scoprite gli spazi di Casa Famiglia Quercia: camere luminose, salotti accoglienti e giardino nel verde di Coazze.",
        "icon": "gallery",
    },
    "servizi": {
        "href": "/servizi/",
        "title": "I nostri servizi",
        "text": "Assistenza discreta h24, pasti genuini, attività quotidiane e cura della casa: tutto incluso nella retta.",
        "icon": "services",
    },
    "visita": {
        "href": "/contatti/",
        "title": "Prenota una visita",
        "text": "Venite a Coazze senza impegno. Vi mostriamo la casa, rispondiamo alle domande e vi accompagniamo con calma.",
        "icon": "visit",
    },
    "rette": {
        "href": "/rette-e-ammissione/",
        "title": "Rette e ammissione",
        "text": "Tariffe trasparenti e percorso di ingresso chiaro per anziani autosufficienti in Valle di Susa.",
        "icon": "services",
    },
    "struttura": {
        "href": "/la-struttura/",
        "title": "La nostra struttura",
        "text": "Camere personalizzate, spazi comuni luminosi e giardino: una villa familiare, non un reparto.",
        "icon": "gallery",
    },
    "coazze": {
        "href": "/casa-famiglia-coazze/",
        "title": "Casa famiglia a Coazze",
        "text": "Scoprite perché Coazze è il cuore della Valle di Susa per anziani autosufficienti.",
        "icon": "visit",
    },
    "giornata": {
        "href": "/la-giornata/",
        "title": "La giornata tipo",
        "text": "Dalla colazione al riposo serale: scoprite com'è una giornata in casa famiglia a Coazze.",
        "icon": "services",
    },
}

PROMO_ICONS = {
    "gallery": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" width="24" height="24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>',
    "services": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" width="24" height="24" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "visit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" width="24" height="24" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
}


def json_str(s):
    return json.dumps(s, ensure_ascii=False)


def strip_html(text):
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def word_count_html(html):
    return len(re.findall(r"\w+", strip_html(html)))


def promo_html(promo_type):
    p = PROMO_BOXES[promo_type]
    icon = PROMO_ICONS[PROMO_BOXES[promo_type]["icon"]]
    return f"""<aside class="blog-promo-box blog-promo-box--{promo_type}">
          <div class="blog-promo-box__icon">{icon}</div>
          <div class="blog-promo-box__content">
            <p class="blog-promo-box__title"><a href="{p['href']}">{html_lib.escape(p['title'])}</a></p>
            <p class="blog-promo-box__text">{html_lib.escape(p['text'])}</p>
          </div>
        </aside>"""


def figure_html(file, alt, caption, loading="lazy"):
    return f"""<figure class="blog-article__figure">
          <img src="{IMG_BASE}{html_lib.escape(file)}" alt="{html_lib.escape(alt)}" width="800" height="500" loading="{loading}">
          <figcaption>{html_lib.escape(caption)}</figcaption>
        </figure>"""


def tags_html(tags):
    items = "".join(
        f'<span class="blog-tag blog-tag--{i % 3}">#{html_lib.escape(t)}</span>'
        for i, t in enumerate(tags)
    )
    return f'<div class="blog-article__tags" aria-label="Tag">{items}</div>'


def build_toc(sections):
    items = "".join(
        f'<li><a href="#{s["id"]}">{html_lib.escape(s["title"])}</a></li>'
        for s in sections
    )
    return f"""<nav class="blog-article__toc" aria-label="Indice dell'articolo">
            <h2>In questo articolo</h2>
            <ol>{items}</ol>
          </nav>"""


def sidebar_related(slugs):
    links = []
    for slug in slugs[:3]:
        meta = ARTICLE_INDEX[slug]
        links.append(
            f"""<li class="blog-sidebar-related__item">
              <a href="/blog/{slug}/" class="blog-sidebar-related__link">
                <span class="blog-sidebar-related__cat">{html_lib.escape(meta['category'])}</span>
                <span class="blog-sidebar-related__title">{html_lib.escape(meta['title'])}</span>
                <span class="blog-sidebar-related__date">22 giugno 2026</span>
              </a>
            </li>"""
        )
    return f"""<div class="blog-sidebar-box blog-sidebar-related">
            <h2 class="blog-sidebar-box__title">Articoli correlati</h2>
            <ul class="blog-sidebar-related__list">{"".join(links)}</ul>
          </div>"""


def sidebar_cta():
    return """<div class="blog-sidebar-box blog-sidebar-cta">
            <h2 class="blog-sidebar-box__title">Scopri Casa Famiglia Quercia</h2>
            <p class="blog-sidebar-cta__text">Una seconda casa per anziani autosufficienti a Coazze, in Valle di Susa.</p>
            <ul class="blog-sidebar-cta__links">
              <li><a href="/galleria/">Galleria fotografica</a></li>
              <li><a href="/servizi/">I nostri servizi</a></li>
              <li><a href="/contatti/">Contatti e visite</a></li>
            </ul>
          </div>"""


def sections_to_body(article):
    parts = []
    inline_images = {img.get("after_section", -1): img for img in article.get("inline_images", [])}
    promos = {p.get("after_section", -1): p.get("type", "visita") for p in article.get("promos", [])}

    if article.get("intro"):
        intro = article["intro"].strip()
        if intro.startswith("<p>"):
            parts.append(intro.replace("<p>", '<p class="blog-dropcap">', 1))
        else:
            parts.append(f'<p class="blog-dropcap">{intro}</p>')

    for i, sec in enumerate(article["sections"]):
        parts.append(f'<h2 id="{sec["id"]}">{html_lib.escape(sec["title"])}</h2>\n{sec["body"]}')
        if i in inline_images:
            img = inline_images[i]
            parts.append(figure_html(img["file"], img["alt"], img["caption"]))
        if i in promos:
            parts.append(promo_html(promos[i]))

    return "\n".join(parts)


def article_tag_metas(tags):
    return "\n".join(
        f'  <meta property="article:tag" content="{html_lib.escape(t)}">'
        for t in tags
    )


def build_html(article):
    slug = article["slug"]
    badge_class = "badge--primary" if article["badge"] == "primary" else "badge--accent"
    body = sections_to_body(article)
    toc = build_toc(article["sections"])
    hero = article.get("hero", "Sala da Pranzo + persone 1.avif")
    hero_alt = article.get("hero_alt", f"Casa famiglia anziani Coazze — {article['title']}")
    hero_caption = article.get("hero_caption", "Casa Famiglia Quercia, Stradale Poirino 152 — Coazze, Valle di Susa")
    wa_text = unquote(article.get("wa_text", "Ciao, ho letto il vostro articolo e vorrei informazioni sulla casa famiglia"))
    author = article.get("author", "Casa Famiglia Quercia")
    tags = article.get("tags", [])
    sidebar = sidebar_related(article.get("related", [])) + sidebar_cta()

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_lib.escape(article['meta_title'])}</title>
  <meta name="description" content="{html_lib.escape(article['meta_desc'])}">
  <meta name="robots" content="index, follow">
  <meta name="keywords" content="{html_lib.escape(article['keywords'])}">
  <link rel="canonical" href="{SITE}/blog/{slug}/">
  <link rel="alternate" hreflang="it" href="{SITE}/blog/{slug}/">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="it_IT">
  <meta property="og:title" content="{html_lib.escape(article['title'])}">
  <meta property="og:description" content="{html_lib.escape(article['meta_desc'][:155])}">
  <meta property="og:url" content="{SITE}/blog/{slug}/">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="article:published_time" content="2026-06-22T09:00:00+02:00">
  <meta property="article:modified_time" content="2026-06-22T09:00:00+02:00">
  <meta property="article:author" content="{html_lib.escape(author)}">
  <meta property="article:section" content="{html_lib.escape(article['category'])}">
{article_tag_metas(tags)}
  <meta name="theme-color" content="#2D5A3D">
  <link rel="icon" href="../../images/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/design-system.css">
  <link rel="stylesheet" href="../../css/global.css">
  <link rel="stylesheet" href="../../css/animations.css">
  <link rel="stylesheet" href="../../css/components.css">
  <link rel="stylesheet" href="../../css/pages.css">
  <link rel="stylesheet" href="../../blog.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {json_str(article['title'])},
    "description": {json_str(article['meta_desc'])},
    "image": {json_str(OG_IMAGE)},
    "datePublished": "2026-06-22T09:00:00+02:00",
    "dateModified": "2026-06-22T09:00:00+02:00",
    "author": {{"@type": "Organization", "name": {json_str(author)}, "url": "{SITE}/"}},
    "publisher": {{"@type": "Organization", "name": "Casa Famiglia Quercia", "url": "{SITE}/"}},
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "{SITE}/blog/{slug}/"}},
    "inLanguage": "it-IT",
    "keywords": {json_str(article['keywords'])},
    "articleSection": {json_str(article['category'])},
    "wordCount": {article.get('word_count', 1500)}
  }}
  </script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"{SITE}/blog/"}},{{"@type":"ListItem","position":3,"name":{json_str(article['breadcrumb'])},"item":"{SITE}/blog/{slug}/"}}]}}</script>
</head>
<body class="blog-page blog-article-page">
  <a href="#main" class="skip-link">Vai al contenuto principale</a>
  <div data-include="header"></div>
  <main id="main">
    <nav class="breadcrumbs container" aria-label="Breadcrumb">
      <ol class="breadcrumbs__list">
        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><a href="/blog/">Blog</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">{html_lib.escape(article['breadcrumb'])}</span></li>
      </ol>
    </nav>
    <article class="container blog-article">
      <header class="blog-article__header">
        <span class="badge {badge_class}">{html_lib.escape(article['category'])}</span>
        <h1>{html_lib.escape(article['title'])}</h1>
        <p class="blog-article__meta">
          <time datetime="2026-06-22">22 giugno 2026</time>
          · {html_lib.escape(article['reading'])} di lettura
          · <span class="blog-article__author">{html_lib.escape(author)}</span>
        </p>
        {tags_html(tags)}
      </header>
      <figure class="blog-article__hero">
        <img src="{IMG_BASE}{html_lib.escape(hero)}" alt="{html_lib.escape(hero_alt)}" width="1200" height="630" loading="eager" fetchpriority="high">
        <figcaption>{html_lib.escape(hero_caption)}</figcaption>
      </figure>
      <div class="blog-article-layout">
        <div class="blog-article-main">
          {toc}
          <div class="content-prose blog-article__body">
{body}
          </div>
        </div>
        <aside class="blog-article-sidebar" aria-label="Barra laterale">
          {sidebar}
        </aside>
      </div>
      <aside class="blog-article-cta">
        <h2>Hai dubbi? Parliamoci</h2>
        <p>Volete approfondire o prenotare una visita gratuita a Coazze? Siamo in Stradale Poirino 152, Valle di Susa — rispondiamo con calma, senza pressione.</p>
        <div class="btn-group blog-article-cta__buttons">
          <a href="tel:+393762031211" class="btn btn--accent btn--lg">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" width="20" height="20" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            Chiama — +39 376 203 1211
          </a>
          <a href="https://wa.me/393762031211?text={quote(wa_text)}" class="btn btn--whatsapp btn--lg" target="_blank" rel="noopener noreferrer">
            <img src="../../icons/whatsapp.svg" alt="" width="20" height="20" aria-hidden="true">
            WhatsApp
          </a>
          <a href="/contatti/" class="btn btn--secondary btn--lg">Prenota una visita</a>
        </div>
      </aside>
    </article>
  </main>
  <div data-include="footer"></div>
  <script src="../../js/includes.js" defer></script>
  <script src="../../js/nav.js" defer></script>
  <script src="../../js/main.js" defer></script>
  <script src="../../js/animations.js" defer></script>
  <script src="../../js/cookie-banner.js" defer></script>
</body>
</html>
"""


def build_md(article):
    lines = [
        "---",
        f'title: "{article["title"]}"',
        f'slug: {article["slug"]}',
        f'metaTitle: "{article["meta_title"]}"',
        f'metaDescription: "{article["meta_desc"]}"',
        "date: 2026-06-22",
        "dateModified: 2026-06-22",
        f'author: {article.get("author", "Casa Famiglia Quercia")}',
        f'category: {article["category"]}',
        f'readingTime: {article["reading"]}',
        f'keywords: {article["keywords"]}',
        f'tags: {", ".join(article.get("tags", []))}',
        "---",
        "",
        f"# {article['title']}",
        "",
    ]
    if article.get("intro"):
        lines.append(article["intro"])
        lines.append("")
    for sec in article["sections"]:
        lines.append(f"## {sec['title']}")
        lines.append("")
        for para in re.findall(r"<p>(.*?)</p>", sec["body"], re.S):
            lines.append(strip_html(para))
            lines.append("")
        for item in re.findall(r"<li>(.*?)</li>", sec["body"], re.S):
            lines.append(f"- {strip_html(item)}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_blog_index():
    featured_slug = "casa-famiglia-vs-rsa-differenze"
    featured = ARTICLE_INDEX[featured_slug]
    all_slugs = list(ARTICLE_INDEX.keys())

    categories = sorted({m["category"] for m in ARTICLE_INDEX.values()})

    filter_buttons = "".join(
        f'<button type="button" class="blog-filter__btn" data-filter="{html_lib.escape(c)}">{html_lib.escape(c)}</button>'
        for c in categories
    )
    filter_buttons = '<button type="button" class="blog-filter__btn blog-filter__btn--active" data-filter="all">Tutti</button>' + filter_buttons

    cards = []
    for slug in all_slugs:
        if slug == featured_slug:
            continue
        meta = ARTICLE_INDEX[slug]
        thumb = meta.get("thumb", meta.get("hero", "Sala da Pranzo + persone 1.avif"))
        tag_html = "".join(
            f'<span class="blog-tag blog-tag--{i % 3}">#{html_lib.escape(t)}</span>'
            for i, t in enumerate(meta.get("tags", [])[:4])
        )
        cards.append(f"""          <article class="card blog-card" data-category="{html_lib.escape(meta['category'])}">
            <a href="/blog/{slug}/" class="blog-card__image-link">
              <img src="../images/Coazze - Casa Famiglia Quercia/{html_lib.escape(thumb)}" alt="{html_lib.escape(meta.get('thumb_alt', meta['title']))}" width="400" height="250" loading="lazy" class="blog-card__image">
            </a>
            <div class="card__body">
              <span class="badge badge--{meta['badge']} card__category">{html_lib.escape(meta['category'])}</span>
              <p class="card__meta"><time datetime="2026-06-22">22 giugno 2026</time> · {html_lib.escape(meta['reading'])} di lettura</p>
              <h2 class="card__title"><a href="/blog/{slug}/">{html_lib.escape(meta['title'])}</a></h2>
              <p class="card__excerpt">{html_lib.escape(meta['excerpt'])}</p>
              <div class="blog-card__tags">{tag_html}</div>
              <a href="/blog/{slug}/" class="card__read-more">Leggi l'articolo →</a>
            </div>
          </article>""")

    intro = """Quando un genitore inizia a faticare da solo, i figli tra i 45 e i 65 anni si trovano spesso senza una mappa. Internet mescola RSA, case famiglia e residenze assistite; i prezzi sono difficili da confrontare; il senso di colpa rende ogni ricerca un peso. Questo blog è pensato per voi: famiglie del Piemonte occidentale che cercano una soluzione serena per un padre o una madre ancora autosufficienti. Qui trovate guide pratiche su differenze tra casa famiglia e RSA, costi delle rette in Piemonte, visite familiari, inserimento sereno e vita quotidiana in Valle di Susa. Ogni articolo nasce dall'esperienza quotidiana di Casa Famiglia Quercia a Coazze: una villa familiare, non un reparto, dove anziani autosufficienti trovano compagnia, sicurezza e autonomia. Che viviate a Giaveno, Pinerolo, Avigliana o Torino, queste pagine vi aiutano a fare domande giuste, confrontare con lucidità e — quando sarà il momento — prenotare una visita senza impegno."""

    featured_thumb = featured.get("hero", "Sala da Pranzo + persone 1.avif")
    featured_tags = "".join(
        f'<span class="blog-tag blog-tag--{i % 3}">#{html_lib.escape(t)}</span>'
        for i, t in enumerate(featured.get("tags", [])[:5])
    )

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog | Casa famiglia anziani Coazze</title>
  <meta name="description" content="Articoli utili per figli e caregiver: scegliere una casa famiglia, Valle di Susa, autonomia degli anziani e vita quotidiana serena a Coazze.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE}/blog/">
  <link rel="alternate" hreflang="it" href="{SITE}/blog/">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="it_IT">
  <meta property="og:title" content="Blog | Casa famiglia anziani Coazze">
  <meta property="og:description" content="Guide e consigli per famiglie che valutano una casa famiglia in Valle di Susa.">
  <meta property="og:url" content="{SITE}/blog/">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta name="theme-color" content="#2D5A3D">
  <link rel="icon" href="../images/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/design-system.css">
  <link rel="stylesheet" href="../css/global.css">
  <link rel="stylesheet" href="../css/animations.css">
  <link rel="stylesheet" href="../css/components.css">
  <link rel="stylesheet" href="../css/pages.css">
  <link rel="stylesheet" href="../blog.css">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Blog","name":"Blog Casa Famiglia Quercia","url":"{SITE}/blog/","description":"Guide per famiglie che scelgono una casa famiglia a Coazze","publisher":{{"@type":"Organization","name":"Casa Famiglia Quercia"}}}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"{SITE}/blog/"}}]}}</script>
</head>
<body class="blog-page">
  <a href="#main" class="skip-link">Vai al contenuto principale</a>
  <div data-include="header"></div>
  <main id="main">
    <nav class="breadcrumbs container" aria-label="Breadcrumb">
      <ol class="breadcrumbs__list">
        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">Blog</span></li>
      </ol>
    </nav>
    <header class="page-header">
      <div class="container">
        <h1>Blog — Consigli per le famiglie di anziani autosufficienti</h1>
        <p class="section__lead blog-index-intro">{html_lib.escape(intro)}</p>
      </div>
    </header>

    <section class="section blog-featured">
      <div class="container">
        <article class="blog-featured__card">
          <a href="/blog/{featured_slug}/" class="blog-featured__image-wrap">
            <img src="../images/Coazze - Casa Famiglia Quercia/{html_lib.escape(featured_thumb)}" alt="{html_lib.escape(featured.get('hero_alt', featured['title']))}" width="1200" height="600" loading="eager" class="blog-featured__image">
          </a>
          <div class="blog-featured__content">
            <span class="badge badge--{featured['badge']}">In evidenza</span>
            <span class="badge badge--{featured['badge']}">{html_lib.escape(featured['category'])}</span>
            <p class="blog-featured__meta"><time datetime="2026-06-22">22 giugno 2026</time> · {html_lib.escape(featured['reading'])} di lettura</p>
            <h2 class="blog-featured__title"><a href="/blog/{featured_slug}/">{html_lib.escape(featured['title'])}</a></h2>
            <p class="blog-featured__excerpt">{html_lib.escape(featured['excerpt'])}</p>
            <div class="blog-card__tags">{featured_tags}</div>
            <a href="/blog/{featured_slug}/" class="btn btn--primary">Leggi l'articolo in evidenza</a>
          </div>
        </article>
      </div>
    </section>

    <section class="section blog-layout">
      <div class="container">
        <nav class="blog-filter" aria-label="Filtra per categoria">
          {filter_buttons}
        </nav>
        <div class="blog-grid" id="blog-grid">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
    <section class="cta-band" aria-labelledby="blog-cta-heading">
      <div class="container">
        <h2 id="blog-cta-heading">Hai altre domande?</h2>
        <p>Parliamone — siamo a Coazze, in Valle di Susa. Visita gratuita, senza impegno.</p>
        <div class="btn-group blog-index-cta__buttons">
          <a href="tel:+393762031211" class="btn btn--accent btn--lg">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" width="20" height="20" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            Chiama — +39 376 203 1211
          </a>
          <a href="https://wa.me/393762031211?text={quote('Ciao, sto cercando informazioni sulla casa famiglia per il mio caro')}" class="btn btn--whatsapp btn--lg" target="_blank" rel="noopener noreferrer">
            <img src="../icons/whatsapp.svg" alt="" width="20" height="20" aria-hidden="true">
            WhatsApp
          </a>
          <a href="/contatti/" class="btn btn--secondary btn--lg">Prenota una visita</a>
          <a href="/servizi/" class="btn btn--ghost btn--lg">I nostri servizi</a>
        </div>
      </div>
    </section>
  </main>
  <div data-include="footer"></div>
  <script src="../js/includes.js" defer></script>
  <script src="../js/nav.js" defer></script>
  <script src="../js/main.js" defer></script>
  <script src="../js/animations.js" defer></script>
  <script src="../js/cookie-banner.js" defer></script>
  <script>
  (function () {{
    var buttons = document.querySelectorAll('.blog-filter__btn');
    var cards = document.querySelectorAll('.blog-card[data-category]');
    buttons.forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        var filter = btn.getAttribute('data-filter');
        buttons.forEach(function (b) {{ b.classList.remove('blog-filter__btn--active'); }});
        btn.classList.add('blog-filter__btn--active');
        cards.forEach(function (card) {{
          var show = filter === 'all' || card.getAttribute('data-category') === filter;
          card.style.display = show ? '' : 'none';
        }});
      }});
    }});
  }})();
  </script>
</body>
</html>"""

    with open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    counts = {}
    for article in ARTICLES:
        slug = article["slug"]
        html_path = os.path.join(BLOG_DIR, slug, "index.html")
        md_path = os.path.join(CONTENT_DIR, f"{slug}.md")
        os.makedirs(os.path.dirname(html_path), exist_ok=True)

        body = sections_to_body(article)
        wc = word_count_html(body)
        article["word_count"] = wc
        counts[slug] = wc

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(build_html(article))
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(build_md(article))

        status = "OK" if wc >= 1500 else ("SHORT" if wc < 1200 else "WARN")
        print(f"{status:5} {wc:4d}  {slug}")

    build_blog_index()
    print("Built blog/index.html")
    return counts


if __name__ == "__main__":
    main()
