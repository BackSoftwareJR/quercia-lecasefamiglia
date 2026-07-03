#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const Critters = require('critters');

const ROOT = path.resolve(__dirname, '..');
const CRITICAL_CSS_PATH = path.join(ROOT, 'css/critical.css');

const PARTIALS = {
  header: fs.readFileSync(path.join(ROOT, 'partials/header.html'), 'utf8'),
  footer: fs.readFileSync(path.join(ROOT, 'partials/footer.html'), 'utf8'),
};

const SKIP_HTML = new Set(['googled383cece6ecba048.html']);

const ASYNC_STYLESHEET_RE =
  /<link rel="stylesheet" href="([^"]+)" media="print" onload="[^"]*">\s*<noscript><link rel="stylesheet" href="\1"><\/noscript>/gi;

const PRELOAD_STYLESHEET_RE =
  /<link rel="preload" href="([^"]+)" as="style" onload="[^"]*">\s*<noscript><link rel="stylesheet" href="\1"><\/noscript>/gi;

const CRITICAL_STYLE_RE =
  /<style[^>]*(?:id="critical-css"|data-critical)[^>]*>[\s\S]*?<\/style>\s*/i;

function inlinePartials(html) {
  return html
    .replace(/<div data-include="header"><\/div>/g, PARTIALS.header)
    .replace(/<div data-include="footer"><\/div>/g, PARTIALS.footer);
}

function hrefToAbsolute(href, filePath) {
  if (href.startsWith('http') || href.startsWith('//') || href.startsWith('/')) {
    return href;
  }
  const resolved = path.resolve(path.dirname(filePath), href);
  return `/${path.relative(ROOT, resolved).split(path.sep).join('/')}`;
}

function toBlockingStylesheets(html, filePath) {
  let result = html.replace(CRITICAL_STYLE_RE, '');
  result = result.replace(ASYNC_STYLESHEET_RE, (_, href) => {
    return `<link rel="stylesheet" href="${hrefToAbsolute(href, filePath)}">`;
  });
  result = result.replace(PRELOAD_STYLESHEET_RE, (_, href) => {
    return `<link rel="stylesheet" href="${hrefToAbsolute(href, filePath)}">`;
  });
  result = result.replace(
    /<link rel="stylesheet" href="([^"]+)">/gi,
    (match, href) => {
      if (href.startsWith('http') || href.startsWith('//')) {
        return match;
      }
      return `<link rel="stylesheet" href="${hrefToAbsolute(href, filePath)}">`;
    },
  );
  return result;
}

function extractCriticalStyle(headHtml) {
  const match =
    headHtml.match(/<style[^>]*data-critical[^>]*>[\s\S]*<\/style>/i) ||
    headHtml.match(/<style>[\s\S]*<\/style>/i);
  if (!match) return '';
  return match[0].replace(/<style([^>]*)>/i, '<style data-critical$1>');
}

function collectLocalStylesheetHrefs(html) {
  const hrefs = new Set();
  const patterns = [
    /<link rel="stylesheet" href="([^"]+\.css)"[^>]*>/gi,
    /<link rel="preload" href="([^"]+\.css)" as="style"[^>]*>/gi,
  ];

  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(html)) !== null) {
      if (!match[1].startsWith('http')) {
        hrefs.add(match[1]);
      }
    }
  }

  return [...hrefs];
}

function asyncStylesheetMarkup(href) {
  return (
    `  <link rel="preload" href="${href}" as="style" onload="this.onload=null;this.rel='stylesheet'">\n` +
    `  <noscript><link rel="stylesheet" href="${href}"></noscript>`
  );
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function replaceLocalStylesheets(html) {
  let result = html;
  for (const href of collectLocalStylesheetHrefs(html)) {
    const blockPattern = new RegExp(
      `<link rel="preload" href="${escapeRegExp(href)}" as="style" onload="[^"]*">\\s*<noscript>\\s*<link rel="stylesheet" href="${escapeRegExp(href)}">\\s*<\\/noscript>|<link rel="stylesheet" href="${escapeRegExp(href)}"(?: media="print")? onload="[^"]*">\\s*<noscript><link rel="stylesheet" href="${escapeRegExp(href)}"><\\/noscript>|<link rel="stylesheet" href="${escapeRegExp(href)}" onload="[^"]*">\\s*<noscript><link rel="stylesheet" href="${escapeRegExp(href)}"><\\/noscript>|<link rel="stylesheet" href="${escapeRegExp(href)}">`,
      'gi',
    );
    result = result.replace(blockPattern, asyncStylesheetMarkup(href));
  }
  return result;
}

function applyHeadOptimizations(originalHtml, processedHead, filePath, fallbackCritical) {
  const criticalStyle = extractCriticalStyle(processedHead) || fallbackCritical;
  if (!criticalStyle) {
    throw new Error(`No critical CSS available for ${path.relative(ROOT, filePath)}`);
  }

  let html = originalHtml.replace(CRITICAL_STYLE_RE, '');
  html = replaceLocalStylesheets(html);

  const insertMarker =
    html.match(/\n  <link rel="preload" as="style" href="https:\/\/fonts\.googleapis\.com/i) ||
    html.match(/\n  <link rel="preload" href="[^"]+\.css" as="style"/i) ||
    html.match(/\n  <link rel="stylesheet" href="[^"]+\.css"/i);

  if (insertMarker) {
    html = html.replace(insertMarker[0], `\n  ${criticalStyle}${insertMarker[0]}`);
  } else {
    html = html.replace('</head>', `  ${criticalStyle}\n</head>`);
  }

  return html;
}

function collectHtmlFiles() {
  const files = [];

  for (const entry of fs.readdirSync(ROOT, { withFileTypes: true })) {
    if (entry.isFile() && entry.name.endsWith('.html') && !SKIP_HTML.has(entry.name)) {
      files.push(path.join(ROOT, entry.name));
    }
  }

  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory() && entry.name !== 'node_modules' && entry.name !== 'partials') {
        walk(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.html')) {
        files.push(fullPath);
      }
    }
  }

  for (const entry of fs.readdirSync(ROOT, { withFileTypes: true })) {
    if (entry.isDirectory() && !['node_modules', 'partials', 'scripts', 'content'].includes(entry.name)) {
      walk(path.join(ROOT, entry.name));
    }
  }

  return [...new Set(files)].sort();
}

async function main() {
  const critters = new Critters({
    path: ROOT,
    publicPath: '/',
    preload: 'swap',
    pruneSource: false,
    logLevel: 'warn',
  });

  const htmlFiles = collectHtmlFiles();
  const indexPath = path.join(ROOT, 'index.html');
  const orderedFiles = [
    ...(htmlFiles.includes(indexPath) ? [indexPath] : []),
    ...htmlFiles.filter((filePath) => filePath !== indexPath),
  ];
  let sharedFallbackCritical = '';

  for (const filePath of orderedFiles) {
    const originalHtml = fs.readFileSync(filePath, 'utf8');
    const expandedHtml = inlinePartials(originalHtml);
    const crittersInput = toBlockingStylesheets(expandedHtml, filePath);
    const processed = await critters.process(crittersInput);
    const processedHead = processed.match(/<head>([\s\S]*?)<\/head>/i)?.[1] || '';
    const pageCritical = extractCriticalStyle(processedHead);
    const fallbackCritical = sharedFallbackCritical || pageCritical;
    const optimizedHtml = applyHeadOptimizations(
      originalHtml,
      processedHead,
      filePath,
      fallbackCritical,
    );

    if (optimizedHtml !== originalHtml) {
      fs.writeFileSync(filePath, optimizedHtml);
      console.log(`updated: ${path.relative(ROOT, filePath)}`);
    }

    if (filePath === path.join(ROOT, 'index.html')) {
      const styleMatch = optimizedHtml.match(/<style data-critical>([\s\S]*)<\/style>/i);
      if (styleMatch) {
        sharedFallbackCritical = `<style data-critical>${styleMatch[1]}</style>`;
        fs.writeFileSync(CRITICAL_CSS_PATH, styleMatch[1]);
        console.log(`updated: css/critical.css (${styleMatch[1].length} bytes)`);
      }
    } else if (!sharedFallbackCritical && pageCritical) {
      sharedFallbackCritical = pageCritical;
    }
  }

  if (!sharedFallbackCritical && fs.existsSync(CRITICAL_CSS_PATH)) {
    sharedFallbackCritical = `<style data-critical>${fs.readFileSync(CRITICAL_CSS_PATH, 'utf8')}</style>`;
  }

  console.log(`Done. Processed ${htmlFiles.length} HTML file(s).`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
