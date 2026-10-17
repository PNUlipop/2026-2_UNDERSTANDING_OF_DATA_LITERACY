from pathlib import Path
import av
p=Path(__file__).resolve().parents[1]
video=av.open(str(p/'assets/workflow.mp4'))
next(video.decode(video=0)).to_image().save(p/'assets/workflow-poster.png')
