/**
 * Casa Famiglia Castelletto - Galleria Fotografica
 * Script per gestire la galleria a schermo intero con scorrimento automatico
 */

document.addEventListener('DOMContentLoaded', function() {
    // Riferimenti agli elementi DOM
    const slides = document.querySelectorAll('.gallery-slide');
    const prevButton = document.querySelector('.gallery-prev');
    const nextButton = document.querySelector('.gallery-next');
    const indicators = document.querySelectorAll('.gallery-indicator');
    
    // Variabili di stato
    let currentSlide = 0;
    let slideInterval;
    const slideDelay = 5000; // 5 secondi tra ogni slide
    
    // Funzione per mostrare una slide specifica
    function showSlide(index) {
        // Rimuovi la classe active da tutte le slide
        slides.forEach(slide => {
            slide.classList.remove('active');
        });
        
        // Rimuovi la classe active da tutti gli indicatori
        indicators.forEach(indicator => {
            indicator.classList.remove('active');
        });
        
        // Aggiungi la classe active alla slide corrente
        slides[index].classList.add('active');
        
        // Aggiungi la classe active all'indicatore corrente
        indicators[index].classList.add('active');
        
        // Aggiorna l'indice della slide corrente
        currentSlide = index;
    }
    
    // Funzione per passare alla slide successiva
    function nextSlide() {
        let newIndex = currentSlide + 1;
        if (newIndex >= slides.length) {
            newIndex = 0; // Torna alla prima slide se siamo all'ultima
        }
        showSlide(newIndex);
    }
    
    // Funzione per passare alla slide precedente
    function prevSlide() {
        let newIndex = currentSlide - 1;
        if (newIndex < 0) {
            newIndex = slides.length - 1; // Vai all'ultima slide se siamo alla prima
        }
        showSlide(newIndex);
    }
    
    // Funzione per avviare lo scorrimento automatico
    function startSlideshow() {
        // Ferma eventuali intervalli precedenti
        if (slideInterval) {
            clearInterval(slideInterval);
        }
        
        // Avvia un nuovo intervallo
        slideInterval = setInterval(nextSlide, slideDelay);
    }
    
    // Funzione per fermare lo scorrimento automatico
    function stopSlideshow() {
        clearInterval(slideInterval);
    }
    
    // Inizializza la galleria
    function initGallery() {
        // Mostra la prima slide
        showSlide(0);
        
        // Avvia lo scorrimento automatico
        startSlideshow();
        
        // Aggiungi event listener ai pulsanti
        if (prevButton) {
            prevButton.addEventListener('click', function() {
                prevSlide();
                // Riavvia lo slideshow dopo l'interazione dell'utente
                startSlideshow();
            });
        }
        
        if (nextButton) {
            nextButton.addEventListener('click', function() {
                nextSlide();
                // Riavvia lo slideshow dopo l'interazione dell'utente
                startSlideshow();
            });
        }
        
        // Aggiungi event listener agli indicatori
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', function() {
                showSlide(index);
                // Riavvia lo slideshow dopo l'interazione dell'utente
                startSlideshow();
            });
        });
        
        // Pausa lo slideshow quando il mouse è sopra la galleria
        const gallery = document.querySelector('.gallery-fullscreen');
        if (gallery) {
            gallery.addEventListener('mouseenter', stopSlideshow);
            gallery.addEventListener('mouseleave', startSlideshow);
            
            // Gestione touch per dispositivi mobili
            gallery.addEventListener('touchstart', function() {
                stopSlideshow();
            }, {passive: true});
            
            gallery.addEventListener('touchend', function() {
                startSlideshow();
            }, {passive: true});
        }
    }
    
    // Avvia la galleria se ci sono slide
    if (slides.length > 0) {
        initGallery();
    }
});
