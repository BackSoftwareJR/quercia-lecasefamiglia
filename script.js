/**
 * Casa Famiglia Quercia - Hero Section JavaScript
 * Funzionalità:
 * 1. Caricamento video in base al dispositivo (desktop/mobile)
 * 2. CTA button sticky su mobile
 * 3. Gestione preferenze reduced motion
 */

document.addEventListener('DOMContentLoaded', function() {
    // Debug mode
    const DEBUG = true;
    function log(message) {
        if (DEBUG) console.log(message);
    }
    
    log('DOM caricato');
    // Riferimenti elementi DOM
    const heroVideo = document.getElementById('heroVideo');
    const ctaButton = document.querySelector('.cta-button');
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
        callButton.href = 'tel:3341174614';
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
        heroVideo.poster = 'images/Pinerolo - Casa Famiglia Quercia 1/img1.avif';
        
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
                            heroContainer.style.backgroundImage = 'url("images/Pinerolo - Casa Famiglia Quercia 1/img1.avif")';
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
