# -*- coding: utf-8 -*-
"""Generates the brand graphics used by the deck:
   * leaf.json  - the two leaves of the logo, traced from logo.png as smooth vector paths
   * topo_*.svg - topographic contour lines (the "land" in أرض البساتين)
   * grain.png  - a soft film grain tile
   * yemen.json - map outline (Natural Earth 1:50m, public domain) + city points
"""
import json, os, sys
import numpy as np, cv2
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(BASE, 'assets')


def smooth_path(pts, closed=True, t=0.5):
    """Catmull-Rom -> cubic Bezier path string."""
    n = len(pts)
    P = lambda i: pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = P(i - 1), P(i), P(i + 1), P(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d + (' Z' if closed else '')


# ------------------------------------------------------------------ leaves
def leaves():
    im = cv2.imread(os.path.join(A, 'logo.png'), cv2.IMREAD_UNCHANGED)
    hsv = cv2.cvtColor(im[:, :, :3], cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0].astype(int) * 2, hsv[..., 1].astype(int), hsv[..., 2].astype(int)
    m = ((H >= 85) & (H <= 138) & (S > 60)) | ((H > 138) & (H <= 152) & (S > 215) & (V > 135))
    m = (m & (im[..., 3] > 0)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    big = 1 + int(np.argmax(st[1:, 4]))
    m = (lab == big).astype(np.uint8) * 255
    # fill holes (water-drop highlights)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m = np.zeros_like(m); cv2.drawContours(m, cs, -1, 255, -1)
    m = (cv2.GaussianBlur(m, (0, 0), 5) > 127).astype(np.uint8) * 255   # soften the anti-aliasing steps
    # junction = lowest point of the mask in the middle band
    ys, xs = np.nonzero(m)
    band = (xs > 820) & (xs < 1000)
    jy = ys[band].max(); jx = int(np.median(xs[band][ys[band] >= jy - 3]))
    out = {}
    for side in ('L', 'R'):
        mm = m.copy()
        if side == 'L': mm[:, jx + 2:] = 0
        else: mm[:, :jx - 2] = 0
        cs, _ = cv2.findContours(mm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(cs, key=cv2.contourArea)
        c = cv2.approxPolyDP(c, 3.2, True)[:, 0, :].astype(float)
        out[side] = c.tolist()
    xs_all = [p[0] for s in out.values() for p in s]; ys_all = [p[1] for s in out.values() for p in s]
    x0, y0, x1, y1 = min(xs_all), min(ys_all), max(xs_all), max(ys_all)
    res = {'box': [x0, y0, x1, y1], 'junction': [jx, int(jy)]}
    for side, pts in out.items():
        pts = [(p[0] - x0, p[1] - y0) for p in pts]
        res[side] = smooth_path(pts)
    # veins: base (junction) -> tip, bowed like the logo
    jx0, jy0 = jx - x0, jy - y0
    tipL = min(out['L'], key=lambda p: p[0] + p[1] * .2); tipL = (tipL[0] - x0, tipL[1] - y0)
    tipR = max(out['R'], key=lambda p: p[0] - p[1] * .2); tipR = (tipR[0] - x0, tipR[1] - y0)
    res['VL'] = f'M{jx0 - 8:.0f},{jy0 - 30:.0f} Q{jx0 - 150:.0f},{(jy0 + tipL[1]) / 2 - 40:.0f} {tipL[0] + 40:.0f},{tipL[1] + 22:.0f}'
    res['VR'] = f'M{jx0 + 22:.0f},{jy0 - 26:.0f} Q{(jx0 + tipR[0]) / 2 + 40:.0f},{(jy0 + tipR[1]) / 2 + 60:.0f} {tipR[0] - 60:.0f},{tipR[1] + 44:.0f}'
    res['w'], res['h'] = x1 - x0, y1 - y0
    json.dump(res, open(os.path.join(A, 'leaf.json'), 'w'))
    print('leaf', res['w'], res['h'], 'junction', jx, jy)


# ------------------------------------------------------------------ topographic lines
def topo(name, W=2880, H=1620, seed=7, levels=16, stroke='#000', sw=2.0, op=1.0, every=4, bold_sw=None):
    rng = np.random.default_rng(seed)
    s = 6
    w, h = W // s, H // s
    f = np.zeros((h, w))
    yy, xx = np.mgrid[0:h, 0:w]
    for _ in range(26):  # a landscape of soft hills
        cx, cy = rng.uniform(-.1, 1.1) * w, rng.uniform(-.1, 1.1) * h
        r = rng.uniform(.08, .32) * w
        f += rng.uniform(.4, 1.0) * np.exp(-(((xx - cx) ** 2) / (2 * r * r) + ((yy - cy) ** 2) / (2 * (r * rng.uniform(.6, 1.4)) ** 2)))
    noise = cv2.GaussianBlur(rng.normal(0, 1, (h, w)), (0, 0), 9)
    f += noise * .25
    f = (f - f.min()) / (f.max() - f.min())
    from skimage import measure
    paths = []
    for k, lv in enumerate(np.linspace(.06, .96, levels)):
        for c in measure.find_contours(f, lv):
            if len(c) < 12:
                continue
            pts = [(p[1] * s, p[0] * s) for p in c[::2]]
            closed = np.hypot(c[0][0] - c[-1][0], c[0][1] - c[-1][1]) < 2
            d = smooth_path(pts, closed=closed)
            wdt = bold_sw if (bold_sw and k % every == 0) else sw
            paths.append(f'<path d="{d}" stroke-width="{wdt}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           f'<g fill="none" stroke="{stroke}" stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round">'
           + ''.join(paths) + '</g></svg>')
    open(os.path.join(A, f'topo_{name}.svg'), 'w').write(svg)
    print('topo', name, len(paths))


# ------------------------------------------------------------------ grain
def grain():
    rng = np.random.default_rng(3)
    n = rng.normal(128, 46, (420, 420)).clip(0, 255).astype(np.uint8)
    a = np.full_like(n, 255)
    Image.fromarray(np.dstack([n, n, n, a]), 'RGBA').save(os.path.join(A, 'grain.png'))


# ------------------------------------------------------------------ yemen
def yemen():
    g = json.load(open(sys.argv[1]))
    polys = [p[0] for p in g['coordinates']] if g['type'] == 'MultiPolygon' else [g['coordinates'][0]]
    k = np.cos(np.radians(15))
    allp = [(x * k, -y) for poly in polys for x, y in poly]
    x0, y0 = min(p[0] for p in allp), min(p[1] for p in allp)
    x1, y1 = max(p[0] for p in allp), max(p[1] for p in allp)
    sc = 1000 / (x1 - x0)
    tr = lambda lon, lat: ((lon * k - x0) * sc, (-lat - y0) * sc)
    ds = []
    for poly in sorted(polys, key=len, reverse=True):
        pts = [tr(x, y) for x, y in poly]
        ds.append('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z')
    cities = {'صنعاء': (44.2066, 15.3694), 'الحديدة': (42.9545, 14.7978), 'ذمار': (44.4058, 14.5427)}
    res = {'w': 1000, 'h': round((y1 - y0) * sc, 1), 'd': ds, 'cities': {c: tr(*v) for c, v in cities.items()}}
    json.dump(res, open(os.path.join(A, 'yemen.json'), 'w'), ensure_ascii=False)
    print('yemen', res['h'], res['cities'])


if __name__ == '__main__':
    leaves()
    topo('light', seed=11, stroke='#2E9E63', sw=1.6, op=.15, bold_sw=2.6)
    topo('dark', seed=11, stroke='#FFFFFF', sw=1.6, op=.10, bold_sw=2.6)
    topo('earth', seed=23, stroke='#8A5A3B', sw=1.6, op=.16, bold_sw=2.6)
    topo('lime', seed=5, stroke='#C3E36B', sw=1.8, op=.22, bold_sw=3)
    grain()
    yemen()
