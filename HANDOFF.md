# Handoff — Casa Famiglia Gramsci

## Deploy

1. Caricare l'intera cartella su Hostinger (sottodominio `gramsci.lecasefamiglia.it`)
2. Assicurarsi che `images/`, `videos/`, `icons/` siano inclusi nel deploy
3. Configurare `404.html` come pagina errore nel pannello hosting
4. Verificare HTTPS attivo

## Azioni obbligatorie pre-lancio

### 1. Email professionale
Creare `info@gramsci.lecasefamiglia.it` su Hostinger Mail e verificare che riceva i messaggi in arrivo (contatto solo via telefono, WhatsApp ed email — nessun modulo online).

### 2. Testimonianze
Sostituire i 3 placeholder in `index.html` sezione 8 con recensioni reali.

### 3. Team Chi Siamo
Sostituire avatar placeholder con foto e nomi reali in `chi-siamo/index.html`.

### 4. Immagine Open Graph
Opzionale: creare `images/og-gramsci.jpg` (1200×630px) per social — intanto si usa la foto sala da pranzo (.avif) già referenziata nei meta.

## Struttura file

```
css/          → design system (nuovo)
js/           → main, gallery, animations, cookie-banner, nav, includes
partials/     → header.html, footer.html
index.html    → homepage 12 sezioni
[page]/index.html → pagine interne
blog/         → 10 articoli
```

## CSS legacy (root)
I file `design-system.css`, `components.css`, `style.css`, `pages.css` alla root sono obsoleti. Le pagine aggiornate usano `css/`. Rimuovere dopo verifica deploy.

## Verifica post-deploy

```bash
curl -I https://gramsci.lecasefamiglia.it/
curl -I https://gramsci.lecasefamiglia.it/sitemap.xml
```

- Testare gallery tab + lightbox su mobile
- Testare cookie banner (cancellare localStorage `gramsci_cookie_consent`)
- Lighthouse audit su URL produzione

## Contatti sito

- Tel: +39 376 203 1211
- WhatsApp: https://wa.me/393762031211
- Email: info@gramsci.lecasefamiglia.it
- Indirizzo: Piazza Gramsci, 17, 10050 Coazze (TO)
- Sito: https://gramsci.lecasefamiglia.it

## Dati legali (GDPR / footer / pagine legali)

- **Ragione sociale:** Quercia & Gramsci S.r.l.s.
- **P.IVA:** IT13186510015 — va indicata in footer, contatti e pagine legali (privacy, cookie, termini)
- **Attività:** Casa Famiglia Gramsci — struttura residenziale per anziani autosufficienti
- Pagine legali: `/privacy-policy/`, `/cookie-policy/`, `/termini-e-condizioni/` (ultimo aggiornamento: 22 giugno 2026)
- Nessun modulo contatti online: raccolta dati solo via telefono, WhatsApp ed email
