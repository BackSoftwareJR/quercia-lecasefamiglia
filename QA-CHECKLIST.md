# QA Checklist — Casa Famiglia Quercia

> Verificato: 2026-06-22 (server locale :8765)

## Funzionale
- [x] Tutti i link interni principali rispondono 200
- [x] Contatti senza form — tel, WhatsApp, email attivi
- [x] WhatsApp link corretto con messaggio precompilato
- [x] Video hero: autoplay muted loop desktop, immagine statica mobile
- [x] Gallery: tab filter + lightbox implementati
- [x] FAQ accordion: 10 domande, prima aperta
- [x] Cookie banner: localStorage, appare al primo accesso
- [x] 404.html personalizzata con link home
- [x] ZERO overlay scuri su immagini/video homepage

## Mobile
- [x] Header hamburger implementato
- [x] Gallery 1 colonna mobile (CSS grid)
- [x] Timeline verticale mobile
- [x] Form campi min-height 44px
- [x] WhatsApp FAB fixed bottom-right
- [x] Body font-size 16px (1rem)

## Performance
- [x] Immagini gallery con lazy loading
- [x] Script con defer
- [x] Font display=swap via Google Fonts
- [ ] Lighthouse >90 (da eseguire su produzione con asset completi)

## SEO
- [x] Title e meta description unici per pagina principale
- [x] sitemap.xml con lastmod
- [x] robots.txt corretto
- [x] LodgingBusiness + FAQPage schema homepage
- [x] Article + BreadcrumbList su blog

## GDPR
- [x] Cookie banner funzionante
- [x] Privacy/Cookie/T&C GDPR con P.IVA IT13206680012
- [x] Contatto solo tel/WhatsApp/email (nessun form)
- [ ] Email info@ da attivare lato client

## Blog slug mapping (direttive → attuali)
| Direttiva | Slug attuale |
|-----------|--------------|
| differenza-casa-famiglia-rsa | casa-famiglia-vs-rsa-differenze |
| quando-genitore-anziano-ha-bisogno-assistenza | domande-figli-casa-famiglia |
| cosa-include-retta-casa-famiglia | costi-retta-casa-famiglia-piemonte |
| benefici-vita-comunita-anziani-autosufficienti | autonomia-dignita-terza-eta |
| come-scegliere-casa-famiglia-anziani | scegliere-casa-famiglia-genitori |
| valle-di-susa-anziani-qualita-vita | valle-di-susa-vita-anziani |
| senso-di-colpa-affidare-genitore-struttura | (coperto in più articoli) |
| ginnastica-dolce-anziani-benefici | (menzionato in la-giornata) |
| inserimento-casa-famiglia-anziani | inserimento-nuovo-ospite |
| visite-familiari-anziani-importanza | visite-familiari-casa-famiglia |
