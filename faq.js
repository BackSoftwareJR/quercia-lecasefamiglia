/**
 * FAQ JavaScript - Implementazione semplice e robusta
 * Gestisce l'apertura e chiusura delle FAQ
 */

document.addEventListener('DOMContentLoaded', function() {
    // Seleziona tutti i bottoni delle domande
    const faqButtons = document.querySelectorAll('.faq-question');
    
    // Aggiungi event listener ad ogni bottone
    faqButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Ottieni l'ID della risposta correlata
            const answerId = this.getAttribute('aria-controls');
            const answer = document.getElementById(answerId);
            
            // Controlla se è già aperta
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            // Chiudi tutte le altre FAQ
            faqButtons.forEach(btn => {
                if (btn !== this) {
                    btn.setAttribute('aria-expanded', 'false');
                    const otherAnswerId = btn.getAttribute('aria-controls');
                    const otherAnswer = document.getElementById(otherAnswerId);
                    if (otherAnswer) {
                        otherAnswer.style.display = 'none';
                    }
                }
            });
            
            // Toggle per questa FAQ
            if (isExpanded) {
                // Chiudi questa FAQ
                this.setAttribute('aria-expanded', 'false');
                answer.style.display = 'none';
            } else {
                // Apri questa FAQ
                this.setAttribute('aria-expanded', 'true');
                answer.style.display = 'block';
            }
        });
    });
    
    // Inizializza le FAQ come chiuse
    faqButtons.forEach(button => {
        button.setAttribute('aria-expanded', 'false');
        const answerId = button.getAttribute('aria-controls');
        const answer = document.getElementById(answerId);
        if (answer) {
            answer.style.display = 'none';
        }
    });
});
