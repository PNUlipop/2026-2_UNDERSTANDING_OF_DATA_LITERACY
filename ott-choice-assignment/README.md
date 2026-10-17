# 과제1 — 사람들은 왜 그 OTT를 선택할까?

플랫폼별 이용 현황과 선택 배경 탐색 · 데이터리터러시의이해 · **202406228 김경현**

발표·제출용: [13장 HTML 슬라이드덱](06_exports/ott-choice-2024.html)

파일 하나에 이미지, 영상, 데이터, CSS와 JS가 들어 있어 인터넷 없이 Chrome에서 열 수 있습니다. 화면에 맞춰 16:9 슬라이드가 축소됩니다.

- `← / →` 또는 `Space`: 이전·다음 / `Home / End`: 처음·끝
- 4페이지: 진입 시 대기 → `Space / →`로 비교 모션 시작 → 재생 중이거나 종료된 뒤 다시 누르면 다음 장으로 이동합니다. 재생 중·종료 후 `←`는 먼저 모션 시작 전으로 복원하며, 대기 상태에서 다시 누르면 3페이지로 이동합니다. 하단 다음 버튼·스와이프도 동일합니다.
- `R`: 현재 그래프 다시 재생 / `M`: 모션 켜기·끄기
- `N`: 발표 메모 / `F`: 전체 화면
- 하단에 마우스를 움직이면 발표 제어가 표시됩니다.
- 8페이지는 문항별 도트 플롯와 Seaborn 히트맵 보기 전환을 지원합니다.
- OS의 모션 줄이기를 존중하며, Manim 영상은 정적 비교 그래프로 대체됩니다.

## 자료와 해석 범위

제공된 KISDI 정책자료 24-07(2024년)의 집계 통계를 재구성했습니다. 만 15–64세 OTT 이용자 2,536명 대상 인터넷 패널 조사로, 전 국민 보급률·현재 시장점유율이 아닙니다. ‘선택 이유’ 직접 순위 문항은 없으므로 콘텐츠·이용 편의·가격 평가를 통해 선택 배경을 탐색합니다. 개인 원자료 분석·인과추론·유의성 검정은 하지 않았습니다.

## 작업 위치

| 경로 | 용도 |
| --- | --- |
| `00_inbox/` | 제공된 원본 PDF |
| `01_brief/brief.md` | 과제 범위·표기 |
| `02_references/evidence/sources.md` | 지표·분모·보고서 쪽수 |
| `02_references/evidence/page-previews/` | 원문 시각 대조용 페이지 |
| `02_references/design/` | BMW M 지침 사본·Flow 생성 기록 |
| `03_content/storyline.md` | 13장 흐름 |
| `03_content/slides.md` | 현재 슬라이드 원고 |
| `03_content/analysis/` | 수치 검증·Seaborn·Manim 코드·CSV |
| `04_assets/charts/survey-summary.json` | 그래프의 공통 데이터 |
| `04_assets/images/` | Flow 이미지 원본 |
| `05_slides/` | 편집용 HTML·CSS·JS·오프라인 vendor |
| `06_exports/` | 제출용 단일 HTML |
| `07_collaboration/` | 결정·검수·피드백 기록 |

## 재생성

```sh
python3 ott-choice-assignment/03_content/analysis/verify_report.py
python3 ott-choice-assignment/03_content/analysis/charts.py
python3 -m manim -qm --media_dir ott-choice-assignment/04_assets/charts/manim ott-choice-assignment/03_content/analysis/motion_scene.py ReachToMain
cp ott-choice-assignment/04_assets/charts/manim/videos/motion_scene/720p30/ReachToMain.mp4 ott-choice-assignment/04_assets/charts/reach-to-main.mp4
python3 ott-choice-assignment/05_slides/build.py
```

저장소 루트에서 실행합니다. Python 의존성은 `03_content/analysis/requirements.txt`에 기록했습니다. Manim 렌더 캐시는 버전 관리에서 제외하며, 최종 MP4는 보존합니다. 숫자를 바꾸면 JSON과 해당 분석·출처 기록을 먼저 수정한 후 재생성합니다. 기존 뉴스 기말 과제는 `../news-consumption-deck/`에서 별도 관리합니다.
