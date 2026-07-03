const purgecss = require('@fullhuman/postcss-purgecss');
const cssnano = require('cssnano');

const CONTENT_GLOBS = [
  './*.html',
  './**/*.html',
  './**/*.js',
  './partials/**/*.html',
];

const SAFELIST = {
  standard: [
    'is-open',
    'is-visible',
    'is-scrolled',
    'is-image-fallback',
    'has-cookie-banner',
    'active',
    'next',
    'prev',
    'completed',
    'user-interacted',
    'cta-sticky',
    'blog-filter__btn--active',
    'animate-on-scroll',
    'stagger-children',
    'stagger-150',
    'fade-in-up',
    'fade-in',
    'slide-in-left',
    'slide-in-right',
    'scale-in',
  ],
  deep: [
    /^faq-/,
    /^accordion/,
    /^mobile-nav/,
    /^cookie-/,
    /^nav-/,
    /^gallery-/,
    /^lightbox/,
    /^blog-/,
  ],
  greedy: [/^btn--/, /^btn-/],
};

module.exports = {
  plugins: [
    purgecss({
      content: CONTENT_GLOBS,
      defaultExtractor: (content) => content.match(/[\w-/:.%[\]()]+(?<!:)/g) || [],
      safelist: SAFELIST,
      variables: true,
      keyframes: true,
    }),
    cssnano({ preset: 'default' }),
  ],
};
