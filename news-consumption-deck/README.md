# 세대별 뉴스 소비 경로 차이 — HTML 슬라이드덱

현재 단계: 총 14장 HTML 슬라이드덱. 중복 선 그래프 삭제, 생성형 AI 뉴스 이용을 결론 전 보조 사례로 배치. 참고자료가 마지막.

## 열기와 수정

- **제출·발표 파일:** `06_exports/news-consumption-2025.html` — 이미지, 영상, 라이브러리, 집계 데이터가 포함된 오프라인 단일 파일. Chrome에서 더블클릭으로 열기.
- **수정용:** `05_slides/index.html`, `styles/deck.css`, `scripts/deck.js`
- **다시 내보내기:** 프로젝트 상위 Week_7에서 `python3 news-consumption-deck/05_slides/build.py`
- **조작:** 방향키·Space 이동, Home/End 처음·끝, R 다시 보기, N 메모, F 전체 화면, M 모션 전환. 하단에 마우스를 두면 조작 버튼 표시.
- **피드백:** 실제 페이지 번호로 알려주세요. 예: “5페이지 범례”, “9페이지 설명”. 고정 S번호와 페이지의 대응은 `03_content/storyline.md`에서 확인합니다.
- **발표자 정보:** 202406228 김경현, 데이터리터러시의이해 중간 대체 과제.

## 분석 재현

```sh
python3 -m pip install pandas numpy pyreadstat matplotlib seaborn openpyxl
python3 news-consumption-deck/03_content/analysis/analyze.py
```

Manim 영상은 `motion_scene.py`와 집계 JSON으로 재생성합니다. Manim 설치에는 Cairo·Pango·pkg-config가 필요합니다.

```sh
python3 -m pip install manim
python3 -m manim -qm --media_dir news-consumption-deck/04_assets/charts/manim news-consumption-deck/03_content/analysis/motion_scene.py NewsRoutes
```

생성 영상 `04_assets/charts/manim/videos/motion_scene/720p30/NewsRoutes.mp4`를 `04_assets/charts/news-routes.mp4`로 복사한 뒤 빌드합니다. 분석 그림은 macOS AppleGothic을 사용합니다. 다른 OS에서는 `analyze.py`의 폰트를 설치된 한글 폰트로 지정하세요.

기술 참고: [Anime.js](https://github.com/juliangarnier/anime/tree/v3.2.2), [Manim](https://docs.manim.community/en/stable/tutorials/quickstart.html). Anime.js 라이선스는 `05_slides/vendor/ANIME-LICENSE.md`에 포함.

## 폴더 안내

```text
news-consumption-deck/
├── 00_inbox/                  # 우선 넣는 곳: 아직 분류하지 않은 파일
├── 01_brief/                 # 발표 목적·대상·범위·조건
├── 02_references/
│   ├── evidence/             # 통계, 논문, 보고서, 기사 원문
│   └── design/               # 참고할 슬라이드, 웹페이지 캡처, 디자인 예시
├── 03_content/               # 스토리라인, 슬라이드 원고, 인용
├── 04_assets/
│   ├── images/               # 실제 슬라이드에 사용할 이미지
│   ├── charts/               # 차트 원본 데이터와 생성 결과
│   └── fonts/                # 사용 가능한 폰트와 라이선스
├── 05_slides/                # HTML·CSS·JS 구현
│   ├── styles/               # CSS
│   └── scripts/              # JS
├── 06_exports/              # 발표·제출용 HTML 묶음, PDF, 미리보기
└── 07_collaboration/        # 피드백과 결정 기록
```

## 우리 둘이 작업하는 방법

1. 자료를 `00_inbox/`에 넣고 채팅에서 파일 이름과 용도를 알려주세요. 링크만 있으면 레퍼런스 목록에 URL을 적어도 됩니다.
2. 사실·수치의 근거는 `02_references/evidence/`, 시각적 참고는 `02_references/design/`에 정리합니다. 각각의 목록에 파일과 설명을 연결합니다.
3. 발표 조건은 `01_brief/brief.md`에서 정리합니다. 미정인 항목은 미정으로 두고, 추정을 확정사항으로 취급하지 않습니다.
4. 슬라이드는 S01, S02처럼 고정 ID를 붙입니다. 피드백은 “S03 · 근거 · 이 수치의 조사 연도를 표시해줘”처럼 남기면 됩니다.
5. 확정된 내용은 `07_collaboration/decisions.md`, 아직 처리할 요청은 `07_collaboration/feedback.md`에 기록합니다. 채팅으로 요청해도 제가 해당 문서에 반영할 수 있습니다.

## 파일 이름과 인용 규칙

- 근거 자료: `SRC-001_기관_연도_짧은제목.pdf`
- 디자인 참고: `DES-001_짧은설명.png`
- 실제 사용할 에셋: `S03_연령별뉴스경로.svg`
- 날짜가 필요한 파일: `2026-10-16_짧은설명.ext`
- 원문 파일은 보존하고, 요약·해석·가공 데이터는 별도 파일에 작성합니다.
- 수치가 등장하는 슬라이드는 출처 ID와 페이지/표 번호를 연결합니다. 디자인 참고자료를 통계 근거로 사용하지 않습니다.
- 웹 링크에는 게시일과 확인일을 기록합니다. 개인정보나 로그인 정보는 넣지 않습니다.

기존 상위 폴더의 분석 파일들은 이동하거나 수정하지 않았습니다.
