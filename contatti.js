/**
 * Contatti — visit, location & contact interactions
 * Tab navigation, anchor sync, copy address
 */

document.addEventListener('DOMContentLoaded', function () {
    const section = document.querySelector('.contact-section');
    if (!section) return;

    const tablist = section.querySelector('.contact-tabs');
    const navLinks = Array.from(section.querySelectorAll('.contact-nav-link'));

    if (tablist) {
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

            if (navLinks[index]) {
                navLinks.forEach(function (link, i) {
                    link.classList.toggle('is-active', i === index);
                });
            }
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

        navLinks.forEach(function (link, index) {
            link.addEventListener('click', function (event) {
                event.preventDefault();
                activateTab(index);
                const main = section.querySelector('.contact-main');
                if (main) {
                    main.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            });
        });
    }

    const copyBtn = section.querySelector('[data-copy-address]');
    if (copyBtn) {
        const address = copyBtn.getAttribute('data-copy-address');
        const defaultLabel = copyBtn.innerHTML;

        copyBtn.addEventListener('click', function () {
            if (!address || !navigator.clipboard) return;

            navigator.clipboard.writeText(address).then(function () {
                copyBtn.classList.add('is-copied');
                copyBtn.innerHTML = '<i class="fas fa-check" aria-hidden="true"></i> Copiato!';
                setTimeout(function () {
                    copyBtn.classList.remove('is-copied');
                    copyBtn.innerHTML = defaultLabel;
                }, 2000);
            });
        });
    }
});
