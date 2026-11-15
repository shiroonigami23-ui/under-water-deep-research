// TOC scroll-spy
(function(){const links=[...document.querySelectorAll('.toc a')];if(!links.length)return;
const map=new Map(links.map(a=>[decodeURIComponent(a.hash.slice(1)),a]));
const obs=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){links.forEach(l=>l.classList.remove('active'));const a=map.get(e.target.id);if(a)a.classList.add('active')}})},{rootMargin:'-80px 0px -70% 0px'});
document.querySelectorAll('.prose h2[id],.prose h3[id]').forEach(h=>obs.observe(h))})();
// Search page
(function(){const box=document.getElementById('q'),out=document.getElementById('results');if(!box)return;
const base=document.querySelector('link[rel=stylesheet]').getAttribute('href').replace('assets/site/site.css','');
let idx=[];fetch(base+'assets/site/search-index.json').then(r=>r.json()).then(d=>{idx=d;const q=new URLSearchParams(location.search).get('q');if(q){box.value=q;run()}});
const esc=s=>s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function run(){const q=box.value.trim().toLowerCase();if(!q){out.innerHTML='';return}const terms=q.split(/\s+/).filter(Boolean);
const res=idx.map(p=>{const t=p.t.toLowerCase(),x=p.x.toLowerCase(),d=p.d.toLowerCase();let s=0;for(const w of terms){if(t.includes(w))s+=10;if(d.includes(w))s+=4;let i=x.indexOf(w),n=0;while(i>-1&&n<20){n++;i=x.indexOf(w,i+1)}if(!n&&!t.includes(w)&&!d.includes(w))return null;s+=n}return{p,s}}).filter(Boolean).sort((a,b)=>b.s-a.s).slice(0,40);
out.innerHTML=`<p class="muted">${res.length} result(s)</p>`+res.map(({p})=>{const x=p.x.toLowerCase(),i=Math.max(0,x.indexOf(terms[0])-90);let snip=esc(p.x.slice(i,i+260));terms.forEach(w=>{snip=snip.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'),'<mark>$1</mark>')});
return `<div class="r"><a href="${base}${p.u}"><b>${esc(p.t)}</b></a><small>${esc(p.s)}</small><p>${esc(p.d)}</p><p class="muted">…${snip}…</p></div>`}).join('')}
box.addEventListener('input',run)})();
// Catalog index: filter, group chips, view toggle, sortable table
(function(){const f=document.querySelector('.catfilter');if(!f)return;let g='*';
const cards=[...document.querySelectorAll('.catgrid .card')],rows=[...document.querySelectorAll('.cattable tbody tr')];
function apply(){const q=f.value.toLowerCase();[...cards,...rows].forEach(el=>{const ok=(g==='*'||el.dataset.g===g)&&el.textContent.toLowerCase().includes(q);el.style.display=ok?'':'none'})}
f.addEventListener('input',apply);
document.querySelectorAll('.chips .chip').forEach(b=>b.onclick=()=>{document.querySelectorAll('.chips .chip').forEach(x=>x.classList.remove('on'));b.classList.add('on');g=b.dataset.g;apply()});
document.querySelectorAll('.viewtoggle .chip').forEach(b=>b.onclick=()=>{document.querySelectorAll('.viewtoggle .chip').forEach(x=>x.classList.remove('on'));b.classList.add('on');
 const t=b.dataset.v==='table';document.querySelector('.catgrid').hidden=t;document.querySelector('.cattable').hidden=!t});
document.querySelectorAll('.cattable th').forEach((th,i)=>th.onclick=()=>{const tb=th.closest('table').tBodies[0],dir=th.dataset.d=th.dataset.d==='1'?'-1':'1';
 [...tb.rows].sort((a,b)=>{const x=a.cells[i].textContent.trim(),y=b.cells[i].textContent.trim(),nx=parseFloat(x.replace(/[,\s]/g,'')),ny=parseFloat(y.replace(/[,\s]/g,''));
 return (isNaN(nx)||isNaN(ny)?x.localeCompare(y):nx-ny)*dir}).forEach(r=>tb.appendChild(r))})})();
// open a collapsible section when linked by #id
(function(){function openHash(){var id=decodeURIComponent(location.hash.slice(1));if(!id)return;var el=document.getElementById(id);if(el&&el.tagName==='DETAILS'){el.open=true;el.scrollIntoView({block:'start'});}}
window.addEventListener('hashchange',openHash);document.addEventListener('DOMContentLoaded',openHash);})();
// ---- live photos from Wikimedia Commons (openly licensed), with credit links ----
(function(){
  var API='https://en.wikipedia.org/api/rest_v1/page/summary/';
  var mem={};
  function get(title){
    if(mem[title])return mem[title];
    var key='wp2:'+title, c=null;
    try{c=JSON.parse(localStorage.getItem(key)||'null')}catch(e){}
    if(c&&Date.now()-c.t<7*864e5)return mem[title]=Promise.resolve(c.v);
    return mem[title]=fetch(API+encodeURIComponent(title.replace(/ /g,'_'))+'?redirect=true').then(function(r){return r.ok?r.json():null}).then(function(j){
      var v=null;
      if(j&&j.thumbnail&&j.originalimage&&j.thumbnail.source.indexOf('/wikipedia/commons/')>-1){
        var src=j.originalimage.source, f=decodeURIComponent(src.split('/').pop());
        v={thumb:j.thumbnail.source, orig:src, file:'https://commons.wikimedia.org/wiki/File:'+encodeURIComponent(f), title:j.title};
      }
      if(j&&j.extract){v=v||{};v.extract=j.extract;v.page=(j.content_urls&&j.content_urls.desktop&&j.content_urls.desktop.page)||'';v.title=v.title||j.title}
      try{localStorage.setItem(key,JSON.stringify({t:Date.now(),v:v}))}catch(e){}
      return v;
    }).catch(function(){return null});
  }
  function sized(u,w){return /\/\d+px-/.test(u)?u.replace(/\/\d+px-/,'/'+w+'px-'):u}
  function fill(el){
    var t=el.getAttribute('data-wiki'); if(!t||el.dataset.done)return; el.dataset.done=1;
    get(t).then(function(v){
      if(!v||!v.thumb){el.classList.add('nophoto');var tx=el.querySelector('svg text:last-of-type');if(tx)tx.textContent='No open photo yet · prompt in prompts.md';return;}
      var big=el.classList.contains('big');
      var img=new Image(); img.alt=v.title; img.loading='lazy'; img.decoding='async';
      img.src=sized(v.thumb,big?960:480);
      img.onerror=function(){img.onerror=null;img.src=v.thumb};
      img.onload=function(){var s=el.querySelector('svg.ph');if(s)s.remove();el.classList.add('hasphoto');};
      el.appendChild(img);
      if(big){var cap=document.createElement('div');cap.className='credit';cap.innerHTML='Photo: <a href="'+v.file+'" target="_blank" rel="noopener">Wikimedia Commons</a> · author &amp; license on file page';el.appendChild(cap);}
    });
  }
  function run(){
    var els=[].slice.call(document.querySelectorAll('.livepic[data-wiki]'));
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);fill(e.target)}})},{rootMargin:'400px'});
      els.forEach(function(e){io.observe(e)});
    } else els.forEach(fill);
    var ps=document.getElementById('photostatus'); if(ps)status(ps);
    [].forEach.call(document.querySelectorAll('.wikibox[data-wiki]'),function(b){get(b.getAttribute('data-wiki')).then(function(v){
      if(v&&v.extract){b.innerHTML='<h3>📘 Overview from Wikipedia</h3><p>'+v.extract.replace(/</g,'&lt;')+'</p><div class="wsrc">Text: <a href="'+v.page+'" target="_blank" rel="noopener">Wikipedia — '+(v.title||'')+'</a> (CC BY-SA 4.0)</div>';b.hidden=false}
      else b.remove();})});
    window.__wpget=get;
  }
  function status(box){
    var base=(document.querySelector('link[href*="site.css"]').getAttribute('href')||'').replace('site.css','');
    Promise.all([fetch(base+'prompts.json').then(function(r){return r.json()}),fetch(base+'photo-index.json').then(function(r){return r.json()})]).then(function(a){
      var prompts={};a[0].forEach(function(p){prompts[p.save]=p});
      var idx=a[1], missing=[], ok=0, n=0;
      return Promise.all(idx.map(function(e){return get(e.wiki).then(function(v){n++;if(v&&v.thumb)ok++;else missing.push(e)})})).then(function(){
        var h='<p><b>'+ok+'</b> of <b>'+idx.length+'</b> entries have a real photo. <b>'+missing.length+'</b> need an image:</p>';
        if(!missing.length)h+='<p>Nothing to generate. 🎉</p>';
        missing.forEach(function(e){var p=prompts[e.save]||{prompt:'Photorealistic image of '+e.name};
          h+='<h3>'+e.name+' <span class="muted small">('+e.coll+')</span></h3><p>Save as: <code>'+e.save+'</code></p><pre class="prompt">'+p.prompt.replace(/</g,'&lt;')+'</pre><button class="btn copy">Copy prompt</button>';});
        box.innerHTML=h;
        [].forEach.call(box.querySelectorAll('button.copy'),function(b){b.onclick=function(){navigator.clipboard.writeText(b.previousElementSibling.textContent);b.textContent='Copied ✓'}});
      });
    }).catch(function(){box.innerHTML='<p>Could not reach Wikipedia from this browser. Every prompt is also in <code>prompts.md</code> in the repository.</p>'});
  }
  document.addEventListener('DOMContentLoaded',run);
})();
// ---- animate charts when scrolled into view ----
(function(){function go(){var cs=document.querySelectorAll('figure.chart.anim');if(!('IntersectionObserver' in window)){cs.forEach(function(c){c.classList.add('inview')});return}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('inview');io.unobserve(e.target)}})},{threshold:.15});cs.forEach(function(c){io.observe(c)})}
document.addEventListener('DOMContentLoaded',go);})();
// ---- animated hero backgrounds: bubbles (ocean) or starfield (space) ----
(function(){function run(){var h=document.querySelector('.hero');var kind=document.body.getAttribute('data-anim');if(!h||!kind)return;
if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var c=document.createElement('canvas');c.className='heroanim';h.insertBefore(c,h.firstChild);var x=c.getContext('2d'),W,H,P=[];
function size(){W=c.width=h.offsetWidth*devicePixelRatio;H=c.height=h.offsetHeight*devicePixelRatio}size();addEventListener('resize',size);
var N=kind==='stars'?220:70;for(var i=0;i<N;i++)P.push({x:Math.random(),y:Math.random(),r:Math.random(),s:Math.random()});
function tick(t){x.clearRect(0,0,W,H);for(var i=0;i<P.length;i++){var p=P[i];
 if(kind==='stars'){var a=.35+.65*Math.abs(Math.sin(t/900*(.3+p.s)+i));x.fillStyle='rgba(255,255,255,'+a+')';x.beginPath();x.arc(p.x*W,p.y*H,(p.r*1.6+.3)*devicePixelRatio,0,6.3);x.fill();p.x+=.00004*(p.s+.2);if(p.x>1)p.x=0}
 else{p.y-=.0006*(p.s+.3);if(p.y<-.05){p.y=1.05;p.x=Math.random()}var px=p.x*W+Math.sin(t/700+i)*6*devicePixelRatio;x.strokeStyle='rgba(160,220,255,'+(.15+.35*p.r)+')';x.lineWidth=1.2*devicePixelRatio;x.beginPath();x.arc(px,p.y*H,(p.r*5+1.5)*devicePixelRatio,0,6.3);x.stroke()}}
requestAnimationFrame(tick)}requestAnimationFrame(tick)}document.addEventListener('DOMContentLoaded',run);})();

// ---- UX: live search dropdown, keyboard shortcuts, scroll state ----
(function(){
 var idx=null,base=(document.querySelector('link[href*="site.css"]')||{}).getAttribute?document.querySelector('link[href*="site.css"]').getAttribute('href').replace('assets/site/site.css',''):'';
 function load(){return idx?Promise.resolve(idx):fetch(base+'assets/site/search-index.json').then(function(r){return r.json()}).then(function(j){idx=j;return j})}
 function score(e,q){var t=e.t.toLowerCase(),i=t.indexOf(q);if(i===0)return 100;if(i>0)return 80;if((e.d||'').toLowerCase().indexOf(q)>-1)return 40;if((e.x||'').toLowerCase().indexOf(q)>-1)return 10;return 0}
 document.addEventListener('DOMContentLoaded',function(){
  var inp=document.getElementById('qs'),box=document.getElementById('qsres'),sel=-1;
  if(inp){
   inp.addEventListener('focus',load);
   inp.addEventListener('input',function(){var q=inp.value.trim().toLowerCase();if(q.length<2){box.hidden=true;return}
    load().then(function(ix){var r=ix.map(function(e){return [score(e,q),e]}).filter(function(a){return a[0]>0}).sort(function(a,b){return b[0]-a[0]}).slice(0,10);
     box.innerHTML=r.map(function(a){return '<a href="'+base+a[1].u+'">'+a[1].t.replace(/</g,'&lt;')+'<small>'+a[1].s+'</small></a>'}).join('')+'<a class="qsall" href="'+base+'wiki/search.html?q='+encodeURIComponent(inp.value)+'">See all results →</a>';
     box.hidden=false;sel=-1;})});
   inp.addEventListener('keydown',function(ev){var as=box.querySelectorAll('a');if(ev.key==='ArrowDown'||ev.key==='ArrowUp'){ev.preventDefault();sel=(sel+(ev.key==='ArrowDown'?1:-1)+as.length)%as.length;as.forEach(function(a,i){a.classList.toggle('sel',i===sel)})}
     else if(ev.key==='Enter'){ev.preventDefault();location.href=(sel>=0&&as[sel])?as[sel].href:base+'wiki/search.html?q='+encodeURIComponent(inp.value)}
     else if(ev.key==='Escape'){box.hidden=true;inp.blur()}});
   document.addEventListener('click',function(ev){if(!ev.target.closest('.search.live'))box.hidden=true;if(!ev.target.closest('.megamenu,.browsebtn,.tabbar'))document.body.classList.remove('megaopen')});
  }
  document.addEventListener('keydown',function(ev){if(ev.key==='/'&&!/INPUT|TEXTAREA/.test(document.activeElement.tagName)){ev.preventDefault();inp&&inp.focus()}if(ev.key==='Escape')document.body.classList.remove('megaopen')});
  addEventListener('scroll',function(){document.body.classList.toggle('scrolled',scrollY>600)},{passive:true});
  // prefill search page from ?q=
  var bq=document.querySelector('.bigsearch'),m=location.search.match(/[?&]q=([^&]+)/);if(bq&&m){bq.value=decodeURIComponent(m[1].replace(/\+/g,' '));bq.dispatchEvent(new Event('input'))}
 });
})();
// ---- Sounds: local file, curated Wikimedia Commons recording, or search on demand ----
(function(){
 var API='https://commons.wikimedia.org/w/api.php?action=query&format=json&origin=*&generator=search&gsrnamespace=6&gsrlimit=8&prop=imageinfo&iiprop=url&gsrsearch=';
 var BAD=/pronunc|^File:(En|De|Fr|Nl|Es|It|Ru|Ja|Zh|Pl|Sv|LL)-|LL-Q|Wikipedia|spoken|\.mid$/i;
 function find(q){return fetch(API+encodeURIComponent('filetype:audio '+q)).then(function(r){return r.json()}).then(function(j){
   var ps=j&&j.query?Object.values(j.query.pages):[];ps.sort(function(a,b){return (a.index||0)-(b.index||0)});
   return ps.filter(function(p){return p.imageinfo&&!BAD.test(p.title)}).map(function(p){return {url:p.imageinfo[0].url,page:p.imageinfo[0].descriptionurl,title:p.title.replace(/^File:/,'')}})}).catch(function(){return []})}
 function player(box,items,auto){
   var it=items[0];
   box.innerHTML='<button class="sbtn">▶ Play sound</button><span class="eq" hidden><i></i><i></i><i></i><i></i></span><div class="sinfo">'+it.title.replace(/</g,'&lt;')+' · <a href="'+it.page+'" target="_blank" rel="noopener">source &amp; licence</a>'+(items.length>1?' · <a href="#" class="snext">try another recording ('+(items.length-1)+')</a>':'')+'</div><audio preload="none" src="'+it.url+'"></audio>';
   var a=box.querySelector('audio'),b=box.querySelector('.sbtn'),eq=box.querySelector('.eq');
   b.onclick=function(){if(a.paused){a.play()}else{a.pause()}};
   a.onplay=function(){b.textContent='⏸ Pause';eq.hidden=false};a.onpause=a.onended=function(){b.textContent='▶ Play sound';eq.hidden=true};
   var nx=box.querySelector('.snext');if(nx)nx.onclick=function(ev){ev.preventDefault();player(box,items.slice(1).concat([items[0]]),true)};
   if(auto){var pr=a.play();if(pr&&pr.catch)pr.catch(function(){b.textContent='🔊 Tap to hear'})}
 }
 function none(box,q){var space=(box.dataset.kind||'')!=='species';box.innerHTML='<span class="sinfo">🔇 No open recording found for this '+(box.dataset.kind||'species')+' yet. '+(space?'Space is a vacuum, so \'sounds\' of space are radio, plasma or data converted to audio (sonifications), and many objects have none yet. ':'Many fish and invertebrates are quiet or have never been recorded. ')+'<a href="#" class="sfind">Search more widely</a> · '+(space?'<a href="https://chandra.harvard.edu/sound/" target="_blank" rel="noopener">NASA Chandra sonifications</a>':'<a href="https://dosits.org/galleries/audio-gallery/" target="_blank" rel="noopener">Ocean sound gallery (DOSITS)</a>')+'</span>';
   box.querySelector('.sfind').onclick=function(ev){ev.preventDefault();box.innerHTML='<span class="sinfo">Searching…</span>';find(q.split(' ').slice(0,2).join(' ')).then(function(r){r.length?player(box,r,true):(box.innerHTML='<span class="sinfo">Still nothing found.</span>')})}}
 function init(box,auto){
   var local=box.dataset.local,q=box.dataset.sound||'',name=box.dataset.name;
   var tryLocal=local?fetch(local,{method:'HEAD'}).then(function(r){return r.ok?[{url:local,page:local,title:'Recording'}]:[]}).catch(function(){return []}):Promise.resolve([]);
   tryLocal.then(function(l){if(l.length)return player(box,l,auto);
     if(!q&&!box.dataset.vocal){box.innerHTML='<button class="sbtn ghost">🔊 Look for a recording</button>';box.querySelector('.sbtn').onclick=function(){box.innerHTML='<span class="sinfo">Searching Wikimedia Commons…</span>';find(name).then(function(r){r.length?player(box,r,true):none(box,name)})};return}
     box.innerHTML='<span class="sinfo">Loading sound…</span>';
     find(q||name).then(function(r){r.length?player(box,r,auto):none(box,name)})});
 }
 document.addEventListener('DOMContentLoaded',function(){
   var b=document.querySelector('.soundbox[data-name]');if(b)init(b,true);
   [].forEach.call(document.querySelectorAll('button.cardsnd'),function(btn){btn.onclick=function(ev){ev.preventDefault();ev.stopPropagation();
     btn.textContent='…';find(btn.dataset.sound).then(function(r){if(!r.length){btn.textContent='🔇';return}var a=new Audio(r[0].url);a.play();btn.textContent='⏸';a.onended=function(){btn.textContent='🔊'};btn.onclick=function(e){e.preventDefault();e.stopPropagation();if(a.paused){a.play();btn.textContent='⏸'}else{a.pause();btn.textContent='🔊'}}})}});
 });
})();
// open the tracker by default on wide screens only (home page)
document.addEventListener('DOMContentLoaded',function(){var t=document.querySelector('details.trackbar[data-openwide]');});
// ---- Paper PDFs: use the copy hosted on this site when available, else the publisher/arXiv PDF ----
document.addEventListener('DOMContentLoaded',function(){
 var b=document.querySelector('.paperbox');if(!b)return;
 var local=b.dataset.local,src=b.dataset.src,note=b.querySelector('.pbnote'),fr=b.querySelector('.pbframe'),view=b.querySelector('.pbview');
 fetch(local,{method:'HEAD'}).then(function(r){
  if(r.ok&&(r.headers.get('content-type')||'').indexOf('pdf')>-1){
   var op=b.querySelector('.pbopen');op.href=local;op.hidden=false;op.target='_blank';op.textContent='↗ Open PDF in new tab';var dl=b.querySelector('.pbdl');dl.href=local;dl.hidden=false;dl.setAttribute('download','');dl.textContent='⬇ Download PDF';dl.removeAttribute('target');
   view.hidden=false;note.innerHTML='✅ An openly licensed copy is hosted on this site, so you can read it below or download it.';
   view.onclick=function(){fr.hidden=!fr.hidden;if(!fr.src)fr.src=local+'#view=FitH';view.textContent=fr.hidden?'📖 Read here':'✖ Close reader'};
   if(innerWidth>900){fr.src=local+'#view=FitH';fr.hidden=false;view.textContent='✖ Close reader'}
  } else note.innerHTML=src?'The PDF opens from the publisher or arXiv. Openly licensed papers are mirrored here automatically by the repository\'s <i>Fetch open-access papers</i> workflow.':'No free PDF is available; use the publisher page (your library may have access).';
 }).catch(function(){note.textContent=''});
});
