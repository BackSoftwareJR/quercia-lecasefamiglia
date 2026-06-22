#!/usr/bin/env python3
"""Regenerate all 10 Quercia blog articles: images, SEO, content, schema, CTA."""
import json
import os
import re
import html as html_lib
from urllib.parse import quote

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE, "blog")
CONTENT_DIR = os.path.join(BASE, "content", "blog")
SITE = "https://casafamigliaquercia.it"
AUTHOR = "Casa Famiglia Quercia"
DATE_PUBLISHED = "2026-06-22T09:00:00+02:00"
OG_IMAGE = f"{SITE}/images/Sala%20da%20Pranzo%20%2B%20persone%201.avif"
PIN = "Pinerolo - Casa Famiglia Quercia 1"
DINING = "Sala da Pranzo + persone 1.avif"

HERO = {
    "casa-famiglia-vs-rsa-differenze": DINING,
    "scegliere-casa-famiglia-genitori": f"{PIN}/img2.avif",
    "anziani-autosufficienti-coazze": f"{PIN}/img1.avif",
    "valle-di-susa-vita-anziani": f"{PIN}/img4.avif",
    "visite-familiari-casa-famiglia": f"{PIN}/img7.avif",
    "costi-retta-casa-famiglia-piemonte": f"{PIN}/img8.avif",
    "inserimento-nuovo-ospite": f"{PIN}/img6.avif",
    "autonomia-dignita-terza-eta": f"{PIN}/img9.avif",
    "coazze-giaveno-pinerolo-servizi": f"{PIN}/img10.avif",
    "domande-figli-casa-famiglia": f"{PIN}/img11.avif",
}

THUMB_ALT = {
    "casa-famiglia-vs-rsa-differenze": "Ospiti e familiari a tavola in Casa Famiglia Quercia, Pinerolo",
    "scegliere-casa-famiglia-genitori": "Momento conviviale in sala da pranzo a Pinerolo",
    "anziani-autosufficienti-coazze": "Salone luminoso di Casa Famiglia Quercia nel Pinerolese",
    "valle-di-susa-vita-anziani": "Spazi comuni accoglienti per anziani autosufficienti",
    "visite-familiari-casa-famiglia": "Camera confortevole pronta per le visite in famiglia",
    "costi-retta-casa-famiglia-piemonte": "Camera luminosa con arredi personali in stile domestico",
    "inserimento-nuovo-ospite": "Cucina di casa dove iniziano le nuove abitudini",
    "autonomia-dignita-terza-eta": "Giardino e verde del Pinerolese intorno alla casa",
    "coazze-giaveno-pinerolo-servizi": "Casa Famiglia Quercia facilmente raggiungibile da Torino",
    "domande-figli-casa-famiglia": "Ingresso accogliente di Casa Famiglia Quercia a Pinerolo",
}


def p(*parts: str) -> str:
    return "".join(f"<p>{t}</p>" for t in parts)


def h3(title: str, *paras: str) -> str:
    return f"<h3>{html_lib.escape(title)}</h3>" + p(*paras)


def section(sid: str, title: str, body: str) -> dict:
    return {"id": sid, "title": title, "body": body}


def json_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def strip_html(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()


def word_count_html(html: str) -> int:
    return len(re.findall(r"\w+", strip_html(html)))


def hero_src(rel_path: str, depth: int = 2) -> str:
    prefix = "../" * depth
    return f"{prefix}images/{rel_path}"


def sections_to_body(article: dict) -> str:
    parts = []
    intro = article.get("intro", "").strip()
    if intro:
        if intro.startswith("<p>"):
            parts.append(intro.replace("<p>", '<p class="blog-dropcap">', 1))
        else:
            parts.append(f'<p class="blog-dropcap">{intro}</p>')
    for sec in article["sections"]:
        parts.append(f'<h2 id="{sec["id"]}">{html_lib.escape(sec["title"])}</h2>\n{sec["body"]}')
    return "\n".join(parts)


def build_toc(sections: list) -> str:
    items = "".join(
        f'<li><a href="#{s["id"]}">{html_lib.escape(s["title"])}</a></li>' for s in sections
    )
    return f"""<nav class="blog-article__toc" aria-label="Indice dell'articolo">
            <h2>In questo articolo</h2>
            <ol>{items}</ol>
          </nav>"""


def tags_html(tags: list) -> str:
    items = "".join(
        f'<span class="blog-tag blog-tag--{i % 3}">#{html_lib.escape(t)}</span>'
        for i, t in enumerate(tags)
    )
    return f'<div class="blog-article__tags" aria-label="Tag">{items}</div>' if tags else ""


def sidebar_related(slugs: list) -> str:
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


def sidebar_cta() -> str:
    return """<div class="blog-sidebar-box blog-sidebar-cta">
            <h2 class="blog-sidebar-box__title">Scopri Casa Quercia</h2>
            <p class="blog-sidebar-cta__text">Una seconda casa per anziani autosufficienti a Pinerolo, nel Pinerolese.</p>
            <ul class="blog-sidebar-cta__links">
              <li><a href="/galleria/">Galleria fotografica</a></li>
              <li><a href="/servizi/">I nostri servizi</a></li>
              <li><a href="/contatti/">Contatti e visite</a></li>
            </ul>
          </div>"""


def article_cta(wa_text: str) -> str:
    return f"""<aside class="blog-article-cta">
        <h2>Prenota visita a Casa Famiglia Quercia</h2>
        <p>Vieni a conoscere la nostra casa a Pinerolo, in Stradale Poirino 152. Visita gratuita e senza impegno: ti mostriamo gli spazi, rispondiamo alle domande e ti aiutiamo a capire se siamo la scelta giusta per la tua famiglia.</p>
        <div class="btn-group blog-article-cta__buttons">
          <a href="tel:+393762031211" class="btn btn--accent btn--lg">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" width="20" height="20" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            Chiama — +39 376 203 1211
          </a>
          <a href="https://wa.me/393762031211?text={quote(wa_text)}" class="btn btn--whatsapp btn--lg" target="_blank" rel="noopener noreferrer">
            <img src="../../icons/whatsapp.svg" alt="" width="20" height="20" aria-hidden="true">
            WhatsApp
          </a>
          <a href="/contatti/" class="btn btn--secondary btn--lg">Prenota visita a Casa Famiglia Quercia</a>
        </div>
      </aside>"""


def build_html(article: dict) -> str:
    slug = article["slug"]
    badge_class = "badge--primary" if article["badge"] == "primary" else "badge--accent"
    body = sections_to_body(article)
    wc = word_count_html(body)
    hero_path = HERO[slug]
    hero_img = hero_src(hero_path)
    og = OG_IMAGE if slug == "casa-famiglia-vs-rsa-differenze" else f"{SITE}/images/{quote(hero_path, safe='/')}"
    meta_title = article["meta_title"]
    tags = article.get("tags", [])

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_lib.escape(meta_title)}</title>
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
  <meta property="og:image" content="{og}">
  <meta property="article:published_time" content="{DATE_PUBLISHED}">
  <meta property="article:modified_time" content="{DATE_PUBLISHED}">
  <meta property="article:author" content="{AUTHOR}">
  <meta property="article:section" content="{html_lib.escape(article['category'])}">
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
    "image": {json_str(og)},
    "datePublished": "{DATE_PUBLISHED}",
    "dateModified": "{DATE_PUBLISHED}",
    "author": {{"@type": "Organization", "name": {json_str(AUTHOR)}, "url": "{SITE}/"}},
    "publisher": {{"@type": "Organization", "name": {json_str(AUTHOR)}, "url": "{SITE}/"}},
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "{SITE}/blog/{slug}/"}},
    "inLanguage": "it-IT",
    "keywords": {json_str(article['keywords'])},
    "articleSection": {json_str(article['category'])},
    "wordCount": {wc}
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
          · <span class="blog-article__author">{AUTHOR}</span>
        </p>
        {tags_html(tags)}
      </header>
      <figure class="blog-article__hero">
        <img src="{html_lib.escape(hero_img)}" alt="{html_lib.escape(article['hero_alt'])}" width="1200" height="630" loading="eager" fetchpriority="high">
        <figcaption>Casa Famiglia Quercia, Stradale Poirino 152 — Pinerolo, Pinerolese</figcaption>
      </figure>
      <div class="blog-article-layout">
        <div class="blog-article-main">
          {build_toc(article['sections'])}
          <div class="content-prose blog-article__body">
{body}
          </div>
        </div>
        <aside class="blog-article-sidebar" aria-label="Barra laterale">
          {sidebar_related(article.get('related', []))}{sidebar_cta()}
        </aside>
      </div>
      {article_cta(article.get('wa_text', 'Buongiorno, vorrei prenotare una visita a Casa Famiglia Quercia a Pinerolo.'))}
    </article>
  </main>
  <div data-include="footer"></div>
  <script src="../../js/includes.js" defer></script>
  <script src="../../js/nav.js" defer></script>
  <script src="../../js/main.js" defer></script>
  <script src="../../js/animations.js" defer></script>
  <script src="../../js/cookie-banner.js" defer></script>
</body>
</html>"""


# --- Priority pillar: RSA vs Casa Famiglia (direttive SEZIONE 6 outline) ---

RSA_ARTICLE = {
    "slug": "casa-famiglia-vs-rsa-differenze",
    "title": "Casa Famiglia o RSA? Le differenze che nessuno ti dice",
    "meta_title": "Casa Famiglia o RSA? Le differenze vere (e come scegliere quella giusta)",
    "meta_desc": "RSA o casa famiglia per il tuo caro? Scopri le differenze reali: costi, assistenza, libertà, atmosfera. Una guida onesta per famiglie in cerca della scelta giusta.",
    "category": "Guida",
    "badge": "primary",
    "reading": "12 min",
    "keywords": "casa famiglia Pinerolo, differenze casa famiglia RSA, scelta figli anziani",
    "breadcrumb": "Casa Famiglia o RSA? Le differenze che nessuno ti dice",
    "hero_alt": "Ospiti e familiari seduti a tavola in un ambiente caldo e domestico a Pinerolo",
    "tags": ["casa famiglia Pinerolo", "differenze RSA", "scelta figli"],
    "related": ["scegliere-casa-famiglia-genitori", "costi-retta-casa-famiglia-piemonte", "domande-figli-casa-famiglia"],
    "wa_text": "Buongiorno, vorrei capire meglio le differenze tra casa famiglia e RSA per mio padre.",
    "intro": p(
        "Quando cerchi una soluzione per un genitore anziano, prima o poi ti trovi davanti a questa domanda: RSA o casa famiglia? Sul web trovi definizioni tecniche, tabelle comparative, sigle. Ma quello che ti serve davvero è capire cosa significa nella vita di tutti i giorni, per tuo padre, per tua madre, per te che vai a trovarlo.",
        'Questa guida non è scritta da un avvocato o da un funzionario sanitario. È scritta da chi gestisce Casa Famiglia Quercia a Pinerolo da anni e ha visto centinaia di famiglie fare questa scelta. Ti diciamo quello che abbiamo imparato, comprese le cose che non tornano a favore nostro. Per orientarti puoi iniziare dai nostri <a href="/servizi/">servizi</a> e dalla pagina <a href="/rette-e-ammissione/">rette e ammissione</a>.',
    ),
    "sections": [
        section(
            "cosa-e-rsa",
            "Cosa si intende per RSA",
            p(
                "RSA significa Residenza Sanitaria Assistenziale: struttura autorizzata dalla Regione, spesso di medie o grandi dimensioni, pensata per persone con bisogni sanitari e assistenziali significativi. L'organizzazione segue protocolli clinici, turni numerosi, reparti distinti e procedure standardizzate necessarie quando si gestiscono decine o centinaia di ospiti.",
                "In RSA l'assistenza sanitaria è integrata: infermieri, fisioterapisti, medici e operatori sociosanitari lavorano secondo piani assistenziali individuali (PAI). È la scelta corretta quando il quadro clinico richiede cure continue, monitoraggio stretto o interventi che una casa famiglia non può garantire.",
                "Per i figli, la RSA può trasmettere un'immagine istituzionale: corridoio lungo, orari di reparto, personale che cambia a ogni turno. Non è necessariamente negativo — è il modello giusto per certi bisogni. Il problema nasce quando viene scelta per un anziano ancora autosufficiente che cerca soprattutto compagnia e sicurezza, non cure intensive.",
            ),
        ),
        section(
            "cosa-e-casa-famiglia",
            "Cosa si intende per casa famiglia (e cosa non è)",
            p(
                "La casa famiglia è una struttura privata autorizzata che accoglie un numero limitato di ospiti — da pochi a una dozzina — in un ambiente domestico vero: salone, cucina, giardino, camere personalizzabili. Non è un reparto ospedaliero mascherato da hotel.",
                "Casa Famiglia Quercia a Pinerolo accoglie al massimo 8 anziani autosufficienti. Chi vive qui cammina da solo, mangia, si veste, gestisce l'igiene. Non serve assistenza sanitaria continua, ma può servire compagnia, pasti preparati, qualcuno presente h24 e un contesto dove la solitudine non è la norma.",
                "Attenzione: casa famiglia non significa badante condivisa a basso costo, né hotel per anziani. Significa una casa vera con regole umane, operatori stabili e familiari sempre benvenuti. Se cerchi «casa famiglia anziani Pinerolo», stai cercando questo equilibrio — non una scorciatoia economica rispetto a una RSA.",
            )
            + h3(
                "Cosa non aspettarti da una casa famiglia",
                "Non troverai reparti geriatrici, barelle nei corridoi o orari di visita contingentati. Se il tuo caro ha bisogni clinici complessi, la casa famiglia non è lo strumento giusto — e una struttura seria te lo dirà con chiarezza, senza accettare un ingresso inadatto.",
            ),
        ),
        section(
            "differenze-pratiche",
            "Le differenze pratiche: tavola comparativa",
            p(
                "Le differenze si sentono ogni giorno, non solo sulla carta. Ecco un confronto onesto tra una RSA tradizionale e Casa Famiglia Quercia:",
            )
            + """<div class="table-responsive"><table class="comparison-table">
<thead><tr><th scope="col">RSA tradizionale</th><th scope="col">Casa Famiglia Quercia</th></tr></thead>
<tbody>
<tr><td>Decine o centinaia di ospiti</td><td>Massimo 8 persone: ci si conosce tutti</td></tr>
<tr><td>Orari rigidi, regole di reparto</td><td>Flessibilità, ritmi personali rispettati</td></tr>
<tr><td>Atmosfera ospedaliera</td><td>Casa vera, arredata con cura a Pinerolo</td></tr>
<tr><td>Personale che ruota ogni turno</td><td>Stesse persone ogni giorno</td></tr>
<tr><td>Visite spesso contingentate</td><td>Familiari sempre benvenuti, senza orari rigidi</td></tr>
<tr><td>Spesso per chi non è autosufficiente</td><td>Solo per chi è ancora pienamente autonomo</td></tr>
</tbody></table></div>"""
            + p(
                "Non è una questione di «meglio» o «peggio» in assoluto. È una questione di bisogno reale. Se tuo padre è ancora in gamba ma non vuole più vivere solo, la colonna destra descrive il contesto che probabilmente cercate. Se ha bisogni sanitari complessi, la colonna sinistra è quella giusta.",
                "Per approfondire l'autonomia quotidiana leggi anche la nostra guida su <a href='/blog/autonomia-dignita-terza-eta/'>autonomia e dignità</a>.",
            ),
        ),
        section(
            "quanto-costano",
            "Quanto costano, davvero?",
            p(
                "Il costo è spesso il primo filtro — e anche il più fuorviante. Confrontare solo la cifra mensile senza chiedere cosa include è il modo più rapido per fare una scelta sbagliata.",
                "In RSA la retta copre assistenza sanitaria, vitto, alloggio e interventi previsti dal PAI. Può essere parzialmente rimborsata tramite contributi regionali o ASL, a seconda del caso. In casa famiglia la retta include generalmente vitto, alloggio, assistenza di base e gestione quotidiana — senza la componente sanitaria intensiva.",
                "Una retta casa famiglia apparentemente più alta può essere più conveniente se include tutto: pasti, pulizie, attività, assistenza notturna, gestione farmaci di routine. Chiedi sempre cosa è extra. Leggi la nostra guida su <a href='/blog/costi-retta-casa-famiglia-piemonte/'>cosa include la retta</a> e consulta <a href='/rette-e-ammissione/'>rette e ammissione</a> per i dettagli su Casa Quercia.",
            )
            + h3(
                "Costi indiretti che nessuno mette nel preventivo",
                "L'assistenza a domicilio somma badante, spese, assenze dal lavoro e stress continuo. Una RSA lontana riduce le visite e aumenta il senso di colpa. Una casa famiglia raggiungibile da Torino in 40 minuti — come Pinerolo — permette presenza reale senza stravolgere la settimana.",
            ),
        ),
        section(
            "per-chi-rsa",
            "Per chi è giusta la RSA",
            p(
                "La RSA è la scelta giusta quando il genitore ha bisogni sanitari che richiedono supervisione infermieristica, gestione di terapie complesse, monitoraggio continuo di patologie gravi o declino cognitivo avanzato che compromette la sicurezza.",
                "Se il medico di famiglia o un geriatra indicano che serve un percorso sociosanitario strutturato, ascoltate quell'indicazione. Forzare un anziano con bisogni clinici elevati in una casa famiglia per anziani autosufficienti non è rispettoso — né per lui né per gli altri ospiti.",
                "In questi casi la famiglia può comunque restare protagonista: visite regolari, coinvolgimento nelle decisioni, attenzione alla qualità della relazione con l'équipe. La RSA non significa abbandono — significa strumento adeguato al bisogno.",
            ),
        ),
        section(
            "per-chi-casa-famiglia",
            "Per chi è giusta una casa famiglia",
            p(
                "La casa famiglia è la scelta giusta quando il genitore è ancora autosufficiente — cammina, mangia, si veste, gestisce le necessità — ma la vita da solo pesa: la casa è troppo grande, le scale fanno paura, la cena solitaria è diventata triste, i figli abitano lontano e dormono male.",
                "È anche la scelta giusta quando una RSA sembra eccessiva ma lasciare tutto com'è non è più giusto. Casa Famiglia Quercia a Pinerolo nasce per questa «terza via»: non una struttura, non l'abbandono, una casa vera con persone vere, a 40 minuti da Torino nel verde del Pinerolese.",
                "Molte famiglie del Pinerolese e dell'area torinese ci scelgono perché vogliono che mamma o papà mantengano autonomia, dignità e ritmi personali — con qualcuno sotto lo stesso tetto che veglia anche di notte.",
            ),
        ),
        section(
            "domande-visita",
            "Le domande da fare durante la visita",
            p(
                "Prima di firmare qualsiasi contratto, visitate di persona. Portate un quaderno e fate domande concrete:",
            )
            + """<ul>
<li>Quanti ospiti accogliete? Qual è il rapporto operatori/ospiti?</li>
<li>Cosa include esattamente la retta? Ci sono extra previsti?</li>
<li>Come funzionano le visite? Ci sono orari rigidi?</li>
<li>Come gestite le emergenze notturne?</li>
<li>Quali requisiti di autonomia chiedete all'ingresso?</li>
<li>Come comunicate con i familiari? Chi è il referente?</li>
<li>Esiste un periodo di ambientamento graduale?</li>
</ul>"""
            + p(
                "Annotate le risposte e confrontatele tra strutture diverse. Una visita ben fatta vale più di dieci pagine web. Per una checklist completa leggi <a href='/blog/scegliere-casa-famiglia-genitori/'>come scegliere una casa famiglia</a> e le <a href='/blog/domande-figli-casa-famiglia/'>domande frequenti dei figli</a>.",
                "Potete prenotare una visita gratuita a Casa Quercia dalla pagina <a href='/contatti/'>contatti</a>.",
            ),
        ),
        section(
            "struttura-familiare",
            'Come capire se una struttura è davvero "familiare"',
            p(
                "Il termine «casa famiglia» viene usato da molte realtà — non tutte uguali. Ecco i segnali che indicano un ambiente davvero domestico:",
            )
            + """<ul>
<li>Gli operatori chiamano gli ospiti per nome, non per numero di camera</li>
<li>Le camere accogliono oggetti personali: foto, libri, coperte di casa</li>
<li>I pasti sono preparati in cucina, non arrivano in vaschette sigillate</li>
<li>C'è conversazione a tavola, non silenzio istituzionale</li>
<li>I familiari entrano senza suonare il campanello di un reparto</li>
<li>La struttura è piccola: riconosci i volti dopo la prima visita</li>
</ul>"""
            + p(
                "Durante la visita a Casa Famiglia Quercia osservate suoni, odori, luce naturale e come gli ospiti reagiscono agli operatori. Sono segnali più affidabili di qualsiasi brochure. Se qualcosa non vi convince, continuate a cercare — la scelta giusta esiste, ma va sentita con i piedi per terra.",
                "Per vedere gli spazi prima della visita, esplora la <a href='/galleria/'>galleria fotografica</a> e scopri i <a href='/servizi/'>servizi inclusi</a>.",
            ),
        ),
    ],
}

# --- Priority: Costi retta ---

COSTI_ARTICLE = {
    "slug": "costi-retta-casa-famiglia-piemonte",
    "title": "Cosa include la retta di una casa famiglia? Tutto quello che devi sapere",
    "meta_title": "Cosa include la retta di una casa famiglia? Tutto quello che devi sapere",
    "meta_desc": "Cosa copre la retta mensile di una casa famiglia? Pasti, assistenza, terapie, pulizie: ecco cosa è incluso (e cosa non lo è). Guida chiara per famiglie.",
    "category": "Costi",
    "badge": "primary",
    "reading": "12 min",
    "keywords": "casa famiglia Pinerolo, retta casa famiglia, costi assistenza anziani Piemonte",
    "breadcrumb": "Cosa include la retta di una casa famiglia?",
    "hero_alt": "Camera luminosa con arredi personali in stile domestico a Casa Quercia",
    "tags": ["retta casa famiglia", "costi Pinerolo", "trasparenza"],
    "related": ["casa-famiglia-vs-rsa-differenze", "domande-figli-casa-famiglia", "coazze-giaveno-pinerolo-servizi"],
    "wa_text": "Buongiorno, vorrei capire cosa include la retta e come valutare eventuali contributi.",
    "intro": p(
        'La prima domanda di quasi tutte le famiglie è: "Quanto costa?" Ed è la domanda giusta. Ma la seconda, quella che fa davvero la differenza, è: "E cosa include?"',
        "Perché una retta apparentemente bassa può nascondere decine di voci extra. E una retta all-inclusive può essere il miglior investimento che fai per tuo padre o tua madre. In Piemonte e nel Pinerolese le offerte variano molto: conviene partire da <a href='/rette-e-ammissione/'>rette e ammissione</a>, <a href='/servizi/'>servizi</a> e <a href='/contatti/'>contatti</a>.",
    ),
    "sections": [
        section(
            "cosa-incluso",
            "Cosa include di solito la retta mensile",
            p(
                "La retta di una casa famiglia copre tipicamente: alloggio in camera singola o doppia, vitto completo (colazione, pranzo, cena, spuntini), assistenza di base h24, gestione della casa (pulizie spazi comuni, biancheria, manutenzione ordinaria), attività ricreative e socializzazione, monitoraggio del benessere quotidiano e comunicazione con i familiari.",
                "A Casa Famiglia Quercia a Pinerolo la retta è pensata come formula all-inclusive: pasti preparati in casa con menu variati, assistenza discreta sempre presente, giardino e spazi comuni, attività quotidiane e referente familiare dedicato. Niente sorprese a fine mese per servizi «base» dimenticati nel preventivo.",
                "Quando valutate un preventivo, chiedete di vedere un esempio di menù settimanale, l'elenco delle attività proposte e come viene gestita la sicurezza notturna. Sono dettagli che fanno la differenza tra una retta giustificata e una cifra che non regge al confronto con la vita reale dell'ospite.",
            )
            + h3(
                "Voci che dovresti sempre chiedere per iscritto",
                "Chiedete elenco scritto di inclusioni ed esclusioni: farmaci (di routine), pannoloni, trasporti per visite mediche, parrucchiere, telefono, lavanderia personale oltre la biancheria base. Una struttura trasparente risponde senza esitazione.",
                "Conservate le email e i documenti ricevuti: in caso di cambiamenti futuri, avere traccia scritta protegge la famiglia e facilita il dialogo con fratelli e sorelle che non hanno partecipato alla visita iniziale.",
            ),
        ),
        section(
            "cosa-non-incluso",
            "Cosa di solito NON è incluso (e va chiesto)",
            p(
                "Anche nelle case famiglia più complete, alcune voci restano extra: visite specialistiche e ticket sanitari, farmaci non di routine, materiali sanitari specifici, servizi estetici (parrucchiere, podologo), trasporti eccezionali, assenze prolungate per ricoveri ospedalieri (politiche diverse per struttura).",
                "Non è un difetto — è normalità. Ma deve essere comunicato prima dell'ingresso, non scoperto sulla prima fattura. Chiedete: «Quali extra avete visto negli ultimi 12 mesi per ospiti simili al nostro caso?»",
            ),
        ),
        section(
            "confronto-reale",
            "Confronto reale: casa famiglia, badante, RSA",
            p(
                "Confrontare solo il numero mensile distorce la scelta. L'assistenza domiciliare con badante h24 a Pinerolo o Torino può costare quanto o più di una casa famiglia, sommando stipendio, contributi, sostituti, vitto e gestione notturna — con il figlio che resta coordinatore di tutto.",
                "La RSA ha costi diversi perché include componente sanitaria; può essere parzialmente coperta da ASL. Ma se il bisogno è relazionale, pagare per servizi clinici non necessari non è risparmio — è scelta incoerente.",
                "Molte famiglie torinesi ci raccontano di aver sottovalutato i costi «nascosti» della soluzione domiciliare: riparazioni in casa vuota, spese fisse su un immobile grande, ore di ferie per emergenze. Una retta unica in casa famiglia elimina gran parte di questo caos amministrativo.",
                "Costruite una tabella a tre colonne: costo diretto mensile, qualità vita attesa, carico organizzativo sui figli. Leggete anche <a href='/blog/casa-famiglia-vs-rsa-differenze/'>casa famiglia vs RSA</a> per il quadro completo.",
            ),
        ),
        section(
            "contributi-piemonte",
            "Contributi e agevolazioni in Piemonte",
            p(
                "In Piemonte esistono strumenti di sostegno economico legati alla non autosufficienza — più rilevanti per RSA e assistenza domiciliare intensiva che per case famiglia per autosufficienti. Comunque vale la pena informarsi: ASL, Comune, CAF e patronato possono indicare percorsi per indennità di accompagnamento, assegno di mantenimento o detrazioni fiscali.",
                "Casa Famiglia Quercia orienta le famiglie verso le fonti corrette senza promettere contributi che non spettano. La chiarezza fin dall'inizio evita delusioni e permette di pianificare con serenità.",
                "Anche le detrazioni fiscali per spese sanitarie e assistenziali meritano attenzione: conservate fatture e ricevute e chiedete al vostro commercialista quali voci sono deducibili nel vostro caso specifico.",
            ),
        ),
        section(
            "sostenibilita",
            "Sostenibilità nel tempo: la vera domanda dei figli",
            p(
                "«Possiamo permettercelo oggi?» è solo metà domanda. L'altra metà: «Reggeremo tra tre anni senza conflitti?» Parlate tra fratelli prima dell'ingresso: quote, imprevisti, chi firma, chi segue le pratiche. Una scelta condivisa regge; una scelta imposta esplode al primo extra.",
                "Molte famiglie del Pinerolese ci dicono che la retta all-inclusive ha eliminato il «mille piccoli bonifici» della badante + spesa + farmaci + riparazioni in casa vuota. Un unico importo, un unico referente, una sola fattura da leggere.",
            ),
        ),
        section(
            "conclusione",
            "Trasparenza economica è cura della famiglia",
            p(
                "Parlare di retta con precisione non è freddezza — è rispetto. Quando numeri, servizi e aspettative sono allineati, il passaggio diventa sereno per l'ospite e per i figli.",
                "Prima di firmare, confrontate almeno due strutture con la stessa griglia di domande. Non per trovare il prezzo più basso, ma per capire dove la qualità della vita e la chiarezza economica coincidono davvero.",
                "Per una stima personalizzata consulta <a href='/rette-e-ammissione/'>rette e ammissione</a>, scopri i <a href='/servizi/'>servizi inclusi</a> e scrivici da <a href='/contatti/'>contatti</a>. Siamo a Pinerolo, Stradale Poirino 152 — rispondiamo con calma, senza pressione commerciale.",
            ),
        ),
    ],
}

# --- Priority: Pinerolo article ---

PINEROLO_ARTICLE = {
    "slug": "coazze-giaveno-pinerolo-servizi",
    "title": "Casa famiglia a Pinerolo: la scelta giusta vicino a Torino",
    "meta_title": "Casa famiglia a Pinerolo: la scelta giusta vicino a Torino",
    "meta_desc": "Cerchi una casa famiglia per anziani vicino a Torino? Scopri perché Pinerolo è la location ideale: verde, tranquilla, a 40 minuti dalla città. Casa Famiglia Quercia.",
    "category": "Servizi locali",
    "badge": "primary",
    "reading": "12 min",
    "keywords": "casa famiglia Pinerolo, casa famiglia vicino Torino, Pinerolese anziani",
    "breadcrumb": "Casa famiglia a Pinerolo: la scelta giusta vicino a Torino",
    "hero_alt": "Casa Famiglia Quercia nel verde del Pinerolese, facilmente raggiungibile da Torino",
    "tags": ["Pinerolo", "Torino", "Pinerolese"],
    "related": ["anziani-autosufficienti-coazze", "costi-retta-casa-famiglia-piemonte", "valle-di-susa-vita-anziani"],
    "wa_text": "Buongiorno, cerchiamo una casa famiglia a Pinerolo vicino Torino e vorremmo informazioni.",
    "intro": p(
        "Cerchi una casa famiglia per anziani vicino a Torino, ma non vuoi rinunciare al verde e alla tranquillità? Pinerolo potrebbe essere la risposta che stavi cercando. A circa 40 minuti dalla città, nel cuore del Pinerolese, trovi un contesto diverso da quello urbano: meno rumore, più spazio, ritmi più umani.",
        "Casa Famiglia Quercia accoglie al massimo 8 anziani autosufficienti in Stradale Poirino 152 — una villa familiare circondata dal verde, pensata per chi è ancora autonomo ma non vuole più vivere da solo. Per iniziare consulta <a href='/servizi/'>servizi</a>, <a href='/rette-e-ammissione/'>rette e ammissione</a> e <a href='/contatti/'>contatti</a>.",
    ),
    "sections": [
        section(
            "perche-pinerolo",
            "Perché Pinerolo e non Torino centro",
            p(
                "Torino offre servizi infiniti — ma anche traffico, smog, ritmi frenetici e case sempre più piccole. Per un anziano autosufficiente che ha passato la vita in provincia, trasferirsi in città può significare perdere il verde, i volti conosciuti e la sensazione di «respirare».",
                "Pinerolo unisce il meglio dei due mondi: comune storico del Pinerolese con farmacie, medici, negozi, mercati e collegamenti rapidi verso Torino (circa 40 km, 35–45 minuti in auto). Il clima è mite, il paesaggio collinare, l'aria migliore. Per molte famiglie torinesi è la soluzione naturale: papà resta «in provincia» ma voi lo raggiungete ogni weekend senza pianificare un'odissea.",
            )
            + h3(
                "Pinerolese: territorio che abbraccia",
                "Dal centro storico di Pinerolo ai borghi collinari, il Pinerolese offre sentieri, piazze, mercati e una comunità ancora umana. Per un ospite che ama la passeggiata e la luce naturale, questo territorio non è secondario — è parte del benessere quotidiano.",
            ),
        ),
        section(
            "distanze-torino",
            "Distanze reali da Torino, Giaveno e dintorni",
            p(
                "Da Torino centro a Casa Famiglia Quercia: circa 40 km via tangenziale e SR-23. Da Giaveno: circa 25 km attraverso la Val Sangone. Da Avigliana: ancora più vicino. Da Pinerolo città: pochi minuti.",
                "La distanza va misurata in «visite sostenibili», non solo chilometri. Se un figlio può passare il mercoledì sera dopo lavoro — non solo il sabato — la qualità della presenza familiare cambia radicalmente. L'ospite non vive in attesa del «grande appuntamento» settimanale.",
                "Simulate una settimana tipo: quante volte potete passare realisticamente? Se la risposta è «almeno due volte», Pinerolo è nel raggio giusto per la maggior parte delle famiglie dell'area metropolitana torinese. Se zero, nessuna distanza basterà — meglio affrontarlo onestamente prima della scelta.",
            ),
        ),
        section(
            "servizi-territorio",
            "Servizi del territorio: farmacie, medici, ospedali",
            p(
                "Pinerolo ha Ospedale Civile, farmacie, ambulatori, specialisti e reti di assistenza domiciliare. Per un anziano autosufficiente che necessita controlli periodici, non serve trasferirsi in città per ogni esigenza routinaria.",
                "Casa Famiglia Quercia collabora con il territorio per appuntamenti, farmaci e comunicazioni con medici di base. La famiglia non resta sola a coordinare tutto da Torino — c'è un referente in casa che conosce l'ospite e sa quando coinvolgervi.",
                "La vicinanza a Torino resta un vantaggio per visite specialistiche più complesse: in un'ora siete in città, ma la vita quotidiana dell'ospite resta nel calmo del Pinerolese — un equilibrio che molte famiglie considerano ideale.",
            ),
        ),
        section(
            "casa-quercia-pinerolo",
            "Casa Famiglia Quercia: cosa offriamo a Pinerolo",
            p(
                "Non siamo una RSA. Siamo una casa vera: massimo 8 ospiti autosufficienti, assistenza h24 discreta, pasti freschi, camere personalizzabili, giardino, attività quotidiane e familiari sempre benvenuti senza orari rigidi.",
                "A differenza di strutture grandi, qui ogni persona è conosciuta per nome. Gli operatori sono gli stessi ogni giorno. Il pranzo è conversazione, non silenzio di reparto. È questo che cercano le famiglie torinesi quando dicono: «Voglio che stia bene, ma non in un ospedale».",
                "Siamo in Stradale Poirino 152, in una villa circondata dal verde del Pinerolese. Gli ospiti mantengono le proprie abitudini — orario del risveglio, preferenze alimentari, oggetti personali in camera — con la sicurezza di avere qualcuno presente anche di notte.",
            )
            + p(
                "Scopri <a href='/servizi/'>tutti i servizi inclusi</a>, visita la <a href='/galleria/'>galleria</a> e leggi <a href='/blog/casa-famiglia-vs-rsa-differenze/'>perché casa famiglia e non RSA</a>. Per i costi, consulta <a href='/rette-e-ammissione/'>rette e ammissione</a>.",
            ),
        ),
        section(
            "visite-famiglia",
            "Visite e presenza familiare: perché la logistica conta",
            p(
                "Una casa famiglia lontana e difficile da raggiungere produce figli assenti e ospiti delusi. Pinerolo risolve questo equilibrio per migliaia di famiglie dell'area metropolitana torinese: abbastanza vicina per visite frequenti, abbastanza lontana dal caos urbano per una vita serena.",
                "Organizzate un calendario condiviso tra fratelli: chi passa quando, chi chiama, chi segue le pratiche amministrative. Una logistica sostenibile mantiene la famiglia unita. Leggi la nostra guida sulle <a href='/blog/visite-familiari-casa-famiglia/'>visite familiari</a>.",
            ),
        ),
        section(
            "conclusione",
            "Pinerolo: la terza via tra solitudine e RSA",
            p(
                "Se tuo padre o tua madre è ancora in gamba ma la casa grande è diventata silenziosa, Pinerolo offre una via d'uscita rispettosa: Casa Famiglia Quercia, nel verde del Pinerolese, a portata di Torino.",
                "Le famiglie che ci scelgono ci dicono spesso la stessa cosa: «Avremmo voluto farlo un anno prima». Agire prima dell'emergenza significa più tempo per ambientarsi, più voce per il genitore nella decisione, meno senso di colpa per i figli.",
                "Non aspettate l'emergenza. Venite a vedere la casa, parlate con chi la vive, fate domande. Consulta <a href='/rette-e-ammissione/'>rette e ammissione</a> e prenota da <a href='/contatti/'>contatti</a>. La visita è gratuita e senza impegno.",
            ),
        ),
    ],
}

# Import remaining articles from existing HTML bodies (already Quercia-branded)
def extract_body_from_html(slug: str) -> str:
    path = os.path.join(BLOG_DIR, slug, "index.html")
    with open(path, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'class="content-prose blog-article__body">\s*(.*?)\s*</div>', html, re.S)
    return m.group(1).strip() if m else ""


def extract_meta_from_html(slug: str) -> dict:
    path = os.path.join(BLOG_DIR, slug, "index.html")
    with open(path, encoding="utf-8") as f:
        html = f.read()

    def meta(name):
        m = re.search(rf'<meta name="{name}" content="([^"]*)"', html)
        return m.group(1) if m else ""

    def tag(pattern):
        m = re.search(pattern, html)
        return m.group(1) if m else ""

    return {
        "title": tag(r"<h1>([^<]+)</h1>"),
        "meta_title": tag(r"<title>([^<]+)</title>"),
        "meta_desc": meta("description"),
        "category": tag(r'badge badge--(?:primary|accent)">([^<]+)</span>'),
        "reading": tag(r"· (\d+ min di lettura)"),
        "keywords": meta("keywords"),
        "breadcrumb": tag(r'aria-current="page">([^<]+)</span>'),
    }


def body_to_sections(body: str) -> list:
    parts = re.split(r'<h2 id="([^"]+)">([^<]+)</h2>', body)
    if len(parts) < 4:
        return [{"id": "contenuto", "title": "Contenuto", "body": body}]
    sections = []
    i = 1
    while i < len(parts):
        sections.append({"id": parts[i], "title": parts[i + 1], "body": parts[i + 2].strip()})
        i += 3
    return sections


def load_existing_article(slug: str) -> dict:
    meta = extract_meta_from_html(slug)
    body = extract_body_from_html(slug)
    intro_m = re.match(r'(<p class="blog-dropcap">.*?</p>(?:\s*<p>.*?</p>)?)', body, re.S)
    intro = intro_m.group(1) if intro_m else ""
    rest = body[len(intro) :].strip() if intro else body
    sections = body_to_sections(rest)
    badge = "accent" if meta["category"] in ("Territorio", "Benessere", "Accoglienza", "Cura relazionale") else "primary"
    return {
        "slug": slug,
        "title": meta["title"],
        "meta_title": meta["meta_title"],
        "meta_desc": meta["meta_desc"],
        "category": meta["category"],
        "badge": badge,
        "reading": meta["reading"].replace(" di lettura", "") if meta["reading"] else "11 min",
        "keywords": meta["keywords"],
        "breadcrumb": meta["breadcrumb"],
        "hero_alt": THUMB_ALT.get(slug, meta["title"]),
        "tags": [],
        "related": [],
        "wa_text": "Buongiorno, vorrei prenotare una visita a Casa Famiglia Quercia a Pinerolo.",
        "intro": intro,
        "sections": sections,
    }


ARTICLE_INDEX = {
    "casa-famiglia-vs-rsa-differenze": {
        "title": RSA_ARTICLE["title"],
        "category": "Guida",
        "badge": "primary",
        "reading": "12 min",
        "excerpt": "RSA o casa famiglia per il tuo caro? Costi, assistenza, libertà e atmosfera: una guida onesta per famiglie in cerca della scelta giusta.",
        "tags": RSA_ARTICLE["tags"],
    },
    "costi-retta-casa-famiglia-piemonte": {
        "title": COSTI_ARTICLE["title"],
        "category": "Costi",
        "badge": "primary",
        "reading": "12 min",
        "excerpt": COSTI_ARTICLE["meta_desc"][:120],
        "tags": COSTI_ARTICLE["tags"],
    },
    "coazze-giaveno-pinerolo-servizi": {
        "title": PINEROLO_ARTICLE["title"],
        "category": "Servizi locali",
        "badge": "primary",
        "reading": "12 min",
        "excerpt": PINEROLO_ARTICLE["meta_desc"][:120],
        "tags": PINEROLO_ARTICLE["tags"],
    },
}


def build_blog_index():
    featured_slug = "casa-famiglia-vs-rsa-differenze"
    all_slugs = [
        "casa-famiglia-vs-rsa-differenze",
        "scegliere-casa-famiglia-genitori",
        "anziani-autosufficienti-coazze",
        "valle-di-susa-vita-anziani",
        "visite-familiari-casa-famiglia",
        "costi-retta-casa-famiglia-piemonte",
        "inserimento-nuovo-ospite",
        "autonomia-dignita-terza-eta",
        "coazze-giaveno-pinerolo-servizi",
        "domande-figli-casa-famiglia",
    ]
    populate_article_index()
    featured = ARTICLE_INDEX[featured_slug]
    categories = sorted({m["category"] for m in ARTICLE_INDEX.values()})
    filter_buttons = '<button type="button" class="blog-filter__btn blog-filter__btn--active" data-filter="all">Tutti</button>' + "".join(
        f'<button type="button" class="blog-filter__btn" data-filter="{html_lib.escape(c)}">{html_lib.escape(c)}</button>'
        for c in categories
    )

    cards = []
    for slug in all_slugs:
        if slug == featured_slug:
            continue
        meta = ARTICLE_INDEX[slug]
        thumb = hero_src(HERO[slug], depth=1)
        tag_html = "".join(
            f'<span class="blog-tag blog-tag--{i % 3}">#{html_lib.escape(t)}</span>'
            for i, t in enumerate(meta.get("tags", [])[:3])
        )
        badge = meta["badge"]
        cards.append(f"""          <article class="card blog-card" data-category="{html_lib.escape(meta['category'])}">
            <a href="/blog/{slug}/" class="blog-card__image-link">
              <img src="{html_lib.escape(thumb)}" alt="{html_lib.escape(THUMB_ALT.get(slug, meta['title']))}" width="400" height="250" loading="lazy" class="blog-card__image">
            </a>
            <div class="card__body">
              <span class="badge badge--{badge} card__category">{html_lib.escape(meta['category'])}</span>
              <p class="card__meta"><time datetime="2026-06-22">22 giugno 2026</time> · {html_lib.escape(meta['reading'])} di lettura</p>
              <h2 class="card__title"><a href="/blog/{slug}/">{html_lib.escape(meta['title'])}</a></h2>
              <p class="card__excerpt">{html_lib.escape(meta['excerpt'])}</p>
              <div class="blog-card__tags">{tag_html}</div>
              <a href="/blog/{slug}/" class="card__read-more">Leggi l'articolo →</a>
            </div>
          </article>""")

    featured_tags = "".join(
        f'<span class="blog-tag blog-tag--{i % 3}">#{html_lib.escape(t)}</span>'
        for i, t in enumerate(featured.get("tags", [])[:3])
    )

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog | Casa Famiglia Quercia – Pinerolo</title>
  <meta name="description" content="Guide e articoli per famiglie: scegliere una casa famiglia, autonomia degli anziani e vita quotidiana serena a Pinerolo.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE}/blog/">
  <link rel="alternate" hreflang="it" href="{SITE}/blog/">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="it_IT">
  <meta property="og:title" content="Blog | Casa Famiglia Quercia – Pinerolo">
  <meta property="og:description" content="Guide e articoli per famiglie: scegliere una casa famiglia, autonomia degli anziani e vita quotidiana serena a Pinerolo.">
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
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Blog","name":"Blog Casa Famiglia Quercia","url":"{SITE}/blog/","description":"Guide per famiglie che scelgono una casa famiglia a Pinerolo","publisher":{{"@type":"Organization","name":"Casa Famiglia Quercia"}}}}</script>
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
        <p class="section__lead blog-index-intro">Quando un genitore inizia a faticare da solo, i figli tra i 45 e i 65 anni si trovano spesso senza una mappa. Internet mescola RSA, case famiglia e residenze assistite; i prezzi sono difficili da confrontare; il senso di colpa rende ogni ricerca un peso. Questo blog è pensato per voi: famiglie del Pinerolese e dell'area torinese che cercano una soluzione serena per un padre o una madre ancora autosufficienti. Qui trovate guide pratiche su differenze tra casa famiglia e RSA, cosa include la retta, visite familiari, inserimento sereno e vita quotidiana a Pinerolo. Ogni articolo nasce dall'esperienza quotidiana di Casa Famiglia Quercia: una casa vera, non un reparto, dove al massimo 8 anziani autosufficienti trovano compagnia, sicurezza e autonomia.</p>
      </div>
    </header>

    <section class="section blog-featured">
      <div class="container">
        <article class="blog-featured__card">
          <a href="/blog/casa-famiglia-vs-rsa-differenze/" class="blog-featured__image-wrap">
            <img src="{hero_src(DINING, 1)}" alt="{html_lib.escape(featured['title'])}" width="1200" height="600" loading="eager" class="blog-featured__image">
          </a>
          <div class="blog-featured__content">
            <span class="badge badge--primary">In evidenza</span>
            <span class="badge badge--primary">Guida</span>
            <p class="blog-featured__meta"><time datetime="2026-06-22">22 giugno 2026</time> · 12 min di lettura</p>
            <h2 class="blog-featured__title"><a href="/blog/casa-famiglia-vs-rsa-differenze/">{html_lib.escape(featured['title'])}</a></h2>
            <p class="blog-featured__excerpt">{html_lib.escape(featured['excerpt'])}</p>
            <div class="blog-card__tags">{featured_tags}</div>
            <a href="/blog/casa-famiglia-vs-rsa-differenze/" class="btn btn--primary">Leggi l'articolo in evidenza</a>
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
    var cards = document.querySelectorAll('.blog-card');
    buttons.forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        buttons.forEach(function (b) {{ b.classList.remove('blog-filter__btn--active'); }});
        btn.classList.add('blog-filter__btn--active');
        var filter = btn.getAttribute('data-filter');
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


RELATED_MAP = {
    "scegliere-casa-famiglia-genitori": ["domande-figli-casa-famiglia", "inserimento-nuovo-ospite", "casa-famiglia-vs-rsa-differenze"],
    "anziani-autosufficienti-coazze": ["valle-di-susa-vita-anziani", "autonomia-dignita-terza-eta", "coazze-giaveno-pinerolo-servizi"],
    "valle-di-susa-vita-anziani": ["anziani-autosufficienti-coazze", "coazze-giaveno-pinerolo-servizi", "autonomia-dignita-terza-eta"],
    "visite-familiari-casa-famiglia": ["inserimento-nuovo-ospite", "domande-figli-casa-famiglia", "scegliere-casa-famiglia-genitori"],
    "inserimento-nuovo-ospite": ["visite-familiari-casa-famiglia", "scegliere-casa-famiglia-genitori", "autonomia-dignita-terza-eta"],
    "autonomia-dignita-terza-eta": ["casa-famiglia-vs-rsa-differenze", "anziani-autosufficienti-coazze", "visite-familiari-casa-famiglia"],
    "domande-figli-casa-famiglia": ["scegliere-casa-famiglia-genitori", "costi-retta-casa-famiglia-piemonte", "casa-famiglia-vs-rsa-differenze"],
}


def populate_article_index():
    all_slugs = list(HERO.keys())
    for slug in all_slugs:
        if slug in ARTICLE_INDEX:
            continue
        meta = extract_meta_from_html(slug)
        ARTICLE_INDEX[slug] = {
            "title": meta["title"],
            "category": meta["category"],
            "badge": "accent"
            if meta["category"] in ("Territorio", "Benessere", "Accoglienza", "Cura relazionale")
            else "primary",
            "reading": meta["reading"].replace(" di lettura", "") if meta.get("reading") else "11 min",
            "excerpt": meta["meta_desc"][:120] if meta.get("meta_desc") else "",
            "tags": [],
        }


def main():
    priority = {
        "casa-famiglia-vs-rsa-differenze": RSA_ARTICLE,
        "costi-retta-casa-famiglia-piemonte": COSTI_ARTICLE,
        "coazze-giaveno-pinerolo-servizi": PINEROLO_ARTICLE,
    }
    all_slugs = list(HERO.keys())
    populate_article_index()

    for slug in all_slugs:
        if slug in priority:
            article = priority[slug]
        else:
            article = load_existing_article(slug)
            article["related"] = RELATED_MAP.get(slug, [])

        html_path = os.path.join(BLOG_DIR, slug, "index.html")
        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        body = sections_to_body(article)
        wc = word_count_html(body)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(build_html(article))
        status = "OK" if wc >= 800 else "SHORT"
        print(f"{status:5} {wc:4d}  {slug}")

    build_blog_index()
    print("Built blog/index.html")


if __name__ == "__main__":
    main()
