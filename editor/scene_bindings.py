"""Parameter bindings for the experimental catalogue; generated into each scene.

These bindings make demo content editable. They do not certify subject extraction,
source-video transitions, or production compositing for every advertised shortcut.
"""

COMMON = r"""
    function text(selector, value) {
      document.querySelectorAll(selector).forEach(el => {
        el.textContent = String(value ?? ''); el.style.whiteSpace = 'pre-line';
      });
    }
    function style(selector, values) {
      document.querySelectorAll(selector).forEach(el => Object.assign(el.style, values));
    }
    function items(selector, values, tag, cls) {
      const parent = document.querySelector(selector); if (!parent) return;
      parent.replaceChildren(...values.map(value => {
        const el = document.createElement(tag); el.className = cls;
        el.textContent = String(value); return el;
      }));
    }
    function media(selector, value) {
      if (!value || value.startsWith('@')) return;
      document.querySelectorAll(selector).forEach(parent => {
        parent.style.position ||= 'relative';
        const video = /\.(mp4|mov|webm)(?:\?|$)/i.test(value);
        const el = document.createElement(video ? 'video' : 'img');
        el.src = value; el.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;';
        if (video) { el.muted = true; el.setAttribute('playsinline',''); el.dataset.start='0'; el.dataset.duration=document.querySelector('#stage').dataset.duration; }
        if (parent.id==='stage') parent.prepend(el); else parent.replaceChildren(el);
      });
    }
    function foreground(value) {
      if (!value || value.startsWith('@')) return;
      let parent = document.getElementById('subject-layer');
      if (!parent) { parent = document.createElement('div'); parent.id='subject-layer';
        parent.style.cssText='position:absolute;inset:0;pointer-events:none;z-index:2;';
        document.getElementById('stage').append(parent); }
      media('#subject-layer', value);
    }
    Object.keys(vars).forEach(key => {
      if (typeof vars[key] === 'string' && /^[\[{]/.test(vars[key])) {
        try { vars[key] = JSON.parse(vars[key]); } catch (_) {}
      }
    });
"""

BINDINGS = {
    "effect-hud": """text('#num', vars.headerNumber); text('#ttl', vars.headerTitle);
items('#col-left',vars.itemsLeft,'div','item'); items('#col-right',vars.itemsRight,'div','item');
document.querySelectorAll('.item')[Math.max(0,vars.activeIndex-1)]?.classList.add('active');
if (vars.theme==='sidebar-green') { style('.hud-cols',{justifyContent:'flex-end'});style('#col-left',{display:'none'});style('.hud-panel',{background:'#123024',width:'48%'}); }
""",
    "keyword-captions": """
text('#l1',vars.line1);text('#l2',vars.keyword);style('#kw',{top:vars.yPercent+'%'});
if(vars.theme==='white-pill-stack') { style('#l1,#l2',{background:'#F6F0E4',color:'#141413',padding:'12px 24px',borderRadius:'18px',textShadow:'none'}); }
""",
    "headline-wall": """
text('#c4 .kicker',vars.kicker);text('#c4 .serif-line:not(.hl-wrap)',vars.headlineLine1);text('.hl-txt',vars.headlineLine2);
vars.subClippings.forEach((v,i)=>text('#c'+(i+1)+' div',v));
""",
    "zoom-through": "style('#fl',{background:vars.flashColor});",
    "vertigo": "foreground(vars.cutoutHandle);style('#subject-layer',{transform:'scale('+vars.fgScale+')'});",
    "green-screen": "media('#gsw',vars.backgroundVideo);foreground(vars.cutoutHandle);style('#gsw',{boxShadow:'inset 0 0 200px rgba(0,0,0,'+vars.vignetteOpacity+')'});text('.gs-label','');",
    "phone-mockup": "media('.screen-Viewport',vars.screenAsset);text('.poster-title',vars.headline);style('.phone-stage',{left:vars.xPercent+'%',top:vars.yPercent+'%'});if(!vars.deviceFrame.startsWith('@'))style('.phone-card',{backgroundImage:'url('+vars.deviceFrame+')',backgroundSize:'100% 100%'});",
    "digital-zoom": """
text('#zv',vars.startZoom.toFixed(2)+' → '+vars.endZoom.toFixed(2)+'×');items('#lticks',vars.focalLengths,'span','');
style('#lbar',{opacity:vars.style==='lens-ring'?'1':'0'});style('.hud-bottom,.face-box',{display:vars.style==='lens-ring'?'none':''});
""",
    "paper-cut": "items('.ransom-row:first-child',Array.from(vars.word1),'span','chip c1');items('.ransom-row:last-child',Array.from(vars.word2),'span','chip c2');foreground(vars.cutoutHandle);if(!vars.gridTexture.startsWith('@'))style('#stage',{backgroundImage:'url('+vars.gridTexture+')'});",
    "ui-world": "text('.ui-input',vars.promptText);text('.prev-box',vars.previewLabel);",
    "orbit": "document.querySelectorAll('.ocard').forEach((el,i)=>{el.style.transform='rotateY('+(i*90)+'deg) translateZ('+vars.radiusPx+'px)';media('.oc'+(i+1),vars.reelCards[i]);});foreground(vars.cutoutHandle);",
    "frame-break": "text('.handle','@'+vars.handle+' · Follow');text('.rcap',vars.caption);",
    "doodle-boil": "document.querySelectorAll('#dsvg path,#dsvg circle').forEach((el,i)=>el.setAttribute('stroke',vars.colors[i%vars.colors.length]));",
    "sticky-text": "text('.st-num',vars.number);text('.st-txt',vars.label);",
    "before-after": "text('#bal',vars.leftLabel);text('#bar',vars.rightLabel);style('#beam',{background:vars.beamColor});",
    "pull-back": "text('.nle-top',vars.windowTitle);vars.checklist.forEach((v,i)=>text('#ck'+(i+1),'✓ '+v));",
    "depth-scatter": "items('#dsb',Array.from(vars.wordBehind),'span','dl');items('#dsf',Array.from(vars.wordFront),'span','fl');foreground(vars.cutoutHandle);style('#dsf',{zIndex:'3'});",
    "reel-grid": """
items('#rg',Array.from({length:vars.columns*vars.rows},(_,i)=>String(i+1).padStart(2,'0')),'div','rg-card');
style('#rg',{gridTemplateColumns:'repeat('+vars.columns+',1fr)'});
if(vars.mode==='background')style('#rg',{inset:'0',width:'100%',height:'100%'});
(vars.reelAssets.length?vars.reelAssets:vars.thumbAssets).forEach((v,i)=>media('.rg-card:nth-child('+(i+1)+')',v));
""",
    "comment-bubble": "text('#cbt,.cb-user b',vars.keyword);text('.cb-rep-txt',vars.replyText);text('.cb-btn',vars.buttonText);",
    "knockout-captions": "text('.ko-pill',vars.pillText);text('.ko-sub,.ko-header',vars.subText);text('.ko-big',vars.stencilLine1+'\\n'+vars.stencilLine2);",
    "live-markup": """
text('#mkt',vars.label);document.querySelector('#mkt').setAttribute('fill',vars.strokeColor);
document.querySelectorAll('#mka,#mkc').forEach(el=>el.setAttribute('stroke',vars.strokeColor));
const ellipse=document.querySelector('#mkc');ellipse.setAttribute('cx',vars.cx);ellipse.setAttribute('cy',vars.cy);ellipse.setAttribute('rx',vars.rx);ellipse.setAttribute('ry',vars.ry);
""",
    "film-look": "style('#fscan',{background:vars.lineColor});media('#stage',vars.grainOverlay);",
    "jiggle-delete": """
text('#jcnt',vars.apps.length+' apps');const row=document.querySelector('.jd-row');row.replaceChildren();
vars.apps.forEach((app,i)=>{const el=document.createElement('div');el.className='jd-app';el.id='ja'+(i+1);
const ic=document.createElement('div');ic.className='ic';ic.textContent=app.name.slice(0,2);
const nm=document.createElement('div');nm.className='nm';nm.textContent=app.name;el.append(ic,nm);row.append(el);media('#'+el.id+' .ic',app.icon);});
""",
    "screenplay-page": "text('.sp-slug',vars.slugline);text('.sp-char',vars.character);text('.sp-par',vars.parenthetical);text('.sp-hl-wrap b',vars.highlightedLine);",
    "contact-sheet-hook": "text('.cs-t1',vars.title);text('#cst2',vars.subtitle);style('#css',{background:vars.bgHex});items('.cs-grid',Array.from({length:20},(_,i)=>String(i+1).padStart(2,'0')),'div','cs-cell');vars.thumbAssets.forEach((v,i)=>media('.cs-cell:nth-child('+(i+1)+')',v));",
    "keycaps": """
document.querySelectorAll('.kc').forEach(el=>el.remove());const stage=document.querySelector('#stage');
vars.keys.forEach((key,i)=>{const el=document.createElement('div');el.className='kc';const b=document.createElement('b');b.textContent=key;el.append(b);el.style.left=(8+(i%4)*20)+'%';el.style.top=(14+Math.floor(i/4)*11)+'%';stage.append(el);});
""",
    "nle-timeline": "text('.nle-head .tc',vars.timecode);items('.clips-row',Array(vars.clipCount).fill(''),'span','cl');",
    "serif-stamp": "text('#ssp',vars.prefix);items('.ss-word',Array.from(vars.word),'span','sl');",
    "icon-strike": "text('#ist',vars.strikeWord);vars.icons.forEach((v,i)=>media('#ib'+(i+1)+' .ic',v));",
    "grease-pencil": "text('.gp-head',vars.header);style('.gx,.gp-head',{color:vars.strokeColor});",
    "video-card": "text('.vc-h',vars.cardTitle);text('#vcs',vars.chapter2);text('.vc-pane:not(.ed)',vars.chapter1);text('.vc-pane.ed',vars.chapter2);media('.vc-top',vars.previewAsset);",
}


def binding_script(slug):
    return COMMON + BINDINGS[slug].replace("\n+", "\n")
