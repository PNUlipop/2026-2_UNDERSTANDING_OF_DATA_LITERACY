"""Manim evidence animation. Data are weighted Q84 rates from survey-summary.json."""
from pathlib import Path
import json
from manim import *
Text.set_default(font='Arial')
config.background_color = '#000000'
config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 30
config.frame_width = 12
config.frame_height = 6.75
class NewsRoutes(Scene):
    def construct(self):
        data=json.loads((Path(__file__).resolve().parents[2]/'04_assets/charts/survey-summary.json').read_text())
        groups=data['groups']
        title=Text('TV vs. Portal',font='Arial',font_size=32,color=WHITE).to_edge(UP,buff=.5)
        self.add(title)
        x0=-4.3; scale=8.4/100
        axis=Line([x0,-2.3,0],[x0+100*scale,-2.3,0],color='#555555')
        ticks=VGroup(*[Text(str(i),font_size=22,color='#a1a1a6').move_to([x0+i*scale,-2.6,0]) for i in [0,25,50,75,100]])
        self.play(Create(axis),FadeIn(ticks),run_time=.6)
        rows=[]
        for i,g in enumerate(groups):
            y=1.65-i*.66
            a=g['main']['TV'];b=g['main']['포털·검색']
            lab=Text(['19-29','30-39','40-49','50-59','60-69','70+'][i],font_size=26,color='#a1a1a6').move_to([-5.3,y,0])
            tv=Dot([x0+a*scale,y,0],radius=.085,color='#a1a1a6')
            portal=Dot([x0+b*scale,y,0],radius=.085,color='#2997ff')
            line=Line(tv.get_center(),portal.get_center(),color='#555555',stroke_width=2)
            va=Text(f'{a:.1f}',font_size=25,color=WHITE).next_to(tv,UP,buff=.12)
            vb=Text(f'{b:.1f}',font_size=25,color='#2997ff').next_to(portal,DOWN,buff=.12)
            rows.append(VGroup(lab,line,tv,portal,va,vb))
        self.play(LaggedStart(*[FadeIn(r,shift=UP*.12) for r in rows],lag_ratio=.25),run_time=3)
        self.wait(1)
        self.play(rows[2].animate.set_opacity(.35),rows[0].animate.set_opacity(.35),rows[1].animate.set_opacity(.35),rows[4].animate.set_opacity(.35),rows[5].animate.set_opacity(.35),run_time=.6)
        note=Text('50s: TV 55.9%   Portal 28.4%',font_size=22,color=WHITE).move_to([0,-3.2,0])
        self.play(FadeIn(note),run_time=.6)
        self.wait(2.5)
