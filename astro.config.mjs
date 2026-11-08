import { defineConfig } from 'astro/config';

// GitHub Pages: https://leinerke.github.io/porfolio/
// Si luego conectas un dominio propio, cambia `site` por el dominio y quita `base`.
export default defineConfig({
  site: 'https://leinerke.github.io',
  base: '/porfolio/',
});
