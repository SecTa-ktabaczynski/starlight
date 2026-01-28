// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

import mdx from '@astrojs/mdx';
import astroExpressiveCode from 'astro-expressive-code';

// https://astro.build/config
export default defineConfig({
  site: 'https://SecTa-ktabaczynski.github.io',
  base: '/starlight',

  integrations: [
    astroExpressiveCode(),
    mdx(),
    starlight({
      title: 'My Docs',
      sidebar: [
        { label: 'Wszystkie dokumenty', link: '/all-docs/' },
        {
          label: 'Guides',
          items: [
            { label: 'Example Guide', slug: 'guides/example' },
            { label: 'Docs', slug: 'guides/docs' },
          ],
        },
        {
          label: 'Reference',
          autogenerate: { directory: 'reference' },
        },
        {
          label: 'Custom',
          autogenerate: { directory: 'custom' },
        },
      ],
      head: [{
        tag: 'script',
        content: `if (!localStorage.getItem('starlight-theme')) {
          localStorage.setItem('starlight-theme', 'dark');
          document.documentElement.classList.add('dark');
        }`,
        attrs: {
          is: 'inline'
        }
      }]
    })
  ]
});
