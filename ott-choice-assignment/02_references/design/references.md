# 디자인·에셋 기록

## 디자인

사용자 제공 `bmw-m/DESIGN.md`를 이 폴더의 `BMW-M-DESIGN.md`로 보존했습니다. BMW M의 검정·흰색, 굵은 제목과 가벼운 본문, 직선형 구획, 삼색의 작은 스트라이프를 적용했습니다. OTT 과제의 의미에 맞도록 자동차 대신 TV·리모컨 사진을 사용했습니다. BMW 로고나 전용 라이선스 폰트는 포함하지 않았습니다. 브랜드 포인트와 별도로 파랑은 비교 지표·히트맵의 데이터 색으로 사용합니다.

## Google Flow 이미지

- 생성일: 2026-10-16
- 서비스: Google Flow, Nano Banana 2.1, 이미지 생성 x2 중 1장 채택
- 프로젝트: https://flow.google.com/project/5465e9d3-137a-4925-b306-fcf001cb627f
- 채택 에셋: `9bb1b069-ac63-4bd9-a2b3-1ca735cb54c2`
- 다운로드: 원본 1K, `Television_remote_on_table_20261016152607.jpg`
- 사용 파일: `04_assets/images/flow-ott-cover.jpg` (1376×768)
- 사용처: 1장 표지, 11장 결론 크롭
- AI 생성임을 표지·결론·참고자료에 명시. 수치·차트·실제 플랫폼 화면은 포함시키지 않았습니다.

### 프롬프트

> Photorealistic premium editorial photograph for a Korean academic presentation about streaming platform choice. Wide 16:9 composition. A matte black television remote in the foreground on a black table, a large television on the right showing an abstract grid of cinematic scenes with no text or logos. Dark minimalist apartment at night. Crisp hard-edged architectural composition, restrained cold blue rim light and tiny red indicator light, deep true black shadows, refined industrial product photography. All objects confined to the right two thirds, left third completely black negative space for typography. No cars, no brands, no lettering, no numbers, no infographic.

## 시각화

- Manim Community 0.22.0: 월간 이용→주 이용 1순위 전환(시간 변화 아님), 720p30 영상
- Seaborn: 플랫폼별 동일 문항 16개 값 히트맵. HTML 모션 그래프와 같은 JSON 사용
- Anime.js: npm 패키지 3.2.2 로컬 번들, MIT 라이선스 파일 동봉. 막대·선·점·히트맵 진입 모션
- 영상·이미지·JS·JSON 모두 제출 HTML에 내장하여 외부 네트워크 의존 없음
