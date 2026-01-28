// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
    site: 'https://SecTa-ktabaczynski.github.io',
    base: '/starlight',

    integrations: [starlight({
        title: 'My Docs',
        sidebar: [
            {
                label: 'Guides',
                items: [
                    // Each item here is one entry in the navigation menu.
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
		}), mdx()],
});