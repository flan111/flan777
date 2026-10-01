// Measures every [data-x] element of deck.html and writes scene.json + image layers for the PPTX builder.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');

const ROOT = __dirname;
const OUT = path.join(ROOT, 'pptx_build');
const IMG = path.join(OUT, 'img');
fs.mkdirSync(IMG, { recursive: true });
const DSF = 2;

(async () => {
  const only = process.argv[2] ? process.argv[2].split(',').map(Number) : null;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: DSF });
  await page.goto('file://' + path.join(ROOT, 'deck/deck.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({ content: `
    html.iso, body.iso, body.iso .slide{background:transparent!important}
    body.iso *{visibility:hidden!important}
    body.iso .iso-t, body.iso .iso-t *{visibility:visible!important}
    body.iso .iso-t [data-x], body.iso .iso-t [data-x] *{visibility:hidden!important}
    body.isobg *{visibility:hidden!important}
    body.isobg .bgfill, body.isobg .grain{visibility:visible!important}
    body.notext [data-x="text"], body.notext [data-x="text"] *{visibility:hidden!important}
  ` });
  await page.waitForTimeout(300);
  const nSlides = await page.$$eval('section.slide', s => s.length);
  const scene = [];
  for (let i = 0; i < nSlides; i++) {
    if (only && !only.includes(i + 1)) continue;
    await page.evaluate(i => {
      document.querySelectorAll('section.slide').forEach((s, j) => s.style.display = (j === i ? 'block' : 'none'));
      window.scrollTo(0, 0);
    }, i);
    const data = await page.evaluate((i) => {
      const slide = document.querySelectorAll('section.slide')[i];
      const sr = slide.getBoundingClientRect();
      const els = [...slide.querySelectorAll('[data-x]')];
      const rgba = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(x => parseFloat(x)); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
      const hex = c => [c.r, c.g, c.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
      function animOf(el) {
        let e = el;
        while (e && e !== slide) { if (e.dataset && e.dataset.a) return { a: e.dataset.a, d: +(e.dataset.d || 0), t: e.dataset.t ? +e.dataset.t : null }; e = e.parentElement; }
        return null;
      }
      function rot(el) {
        const t = getComputedStyle(el).transform;
        if (!t || t === 'none') return 0;
        const m = t.match(/matrix\(([^)]+)\)/); if (!m) return 0;
        const [a, b] = m[1].split(',').map(parseFloat);
        return Math.round(Math.atan2(b, a) * 180 / Math.PI * 100) / 100;
      }
      function bgBehind(el) { // first opaque-ish background up the tree (for blending translucent text)
        let e = el.parentElement;
        while (e && e !== document.body) {
          const c = rgba(getComputedStyle(e).backgroundColor);
          if (c && c.a > 0.5) return c;
          if (e.classList.contains('slide')) { const bg = e.querySelector('.bgfill'); if (bg) { const im = getComputedStyle(bg).backgroundImage; if (im.includes('255, 141')||im.includes('#FF8D26')) return { r: 250, g: 132, b: 30, a: 1 }; return { r: 45, g: 105, b: 160, a: 1 }; } return { r: 255, g: 255, b: 255, a: 1 }; }
          e = e.parentElement;
        }
        return { r: 255, g: 255, b: 255, a: 1 };
      }
      function hasOwnVisuals(el) { // visible content inside el that is not covered by a nested [data-x]
        const walk = (n) => {
          for (const c of n.children) {
            if (c.hasAttribute('data-x')) continue;
            const cs = getComputedStyle(c);
            if (cs.display === 'none' || cs.visibility === 'hidden') continue;
            if (c.tagName === 'svg' || c.tagName === 'IMG') return true;
            const bg = rgba(cs.backgroundColor);
            if ((bg && bg.a > 0) || cs.backgroundImage !== 'none') return true;
            if (parseFloat(cs.borderTopWidth) > 0 || parseFloat(cs.borderRightWidth) > 0 || parseFloat(cs.borderBottomWidth) > 0) return true;
            if (walk(c)) return true;
          }
          for (const t of n.childNodes) if (t.nodeType === 3 && t.textContent.trim()) return true;
          return false;
        };
        return walk(el);
      }
      function clipAncestor(el) { // nearest overflow:hidden ancestor below the slide
        let e = el.parentElement;
        while (e && e !== slide) { if (getComputedStyle(e).overflow === 'hidden') return e; e = e.parentElement; }
        return null;
      }
      function textData(el) {
        const cs = getComputedStyle(el);
        const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.4;
        const tokens = [];
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
          const pe = node.parentElement;
          const pcs = getComputedStyle(pe);
          if (pcs.visibility === 'hidden' || pcs.display === 'none') continue;
          const t = node.textContent;
          const re = /\S+|\s+/g; let m;
          while ((m = re.exec(t))) {
            const isSp = /^\s+$/.test(m[0]);
            let rect = null;
            if (!isSp) {
              const range = document.createRange(); range.setStart(node, m.index); range.setEnd(node, m.index + m[0].length);
              const rs = [...range.getClientRects()].filter(q => q.width > 0.5);
              if (rs.length) { rect = rs.reduce((a, b) => (b.width > a.width ? b : a)); rect = { x: rect.x, y: rect.y, w: rect.width, h: rect.height }; }
            }
            const col = rgba(pcs.color);
            const fs_ = parseFloat(pcs.fontSize);
            // a flex/grid gap between two sibling spans reads as a word space
            const prev = tokens[tokens.length - 1];
            if (!isSp && rect && prev && !prev.sp && prev.rect && prev.pe !== pe) {
              const gap = Math.max(prev.rect.x - (rect.x + rect.w), rect.x - (prev.rect.x + prev.rect.w));
              if (gap > fs_ * 0.15) tokens.push({ t: ' ', sp: true, rect: null, size: fs_, color: col, bold: false, dir: pcs.direction, pe });
            }
            const sw = parseFloat(pcs.webkitTextStrokeWidth) || 0;
            tokens.push({ t: isSp ? ' ' : m[0], sp: isSp, rect, size: fs_, color: col, bold: sw / fs_ >= 0.02, dir: pcs.direction, pe });
          }
        }
        // lines
        const lines = []; let cur = null;
        for (const tk of tokens) {
          if (tk.sp) { if (cur) cur.toks.push(tk); continue; }
          const cy = tk.rect ? tk.rect.y + tk.rect.h / 2 : (cur ? cur.cy : 0);
          if (!cur || Math.abs(cy - cur.cy) > lh * 0.5) { cur = { cy, toks: [] }; lines.push(cur); }
          cur.toks.push(tk);
        }
        const out = lines.map(l => {
          while (l.toks.length && l.toks[l.toks.length - 1].sp) l.toks.pop();
          while (l.toks.length && l.toks[0].sp) l.toks.shift();
          const runs = [];
          for (const tk of l.toks) {
            let col = tk.color;
            if (col.a < 1) { const b = bgBehind(el); col = { r: col.r * col.a + b.r * (1 - col.a), g: col.g * col.a + b.g * (1 - col.a), b: col.b * col.a + b.b * (1 - col.a), a: 1 }; }
            const key = hex(col) + '|' + tk.size + '|' + tk.bold;
            const last = runs[runs.length - 1];
            if (last && last.key === key) last.text += tk.t; else runs.push({ key, text: tk.t, color: hex(col), size: tk.size, bold: tk.bold });
          }
          return runs.map(({ key, ...r }) => r);
        }).filter(r => r.length);
        // tight text bounds
        const rects = tokens.filter(t => t.rect).map(t => t.rect);
        let tb = null;
        if (rects.length) { const x0 = Math.min(...rects.map(r => r.x)), y0 = Math.min(...rects.map(r => r.y)), x1 = Math.max(...rects.map(r => r.x + r.w)), y1 = Math.max(...rects.map(r => r.y + r.h)); tb = { x: x0 - sr.x, y: y0 - sr.y, w: x1 - x0, h: y1 - y0 }; }
        let align = cs.textAlign; const dir = cs.direction;
        if (align === 'start') align = dir === 'rtl' ? 'right' : 'left';
        if (align === 'end') align = dir === 'rtl' ? 'left' : 'right';
        // flex containers centre their content
        if (cs.display.includes('flex') && cs.justifyContent === 'center') align = 'center';
        const cy0 = lines.length ? lines[0].cy - sr.y : null;
        return { lines: out, lh, align, dir, tb, cy0, size: parseFloat(cs.fontSize) };
      }
      const items = [];
      els.forEach((el, k) => {
        const cs = getComputedStyle(el);
        if (cs.display === 'none') return;
        let type = el.dataset.x;
        const r = el.getBoundingClientRect();
        const box = { x: r.x - sr.x, y: r.y - sr.y, w: r.width, h: r.height };
        const it = { k, type, name: el.dataset.name || '', anim: animOf(el), box, rot: 0 };
        if (type === 'group') return;
        if (type === 'asset') {
          it.src = el.dataset.src; it.rot = rot(el);
          it.w0 = el.offsetWidth; it.h0 = el.offsetHeight;
          it.cx = box.x + box.w / 2; it.cy = box.y + box.h / 2;
          it.opacity = parseFloat(cs.opacity);
          const ca = clipAncestor(el);
          if (ca) { const c = ca.getBoundingClientRect(); if (r.x < c.x - 1 || r.y < c.y - 1 || r.right > c.right + 1 || r.bottom > c.bottom + 1) { it.type = 'snap'; it.clip = { x: Math.max(r.x, c.x) - sr.x, y: Math.max(r.y, c.y) - sr.y, w: Math.min(r.right, c.right) - Math.max(r.x, c.x), h: Math.min(r.bottom, c.bottom) - Math.max(r.y, c.y) }; } }
        }
        if (type === 'shape') {
          const bg = rgba(cs.backgroundColor);
          const hasImg = cs.backgroundImage !== 'none';
          const bw = parseFloat(cs.borderTopWidth) || 0;
          if (hasImg || hasOwnVisuals(el)) { it.type = 'snap'; }
          else {
            if ((!bg || bg.a === 0) && bw === 0) return; // pure layout wrapper
            it.fill = bg && bg.a > 0 ? { color: hex(bg), alpha: bg.a * parseFloat(cs.opacity) } : null;
            it.border = bw > 0 ? { w: bw, color: hex(rgba(cs.borderTopColor)) } : null;
            const rr = cs.borderTopLeftRadius;
            it.radius = rr.endsWith('%') ? parseFloat(rr) / 100 * Math.min(box.w, box.h) : (parseFloat(rr) || 0);
            it.shadow = cs.boxShadow !== 'none';
          }
        }
        if (it.type === 'snap' || type === 'bg') {
          it.shadow = cs.boxShadow !== 'none';
          it.rot = rot(el);
        }
        if (type === 'text') {
          Object.assign(it, textData(el));
          if (!it.lines.length) return;
        }
        if (type === 'chart') { it.chart = JSON.parse(el.dataset.chart); }
        el.setAttribute('data-k', k);
        items.push(it);
      });
      return { items, tr: slide.dataset.tr || 'morph', dark: slide.classList.contains('dark') };
    }, i);

    // ---- image layers
    for (const it of data.items) {
      if (it.type === 'bg') {
        await page.evaluate(() => document.body.classList.add('isobg'));
        const f = `bg_${i + 1}.jpg`;
        await page.screenshot({ path: path.join(IMG, f), type: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
        await page.evaluate(() => document.body.classList.remove('isobg'));
        it.file = f;
      }
      if (it.type === 'snap') {
        const pad = it.shadow ? 70 : 6;
        let c = it.clip || { x: it.box.x - pad, y: it.box.y - pad, w: it.box.w + pad * 2, h: it.box.h + pad * 2 };
        // keep inside the viewport
        const x0 = Math.max(0, c.x), y0 = Math.max(0, c.y), x1 = Math.min(1920, c.x + c.w), y1 = Math.min(1080, c.y + c.h);
        c = { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
        if (c.w < 1 || c.h < 1) { it.skip = true; continue; }
        await page.evaluate(k => { document.body.classList.add('iso'); document.documentElement.classList.add('iso'); document.querySelector(`.slide[style*="block"] [data-k="${k}"]`).classList.add('iso-t'); }, it.k);
        const f = `s${i + 1}_${it.k}.png`;
        await page.screenshot({ path: path.join(IMG, f), omitBackground: true, clip: { x: c.x, y: c.y, width: c.w, height: c.h } });
        await page.evaluate(k => { document.body.classList.remove('iso'); document.documentElement.classList.remove('iso'); document.querySelector(`.slide[style*="block"] [data-k="${k}"]`).classList.remove('iso-t'); }, it.k);
        it.file = f; it.img = c;
      }
    }
    // reference render of the slide (for QA)
    await page.screenshot({ path: path.join(OUT, `ref_${String(i + 1).padStart(2, '0')}.png`), clip: { x: 0, y: 0, width: 1920, height: 1080 }, scale: 'css' });
    scene.push({ n: i + 1, ...data });
    process.stdout.write(`${i + 1} `);
  }
  // assets: render each unique svg to png at high resolution
  const assets = new Set(); scene.forEach(s => s.items.forEach(it => it.type === 'asset' && assets.add(it.src)));
  const ap = await browser.newPage({ viewport: { width: 2400, height: 2400 }, deviceScaleFactor: 1 });
  for (const src of assets) {
    const svg = fs.readFileSync(path.join(ROOT, 'assets', src + '.svg'), 'utf8');
    const vb = svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
    const H = 1600, W = Math.round(H * vb[2] / vb[3]);
    const w = W > 2400 ? 2400 : W, h = W > 2400 ? Math.round(2400 * vb[3] / vb[2]) : H;
    await ap.setContent(`<html><body style="margin:0;background:transparent"><img id="i" src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}" style="width:${w}px;height:${h}px;display:block"></body></html>`);
    await ap.waitForTimeout(50);
    const f = 'asset_' + src.replace(/\//g, '_') + '.png';
    await (await ap.$('#i')).screenshot({ path: path.join(IMG, f), omitBackground: true });
  }
  fs.writeFileSync(path.join(OUT, only ? 'scene_partial.json' : 'scene.json'), JSON.stringify(scene));
  await browser.close();
  console.log('\nok', scene.length);
})();
