"""A measured transition from monthly reach to most-frequent use. Source pp.33,36."""
from pathlib import Path
import json
from manim import *
Text.set_default(font='Arial')
config.background_color='#000000'
config.pixel_width=1280
config.pixel_height=720
config.frame_rate=30
config.frame_width=12
config.frame_height=6.75
class ReachToMain(Scene):
 def construct(self):
  d=json.loads((Path(__file__).resolve().parents[2]/'04_assets/charts/survey-summary.json').read_text())
  names=['YouTube','Netflix','Coupang Play','TVING','Wavve']
  title=Text('MONTHLY USE  /  MULTIPLE ANSWERS',font_size=27).move_to([0,2.65,0])
  self.add(title)
  x0=-3.2; scale=7.3/80
  axis=Line([x0,-2.15,0],[x0+80*scale,-2.15,0],color='#666666')
  self.add(axis,*[Text(str(v),font_size=20,color='#bbbbbb').move_to([x0+v*scale,-2.45,0]) for v in [0,20,40,60,80]])
  bars=[]; vals=[]
  for i,(name,v) in enumerate(zip(names,d['monthly'])):
   y=1.6-i*.7
   lab=Text(name,font_size=23).move_to([-4.75,y,0])
   bar=Rectangle(width=v*scale,height=.27,stroke_width=0,fill_color='#bbbbbb',fill_opacity=1).move_to([x0+v*scale/2,y,0])
   val=Text(f'{v:.1f}%',font_size=23).next_to(bar,RIGHT,buff=.15)
   self.add(lab);bars.append(bar);vals.append(val)
  self.play(LaggedStart(*[GrowFromEdge(b,LEFT) for b in bars],lag_ratio=.12),LaggedStart(*[FadeIn(v) for v in vals],lag_ratio=.12),run_time=1.7)
  self.wait(1.6)
  next_title=Text('MOST-FREQUENT USE  /  FIRST CHOICE',font_size=27).move_to(title)
  anim=[Transform(title,next_title)]
  for i,v in enumerate(d['main']):
   y=1.6-i*.7
   nb=Rectangle(width=v*scale,height=.27,stroke_width=0,fill_color='#1c69d4',fill_opacity=1).move_to([x0+v*scale/2,y,0])
   nv=Text(f'{v:.1f}%',font_size=23,color=WHITE).next_to(nb,RIGHT,buff=.15)
   anim.extend([Transform(bars[i],nb),Transform(vals[i],nv)])
  self.play(*anim,run_time=2)
  self.add(Text('Same respondents, different questions. N = 2,536',font_size=21,color='#bbbbbb').move_to([0,-3,0]))
  self.wait(2)
