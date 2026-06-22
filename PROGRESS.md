# Casa Famiglia Gramsci — Progress Tracker

> Last updated: 2026-06-22 — Blog overhaul completo (10 articoli + index)

## Stato generale: ~92%

| Area | Status |
|------|--------|
| Homepage 12 sezioni (direttive) | Completa |
| Brand identity (#2D5A3D, Inter, zero overlay) | Applicata |
| Visual polish pass (SVG icons, nav, cookie banner, hero) | Completata |
| Pagine dedicate (galleria, storia, requisiti) | ✅ Create |
| Landing geo (5 pagine) | ✅ Create |
| Blog 10 articoli (1.200–1.800 parole, TOC, schema, CTA) | ✅ Completato |
| Blog index (hero, filtri categoria, SEO intro) | ✅ Completato |
| blog.css (layout magazine, sidebar, prose) | ✅ Completato |
| Sitemap (29 URL) | ✅ Aggiornata |
| Footer espanso | ✅ Zone + scopri + blog |

## Blog overhaul (2026-06-22)

- 10 articoli espansi con contenuto unico in italiano (1.200–1.300+ parole ciascuno)
- TOC con anchor H2, hero image, sidebar articoli correlati
- Schema Article + BreadcrumbList, og:image, hreflang it
- CTA finale: Chiama + WhatsApp + /contatti/
- Generator: `scripts/build-blog-overhaul.py` + `scripts/blog_articles_data.py`
- Sorgenti markdown: `content/blog/{slug}.md`

## Prossimo loop (vedi CONTENT-ROADMAP.md)

1. 5 nuovi articoli blog (Fase 2)
2. Landing geo: Trana, Valgioie, Susa
3. Testimonianze reali
4. Formspree + email info@
5. Lighthouse audit post-deploy

## File chiave

- `direttive.txt` — source of truth vincolante
- `CONTENT-ROADMAP.md` — strategia contenuti
- `scripts/build-blog-overhaul.py` — rigenera blog HTML da dati
- `HANDOFF.md` — deploy e task manuali
