#!/usr/bin/env node
/**
 * Validates that published site content reflects max 6 guests (not 8).
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

const SCAN_DIRS = [
  '.',
  'blog',
  'content',
  'partials',
  'casa-famiglia-avigliana',
  'casa-famiglia-coazze',
  'casa-famiglia-giaveno',
  'casa-famiglia-pinerolo',
  'casa-famiglia-valle-di-susa',
  'chi-siamo',
  'contatti',
  'galleria',
  'la-giornata',
  'la-struttura',
  'rette-e-ammissione',
  'servizi',
  'storia',
  'requisiti-autosufficienza',
];

const EXTENSIONS = new Set(['.html', '.md', '.js', '.py']);

const FORBIDDEN_PATTERNS = [
  /8\s+ospiti/i,
  /max\s+8\s+ospiti/i,
  /massimo\s+8\s+(ospiti|persone|anziani)/i,
  /al\s+massimo\s+8\s+(ospiti|persone|anziani)/i,
  /accogli(e|amo)\s+al\s+massimo\s+8/i,
  /trust-stat__number">8</,
  /maximumAttendeeCapacity":8\b/,
];

function collectFiles(dir, files = []) {
  if (!fs.existsSync(dir)) return files;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      collectFiles(full, files);
    } else if (EXTENSIONS.has(path.extname(entry.name))) {
      files.push(full);
    }
  }
  return files;
}

const files = SCAN_DIRS.flatMap((dir) => collectFiles(path.join(ROOT, dir)));
const violations = [];

for (const file of files) {
  const rel = path.relative(ROOT, file);
  if (rel === 'scripts/validate-guest-count.js') continue;

  const content = fs.readFileSync(file, 'utf8');
  for (const pattern of FORBIDDEN_PATTERNS) {
    const match = content.match(pattern);
    if (match) {
      violations.push({ file: rel, match: match[0] });
    }
  }
}

if (violations.length > 0) {
  console.error('Guest count validation failed. Found references to 8 guests:\n');
  for (const { file, match } of violations) {
    console.error(`  ${file}: "${match}"`);
  }
  process.exit(1);
}

const homepage = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
if (!homepage.includes('trust-stat__number">6</span>')) {
  console.error('Homepage trust bar must show 6 guests.');
  process.exit(1);
}

console.log(`Guest count OK (max 6 ospiti) — checked ${files.length} files.`);
