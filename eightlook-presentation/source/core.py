# -*- coding: utf-8 -*-
"""Core helpers: source text access, icons, brand mark pieces, CSS."""
import json, re, html, os

BASE = os.path.dirname(os.path.abspath(__file__))
P = {int(k): v for k, v in json.load(open(os.path.join(BASE, 'paras.json'))).items()}
MARK = json.load(open(os.path.join(BASE, 'assets/mark/meta.json')))
ICON_DIR = os.path.join(BASE, 'build/node_modules/@phosphor-icons/core/assets/duotone')


def clean(s):
    s = s.replace('\xa0', ' ').replace('\t', ' ')
    s = re.sub(r'[ ]{2,}', ' ', s)
    return s.strip()


def T(i):
    """Whole paragraph text (single line)."""
    return clean(P[i].replace('\n', ' '))


def L(i):
    """Paragraph lines, bullet markers removed, empties dropped."""
    out = []
    for ln in P[i].split('\n'):
        ln = clean(ln)
        ln = re.sub(r'^•\s*', '', ln)
        if ln:
            out.append(ln)
    return out


def e(s):
    return html.escape(s, quote=False)


def kv(s):
    """Split 'label : value' at the first colon."""
    m = re.match(r'^(.*?)\s*:\s*(.*)$', s)
    return (clean(m.group(1)), clean(m.group(2))) if m else (s, '')


# ---------------------------------------------------------------- icons
def icon(name, fg='var(--b)', bg='var(--y)', size=64, cls='', bgop=.45):
    svg = open(os.path.join(ICON_DIR, f'{name}-duotone.svg')).read()
    svg = svg.replace('fill="currentColor"', '')
    svg = svg.replace('opacity="0.2"', f'fill="{bg}" opacity="{bgop}" class="du"', 1)
    svg = re.sub(r'<path d=', f'<path fill="{fg}" d=', svg)
    svg = svg.replace('<svg ', f'<svg width="{size}" height="{size}" class="ic {cls}" ', 1)
    return svg


# ---------------------------------------------------------------- brand mark (geometric rebuild of the logo)
FULL = MARK['full']
FW, FH = FULL[2] - FULL[0], FULL[3] - FULL[1]


def mark(x, y, h, rot=0, color='o', glint=None, names=None, spread=0, op=1, anim=None, z=0, pieces=('top', 'bot', 'arc')):
    """Place the logo mark pieces. (x,y)=top-left of the whole mark box, h=height px.
    Each piece is its own element (so PowerPoint Morph can move them independently)."""
    import math
    s = h / FH
    cx, cy = x + FW * s / 2, y + h / 2
    out = []
    glint = glint or color
    th = math.radians(rot)
    for k in pieces:
        bx0, by0, bx1, by1 = MARK[k]
        w, hh = (bx1 - bx0) * s, (by1 - by0) * s
        pcx = x + ((bx0 + bx1) / 2 - FULL[0]) * s
        pcy = y + ((by0 + by1) / 2 - FULL[1]) * s
        if spread and k != 'arc':
            d = spread * (-1 if k == 'top' else 1)
            pcx += d * 0.55
            pcy += d
        dx, dy = pcx - cx, pcy - cy
        rx = cx + dx * math.cos(th) - dy * math.sin(th)
        ry = cy + dx * math.sin(th) + dy * math.cos(th)
        col = glint if k == 'arc' else color
        nm = (names or {}).get(k, '')
        a = anim.get(k, '') if isinstance(anim, dict) else (anim or '')
        out.append(
            f'<img class="mk" src="assets/mark/{k}_{col}.svg" data-x="asset" data-src="mark/{k}_{col}"'
            + (f' data-name="{nm}"' if nm else '') + (f' {a}' if a else '')
            + f' style="left:{rx - w / 2:.1f}px;top:{ry - hh / 2:.1f}px;width:{w:.1f}px;height:{hh:.1f}px;'
            f'transform:rotate({rot}deg);opacity:{op};z-index:{z}">')
    return ''.join(out)


CSS = r"""
@font-face{font-family:"SS";src:url(assets/sakkal.otf) format("opentype");}
:root{
 --o:#FF8D26;--o2:#E9720C;--o3:#FFB15E;--ot:#FFF1E3;
 --b:#43644B;--b2:#859A8A;--b3:#36503C;--bt:#EEF2EF;--bl:#D9E0DB;
 --y:#F6C342;--y2:#F9D77A;--yt:#FFF7DE;
 --ink:#1E2A36;--mut:#5E6D7C;--line:#E4EBF2;--w:#fff;
}
*{box-sizing:border-box;margin:0;padding:0}
@page{size:1920px 1080px;margin:0}
html,body{background:#fff}
body{font-family:"SS",sans-serif;direction:rtl;color:var(--ink);
 font-feature-settings:"kern","liga","calt","rlig","mark","mkmk";
 font-synthesis:none;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
.slide{position:relative;width:1920px;height:1080px;overflow:hidden;background:#fff;break-after:page;page-break-after:always}
.abs{position:absolute}
.mk{position:absolute;display:block}
/* ---------- weights: the font ships one (Light) weight; heavier grades are built with a hairline stroke */
.w3{-webkit-text-stroke:0}
.w5{-webkit-text-stroke:.011em currentColor;paint-order:stroke fill}
.w7{-webkit-text-stroke:.026em currentColor;paint-order:stroke fill}
.w9{-webkit-text-stroke:.042em currentColor;paint-order:stroke fill}
.hollow{color:transparent!important;-webkit-text-stroke:5px var(--y)}
/* ---------- OpenType feature recipes */
.f-disp{font-feature-settings:"kern","liga","calt","rlig","mark","mkmk","ss01","ss07","dlig"}
.f-swash{font-feature-settings:"kern","liga","calt","rlig","mark","mkmk","ss06","dlig"}
.f-kash{font-feature-settings:"kern","liga","calt","rlig","mark","mkmk","ss01","ss18"}
.f-kash2{font-feature-settings:"kern","liga","calt","rlig","mark","mkmk","ss17","ss06"}
.f-num{font-feature-settings:"kern","tnum","lnum"}
.f-head{font-feature-settings:"kern","liga","calt","rlig","mark","mkmk","ss06","ss02"}
.lat{direction:ltr;unicode-bidi:isolate}
/* ---------- HUD (viewfinder) */
.hud-c{position:absolute;inset:34px;pointer-events:none}
.hud-c i{position:absolute;width:46px;height:46px;border-color:var(--bl);border-style:solid;border-width:0}
.hud-c i:nth-child(1){top:0;right:0;border-top-width:4px;border-right-width:4px;border-top-right-radius:14px}
.hud-c i:nth-child(2){top:0;left:0;border-top-width:4px;border-left-width:4px;border-top-left-radius:14px}
.hud-c i:nth-child(3){bottom:0;right:0;border-bottom-width:4px;border-right-width:4px;border-bottom-right-radius:14px}
.hud-c i:nth-child(4){bottom:0;left:0;border-bottom-width:4px;border-left-width:4px;border-bottom-left-radius:14px}
.dark .hud-c i{border-color:rgba(255,255,255,.35)}
.rec{position:absolute;left:100px;bottom:62px;display:flex;align-items:center;gap:14px;direction:ltr}
.rec .dot{width:16px;height:16px;border-radius:50%;background:var(--o)}
.rec .t{font-size:24px;letter-spacing:.14em;color:var(--mut);line-height:1}
.dark .rec .t{color:rgba(255,255,255,.8)}
.kicker{position:absolute;right:100px;top:58px;display:flex;align-items:center;gap:16px;font-size:30px;color:var(--o2);line-height:1.2}
.kicker .n{font-size:30px;color:var(--b)}
.dark .kicker{color:var(--y)} .dark .kicker .n{color:#fff}
.mini{position:absolute;left:96px;bottom:58px;height:40px}
/* ---------- type */
h1,h2,h3{font-weight:normal}
.title{position:absolute;right:100px;top:132px;font-size:76px;line-height:1.35;color:var(--ink)}
.title em{font-style:normal;color:var(--o2)}
.dark .title{color:#fff} .dark .title em{color:var(--y)}
.lead{font-size:36px;line-height:1.65;color:var(--ink)}
.body{font-size:32px;line-height:1.6}
.small{font-size:27px;line-height:1.55}
.mut{color:var(--mut)}
/* ---------- cards (bento) */
.card{position:absolute;border-radius:40px;background:var(--bt);padding:44px 48px}
.card.o{background:var(--o)}
.card.ot{background:var(--ot)}
.card.y{background:var(--y)}
.card.yt{background:var(--yt)}
.card.b{background:var(--b);color:#fff}
.card.w{background:#fff;box-shadow:0 18px 50px rgba(30,42,54,.08),0 2px 6px rgba(30,42,54,.05)}
.card.line{background:#fff;border:3px solid var(--line)}
.chip{display:inline-flex;align-items:center;gap:12px;border-radius:999px;padding:10px 26px;font-size:28px;line-height:1.3}
.ichip{display:flex;align-items:center;justify-content:center;border-radius:28px;flex:none}
/* ---------- dark slides */
.dark{color:#fff;background:var(--b)}
.bgfill{position:absolute;inset:0}
.bg-blue{background:radial-gradient(1200px 900px at 85% 10%,#5F7B66 0%,rgba(95,123,102,0) 60%),linear-gradient(135deg,#43644B 0%,#3A5841 100%)}
.bg-orange{background:radial-gradient(1100px 800px at 15% 90%,#FFB15E 0%,rgba(255,177,94,0) 60%),linear-gradient(135deg,#FF8D26 0%,#F57B14 100%)}
.grain{position:absolute;inset:0;background:url(assets/grain.png);opacity:.07}
"""


def hud(num, kicker_n='', kicker='', dark=False, mini=True):
    k = ''
    if kicker:
        k = (f'<div class="kicker" data-x="text" data-name="!!kick">'
             f'<span class="n w7 f-num">{kicker_n}</span><span class="w5">{e(kicker)}</span></div>')
    logo = 'logo_w' if dark else 'logo_ink'
    return (
        f'<div class="hud-c" data-x="snap" data-name="!!hud"><i></i><i></i><i></i><i></i></div>'
        f'<div class="rec"><span class="dot" data-x="shape" data-name="!!rec" data-a="blink"></span>'
        f'<span class="t" data-x="text" data-name="!!num">REC · {num:02d}</span></div>'
        + k
    )


def page(slides, title='نظرة ثمانية'):
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{CSS}</style></head><body>' + ''.join(slides) + '</body></html>')
