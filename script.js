/**
 * Casa Famiglia Quercia – Core interactions
 * Hero video (deferred), contact tracking, reduced motion
 */

document.addEventListener('DOMContentLoaded', function () {
    const heroVideo = document.getElementById('heroVideo');
    const HERO_POSTER = 'images/Pinerolo - Casa Famiglia Quercia 1/img1.avif';

    function trackContactClick(type, label) {
        const eventName = type === 'phone' ? 'phone_click' : 'whatsapp_click';

        if (typeof gtag === 'function') {
            gtag('event', 'conversion', {
                send_to: 'AW-16969391678',
                event_category: 'contact',
                event_label: label || eventName
            });
            gtag('event', eventName, {
                event_category: 'contact',
                event_label: label || 'unknown'
            });
        }

        if (typeof fbq === 'function') {
            fbq('track', 'Contact', { content_name: label || eventName });
        }

        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            event: eventName,
            contact_type: type,
            contact_label: label || 'unknown'
        });
    }

    document.querySelectorAll('.track-phone').forEach(function (el) {
        el.addEventListener('click', function () {
            trackContactClick('phone', el.dataset.trackLabel);
        });
    });

    document.querySelectorAll('.track-whatsapp').forEach(function (el) {
        el.addEventListener('click', function () {
            trackContactClick('whatsapp', el.dataset.trackLabel);
        });
    });

    function getHeroVideoSrc() {
        return window.innerWidth < 768 ? 'videos/hero-mobile.mp4' : 'videos/hero-desktop.mp4';
    }

    function loadHeroVideo() {
        if (!heroVideo) return;

        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) {
            heroVideo.remove();
            return;
        }

        const correctSrc = getHeroVideoSrc();
        const existingSource = heroVideo.querySelector('source');

        if (existingSource && existingSource.getAttribute('src') === correctSrc) {
            return;
        }

        const videoSource = document.createElement('source');
        videoSource.src = correctSrc;
        videoSource.type = 'video/mp4';

        while (heroVideo.firstChild) {
            heroVideo.removeChild(heroVideo.firstChild);
        }
        heroVideo.appendChild(videoSource);

        heroVideo.muted = true;
        heroVideo.loop = true;
        heroVideo.playsInline = true;
        heroVideo.preload = 'none';
        heroVideo.setAttribute('playsinline', '');
        heroVideo.setAttribute('muted', '');
        heroVideo.setAttribute('preload', 'none');
        heroVideo.poster = HERO_POSTER;

        heroVideo.addEventListener('canplay', function onCanPlay() {
            heroVideo.removeEventListener('canplay', onCanPlay);
            heroVideo.classList.add('is-ready');
        }, { once: true });

        heroVideo.play().catch(function () {
            heroVideo.classList.remove('is-ready');
        });
    }

    function scheduleHeroVideoLoad() {
        if ('requestIdleCallback' in window) {
            requestIdleCallback(loadHeroVideo, { timeout: 3000 });
        } else {
            setTimeout(loadHeroVideo, 1500);
        }
    }

    if (document.readyState === 'complete') {
        scheduleHeroVideoLoad();
    } else {
        window.addEventListener('load', scheduleHeroVideoLoad, { once: true });
    }

    let resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(loadHeroVideo, 200);
    });

    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', loadHeroVideo);
});
