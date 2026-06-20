/**
 * Una seconda famiglia — interactive story panels
 * Accessible tab navigation with keyboard support
 */

document.addEventListener('DOMContentLoaded', function () {
    const tablist = document.querySelector('.famiglia-tabs');
    if (!tablist) return;

    const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
    const panels = tabs.map(function (tab) {
        return document.getElementById(tab.getAttribute('aria-controls'));
    });

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
});
