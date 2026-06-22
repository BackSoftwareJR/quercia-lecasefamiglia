/**
 * Navigation: mobile menu, active link, overlay
 */
(function () {
  'use strict';

  function setActiveNav() {
    var path = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';
    var links = document.querySelectorAll('[data-nav]');
    links.forEach(function (link) {
      var navKey = link.getAttribute('data-nav');
      var href = link.getAttribute('href').replace(/\/$/, '') || '/';
      var match = path === href || path.endsWith('/' + navKey);
      if (match) {
        link.setAttribute('aria-current', 'page');
      } else {
        link.removeAttribute('aria-current');
      }
    });
  }

  function initMobileNav() {
    var toggle = document.querySelector('.nav-toggle');
    var mobileNav = document.getElementById('mobile-nav');
    var overlay = document.getElementById('nav-overlay');
    if (!toggle || !mobileNav) return;

    mobileNav.hidden = false;
    if (overlay) overlay.hidden = false;

    function openNav() {
      toggle.setAttribute('aria-expanded', 'true');
      mobileNav.classList.add('is-open');
      if (overlay) overlay.classList.add('is-visible');
      document.body.style.overflow = 'hidden';
    }

    function closeNav() {
      toggle.setAttribute('aria-expanded', 'false');
      mobileNav.classList.remove('is-open');
      if (overlay) overlay.classList.remove('is-visible');
      document.body.style.overflow = '';
    }

    toggle.addEventListener('click', function () {
      var expanded = toggle.getAttribute('aria-expanded') === 'true';
      if (expanded) closeNav();
      else openNav();
    });

    if (overlay) {
      overlay.addEventListener('click', closeNav);
    }

    mobileNav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', closeNav);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeNav();
    });
  }

  document.addEventListener('partials:loaded', function () {
    setActiveNav();
    initMobileNav();
  });
})();
