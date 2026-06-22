/**
 * Animations via Intersection Observer
 */
(function () {
  'use strict';

  function initCounterUp(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var suffix = el.getAttribute('data-suffix') || '';
    var prefix = el.getAttribute('data-prefix') || '';
    if (isNaN(target)) return;

    var duration = 1500;
    var start = 0;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var current = Math.floor(progress * (target - start) + start);
      el.textContent = prefix + current + suffix;
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = prefix + target + suffix;
    }

    requestAnimationFrame(step);
  }

  function initAnimations() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.querySelectorAll('.animate-on-scroll, .stagger-children, .stagger-150').forEach(function (el) {
        el.classList.add('is-visible');
      });
      document.querySelectorAll('[data-count]').forEach(function (el) {
        var target = el.getAttribute('data-count');
        var suffix = el.getAttribute('data-suffix') || '';
        var prefix = el.getAttribute('data-prefix') || '';
        el.textContent = prefix + target + suffix;
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          el.classList.add('is-visible');

          if (el.classList.contains('trust-bar')) {
            el.querySelectorAll('[data-count]').forEach(initCounterUp);
          }

          observer.unobserve(el);
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );

    document.querySelectorAll('.animate-on-scroll, .stagger-children, .stagger-150, .trust-bar').forEach(function (el) {
      observer.observe(el);
    });
  }

  document.addEventListener('DOMContentLoaded', initAnimations);
  document.addEventListener('partials:loaded', initAnimations);
})();
