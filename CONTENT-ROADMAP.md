# Content & SEO Roadmap — Casa Famiglia Castelletto

> Strategia per massima visibilità organica. Aggiornato: 2026-06-22

## Obiettivo

Essere trovati da figli 45–65 che cercano una soluzione per genitori autosufficienti in **Coazze, Valle di Susa, Giaveno, Pinerolo, Avigliana** e dintorni — con contenuti profondi, non pagine sottili.

## Architettura contenuti

### Tier 1 — Pagine core (conversione)
| URL | Keyword primaria | Ruolo |
|-----|------------------|-------|
| `/` | casa famiglia anziani Coazze | Landing principale — 12 sezioni |
| `/contatti/` | contatti casa famiglia Coazze | Conversione diretta |
| `/rette-e-ammissione/` | retta casa famiglia anziani | Trasparenza processo |

### Tier 2 — Pagine dedicate (fiducia + profondità)
| URL | Keyword | Stato |
|-----|---------|-------|
| `/storia/` | storia casa famiglia Casa Famiglia Castelletto – Pinerolo | ✅ Creata |
| `/galleria/` | foto casa famiglia Coazze | ✅ Creata |
| `/requisiti-autosufficienza/` | requisiti anziani autosufficienti | ✅ Creata |
| `/chi-siamo/` | chi siamo casa famiglia | Esistente — arricchire |
| `/servizi/` | servizi casa famiglia anziani | Esistente — arricchire |
| `/la-struttura/` | ambienti villa anziani | Esistente — arricchire |
| `/la-giornata/` | giornata tipo casa famiglia | Esistente — arricchire |

### Tier 3 — Landing geografiche (long-tail locale)
| URL | Keyword target |
|-----|----------------|
| `/casa-famiglia-coazze/` | casa famiglia anziani Coazze |
| `/casa-famiglia-giaveno/` | casa famiglia anziani Giaveno |
| `/casa-famiglia-pinerolo/` | casa famiglia anziani Pinerolo |
| `/casa-famiglia-valle-di-susa/` | casa famiglia Valle di Susa anziani |
| `/casa-famiglia-avigliana/` | casa famiglia anziani Avigliana |

### Tier 4 — Blog (autorità + educazione)
**10 articoli pubblicati** — ogni articolo 1.200–1.800 parole, TOC, schema Article, CTA tel/WhatsApp, articoli correlati in sidebar, hero image, internal linking verso pagine core e geo.

| Slug | Categoria |
|------|-----------|
| `casa-famiglia-vs-rsa-differenze` | Guida |
| `scegliere-casa-famiglia-genitori` | Scelta consapevole |
| `anziani-autosufficienti-coazze` | Territorio |
| `valle-di-susa-vita-anziani` | Benessere |
| `visite-familiari-casa-famiglia` | Vita in casa |
| `costi-retta-casa-famiglia-piemonte` | Costi |
| `inserimento-nuovo-ospite` | Accoglienza |
| `autonomia-dignita-terza-eta` | Cura relazionale |
| `coazze-giaveno-pinerolo-servizi` | Servizi locali |
| `domande-figli-casa-famiglia` | FAQ |

Rigenerazione: `python3 scripts/build-blog-overhaul.py`

**Articoli aggiuntivi pianificati (Fase 2 blog):**
- Senso di colpa nell'affidare un genitore
- Ginnastica dolce per anziani: benefici quotidiani
- Quando un genitore ha bisogno di assistenza (segnali)
- Differenza casa famiglia vs residenza assistita
- Come preparare l'inserimento del genitore

## Brand identity (vincolante)

- **Voce:** calda, rassicurante, parla ai figli — mai istituzionale
- **Promessa:** seconda casa, non RSA
- **Colori:** verde `#2D5A3D`, crema `#F5EDD8`, terracotta `#C17A3A`
- **Font:** Cormorant Garamond (titoli) + Inter (corpo)
- **Regola immagini:** ZERO overlay scuri su foto/video

## Internal linking

Ogni pagina → minimo 3 link interni verso: `/contatti/`, `/rette-e-ammissione/`, `/servizi/`, landing geo correlate, blog pertinente.

## Prossimo loop (priorità)

1. [x] Espandere tutti i 10 blog a 1.200+ parole con TOC e articoli correlati
2. [ ] Aggiungere 5 nuovi articoli blog (Fase 2)
3. [ ] Landing geo: Trana, Valgioie, Torino provincia
4. [ ] Testimonianze reali (sostituire placeholder)
5. [ ] Formspree + email info@casafamigliaquercia.it
6. [ ] Lighthouse audit post-deploy
7. [ ] Google Search Console + sitemap submit

## Metriche target

- Lighthouse: >90 tutte le categorie
- Blog: min 1.200 parole/articolo ✅
- Landing geo: min 800 parole uniche per pagina
- Schema: LodgingBusiness, FAQPage, Article, BreadcrumbList su ogni pagina pertinente
