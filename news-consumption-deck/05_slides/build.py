"""Build the offline, single-file submission HTML from editable source files."""
from pathlib import Path
import base64, mimetypes, re
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent
html=(ROOT/'index.html').read_text()
data=(PROJECT/'04_assets/charts/survey-summary.json').read_text()
# Keep JSON embedded locally in the editable source too, so file:// works.
html=re.sub(r'(<script id="survey-data" type="application/json">).*?(</script>)',lambda m:m[1]+data+m[2],html,flags=re.S)
(ROOT/'index.html').write_text(html)
html=html.replace('<link rel="stylesheet" href="styles/deck.css">','<style>'+(ROOT/'styles/deck.css').read_text()+'</style>')
for name in ['vendor/anime.min.js','scripts/deck.js']:
    html=html.replace(f'<script src="{name}"></script>','<script>'+(ROOT/name).read_text().replace('</script','<\\/script')+'</script>')
def embed(m):
    path=(ROOT/m[1]).resolve()
    mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'
    return 'src="data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()+'"'
html=re.sub(r'src="(\.\./04_assets/[^"]+)"',embed,html)
out=PROJECT/'06_exports/news-consumption-2025.html'
out.write_text(html)
print(out, out.stat().st_size, 'bytes')
