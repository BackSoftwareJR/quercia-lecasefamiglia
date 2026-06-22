#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

const CSS_STACK = [
  'design-system.css',
  'global.css',
  'animations.css',
  'components.css',
  'pages.css'
];

function walk(dir, files = []) {
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    if (name === 'node_modules' || name === '.git') continue;
    if (fs.statSync(p).isDirectory()) walk(p, files);
    else if (name === 'index.html' || name === '404.html') files.push(p);
  }
  return files;
}

function fixFile(file) {
  let html = fs.readFileSync(file, 'utf8');
  const rel = path.relative(ROOT, path.dirname(file));
  const depth = rel === '' ? 0 : rel.split(path.sep).length;
  const prefix = depth === 0 ? '' : '../'.repeat(depth);

  if (!html.includes('components.css') && !html.includes('design-system.css')) return false;

  // Skip if already full css/ stack with global.css
  if (html.includes(`${prefix}css/global.css`)) return false;

  const links = CSS_STACK.map(function (f) {
    return `  <link rel="stylesheet" href="${prefix}css/${f}">`;
  }).join('\n');

  // Remove old stylesheet links (root or partial css)
  let next = html.replace(/\s*<link rel="stylesheet" href="[^"]*(?:design-system|components|pages|global|animations)[^"]*">\n?/g, '\n');

  // Insert after font link or before first script
  const fontMatch = next.match(/<link href="https:\/\/fonts\.googleapis\.com[^>]+>\n/);
  if (fontMatch) {
    next = next.replace(fontMatch[0], fontMatch[0] + links + '\n');
  } else {
    next = next.replace('</head>', links + '\n</head>');
  }

  // Ensure cookie-banner.js on pages with footer partial
  if (next.includes('data-include="footer"') && !next.includes('cookie-banner.js')) {
    next = next.replace(
      /(<script src="[^"]*main\.js"><\/script>\n)/,
      '$1  <script src="' + prefix + 'js/cookie-banner.js"></script>\n'
    );
  }

  if (next !== html) {
    fs.writeFileSync(file, next, 'utf8');
    console.log('Fixed', path.relative(ROOT, file));
    return true;
  }
  return false;
}

walk(ROOT).forEach(fixFile);
