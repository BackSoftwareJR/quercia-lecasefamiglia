/**
 * Footer gallery carousel — auto-advance preview with manual controls
 */

document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('.footer-carousel');
    if (!carousel) return;

    const track = carousel.querySelector('.footer-carousel-track');
    const slides = Array.from(carousel.querySelectorAll('.footer-carousel-slide'));
    const prevButton = carousel.querySelector('.footer-carousel-prev');
    const nextButton = carousel.querySelector('.footer-carousel-next');
    const dotsContainer = carousel.querySelector('.footer-carousel-dots');

    if (!track || slides.length === 0) return;

    let currentIndex = 0;
    let slideInterval;
    const slideDelay = 4500;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    slides.forEach(function (_, index) {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'footer-carousel-dot' + (index === 0 ? ' is-active' : '');
        dot.setAttribute('role', 'tab');
        dot.setAttribute('aria-label', 'Vai alla foto ' + (index + 1));
        dot.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
        dot.addEventListener('click', function () {
            showSlide(index);
            restartSlideshow();
        });
        dotsContainer.appendChild(dot);
    });

    const dots = Array.from(dotsContainer.querySelectorAll('.footer-carousel-dot'));

    function showSlide(index) {
        slides.forEach(function (slide, i) {
            slide.classList.toggle('is-active', i === index);
        });

        dots.forEach(function (dot, i) {
            const isActive = i === index;
            dot.classList.toggle('is-active', isActive);
            dot.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });

        track.style.transform = 'translateX(-' + (index * 100) + '%)';
        currentIndex = index;
    }

    function nextSlide() {
        showSlide((currentIndex + 1) % slides.length);
    }

    function prevSlide() {
        showSlide((currentIndex - 1 + slides.length) % slides.length);
    }

    function startSlideshow() {
        if (prefersReducedMotion || slides.length <= 1) return;
        clearInterval(slideInterval);
        slideInterval = setInterval(nextSlide, slideDelay);
    }

    function stopSlideshow() {
        clearInterval(slideInterval);
    }

    function restartSlideshow() {
        stopSlideshow();
        startSlideshow();
    }

    if (prevButton) {
        prevButton.addEventListener('click', function () {
            prevSlide();
            restartSlideshow();
        });
    }

    if (nextButton) {
        nextButton.addEventListener('click', function () {
            nextSlide();
            restartSlideshow();
        });
    }

    carousel.addEventListener('mouseenter', stopSlideshow);
    carousel.addEventListener('mouseleave', startSlideshow);
    carousel.addEventListener('focusin', stopSlideshow);
    carousel.addEventListener('focusout', function (event) {
        if (!carousel.contains(event.relatedTarget)) {
            startSlideshow();
        }
    });

    carousel.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowLeft') {
            event.preventDefault();
            prevSlide();
            restartSlideshow();
        } else if (event.key === 'ArrowRight') {
            event.preventDefault();
            nextSlide();
            restartSlideshow();
        }
    });

    let touchStartX = 0;

    carousel.addEventListener('touchstart', function (event) {
        touchStartX = event.changedTouches[0].screenX;
        stopSlideshow();
    }, { passive: true });

    carousel.addEventListener('touchend', function (event) {
        const deltaX = event.changedTouches[0].screenX - touchStartX;
        if (Math.abs(deltaX) > 40) {
            if (deltaX < 0) {
                nextSlide();
            } else {
                prevSlide();
            }
        }
        restartSlideshow();
    }, { passive: true });

    showSlide(0);
    startSlideshow();
});
