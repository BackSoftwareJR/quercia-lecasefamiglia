/**
 * Responsive image helpers — srcset / picture markup for AVIF + WebP + JPEG.
 */
(function (global) {
  'use strict';

  var WIDTHS = [400, 640, 800, 960, 1200, 1280, 1920];
  var HERO_WIDTHS = [640, 960, 1280, 1920];
  var CARD_WIDTHS = [400, 640, 800, 1200];

  function parseAvifPath(url) {
    var match = url.match(/^(.+\/)([^/]+)\.avif$/);
    if (!match) return null;
    return { dir: match[1], stem: match[2] };
  }

  function variantUrl(dir, stem, width, ext) {
    return dir + stem + '-' + width + 'w.' + ext;
  }

  function buildSrcset(dir, stem, widths, ext) {
    return widths.map(function (w) {
      return variantUrl(dir, stem, w, ext) + ' ' + w + 'w';
    }).join(', ');
  }

  function defaultFallbackWidth(widths) {
    return widths.indexOf(1280) !== -1 ? 1280 : widths[widths.length - 1];
  }

  function responsivePicture(options) {
    var avifUrl = options.avifUrl;
    var parsed = parseAvifPath(avifUrl);
    if (!parsed) {
      return '<img src="' + avifUrl + '" alt="' + (options.alt || '') + '">';
    }

    var widths = options.widths || WIDTHS;
    var sizes = options.sizes || '100vw';
    var fallbackW = options.fallbackWidth || defaultFallbackWidth(widths);
    var attrs = [];

    if (options.id) attrs.push('id="' + options.id + '"');
    if (options.className) attrs.push('class="' + options.className + '"');
    attrs.push('src="' + variantUrl(parsed.dir, parsed.stem, fallbackW, 'jpg') + '"');
    attrs.push('srcset="' + buildSrcset(parsed.dir, parsed.stem, widths, 'jpg') + '"');
    attrs.push('sizes="' + sizes + '"');
    attrs.push('alt="' + (options.alt || '').replace(/"/g, '&quot;') + '"');
    if (options.width) attrs.push('width="' + options.width + '"');
    if (options.height) attrs.push('height="' + options.height + '"');
    if (options.loading) attrs.push('loading="' + options.loading + '"');
    if (options.fetchpriority) attrs.push('fetchpriority="' + options.fetchpriority + '"');
    if (options.decoding) attrs.push('decoding="' + options.decoding + '"');

    return (
      '<picture>' +
        '<source type="image/avif" srcset="' + buildSrcset(parsed.dir, parsed.stem, widths, 'avif') + '" sizes="' + sizes + '">' +
        '<source type="image/webp" srcset="' + buildSrcset(parsed.dir, parsed.stem, widths, 'webp') + '" sizes="' + sizes + '">' +
        '<img ' + attrs.join(' ') + '>' +
      '</picture>'
    );
  }

  function responsiveImg(options) {
    var avifUrl = options.avifUrl;
    var parsed = parseAvifPath(avifUrl);
    if (!parsed) {
      var basic = ['src="' + avifUrl + '"', 'alt="' + (options.alt || '').replace(/"/g, '&quot;') + '"'];
      if (options.loading) basic.push('loading="' + options.loading + '"');
      if (options.className) basic.push('class="' + options.className + '"');
      return '<img ' + basic.join(' ') + '>';
    }

    var widths = options.widths || CARD_WIDTHS;
    var sizes = options.sizes || '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 400px';
    var fallbackW = options.fallbackWidth || 800;
    var attrs = ['src="' + variantUrl(parsed.dir, parsed.stem, fallbackW, 'jpg') + '"'];
    attrs.push('srcset="' + buildSrcset(parsed.dir, parsed.stem, widths, 'jpg') + '"');
    attrs.push('sizes="' + sizes + '"');
    attrs.push('alt="' + (options.alt || '').replace(/"/g, '&quot;') + '"');
    if (options.width) attrs.push('width="' + options.width + '"');
    if (options.height) attrs.push('height="' + options.height + '"');
    attrs.push('loading="' + (options.loading || 'lazy') + '"');
    attrs.push('decoding="async"');
    if (options.className) attrs.push('class="' + options.className + '"');

    return '<img ' + attrs.join(' ') + '>';
  }

  function lcpPreloadLink(avifUrl, sizes) {
    var parsed = parseAvifPath(avifUrl);
    if (!parsed) {
      return '<link rel="preload" as="image" href="' + avifUrl + '" fetchpriority="high">';
    }
    var widths = HERO_WIDTHS;
    var srcset = buildSrcset(parsed.dir, parsed.stem, widths, 'avif');
    var fallback = variantUrl(parsed.dir, parsed.stem, 1280, 'avif');
    return (
      '<link rel="preload" as="image" href="' + fallback + '" ' +
      'imagesrcset="' + srcset + '" imagesizes="' + (sizes || '100vw') + '" ' +
      'fetchpriority="high" type="image/avif">'
    );
  }

  global.ResponsiveImages = {
    WIDTHS: WIDTHS,
    HERO_WIDTHS: HERO_WIDTHS,
    CARD_WIDTHS: CARD_WIDTHS,
    parseAvifPath: parseAvifPath,
    variantUrl: variantUrl,
    buildSrcset: buildSrcset,
    responsivePicture: responsivePicture,
    responsiveImg: responsiveImg,
    lcpPreloadLink: lcpPreloadLink
  };
})(typeof window !== 'undefined' ? window : globalThis);
