/**
 * Casa Famiglia Castelletto - Hero Section JavaScript
 * Funzionalità:
 * 1. Caricamento video in base al dispositivo (desktop/mobile)
 * 2. CTA button sticky su mobile
 * 3. Gestione preferenze reduced motion
 */

document.addEventListener('DOMContentLoaded', function() {
    // Debug mode
    const DEBUG = false;
    function log(message) {
        if (DEBUG) console.log(message);
    }
    
    log('DOM caricato');
    // Riferimenti elementi DOM
    const heroVideo = document.getElementById('heroVideo');
    const ctaButton = document.querySelector('.cta-buttons');
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const lightboxClose = document.querySelector('.lightbox-close');
    const lightboxPrev = document.getElementById('lightbox-prev');
    const lightboxNext = document.getElementById('lightbox-next');
    
    // Aggiungiamo il CTA mobile per la sezione servizi
    const servicesSection = document.querySelector('.services-section');
    if (servicesSection) {
        // Crea il container per il CTA mobile
        const mobileCta = document.createElement('div');
        mobileCta.className = 'mobile-cta';
        
        // Crea il bottone di chiamata
        const callButton = document.createElement('a');
        callButton.href = 'tel:+393762031211';
        callButton.className = 'btn btn-call';
        callButton.textContent = 'Parliamone Insieme';
        
        // Aggiungi il bottone al container
        mobileCta.appendChild(callButton);
        
        // Aggiungi il tutto al body
        document.body.appendChild(mobileCta);
    }
    
    // 1. Rilevamento dispositivo e caricamento video appropriato
    function loadAppropriateVideo() {
        // Controllo se il browser supporta la media query prefers-reduced-motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        // Se l'utente preferisce reduced motion, non carichiamo il video
        if (prefersReducedMotion) {
            // Il CSS si occuperà di mostrare l'immagine fallback
            heroVideo.style.display = 'none';
            return;
        }
        
        // Determina se il dispositivo è mobile (< 768px) o desktop
        const isMobile = window.innerWidth < 768;
        const isAndroid = /Android/i.test(navigator.userAgent);
        
        log('Dispositivo: ' + (isMobile ? 'Mobile' : 'Desktop') + (isAndroid ? ' (Android)' : ''));
        
        // Controlla se il video è già stato configurato correttamente
        const existingSource = heroVideo.querySelector('source');
        const correctSrc = isMobile ? 'videos/hero-mobile.mp4' : 'videos/hero-desktop.mp4';
        
        // Se il source esiste già ed è quello giusto, non facciamo nulla
        if (existingSource && existingSource.src.endsWith(correctSrc)) {
            return; // Evita il ricaricamento del video se è già configurato
        }
        
        const videoSource = document.createElement('source');
        
        // Imposta il percorso del video in base al dispositivo
        videoSource.src = correctSrc;
        videoSource.type = 'video/mp4';
        
        // Svuota eventuali source esistenti e aggiungi quella appropriata
        while (heroVideo.firstChild) {
            heroVideo.removeChild(heroVideo.firstChild);
        }
        
        heroVideo.appendChild(videoSource);
        
        // Configurazione ottimizzata per tutte le piattaforme incluso Android
        heroVideo.autoplay = true;
        heroVideo.muted = true;
        heroVideo.loop = true;
        heroVideo.playsInline = true;
        heroVideo.controls = false; // Nascondi esplicitamente i controlli
        heroVideo.defaultMuted = true; // Assicura che sia inizialmente in muto
        heroVideo.preload = 'auto'; // Precarica il video
        
        // Attributi aggiuntivi per ottimizzare la compatibilità
        heroVideo.setAttribute('playsinline', ''); // iOS
        heroVideo.setAttribute('muted', ''); // Doppia sicurezza per il muto
        heroVideo.setAttribute('disablePictureInPicture', ''); // Disabilita PIP su Android
        heroVideo.setAttribute('controlslist', 'nodownload nofullscreen noremoteplayback'); // Disabilita controlli extra
        
        // Imposta il poster per evitare flash di schermo grigio
        heroVideo.poster = 'images/Coazze - Casa Famiglia Castelletto/Spazi Comuni.avif';
        
        // Forza l'autoplay subito e dopo un breve delay (può aiutare su Android)
        heroVideo.play()
            .then(() => {
                log('Video avviato con successo');
            })
            .catch(err => {
                log('Primo tentativo di auto-play fallito: ' + err);
                
                // Secondo tentativo dopo un breve ritardo
                setTimeout(() => {
                    heroVideo.play()
                        .then(() => log('Video avviato al secondo tentativo'))
                        .catch(err => {
                            log('Auto-play fallito definitivamente: ' + err);
                            // Mostra l'immagine fallback se l'autoplay fallisce
                            heroVideo.style.display = 'none';
                            const heroContainer = document.querySelector('.hero-video-container');
                            heroContainer.style.backgroundImage = 'url("images/Coazze - Casa Famiglia Castelletto/Spazi Comuni.avif")';
                            heroContainer.style.backgroundSize = 'cover';
                            heroContainer.style.backgroundPosition = 'center';
                        });
                }, 300);
            });
            
        // Se è Android, impostiamo un event listener per il touchstart
        // che è spesso necessario per avviare i media su Android
        if (isAndroid) {
            const heroSection = document.querySelector('.hero-section');
            heroSection.addEventListener('touchstart', function() {
                heroVideo.play().catch(e => log('Errore dopo touchstart: ' + e));
            }, { once: true }); // Una volta sola per evitare multiple attivazioni
        }
    }
    
    // 2. Gestione CTA sticky su mobile
    function handleStickyButton() {
        if (!ctaButton) {
            return;
        }
        
        if (window.innerWidth < 768) {
            // Aggiungi classe sticky su mobile
            ctaButton.classList.add('cta-sticky');
        } else {
            // Rimuovi classe sticky su desktop
            ctaButton.classList.remove('cta-sticky');
        }
    }
    
    // Esegui funzioni all'avvio
    loadAppropriateVideo();
    handleStickyButton();
    
    // Gestione resize della finestra
    window.addEventListener('resize', function() {
        loadAppropriateVideo(); // Ricarica il video appropriato
        handleStickyButton();   // Aggiorna stato del bottone
    });
    
    // Gestione cambio preferenze reduced motion 
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', loadAppropriateVideo);
    
    // La gestione FAQ è stata spostata in faq.js

    // 5. Gestione Carosello Sezione About
    function initCarousel() {
        const aboutCarousel = document.querySelector('.about-carousel');
        
        if (aboutCarousel) {
            const slides = aboutCarousel.querySelectorAll('.carousel-slide');
            const indicators = aboutCarousel.querySelectorAll('.indicator');
            
            let currentSlide = 0;
            let carouselInterval;

            function showSlide(index) {
                // Rimuovi classe active da tutte le slide e indicatori
                slides.forEach(slide => slide.classList.remove('active'));
                indicators.forEach(indicator => indicator.classList.remove('active'));
                
                // Aggiungi classe active alla slide e indicatore corrente
                if (slides[index] && indicators[index]) {
                    slides[index].classList.add('active');
                    indicators[index].classList.add('active');
                }
                
                currentSlide = index;
            }

            function nextSlide() {
                const nextIndex = (currentSlide + 1) % slides.length;
                showSlide(nextIndex);
            }

            function startCarousel() {
                if (carouselInterval) {
                    clearInterval(carouselInterval);
                }
                carouselInterval = setInterval(nextSlide, 3000); // Cambia slide ogni 3 secondi
            }

            function stopCarousel() {
                if (carouselInterval) {
                    clearInterval(carouselInterval);
                    carouselInterval = null;
                }
            }

            // Event listeners per gli indicatori
            indicators.forEach((indicator, index) => {
                indicator.addEventListener('click', () => {
                    showSlide(index);
                    stopCarousel();
                    setTimeout(startCarousel, 1000); // Riavvia dopo 1 secondo
                });
            });

            // Pausa il carosello quando l'utente interagisce
            aboutCarousel.addEventListener('mouseenter', stopCarousel);
            aboutCarousel.addEventListener('mouseleave', startCarousel);

            // Inizializza la prima slide
            showSlide(0);
            
            // Avvia il carosello dopo un breve delay
            setTimeout(startCarousel, 1000);
        } else {
            setTimeout(initCarousel, 500);
        }
    }
    
    // Inizializza il carosello
    initCarousel();

    // 6. Gestione Carosello Servizi con Frecce
    function initServicesCarousel() {
        const servicesCarousel = document.querySelector('.services-carousel');
        const serviceCards = document.querySelectorAll('.service-card-carousel');
        const progressDots = document.querySelectorAll('.progress-dot');
        const prevButton = document.querySelector('.carousel-prev');
        const nextButton = document.querySelector('.carousel-next');
        
        if (!servicesCarousel || serviceCards.length === 0) {
            return;
        }
        
        let currentIndex = 0;
        let isAnimating = false;
        let autoPlayInterval;
        
        // Funzione per aggiornare le classi delle card
        function updateCards() {
            serviceCards.forEach((card, index) => {
                card.classList.remove('active', 'next', 'prev');
                
                if (index === currentIndex) {
                    card.classList.add('active');
                } else if (index === (currentIndex + 1) % serviceCards.length) {
                    card.classList.add('next');
                } else if (index === (currentIndex - 1 + serviceCards.length) % serviceCards.length) {
                    card.classList.add('prev');
                }
            });
            
            // Aggiorna gli indicatori
            progressDots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentIndex);
            });
        }
        
        // Funzione per andare alla prossima card
        function nextCard() {
            if (isAnimating) return;
            
            isAnimating = true;
            currentIndex = (currentIndex + 1) % serviceCards.length;
            updateCards();
            
            setTimeout(() => {
                isAnimating = false;
            }, 800);
        }
        
        // Funzione per andare alla card precedente
        function prevCard() {
            if (isAnimating) return;
            
            isAnimating = true;
            currentIndex = (currentIndex - 1 + serviceCards.length) % serviceCards.length;
            updateCards();
            
            setTimeout(() => {
                isAnimating = false;
            }, 800);
        }
        
        // Funzione per andare a una card specifica
        function goToCard(index) {
            if (isAnimating || index === currentIndex) return;
            
            isAnimating = true;
            currentIndex = index;
            updateCards();
            
            setTimeout(() => {
                isAnimating = false;
            }, 800);
        }
        
        // Auto-play
        function startAutoPlay() {
            autoPlayInterval = setInterval(nextCard, 4000);
        }
        
        function stopAutoPlay() {
            if (autoPlayInterval) {
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
            }
        }
        
        // Gestione scroll per cambiare card
        let scrollTimeout;
        function handleScroll() {
            if (scrollTimeout) {
                clearTimeout(scrollTimeout);
            }
            
            scrollTimeout = setTimeout(() => {
                const rect = servicesCarousel.getBoundingClientRect();
                const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
                
                if (isVisible) {
                    startAutoPlay();
                } else {
                    stopAutoPlay();
                }
            }, 100);
        }
        
        // Gestione touch/swipe per mobile
        let touchStartX = 0;
        let touchEndX = 0;
        
        function handleTouchStart(e) {
            touchStartX = e.changedTouches[0].screenX;
        }
        
        function handleTouchEnd(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }
        
        function handleSwipe() {
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    nextCard();
                } else {
                    prevCard();
                }
            }
        }
        
        // Event listeners per le frecce
        if (prevButton) {
            prevButton.addEventListener('click', prevCard);
        }
        
        if (nextButton) {
            nextButton.addEventListener('click', nextCard);
        }
        
        // Event listeners per scroll
        window.addEventListener('scroll', handleScroll);
        servicesCarousel.addEventListener('touchstart', handleTouchStart, { passive: true });
        servicesCarousel.addEventListener('touchend', handleTouchEnd, { passive: true });
        
        // Pausa auto-play quando l'utente interagisce
        servicesCarousel.addEventListener('mouseenter', stopAutoPlay);
        servicesCarousel.addEventListener('mouseleave', () => {
            const rect = servicesCarousel.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
            if (isVisible) {
                startAutoPlay();
            }
        });
        
        // Gestione click sulle card per navigazione
        serviceCards.forEach((card, index) => {
            card.addEventListener('click', () => {
                if (index !== currentIndex) {
                    goToCard(index);
                }
            });
        });
        
        // Gestione click sugli indicatori
        progressDots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                if (index !== currentIndex) {
                    goToCard(index);
                }
            });
        });
        
        // Inizializza con animazione di entrata
        setTimeout(() => {
            updateCards();
        }, 100);
        
        // Avvia auto-play se la sezione è visibile
        const rect = servicesCarousel.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
        if (isVisible) {
            setTimeout(startAutoPlay, 2000);
        }
    }
    
    // Inizializza il carosello di servizi
    initServicesCarousel();

    // 7. Gestione Timeline Giornata Tipo
    function initDailyRoutineTimeline() {
        const timelineSteps = document.querySelectorAll('.timeline-step');
        const prevButton = document.querySelector('.timeline-prev');
        const nextButton = document.querySelector('.timeline-next');
        const currentStepSpan = document.querySelector('.current-step');
        const totalStepsSpan = document.querySelector('.total-steps');
        
        if (!timelineSteps.length || !prevButton || !nextButton) {
            return;
        }
        
        let currentStep = 0;
        let isAnimating = false;
        let autoPlayInterval;
        
        // Aggiorna il display del progresso
        function updateProgress() {
            if (currentStepSpan) {
                currentStepSpan.textContent = currentStep + 1;
            }
            if (totalStepsSpan) {
                totalStepsSpan.textContent = timelineSteps.length;
            }
        }
        
        // Aggiorna le classi degli step
        function updateSteps() {
            timelineSteps.forEach((step, index) => {
                step.classList.remove('active', 'completed');
                
                if (index === currentStep) {
                    step.classList.add('active');
                } else if (index < currentStep) {
                    step.classList.add('completed');
                }
            });
            
            // Aggiorna stato dei bottoni
            prevButton.disabled = currentStep === 0;
            nextButton.disabled = currentStep === timelineSteps.length - 1;
        }
        
        // Vai al prossimo step
        function nextStep() {
            if (isAnimating || currentStep >= timelineSteps.length - 1) return;
            
            isAnimating = true;
            currentStep++;
            updateSteps();
            updateProgress();
            
            setTimeout(() => {
                isAnimating = false;
            }, 600);
        }
        
        // Vai al step precedente
        function prevStep() {
            if (isAnimating || currentStep <= 0) return;
            
            isAnimating = true;
            currentStep--;
            updateSteps();
            updateProgress();
            
            setTimeout(() => {
                isAnimating = false;
            }, 600);
        }
        
        // Vai a uno step specifico
        function goToStep(stepIndex) {
            if (isAnimating || stepIndex === currentStep) return;
            
            isAnimating = true;
            currentStep = stepIndex;
            updateSteps();
            updateProgress();
            
            setTimeout(() => {
                isAnimating = false;
            }, 600);
        }
        
        // Auto-play progressivo (senza loop)
        function startAutoPlay() {
            autoPlayInterval = setInterval(() => {
                if (currentStep < timelineSteps.length - 1) {
                    nextStep();
                } else {
                    // Ferma l'auto-play quando arriva all'ultimo step
                    stopAutoPlay();
                }
            }, 3000);
        }
        
        function stopAutoPlay() {
            if (autoPlayInterval) {
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
            }
        }
        
        // Event listeners
        prevButton.addEventListener('click', prevStep);
        nextButton.addEventListener('click', nextStep);
        
        // Click sugli step per navigazione diretta
        timelineSteps.forEach((step, index) => {
            step.addEventListener('click', () => {
                if (index !== currentStep) {
                    goToStep(index);
                }
            });
        });
        
        // Gestione scroll per illuminazione progressiva
        let scrollTimeout;
        function handleScroll() {
            if (scrollTimeout) {
                clearTimeout(scrollTimeout);
            }
            
            scrollTimeout = setTimeout(() => {
                const timelineSection = document.querySelector('.daily-routine-section');
                if (timelineSection) {
                    const rect = timelineSection.getBoundingClientRect();
                    const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
                    
                    if (isVisible) {
                        // Calcola quale step dovrebbe essere illuminato basato sulla posizione
                        const sectionHeight = timelineSection.offsetHeight;
                        const scrollProgress = Math.max(0, Math.min(1, (window.innerHeight - rect.top) / sectionHeight));
                        const targetStep = Math.floor(scrollProgress * timelineSteps.length);
                        
                        // Illumina progressivamente gli step
                        timelineSteps.forEach((step, index) => {
                            if (index <= targetStep) {
                                step.classList.add('completed');
                                step.classList.remove('active');
                            } else {
                                step.classList.remove('active', 'completed');
                            }
                        });
                        
                        // Lo step attivo è sempre l'ultimo illuminato
                        if (targetStep < timelineSteps.length) {
                            timelineSteps[targetStep].classList.add('active');
                            timelineSteps[targetStep].classList.remove('completed');
                        }
                        
                        // Aggiorna il progresso
                        currentStep = Math.min(targetStep, timelineSteps.length - 1);
                        updateProgress();
                    }
                }
            }, 50);
        }
        
        // Gestione interazione utente
        const timelineSection = document.querySelector('.daily-routine-section');
        if (timelineSection) {
            // Aggiungi classe per indicare che l'utente ha interagito
            timelineSection.addEventListener('click', () => {
                timelineSection.classList.add('user-interacted');
            });
        }
        
        // Gestione touch/swipe per mobile
        let touchStartX = 0;
        let touchEndX = 0;
        
        function handleTouchStart(e) {
            touchStartX = e.changedTouches[0].screenX;
        }
        
        function handleTouchEnd(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }
        
        function handleSwipe() {
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    nextStep();
                } else {
                    prevStep();
                }
            }
        }
        
        // Event listeners per scroll e touch
        window.addEventListener('scroll', handleScroll);
        if (timelineSection) {
            timelineSection.addEventListener('touchstart', handleTouchStart, { passive: true });
            timelineSection.addEventListener('touchend', handleTouchEnd, { passive: true });
        }
        
        // Inizializza
        updateSteps();
        updateProgress();
        
        // Avvia l'effetto di scroll immediatamente
        handleScroll();
    }
    
    // Inizializza la timeline
    initDailyRoutineTimeline();

    // 4. Gestione Lightbox per Galleria Fotografica
    if (galleryItems.length > 0) {
        let currentIndex = 0;
        let galleryImages = [];

        // Popola l'array di immagini dalla galleria
        galleryItems.forEach((item, index) => {
            const img = item.querySelector('img');
            galleryImages.push({
                src: img.src,
                alt: img.alt
            });

            // Aggiungi l'evento click su ogni immagine della galleria
            item.addEventListener('click', function() {
                openLightbox(index);
            });
        });

        // Funzione per aprire il lightbox
        function openLightbox(index) {
            currentIndex = index;
            updateLightboxContent();
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden'; // Blocca lo scroll della pagina
        }

        // Funzione per chiudere il lightbox
        function closeLightbox() {
            lightbox.classList.remove('active');
            document.body.style.overflow = ''; // Ripristina lo scroll della pagina
            setTimeout(() => {
                lightboxImage.src = '';
            }, 300);
        }

        // Funzione per aggiornare i contenuti del lightbox
        function updateLightboxContent() {
            const image = galleryImages[currentIndex];
            lightboxImage.src = image.src;
            lightboxCaption.textContent = image.alt;
            
            // Mostra/nascondi i controlli in base alla posizione
            lightboxPrev.style.display = currentIndex > 0 ? 'flex' : 'none';
            lightboxNext.style.display = currentIndex < galleryImages.length - 1 ? 'flex' : 'none';
        }

        // Funzione per mostrare l'immagine precedente
        function showPrevImage() {
            if (currentIndex > 0) {
                currentIndex--;
                updateLightboxContent();
            }
        }

        // Funzione per mostrare l'immagine successiva
        function showNextImage() {
            if (currentIndex < galleryImages.length - 1) {
                currentIndex++;
                updateLightboxContent();
            }
        }

        // Eventi per i controlli del lightbox
        lightboxClose.addEventListener('click', closeLightbox);
        lightboxPrev.addEventListener('click', showPrevImage);
        lightboxNext.addEventListener('click', showNextImage);

        // Chiudi il lightbox quando si clicca fuori dall'immagine
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });

        // Gestione navigazione da tastiera
        document.addEventListener('keydown', function(e) {
            if (!lightbox.classList.contains('active')) return;

            switch (e.key) {
                case 'Escape':
                    closeLightbox();
                    break;
                case 'ArrowLeft':
                    showPrevImage();
                    break;
                case 'ArrowRight':
                    showNextImage();
                    break;
            }
        });
    }
});
