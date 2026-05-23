import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  site: 'https://www.marekpotucek.com',
  // Řádek s output: 'hybrid' jsme úplně smazali, Astro si samo doplní 'static'
  adapter: node({
    mode: 'standalone',
  }),
});