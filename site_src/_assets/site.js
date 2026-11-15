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
    var key='wp:'+title, c=null;
    try{c=JSON.parse(localStorage.getItem(key)||'null')}catch(e){}
    if(c&&Date.now()-c.t<7*864e5)return mem[title]=Promise.resolve(c.v);
    return mem[title]=fetch(API+encodeURIComponent(title.replace(/ /g,'_'))+'?redirect=true').then(function(r){return r.ok?r.json():null}).then(function(j){
      var v=null;
      if(j&&j.thumbnail&&j.originalimage&&j.thumbnail.source.indexOf('/wikipedia/commons/')>-1){
        var src=j.originalimage.source, f=decodeURIComponent(src.split('/').pop());
        v={thumb:j.thumbnail.source, orig:src, file:'https://commons.wikimedia.org/wiki/File:'+encodeURIComponent(f), title:j.title};
      }
      try{localStorage.setItem(key,JSON.stringify({t:Date.now(),v:v}))}catch(e){}
      return v;
    }).catch(function(){return null});
  }
  function sized(u,w){return /\/\d+px-/.test(u)?u.replace(/\/\d+px-/,'/'+w+'px-'):u}
  function fill(el){
    var t=el.getAttribute('data-wiki'); if(!t||el.dataset.done)return; el.dataset.done=1;
    get(t).then(function(v){
      if(!v){el.classList.add('nophoto');var tx=el.querySelector('svg text:last-of-type');if(tx)tx.textContent='No open photo yet · prompt in prompts.md';return;}
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
  }
  function status(box){
    var base=(document.querySelector('link[href*="site.css"]').getAttribute('href')||'').replace('site.css','');
    Promise.all([fetch(base+'prompts.json').then(function(r){return r.json()}),fetch(base+'photo-index.json').then(function(r){return r.json()})]).then(function(a){
      var prompts={};a[0].forEach(function(p){prompts[p.save]=p});
      var idx=a[1], missing=[], ok=0, n=0;
      return Promise.all(idx.map(function(e){return get(e.wiki).then(function(v){n++;if(v)ok++;else missing.push(e)})})).then(function(){
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
