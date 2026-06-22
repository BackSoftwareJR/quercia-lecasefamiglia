/**
 * Casa Famiglia Gramsci — Design Tokens (JS)
 * Mirror of design-system.css for programmatic use (theme, analytics, A/B)
 */
(function (global) {
  'use strict';

  const tokens = {
    brand: {
      name: 'Casa Famiglia Gramsci',
      tagline: 'Una seconda casa, non una struttura',
      domain: 'https://gramsci.lecasefamiglia.it',
      parentSite: 'https://www.lecasefamiglia.it/',
    },

    contact: {
      phone: '+39 376 203 1211',
      phoneHref: 'tel:+393762031211',
      whatsapp: '393762031211',
      whatsappHref: 'https://wa.me/393762031211',
      email: 'associazioneunocoazze@gmail.com',
      emailHref: 'mailto:associazioneunocoazze@gmail.com',
      address: {
        street: 'Piazza Gramsci, 17',
        city: 'Coazze',
        province: 'TO',
        postalCode: '10050',
        country: 'IT',
        full: 'Piazza Gramsci, 17, 10050 Coazze (TO)',
      },
    },

    colors: {
      primary: {
        50: '#eef4f0',
        100: '#dce9e1',
        200: '#b9d3c3',
        300: '#96bda5',
        400: '#5f9478',
        500: '#3a6b4a',
        600: '#2f563c',
        700: '#24412e',
        800: '#192c1f',
        900: '#0e1710',
      },
      secondary: {
        50: '#fdfaf5',
        100: '#f5edd8',
        200: '#ebdbb1',
        300: '#e0c98a',
        400: '#d6b763',
        500: '#cca53c',
      },
      accent: {
        50: '#faf0e8',
        100: '#f5e1d1',
        200: '#ebc3a3',
        300: '#e1a575',
        400: '#d18747',
        500: '#c17a3a',
        600: '#9a6230',
        700: '#734a24',
        800: '#4c3218',
        900: '#251a0c',
      },
      neutral: {
        50: '#f7f6f5',
        100: '#eceae8',
        200: '#d9d6d3',
        300: '#b8b4b0',
        400: '#8a8682',
        500: '#4a4a4a',
        600: '#3d3d3d',
        700: '#2e2e2e',
        800: '#1f1f1f',
        900: '#121212',
      },
      semantic: {
        bg: '#fdfaf5',
        text: '#2e2e2e',
        textMuted: '#4a4a4a',
        success: '#2d6a4f',
        warning: '#b8860b',
        error: '#c0392b',
        info: '#2f563c',
      },
    },

    typography: {
      fontHeading: '"Cormorant Garamond", Georgia, serif',
      fontBody: '"DM Sans", "Inter", sans-serif',
      scale: {
        xs: '0.75rem',
        sm: '0.875rem',
        base: '1rem',
        lg: '1.125rem',
        xl: '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
        '5xl': '3rem',
      },
      weight: {
        light: 300,
        regular: 400,
        medium: 500,
        semibold: 600,
        bold: 700,
      },
      leading: {
        tight: 1.25,
        snug: 1.375,
        normal: 1.6,
        relaxed: 1.75,
        loose: 2,
      },
    },

    spacing: {
      1: '0.25rem',
      2: '0.5rem',
      3: '0.75rem',
      4: '1rem',
      6: '1.5rem',
      8: '2rem',
      12: '3rem',
      16: '4rem',
      24: '6rem',
    },

    radius: {
      sm: '0.25rem',
      md: '0.5rem',
      lg: '0.75rem',
      xl: '1rem',
      '2xl': '1.5rem',
      full: '9999px',
    },

    breakpoints: {
      sm: 375,
      md: 768,
      lg: 1024,
      xl: 1280,
    },

    shadows: {
      xs: '0 1px 2px rgba(14, 23, 16, 0.06)',
      sm: '0 2px 4px rgba(14, 23, 16, 0.08)',
      md: '0 4px 12px rgba(14, 23, 16, 0.1)',
      lg: '0 8px 24px rgba(14, 23, 16, 0.12)',
      xl: '0 16px 40px rgba(14, 23, 16, 0.14)',
    },

    cta: {
      discover: 'Scopri di più',
      call: 'Chiama',
      help: 'Ti aiutiamo noi',
      questions: 'Hai altre domande?',
      visit: 'Prenota una visita',
      whatsapp: 'Scrivici su WhatsApp',
    },

    areaServed: [
      'Coazze',
      'Valle di Susa',
      'Giaveno',
      'Avigliana',
      'Pinerolo',
      'Trana',
      'Valgioie',
    ],

    seo: {
      primaryKeyword: 'casa famiglia anziani Coazze',
      siteName: 'Casa Famiglia Gramsci',
    },
  };

  /** Apply CSS custom properties from tokens (optional runtime theming) */
  tokens.applyToDocument = function applyToDocument(doc) {
    const root = (doc || document).documentElement;
    root.style.setProperty('--color-primary', tokens.colors.primary[500]);
    root.style.setProperty('--color-accent', tokens.colors.accent[500]);
    root.style.setProperty('--color-bg', tokens.colors.semantic.bg);
  };

  /** Breakpoint helper */
  tokens.matchesBreakpoint = function matchesBreakpoint(name) {
    const min = tokens.breakpoints[name];
    if (!min) return false;
    return global.matchMedia('(min-width: ' + min + 'px)').matches;
  };

  global.GramsciTokens = tokens;
})(typeof window !== 'undefined' ? window : globalThis);
