/**
 * Gallery masonry + tab filter + lightbox
 */
(function () {
  'use strict';

  var GALLERY_ITEMS = [
    { file: 'images/map-placeholder.jpg', alt: 'Salone luminoso di Casa Famiglia Quercia a Pinerolo', category: 'spazi-comuni' },
    { file: 'images/avatars/avatar3.jpg', alt: 'Attività ricreative nel salone comune a Pinerolo', category: 'spazi-comuni' },
    { file: 'images/avatars/avatar1.jpg', alt: 'Pranzo conviviale in sala da pranzo — Casa Quercia', category: 'cucina' },
    { file: 'images/avatars/avatar2.jpg', alt: 'Cucina di casa con pasti freschi ogni giorno a Pinerolo', category: 'cucina' },
    { file: 'images/avatars/avatar1.jpg', alt: 'Camera confortevole con arredi personali — Pinerolo', category: 'camere' },
    { file: 'images/avatars/avatar2.jpg', alt: 'Camera luminosa e accogliente nel Pinerolese', category: 'camere' },
    { file: 'images/map-placeholder.jpg', alt: 'Giardino privato nel verde del Pinerolese', category: 'giardino' },
    { file: 'images/avatars/avatar3.jpg', alt: 'Spazi verdi per passeggiate a Casa Famiglia Quercia', category: 'giardino' }
  ];

  function getSiteBase() {
    var path = window.location.pathname;
    var segments = path.split('/').filter(Boolean);
    if (segments.length && segments[segments.length - 1].includes('.')) {
      segments.pop();
    }
    return segments.length > 0 ? '../'.repeat(segments.length) : '';
  }

  function initGallery() {
    var root = document.getElementById('home-gallery');
    if (!root) return;

    var IMG_BASE = getSiteBase();

    var grid = root.querySelector('.gallery-grid');
    var tabs = root.querySelectorAll('.gallery-tabs__btn');
    var lightbox = document.getElementById('gallery-lightbox');
    var currentFilter = 'tutti';
    var visibleItems = [];
    var currentIndex = 0;

    function renderItems(filter) {
      var filtered = filter === 'tutti'
        ? GALLERY_ITEMS
        : GALLERY_ITEMS.filter(function (item) { return item.category === filter; });

      grid.classList.add('is-fading');
      setTimeout(function () {
        grid.innerHTML = '';
        filtered.forEach(function (item, idx) {
          var btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'gallery-item scale-in animate-on-scroll';
          btn.setAttribute('data-index', String(idx));
          btn.innerHTML = '<img src="' + IMG_BASE + item.file + '" alt="' + item.alt + '" loading="lazy" width="400" height="300">';
          btn.addEventListener('click', function () { openLightbox(filtered, idx); });
          grid.appendChild(btn);
        });
        visibleItems = filtered;
        grid.classList.remove('is-fading');

        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          grid.querySelectorAll('.animate-on-scroll').forEach(function (el) {
            el.classList.add('is-visible');
          });
        } else {
          var obs = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
              if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                obs.unobserve(entry.target);
              }
            });
          }, { threshold: 0.1 });
          grid.querySelectorAll('.animate-on-scroll').forEach(function (el) { obs.observe(el); });
        }
      }, 200);
    }

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var filter = tab.getAttribute('data-filter');
        if (filter === currentFilter) return;
        currentFilter = filter;
        tabs.forEach(function (t) {
          t.classList.toggle('is-active', t === tab);
          t.setAttribute('aria-selected', t === tab ? 'true' : 'false');
        });
        renderItems(filter);
      });
    });

    function openLightbox(items, idx) {
      if (!lightbox) return;
      visibleItems = items;
      currentIndex = idx;
      showSlide();
      lightbox.classList.add('is-open');
      lightbox.hidden = false;
      document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      lightbox.classList.remove('is-open');
      document.body.style.overflow = '';
      setTimeout(function () { lightbox.hidden = true; }, 300);
    }

    function showSlide() {
      var img = lightbox.querySelector('.lightbox__image');
      var item = visibleItems[currentIndex];
      img.src = IMG_BASE + item.file;
      img.alt = item.alt;
    }

    if (lightbox) {
      lightbox.querySelector('.lightbox__close').addEventListener('click', closeLightbox);
      lightbox.querySelector('.lightbox__nav--prev').addEventListener('click', function () {
        currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
        showSlide();
      });
      lightbox.querySelector('.lightbox__nav--next').addEventListener('click', function () {
        currentIndex = (currentIndex + 1) % visibleItems.length;
        showSlide();
      });
      lightbox.addEventListener('click', function (e) {
        if (e.target === lightbox) closeLightbox();
      });

      var touchStartX = 0;
      lightbox.addEventListener('touchstart', function (e) {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });
      lightbox.addEventListener('touchend', function (e) {
        var diff = e.changedTouches[0].screenX - touchStartX;
        if (Math.abs(diff) < 50) return;
        if (diff > 0) {
          currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
        } else {
          currentIndex = (currentIndex + 1) % visibleItems.length;
        }
        showSlide();
      }, { passive: true });

      document.addEventListener('keydown', function (e) {
        if (!lightbox.classList.contains('is-open')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') {
          currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
          showSlide();
        }
        if (e.key === 'ArrowRight') {
          currentIndex = (currentIndex + 1) % visibleItems.length;
          showSlide();
        }
      });
    }

    renderItems('tutti');
  }

  document.addEventListener('DOMContentLoaded', initGallery);
})();
