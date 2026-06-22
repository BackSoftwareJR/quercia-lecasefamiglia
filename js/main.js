/**
 * Main: header scroll, hamburger, smooth scroll, hero video, accordion
 */
(function () {
  'use strict';

  function setYear() {
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  function initHeaderScroll() {
    var header = document.querySelector('.site-header');
    if (!header) return;
    function onScroll() {
      header.classList.toggle('is-scrolled', window.scrollY > 40);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        var id = link.getAttribute('href');
        if (id.length < 2) return;
        var target = document.querySelector(id);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  function initAccordions() {
    document.querySelectorAll('.faq-accordion, .accordion').forEach(function (accordion) {
      var triggers = accordion.querySelectorAll('.faq-question, .accordion__trigger');
      triggers.forEach(function (trigger) {
        trigger.addEventListener('click', function () {
          var expanded = trigger.getAttribute('aria-expanded') === 'true';
          var panel = document.getElementById(trigger.getAttribute('aria-controls'));
          if (!panel) return;

          triggers.forEach(function (t) {
            if (t !== trigger) {
              t.setAttribute('aria-expanded', 'false');
              t.classList.remove('is-open');
              var p = document.getElementById(t.getAttribute('aria-controls'));
              if (p) p.hidden = true;
            }
          });

          trigger.setAttribute('aria-expanded', expanded ? 'false' : 'true');
          trigger.classList.toggle('is-open', !expanded);
          panel.hidden = expanded;
        });
      });
    });
  }

  function initHeroVideo() {
    var video = document.getElementById('heroVideo');
    var fallback = document.getElementById('heroFallback');
    if (!video) return;

    video.style.display = 'none';
    if (fallback) {
      fallback.src = '/images/map-placeholder.jpg';
      fallback.alt = 'Spazi comuni luminosi di Casa Famiglia Quercia a Pinerolo';
      fallback.hidden = false;
    }
  }

  function initAll() {
    setYear();
    initHeaderScroll();
    initSmoothScroll();
    initAccordions();
    initHeroVideo();
  }

  document.addEventListener('partials:loaded', initAll);
  document.addEventListener('DOMContentLoaded', function () {
    if (!document.querySelector('[data-include="header"]')) initAll();
  });
})();
