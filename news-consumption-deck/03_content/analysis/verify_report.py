"""Cross-check deck data against report figures transcribed after reading source pages."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import pyreadstat
ROOT=Path(__file__).resolve().parents[2]
d=json.loads((ROOT/'04_assets/charts/survey-summary.json').read_text())
# Entries: report page, figure/table, overall, then six age groups in deck order.
controls={
 ('main','TV'):(70,'표 4-2',[48.0,11.1,24.9,37.9,55.9,71.1,82.2]),
 ('main','포털·검색'):(70,'표 4-2',[33.0,56.8,51.4,41.8,28.4,14.9,7.7]),
 ('main','온라인 동영상'):(70,'표 4-2',[5.6,7.7,6.4,8.0,5.7,3.9,1.8]),
 ('main','숏폼'):(70,'표 4-2',[1.2,2.6,2.9,1.0,0.5,0.1,0.4]),
 ('main','SNS'):(70,'표 4-2',[0.9,3.3,2.3,0.3,0.1,0.0,0.0]),
 ('main','뉴스 비이용'):(70,'표 4-2',[3.7,9.5,4.1,1.9,1.9,2.4,3.2]),
 ('weekly','TV'):(83,'그림 4-27',[81.4,48.2,70.1,85.6,91.2,93.0,94.0]),
 ('weekly','포털·검색'):(96,'그림 4-49',[66.5,80.5,81.8,79.3,70.7,56.3,29.5]),
 ('weekly','온라인 동영상'):(116,'그림 4-90',[30.0,34.6,35.5,37.4,34.9,24.6,11.9]),
 ('weekly','숏폼'):(122,'그림 4-102',[22.9,26.5,34.3,28.0,26.0,15.2,7.1]),
 ('weekly','SNS'):(110,'그림 4-78',[8.1,16.3,14.9,8.6,5.8,2.7,1.5]),
 ('weekly','생성형 AI'):(130,'그림 4-120·122',[2.1,3.9,3.7,2.5,2.4,0.5,0.0]),
}
rows=[]
for (metric,channel),(page,figure,expected) in controls.items():
 actual=[d['overall'][metric][channel]]+[g[metric][channel] for g in d['groups']]
 assert [round(v,1) for v in actual]==expected,(metric,channel,actual,expected)
 rows.append(f'| {"주 이용" if metric=="main" else "주간 이용"} | {channel} | p.{page}, {figure} | '+ ' / '.join(f'{v:.1f}' for v in expected)+' | 일치 |')
# Independent reconstruction of all overlap categories from respondent-level SAV.
raw,meta=pyreadstat.read_sav(next((ROOT/'00_inbox').rglob('*.SAV')))
assert len(raw)==6000
bins=[(19,29),(30,39),(40,49),(50,59),(60,69),(70,150)]
for g,(lo,hi) in zip(d['groups'],bins):
 r=raw[raw.DQ3.between(lo,hi)]
 assert len(r)==g['n']
 a,b=r.Q53.eq(1),r.Q61.eq(1)
 for label,mask in [('동영상만',a&~b),('둘 다',a&b),('숏폼만',~a&b),('둘 다 비이용',~a&~b)]:
  value=float(r.loc[mask,'WT'].sum()/r.WT.sum()*100)
  assert abs(value-g['overlap'][label])<1e-9
expected_cases=[885,938,1038,1165,1055,918]
assert [round(g['weighted_n']) for g in d['groups']]==expected_cases
p=ROOT/'07_collaboration/report-check.md'
p.write_text('''# 2025 언론수용자 조사 보고서 대조 기록

검토일: 2026-10-16. 대상: HTML 슬라이드 S01–S15, 집계 JSON, 분석 코드.

## 결과

보고서에 직접 실린 가중 비율 84개(전체 및 6개 연령집단 × 12개 지표)를 대조했고, 모두 소수점 첫째 자리까지 일치했습니다. 설계·문항 정의·주요 해석도 확인했습니다.

열의 수치 순서: 전체 / 19–29세 / 30대 / 40대 / 50대 / 60대 / 70세 이상. 단위: %.

| 지표 | 경로 | 보고서 근거 | 보고서 및 덱 수치 | 결과 |
| --- | --- | --- | --- | --- |
'''+ '\n'.join(rows)+'''

## 보고서에 직접 있는 내용과 추가 분석의 구분

- S02 조사 대상·표본 6,000명·기간·대면면접 방식: p.48, 표 3-1과 일치.
- S05 ‘40대 이하 포털, 50대 이상 TV가 1위’: p.70 본문의 설명과 일치.
- S09 온라인 동영상 뉴스는 40대 37.4%, 숏폼 뉴스는 30대 34.3%가 최고: p.116·122와 일치.
- S11 19–29세 뉴스 비이용 응답 9.5%: p.70 표 4-2의 ‘20대’ 9.5%와 일치. 조사의 하한은 만 19세이며, 덱은 해당 집단을 19–29세로 명시.
- S07 50대 TV·포털 격차 27.6%포인트: 공개 원자료의 반올림 전 가중 비율 55.908012… − 28.352686… = 27.555326…을 반올림. 보고서 표시값 55.9 − 28.4로 계산하면 27.5가 되므로 계산 기준을 주석으로 명시. 보고서에 직접 실린 격차 수치로 취급하지 않음.
- S10 중복 이용: 보고서에 직접 제시된 표가 아니라 Q53·Q61 원자료 교차분석. 6개 연령대 × 4개 응답 조합을 원자료로 독립 재계산해 일치 확인. 30대 합집합 47.9%, 중복 21.9%.
- S04 TV+포털 81.0%, S06 ‘기타 경로’ 구성: 원자료에서 별도 합산·재분류한 값. 원래 경로를 중복하지 않도록 계산.
- S13 뉴스 전달·원문 출처 확인에 대한 제언: 보고서의 직접 인용이 아닌 분석자의 해석으로 표시.
- 실제 비가중 n(828/869/1,038/1,189/1,098/978)과 보고서 가중 사례수(885/938/1,038/1,165/1,055/918)를 구분. 가중 사례수도 재계산 결과와 일치.

## 명확히 보완한 표현

- S08 TV 주간 이용률은 TV 수상기만 뜻하지 않음. 문13은 모바일·컴퓨터를 통한 TV 뉴스/시사 프로그램 시청도 포함하므로 해당 정의를 각주·메모에 추가.
- S10은 원자료 추가 교차분석이라는 점을 화면 출처와 메모에 명시.
- S12 생성형 AI 뉴스 이용률에 보고서 p.130 그림 4-120·122를 추가해 직접 찾을 수 있도록 함.
- S14 백분율 계산식에 ×100을 명시.

## 해석 범위

현재 연령집단의 기술통계 비교이며 세대의 인과효과, 개인의 노화에 따른 변화, 통계적 유의성을 입증한 분석이 아닙니다. 주 이용 경로(단일응답)와 주간 뉴스 이용 여부(여러 경로 중복 가능)를 구분합니다.

재검증: `python3 news-consumption-deck/03_content/analysis/verify_report.py`
''')
print('보고서 비율 84개 일치. 원자료 중복 이용 24개 및 사례수 재계산 일치.')
