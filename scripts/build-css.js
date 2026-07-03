#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const postcss = require('postcss');
const cssnano = require('cssnano');

const ROOT = path.resolve(__dirname, '..');
const postcssConfig = require('../postcss.config.js');

const ROOT_CSS_FILES = ['blog.css', 'galleria.css', 'faq.css'];

async function processCss(filePath, plugins) {
  const input = fs.readFileSync(filePath, 'utf8');
  const result = await postcss(plugins).process(input, { from: filePath, to: filePath });
  if (result.css !== input) {
    fs.writeFileSync(filePath, result.css);
  }
  const relative = path.relative(ROOT, filePath);
  console.log(`  ${relative}: ${input.length} → ${result.css.length} bytes`);
}

async function main() {
  const allPlugins = postcssConfig.plugins || [];
  const minifyOnly = [cssnano({ preset: 'default' })];

  console.log('Processing css/…');
  for (const name of fs.readdirSync(path.join(ROOT, 'css')).sort()) {
    if (!name.endsWith('.css')) continue;
    const filePath = path.join(ROOT, 'css', name);
    const skipPurge = name === 'critical.css' || name === 'design-system.css';
    const plugins = skipPurge ? minifyOnly : allPlugins;
    await processCss(filePath, plugins);
  }

  console.log('Processing root CSS…');
  for (const name of ROOT_CSS_FILES) {
    const filePath = path.join(ROOT, name);
    if (fs.existsSync(filePath)) {
      await processCss(filePath, allPlugins);
    }
  }

  console.log('CSS build complete.');
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
