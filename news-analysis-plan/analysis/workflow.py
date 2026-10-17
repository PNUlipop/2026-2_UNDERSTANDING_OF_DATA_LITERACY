from manim import *
config.background_color='#000000'
class AnalysisPlan(Scene):
 def construct(self):
  xs=[-4.8,-1.6,1.6,4.8];labels=['SOURCE','CLEAN','WEIGHT','VERIFY']
  path=Line([-4.8,0,0],[4.8,0,0],color='#444444',stroke_width=3)
  self.add(path)
  for i,(x,label) in enumerate(zip(xs,labels)):
   self.add(Circle(radius=.17,stroke_width=3,color='#aaaaaa').move_to([x,0,0]),Text(label,font='Arial',font_size=26,color='#bbbbbb').move_to([x,-.75,0]),Text(f'0{i+1}',font='Arial',font_size=20,color='#777777').move_to([x,.7,0]))
  cursor=Dot([xs[0],0,0],radius=.11,color='#1c69d4');self.add(cursor);self.wait(.4)
  for x in xs[1:]:self.play(cursor.animate.move_to([x,0,0]),run_time=1.3,rate_func=smooth);self.wait(.35)
  self.wait(.8)
