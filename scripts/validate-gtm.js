const fs = require('fs');
const path = require('path');

const pages = ['index.html'];

function validatePage(filePath) {
  const html = fs.readFileSync(filePath, 'utf8');
  const errors = [];

  const headMatch = html.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
  if (!headMatch) {
    errors.push(`${filePath}: missing <head>`);
    return errors;
  }

  const headContent = headMatch[1].trimStart();
  if (!headContent.startsWith('<!-- Google Tag Manager -->')) {
    errors.push(`${filePath}: GTM script must be at the very top of <head>`);
  }

  if (!/googletagmanager\.com\/gtm\.js/.test(html) || !/'GTM-[A-Z0-9]+'/.test(html)) {
    errors.push(`${filePath}: missing GTM head script`);
  }

  const bodyMatch = html.match(/<body[^>]*>([\s\S]*)/i);
  if (!bodyMatch) {
    errors.push(`${filePath}: missing <body>`);
    return errors;
  }

  const bodyStart = bodyMatch[1].trimStart();
  if (!bodyStart.startsWith('<!-- Google Tag Manager (noscript) -->')) {
    errors.push(`${filePath}: GTM noscript must immediately follow <body>`);
  }

  if (!/googletagmanager\.com\/ns\.html\?id=GTM-[A-Z0-9]+/.test(html)) {
    errors.push(`${filePath}: missing GTM noscript iframe`);
  }

  const gtmIds = [...html.matchAll(/GTM-[A-Z0-9]+/g)].map((match) => match[0]);
  if (new Set(gtmIds).size !== 1) {
    errors.push(`${filePath}: GTM container ID must match in head and noscript snippets`);
  }

  return errors;
}

const root = path.resolve(__dirname, '..');
const allErrors = pages.flatMap((page) => validatePage(path.join(root, page)));

if (allErrors.length > 0) {
  console.error('GTM validation failed:\n' + allErrors.map((e) => `  - ${e}`).join('\n'));
  process.exit(1);
}

console.log(`GTM validation passed for ${pages.length} page(s).`);
