## 프로젝트 개요

- KSJ 랜딩 홈페이지. Astro 7 + Tailwind CSS 4 (정적 사이트).
- 이 폴더(`ksj-landing`) 안에서만 작업한다. 형제 폴더(ksj-365blog, ksj-bookmaker 등)는 참조하지 않는다.
- 사용자는 초보자 — 설명은 쉽게, 명령어는 복사해서 붙여넣을 수 있게 제공한다.
- 페이지는 `src/pages/`, 공통 틀은 `src/layouts/Layout.astro`, 재사용 조각은 `src/components/`, 이미지 등 정적 파일은 `public/`.

## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)
