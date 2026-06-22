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

  function getSiteBase() {
    var path = window.location.pathname;
    var segments = path.split('/').filter(Boolean);
    if (segments.length && segments[segments.length - 1].includes('.')) {
      segments.pop();
    }
    return segments.length > 0 ? '../'.repeat(segments.length) : '';
  }

  function initHeroVideo() {
    var video = document.getElementById('heroVideo');
    var fallback = document.getElementById('heroFallback');
    var mediaWrap = video && video.closest('.hero-clean__media');
    if (!video) return;

    var heroImage = '/images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/img1.avif';
    var isMobile = window.matchMedia('(max-width: 767px)').matches;
    var videoSrc = '/videos/' + (isMobile ? 'hero-mobile.mp4' : 'hero-desktop.mp4');
    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function showImageFallback() {
      video.style.display = 'none';
      video.pause();
      if (fallback) {
        fallback.src = heroImage;
        fallback.alt = 'Casa Famiglia Quercia a Pinerolo — ambiente familiare nel Pinerolese';
        fallback.hidden = false;
        fallback.removeAttribute('hidden');
        fallback.style.display = 'block';
      }
      if (mediaWrap) mediaWrap.classList.add('is-image-fallback');
    }

    function showVideo() {
      if (fallback) {
        fallback.hidden = true;
        fallback.style.display = 'none';
      }
      video.style.display = 'block';
      if (mediaWrap) mediaWrap.classList.remove('is-image-fallback');
    }

    if (fallback) {
      fallback.src = heroImage;
      fallback.alt = 'Casa Famiglia Quercia a Pinerolo — ambiente familiare nel Pinerolese';
    }
    video.poster = heroImage;

    if (prefersReducedMotion) {
      showImageFallback();
      return;
    }

    showImageFallback();

    var source = document.createElement('source');
    source.src = videoSrc;
    source.type = 'video/mp4';
    video.appendChild(source);
    video.muted = true;
    video.playsInline = true;
    video.load();

    video.addEventListener('error', showImageFallback, { once: true });
    video.addEventListener('canplay', function () {
      var playPromise = video.play();
      if (playPromise && playPromise.then) {
        playPromise.then(showVideo).catch(showImageFallback);
      } else {
        showVideo();
      }
    }, { once: true });

    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        var nowMobile = window.matchMedia('(max-width: 767px)').matches;
        if (nowMobile === isMobile) return;
        isMobile = nowMobile;
        while (video.firstChild) video.removeChild(video.firstChild);
        source = document.createElement('source');
        source.src = base + 'videos/' + (isMobile ? 'hero-mobile.mp4' : 'hero-desktop.mp4');
        source.type = 'video/mp4';
        video.appendChild(source);
        video.load();
      }, 250);
    }, { passive: true });
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
