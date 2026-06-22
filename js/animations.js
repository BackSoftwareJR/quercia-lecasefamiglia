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

    function revealElement(el) {
      if (el.classList.contains('is-visible')) return;
      el.classList.add('is-visible');

      if (el.classList.contains('trust-bar')) {
        el.querySelectorAll('[data-count]').forEach(initCounterUp);
      }
    }

    function observerOptions(el) {
      // Tall stagger containers (e.g. servizi detail blocks) rarely hit 15% visibility
      if (el.classList.contains('stagger-children') || el.classList.contains('stagger-150')) {
        return { threshold: 0, rootMargin: '0px 0px -40px 0px' };
      }
      return { threshold: 0.15, rootMargin: '0px 0px -40px 0px' };
    }

    document.querySelectorAll('.animate-on-scroll, .stagger-children, .stagger-150, .trust-bar').forEach(function (el) {
      if (el.classList.contains('is-visible')) return;

      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            revealElement(entry.target);
            observer.unobserve(entry.target);
          });
        },
        observerOptions(el)
      );

      observer.observe(el);
    });

    window.setTimeout(function () {
      document.querySelectorAll('.animate-on-scroll:not(.is-visible), .stagger-children:not(.is-visible), .stagger-150:not(.is-visible)').forEach(revealElement);
    }, 2000);
  }

  document.addEventListener('DOMContentLoaded', initAnimations);
  document.addEventListener('partials:loaded', initAnimations);
})();
