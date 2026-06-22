#!/usr/bin/env node
/**
 * Genera landing pages geografiche SEO
 */
const fs = require('fs');
const path = require('path');

const BASE = path.join(__dirname, '..');

const pages = [
  {
    slug: 'casa-famiglia-coazze',
    title: 'Casa famiglia anziani Coazze | Gramsci',
    meta: 'Casa famiglia per anziani autosufficienti a Coazze (TO). Villa familiare in Valle di Susa, assistenza 24h, pasti di casa. Prenota una visita gratuita.',
    h1: 'Casa famiglia per anziani a Coazze',
    lead: 'Nel cuore della Valle di Susa, a Piazza Gramsci 17, accogliamo anziani autosufficienti in una villa familiare circondata dal verde.',
    distance: 'Siamo nel centro di Coazze, comune della Valle di Susa a circa 30 km da Torino.',
    local: 'Coazze è un paese di montagna con aria pulita, sentieri, comunità accogliente. Ideale per chi ama la natura e vuole restare vicino al proprio territorio.',
    keyword: 'casa famiglia anziani Coazze'
  },
  {
    slug: 'casa-famiglia-giaveno',
    title: 'Casa famiglia anziani Giaveno | Vicino Coazze',
    meta: 'Cerchi una casa famiglia per genitori autosufficienti vicino Giaveno? Casa Famiglia Gramsci a Coazze è a pochi minuti. Visita gratuita.',
    h1: 'Casa famiglia per anziani vicino Giaveno',
    lead: 'Se abitate a Giaveno o nelle valli limitrofe e cercate una soluzione serena per un genitore autosufficiente, Casa Famiglia Gramsci a Coazze è raggiungibile in pochi minuti.',
    distance: 'Da Giaveno a Coazze: circa 15–20 minuti in auto, percorrendo la Valle di Susa.',
    local: 'Molte famiglie di Giaveno ci scelgono per la vicinanza: visite frequenti, nipoti che vengono nel weekend, senza lunghi tragitti.',
    keyword: 'casa famiglia anziani Giaveno'
  },
  {
    slug: 'casa-famiglia-pinerolo',
    title: 'Casa famiglia anziani Pinerolo | Valle Susa',
    meta: 'Casa famiglia per anziani autosufficienti vicino Pinerolo. Casa Gramsci a Coazze: ambiente familiare, natura, assistenza discreta h24.',
    h1: 'Casa famiglia per anziani vicino Pinerolo',
    lead: 'Da Pinerolo e dintorni, raggiungere Casa Famiglia Gramsci a Coazze è semplice. Offriamo un\'alternativa calda alle RSA per genitori ancora autonomi.',
    distance: 'Da Pinerolo a Coazze: circa 25–35 minuti in auto attraverso la Valle di Susa.',
    local: 'Pinerolo e Coazze condividono la stessa valle: paesaggio, tradizioni, legami familiari che spesso attraversano i comuni limitrofi.',
    keyword: 'casa famiglia anziani Pinerolo'
  },
  {
    slug: 'casa-famiglia-valle-di-susa',
    title: 'Casa famiglia Valle di Susa | Anziani autosufficienti',
    meta: 'Casa famiglia per anziani autosufficienti in Valle di Susa. Coazze, natura, assistenza 24h e vita di comunità. Gramsci — una seconda casa.',
    h1: 'Casa famiglia in Valle di Susa per anziani autosufficienti',
    lead: 'La Valle di Susa offre qualità della vita rara: aria buona, montagne, comunità umana. Casa Famiglia Gramsci a Coazze è pensata per chi vuole invecchiare bene qui.',
    distance: 'Siamo a Coazze, nel cuore della valle, facilmente raggiungibili da Giaveno, Avigliana, Pinerolo, Susa e Torino.',
    local: 'Vivere in valle significa ritmi più lenti, passeggiate nel verde, meno stress urbano — benefici documentati per il benessere degli anziani.',
    keyword: 'casa famiglia Valle di Susa anziani'
  },
  {
    slug: 'casa-famiglia-avigliana',
    title: 'Casa famiglia anziani Avigliana | Coazze',
    meta: 'Casa famiglia per anziani autosufficienti vicino Avigliana. Casa Gramsci a Coazze in Valle di Susa. Ambiente familiare, visita gratuita.',
    h1: 'Casa famiglia per anziani vicino Avigliana',
    lead: 'Le famiglie di Avigliana che cercano una casa famiglia per genitori autosufficienti trovano in Casa Gramsci a Coazze una risposta vicina e umana.',
    distance: 'Da Avigliana a Coazze: circa 20–30 minuti in auto, seguendo la Valle di Susa.',
    local: 'Avigliana e Coazze sono collegate dalla stessa valle: molti nostri ospiti hanno figli e nipoti che vivono tra i due comuni.',
    keyword: 'casa famiglia anziani Avigliana'
  }
];

function buildPage(p) {
  const url = `https://gramsci.lecasefamiglia.it/${p.slug}/`;
  return `<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${p.title}</title>
  <meta name="description" content="${p.meta}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="${url}">
  <meta property="og:title" content="${p.title}">
  <meta property="og:description" content="${p.meta}">
  <meta property="og:url" content="${url}">
  <meta name="theme-color" content="#2d5a3d">
  <link rel="icon" href="../images/favicon.ico" type="image/x-icon">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/design-system.css">
  <link rel="stylesheet" href="../css/global.css">
  <link rel="stylesheet" href="../css/animations.css">
  <link rel="stylesheet" href="../css/components.css">
  <link rel="stylesheet" href="../css/pages.css">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"LodgingBusiness","name":"Casa Famiglia Gramsci","description":"${p.meta.replace(/"/g, '\\"')}","url":"${url}","telephone":"+39 376 203 1211","address":{"@type":"PostalAddress","streetAddress":"Piazza Gramsci, 17","addressLocality":"Coazze","postalCode":"10050","addressCountry":"IT"}}</script>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://gramsci.lecasefamiglia.it/"},{"@type":"ListItem","position":2,"name":"${p.h1.replace(/"/g, '')}","item":"${url}"}]}</script>
</head>
<body>
  <a href="#main" class="skip-link">Vai al contenuto principale</a>
  <div data-include="header"></div>
  <main id="main">
    <nav class="breadcrumbs container" aria-label="Breadcrumb">
      <ol class="breadcrumbs__list">
        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">${p.h1}</span></li>
      </ol>
    </nav>
    <header class="landing-hero">
      <div class="container">
        <p class="section__eyebrow">Casa Famiglia Gramsci · Coazze</p>
        <h1>${p.h1}</h1>
        <p class="section__lead" style="max-width: 42rem;">${p.lead}</p>
        <div class="btn-group" style="margin-top: var(--space-8);">
          <a href="tel:+393762031211" class="btn btn--accent btn--lg">Chiama ora</a>
          <a href="/contatti/" class="btn btn--ghost btn--lg">Prenota visita gratuita</a>
        </div>
      </div>
    </header>
    <section class="section">
      <div class="container">
        <div class="problem-split">
          <div class="content-prose">
            <h2>Perché scegliere una casa famiglia</h2>
            <p>Se stai cercando "${p.keyword}", probabilmente hai un genitore ancora in salute ma solo a casa. La solitudine pesa. Una RSA sembra eccessiva. La casa famiglia è la terza via: ambiente domestico, pochi ospiti, assistenza discreta h24.</p>
            <p>${p.distance}</p>
            <p>${p.local}</p>
            <h2>Cosa offriamo</h2>
            <ul>
              <li>Camera personale con i propri oggetti e ricordi</li>
              <li>Pasti preparati in casa, non mensa istituzionale</li>
              <li>Attività quotidiane: ginnastica dolce, giardinaggio, socialità</li>
              <li>Assistenza 24 ore, presente ma non invadente</li>
              <li>Visite familiari sempre benvenute, senza orari rigidi</li>
            </ul>
            <h2>Non siamo una RSA</h2>
            <p>Accogliamo solo anziani <strong>autosufficienti</strong> over 65. Niente atmosfera ospedaliera, niente reparti. Una villa familiare nel verde. <a href="/requisiti-autosufficienza/">Scopri i requisiti</a>.</p>
            <h2>Come iniziare</h2>
            <p>Chiamaci o scrivici su WhatsApp. Raccontaci la situazione di tuo padre o tua madre. Organizziamo una visita gratuita — portatelo con voi, fate tutte le domande che volete.</p>
            <p>
              <a href="/servizi/">Servizi</a> ·
              <a href="/galleria/">Galleria foto</a> ·
              <a href="/storia/">La nostra storia</a> ·
              <a href="/rette-e-ammissione/">Rette e ammissione</a> ·
              <a href="/blog/">Blog per famiglie</a>
            </p>
          </div>
          <div class="problem-split__image">
            <img src="../images/Coazze - Casa Famiglia Gramsci/Sala da Pranzo + persone 1.avif" alt="Sala da pranzo accogliente Casa Famiglia Gramsci ${p.keyword}" width="800" height="600" loading="lazy">
          </div>
        </div>
      </div>
    </section>
    <section class="section section--alt">
      <div class="container landing-benefits">
        <article class="landing-benefit">
          <h3>Vicino a te</h3>
          <p>Raggiungibile dalle famiglie della zona. Visite frequenti, legami che restano vivi.</p>
        </article>
        <article class="landing-benefit">
          <h3>Natura e serenità</h3>
          <p>Valle di Susa: aria pulita, giardino, ritmi lenti. Benessere per la terza età.</p>
        </article>
        <article class="landing-benefit">
          <h3>Trasparenza</h3>
          <p>Retta chiara, nessun costo nascosto. Ti spieghiamo tutto al telefono.</p>
        </article>
      </div>
    </section>
    <section class="cta-band">
      <div class="container">
        <h2>Hai altre domande?</h2>
        <p>Ti aiutiamo noi — con calma, senza pressione commerciale.</p>
        <div class="btn-group" style="justify-content: center;">
          <a href="/contatti/" class="btn btn--accent btn--lg">Contattaci</a>
          <a href="https://www.lecasefamiglia.it/" class="btn btn--ghost btn--lg" target="_blank" rel="noopener noreferrer">Scopri di più</a>
        </div>
      </div>
    </section>
  </main>
  <div data-include="footer"></div>
  <script src="../tokens.js"></script>
  <script src="../js/includes.js"></script>
  <script src="../js/nav.js"></script>
  <script src="../js/main.js"></script>
  <script src="../js/cookie-banner.js"></script>
</body>
</html>`;
}

pages.forEach(function (p) {
  const dir = path.join(BASE, p.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), buildPage(p), 'utf8');
  console.log('Created', p.slug);
});
