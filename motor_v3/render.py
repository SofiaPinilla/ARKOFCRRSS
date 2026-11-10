import json, sys, base64, subprocess, os, time
from playwright.sync_api import sync_playwright
def open_page(p):
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--disable-gpu','--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file:///home/claude/eng/engine.html')
    pg.evaluate("document.fonts.load('100px Anton')"); pg.evaluate("document.fonts.load('italic 800 60px BarlowC')")
    pg.evaluate("document.fonts.ready.then(()=>1)")
    return b, pg
def stills(spec, tl, times, out):
    with sync_playwright() as p:
        b, pg = open_page(p)
        pg.evaluate("([s,t])=>init(s,t)", [spec, tl])
        for t in times:
            d = pg.evaluate("t=>{draw(t);return document.getElementById('c').toDataURL('image/jpeg',0.9)}", t)
            open(f"{out}_{t:05.2f}.jpg", 'wb').write(base64.b64decode(d.split(',')[1]))
        b.close()
def video(spec, tl, out, fps=30, tag=''):
    n = int(round(tl['total'] * fps))
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    t0 = time.time()
    with sync_playwright() as p:
        b, pg = open_page(p)
        pg.evaluate("([s,t])=>init(s,t)", [spec, tl])
        for i in range(n):
            d = pg.evaluate("t=>{draw(t);return document.getElementById('c').toDataURL('image/jpeg',0.93)}", i / fps)
            ff.stdin.write(base64.b64decode(d.split(',')[1]))
        b.close()
    ff.stdin.close(); ff.wait()
    print(tag, 'frames', n, 'in', round(time.time() - t0, 1), 's', flush=True)
