// Builds the .pptx from pptx_build/scene.json (geometry measured from the HTML design).
const path = require('path'), fs = require('fs');
const pptxgen = require(path.join(__dirname, 'build/node_modules/pptxgenjs'));

const ROOT = __dirname, OUT = path.join(ROOT, 'pptx_build'), IMG = path.join(OUT, 'img');
const scene = JSON.parse(fs.readFileSync(path.join(OUT, process.argv[2] || 'scene.json')));
const outFile = process.argv[3] || path.join(OUT, 'raw.pptx');
const PX = 1 / 144;              // inches per CSS px (1920px == 13.333in)
const PT = 0.5;                  // points per CSS px
const FONT = 'Sakkal Saad TN Trial Light';

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.rtlMode = true;
pres.title = 'الخطة التسويقية لمشروع نظرة ثمانية – Eightlook';
pres.author = 'زينب عبدالله الشراعي';

const anims = [];
for (const s of scene) {
  const slide = pres.addSlide();
  slide.background = { color: s.dark ? '2F6FA8' : 'FFFFFF' };
  const sAn = { n: s.n, tr: s.tr, items: [] };
  for (const it of s.items) {
    if (it.skip) continue;
    const name = it.name || `s${s.n}-${it.type}-${it.k}`;
    const a = it.anim;
    if (a) sAn.items.push({ name, a: a.a, d: a.d, t: a.t, type: it.type });
    if (it.type === 'bg') { slide.background = { path: path.join(IMG, it.file) }; continue; }
    if (it.type === 'snap') {
      slide.addImage({ path: path.join(IMG, it.file), x: it.img.x * PX, y: it.img.y * PX, w: it.img.w * PX, h: it.img.h * PX, objectName: name, altText: name });
      continue;
    }
    if (it.type === 'asset') {
      const f = path.join(IMG, 'asset_' + it.src.replace(/\//g, '_') + '.png');
      const o = { path: f, x: (it.cx - it.w0 / 2) * PX, y: (it.cy - it.h0 / 2) * PX, w: it.w0 * PX, h: it.h0 * PX, objectName: name, altText: it.src.includes('basmat') ? 'شعار بصمة وعي للتدريب' : 'شعار نظرة ثمانية' };
      if (it.rot) o.rotate = it.rot;
      if (it.opacity < 1) o.transparency = Math.round((1 - it.opacity) * 100);
      slide.addImage(o);
      continue;
    }
    if (it.type === 'shape') {
      const b = it.box, minS = Math.min(b.w, b.h);
      let shp = pres.shapes.RECTANGLE; const o = { x: b.x * PX, y: b.y * PX, w: b.w * PX, h: b.h * PX, objectName: name };
      if (it.radius >= minS / 2 - 1) {
        shp = Math.abs(b.w - b.h) < 2 ? pres.shapes.OVAL : pres.shapes.ROUNDED_RECTANGLE;
        if (shp !== pres.shapes.OVAL) o.rectRadius = (minS / 2) * PX;
      } else if (it.radius > 0) { shp = pres.shapes.ROUNDED_RECTANGLE; o.rectRadius = it.radius * PX; }
      o.fill = it.fill ? { color: it.fill.color, transparency: Math.round((1 - it.fill.alpha) * 100) } : { type: 'none' };
      o.line = it.border ? { color: it.border.color, width: it.border.w * PT } : { type: 'none' };
      if (it.shadow) o.shadow = { type: 'outer', color: '1E2A36', opacity: 0.10, blur: 20, offset: 6, angle: 90 };
      slide.addShape(shp, o);
      continue;
    }
    if (it.type === 'text') {
      const runs = [];
      it.lines.forEach((line, li) => line.forEach((r, ri) => runs.push({
        text: r.text, options: { color: r.color, fontSize: Math.round(r.size * PT * 2) / 2, bold: r.bold, rtlMode: it.dir === 'rtl', align: it.align, lineSpacing: it.lh * PT, breakLine: ri === line.length - 1 && li < it.lines.length - 1 }
      })));
      const b = it.box;
      const slack = Math.max(16, b.w * 0.08);
      let x = b.x, w = b.w + slack;
      if (it.align === 'right') x = b.x - slack;
      else if (it.align === 'center') x = b.x - slack / 2;
      const h = it.lines.length * it.lh + 8;
      // PowerPoint puts the first baseline ~0.83 of an "exact" line from the top; CSS centres the line box.
      const fs0 = Math.max(...it.lines[0].map(r => r.size));
      const dy = 0.33 * it.lh - 0.153 * fs0;
      const top = it.cy0 != null ? it.cy0 - it.lh / 2 : b.y;   // line box of the first measured line
      slide.addText(runs, {
        x: x * PX, y: (top - dy) * PX, w: w * PX, h: h * PX, fontFace: FONT, margin: 0, valign: 'top',
        align: it.align, rtlMode: it.dir === 'rtl', lang: it.dir === 'rtl' ? 'ar-SA' : 'en-US',
        lineSpacing: it.lh * PT, paraSpaceBefore: 0, paraSpaceAfter: 0, isTextBox: true, objectName: name, fit: 'none', wrap: true,
      });
      continue;
    }
    if (it.type === 'chart') {
      const b = it.box;
      slide.addChart(pres.charts.DOUGHNUT, [{ name: 'التوزيع', labels: it.chart.labels, values: it.chart.values }], {
        x: b.x * PX, y: b.y * PX, w: b.w * PX, h: b.h * PX, objectName: name, holeSize: 62, chartColors: it.chart.colors,
        showLegend: false, showValue: false, showPercent: false, showLabel: false, showTitle: false, firstSliceAng: 0,
        dataBorder: { pt: 3, color: 'FFFFFF' }, plotArea: { fill: { color: 'FFFFFF', transparency: 100 } },
      });
      continue;
    }
  }
  anims.push(sAn);
}
fs.writeFileSync(path.join(OUT, 'anims.json'), JSON.stringify(anims));
pres.writeFile({ fileName: outFile }).then(f => console.log('wrote', f));
