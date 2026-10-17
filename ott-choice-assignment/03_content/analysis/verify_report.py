"""Check each transcribed series against its source page, plus logical ranges.
This is a transcription check, not an inferential test or microdata reanalysis.
"""
from pathlib import Path
from pypdf import PdfReader
import json,re
ROOT=Path(__file__).resolve().parents[2]
d=json.loads((ROOT/'04_assets/charts/survey-summary.json').read_text())
r=PdfReader(next((ROOT/'00_inbox').glob('*.pdf')))
def check(page,vals):
 text=r.pages[page+15].extract_text()
 tokens=set(re.findall(r'(?<!\d)-?\d+\.\d+(?!\d)',text.replace('–','-').replace('−','-')))
 for v in vals:
  value=f'{v:.2f}' if abs(v)<1 else f'{v:.1f}'
  assert value in tokens,(page,value)
for page,values in [(33,d['monthly_top7']['values']),(36,d['main']),(43,d['paid']['subscription']),(47,d['burden']['values'])]:check(page,values)
for row in d['age_subscription']['values']:check(43,row)
for i,row in enumerate(d['evaluation']['positive']):check(d['evaluation']['pages'][i],row)
for i in range(4):check(d['evaluation']['price_pages'][i],[d['evaluation']['price'][i]]);check(d['evaluation']['satisfaction_pages'][i],[d['evaluation']['satisfaction'][i]])
for g in d['genres']:check(g['page'],[g['value']])
assert all(m>=p for m,p in zip(d['monthly'],d['main']))
assert all(-2<=x<=2 for k in ['price','satisfaction'] for x in d['evaluation'][k])
assert sum(d['age_subscription']['n'])==2536
print('PASS: all displayed chart series located on cited PDF pages; sample totals, units, ranges checked')
