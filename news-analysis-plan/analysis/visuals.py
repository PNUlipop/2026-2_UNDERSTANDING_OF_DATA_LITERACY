from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.font_manager import FontProperties
P=Path(__file__).resolve().parents[1]
font=FontProperties(fname='/System/Library/Fonts/AppleSDGothicNeo.ttc',size=17)
fig,ax=plt.subplots(figsize=(10,4.6),dpi=160)
fig.patch.set_facecolor('black');ax.set_facecolor('black')
sns.heatmap(np.zeros((5,6)),annot=np.full((5,6),'—'),fmt='',cmap=sns.color_palette(['#141414'],as_cmap=True),cbar=False,linewidths=4,linecolor='black',ax=ax,annot_kws={'color':'#888','size':22})
ax.set_xticklabels(['19–29세','30대','40대','50대','60대','70세 이상'],fontproperties=font,rotation=0,color='#ccc')
ax.set_yticklabels(['TV','포털·검색','온라인 동영상','숏폼','SNS'],fontproperties=font,rotation=0,color='white');ax.tick_params(length=0,pad=12)
fig.tight_layout(pad=1.3);fig.savefig(P/'assets/heatmap-plan.png',facecolor='black');plt.close(fig)
