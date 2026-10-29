#!/usr/bin/env python3
"""Prepare reproducible effect instances with explicit fixtures; no shared scene edits.

Default fixtures are synthetic. --reference uses the supplied edited reel and an
Apple Vision cutout, whose baked-in captions remain part of the source/matte.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from editor.core import ROOT
from editor.stockpile import instantiate


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default='renders/drafts/stockpile-validation')
    parser.add_argument('--reference',action='store_true')
    parser.add_argument('--replace',action='store_true',help='Replace this validation folder only')
    args=parser.parse_args()
    base=Path(args.output).resolve()
    if not base.is_relative_to((ROOT/'renders').resolve()):
        raise ValueError('Validation output must stay under renders/')
    if base.exists():
        if not args.replace:raise ValueError('Output exists; choose a new directory or --replace')
        if base==(ROOT/'renders').resolve():raise ValueError('Cannot replace renders root')
        if not (base/'.stockpile-validation').is_file():raise ValueError('Refusing to replace a folder not created by this helper')
        shutil.rmtree(base)
    assets=base/'assets';assets.mkdir(parents=True)
    (base/'.stockpile-validation').write_text('Owned synthetic/reference validation artifacts, not production media.\n')
    def run(*arguments):subprocess.run(list(map(str,arguments)),check=True,cwd=ROOT)
    def ff(*arguments):run('ffmpeg','-y','-v','error',*arguments)
    if args.reference:
        source=ROOT/'examples/igexport-Def9pj5TWtA.mp4'
        ff('-ss','17.3','-i',source,'-frames:v','1',assets/'presenter.png')
        run('swift','-module-cache-path',base/'swift-cache',ROOT/'scripts/person_cutout.swift',
            '--input',source,'--start','17.3','--end','17.6','--output',assets/'subject.mov')
        ff('-i',assets/'subject.mov','-frames:v','1',assets/'subject.png')
        ff('-ss','25.8','-i',source,'-vf','crop=294:374:212:618','-frames:v','1',assets/'profile.png')
        for i,time in enumerate([0.5,1.5,5.5,8.5,15.5,16.5]):
            ff('-ss',time,'-i',source,'-vf','crop=230:400:245:570','-frames:v','1',assets/f'card-{i}.png')
        suffix='png'
    else:
        # Vector fixtures are visibly synthetic and avoid a dependency on ASR or Vision.
        (assets/'subject.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920"><ellipse cx="540" cy="650" rx="170" ry="210" fill="#D99A75"/><path d="M180 1800V1200Q180 900 540 900Q900 900 900 1200V1800Z" fill="#405D65"/></svg>')
        (assets/'presenter.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920"><rect width="1080" height="1920" fill="#20312E"/></svg>')
        (assets/'profile.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="600" height="800"><rect width="600" height="800" fill="#172822"/><text x="40" y="100" font-family="sans-serif" font-size="48" fill="white">DEMO PROFILE</text><rect x="40" y="180" width="520" height="300" rx="24" fill="#405D65"/></svg>')
        for i in range(6):
            (assets/f'card-{i}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="270" height="480"><rect width="270" height="480" fill="{["#405D65","#61463F","#345C4B"][i%3]}"/><text x="135" y="250" text-anchor="middle" font-family="sans-serif" font-size="72" fill="white">{i+1}</text></svg>')
        suffix='svg'
    for color in ['red','blue']:
        ff('-f','lavfi','-i',f'color=c={color}:s=270x480:r=30:d=1.5','-c:v','libx264','-pix_fmt','yuv420p',assets/f'{color}.mp4')
    def asset(name):return str(assets/(name+'.'+suffix))
    configs={
        'couch-wall':{'cards':[asset(f'card-{i}') for i in range(6)],'subjectAsset':asset('subject'),'heading':'Selected work'},
        'chart-grow':{'title':'Example: explicit values','labels':['One','Two','Three'],'values':[8,2,6],'unit':'sample units'},
        'cover-story':{'subjectAsset':asset('subject'),'backgroundAsset':asset('presenter'),'masthead':'EDIT','coverLine':'Make your story clear'},
        'glass-type':{'text':'STUDIO','subjectAsset':asset('subject')},
        'checklist':{'title':'REVIEW THE REEL','items':['Choose a take','Show the proof','Check the delivery']},
        'proof-player':{'title':'Proof, in sync','sequence':[
            {'label':'Red clip','start':0.3,'duration':1.2,'src':str(assets/'red.mp4')},
            {'label':'Blue clip','start':1.5,'duration':1.2,'src':str(assets/'blue.mp4')},
            {'label':'Reference still' if args.reference else 'Sample still','start':2.7,'duration':1.2,'src':asset('card-0')}]},
        'profile-card':{'profileAsset':asset('profile'),'creatorHandle':'reference-profile' if args.reference else 'demo-profile','cta':'Follow for more'}
    }
    results=[instantiate(slug,base/slug,variables) for slug,variables in configs.items()]
    results.append(instantiate('proof-player',base/'proof-player-instant',{
        'title':'Immediate proof','sequence':[{'label':'Frame-zero hook','src':str(assets/'red.mp4'),'start':0,'duration':1}]}))
    (base/'instances.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'instances':len(results),'output':str(base),'fixture_type':'edited reference' if args.reference else 'synthetic'}))


if __name__=='__main__':main()
