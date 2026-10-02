// Builds the .pptx from pptx_build/scene.json (geometry measured from the HTML design).
const path = require('path'), fs = require('fs');
const pptxgen = require(path.join(__dirname, 'build/node_modules/pptxgenjs'));

const ROOT = __dirname, OUT = path.join(ROOT, 'pptx_build'), IMG = path.join(OUT, 'img');
const scene = JSON.parse(fs.readFileSync(path.join(OUT, process.argv[2] || 'scene.json')));
const outFile = process.argv[3] || path.join(OUT, 'raw.pptx');
const PX = 1 / 144;              // inches per CSS px (1920px == 13.333in)
const PT = 0.5;                  // points per CSS px
// Alexandria static weights: every weight is its own family name so PowerPoint can address it.
const FACE = { 100: 'Alexandria Thin', 200: 'Alexandria ExtraLight', 300: 'Alexandria Light', 400: 'Alexandria', 500: 'Alexandria Medium',
  600: 'Alexandria SemiBold', 700: 'Alexandria', 800: 'Alexandria ExtraBold', 900: 'Alexandria Black' };
const CAL = JSON.parse(fs.readFileSync(path.join(ROOT, 'calib.json')));   // baseline calibration (see README)

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.rtlMode = true;
pres.title = 'أرض البساتين — الخطة التسويقية';
pres.author = 'حمير بشبر علي غالب زايد';
pres.company = 'بصمة وعي';

const crypto = require('crypto');
const md5 = f => crypto.createHash('md5').update(fs.readFileSync(f)).digest('hex');
const r4 = v => Math.round(v / 4);
function sig(it) {   // what makes an object 'the same' for Morph
  if (it.type === 'text') return `T|${r4(it.box.x)}|${r4(it.box.y)}|${r4(it.box.w)}|` + it.lines.map(l => l.map(r => r.text + r.color + r.weight).join('')).join('/');
  if (it.type === 'shape') return `S|${r4(it.box.x)}|${r4(it.box.y)}|${r4(it.box.w)}|${r4(it.box.h)}|${it.fill ? it.fill.color + it.fill.alpha : ''}`;
  if (it.type === 'snap' && it.file) return `I|${r4(it.img.x)}|${r4(it.img.y)}|${md5(path.join(IMG, it.file))}`;
  if (it.type === 'asset') return `A|${it.src}|${r4(it.cx)}|${r4(it.cy)}|${r4(it.w0)}|${it.rot}`;
  return null;
}
let prevSigs = new Set();
const anims = [], geo = [];
for (const s of scene) {
  const sigs = new Set(s.items.filter(it => !it.skip).map(sig).filter(Boolean));
  const slide = pres.addSlide();
  slide.background = { color: s.dark ? '014A4D' : 'FFFFFF' };
  const sAn = { n: s.n, tr: s.tr, items: [] };
  const sGeo = { n: s.n, shapes: {} };
  for (const it of s.items) {
    if (it.skip) continue;
    const name = it.name || `s${s.n}-${it.type}-${it.k}`;
    const a = it.anim;
    if (a && !prevSigs.has(sig(it))) sAn.items.push({ name, a: a.a, d: a.d, t: a.t, type: it.type });
    if (it.anim2) sAn.items.push({ name, a: it.anim2, d: 0, loop: true, type: it.type });
    if (it.type === 'bg') { slide.background = { path: path.join(IMG, it.file) }; continue; }
    if (it.type === 'snap') {
      slide.addImage({ path: path.join(IMG, it.file), x: it.img.x * PX, y: it.img.y * PX, w: it.img.w * PX, h: it.img.h * PX, objectName: name, altText: '' });
      continue;
    }
    if (it.type === 'asset') {
      const f = path.join(IMG, 'asset_' + it.src.replace(/\//g, '_') + '.png');
      const alt = it.src.startsWith('logo') ? 'شعار أرض البساتين' : '';
      const o = { path: f, x: (it.cx - it.w0 / 2) * PX, y: (it.cy - it.h0 / 2) * PX, w: it.w0 * PX, h: it.h0 * PX, objectName: name, altText: alt };
      if (it.rot) o.rotate = it.rot;
      if (it.opacity < 1) o.transparency = Math.round((1 - it.opacity) * 100);
      slide.addImage(o);
      continue;
    }
    if (it.type === 'shape') {
      const b = it.box, minS = Math.min(b.w, b.h);
      const [tl, tr, br, bl] = it.radii || [0, 0, 0, 0];
      let shp = pres.shapes.RECTANGLE; const o = { x: b.x * PX, y: b.y * PX, w: b.w * PX, h: b.h * PX, objectName: name };
      const eq = (p, q) => Math.abs(p - q) < 1.5;
      if (eq(tl, tr) && eq(tr, br) && eq(br, bl)) {
        if (tl >= minS / 2 - 1) {
          shp = Math.abs(b.w - b.h) < 2 ? pres.shapes.OVAL : pres.shapes.ROUNDED_RECTANGLE;
          if (shp !== pres.shapes.OVAL) o.rectRadius = (minS / 2) * PX;
        } else if (tl > 0) { shp = pres.shapes.ROUNDED_RECTANGLE; o.rectRadius = tl * PX; }
      } else if (eq(tl, br) && eq(br, bl) && tr < 1 && tl >= minS / 2 - 1) {
        shp = 'teardrop'; sGeo.shapes[name] = { prst: 'teardrop', adj: { adj: 100000 } };
      } else if (eq(tl, br) && eq(tr, bl)) {
        shp = 'round2DiagRect';
        sGeo.shapes[name] = { prst: 'round2DiagRect', adj: { adj1: Math.round(Math.min(.5, tl / minS) * 100000), adj2: Math.round(Math.min(.5, tr / minS) * 100000) } };
      } else if (tl > 0) { shp = pres.shapes.ROUNDED_RECTANGLE; o.rectRadius = tl * PX; }
      o.fill = it.fill ? { color: it.fill.color, transparency: Math.round((1 - it.fill.alpha) * 100) } : { type: 'none' };
      o.line = it.border ? { color: it.border.color, width: it.border.w * PT } : { type: 'none' };
      if (it.shadow) o.shadow = { type: 'outer', color: '013B3E', opacity: 0.12, blur: 24, offset: 8, angle: 90 };
      slide.addShape(shp, o);
      continue;
    }
    if (it.type === 'text') {
      const runs = [];
      it.lines.forEach((line, li) => line.forEach((r, ri) => {
        const op = { color: r.color, fontSize: Math.round(r.size * PT * 2) / 2, fontFace: FACE[r.weight] || 'Alexandria', bold: r.weight === 700,
          rtlMode: it.dir === 'rtl', align: it.align, lineSpacing: it.lh * PT, breakLine: ri === line.length - 1 && li < it.lines.length - 1 };
        if (r.ls) op.charSpacing = r.ls * PT;
        runs.push({ text: r.text, options: op });
      }));
      const b = it.box;
      const slack = Math.max(16, b.w * 0.08);
      let x = b.x, w = b.w + slack;
      if (it.align === 'right') x = b.x - slack;
      else if (it.align === 'center') x = b.x - slack / 2;
      const h = it.lines.length * it.lh + 8;
      // align PowerPoint's first baseline with the browser's (calibrated, see calib.json)
      const fs0 = Math.max(...it.lines[0].map(r => r.size));
      const dy = CAL.a * it.lh + CAL.b * fs0;
      const top = it.cy0 != null ? it.cy0 - it.lh / 2 : b.y;
      slide.addText(runs, {
        x: x * PX, y: (top - dy) * PX, w: w * PX, h: h * PX, fontFace: 'Alexandria', margin: 0, valign: 'top',
        align: it.align, rtlMode: it.dir === 'rtl', lang: it.dir === 'rtl' ? 'ar-SA' : 'en-US',
        lineSpacing: it.lh * PT, paraSpaceBefore: 0, paraSpaceAfter: 0, isTextBox: true, objectName: name, fit: 'none', wrap: true,
      });
      continue;
    }
    if (it.type === 'chart') {
      const b = it.box;
      slide.addChart(pres.charts.DOUGHNUT, [{ name: it.chart.name || 'التوزيع', labels: it.chart.labels, values: it.chart.values }], {
        x: b.x * PX, y: b.y * PX, w: b.w * PX, h: b.h * PX, objectName: name, holeSize: it.chart.hole || 58, chartColors: it.chart.colors,
        showLegend: false, showValue: false, showPercent: false, showLabel: false, showTitle: false, firstSliceAng: 0,
        dataBorder: { pt: 4, color: it.chart.border || 'FFFFFF' }, plotArea: { fill: { color: 'FFFFFF', transparency: 100 } },
      });
      continue;
    }
  }
  anims.push(sAn); geo.push(sGeo);
  prevSigs = sigs;
}
fs.writeFileSync(path.join(OUT, 'anims.json'), JSON.stringify(anims));
fs.writeFileSync(path.join(OUT, 'geo.json'), JSON.stringify(geo));
pres.writeFile({ fileName: outFile }).then(f => console.log('wrote', f));
