// Motor de vídeo F7 — estilo vídeo de referencia futbol7_v4 (1080x1920)
const W = 1080, H = 1920;
const LIME = '#C6FB02', GOLD = '#FFD400', RED = '#E8322B', BLACK = '#0b0b0b';
let FX0 = 112, FX1 = 930, FY0 = 432, FY1 = 1556, FW = FX1 - FX0, FH = FY1 - FY0, CX = (FX0 + FX1) / 2;
let FS = false;
const PR = 37; // player radius
const DEF7 = {
  y1: [0.5, 0.945], y2: [0.5, 0.80], y3: [0.166, 0.76], y4: [0.834, 0.76], y5: [0.33, 0.56], y6: [0.67, 0.56], y7: [0.5, 0.30],
  r1: [0.5, 0.055], r2: [0.5, 0.20], r3: [0.166, 0.24], r4: [0.834, 0.24], r5: [0.33, 0.44], r6: [0.67, 0.44], r7: [0.5, 0.70],
};
const DEF5 = {
  y1: [0.5, 0.945], y2: [0.5, 0.76], y3: [0.18, 0.60], y4: [0.82, 0.60], y5: [0.5, 0.36],
  r1: [0.5, 0.055], r2: [0.5, 0.24], r3: [0.18, 0.40], r4: [0.82, 0.40], r5: [0.5, 0.64],
};
let DEF = DEF7, IDS = Object.keys(DEF);
let cv, ctx, SPEC, TL, BG, FIELD, BAND_H, BAND_C;

function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const ease = x => { x = clamp(x, 0, 1); return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; };
const easeOut = x => 1 - Math.pow(1 - clamp(x, 0, 1), 3);
const backOut = x => { x = clamp(x, 0, 1); const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const lerp = (a, b, t) => a + (b - a) * t;
const P = f => [FX0 + f[0] * FW, FY0 + f[1] * FH];

function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }

// ---------- static layers ----------
function buildBG() {
  const c = mk(W, H), g = c.getContext('2d');
  const gr = g.createRadialGradient(540, 900, 100, 540, 900, 1250);
  gr.addColorStop(0, '#1d4f2c'); gr.addColorStop(0.6, '#163f22'); gr.addColorStop(1, '#0b2614');
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  g.save(); g.translate(540, 960); g.rotate(-0.52);
  for (let i = -20; i < 20; i++) { if (i % 2) continue; g.fillStyle = 'rgba(255,255,255,0.028)'; g.fillRect(-1600, i * 120, 3200, 120); }
  g.restore();
  const r = rng(7);
  for (let i = 0; i < 9000; i++) { g.fillStyle = r() < 0.5 ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.025)'; g.fillRect(r() * W, r() * H, 2, 2); }
  return c;
}
function drawGoal(g, top) {
  const w = FS ? Math.round(FW * 0.15) : 138, h = 42, x = CX - w / 2, y = top ? FY0 - 56 : FY1 + 14;
  g.save(); g.shadowColor = 'rgba(0,0,0,0.45)'; g.shadowBlur = 10; g.shadowOffsetY = 4;
  rr(g, x, y, w, h, 7); g.fillStyle = '#fff'; g.fill(); g.restore();
  rr(g, x + 6, y + 6, w - 12, h - 12, 3); g.fillStyle = '#4a4a4a'; g.fill();
  g.fillStyle = '#b9b9b9';
  for (let xx = x + 11; xx < x + w - 10; xx += 10) g.fillRect(xx, y + 8, 4, h - 16);
}
function buildField() {
  const c = mk(W, H), g = c.getContext('2d');
  // card shadow
  g.save(); g.shadowColor = 'rgba(0,0,0,0.55)'; g.shadowBlur = 34; g.shadowOffsetY = 10;
  rr(g, FX0 - 14, FY0 - 14, FW + 28, FH + 28, 22); g.fillStyle = '#0c2614'; g.fill(); g.restore();
  // grass
  g.save(); rr(g, FX0, FY0, FW, FH, 12); g.clip();
  const n = 12, bh = FH / n;
  for (let i = 0; i < n; i++) { g.fillStyle = i % 2 ? '#359E44' : '#2E8D3D'; g.fillRect(FX0, FY0 + i * bh, FW, bh + 1); }
  const r = rng(11);
  for (let i = 0; i < 7000; i++) { g.fillStyle = r() < 0.55 ? 'rgba(0,0,0,0.07)' : 'rgba(255,255,255,0.06)'; g.fillRect(FX0 + r() * FW, FY0 + r() * FH, 2, 3); }
  // lines
  g.strokeStyle = '#fff'; g.lineWidth = 7; g.lineJoin = 'round';
  g.beginPath(); g.moveTo(FX0, FY0 + FH / 2); g.lineTo(FX1, FY0 + FH / 2); g.stroke();
  g.beginPath(); g.arc(CX, FY0 + FH / 2, 106, 0, Math.PI * 2); g.stroke();
  g.fillStyle = '#fff'; g.beginPath(); g.arc(CX, FY0 + FH / 2, 8, 0, Math.PI * 2); g.fill();
  const bw = FW * 0.5, bd = FH * 0.158, sw = FW * 0.24, sd = FH * 0.062;
  g.strokeRect(CX - bw / 2, FY0 - 4, bw, bd + 4); g.strokeRect(CX - sw / 2, FY0 - 4, sw, sd + 4);
  g.strokeRect(CX - bw / 2, FY1 - bd, bw, bd + 4); g.strokeRect(CX - sw / 2, FY1 - sd, sw, sd + 4);
  g.restore();
  g.strokeStyle = '#fff'; g.lineWidth = 7; rr(g, FX0, FY0, FW, FH, 12); g.stroke();
  drawGoal(g, true); drawGoal(g, false);
  return c;
}

function buildCourt() {
  const c = mk(W, H), g = c.getContext('2d');
  g.save(); g.shadowColor = 'rgba(0,0,0,0.55)'; g.shadowBlur = 34; g.shadowOffsetY = 10;
  rr(g, FX0 - 14, FY0 - 14, FW + 28, FH + 28, 22); g.fillStyle = '#0c2614'; g.fill(); g.restore();
  g.save(); rr(g, FX0, FY0, FW, FH, 12); g.clip();
  // sports floor: flat with long subtle boards and sheen
  g.fillStyle = '#2F8F42'; g.fillRect(FX0, FY0, FW, FH);
  const r = rng(13);
  for (let x = FX0; x < FX1; x += 38) { g.fillStyle = r() < 0.5 ? 'rgba(0,0,0,0.035)' : 'rgba(255,255,255,0.025)'; g.fillRect(x, FY0, 38, FH); }
  const sh = g.createLinearGradient(FX0, FY0, FX1, FY1); sh.addColorStop(0, 'rgba(255,255,255,0.10)'); sh.addColorStop(0.5, 'rgba(255,255,255,0)'); sh.addColorStop(1, 'rgba(0,0,0,0.10)');
  g.fillStyle = sh; g.fillRect(FX0, FY0, FW, FH);
  for (let i = 0; i < 3500; i++) { g.fillStyle = r() < 0.5 ? 'rgba(0,0,0,0.05)' : 'rgba(255,255,255,0.04)'; g.fillRect(FX0 + r() * FW, FY0 + r() * FH, 2, 2); }
  // areas (D shape: 6 m quarter circles from each post, 20x40 court)
  const ax = 0.30 * FW, ay = 0.15 * FH, pw = 0.075 * FW;
  const area = (top) => {
    const y = top ? FY0 : FY1, s = top ? 1 : -1;
    g.beginPath();
    g.moveTo(CX - pw - ax, y);
    g.ellipse(CX - pw, y, ax, ay, 0, Math.PI, top ? Math.PI / 2 : Math.PI * 1.5, !top);
    g.lineTo(CX + pw, y + s * ay);
    g.ellipse(CX + pw, y, ax, ay, 0, top ? Math.PI / 2 : Math.PI * 1.5, 0, !top);
    g.closePath();
  };
  g.fillStyle = '#3AA24F'; area(true); g.fill(); area(false); g.fill();
  g.strokeStyle = '#fff'; g.lineWidth = 7; g.lineJoin = 'round';
  area(true); g.stroke(); area(false); g.stroke();
  g.beginPath(); g.moveTo(FX0, FY0 + FH / 2); g.lineTo(FX1, FY0 + FH / 2); g.stroke();
  g.beginPath(); g.arc(CX, FY0 + FH / 2, 0.15 * FW, 0, Math.PI * 2); g.stroke();
  g.fillStyle = '#fff';
  for (const yy of [FY0 + FH / 2, FY0 + 0.15 * FH, FY1 - 0.15 * FH, FY0 + 0.25 * FH, FY1 - 0.25 * FH]) { g.beginPath(); g.arc(CX, yy, 8, 0, Math.PI * 2); g.fill(); }
  // substitution zone ticks on the left touchline
  for (const yy of [0.35, 0.45, 0.55, 0.65]) g.fillRect(FX0, FY0 + yy * FH - 3, 26, 6);
  g.restore();
  g.strokeStyle = '#fff'; g.lineWidth = 7; rr(g, FX0, FY0, FW, FH, 12); g.stroke();
  drawGoal(g, true); drawGoal(g, false);
  return c;
}
function buildBand(seed, y0, y1) { // torn black band with splatter
  const c = mk(W, H), g = c.getContext('2d'), r = rng(seed);
  g.fillStyle = '#050805';
  g.beginPath(); g.moveTo(-30, y0 + 20);
  for (let x = -30; x <= W + 30; x += 26 + r() * 30) g.lineTo(x, y0 + (r() - 0.5) * 70 + (r() < 0.15 ? -40 * r() : 0));
  g.lineTo(W + 30, y1);
  for (let x = W + 30; x >= -30; x -= 26 + r() * 30) g.lineTo(x, y1 + (r() - 0.5) * 80 + (r() < 0.18 ? 55 * r() : 0));
  g.closePath(); g.fill();
  // drips / blobs
  for (let i = 0; i < 9; i++) { const x = r() * W, yy = r() < 0.5 ? y0 - 10 : y1 + 10; g.beginPath(); g.ellipse(x, yy, 30 + r() * 60, 18 + r() * 30, r(), 0, 7); g.fill(); }
  for (let i = 0; i < 40; i++) { const x = r() * W, yy = r() < 0.5 ? y0 - 30 - r() * 120 : y1 + 30 + r() * 140; g.beginPath(); g.arc(x, yy, 3 + r() * 10, 0, 7); g.fill(); }
  return c;
}

// ---------- text helpers ----------
function fitFont(text, family, max, maxW, weight = '') {
  let s = max; ctx.font = `${weight} ${s}px ${family}`;
  while (ctx.measureText(text).width > maxW && s > 20) { s -= 2; ctx.font = `${weight} ${s}px ${family}`; }
  return s;
}
function anton(text, x, y, size, fill, stroke = 10, align = 'center', skew = -0.18, shadow = true) {
  ctx.save(); ctx.translate(x, y); ctx.transform(1, 0, skew, 1, 0, 0);
  ctx.font = `${size}px Anton`; ctx.textAlign = align; ctx.textBaseline = 'middle';
  if (shadow) { ctx.save(); ctx.fillStyle = 'rgba(0,0,0,0.55)'; ctx.fillText(text, 6, 8); ctx.restore(); }
  if (stroke) { ctx.lineJoin = 'round'; ctx.lineWidth = stroke; ctx.strokeStyle = BLACK; ctx.strokeText(text, 0, 0); }
  ctx.fillStyle = fill; ctx.fillText(text, 0, 0); ctx.restore();
}

// ---------- scene state ----------
function posOf(scene, id, u) {
  let p = (scene.pos[id] || DEF[id]).slice();
  for (const e of scene.ev) {
    if (e.k !== 'mv' || e.p !== id || u < e.t) continue;
    const k = ease((u - e.t) / e.d); p = [lerp(p[0], e.to[0], k), lerp(p[1], e.to[1], k)];
  }
  return p;
}
function startOf(scene, id, t) { // position at time t (before events at t)
  return posOf(scene, id, t - 1e-6);
}
const isP = x => typeof x === 'string';
function ballOf(scene, u) {
  let holder = scene.ball, pt = null, flying = false;
  const passes = scene.ev.filter(e => e.k === 'pass').sort((a, b) => a.t - b.t);
  const at = (h, uu) => isP(h) ? posOf(scene, h, uu) : h;
  for (const e of passes) {
    if (u < e.t) break;
    const from = at(isP(e.fr) ? e.fr : e.fr, e.t);
    const endT = e.t + e.d;
    const target = e.cut || e.to;
    if (u < endT) {
      const k = (u - e.t) / e.d; const tp = isP(target) ? posOf(scene, target, u) : target;
      return { p: [lerp(from[0], tp[0], k), lerp(from[1], tp[1], k)], free: true };
    }
    if (e.cut) {
      // whoever stands at the cut point gets it
      let best = null, bd = 0.06;
      for (const id of IDS) { const q = posOf(scene, id, endT); const d = Math.hypot(q[0] - e.cut[0], (q[1] - e.cut[1]) * 1.37); if (d < bd) { bd = d; best = id; } }
      holder = best || e.cut;
    } else holder = e.to;
  }
  if (!holder) return null;
  if (isP(holder)) { const q = posOf(scene, holder, u); return { p: q, free: false, holder }; }
  return { p: holder, free: true };
}

// ---------- drawing primitives ----------
function drawPlayer(id, p, alpha = 1, scale = 1) {
  const [x, y] = P(p), mine = id[0] === 'y', num = id.slice(1), r = PR * scale;
  ctx.save(); ctx.globalAlpha = alpha;
  ctx.fillStyle = 'rgba(0,0,0,0.30)'; ctx.beginPath(); ctx.ellipse(x + 6, y + r * 0.62, r * 0.98, r * 0.5, 0, 0, 7); ctx.fill();
  ctx.beginPath(); ctx.arc(x, y, r, 0, 7);
  if (mine) { ctx.fillStyle = LIME; ctx.fill(); ctx.lineWidth = 7; ctx.strokeStyle = BLACK; ctx.stroke(); }
  else {
    ctx.fillStyle = '#141414'; ctx.fill(); ctx.lineWidth = 5.5; ctx.strokeStyle = '#fff'; ctx.stroke();
    ctx.beginPath(); ctx.arc(x, y, r + 3.6, 0, 7); ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(0,0,0,0.7)'; ctx.stroke();
  }
  ctx.save(); ctx.translate(x - r * 0.36, y - r * 0.46); ctx.rotate(-0.5); ctx.fillStyle = mine ? 'rgba(255,255,255,0.55)' : 'rgba(255,255,255,0.28)';
  ctx.beginPath(); ctx.ellipse(0, 0, r * 0.3, r * 0.15, 0, 0, 7); ctx.fill(); ctx.restore();
  ctx.fillStyle = mine ? BLACK : '#fff'; ctx.font = `${Math.round(46 * scale)}px Anton`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(num, x, y + 2);
  ctx.restore();
}
function drawBall(x, y, r = 19) {
  ctx.save();
  ctx.fillStyle = 'rgba(0,0,0,0.3)'; ctx.beginPath(); ctx.ellipse(x + 4, y + r * 0.7, r * 0.9, r * 0.4, 0, 0, 7); ctx.fill();
  ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fillStyle = '#fff'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = BLACK; ctx.stroke();
  ctx.save(); ctx.beginPath(); ctx.arc(x, y, r - 1.5, 0, 7); ctx.clip(); ctx.fillStyle = BLACK;
  const pent = (cx, cy, s, rot) => { ctx.beginPath(); for (let i = 0; i < 5; i++) { const a = rot + i * Math.PI * 2 / 5; ctx.lineTo(cx + Math.cos(a) * s, cy + Math.sin(a) * s); } ctx.closePath(); ctx.fill(); };
  pent(x, y, r * 0.36, -Math.PI / 2);
  for (let i = 0; i < 5; i++) { const a = -Math.PI / 2 + i * Math.PI * 2 / 5; pent(x + Math.cos(a) * r * 0.98, y + Math.sin(a) * r * 0.98, r * 0.33, a); }
  ctx.strokeStyle = BLACK; ctx.lineWidth = 1.6;
  for (let i = 0; i < 5; i++) { const a = -Math.PI / 2 + i * Math.PI * 2 / 5; ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * r * 0.36, y + Math.sin(a) * r * 0.36); ctx.lineTo(x + Math.cos(a) * r * 0.7, y + Math.sin(a) * r * 0.7); ctx.stroke(); }
  ctx.restore(); ctx.restore();
}
function arrow(a, b, kind, prog = 1, alpha = 1) {
  let [x0, y0] = P(a), [x1, y1] = P(b);
  const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy); if (L < 10) return;
  const ux = dx / L, uy = dy / L;
  const s0 = kind === 'pass' || kind === 'bad' || kind === 'shot' ? 0 : PR + 4;
  const e0 = kind === 'look' ? PR + 8 : (kind === 'run' || kind === 'rrun' ? 6 : 4);
  x0 += ux * s0; y0 += uy * s0; const Ld = Math.max(0, L - s0 - e0) * prog;
  const xe = x0 + ux * Ld, ye = y0 + uy * Ld;
  const col = { pass: '#fff', shot: '#fff', run: LIME, rrun: '#fff', bad: '#FF3B30', look: LIME }[kind];
  ctx.save(); ctx.globalAlpha = alpha; ctx.lineCap = 'round';
  ctx.setLineDash({ pass: [], shot: [], run: [18, 12], rrun: [12, 12], bad: [16, 12], look: [4, 12] }[kind]);
  const lw = { pass: 6, shot: 6, run: 6.5, rrun: 4.5, bad: 6, look: 5 }[kind];
  ctx.strokeStyle = 'rgba(0,0,0,0.35)'; ctx.lineWidth = lw + 4; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(xe, ye); ctx.stroke();
  ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(xe, ye); ctx.stroke();
  ctx.setLineDash([]);
  if (Ld > 20 && kind !== 'look') {
    const hs = kind === 'rrun' ? 16 : 22;
    ctx.fillStyle = col; ctx.strokeStyle = 'rgba(0,0,0,0.5)'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(xe + ux * 4, ye + uy * 4); ctx.lineTo(xe - ux * hs - uy * hs * 0.62, ye - uy * hs + ux * hs * 0.62);
    ctx.lineTo(xe - ux * hs + uy * hs * 0.62, ye - uy * hs - ux * hs * 0.62); ctx.closePath(); ctx.fill(); ctx.stroke();
  }
  ctx.restore();
}
function xMark(p, k) {
  const [x, y] = P(p), s = backOut(k); if (k <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.beginPath(); ctx.arc(0, 0, 25, 0, 7); ctx.fillStyle = RED; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = BLACK; ctx.stroke();
  ctx.strokeStyle = BLACK; ctx.lineWidth = 6; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(-9, -9); ctx.lineTo(9, 9); ctx.moveTo(9, -9); ctx.lineTo(-9, 9); ctx.stroke();
  ctx.restore();
}
function tagBox(x, y, text, k) {
  if (k <= 0) return; const s = backOut(k);
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.font = 'italic 800 31px BarlowC'; const w = ctx.measureText(text).width + 24, h = 40;
  rr(ctx, -w / 2, -h / 2, w, h, 7); ctx.fillStyle = 'rgba(232,212,22,0.93)'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = BLACK; ctx.stroke();
  ctx.fillStyle = BLACK; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, 0, 2);
  ctx.restore();
}
function bubble(x, y, text, k) {
  if (k <= 0) return; const s = backOut(Math.min(1, k));
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.font = '38px Anton'; const w = ctx.measureText(text).width + 30, h = 56;
  ctx.fillStyle = 'rgba(0,0,0,0.3)'; rr(ctx, -w / 2 + 4, -h - 14 + 6, w, h, 12); ctx.fill();
  ctx.beginPath(); rr(ctx, -w / 2, -h - 14, w, h, 12); ctx.fillStyle = '#fff'; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = BLACK; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(-12, -16); ctx.lineTo(0, 2); ctx.lineTo(12, -16); ctx.fillStyle = '#fff'; ctx.fill();
  ctx.beginPath(); ctx.moveTo(-12, -14); ctx.lineTo(0, 2); ctx.lineTo(12, -14); ctx.stroke();
  ctx.fillStyle = '#fff'; ctx.fillRect(-14, -20, 28, 6);
  ctx.save(); ctx.transform(1, 0, -0.12, 1, 0, 0); ctx.fillStyle = BLACK; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, 0, -h / 2 - 12); ctx.restore();
  ctx.restore();
}
function zoneMark(e, k, fade) {
  const [x, y] = P(e.at), r = e.r * FW, col = e.col === 'lime' ? LIME : '#FF3B30';
  ctx.save(); ctx.globalAlpha = fade; const s = easeOut(k);
  ctx.beginPath(); ctx.arc(x, y, r * s, 0, 7); ctx.fillStyle = e.col === 'lime' ? 'rgba(198,251,2,0.18)' : 'rgba(255,59,48,0.22)'; ctx.fill();
  ctx.setLineDash([14, 10]); ctx.lineWidth = 5; ctx.strokeStyle = col; ctx.stroke(); ctx.setLineDash([]);
  if (e.text) {
    ctx.font = '30px Anton'; const w = ctx.measureText(e.text).width + 22;
    ctx.save(); ctx.translate(x, y + r * s + 6); ctx.transform(1, 0, -0.15, 1, 0, 0);
    ctx.fillStyle = col; ctx.fillRect(-w / 2, 0, w, 40); ctx.fillStyle = e.col === 'lime' ? BLACK : '#fff';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(e.text, 0, 22); ctx.restore();
  }
  ctx.restore();
}

// ---------- scene drawing ----------
function drawTitleLegend(title, k) {
  const off = (1 - easeOut(k)) * -60;
  ctx.save(); ctx.globalAlpha = clamp(k * 2, 0, 1);
  const size = fitFont(title, 'Anton', 84, 470);
  ctx.save(); ctx.translate(off, 0); anton(title, 160, 300, size, LIME, 9, 'left', -0.2);
  ctx.fillStyle = LIME; ctx.fillRect(155, 355, 150 * easeOut(k * 1.4), 8); ctx.restore();
  ctx.restore();
  // legend (static)
  ctx.save();
  ctx.beginPath(); ctx.arc(668, 306, 16, 0, 7); ctx.fillStyle = LIME; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = BLACK; ctx.stroke();
  ctx.beginPath(); ctx.arc(668, 352, 16, 0, 7); ctx.fillStyle = '#141414'; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = '#fff'; ctx.stroke();
  for (const [t, yy] of [['TU EQUIPO', 306], ['RIVAL', 352]]) {
    ctx.save(); ctx.translate(694, yy + 2); ctx.transform(1, 0, -0.1, 1, 0, 0); ctx.font = '36px Anton'; ctx.textBaseline = 'middle';
    ctx.lineWidth = 7; ctx.lineJoin = 'round'; ctx.strokeStyle = BLACK; ctx.strokeText(t, 0, 0); ctx.fillStyle = '#fff'; ctx.fillText(t, 0, 0); ctx.restore();
  }
  ctx.restore();
}
function drawSub(lines, k) {
  if (!lines) return;
  const y0 = 1632, y1 = 1782;
  ctx.save();
  ctx.fillStyle = 'rgba(6,9,7,0.94)';
  ctx.beginPath(); ctx.moveTo(80, y0); ctx.lineTo(940, y0); ctx.lineTo(920, y1); ctx.lineTo(70, y1); ctx.closePath(); ctx.fill();
  ctx.fillStyle = LIME; ctx.beginPath(); ctx.moveTo(73, y0); ctx.lineTo(97, y0); ctx.lineTo(87, y1); ctx.lineTo(62, y1); ctx.closePath(); ctx.fill();
  const a = clamp(k, 0, 1);
  const col = `rgb(${Math.round(lerp(90, 236, a))},${Math.round(lerp(96, 236, a))},${Math.round(lerp(92, 236, a))})`;
  const l1 = lines[0], l2 = lines[1] || '';
  ctx.font = 'italic 800 64px BarlowC';
  let s = 64; while (Math.max(ctx.measureText(l1).width, ctx.measureText(l2).width) > 790 && s > 40) { s -= 2; ctx.font = `italic 800 ${s}px BarlowC`; }
  ctx.fillStyle = col; ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
  ctx.fillText(l1, 114, 1701); ctx.fillText(l2, 110, 1765);
  ctx.restore();
}
function drawPlay(scene, u, tl, dur) {
  // arrows (persist)
  const tU = 0.12; // seconds-equivalent helpers
  for (const e of scene.ev) {
    if (u < e.t) continue;
    if (e.k === 'mv' && e.a !== 'none') {
      const a = startOf(scene, e.p, e.t); const pr = clamp((u - e.t) / (e.d * 0.55), 0, 1);
      arrow(a, e.to, e.a, easeOut(pr));
    } else if (e.k === 'pass') {
      const from = isP(e.fr) ? posOf(scene, e.fr, e.t) : e.fr;
      const tgt = e.cut ? (isP(e.to) ? posOf(scene, e.to, e.t + e.d) : e.to) : (isP(e.to) ? posOf(scene, e.to, e.t + e.d) : e.to);
      const pr = clamp((u - e.t) / e.d, 0, 1);
      if (e.kind === 'bad') arrow(from, tgt, 'bad', easeOut(clamp((u - e.t) / (e.d * 0.8), 0, 1)));
      else {
        const curT = isP(e.to) ? posOf(scene, e.to, Math.min(u, e.t + e.d)) : e.to;
        arrow(from, pr < 1 ? [lerp(from[0], curT[0], pr), lerp(from[1], curT[1], pr)] : tgt, e.kind === 'shot' ? 'shot' : 'pass', 1);
      }
    } else if (e.k === 'arrow') {
      const from = isP(e.fr) ? posOf(scene, e.fr, e.t) : e.fr; const to = isP(e.to) ? posOf(scene, e.to, e.t) : e.to;
      const pr = clamp((u - e.t) / 0.12, 0, 1);
      arrow(from, to, e.kind, easeOut(pr));
    }
  }
  // zones
  for (const e of scene.ev) if (e.k === 'zone' && u >= e.t) {
    const k = clamp((u - e.t) / 0.08, 0, 1), fade = 1 - clamp((u - (e.t + e.d)) / 0.06, 0, 1);
    if (fade > 0) zoneMark(e, k, fade);
  }
  // focus ring under players
  const pos = {}; for (const id of IDS) pos[id] = posOf(scene, id, u);
  if (scene.focus) {
    const [fx, fy] = P(pos[scene.focus[0]]); const pulse = 1 + 0.06 * Math.sin(tl * 6.5);
    ctx.save(); ctx.beginPath(); ctx.arc(fx, fy, (PR + 20) * pulse * backOut(clamp(u / 0.06, 0, 1)), 0, 7);
    ctx.lineWidth = 7; ctx.strokeStyle = GOLD; ctx.shadowColor = 'rgba(0,0,0,0.4)'; ctx.shadowBlur = 6; ctx.stroke(); ctx.restore();
  }
  // players (rivals first)
  const order = IDS.filter(i => !scene.hide.includes(i)).sort((a, b) => pos[a][1] - pos[b][1]);
  for (const id of order) drawPlayer(id, pos[id]);
  // ball
  const b = ballOf(scene, u);
  if (b) { const [bx, by] = P(b.p); if (b.free) drawBall(bx, by); else drawBall(bx + PR * 0.62, by - PR * 0.5); }
  // X marks
  for (const e of scene.ev) {
    if (e.k === 'arrow' && e.x && u >= e.t + 0.1) xMark(e.x, (u - e.t - 0.1) / 0.06);
    if (e.k === 'pass' && e.cut && u >= e.t + e.d) xMark([e.cut[0] + 0.0, e.cut[1] - 0.045], (u - e.t - e.d) / 0.06);
  }
  // tags
  const tags = {};
  if (scene.focus) tags[scene.focus[0]] = [scene.focus[1], clamp((u - 0.02) / 0.06, 0, 1)];
  for (const e of scene.ev) if (e.k === 'tag' && u >= e.t) tags[e.p] = [e.text, clamp((u - e.t) / 0.06, 0, 1)];
  for (const [id, [text, k]] of Object.entries(tags)) { const [x, y] = P(pos[id]); tagBox(x, y - PR - 28, text, k); }
  // bubbles
  for (const e of scene.ev) if (e.k === 'bub' && u >= e.t && u <= e.t + e.d + 0.05) {
    const [x, y] = P(pos[e.p]); const k = Math.min(clamp((u - e.t) / 0.05, 0, 1), clamp((e.t + e.d + 0.05 - u) / 0.05, 0, 1));
    bubble(x, y - PR - (tags[e.p] ? 50 : 4), e.text, k);
  }
  // goal
  for (const e of scene.ev) if (e.k === 'goal' && u >= e.t) {
    const k = (u - e.t) / 0.07; const s = backOut(k) * (1 + 0.03 * Math.sin(tl * 9));
    ctx.save(); ctx.translate(CX, FY0 + FH * 0.36); ctx.rotate(-0.06); ctx.scale(s, s);
    anton('¡GOOOL!', 0, 0, 205, LIME, 16, 'center', -0.18); ctx.restore();
  }
}

// ---------- hook & CTA ----------
function drawDimField(tl, z) {
  ctx.save(); ctx.translate(CX, 990); ctx.scale(z, z); ctx.translate(-CX, -990);
  ctx.drawImage(FIELD, 0, 0);
  for (const id of IDS) drawPlayer(id, DEF[id]);
  const [bx, by] = P([0.5, 0.5]); drawBall(bx, by);
  ctx.restore();
  ctx.fillStyle = 'rgba(2,8,3,0.66)'; ctx.fillRect(0, 0, W, H);
}
function drawHook(t, seg) {
  const lt = t - seg.t0;
  drawDimField(t, 1 + 0.015 * lt);
  const tt = seg.times; // [t_line1, t_line2, t_box]
  const k1 = clamp((lt - tt[0]) / 0.18, 0, 1);
  if (k1 > 0) { ctx.save(); ctx.globalAlpha = clamp(k1 * 3, 0, 1); ctx.drawImage(BAND_H, 0, 0); ctx.restore(); }
  const [l1, l2, box] = SPEC.hook;
  const s1 = fitFont(l1, 'Anton', 150, 930), s2 = fitFont(l2, 'Anton', 104, 930);
  if (k1 > 0) { const sc = lerp(1.35, 1, easeOut(k1)); ctx.save(); ctx.translate(530, 735); ctx.scale(sc, sc); anton(l1, 0, 0, s1, '#fff', 12); ctx.restore(); }
  const k2 = clamp((lt - tt[1]) / 0.2, 0, 1);
  if (k2 > 0) { ctx.save(); ctx.globalAlpha = clamp(k2 * 2, 0, 1); anton(l2, 530 + (1 - easeOut(k2)) * 500, 735 + s1 * 0.5 + s2 * 0.62, s2, LIME, 10); ctx.restore(); }
  const k3 = clamp((lt - tt[2]) / 0.16, 0, 1);
  if (k3 > 0) {
    const yb = 735 + s1 * 0.5 + s2 * 1.12 + 120;
    const sb = fitFont(box, 'Anton', 128, 760);
    ctx.font = `${sb}px Anton`; const bw = ctx.measureText(box).width + 90, bh = sb * 1.18;
    ctx.save(); ctx.translate(530, yb); ctx.rotate(-0.035); const sc = backOut(k3); ctx.scale(sc, sc);
    ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.beginPath(); ctx.moveTo(-bw / 2 + 30 + 8, -bh / 2 + 10); ctx.lineTo(bw / 2 + 8, -bh / 2 + 10); ctx.lineTo(bw / 2 - 30 + 8, bh / 2 + 10); ctx.lineTo(-bw / 2 + 8, bh / 2 + 10); ctx.fill();
    ctx.fillStyle = LIME; ctx.beginPath(); ctx.moveTo(-bw / 2 + 30, -bh / 2); ctx.lineTo(bw / 2, -bh / 2); ctx.lineTo(bw / 2 - 30, bh / 2); ctx.lineTo(-bw / 2, bh / 2); ctx.fill();
    anton(box, 0, 4, sb, BLACK, 0, 'center', -0.18, false);
    ctx.restore();
  }
}
function drawCTA(t, seg) {
  const lt = t - seg.t0, tt = seg.times; // [line1, line2, banner, link]
  drawDimField(t, 1 + 0.012 * lt);
  const k1 = clamp((lt - tt[0]) / 0.18, 0, 1);
  if (k1 > 0) { ctx.save(); ctx.globalAlpha = clamp(k1 * 3, 0, 1); ctx.drawImage(BAND_C, 0, 0); ctx.restore(); }
  const l1 = FS ? '¿QUIERES JUGAR FÚTBOL SALA' : '¿QUIERES JUGAR F7', l2 = 'SIN TENER EQUIPO?';
  if (k1 > 0) { const sc = lerp(1.3, 1, easeOut(k1)); ctx.save(); ctx.translate(530, 585); ctx.scale(sc, sc); anton(l1, 0, 0, fitFont(l1, 'Anton', 116, 960), '#fff', 11); ctx.restore(); }
  const k2 = clamp((lt - tt[1]) / 0.2, 0, 1);
  if (k2 > 0) { ctx.save(); ctx.globalAlpha = clamp(k2 * 2, 0, 1); anton(l2, 530 + (1 - easeOut(k2)) * 500, 745, 116, LIME, 11); ctx.restore(); }
  const k3 = clamp((lt - tt[2]) / 0.16, 0, 1);
  if (k3 > 0) {
    ctx.save(); ctx.translate(540, 950); ctx.scale(lerp(0.6, 1, backOut(k3)), lerp(0.6, 1, backOut(k3))); ctx.globalAlpha = clamp(k3 * 2, 0, 1);
    ctx.fillStyle = LIME; ctx.beginPath(); ctx.moveTo(-430, -44); ctx.lineTo(446, -44); ctx.lineTo(430, 44); ctx.lineTo(-446, 44); ctx.fill();
    anton('ÚNETE AL GRUPO DE WHATSAPP', 0, 3, 66, BLACK, 0, 'center', -0.18, false); ctx.restore();
    const k4 = clamp((lt - tt[2] - 0.25) / 0.2, 0, 1);
    ctx.save(); ctx.globalAlpha = k4; ctx.font = 'italic 800 44px BarlowC'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.lineWidth = 6; ctx.strokeStyle = BLACK; ctx.lineJoin = 'round';
    ctx.strokeText('PACHANGAS DE 1 HORA · TÚ VIENES Y JUEGAS', 540, 1074); ctx.fillStyle = '#fff'; ctx.fillText('PACHANGAS DE 1 HORA · TÚ VIENES Y JUEGAS', 540, 1074);
    ctx.strokeText('SIN LIGAS · SIN TORNEOS · SIN COMPROMISO', 540, 1134); ctx.fillStyle = LIME; ctx.fillText('SIN LIGAS · SIN TORNEOS · SIN COMPROMISO', 540, 1134);
    ctx.restore();
  }
  const k5 = clamp((lt - tt[3]) / 0.16, 0, 1);
  if (k5 > 0) {
    ctx.save(); ctx.translate(548, 1296); const sc = backOut(k5); ctx.scale(sc, sc);
    ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.beginPath(); ctx.moveTo(-290 + 8, -52 + 9); ctx.lineTo(312 + 8, -52 + 9); ctx.lineTo(296 + 8, 52 + 9); ctx.lineTo(-306 + 8, 52 + 9); ctx.fill();
    ctx.fillStyle = LIME; ctx.beginPath(); ctx.moveTo(-290, -52); ctx.lineTo(312, -52); ctx.lineTo(296, 52); ctx.lineTo(-306, 52); ctx.fill();
    anton('ENLACE EN LA BIO', 0, 4, 84, BLACK, 0, 'center', -0.18, false); ctx.restore();
    const bob = Math.abs(Math.sin((lt - tt[3]) * 5)) * 18;
    ctx.save(); ctx.globalAlpha = clamp(k5 * 2, 0, 1); ctx.translate(548, 1430 - bob);
    ctx.fillStyle = LIME; ctx.strokeStyle = BLACK; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(0, -28); ctx.lineTo(34, 22); ctx.lineTo(-34, 22); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
  }
}

// ---------- transitions ----------
function wipe(p) { // p 0..1
  if (p <= 0 || p >= 1) return;
  const xl = lerp(1180, -2100, p), sl = 260, bw = 1650;
  ctx.save();
  ctx.fillStyle = BLACK; ctx.beginPath(); ctx.moveTo(xl + sl - 34, 0); ctx.lineTo(xl + sl + bw, 0); ctx.lineTo(xl + bw, H); ctx.lineTo(xl - 34, H); ctx.fill();
  ctx.fillStyle = LIME; ctx.beginPath(); ctx.moveTo(xl + sl, 0); ctx.lineTo(xl + sl + bw, 0); ctx.lineTo(xl + bw, H); ctx.lineTo(xl, H); ctx.fill();
  ctx.restore();
}

// ---------- main ----------
function init(spec, tl) {
  SPEC = spec; TL = tl;
  FS = spec.sport === 'fs';
  if (FS) { FX0 = 160; FX1 = 920; } else { FX0 = 112; FX1 = 930; }
  FW = FX1 - FX0; FH = FY1 - FY0; CX = (FX0 + FX1) / 2;
  DEF = FS ? DEF5 : DEF7; IDS = Object.keys(DEF);
  cv = document.getElementById('c'); ctx = cv.getContext('2d');
  BG = buildBG(); FIELD = FS ? buildCourt() : buildField();
  BAND_H = buildBand(3, 600, 1020); BAND_C = buildBand(5, 470, 1190);
  for (const s of SPEC.scenes) { s.ev.sort((a, b) => a.t - b.t); }
}
function draw(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H);
  ctx.drawImage(BG, 0, 0);
  let seg = TL.segs[TL.segs.length - 1];
  for (const s of TL.segs) if (t >= s.t0 && t < s.t1) { seg = s; break; }
  if (seg.type === 'hook') drawHook(t, seg);
  else if (seg.type === 'cta') drawCTA(t, seg);
  else {
    const sc = SPEC.scenes[seg.idx]; const u = (t - seg.t0) / (seg.t1 - seg.t0);
    // scene-relative time mapping: events use u of the scene
    ctx.drawImage(FIELD, 0, 0);
    drawPlay(sc, u, t, seg.t1 - seg.t0);
    drawTitleLegend(sc.title, clamp((t - seg.t0 - 0.12) / 0.3, 0, 1));
    drawSub(sc.sub, clamp((t - seg.t0 - 0.15) / 0.3, 0, 1));
  }
  // wipes at boundaries
  const WD = 0.44;
  for (let i = 1; i < TL.segs.length; i++) { const b = TL.segs[i].t0; if (Math.abs(t - b) < WD / 2) wipe((t - b + WD / 2) / WD); }
  // fade in from black at very start
  if (t < 0.06) { ctx.fillStyle = `rgba(0,0,0,${1 - t / 0.06})`; ctx.fillRect(0, 0, W, H); }
}
window.init = init; window.draw = draw;
