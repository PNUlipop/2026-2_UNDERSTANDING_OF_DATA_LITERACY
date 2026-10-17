from pathlib import Path
import base64,mimetypes,re
P=Path(__file__).resolve().parent
s=(P/'src/index.html').read_text()
s=s.replace('<link rel="stylesheet" href="deck.css">','<style>'+(P/'src/deck.css').read_text()+'</style>')
for name,path in [('../assets/anime.min.js',P/'assets/anime.min.js'),('deck.js',P/'src/deck.js')]:s=s.replace(f'<script src="{name}"></script>','<script>'+path.read_text().replace('</script','<\\/script')+'</script>')
def embed(m):
 path=(P/'src'/m[1]).resolve();mime=mimetypes.guess_type(path)[0];return m[0].replace(m[1],'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode())
s=re.sub(r'(?:src|poster)="(\.\./assets/[^"]+)"',embed,s)
(P/'dist/index.html').write_text(s);(P/'news-analysis-plan.html').write_text(s)
print('Built',P/'news-analysis-plan.html',len(s.encode()),'bytes')
