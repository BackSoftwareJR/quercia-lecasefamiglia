(function () {
  'use strict';

  var SELECTORS = '.animate-on-scroll,.stagger-children,.stagger-150,.trust-bar';
  var booted = false;

  function initCounterUp(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var suffix = el.getAttribute('data-suffix') || '';
    var prefix = el.getAttribute('data-prefix') || '';
    if (isNaN(target)) return;

    var duration = 1500;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var current = Math.floor(progress * target);
      el.textContent = prefix + current + suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = prefix + target + suffix;
      }
    }

    requestAnimationFrame(step);
  }

  function revealElement(el) {
    if (el.classList.contains('is-visible')) return;
    el.classList.add('is-visible');
    if (el.classList.contains('trust-bar')) {
      el.querySelectorAll('[data-count]').forEach(initCounterUp);
    }
  }

  function revealAll() {
    document.querySelectorAll(SELECTORS).forEach(revealElement);
  }

  function revealInViewport() {
    var viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    document.querySelectorAll(SELECTORS + ':not(.is-visible)').forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.top < viewportHeight && rect.bottom > 0) {
        revealElement(el);
      }
    });
  }

  function observerOptions(el) {
    if (el.classList.contains('stagger-children') || el.classList.contains('stagger-150')) {
      return { threshold: 0, rootMargin: '0px 0px -40px 0px' };
    }
    return { threshold: 0.05, rootMargin: '0px 0px -40px 0px' };
  }

  function initAnimations() {
    try {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        revealAll();
        document.querySelectorAll('[data-count]').forEach(function (el) {
          var target = el.getAttribute('data-count');
          var suffix = el.getAttribute('data-suffix') || '';
          var prefix = el.getAttribute('data-prefix') || '';
          el.textContent = prefix + target + suffix;
        });
        return;
      }

      revealInViewport();

      if (!('IntersectionObserver' in window)) {
        revealAll();
        return;
      }

      document.querySelectorAll(SELECTORS).forEach(function (el) {
        if (el.classList.contains('is-visible')) return;

        var observer = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            revealElement(entry.target);
            observer.unobserve(entry.target);
          });
        }, observerOptions(el));

        observer.observe(el);
      });

      requestAnimationFrame(revealInViewport);
      document.documentElement.classList.add('js-animations');

      window.setTimeout(revealAll, 500);
    } catch (err) {
      revealAll();
      document.documentElement.classList.remove('js-animations');
    }
  }

  function boot() {
    if (booted) return;
    booted = true;
    initAnimations();
  }

  document.addEventListener('DOMContentLoaded', boot);
  document.addEventListener('partials:loaded', boot);
})();
