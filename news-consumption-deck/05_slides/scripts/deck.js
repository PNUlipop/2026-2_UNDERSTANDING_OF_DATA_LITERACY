'use strict';
const DATA=JSON.parse(document.getElementById('survey-data').textContent);
const G=DATA.groups, ages=G.map(x=>x.age);
const BLUE='#0066cc', SKY='#2997ff', GRAY='#7a7a7a';
const fmt=v=>Number(v).toFixed(1);
const el=id=>document.getElementById(id);
const svg=(content,w=1250,h=450,label='')=>`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${label}"><title>${label}</title>${content}</svg>`;
const text=(x,y,t,cls='',anchor='start',fill='')=>`<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}" ${fill?`style="fill:${fill}"`:''}>${t}</text>`;
function accessibleTable(host,rows,headers){const t=document.createElement('table');t.className='sr-only';t.innerHTML=`<caption>그래프 데이터</caption><thead><tr>${headers.map(h=>`<th scope="col">${h}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map((v,i)=>i?`<td>${v}</td>`:`<th scope="row">${v}</th>`).join('')}</tr>`).join('')}</tbody>`;host.append(t)}
function horizontal(id,labels,values,colors,max=100){
 const W=920,H=435,L=170,R=85,T=25,B=42,iw=W-L-R,step=(H-T-B)/labels.length;
 let s='';[0,max/2,max].forEach(v=>{let x=L+iw*v/max;s+=`<line class="grid" x1="${x}" y1="${T-10}" x2="${x}" y2="${H-B}"/>`+text(x,H-8,v+'%','','middle')});
 labels.forEach((lab,i)=>{let y=T+i*step,ww=iw*values[i]/max;s+=text(L-22,y+24,lab,'','end');s+=`<rect class="bar" x="${L}" y="${y}" width="${ww}" height="32" rx="3" fill="${colors[i]}" data-width="${ww}"/>`;s+=text(L+ww+12,y+25,fmt(values[i]),'value')});
 el(id).innerHTML=svg(s,W,H,labels.map((v,i)=>`${v} ${fmt(values[i])}%`).join(', '));accessibleTable(el(id),labels.map((v,i)=>[v,fmt(values[i])]),['구분','가중 비율 (%)']);
}
function lineChart(id,series,key,max=100){
 const W=1360,H=460,L=65,R=70,T=34,B=68,iw=W-L-R,ih=H-T-B;
 const xx=i=>L+iw*i/(G.length-1), yy=v=>T+ih*(1-v/max);let s='';
 for(let v=0;v<=max;v+=(max===50?10:max/4)){let y=yy(v);s+=`<line class="grid" x1="${L}" y1="${y}" x2="${W-R}" y2="${y}"/>`+text(L-18,y+7,v+'%','','end')}
 G.forEach((g,i)=>s+=text(xx(i),H-22,g.age,'','middle'));
 series.forEach((ser,j)=>{let vals=G.map(g=>g[key][ser.name]);let points=vals.map((v,i)=>`${xx(i)},${yy(v)}`).join(' L ');s+=`<path class="draw" d="M ${points}" stroke="${ser.color}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
 vals.forEach((v,i)=>{let off=(j===0? (vals[i]>=G[i][key][series[1].name]?-20:34) : (vals[i]>G[i][key][series[0].name]?-20:34));s+=`<circle class="mark" cx="${xx(i)}" cy="${yy(v)}" r="7" fill="${ser.color}"/>`;s+=text(xx(i)+(i===0?12:0),yy(v)+off,fmt(v),'value',i===0?'start':'middle',ser.color)})});
 el(id).innerHTML=svg(s,W,H,`${key==='main'?'주 이용 경로':'주간 뉴스 이용률'} 연령별 비교`);accessibleTable(el(id),G.map(g=>[g.age,...series.map(s=>fmt(g[key][s.name]))]),['연령',...series.map(s=>s.name+' (%)')]);
}
function stacked(){let s='';const W=1360,H=440,L=145,R=55,T=15,B=40,iw=W-L-R,step=62;[0,25,50,75,100].forEach(v=>{let x=L+v*iw/100;s+=`<line class="grid" x1="${x}" y1="0" x2="${x}" y2="${H-B}"/>`+text(x,H-7,v+'%','','middle')});
 const colors=[GRAY,BLUE,'#74b7f7','#c4c4c9','#e9e9ed'];let rows=[];
 G.forEach((g,i)=>{let m=g.main,v=[m.TV,m['포털·검색'],m['온라인 동영상'],100-m.TV-m['포털·검색']-m['온라인 동영상']-m['뉴스 비이용'],m['뉴스 비이용']];rows.push([g.age,...v.map(fmt)]);let x=L,y=T+i*step;s+=text(L-22,y+28,g.age,'','end');v.forEach((a,j)=>{let width=iw*a/100;s+=`<rect class="bar" x="${x}" y="${y}" width="${width}" height="42" fill="${colors[j]}" data-width="${width}"/>`;if(a>9)s+=text(x+width/2,y+29,fmt(a),'value','middle',j<2?'#fff':'#1d1d1f');x+=width})});el('stacked-chart').innerHTML=svg(s,W,H,'각 연령대의 주 이용 경로 구성, 합계 100%');accessibleTable(el('stacked-chart'),rows,['연령','TV','포털·검색','동영상','기타','비이용']);}
function heatmap(){const cols=['TV','포털·검색','온라인 동영상','숏폼','SNS','생성형 AI'];let html='<div></div>'+cols.map(v=>`<div class="label">${v==='온라인 동영상'?'온라인<br>동영상':v}</div>`).join('');G.forEach(g=>{html+=`<div class="label">${g.age}</div>`;cols.forEach(k=>{const v=g.weekly[k],a=.06+.94*v/100;html+=`<div class="cell" style="background:rgba(0,102,204,${a});color:${v>52?'#fff':'#1d1d1f'}" aria-label="${g.age} ${k} ${fmt(v)}%">${fmt(v)}</div>`})});el('heatmap').innerHTML=html;}
let selectedAge=1;
function overlap(index){selectedAge=index;const g=G[index],o=g.overlap;let union=100-o['둘 다 비이용'];el('overlap-age').textContent=g.age+'의 지난 1주일 뉴스 이용';el('overlap-union').innerHTML=`${fmt(union)}<span class="unit">%</span>`;el('overlap-details').innerHTML=`<div><b>${fmt(g.weekly['온라인 동영상'])}%</b> 온라인 동영상 뉴스 이용</div><div><b>${fmt(g.weekly['숏폼'])}%</b> 숏폼 뉴스 이용</div><div class="accent"><b>${fmt(o['둘 다'])}%</b> 두 문항에 모두 이용 응답</div><small>합집합 = 동영상 이용 + 숏폼 이용 − 중복 이용</small>`;
 const colors=['#74b7f7',BLUE,'#a8cbed','#dedee3'],keys=Object.keys(o);let x=0,s='';keys.forEach((k,i)=>{let w=o[k]*6.6;s+=`<rect class="bar" x="${x}" y="20" width="${w}" height="52" fill="${colors[i]}" data-width="${w}"/>`;x+=w});s+=text(0,105,'0%')+text(660,105,'100%','','end');el('overlap-bar').innerHTML=svg(s,680,135,'동영상만, 둘 다, 숏폼만, 둘 다 비이용의 100% 누적 막대');accessibleTable(el('overlap-bar'),keys.map(k=>[k,fmt(o[k])]),['응답 조합','가중 비율 (%)']);el('overlap-legend').innerHTML=keys.map((k,i)=>`<span style="--c:${colors[i]}">${k} ${fmt(o[k])}%</span>`).join('');
 el('age-selector').querySelectorAll('button').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));if(typeof motion!=='undefined')animateSlide(el('S10'),true);
}
function buildCharts(){let m=DATA.overall.main;const other=100-m.TV-m['포털·검색']-m['온라인 동영상']-m['뉴스 비이용'];horizontal('overall-chart',['TV','포털·검색','온라인 동영상','기타 경로','비이용'],[m.TV,m['포털·검색'],m['온라인 동영상'],other,m['뉴스 비이용']],[GRAY,BLUE,'#74b7f7','#c4c4c9','#e9e9ed']);stacked();heatmap();lineChart('video-lines',[{name:'숏폼',color:BLUE},{name:'온라인 동영상',color:GRAY}],'weekly',50);horizontal('nonuse-chart',ages,G.map(g=>g.main['뉴스 비이용']),G.map((g,i)=>i===0?BLUE:'#c4c4c9'),10);horizontal('ai-chart',ages,G.map(g=>g.weekly['생성형 AI']),G.map((g,i)=>i===0?SKY:'#77777d'),5);el('age-selector').innerHTML=ages.map((a,i)=>`<button data-index="${i}" aria-pressed="${i===1}">${a}</button>`).join('');el('age-selector').addEventListener('click',e=>{let b=e.target.closest('button');if(b)overlap(Number(b.dataset.index))});overlap(1);}
let motion=!matchMedia('(prefers-reduced-motion: reduce)').matches;
let animations=[];
function stopAnimations(){animations.forEach(a=>{a.seek(a.duration);a.pause()});animations=[];}
function animateSlide(slide,chartOnly=false){
 if(!window.anime)return;
 const run=config=>{if(motion)animations.push(anime(config))};
 if(!chartOnly&&motion)run({targets:slide.querySelectorAll('h1,h2,.eyebrow,.lead,.aside,.method-layout,.measure,.takeaways,.reference-list,.appendix-grid'),opacity:[0,1],translateY:[14,0],delay:anime.stagger(65),duration:700,easing:'easeOutCubic'});
 slide.querySelectorAll('.bar').forEach((b,i)=>{b.setAttribute('width',b.dataset.width);if(motion)run({targets:b,width:[0,Number(b.dataset.width)],duration:950,delay:i*45,easing:'easeInOutCubic'})});
 slide.querySelectorAll('.draw').forEach((p,i)=>{if(motion)run({targets:p,strokeDashoffset:[anime.setDashoffset,0],duration:1600,delay:i*180,easing:'easeInOutCubic'})});
 if(motion){run({targets:slide.querySelectorAll('.mark,.cell'),opacity:[0,1],delay:anime.stagger(25),duration:600,easing:'easeOutCubic'});}
 slide.querySelectorAll('[data-count]').forEach(n=>{const val=Number(n.dataset.count);n.textContent=fmt(val);if(motion){const state={value:0};run({targets:state,value:val,duration:1200,easing:'easeOutCubic',update:()=>n.textContent=fmt(state.value)})}});
 const vid=slide.querySelector('video');if(vid){vid.currentTime=motion?0:Math.max(0,(vid.duration||8)-.1);if(motion)vid.play().catch(()=>{vid.controls=true});else vid.pause();}
}
const slides=Array.from(document.querySelectorAll('.slide'));let current=0;
function resize(){el('deck').style.transform=`scale(${Math.min(innerWidth/1600,innerHeight/900)})`}
function show(n,changeHash=true){stopAnimations();slides.forEach(s=>{s.classList.remove('active');s.setAttribute('aria-hidden','true');let v=s.querySelector('video');if(v)v.pause()});current=Math.min(slides.length-1,Math.max(0,n));const s=slides[current];s.classList.add('active');s.setAttribute('aria-hidden','false');el('counter').textContent=`${current+1} / ${slides.length}`;el('progress').style.width=`${(current+1)/slides.length*100}%`;document.title=`${current+1}. ${s.dataset.title}`;el('prev').disabled=current===0;el('next').disabled=current===slides.length-1;el('notes').innerHTML=`<h3>${current+1}. ${s.dataset.title}</h3><p>${s.dataset.notes}</p>`;if(changeHash)history.replaceState(null,'',`#${s.id}`);animateSlide(s)}
function toggleMotion(){stopAnimations();motion=!motion;el('motion').setAttribute('aria-pressed',String(motion));el('motion').textContent=motion?'모션 켜짐':'모션 꺼짐';show(current)}
function toggleNotes(){el('notes').hidden=!el('notes').hidden;el('notes-btn').setAttribute('aria-expanded',String(!el('notes').hidden))}
function full(){if(document.fullscreenElement)document.exitFullscreen?.();else document.documentElement.requestFullscreen?.().catch(()=>{})}
el('prev').onclick=()=>show(current-1);el('next').onclick=()=>show(current+1);el('replay').onclick=()=>show(current);el('notes-btn').onclick=toggleNotes;el('motion').onclick=toggleMotion;el('fullscreen').onclick=full;el('print').onclick=()=>window.print();
document.addEventListener('keydown',e=>{if(e.target.closest('input,textarea,select'))return;if(e.target.closest('button')&&[' ','Enter'].includes(e.key))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1)}else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(current-1)}else if(e.key==='Home'){e.preventDefault();show(0)}else if(e.key==='End'){e.preventDefault();show(slides.length-1)}else if((e.key.toLowerCase()==='r'||e.code==='KeyR'))show(current);else if((e.key.toLowerCase()==='n'||e.code==='KeyN'))toggleNotes();else if((e.key.toLowerCase()==='f'||e.code==='KeyF'))full();else if((e.key.toLowerCase()==='m'||e.code==='KeyM'))toggleMotion();else if(e.key==='Escape')el('notes').hidden=true;});
el('seaborn-toggle').onclick=()=>{let img=el('seaborn-image');img.hidden=!img.hidden;el('heatmap').style.display=img.hidden?'grid':'none';el('seaborn-toggle').textContent=img.hidden?'Seaborn 분석 차트 보기':'애니메이션 히트맵 보기'};
window.addEventListener('resize',resize);window.addEventListener('hashchange',()=>{let i=slides.findIndex(s=>'#'+s.id===location.hash);if(i>=0)show(i,false)});window.addEventListener('beforeprint',()=>{stopAnimations();slides.forEach(s=>{s.querySelectorAll('.bar').forEach(b=>b.setAttribute('width',b.dataset.width));s.querySelectorAll('.draw').forEach(p=>p.style.strokeDashoffset='0')})});
buildCharts();resize();el('motion').textContent=motion?'모션 켜짐':'모션 꺼짐';el('motion').setAttribute('aria-pressed',String(motion));show(Math.max(0,slides.findIndex(s=>'#'+s.id===location.hash)));
