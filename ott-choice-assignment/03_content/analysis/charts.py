"""Rebuild Seaborn chart from transcribed, page-audited report statistics (not microdata)."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
ROOT=Path(__file__).resolve().parents[2]
d=json.loads((ROOT/'04_assets/charts/survey-summary.json').read_text())['evaluation']
sns.set_theme(style='white',rc={'figure.facecolor':'black','axes.facecolor':'black','text.color':'white'})
font=FontProperties(fname='/System/Library/Fonts/AppleSDGothicNeo.ttc',size=16)
fig,ax=plt.subplots(figsize=(13,5.3),dpi=160)
cm=sns.blend_palette(['#0d0d0d','#0066b1','#1c69d4'],as_cmap=True)
sns.heatmap(d['positive'],annot=True,fmt='.1f',vmin=0,vmax=100,cmap=cm,linewidths=4,linecolor='black',cbar=False,ax=ax,annot_kws={'fontsize':19,'color':'white'})
ax.set_xticklabels(['원하는 콘텐츠','다른 곳에 없는 콘텐츠','구성 방식의 편의','재생 자유도'],fontproperties=font,rotation=0,color='#bbbbbb')
ax.set_yticklabels(d['platforms'],fontproperties=font,rotation=0,color='white');ax.tick_params(length=0,pad=14)
plt.tight_layout(pad=1.2);fig.savefig(ROOT/'04_assets/charts/evaluation-seaborn.png',facecolor='black');plt.close(fig)
print('Seaborn heatmap built')
# Static evidence view for reduced-motion users, print, and video fallback.
all_data=json.loads((ROOT/'04_assets/charts/survey-summary.json').read_text())
fig,ax=plt.subplots(figsize=(12.8,7.2),dpi=100)
fig.patch.set_facecolor('black');ax.set_facecolor('black')
import numpy as np
y=np.arange(5)
ax.barh(y-.16,all_data['monthly'],height=.26,color='#bbbbbb',label='Monthly use')
ax.barh(y+.16,all_data['main'],height=.26,color='#1c69d4',label='Most frequent / first choice')
for i,(a,b) in enumerate(zip(all_data['monthly'],all_data['main'])):
 ax.text(a+1,i-.16,f'{a:.1f}%',va='center',color='white',fontsize=17)
 ax.text(b+1,i+.16,f'{b:.1f}%',va='center',color='white',fontsize=17)
ax.set_yticks(y,['YouTube','Netflix','Coupang Play','TVING','Wavve'],color='white',fontsize=17);ax.invert_yaxis();ax.set_xlim(0,85);ax.set_xticks([0,20,40,60,80]);ax.tick_params(axis='x',colors='#bbb',labelsize=15);ax.spines[:].set_visible(False);ax.grid(axis='x',color='#292929');ax.set_axisbelow(True);ax.legend(loc='lower right',facecolor='black',labelcolor='white',edgecolor='none',fontsize=14);fig.tight_layout(pad=3);fig.savefig(ROOT/'04_assets/charts/reach-main-static.png',facecolor='black');plt.close(fig)
