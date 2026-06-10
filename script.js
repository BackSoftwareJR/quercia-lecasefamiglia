/**
 * Casa Famiglia Quercia – Core interactions
 * Hero video, contact tracking, reduced motion
 */

document.addEventListener('DOMContentLoaded', function () {
    const heroVideo = document.getElementById('heroVideo');

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

    function loadAppropriateVideo() {
        if (!heroVideo) return;

        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) {
            heroVideo.style.display = 'none';
            return;
        }

        const isMobile = window.innerWidth < 768;
        const correctSrc = isMobile ? 'videos/hero-mobile.mp4' : 'videos/hero-desktop.mp4';
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
        heroVideo.setAttribute('playsinline', '');
        heroVideo.setAttribute('muted', '');
        heroVideo.poster = 'images/Pinerolo - Casa Famiglia Quercia 1/img1.avif';

        heroVideo.play().catch(function () {
            heroVideo.style.display = 'none';
            const container = document.querySelector('.hero-video-container');
            if (container) {
                container.style.backgroundImage = 'url("images/Pinerolo - Casa Famiglia Quercia 1/img1.avif")';
                container.style.backgroundSize = 'cover';
                container.style.backgroundPosition = 'center';
            }
        });
    }

    loadAppropriateVideo();

    let resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(loadAppropriateVideo, 200);
    });

    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', loadAppropriateVideo);
});
