#!/usr/bin/env node
// Browser regression checks for prepared stockpile instances (no external requests).
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {execFileSync} = require('node:child_process');
const puppeteer = require('puppeteer-core');

const root = path.resolve(process.argv[2] || 'renders/drafts/stockpile-validation');
const browserPath = process.env.CHROME_BIN || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const mime = {'.html':'text/html','.js':'text/javascript','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.mp4':'video/mp4','.mov':'video/quicktime'};
const server = http.createServer((req,res)=>{
  const relative = decodeURIComponent(req.url.split('?')[0]);
  const file = path.resolve(root,'.'+relative);
  if (!file.startsWith(root+path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
    res.writeHead(404);res.end();return;
  }
  const size = fs.statSync(file).size;
  // Chrome can seek the local proof clips through standard range requests.
  if(req.headers.range){
    const match=/bytes=(\d+)-(\d*)/.exec(req.headers.range);
    const start=Number(match[1]),end=match[2]?Number(match[2]):size-1;
    res.writeHead(206,{'Content-Type':mime[path.extname(file)]||'application/octet-stream','Content-Range':`bytes ${start}-${end}/${size}`,'Accept-Ranges':'bytes','Content-Length':end-start+1});
    fs.createReadStream(file,{start,end}).pipe(res);
  } else {
    res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream','Content-Length':size});
    fs.createReadStream(file).pipe(res);
  }
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await puppeteer.launch({executablePath:browserPath,headless:true,args:['--disable-background-networking']});
  const results=[];
  try {
    const scenes=['couch-wall','chart-grow','cover-story','glass-type','checklist','proof-player','profile-card'];
    for(const slug of scenes){
      const page=await browser.newPage();const errors=[];
      page.on('pageerror',error=>errors.push(error.message));
      await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
      const response=await page.goto(`http://127.0.0.1:${server.address().port}/${slug}/index.html`,{waitUntil:'networkidle0'});
      assert.equal(response.status(),200);
      try { await page.waitForFunction(()=>Boolean(window.__timelines?.main),{timeout:10000}); }
      catch(error) { throw new Error(slug+': '+errors.join('; ')+' ' +error.message); }
      const state=await page.evaluate(async()=>{
        const seek=async time=>{
          window.__timelines.main.pause().seek(time,false);
          await Promise.all(Array.from(document.querySelectorAll('video')).map(el=>{
            const start=Number(el.dataset.start||0),duration=Number(el.dataset.duration||Infinity);
            if(time<start||time>=start+duration)return;
            const target=Number(el.dataset.mediaStart||0)+time-start;
            if(Math.abs(el.currentTime-target)<0.002)return;
            return new Promise(resolve=>{el.addEventListener('seeked',resolve,{once:true});el.currentTime=target;});
          }));
        };
        await seek(1.0);
        return {images:Array.from(document.images).map(el=>({loaded:el.complete&&el.naturalWidth>0})),
          count:document.querySelectorAll('video').length,
          title:document.querySelector('#chart-title')?.textContent,
          dots:document.querySelectorAll('.data-dot').length,
          subjectZ:document.querySelector('#cover-person')?getComputedStyle(document.querySelector('#cover-person')).zIndex:null,
          mastheadZ:document.querySelector('#masthead')?getComputedStyle(document.querySelector('#masthead')).zIndex:null};
      });
      assert.equal(errors.length,0,`${slug}: ${errors.join('; ')}`);
      assert(state.images.every(i=>i.loaded),`${slug}: missing media`);
      if(slug==='chart-grow'){assert.equal(state.dots,3);assert.equal(state.title,'Example: explicit values');}
      if(slug==='cover-story')assert(Number(state.subjectZ)>Number(state.mastheadZ));
      if(slug==='proof-player'){
        const states=await page.evaluate(()=>[0.8,1.9,3.3,0.8].map(time=>{
          window.__timelines.main.pause().seek(time,false);
          return {counter:document.querySelector('#proof-counter').textContent,
            rows:Array.from(document.querySelectorAll('.proof-row')).map(el=>Number(getComputedStyle(el).opacity)),
            panes:Array.from(document.querySelectorAll('.proof-pane')).map(el=>Number(getComputedStyle(el).opacity))};
        }));
        for(const [i,state] of states.entries()){
          const expected=[0,1,2,0][i];
          assert.equal(state.counter,`${expected+1}/3`);
          assert.equal(state.rows.filter(v=>v===1).length,1);
          assert.equal(state.panes.filter(v=>v===1).length,1);
          assert.equal(state.rows[expected],1);assert.equal(state.panes[expected],1);
        }
      }
      if(slug==='checklist'){
        const states=await page.evaluate(()=>[0.4,0.8,1.4,2.2,0.8].map(time=>{
          window.__timelines.main.pause().seek(time,false);return {count:document.querySelector('#check-count').textContent,
            ticks:Array.from(document.querySelectorAll('.task-check')).map(el=>Number(getComputedStyle(el).opacity))};
        }));
        assert.deepEqual(states.map(s=>s.count),['0 of 3','1 of 3','2 of 3','3 of 3','1 of 3']);
        assert.deepEqual(states.map(s=>s.ticks),[[0,0,0],[1,0,0],[1,1,0],[1,1,1],[1,0,0]]);
      }
      await page.evaluate(time=>{window.__timelines.main.pause().seek(time,false);},slug==='chart-grow'?2.2:slug==='checklist'?1.4:1.0);
      await page.screenshot({path:path.join(root,slug+'.png'),omitBackground:true});
      const exit=await page.evaluate(()=>{
        const duration=Number(document.querySelector('#stage').dataset.duration);
        window.__timelines.main.pause().seek(duration-0.01,false);
        const target=document.querySelector('#stockpile-root');
        return Number(getComputedStyle(target).opacity);
      });
      // Some effects exit their card rather than the shared wrapper.
      if(['couch-wall','cover-story','proof-player','profile-card'].includes(slug))assert(exit<0.1,slug+': exit failed');
      results.push({effect:slug,status:'passed',media_images:state.images.length,media_videos:state.count});
      await page.close();
    }
    if(fs.existsSync(path.join(root,'proof-player-instant/index.html'))){
      const page=await browser.newPage();
      await page.goto(`http://127.0.0.1:${server.address().port}/proof-player-instant/index.html`,{waitUntil:'networkidle0'});
      const first=await page.evaluate(()=>{
        window.__timelines.main.pause().seek(0,false);
        return {counter:document.querySelector('#proof-counter').textContent,opacity:Number(getComputedStyle(document.querySelector('#proof-player')).opacity)};
      });
      assert.equal(first.counter,'1/1');assert(first.opacity>0.99,'Frame-zero proof should not wait for an intro');
      results.push({effect:'proof-player-frame-zero',status:'passed'});
      await page.close();
    }
    if(process.argv[3]){
      const movie=path.resolve(process.argv[3]);
      const pixel=time=>execFileSync('ffmpeg',['-v','error','-ss',String(time),'-i',movie,'-vf','format=rgb24,crop=1:1:540:1100','-frames:v','1','-f','rawvideo','-']);
      const red=pixel(0.8),blue=pixel(1.9);
      assert(red[0]>180&&red[2]<80,'Expected first actual video clip to be red');
      assert(blue[2]>180&&blue[0]<80,'Expected second actual video clip to be blue');
      results.push({effect:'proof-player-rendered-media',status:'passed',pixels:{first:Array.from(red),second:Array.from(blue)}});
    }
    fs.writeFileSync(path.join(root,'browser-verification.json'),JSON.stringify(results,null,2)+'\n');
    process.stdout.write(JSON.stringify(results,null,2)+'\n');
  } finally {await browser.close();server.close();}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
