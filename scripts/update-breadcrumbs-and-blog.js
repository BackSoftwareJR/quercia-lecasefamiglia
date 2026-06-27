#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

const breadcrumbUpdates = [
  {
    file: 'storia/index.html',
    html: `        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><a href="/chi-siamo/">Chi siamo</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">La nostra storia</span></li>`,
    json: `[{"@type":"ListItem","position":1,"name":"Home","item":"https://casafamigliaquercia.it/"},{"@type":"ListItem","position":2,"name":"Chi siamo","item":"https://casafamigliaquercia.it/chi-siamo/"},{"@type":"ListItem","position":3,"name":"La nostra storia","item":"https://casafamigliaquercia.it/storia/"}]`,
    oldHtml: `        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">La nostra storia</span></li>`,
    oldJson: `[{"@type":"ListItem","position":1,"name":"Home","item":"https://casafamigliaquercia.it/"},{"@type":"ListItem","position":2,"name":"La nostra storia","item":"https://casafamigliaquercia.it/storia/"}]`,
  },
  {
    file: 'requisiti-autosufficienza/index.html',
    html: `        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><a href="/rette-e-ammissione/">Rette e ammissione</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">Requisiti autosufficienza</span></li>`,
    json: `[{"@type":"ListItem","position":1,"name":"Home","item":"https://casafamigliaquercia.it/"},{"@type":"ListItem","position":2,"name":"Rette e ammissione","item":"https://casafamigliaquercia.it/rette-e-ammissione/"},{"@type":"ListItem","position":3,"name":"Requisiti autosufficienza","item":"https://casafamigliaquercia.it/requisiti-autosufficienza/"}]`,
    oldHtml: `        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">Requisiti autosufficienza</span></li>`,
    oldJson: `[{"@type":"ListItem","position":1,"name":"Home","item":"https://casafamigliaquercia.it/"},{"@type":"ListItem","position":2,"name":"Requisiti autosufficienza","item":"https://casafamigliaquercia.it/requisiti-autosufficienza/"}]`,
  },
  {
    file: 'casa-famiglia-pinerolo/index.html',
    category: 'Casa famiglia a Pinerolo',
    page: 'Casa famiglia anziani autosufficienti a Pinerolo',
    url: 'https://casafamigliaquercia.it/casa-famiglia-pinerolo/',
  },
  {
    file: 'casa-famiglia-coazze/index.html',
    category: 'Zone servite',
    page: 'Casa famiglia per famiglie di Coazze',
    url: 'https://casafamigliaquercia.it/casa-famiglia-coazze/',
  },
  {
    file: 'casa-famiglia-giaveno/index.html',
    category: 'Casa famiglia vicino Giaveno',
    page: 'Casa famiglia per anziani vicino Giaveno',
    url: 'https://casafamigliaquercia.it/casa-famiglia-giaveno/',
  },
  {
    file: 'casa-famiglia-avigliana/index.html',
    category: 'Casa famiglia vicino Avigliana',
    page: 'Casa famiglia per anziani vicino Avigliana',
    url: 'https://casafamigliaquercia.it/casa-famiglia-avigliana/',
  },
  {
    file: 'casa-famiglia-valle-di-susa/index.html',
    category: 'Zone servite',
    page: 'Casa famiglia nel Pinerolese',
    url: 'https://casafamigliaquercia.it/casa-famiglia-valle-di-susa/',
  },
  {
    file: 'privacy-policy/index.html',
    category: 'Legale',
    page: 'Privacy Policy',
    url: 'https://casafamigliaquercia.it/privacy-policy/',
  },
  {
    file: 'cookie-policy/index.html',
    category: 'Legale',
    page: 'Cookie Policy',
    url: 'https://casafamigliaquercia.it/cookie-policy/',
  },
  {
    file: 'termini-e-condizioni/index.html',
    category: 'Legale',
    page: 'Termini e condizioni',
    url: 'https://casafamigliaquercia.it/termini-e-condizioni/',
  },
];

function zoneBreadcrumb(item) {
  return {
    html: `        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><a href="/casa-famiglia-pinerolo/">Zone servite</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">${item.page}</span></li>`,
    json: `[{"@type":"ListItem","position":1,"name":"Home","item":"https://casafamigliaquercia.it/"},{"@type":"ListItem","position":2,"name":"Zone servite","item":"https://casafamigliaquercia.it/casa-famiglia-pinerolo/"},{"@type":"ListItem","position":3,"name":"${item.page}","item":"${item.url}"}]`,
  };
}

function legalBreadcrumb(item) {
  return {
    html: `        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><a href="/privacy-policy/">Legale</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">${item.page}</span></li>`,
    json: `[{"@type":"ListItem","position":1,"name":"Home","item":"https://casafamigliaquercia.it/"},{"@type":"ListItem","position":2,"name":"Legale","item":"https://casafamigliaquercia.it/privacy-policy/"},{"@type":"ListItem","position":3,"name":"${item.page}","item":"${item.url}"}]`,
  };
}

function updateBreadcrumbs() {
  breadcrumbUpdates.forEach(function (item) {
    const filePath = path.join(ROOT, item.file);
    let content = fs.readFileSync(filePath, 'utf8');

    let html, json;
    if (item.html) {
      html = item.html;
      json = item.json;
    } else if (item.file.startsWith('casa-famiglia')) {
      const z = zoneBreadcrumb(item);
      html = z.html;
      json = z.json;
    } else {
      const l = legalBreadcrumb(item);
      html = l.html;
      json = l.json;
    }

    if (item.oldHtml) {
      content = content.replace(item.oldHtml, html);
      content = content.replace(item.oldJson, json);
    } else {
      content = content.replace(
        /<ol class="breadcrumbs__list">[\s\S]*?<\/ol>/,
        `<ol class="breadcrumbs__list">\n${html}\n      </ol>`
      );
      content = content.replace(
        /"@type":"BreadcrumbList","itemListElement":\[[\s\S]*?\]/,
        `"@type":"BreadcrumbList","itemListElement":${json}`
      );
      content = content.replace(
        /"itemListElement":\[[\s\S]*?\](?=\s*\})/,
        `"itemListElement":${json}`
      );
    }

    fs.writeFileSync(filePath, content);
    console.log('Updated breadcrumbs:', item.file);
  });

  const notFoundPath = path.join(ROOT, '404.html');
  let notFound = fs.readFileSync(notFoundPath, 'utf8');
  if (!notFound.includes('breadcrumbs')) {
    notFound = notFound.replace(
      '<main id="main" class="error-page"',
      `<nav class="breadcrumbs container" aria-label="Breadcrumb">
      <ol class="breadcrumbs__list">
        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">Pagina non trovata</span></li>
      </ol>
    </nav>
  <main id="main" class="error-page"`
    );
    fs.writeFileSync(notFoundPath, notFound);
    console.log('Updated breadcrumbs: 404.html');
  }
}

function addBlogApprofondimenti() {
  const blogDir = path.join(ROOT, 'blog');
  const entries = fs.readdirSync(blogDir, { withFileTypes: true });

  entries.forEach(function (entry) {
    if (!entry.isDirectory()) return;
    const indexPath = path.join(blogDir, entry.name, 'index.html');
    if (!fs.existsSync(indexPath)) return;

    let content = fs.readFileSync(indexPath, 'utf8');
    if (content.includes('blog-approfondimenti')) {
      console.log('Skipped (already has approfondimenti):', entry.name);
      return;
    }

    const relatedMatch = content.match(
      /<div class="blog-sidebar-box blog-sidebar-related">[\s\S]*?<ul class="blog-sidebar-related__list">([\s\S]*?)<\/ul>/
    );
    if (!relatedMatch) {
      console.warn('No related block:', entry.name);
      return;
    }

    const links = [];
    const linkRegex = /<a href="([^"]+)" class="blog-sidebar-related__link">[\s\S]*?<span class="blog-sidebar-related__title">([^<]+)<\/span>/g;
    let m;
    while ((m = linkRegex.exec(relatedMatch[1])) !== null) {
      links.push({ href: m[1], title: m[2].trim() });
    }

    if (!links.length) return;

    const listItems = links
      .map(function (link) {
        return `            <li><a href="${link.href}">${link.title}</a></li>`;
      })
      .join('\n');

    const block = `
          <section class="blog-approfondimenti" aria-labelledby="approfondimenti-${entry.name}">
            <h2 id="approfondimenti-${entry.name}">Approfondimenti</h2>
            <ul class="blog-approfondimenti__list">
${listItems}
            </ul>
            <p class="blog-approfondimenti__more"><a href="/blog/">Tutti gli articoli del blog</a></p>
          </section>`;

    content = content.replace(
      /(\s*)<\/section>\s*<\/div>\s*<aside class="blog-article-sidebar"/,
      `${block}$1</section>\n        </div>\n        <aside class="blog-article-sidebar"`
    );

    if (!content.includes('blog-approfondimenti')) {
      content = content.replace(
        /(\s*)<\/div>\s*<\/div>\s*<aside class="blog-article-sidebar"/,
        `${block}$1</div>\n        </div>\n        <aside class="blog-article-sidebar"`
      );
    }

    fs.writeFileSync(indexPath, content);
    console.log('Added approfondimenti:', entry.name);
  });
}

updateBreadcrumbs();
addBlogApprofondimenti();