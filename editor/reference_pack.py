"""Reusable compositions and provenance from the Def9pj5TWtA reference reel.

Source code for generated library scenes; visual approximation is explicit metadata.
These compositions accept actual local media. They do not generate subject masks.
"""

SOURCE = "examples/igexport-Def9pj5TWtA.mp4"

REFERENCE_EFFECTS = [
    ("orbit", "orbit", 0.07), ("couch wall", "couch-wall", 0.90),
    ("ui world", "ui-world", 1.62), ("frame break", "frame-break", 2.69),
    ("digital zoom", "digital-zoom", 3.50), ("phone mockup", "phone-mockup", 4.59),
    ("checklist", "checklist", 5.41), ("headline wall", "headline-wall", 6.36),
    ("zoom-through cut", "zoom-through", 7.40), ("chart grow", "chart-grow", 8.77),
    ("pull-back reveal", "pull-back", 9.51), ("green screen", "green-screen", 10.74),
    ("paper cut", "paper-cut", 11.70), ("doodle boil", "doodle-boil", 12.80),
    ("vertigo", "vertigo", 13.98), ("cover story", "cover-story", 14.73),
    ("glass type", "glass-type", 15.68),
]

HELPERS = r"""
    const stage = document.getElementById('stage');
    const stageDuration = Number(stage.dataset.duration);
    const $ = selector => document.querySelector(selector);
    const all = selector => Array.from(document.querySelectorAll(selector));
    function assert(ok, message) { if (!ok) throw new Error(message); }
    function finite(n) { return typeof n === 'number' && Number.isFinite(n); }
    function make(tag, cls, value) {
      const el = document.createElement(tag); el.className = cls;
      if (value !== undefined) el.textContent = String(value);
      return el;
    }
    function mount(parent, asset, timing = {}) {
      if (!asset) return null;
      const config = typeof asset === 'string' ? {src:asset} : asset;
      assert(typeof config.src === 'string' && config.src.length > 0, 'Media needs src');
      assert(!config.src.startsWith('@'), 'Resolve media handles with editor stockpile --output or the EDL adapter');
      const isVideo = config.kind === 'video' || /\.(mp4|mov|webm)(?:\?|$)/i.test(config.src);
      const el = document.createElement(isVideo ? 'video' : 'img');
      el.src = config.src; el.alt = config.alt || '';
      Object.assign(el.style,{width:'100%',height:'100%',objectFit:config.fit || 'cover',display:'block'});
      el.dataset.start = String(timing.start ?? 0);
      el.dataset.duration = String(timing.duration ?? stageDuration);
      if (isVideo) {
        el.muted = true; el.playsInline = true;
        el.dataset.mediaStart = String(config.mediaStart ?? 0);
      }
      parent.append(el); return el;
    }
    function exit(tl, target, lead=0.25) {
      tl.to(target,{opacity:0,y:-12,duration:lead,ease:'power2.in'},stageDuration-lead-0.05);
    }
"""


def scene(slug, title, duration, variables, html, css, binding, animation, *,
          cutout=False, assets=(), notes="", aliases=(), zone="top"):
    return {"slug": slug, "shortcut": "@"+slug, "rule": "Reference Pack Def9pj5TWtA",
            "title": title, "duration": duration, "sfx": "", "requires_cutout": cutout,
            "top_zone": zone == "top", "default_vars": variables, "body_html": '<div id="stockpile-root">'+html+'</div>',
            "extra_css": "#stockpile-root{position:absolute;inset:0}"+css, "binding_js": HELPERS+binding, "gsap_js": animation.replace("exit(tl,'#stage')", "exit(tl,'#stockpile-root')"),
            "pack": "reference-def9pj5twta", "required_media_variables": list(assets),
            "min_duration_sec": {"chart-grow":2.6,"glass-type":2.2,"couch-wall":1.6,"cover-story":1.3}.get(slug,1.0),
            "aliases": list(aliases), "fidelity_notes": notes,
            "occupies_zones": [zone], "reference": SOURCE}


REFERENCE_SPECS = [
    scene("couch-wall", "Layered reel wall behind a seated subject", 3.0,
          {"cards": [], "subjectAsset": "", "heading": "Your work, in context", "spread": 1.0},
          '<div id="wall" class="wall"></div><div id="subject" class="subject"></div><div id="wall-heading" class="wall-heading"></div>',
          '''.wall{position:absolute;left:4%;top:10%;width:92%;height:52%;display:grid;grid-template-columns:repeat(3,1fr);gap:24px;perspective:1600px}
          .wall-card{height:100%;min-height:0;overflow:hidden;border-radius:22px;border:3px solid #FFFFFF55;background:#102323;box-shadow:0 18px 48px #0008;opacity:0}
          .subject{position:absolute;inset:0;z-index:2}.subject img,.subject video{object-fit:contain!important}
          .wall-heading{position:absolute;left:8%;right:8%;top:70%;text-align:center;color:#FFF;font-size:68px;font-weight:800;text-shadow:0 6px 20px #000;z-index:3}''',
          r"""
    assert(Array.isArray(vars.cards) && vars.cards.length <= 9,'cards must contain at most 9 media entries');
    assert(finite(vars.spread) && vars.spread>=0.5 && vars.spread<=1.5,'spread must be 0.5..1.5');
    vars.cards.forEach((asset,i)=>{const card=make('div','wall-card');card.style.transform='rotate('+(i%2?3:-3)+'deg)';mount(card,asset);$('#wall').append(card);});
    $('#wall').style.transform='scale('+vars.spread+')';
    $('#wall').style.gridTemplateRows='repeat('+Math.max(1,Math.ceil(vars.cards.length/3))+',1fr)';
    mount($('#subject'),vars.subjectAsset);$('#wall-heading').textContent=vars.heading;
""",
          """tl.fromTo('.wall-card',{opacity:0,y:60,rotationY:-12},{opacity:1,y:0,rotationY:0,duration:0.42,stagger:0.06,ease:'power3.out'},0)
      .fromTo('#wall-heading',{opacity:0,y:20},{opacity:1,y:0,duration:0.3},0.25);exit(tl,'#stage');""",
          cutout=True, assets=("cards", "subjectAsset"), zone="background",
          notes="Real media cards and a supplied alpha subject. Does not segment people or generate missing background pixels."),

    scene("chart-grow", "Data-backed animated line chart", 3.0,
          {"title":"Example data", "labels":["Mon","Tue","Wed","Thu","Fri"],
           "values":[10,20,16,35,48], "unit":"units", "accent":"#F6E478", "yPercent":14},
          '<div id="chart" class="chart"><div id="chart-title"></div><svg id="plot" viewBox="0 0 900 520" role="img" aria-label="Animated data chart"></svg></div>',
          '''.chart{position:absolute;left:7%;width:86%;top:14%;background:#101716ed;border:2px solid #FFFFFF30;border-radius:26px;padding:34px;box-shadow:0 20px 60px #0008}
          #chart-title{font-size:42px;font-weight:800;color:#F0EADE;margin-bottom:20px}#plot{width:100%;height:auto;display:block}''',
          r"""
    assert(Array.isArray(vars.values)&&vars.values.length>=2&&vars.values.length<=12&&vars.values.every(finite),'values needs 2..12 finite numbers');
    assert(Array.isArray(vars.labels)&&vars.labels.length===vars.values.length,'One label per value required');
    assert(finite(vars.yPercent)&&vars.yPercent>=5&&vars.yPercent<=55,'yPercent must be 5..55');
    $('#chart-title').textContent=vars.title;$('#chart').style.top=vars.yPercent+'%';
    const svg=$('#plot'),ns='http://www.w3.org/2000/svg';
    function svgEl(tag,attrs,text){const el=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,String(v)));if(text!==undefined)el.textContent=text;svg.append(el);return el;}
    const min=Math.min(0,...vars.values),max=Math.max(0,...vars.values),span=max-min||1;
    const points=vars.values.map((v,i)=>[90+i*760/(vars.values.length-1),410-(v-min)/span*340]);
    [0,0.5,1].forEach(f=>{const y=410-f*340;svgEl('line',{x1:90,x2:850,y1:y,y2:y,stroke:'#FFFFFF24'});svgEl('text',{x:76,y:y+7,fill:'#F0EADE','font-size':23,'text-anchor':'end'},String(Math.round((min+f*span)*100)/100));});
    vars.labels.forEach((v,i)=>svgEl('text',{x:points[i][0],y:455,fill:'#F0EADE','font-size':Math.max(17,26-vars.labels.length/3),'text-anchor':'middle'},v));
    svgEl('text',{x:90,y:505,fill:'#F0EADE','font-size':24},vars.unit);
    const line=svgEl('path',{id:'growth-line',d:points.map((p,i)=>(i?'L':'M')+p.join(',')).join(' '),fill:'none',stroke:vars.accent,'stroke-width':7,'stroke-linecap':'round','stroke-linejoin':'round'});
    const length=line.getTotalLength();line.style.strokeDasharray=String(length);line.style.strokeDashoffset=String(length);
    points.forEach((p,i)=>svgEl('circle',{class:'data-dot',cx:p[0],cy:p[1],r:8,fill:vars.accent,opacity:0}));
""",
          """tl.fromTo('#chart',{opacity:0,y:26},{opacity:1,y:0,duration:0.3},0)
      .to('#growth-line',{strokeDashoffset:0,duration:1.65,ease:'none'},0.35)
      .to('.data-dot',{opacity:1,duration:0.1,stagger:1.65/(vars.values.length-1)},0.35);exit(tl,'#chart');""",
          notes="Chart geometry follows explicit values, labels and units. Defaults are labeled example data, never inferred performance metrics."),

    scene("cover-story", "Magazine masthead behind subject with cover furniture", 3.0,
          {"masthead":"EDIT", "subjectAsset":"", "backgroundAsset":"", "issue":"ISSUE 01",
           "coverLine":"A story worth sharing", "accent":"#D4AF37", "mastheadY":16},
          '<div id="cover-bg" class="cover-layer"></div><div id="masthead"></div><div id="cover-person" class="cover-layer"></div><div id="cover-front"><span id="issue"></span><span id="cover-line"></span><svg id="barcode" viewBox="0 0 160 80" aria-label="Decorative cover barcode"></svg></div>',
          '''.cover-layer{position:absolute;inset:0}.cover-layer img,.cover-layer video{object-fit:contain!important}
          #masthead{position:absolute;left:5%;right:5%;top:16%;text-align:center;font-family:Georgia,serif;font-size:270px;letter-spacing:-0.05em;color:#F4F4F2;z-index:1}
          #cover-person{z-index:2}#cover-front{position:absolute;inset:8% 6% 10%;border:4px solid #D4AF37;z-index:3;opacity:0}
          #issue{position:absolute;left:24px;top:24px;font-size:28px;color:#F0EADE}#cover-line{position:absolute;left:28px;right:28px;bottom:140px;font-family:Georgia,serif;font-size:70px;line-height:1.08;color:#FFF;text-shadow:0 5px 16px #000}
          #barcode{position:absolute;left:28px;bottom:30px;width:160px;height:80px;background:#FFF;padding:8px}''',
          r"""
    assert(typeof vars.masthead==='string'&&vars.masthead.length>0&&vars.masthead.length<=24,'masthead needs 1..24 characters');
    mount($('#cover-bg'),vars.backgroundAsset);mount($('#cover-person'),vars.subjectAsset);
    $('#masthead').textContent=vars.masthead;$('#masthead').style.top=vars.mastheadY+'%';
    $('#masthead').style.fontSize=Math.min(270,1500/vars.masthead.length)+'px';
    $('#issue').textContent=vars.issue;$('#cover-line').textContent=vars.coverLine;$('#cover-front').style.borderColor=vars.accent;
    const ns='http://www.w3.org/2000/svg';let bx=0;for(let i=0;i<34;i++){const rect=document.createElementNS(ns,'rect');const width=1+(i*7%3);rect.setAttribute('x',bx);rect.setAttribute('width',width);rect.setAttribute('height',64);rect.setAttribute('fill','#161616');$('#barcode').append(rect);bx+=width+2;}
""",
          """tl.fromTo('#masthead',{opacity:0,y:35},{opacity:1,y:0,duration:0.35,ease:'power3.out'},0)
      .to('#cover-front',{opacity:1,duration:0.3},0.2);exit(tl,'#stage');""",
          cutout=True, assets=("subjectAsset",), aliases=("magazine cover",),
          notes="Actual behind/foreground/front layers with supplied aligned alpha media. Barcode is decorative. Does not create segmentation masks."),

    scene("glass-type", "Translucent embossed display type", 2.6,
          {"text":"DESIGN", "yPercent":25, "tint":"#EAF2FF", "subjectAsset":"", "fontSize":210},
          '<div id="glass-word" class="glass-word"></div><div id="glass-person" class="glass-person"></div>',
          '''.glass-word{position:absolute;left:6%;right:6%;top:25%;font-size:210px;font-weight:900;letter-spacing:-0.05em;text-align:center;line-height:1.1;color:#FFFFFF12;-webkit-text-stroke:2px #EAF2FF99;text-shadow:2px 3px 2px #FFF8,-3px -2px 2px #0008,10px 18px 24px #0005;filter:drop-shadow(0 2px 2px #FFF5);opacity:0}
          .glass-person{position:absolute;inset:0;z-index:2}.glass-person img,.glass-person video{object-fit:contain!important}''',
          r"""
    assert(typeof vars.text==='string'&&vars.text.length>0&&vars.text.length<=32,'text needs 1..32 characters');
    assert(finite(vars.fontSize)&&vars.fontSize>=40&&vars.fontSize<=360,'fontSize must be 40..360');
    $('#glass-word').textContent=vars.text;$('#glass-word').style.top=vars.yPercent+'%';
    $('#glass-word').style.fontSize=Math.min(vars.fontSize,1550/vars.text.length)+'px';
    $('#glass-word').style.webkitTextStrokeColor=vars.tint;mount($('#glass-person'),vars.subjectAsset);
""",
          """tl.fromTo('#glass-word',{opacity:0,scale:1.15,filter:'blur(9px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:0.45,ease:'power3.out'},0)
      .to('#glass-word',{y:-8,duration:1.4,ease:'sine.inOut'},0.45);exit(tl,'#glass-word');""",
          notes="Embossed/translucent CSS treatment, not physically accurate background refraction. Optional alpha subject creates depth."),

    scene("checklist", "Timed glass task checklist with progress", 3.0,
          {"title":"A clear workflow", "items":["Choose the take","Add visual proof","Review the reel"],
           "completeTimes":[0.6,1.2,1.8], "accent":"#F6E478", "yPercent":16},
          '<div id="check-card"><div class="check-heading"><span id="check-title"></span><span id="check-count"></span></div><div id="check-items"></div><div class="check-track"><div id="check-progress"></div></div></div>',
          '''#check-card{position:absolute;left:8%;right:8%;top:16%;border:2px solid #FFFFFF35;border-radius:26px;padding:30px;background:#101614ed;box-shadow:0 18px 60px #0008;opacity:0}
          .check-heading{display:flex;justify-content:space-between;gap:24px;color:#F0EADE;font-size:24px;letter-spacing:0.03em;margin-bottom:28px}
          .task-row{display:flex;gap:24px;align-items:center;min-height:86px;color:#FFF;font-size:38px;opacity:0.48}.task-circle{flex-shrink:0;width:38px;height:38px;border:2px solid #FFFFFF70;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:26px}
          .task-check{opacity:0}.check-track{height:5px;background:#FFFFFF20;margin-top:26px}#check-progress{height:100%;width:100%;transform:scaleX(0);transform-origin:left center;background:#F6E478}''',
          r"""
    assert(Array.isArray(vars.items)&&vars.items.length>0&&vars.items.length<=8,'items needs 1..8 labels');
    assert(Array.isArray(vars.completeTimes)&&vars.completeTimes.length===vars.items.length,'One completion time per item required');
    assert(vars.completeTimes.every((t,i)=>finite(t)&&t>=0.3&&t<stageDuration-0.3&&(i===0||t>vars.completeTimes[i-1])),'Completion times must increase within the hold interval');
    $('#check-title').textContent=vars.title;$('#check-count').textContent='0 of '+vars.items.length;$('#check-card').style.top=vars.yPercent+'%';$('#check-progress').style.background=vars.accent;
    vars.items.forEach((label,i)=>{const row=make('div','task-row');row.id='task-'+i;const circle=make('span','task-circle');circle.id='tick-'+i;circle.append(make('span','task-check','✓'));row.append(circle,make('span','task-label',label));$('#check-items').append(row);});
""",
          """tl.fromTo('#check-card',{opacity:0,y:30},{opacity:1,y:0,duration:0.3,ease:'power3.out'},0);
      vars.completeTimes.forEach((time,i)=>{tl.set('#task-'+i,{opacity:1},time).set('#tick-'+i,{backgroundColor:vars.accent,color:'#121414'},time).set('#tick-'+i+' .task-check',{opacity:1},time)
        .set('#check-count',{textContent:(i+1)+' of '+vars.items.length},time).to('#check-progress',{scaleX:(i+1)/vars.items.length,duration:0.15},time);});exit(tl,'#check-card');""",
          notes="In-player or standalone task checklist; distinct from the effect-index HUD. Completion times are explicit composition-local seconds."),

    scene("proof-player", "Synchronized media proof player, counter and effect index", 4.5,
          {"title":"Show the effect", "sequence":[
              {"label":"First effect","start":0.3,"duration":1.2,"src":""},
              {"label":"Second effect","start":1.5,"duration":1.2,"src":""},
              {"label":"Third effect","start":2.7,"duration":1.2,"src":""}], "accent":"#F6E478"},
          '<div id="proof-title"></div><div id="proof-left" class="proof-list"></div><div id="proof-right" class="proof-list"></div><div id="proof-player"><div id="proof-screen"></div><div id="proof-counter"></div><div class="proof-track"><div id="proof-progress"></div></div></div>',
          '''#proof-title{position:absolute;left:12%;right:12%;top:10%;font-size:66px;font-weight:850;line-height:1.04;text-align:center;color:#FFF;text-shadow:0 5px 18px #000;opacity:0}
          .proof-list{position:absolute;top:23%;width:27%;background:#141815c9;border:1px solid #FFFFFF25;padding:18px;border-radius:20px;display:flex;flex-direction:column;gap:10px}
          #proof-left{left:3%}#proof-right{right:3%}.proof-row{font-size:25px;font-weight:650;color:#FFF;opacity:0.44;line-height:1.18}.proof-number{font-size:20px;margin-right:8px;font-variant-numeric:tabular-nums}
          #proof-player{position:absolute;left:31%;top:45%;width:38%;height:38%;border:4px solid #F0EADE;border-radius:32px;overflow:hidden;background:#0D1518;box-shadow:0 20px 60px #0008;opacity:0}
          #proof-screen{position:absolute;inset:0}.proof-pane{position:absolute;inset:0;opacity:0}#proof-counter{position:absolute;top:16px;left:16px;z-index:3;background:#101614df;color:#FFF;font-size:24px;padding:8px 14px;border-radius:30px;font-variant-numeric:tabular-nums}
          .proof-track{position:absolute;bottom:0;left:0;right:0;height:6px;background:#FFFFFF30;z-index:3}#proof-progress{height:100%;background:#F6E478;transform:scaleX(0);transform-origin:left}''',
          r"""
    assert(Array.isArray(vars.sequence)&&vars.sequence.length>0&&vars.sequence.length<=20,'sequence needs 1..20 entries');
    vars.sequence.forEach((e,i)=>{assert(typeof e.label==='string'&&finite(e.start)&&finite(e.duration)&&e.start>=0&&e.duration>0&&e.start+e.duration<=stageDuration-0.3,'Invalid sequence timing/label');if(i)assert(e.start>=vars.sequence[i-1].start+vars.sequence[i-1].duration,'Sequence entries overlap');});
    $('#proof-title').textContent=vars.title;$('#proof-counter').textContent='';$('#proof-progress').style.background=vars.accent;
    vars.sequence.forEach((e,i)=>{const row=make('div','proof-row');row.id='proof-row-'+i;row.append(make('span','proof-number',String(i+1).padStart(2,'0')),make('span','proof-label',e.label));$(i<Math.ceil(vars.sequence.length/2)?'#proof-left':'#proof-right').append(row);
      const pane=make('div','proof-pane');pane.id='proof-pane-'+i;const asset=e.src?{src:e.src,mediaStart:e.mediaStart??0,kind:e.kind}:null;mount(pane,asset,{start:e.start,duration:e.duration});$('#proof-screen').append(pane);});
    if(vars.sequence[0].start===0){$('#proof-counter').textContent='1/'+vars.sequence.length;Object.assign($('#proof-row-0').style,{opacity:'1',color:vars.accent});$('#proof-pane-0').style.opacity='1';}
""",
          """const intro=Math.min(0.3,vars.sequence[0].start);tl.fromTo('#proof-title,#proof-player,.proof-list',{opacity:intro?0:1,y:intro?20:0},{opacity:1,y:0,duration:Math.max(0.0001,intro),ease:'power3.out'},0);
      vars.sequence.forEach((e,i)=>{const stop=e.start+e.duration;
        tl.set('#proof-pane-'+i,{opacity:1},e.start).set('#proof-pane-'+i,{opacity:0},stop)
          .set('#proof-row-'+i,{opacity:1,color:vars.accent},e.start).set('#proof-row-'+i,{opacity:0.44,color:'#FFFFFF'},stop)
          .set('#proof-counter',{textContent:(i+1)+'/'+vars.sequence.length},e.start).set('#proof-counter',{textContent:''},stop)
          .fromTo('#proof-progress',{scaleX:0},{scaleX:1,duration:e.duration,ease:'none',immediateRender:false},e.start).set('#proof-progress',{scaleX:0},stop);});exit(tl,'#stage');""",
          assets=("sequence",), aliases=("showcase player", "effect showcase"), zone="center",
          notes="One sequence drives visible clip, highlighted row, counter and progress. Main presenter remains the base video; child clips use their own local media offsets. Not a phone screen recording generator."),

    scene("profile-card", "Screenshot-backed social profile CTA", 2.8,
          {"profileAsset":"", "creatorHandle":"yourhandle", "cta":"Follow for more", "yPercent":46, "widthPercent":48},
          '<div id="profile-cta"></div><div id="profile-card"><div id="profile-media"></div><div id="profile-handle"></div></div>',
          '''#profile-cta{position:absolute;top:12%;left:10%;right:10%;text-align:center;font-size:68px;font-weight:850;color:#FFF;text-shadow:0 6px 20px #000;opacity:0}
          #profile-card{position:absolute;top:46%;left:26%;width:48%;height:37%;border:2px solid #FFFFFF70;border-radius:26px;background:#111;overflow:hidden;box-shadow:0 20px 60px #0009;opacity:0}
          #profile-media{position:absolute;inset:0 0 58px}#profile-handle{position:absolute;left:12px;right:12px;bottom:14px;color:#FFF;font-size:24px;text-align:center}''',
          r"""
    assert(finite(vars.widthPercent)&&vars.widthPercent>=25&&vars.widthPercent<=80,'widthPercent must be 25..80');
    mount($('#profile-media'),vars.profileAsset);$('#profile-handle').textContent='@'+vars.creatorHandle.replace(/^@/,'');$('#profile-cta').textContent=vars.cta;
    Object.assign($('#profile-card').style,{width:vars.widthPercent+'%',left:(100-vars.widthPercent)/2+'%',top:vars.yPercent+'%'});
""",
          """tl.fromTo('#profile-cta',{opacity:0,y:16},{opacity:1,y:0,duration:0.25},0)
      .fromTo('#profile-card',{opacity:0,y:45,scale:0.94},{opacity:1,y:0,scale:1,duration:0.35,ease:'power3.out'},0.15);exit(tl,'#stage');""",
          assets=("profileAsset",), zone="center",
          notes="Uses a supplied profile screenshot; does not invent follower counts, follow users, or send DMs."),
]
