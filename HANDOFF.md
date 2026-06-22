# Handoff — Casa Famiglia Quercia

## Deploy

1. Caricare l'intera cartella su Hostinger (sottodominio `casafamigliaquercia.it`)
2. Assicurarsi che `images/`, `videos/`, `icons/` siano inclusi nel deploy
3. Configurare `404.html` come pagina errore nel pannello hosting
4. Verificare HTTPS attivo

## Azioni obbligatorie pre-lancio

### 1. Email professionale
Creare `info@casafamigliaquercia.it` su Hostinger Mail e verificare che riceva i messaggi in arrivo (contatto solo via telefono, WhatsApp ed email — nessun modulo online).

### 2. Testimonianze
Sostituire i 3 placeholder in `index.html` sezione 8 con recensioni reali.

### 3. Team Chi Siamo
Sostituire avatar placeholder con foto e nomi reali in `chi-siamo/index.html`.

### 4. Immagine Open Graph
Opzionale: creare `images/og-quercia.jpg` (1200×630px) per social — intanto si usa la foto sala da pranzo (.avif) già referenziata nei meta.

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
curl -I https://casafamigliaquercia.it/
curl -I https://casafamigliaquercia.it/sitemap.xml
```

- Testare gallery tab + lightbox su mobile
- Testare cookie banner (cancellare localStorage `quercia_cookie_consent`)
- Lighthouse audit su URL produzione

## Contatti sito

- Tel: +39 376 203 1211
- WhatsApp: https://wa.me/393762031211
- Email: info@casafamigliaquercia.it
- Indirizzo: Stradale Poirino, 152, 10050 Coazze (TO)
- Sito: https://casafamigliaquercia.it

## Dati legali (GDPR / footer / pagine legali)

- **Ragione sociale:** Quercia S.r.l.s.
- **P.IVA:** IT13206680012 — va indicata in footer, contatti e pagine legali (privacy, cookie, termini)
- **Attività:** Casa Famiglia Quercia — struttura residenziale per anziani autosufficienti
- Pagine legali: `/privacy-policy/`, `/cookie-policy/`, `/termini-e-condizioni/` (ultimo aggiornamento: 22 giugno 2026)
- Nessun modulo contatti online: raccolta dati solo via telefono, WhatsApp ed email
