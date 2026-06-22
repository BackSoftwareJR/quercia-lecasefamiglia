#!/usr/bin/env node
/**
 * Genera landing pages geografiche SEO — Casa Famiglia Quercia (Pinerolo)
 * Nota: le pagine sono mantenute manualmente; questo script è un riferimento/template.
 */
const fs = require('fs');
const path = require('path');

const BASE = path.join(__dirname, '..');
const SITE = 'https://casafamigliaquercia.it';
const IMG_PIN = '/images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/';
const IMG_DINING = '/images/Sala%20da%20Pranzo%20%2B%20persone%201.avif';

const pages = [
  {
    slug: 'casa-famiglia-pinerolo',
    title: 'Casa famiglia anziani Pinerolo | Casa Famiglia Quercia – Pinerolese',
    meta: 'Casa famiglia per anziani autosufficienti a Pinerolo (TO). Max 8 ospiti, assistenza 24h, pasti di casa in Stradale Poirino 152. A 40 min da Torino. Prenota una visita gratuita.',
    h1: 'Casa famiglia per anziani autosufficienti a Pinerolo',
    eyebrow: 'Casa Famiglia Quercia · Stradale Poirino 152, Pinerolo',
    lead: 'Nel cuore del Pinerolese, a pochi minuti dal centro di Pinerolo, accogliamo al massimo otto ospiti over 65 in una villa familiare circondata dal verde.',
    image: IMG_DINING,
    imageAlt: 'Pranzo conviviale in sala da pranzo — Casa Famiglia Quercia, Pinerolo',
    primary: true
  },
  {
    slug: 'casa-famiglia-coazze',
    title: 'Casa famiglia per famiglie di Coazze | Casa Famiglia Quercia – Pinerolo',
    meta: 'Cerchi una casa famiglia per anziani autosufficienti vicino Coazze? Casa Famiglia Quercia è a Pinerolo, raggiungibile in 25–35 minuti. Visita gratuita.',
    h1: 'Casa famiglia per famiglie di Coazze e Valle di Susa',
    eyebrow: 'Area servita · Valle di Susa → Pinerolo',
    lead: 'Casa Famiglia Quercia si trova a Pinerolo — a circa 25–35 minuti da Coazze. Accogliamo famiglie della Valle di Susa che cercano un ambiente familiare per genitori ancora autonomi.',
    image: IMG_PIN + 'img9.avif',
    imageAlt: 'Giardino verde di Casa Famiglia Quercia nel Pinerolese — area servita Coazze e Valle di Susa',
    redirectNote: true
  },
  {
    slug: 'casa-famiglia-giaveno',
    title: 'Casa famiglia anziani vicino Giaveno | Casa Famiglia Quercia – Pinerolo',
    meta: 'Cerchi una casa famiglia per genitori autosufficienti vicino Giaveno? Casa Famiglia Quercia a Pinerolo è raggiungibile in 15–20 minuti. Visita gratuita, max 8 ospiti.',
    h1: 'Casa famiglia per anziani vicino Giaveno',
    eyebrow: 'Casa Famiglia Quercia · 15–20 min da Giaveno',
    lead: 'Se abitate a Giaveno e cercate una soluzione serena per un genitore autosufficiente, Casa Famiglia Quercia a Pinerolo è raggiungibile in pochi minuti.',
    image: IMG_PIN + 'img2.avif',
    imageAlt: 'Attività ricreative nel salone comune — Casa Famiglia Quercia, raggiungibile da Giaveno'
  },
  {
    slug: 'casa-famiglia-valle-di-susa',
    title: 'Casa famiglia Valle di Susa e Pinerolese | Casa Famiglia Quercia',
    meta: 'Casa famiglia per anziani autosufficienti in Valle di Susa e Pinerolese. Casa Famiglia Quercia a Pinerolo: natura, assistenza 24h, max 8 ospiti. Prenota una visita.',
    h1: 'Casa famiglia in Valle di Susa e Pinerolese per anziani autosufficienti',
    eyebrow: 'Casa Famiglia Quercia · Valle di Susa e Pinerolese',
    lead: 'La Valle di Susa e il Pinerolese offrono qualità della vita rara. Casa Famiglia Quercia a Pinerolo è pensata per chi vuole invecchiare bene in questo territorio.',
    image: IMG_PIN + 'img10.avif',
    imageAlt: 'Spazi verdi per passeggiate — Casa Famiglia Quercia nel Pinerolese, Valle di Susa'
  },
  {
    slug: 'casa-famiglia-avigliana',
    title: 'Casa famiglia anziani vicino Avigliana | Casa Famiglia Quercia – Pinerolo',
    meta: 'Casa famiglia per anziani autosufficienti vicino Avigliana. Casa Famiglia Quercia a Pinerolo nel Pinerolese — 20–30 min in auto. Ambiente familiare, visita gratuita.',
    h1: 'Casa famiglia per anziani vicino Avigliana',
    eyebrow: 'Casa Famiglia Quercia · Pinerolese, vicino Avigliana',
    lead: 'Le famiglie di Avigliana trovano in Casa Famiglia Quercia a Pinerolo una risposta vicina e umana — a 20–30 minuti in auto.',
    image: IMG_PIN + 'img7.avif',
    imageAlt: 'Camera confortevole con arredi personali — Casa Famiglia Quercia, vicino Avigliana'
  }
];

console.log('Geo landing pages are maintained as hand-written HTML in each slug folder.');
console.log('Pages:', pages.map(function (p) { return p.slug; }).join(', '));
console.log('Run manual edits only — do not overwrite with thin templates.');
