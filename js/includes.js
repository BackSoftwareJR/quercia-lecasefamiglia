/**
 * Load shared partials (header, footer) into placeholder elements
 */
(function () {
  'use strict';

  function partialUrl(name) {
    var path = window.location.pathname;
    var segments = path.split('/').filter(Boolean);
    if (segments.length && segments[segments.length - 1].includes('.')) {
      segments.pop();
    }
    var depth = segments.length;
    var prefix = depth > 0 ? '../'.repeat(depth) : './';
    return prefix + 'partials/' + name + '.html';
  }

  function injectPartial(selector, name) {
    var el = document.querySelector(selector);
    if (!el) return Promise.resolve();
    return fetch(partialUrl(name))
      .then(function (res) {
        if (!res.ok) throw new Error('Partial not found: ' + name);
        return res.text();
      })
      .then(function (html) {
        el.insertAdjacentHTML('beforebegin', html);
        el.remove();
      })
      .catch(function (err) {
        console.warn('[includes]', err.message);
      });
  }

  document.addEventListener('DOMContentLoaded', function () {
    Promise.all([
      injectPartial('[data-include="header"]', 'header'),
      injectPartial('[data-include="footer"]', 'footer'),
    ]).then(function () {
      document.dispatchEvent(new CustomEvent('partials:loaded'));
    });
  });
})();
