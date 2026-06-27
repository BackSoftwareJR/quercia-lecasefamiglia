/**
 * Image path registry — Casa Famiglia Castelletto (Pinerolo)
 *
 * Pattern: root-absolute paths + encodeURI for spaces/special chars.
 * Real assets live in:
 *   /images/Pinerolo - Casa Famiglia Quercia 1/img1.avif … img12.avif
 *   /images/Sala da Pranzo + persone 1.avif
 *
 * Do NOT use map-placeholder.jpg or avatars/*.jpg — they are 1-byte stubs.
 * In HTML: src="/images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/imgN.avif"
 */
(function (global) {
  'use strict';

  var SITE = 'https://casafamigliaquercia.it';
  var PINEROLO_DIR = '/images/Pinerolo - Casa Famiglia Quercia 1/';
  var DINING_ROOM = '/images/Sala da Pranzo + persone 1.avif';

  function pineroImg(n) {
    return encodeURI(PINEROLO_DIR + 'img' + n + '.avif');
  }

  /**
   * CDN image optimization — Cloudflare Image Resizing.
   * Enable at zone level (Polish Lossy + Auto AVIF/WebP) then set CDN_ENABLED = true.
   * URL pattern: /cdn-cgi/image/width=W,quality=Q,format=FM/source-path
   * Imgix-style fallback: path?w=800&q=80&fm=avif
   */
  var CDN_ENABLED = false;
  var CDN_PROVIDER = 'cloudflare';

  function cdnUrl(path, options) {
    if (!CDN_ENABLED || !path || path.indexOf('/images/') !== 0) {
      return path;
    }
    var opts = options || {};
    var w = opts.width || 800;
    var q = opts.quality || 80;
    var fm = opts.format || 'avif';

    if (CDN_PROVIDER === 'cloudflare') {
      return '/cdn-cgi/image/width=' + w + ',quality=' + q + ',format=' + fm + path;
    }
    var sep = path.indexOf('?') === -1 ? '?' : '&';
    return path + sep + 'w=' + w + '&q=' + q + '&fm=' + fm;
  }

  global.CFQ_IMAGES = {
    PINEROLO_DIR: encodeURI(PINEROLO_DIR),
    DINING_ROOM: encodeURI(DINING_ROOM),
    OG_IMAGE: SITE + encodeURI(DINING_ROOM),
    CDN_ENABLED: CDN_ENABLED,
    pineroImg: pineroImg,
    cdnUrl: cdnUrl
  };
})(typeof window !== 'undefined' ? window : this);
