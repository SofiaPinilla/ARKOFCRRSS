# Construye un vídeo: corta la toma de voz por párrafos, monta la línea de tiempo, música y render.
import json, sys, os, subprocess, wave
import numpy as np
sys.path.insert(0, '/home/claude/eng')
from render import video

SR = 48000
V = json.load(open('/home/claude/eng/specs.json'))
TAKES = '/home/claude/eng/takes'
OUT = '/home/claude/eng/out'
os.makedirs(OUT, exist_ok=True)

def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def split(x, n, texts):
    hop = int(0.01 * SR)
    fr = len(x) // hop
    rms = np.sqrt(np.mean(x[:fr * hop].reshape(fr, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms / rms.max())
    sil = db < -38
    # speech extent
    sp = np.where(~sil)[0]; s0, s1 = sp[0], sp[-1]
    runs = []; i = s0
    while i <= s1:
        if sil[i]:
            j = i
            while j <= s1 and sil[j]: j += 1
            if j - i >= 18: runs.append((i, j))
            i = j
        else: i += 1
    chars = np.array([len(t) for t in texts], float)
    m = len(runs); K = len(texts) - 1
    tot = s1 - s0; rate0 = tot / chars.sum()
    import functools
    def segcost(a_end, b_start, k):  # segment k spans from a_end to b_start (frames)
        d = max(1, b_start - a_end)
        r = d / chars[k] / rate0
        return 3.0 * np.log(r) ** 2
    @functools.lru_cache(None)
    def best(ri, k):  # boundary k placed at run ri; returns cost of segments k+1.. to end
        st = runs[ri][1]
        if k == K - 1:
            return (segcost(st, s1, k + 1), ())
        res = (1e9, ())
        for rj in range(ri + 1, m):
            c, path = best(rj, k + 1)
            c += segcost(st, runs[rj][0], k + 1) - 0.02 * (runs[rj][1] - runs[rj][0])
            if c < res[0]: res = (c, (rj,) + path)
        return res
    res = (1e9, ())
    for ri in range(m):
        c, path = best(ri, 0)
        c += segcost(s0, runs[ri][0], 0) - 0.02 * (runs[ri][1] - runs[ri][0])
        if c < res[0]: res = (c, (ri,) + path)
    chosen = [runs[r] for r in res[1]]
    clips = []; st = s0
    for (a, b) in chosen:
        clips.append((st * hop, a * hop)); st = b
    clips.append((st * hop, (s1 + 1) * hop))
    return clips, [(b - a) / 100 for a, b in chosen]

def synth_music(dur, bpm=124, seed=1):
    rng = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n, np.float32)
    beat = 60 / bpm
    def add(sig, at):
        i = int(at * SR); j = min(n, i + len(sig))
        if i < n: out[i:j] += sig[:j - i]
    tk = np.arange(int(0.35 * SR)) / SR
    kick = (np.sin(2 * np.pi * (45 * tk + 90 * (1 - np.exp(-tk * 30)) / 30)) * np.exp(-tk * 9)).astype(np.float32) * 0.9
    tc = np.arange(int(0.2 * SR)) / SR
    clap = (rng.standard_normal(len(tc)) * np.exp(-tc * 22)).astype(np.float32) * 0.28
    th = np.arange(int(0.05 * SR)) / SR
    hat = np.diff(rng.standard_normal(len(th) + 1)).astype(np.float32) * np.exp(-th * 70).astype(np.float32) * 0.09
    roots = [55.0, 43.65, 65.41, 49.0]  # A1 F1 C2 G1
    nb = int(dur / beat) + 2
    for b in range(nb):
        at = b * beat
        add(kick, at)
        if b % 2 == 1: add(clap, at)
        add(hat, at + beat / 2)
        bar = (b // 4) % 4; f = roots[bar]
        for half in (0, 0.5):
            tb = np.arange(int(beat * 0.45 * SR)) / SR
            ph = 2 * np.pi * f * 2 * tb
            saw = (2 * ((f * 2 * tb) % 1) - 1)
            bass = (0.6 * np.sin(ph) + 0.25 * saw) * np.minimum(1, tb * 200) * np.exp(-tb * 5)
            add(bass.astype(np.float32) * 0.32, at + half * beat)
    # pad
    chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]]
    barlen = 4 * beat
    for bi in range(int(dur / barlen) + 1):
        ch = chords[bi % 4]; tb = np.arange(int(barlen * SR)) / SR
        pad = sum(np.sin(2 * np.pi * f * tb) + 0.3 * np.sin(2 * np.pi * f * 2.003 * tb) for f in ch)
        env = np.minimum(1, tb / 0.3) * np.minimum(1, (barlen - tb) / 0.3)
        add((pad * env * 0.035).astype(np.float32), bi * barlen)
    return out

def whoosh(d=0.45, seed=3):
    rng = np.random.default_rng(seed); n = int(d * SR); tt = np.arange(n) / n
    nz = rng.standard_normal(n).astype(np.float32)
    # moving lowpass-ish via cumulative smoothing with varying alpha
    y = np.zeros(n, np.float32); a = 0.02 + 0.5 * np.sin(np.pi * tt) ** 2; acc = 0.0
    for i in range(n): acc += a[i] * (nz[i] - acc); y[i] = acc
    return y * np.sin(np.pi * tt) ** 1.5 * 0.5

def build(vid, take=None, render=True):
    spec = V[vid]
    texts = [spec['hook_voice']] + [s['voice'] for s in spec['scenes']] + [spec['cta_voice']]
    x = load(take or f'{TAKES}/{vid}.wav')
    clips, gaps = split(x, len(texts), texts)
    info = []
    LEAD_H, LEAD_S, TAIL, MIN_S = 0.12, 0.42, 0.45, 3.7
    segs = []; t = 0.0; voice_place = []
    for k, (a, b) in enumerate(clips):
        d = (b - a) / SR
        if k == 0:
            seg = dict(type='hook', t0=t, t1=t + LEAD_H + d + 0.35)
            l1, l2, bx = spec['hook']
            L = len(l1) + len(l2) + len(bx)
            seg['times'] = [0.0, LEAD_H + d * len(l1) / L * 0.95, LEAD_H + d * (len(l1) + len(l2)) / L * 0.97]
            voice_place.append((t + LEAD_H, a, b))
        elif k == len(clips) - 1:
            seg = dict(type='cta', t0=t, t1=t + LEAD_S + d + 1.8)
            seg['times'] = [0.0, LEAD_S + d * 0.17, LEAD_S + d * 0.42, LEAD_S + d * 0.72]
            voice_place.append((t + LEAD_S, a, b))
        else:
            dur = max(MIN_S, LEAD_S + d + TAIL)
            seg = dict(type='play', idx=k - 1, t0=t, t1=t + dur)
            voice_place.append((t + LEAD_S, a, b))
        segs.append(seg); t = seg['t1']
        info.append(f"{d:4.1f}s {len(texts[k]):3d}c {d/len(texts[k])*1000:4.0f}ms/c")
    total = round(t * 30) / 30
    tl = dict(segs=segs, total=total)
    # audio
    n = int(total * SR) + SR
    voice = np.zeros(n, np.float32)
    for (at, a, b) in voice_place:
        i = int(at * SR); clip = x[a:b].copy()
        f = int(0.01 * SR); clip[:f] *= np.linspace(0, 1, f); clip[-f:] *= np.linspace(1, 0, f)
        voice[i:i + len(clip)] += clip
    voice /= max(1e-6, np.abs(voice).max()) / 0.9
    mus = synth_music(n / SR)
    env = np.abs(voice); k = int(0.25 * SR)
    env = np.convolve(env, np.ones(k) / k, mode='same'); duck = 1 - 0.6 * np.clip(env / 0.04, 0, 1)
    mus = mus / max(1e-6, np.abs(mus).max()) * 0.22 * duck
    sfx = np.zeros(n, np.float32); w = whoosh()
    for s in segs[1:]:
        i = int((s['t0'] - 0.22) * SR); sfx[i:i + len(w)] += w[:max(0, min(len(w), n - i))] * 0.6
    mix = voice + mus + sfx
    mix[int(total * SR):] = 0
    fade = int(0.5 * SR); e = int(total * SR); mix[e - fade:e] *= np.linspace(1, 0, fade)
    mix = mix[:e]
    wav = f'{OUT}/{vid}_mix.wav'
    with wave.open(wav, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    json.dump(tl, open(f'{OUT}/{vid}_tl.json', 'w'))
    print(vid, 'total', total, '|', ' / '.join(info), '| gaps', gaps, flush=True)
    if render:
        vtmp = f'{OUT}/{vid}_v.mp4'
        video(spec, tl, vtmp, tag=vid)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vtmp, '-i', wav, '-c:v', 'copy',
                        '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', '48000', '-ac', '2', '-c:a', 'aac', '-b:a', '192k',
                        '-shortest', '-movflags', '+faststart', f'{OUT}/{vid}.mp4'], check=True)
        os.remove(vtmp)
    return tl

if __name__ == '__main__':
    render = '--norender' not in sys.argv
    for vid in [a for a in sys.argv[1:] if not a.startswith('--')]:
        build(vid, render=render)
