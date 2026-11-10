import json, sys, subprocess
from PIL import Image
vid=sys.argv[1]; tl=json.load(open(f'out/{vid}_tl.json'))
ts=[]
for s in tl['segs']:
    d=s['t1']-s['t0']
    if s['type']=='play': ts += [s['t0']+d*f for f in (0.15,0.45,0.75,0.95)]
    else: ts += [s['t0']+d*f for f in (0.12,0.5,0.95)]
ims=[]
for t in ts:
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.2f}','-i',f'out/{vid}.mp4','-frames:v','1','-vf','scale=270:-1','/tmp/f.png'])
    ims.append(Image.open('/tmp/f.png').copy())
cols=6; w,h=ims[0].size
g=Image.new('RGB',(w*cols,h*((len(ims)+cols-1)//cols)))
for i,im in enumerate(ims): g.paste(im,((i%cols)*w,(i//cols)*h))
g.save(f'test/sheet_{vid}.png'); print(len(ims))
