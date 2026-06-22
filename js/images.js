/**
 * Image path registry — Casa Famiglia Quercia (Pinerolo)
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

  global.CFQ_IMAGES = {
    PINEROLO_DIR: encodeURI(PINEROLO_DIR),
    DINING_ROOM: encodeURI(DINING_ROOM),
    OG_IMAGE: SITE + encodeURI(DINING_ROOM),
    pineroImg: pineroImg
  };
})(typeof window !== 'undefined' ? window : this);
