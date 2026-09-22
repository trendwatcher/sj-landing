# 김세진 소상공인 컨설팅 랜딩페이지

소상공인 컨설턴트 김세진의 홍보용 랜딩페이지입니다. 상담 문의와 LMS VOD 과정 안내가 목적입니다.

- 주소: https://trendwatcher.github.io/sj-landing
- 기술: [Astro](https://astro.build) + [Tailwind CSS](https://tailwindcss.com) (정적 사이트)

## 내용을 고치려면

| 고치고 싶은 것 | 파일 |
|---|---|
| 전화번호·이메일·주소·LMS 주소 | `src/consts.ts` |
| 첫 화면 문구 | `src/components/Hero.astro` |
| 고민 목록 | `src/components/Pain.astro` |
| 컨설팅 소개 3가지 | `src/components/Solution.astro` |
| Before / After 표 | `src/components/Benefits.astro` |
| VOD 과정 카드 | `src/components/Courses.astro` |
| 고객 후기 | `src/components/Proof.astro` |
| 자주 묻는 질문 | `src/components/Faq.astro` |

## 명령어

```bash
npm install      # 처음 한 번만
npm run dev      # 미리보기 (http://localhost:4321)
npm run build    # 배포용 파일 만들기 (dist 폴더)
```

`main` 브랜치에 올리면 GitHub Actions가 자동으로 GitHub Pages에 배포합니다.
