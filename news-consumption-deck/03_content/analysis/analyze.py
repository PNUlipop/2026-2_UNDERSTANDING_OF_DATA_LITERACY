"""Reproduce weighted descriptive analysis from the user-supplied 2025 survey."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import pyreadstat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '04_assets/charts'
OUT.mkdir(parents=True, exist_ok=True)
df, meta = pyreadstat.read_sav(next((ROOT/'00_inbox').rglob('*.SAV')))
AGES = ['19–29세', '30대', '40대', '50대', '60대', '70세 이상']
df['age_group'] = pd.cut(df.DQ3, [18,29,39,49,59,69,150], labels=AGES)
assert len(df) == 6000 and df.age_group.notna().all()
assert df.WT.notna().all() and (df.WT > 0).all()
MAIN = {'TV':2, '포털·검색':5, '온라인 동영상':13, '숏폼':14,
        'SNS':11, '뉴스 비이용':9998}
WEEK = {'TV':df.Q13.eq(1), '포털·검색':df.Q31_1.eq(1)|df.Q31_2.eq(2),
        '온라인 동영상':df.Q53.eq(1), '숏폼':df.Q61.eq(1),
        'SNS':df.Q46.eq(1), '생성형 AI':df.Q73.eq(1)}
def pct(g, mask):
    return float(np.average(mask.loc[g.index].astype(float),weights=g.WT)*100)
def main_rates(g):
    return {k:pct(g,df.Q84.eq(v)) for k,v in MAIN.items()}
def weekly_rates(g):
    return {k:pct(g,v) for k,v in WEEK.items()}
records=[]
for name,g in df.groupby('age_group',observed=True):
    a,b=WEEK['온라인 동영상'],WEEK['숏폼']
    overlap={'동영상만':pct(g,a&~b),'둘 다':pct(g,a&b),
             '숏폼만':pct(g,~a&b),'둘 다 비이용':pct(g,~a&~b)}
    records.append({'age':str(name),'n':len(g),'weighted_n':float(g.WT.sum()),
                    'main':main_rates(g),'weekly':weekly_rates(g),'overlap':overlap})
data={'n':len(df),'weight_sum':float(df.WT.sum()),'groups':records,
      'overall':{'main':main_rates(df),'weekly':weekly_rates(df)},
      'overall_main_full':{meta.variable_value_labels['Q84'][k]:float(v)
        for k,v in (df.groupby('Q84').WT.sum()/df.WT.sum()*100).items()},
      'method':{'weight':'WT','age':'DQ3','main':'Q84',
        'weekly':{'TV':'Q13=1','포털·검색':'Q31_1=1 OR Q31_2=2',
                  '온라인 동영상':'Q53=1','숏폼':'Q61=1','SNS':'Q46=1','생성형 AI':'Q73=1'},
        'population':'전국 만 19세 이상 성인','fieldwork':'2025-07-08 ~ 2025-09-02'}}
# Independent controls from report p.70, table 4-2, rounded to 1 decimal.
expected_tv=[11.1,24.9,37.9,55.9,71.1,82.2]
expected_portal=[56.8,51.4,41.8,28.4,14.9,7.7]
for i,r in enumerate(records):
    assert round(r['main']['TV'],1)==expected_tv[i]
    assert round(r['main']['포털·검색'],1)==expected_portal[i]
    assert abs(sum(r['overlap'].values())-100)<1e-8
assert round(data['overall']['main']['TV'],1)==48.0
assert round(data['overall']['main']['포털·검색'],1)==33.0
(OUT/'survey-summary.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
flat=[]
for r in records:
    for metric in ['main','weekly','overlap']:
        for channel,value in r[metric].items():
            flat.append({'age':r['age'],'unweighted_n':r['n'],
                         'weighted_n':r['weighted_n'],'metric':metric,
                         'channel':channel,'weighted_percent':value})
pd.DataFrame(flat).to_csv(OUT/'weighted-results.csv',index=False,encoding='utf-8-sig')
sns.set_theme(style='white',font='AppleGothic',font_scale=1.15)
plt.rcParams['axes.unicode_minus']=False
matrix=pd.DataFrame([r['weekly'] for r in records], index=AGES)
fig,ax=plt.subplots(figsize=(12,5.2),facecolor='#f5f5f7')
ax.set_facecolor('#f5f5f7')
sns.heatmap(matrix,annot=True,fmt='.1f',cmap=sns.light_palette('#0066cc',as_cmap=True),
            vmin=0,vmax=100,linewidths=5,linecolor='#f5f5f7',
            cbar_kws={'label':'가중 이용률 (%)'},ax=ax)
ax.set_xlabel('');ax.set_ylabel('');ax.tick_params(length=0)
ax.set_yticklabels(ax.get_yticklabels(),rotation=0)
fig.tight_layout()
fig.savefig(OUT/'weekly-heatmap.png',dpi=180,facecolor=fig.get_facecolor())
plt.close(fig)
print(json.dumps(data,ensure_ascii=False,indent=2))
