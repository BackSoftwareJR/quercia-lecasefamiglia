/**
 * Cosa è incluso — immersive service navigator
 * Accessible tab navigation with visual crossfade
 */

document.addEventListener('DOMContentLoaded', function () {
    const section = document.querySelector('.services-immersive');
    if (!section) return;

    const tablist = section.querySelector('.services-list');
    const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
    const panels = tabs.map(function (tab) {
        return document.getElementById(tab.getAttribute('aria-controls'));
    });
    const stageImages = Array.from(section.querySelectorAll('.services-stage-image'));
    const progressBar = section.querySelector('.services-flow-progress');
    const caption = document.getElementById('services-stage-caption');
    const total = tabs.length;

    function updateProgress(index) {
        if (!progressBar || total <= 1) return;
        const percent = ((index + 1) / total) * 100;
        progressBar.style.height = percent + '%';
    }

    function activateTab(index) {
        tabs.forEach(function (tab, i) {
            const isActive = i === index;
            tab.classList.toggle('is-active', isActive);
            tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
            tab.setAttribute('tabindex', isActive ? '0' : '-1');
        });

        panels.forEach(function (panel, i) {
            if (!panel) return;
            const isActive = i === index;
            panel.classList.toggle('is-active', isActive);
            if (isActive) {
                panel.removeAttribute('hidden');
            } else {
                panel.setAttribute('hidden', '');
            }
        });

        stageImages.forEach(function (figure, i) {
            figure.classList.toggle('is-active', i === index);
        });

        if (caption && tabs[index]) {
            caption.textContent = tabs[index].dataset.caption || '';
        }

        updateProgress(index);
    }

    tabs.forEach(function (tab, index) {
        tab.addEventListener('click', function () {
            activateTab(index);
        });

        tab.addEventListener('keydown', function (event) {
            let targetIndex = index;

            if (event.key === 'ArrowDown' || event.key === 'ArrowRight') {
                event.preventDefault();
                targetIndex = (index + 1) % tabs.length;
            } else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') {
                event.preventDefault();
                targetIndex = (index - 1 + tabs.length) % tabs.length;
            } else if (event.key === 'Home') {
                event.preventDefault();
                targetIndex = 0;
            } else if (event.key === 'End') {
                event.preventDefault();
                targetIndex = tabs.length - 1;
            } else {
                return;
            }

            activateTab(targetIndex);
            tabs[targetIndex].focus();
        });
    });

    updateProgress(0);
});
