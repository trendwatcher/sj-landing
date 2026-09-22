// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// GitHub Pages 주소: https://trendwatcher.github.io/sj-landing
// 나중에 개인 도메인을 연결하면 site 를 그 주소로 바꾸고 base 는 '/' 로 두면 됩니다.
// https://astro.build/config
export default defineConfig({
  site: 'https://trendwatcher.github.io',
  base: '/sj-landing/',
  vite: {
    plugins: [tailwindcss()]
  }
});
