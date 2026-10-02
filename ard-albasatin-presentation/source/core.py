# -*- coding: utf-8 -*-
"""Design system for the Ard Albasatin deck: source text access, palette, type scale,
brand motifs (traced leaves, topographic land, drip line) and the slide frame."""
import json, re, html, os, math

BASE = os.path.dirname(os.path.abspath(__file__))
_SRC = json.load(open(os.path.join(BASE, 'paras.json')))
P = {int(k): v for k, v in _SRC['p'].items()}
TB = {int(k): v for k, v in _SRC['t'].items()}
LEAF = json.load(open(os.path.join(BASE, 'assets/leaf.json')))
YEM = json.load(open(os.path.join(BASE, 'assets/yemen.json')))
ICON_DIR = os.path.join(BASE, 'build/node_modules/@phosphor-icons/core/assets/duotone')
GEN = os.path.join(BASE, 'assets/gen')
os.makedirs(GEN, exist_ok=True)
USED = set()   # paragraph indices quoted on slides (coverage check)


# ------------------------------------------------------------------ source text
def clean(s):
    s = s.replace('\xa0', ' ').replace('\t', ' ')
    s = re.sub(r'[ ]{2,}', ' ', s)
    return s.strip()


def T(i, colon=True):
    """Exact paragraph text. colon=False drops a trailing heading colon (typographic only)."""
    USED.add(i)
    s = clean(P[i].replace('\n', ' '))
    if not colon:
        s = re.sub(r'\s*[:：]\s*$', '', s)
    return s


def L(i):
    """Lines of a paragraph that holds soft line breaks."""
    USED.add(i)
    return [clean(x) for x in P[i].split('\n') if clean(x)]


def e(s):
    return html.escape(s, quote=False)


def kv(s):
    m = re.match(r'^(.*?)\s*:\s*(.*)$', s)
    return (clean(m.group(1)), clean(m.group(2))) if m else (s, '')


# ------------------------------------------------------------------ palette
C = dict(
    teal='#015256', teal9='#013B3E', forest='#01804C', leaf='#029C3F', brand='#35B86E',
    lime='#C3E36B', mint='#E3F3E9', mint2='#F2F9F5', aqua='#5CC4BC',
    soil='#5E3F2A', brown='#8A6142', clay='#C29A74', sand='#F6EFE6', sand2='#EBDFCF',
    ink='#0E3A3C', mut='#557274', line='#D5E6DC', w='#FFFFFF')


# ------------------------------------------------------------------ icons (Phosphor, duotone, MIT)
def icon(name, fg=None, du=None, size=64, duop=1):
    fg = fg or C['teal']
    du = du or C['lime']
    weight = 'fill' if name.endswith('-logo') else 'duotone'
    svg = open(os.path.join(ICON_DIR, '..', weight, f'{name}-{weight}.svg')).read()
    svg = svg.replace(' fill="currentColor"', '')

    def paint(m):
        tag = m.group(0)
        if 'opacity="0.2"' in tag:
            return tag.replace('<path ', f'<path fill="{du}" ', 1).replace('opacity="0.2"', f'opacity="{duop}"')
        return tag.replace('<path ', f'<path fill="{fg}" ', 1)
    svg = re.sub(r'<path [^>]*>', paint, svg)
    svg = svg.replace('<svg ', f'<svg width="{size}" height="{size}" style="display:block" ', 1)
    return svg


def ico(name, x, y, s=96, tile='mint', fg=None, du=None, isz=None, shape='drop', a='pop', d=0, name_=''):
    """Icon on a water-drop (teardrop) tile. Tile and icon are separate objects (native shape + picture)."""
    bg = C.get(tile, tile)
    isz = isz or int(s * .56)
    fg = fg or (C['teal'] if tile in ('mint', 'lime', 'w', 'sand', 'sand2', 'mint2') else '#FFFFFF')
    du = du or (C['brand'] if tile in ('mint', 'w', 'mint2', 'sand', 'sand2') else (C['forest'] if tile == 'lime' else C['lime']))
    cls = {'drop': 'tile-drop', 'circle': 'tile-circ', 'leaf': 'tile-leaf'}[shape]
    an = f' data-a="{a}" data-d="{d}"' if a else ''
    nm = f' data-name="{name_}"' if name_ else ''
    return (f'<div class="abs {cls}" data-x="shape"{an}{nm} style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{bg}"></div>'
            f'<div class="abs" data-x="snap"{an} style="left:{x + (s - isz) / 2:.1f}px;top:{y + (s - isz) / 2:.1f}px;width:{isz}px;height:{isz}px">{icon(name, fg, du, isz)}</div>')


# ------------------------------------------------------------------ leaf glyph (traced from the logo)
def leaf_svg(variant):
    """Writes assets/gen/leafL_<v>.svg and leafR_<v>.svg (each holds one leaf in the shared glyph box)."""
    pal = {
        'g': (C['brand'], C['leaf'], 'rgba(255,255,255,.55)'),
        'w': ('#FFFFFF', '#FFFFFF', C['brand']),
        'lime': (C['lime'], C['lime'], C['forest']),
        'mint': ('#D3ECDD', '#C2E5D0', '#FFFFFF'),
        'dk': ('#0B6A63', '#0E7A6E', '#0D5C58'),
        'soil': (C['clay'], C['brown'], 'rgba(255,255,255,.5)'),
    }[variant]
    W, H = LEAF['w'], LEAF['h']
    for side, col, vein in (('L', pal[0], 'VL'), ('R', pal[1], 'VR')):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
               f'<path d="{LEAF[side]}" fill="{col}"/>'
               f'<path d="{LEAF[vein]}" fill="none" stroke="{pal[2]}" stroke-width="9" stroke-linecap="round"/></svg>')
        open(os.path.join(GEN, f'leaf{side}_{variant}.svg'), 'w').write(svg)


for _v in ('g', 'w', 'lime', 'mint', 'dk', 'soil'):
    leaf_svg(_v)
LW, LH = LEAF['w'], LEAF['h']


def leaves(x, y, h, rot=0, v='g', spread=0, a=None, d=0, names=('!!leafL', '!!leafR'), op=1, z=1, sway=False):
    """Both leaves as separate pictures so Morph can grow / open them between slides."""
    w = h * LW / LH
    out = ''
    for k, side in enumerate(('L', 'R')):
        dx = (-spread if side == 'L' else spread)
        dy = (spread * .35 if side == 'L' else -spread * .2)
        an = ''
        if a:
            an = f' data-a="{a}" data-d="{d + k * 160}"'
        if sway:
            an += f' data-a2="sway{side}"'
        out += (f'<img class="abs" src="assets/gen/leaf{side}_{v}.svg" data-x="asset" data-src="gen/leaf{side}_{v}" data-name="{names[k]}"{an}'
                f' style="left:{x + dx:.1f}px;top:{y + dy:.1f}px;width:{w:.1f}px;height:{h:.1f}px;transform:rotate({rot}deg);opacity:{op};z-index:{z}">')
    return out


# ------------------------------------------------------------------ CSS
CSS = r"""
@font-face{font-family:"AX";src:url(../fonts/Alexandria-Thin.ttf) format("truetype");font-weight:100}
@font-face{font-family:"AX";src:url(../fonts/Alexandria-ExtraLight.ttf) format("truetype");font-weight:200}
@font-face{font-family:"AX";src:url(../fonts/Alexandria-Light.ttf) format("truetype");font-weight:300}
@font-face{font-family:"AX";src:url(../fonts/Alexandria-Regular.ttf) format("truetype");font-weight:400}
@font-face{font-family:"AX";src:url(../fonts/Alexandria-Medium.ttf) format("truetype");font-weight:500}
@font-face{font-family:"AX";src:url(../fonts/Alexandria-SemiBold.ttf) format("truetype");font-weight:600}
@font-face{font-family:"AX";src:url(../fonts/Alexandria-Bold.ttf) format("truetype");font-weight:700}
@font-face{font-family:"AX";src:url(../fonts/Alexandria-ExtraBold.ttf) format("truetype");font-weight:800}
@font-face{font-family:"AX";src:url(../fonts/Alexandria-Black.ttf) format("truetype");font-weight:900}
:root{--teal:#015256;--teal9:#013B3E;--forest:#01804C;--leaf:#029C3F;--brand:#35B86E;--lime:#C3E36B;--mint:#E3F3E9;--mint2:#F2F9F5;
 --aqua:#5CC4BC;--soil:#5E3F2A;--brown:#8A6142;--clay:#C29A74;--sand:#F6EFE6;--sand2:#EBDFCF;--ink:#0E3A3C;--mut:#557274;--line:#D5E6DC}
*{box-sizing:border-box;margin:0;padding:0}
@page{size:1920px 1080px;margin:0}
html,body{background:#fff}
body{font-family:"AX",sans-serif;direction:rtl;color:var(--ink);font-synthesis:none;-webkit-font-smoothing:antialiased;
 font-feature-settings:"kern","liga","calt","rlig","mark","mkmk";text-rendering:geometricPrecision}
.slide{position:relative;width:1920px;height:1080px;overflow:hidden;background:#fff;break-after:page;page-break-after:always}
.abs{position:absolute}
.w1{font-weight:100}.w2{font-weight:200}.w3{font-weight:300}.w4{font-weight:400}.w5{font-weight:500}
.w6{font-weight:600}.w7{font-weight:700}.w8{font-weight:800}.w9{font-weight:900}
.lat{direction:ltr;unicode-bidi:isolate}
.num{font-feature-settings:"kern","lnum"}
/* ---------- backgrounds */
.bgfill{position:absolute;inset:0}
.bg-L{background:radial-gradient(900px 700px at 0% 0%,#E9F6EE 0%,rgba(233,246,238,0) 70%),radial-gradient(800px 600px at 100% 100%,#F1F8F3 0%,rgba(241,248,243,0) 70%),#fff}
.bg-D{background:radial-gradient(1100px 820px at 8% 100%,rgba(2,156,63,.42) 0%,rgba(2,156,63,0) 62%),radial-gradient(900px 700px at 100% 0%,rgba(92,196,188,.20) 0%,rgba(92,196,188,0) 60%),linear-gradient(160deg,#015A5E 0%,#013B3E 100%)}
.bg-E{background:radial-gradient(1000px 760px at 0% 100%,#EADCC9 0%,rgba(234,220,201,0) 65%),radial-gradient(800px 600px at 100% 0%,#FBF7F1 0%,rgba(251,247,241,0) 70%),#F6EFE6}
.bg-G{background:radial-gradient(1000px 800px at 100% 0%,rgba(195,227,107,.35) 0%,rgba(195,227,107,0) 60%),linear-gradient(150deg,#029C3F 0%,#01804C 100%)}
.grain{position:absolute;inset:0;background:url(assets/grain.png);opacity:.045;mix-blend-mode:multiply}
.D .grain,.G .grain{opacity:.07;mix-blend-mode:overlay}
.D,.G{color:#fff}
/* ---------- frame */
.kick{position:absolute;right:110px;top:62px;font-size:26px;line-height:1.3;color:var(--mut);white-space:nowrap}
.kick b{font-weight:900;color:var(--leaf);margin-left:14px}
.D .kick,.G .kick{color:rgba(255,255,255,.72)} .D .kick b{color:var(--lime)} .G .kick b{color:var(--lime)}
.E .kick b{color:var(--brown)}
.pg{position:absolute;left:206px;top:62px;font-size:26px;line-height:1.3;color:var(--mut);direction:ltr}
.pg b{font-weight:900;color:var(--ink)}
.D .pg,.G .pg{color:rgba(255,255,255,.6)} .D .pg b,.G .pg b{color:#fff}
/* ---------- type */
.eyb{color:var(--leaf)} .D .eyb,.G .eyb{color:var(--lime)} .E .eyb{color:var(--brown)}
.ttl{position:absolute;right:110px;top:132px;font-size:84px;line-height:1.28;font-weight:800;color:var(--ink);white-space:nowrap}
.ttl i{font-style:normal;font-weight:200;color:var(--forest)}
.D .ttl,.G .ttl{color:#fff} .D .ttl i{color:var(--lime)} .G .ttl i{color:var(--lime)}
.E .ttl i{color:var(--brown)}
.lead{font-size:40px;line-height:1.62;font-weight:300}
.body{font-size:33px;line-height:1.6;font-weight:400}
.sm{font-size:28px;line-height:1.55;font-weight:400}
.lbl{font-size:28px;line-height:1.35;font-weight:600;color:var(--forest)}
.mut{color:var(--mut)}
.D .mut{color:rgba(255,255,255,.72)}
/* ---------- shapes */
.card{position:absolute;border-radius:28px;background:#fff}
.card.mint{background:var(--mint)} .card.mint2{background:var(--mint2)} .card.sand{background:var(--sand)} .card.sand2{background:var(--sand2)}
.card.teal{background:var(--teal)} .card.forest{background:var(--forest)} .card.lime{background:var(--lime)} .card.brown{background:var(--brown)}
.card.shadow{box-shadow:0 22px 60px rgba(1,59,62,.10),0 3px 10px rgba(1,59,62,.05)}
.card.glass{background:rgba(255,255,255,.08)}
.card.line{background:transparent;border:2px solid var(--line)}
.leafcard{border-radius:72px 10px 72px 10px}
.tile-drop{border-radius:50% 0 50% 50%}
.tile-circ{border-radius:50%}
.tile-leaf{border-radius:50% 6% 50% 6%}
.pill{border-radius:999px}
.dot{position:absolute;border-radius:50%}
"""


# ------------------------------------------------------------------ frame
NSLIDES = [0]


def topo_pos(n):
    return (-240 - 230 * math.sin(n * .62), -135 - 125 * math.cos(n * .47))


def frame(n, mode='L', sec=None, topo=True, pg=True, mark=True, topo_v=None):
    """Background, drifting topographic layer, section kicker, page number, leaf mark."""
    tv = topo_v or {'L': 'light', 'D': 'dark', 'E': 'earth', 'G': 'lime'}[mode]
    out = f'<div class="bgfill bg-{mode}" data-x="bg"><div class="grain"></div></div>'
    if topo:
        tx, ty = topo_pos(n)
        out += (f'<img class="abs" src="assets/topo_{tv}.svg" data-x="asset" data-src="topo_{tv}" data-name="!!topo"'
                f' style="left:{tx:.0f}px;top:{ty:.0f}px;width:2880px;height:1620px">')
    if sec:
        num, title = sec
        nb = f'<b class="num">{num}</b>' if num else ''
        out += f'<div class="kick" data-x="text" data-name="!!kick">{nb}{e(title)}</div>'
    if pg:
        out += f'<div class="pg num" data-x="text" data-name="!!pg"><b>{n:02d}</b> / {NTOTAL}</div>'
    if mark:
        v = {'L': 'g', 'D': 'g', 'E': 'soil', 'G': 'w'}[mode]
        out += leaves(110, 62, 34, v=v)
    return out


NTOTAL = 60


def title(txt_light, txt_bold, top=132, right=110, size=84, a='wipeR', d=150, extra='', order='lb', name=''):
    """Two-weight title: a thin word set against an extra-bold word."""
    lt = f'<i>{e(txt_light)}</i>' if txt_light else ''
    bd = e(txt_bold)
    inner = f'{lt} {bd}' if order == 'lb' else f'{bd} {lt}'
    nm = f' data-name="{name}"' if name else ''
    return (f'<h2 class="ttl" data-x="text" data-a="{a}" data-d="{d}"{nm} style="top:{top}px;right:{right}px;font-size:{size}px;{extra}">{inner.strip()}</h2>')


def text(x, y, w, inner, cls='body', a='rise', d=300, style='', name='', tag='div', align=None):
    """Positioned text block. x = right edge offset (RTL), y = top, w = width."""
    al = f'text-align:{align};' if align else ''
    nm = f' data-name="{name}"' if name else ''
    an = f' data-a="{a}" data-d="{d}"' if a else ''
    return f'<{tag} class="abs {cls}" data-x="text"{an}{nm} style="right:{x}px;top:{y}px;width:{w}px;{al}{style}">{inner}</{tag}>'


def textl(x, y, w, inner, cls='body', a='rise', d=300, style='', name='', align=None):
    """Same as text() but positioned from the left edge."""
    al = f'text-align:{align};' if align else ''
    nm = f' data-name="{name}"' if name else ''
    an = f' data-a="{a}" data-d="{d}"' if a else ''
    return f'<div class="abs {cls}" data-x="text"{an}{nm} style="left:{x}px;top:{y}px;width:{w}px;{al}{style}">{inner}</div>'


def box(x, y, w, h, cls='card', a='rise', d=200, style='', name='', right=False):
    an = f' data-a="{a}" data-d="{d}"' if a else ''
    nm = f' data-name="{name}"' if name else ''
    pos = f'right:{x}px' if right else f'left:{x}px'
    return f'<div class="{cls}" data-x="shape"{an}{nm} style="{pos};top:{y}px;width:{w}px;height:{h}px;{style}"></div>'


def dot(x, y, s, color, a='pop', d=0, name='', right=False):
    an = f' data-a="{a}" data-d="{d}"' if a else ''
    nm = f' data-name="{name}"' if name else ''
    pos = f'right:{x}px' if right else f'left:{x}px'
    return f'<div class="dot" data-x="shape"{an}{nm} style="{pos};top:{y}px;width:{s}px;height:{s}px;background:{color}"></div>'


def snap(x, y, w, h, inner, a='fade', d=0, name='', style=''):
    an = f' data-a="{a}" data-d="{d}"' if a else ''
    nm = f' data-name="{name}"' if name else ''
    return f'<div class="abs" data-x="snap"{an}{nm} style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}">{inner}</div>'


def dripline(x, y, w, color='#35B86E', emit='#35B86E', step=46, sw=3, a='wipeR', d=0, name='', vertical=False, op=1):
    """Drip-irrigation tape: a thin line with emitters at a steady pitch (the deck's connector)."""
    if vertical:
        n = int(w // step)
        dots = ''.join(f'<circle cx="8" cy="{8 + i * step}" r="5.5" fill="{emit}"/>' for i in range(n + 1))
        svg = (f'<svg width="16" height="{w + 16}" viewBox="0 0 16 {w + 16}"><line x1="8" y1="8" x2="8" y2="{w + 8}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" opacity="{op}"/>{dots}</svg>')
        return snap(x - 8, y - 8, 16, w + 16, svg, a=a, d=d, name=name)
    n = int(w // step)
    dots = ''.join(f'<circle cx="{8 + i * step}" cy="8" r="5.5" fill="{emit}"/>' for i in range(n + 1))
    svg = (f'<svg width="{w + 16}" height="16" viewBox="0 0 {w + 16} 16"><line x1="8" y1="8" x2="{w + 8}" y2="8" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" opacity="{op}"/>{dots}</svg>')
    return snap(x - 8, y - 8, w + 16, 16, svg, a=a, d=d, name=name)


def drop_svg(color, w=40, glint=True):
    h = w * 1.32
    g = f'<ellipse cx="{w * .36:.1f}" cy="{h * .64:.1f}" rx="{w * .09:.1f}" ry="{w * .16:.1f}" fill="#fff" opacity=".55"/>' if glint else ''
    return (f'<svg width="{w}" height="{h:.1f}" viewBox="0 0 {w} {h:.1f}"><path d="M{w / 2},0 C{w * .5},{h * .18} {w},{h * .45} {w},{h * .66} '
            f'A{w / 2},{w / 2} 0 0 1 0,{h * .66} C0,{h * .45} {w * .5},{h * .18} {w / 2},0 Z" fill="{color}"/>{g}</svg>')


def logo(x, y, s, a=None, d=0, name='!!logo', op=1):
    an = f' data-a="{a}" data-d="{d}"' if a else ''
    f = 'logo_sm.png' if s <= 120 else 'logo.png'
    return (f'<img class="abs" src="assets/{f}" data-x="asset" data-src="{f}" data-name="{name}"{an}'
            f' style="left:{x}px;top:{y}px;width:{s * 1984 / 2000:.1f}px;height:{s}px;opacity:{op}">')


def slide(mode, body, tr='morph', cls=''):
    return f'<section class="slide {mode} {cls}" data-tr="{tr}">{body}</section>'


def page(slides, title='أرض البساتين'):
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><base href="../"><title>{title}</title>'
            f'<style>{CSS}</style></head><body>' + ''.join(slides) + '</body></html>')


# ------------------------------------------------------------------ components
ORD = re.compile(r'^(أولًا|ثانيًا|ثالثًا|رابعًا|خامسًا|سادسًا)\s*:\s*')


def heading(s, k=1, size=84, a='wipeR', d=150, top=132, eyebrow_color=None):
    """Slide title from a source heading: optional ordinal eyebrow ('أولًا:'), first k words thin, rest extra-bold."""
    s = re.sub(r'\s*[:：]\s*$', '', s)
    out = ''
    m = ORD.match(s)
    if m:
        col = f'color:{eyebrow_color};' if eyebrow_color else ''
        out += (f'<div class="abs w6 eyb" data-x="text" data-a="fade" data-d="{d}" style="right:110px;top:{top - 4}px;font-size:30px;line-height:1.3;{col}">'
                f'{e(m.group(1))}</div>')
        s = s[m.end():]
        top += 44
    w = s.split(' ')
    lt, bd = ' '.join(w[:k]), ' '.join(w[k:])
    lt = re.sub(r'^(\d+)\.$', r'\1', lt)
    if not bd:
        lt, bd = '', lt
    return out + title(lt, bd, top=top, size=size, a=a, d=d)


_HB = {}


def _font(wt):
    """HarfBuzz font for a static weight (exact Arabic shaping for line-break estimates)."""
    import uharfbuzz as hb
    if wt not in _HB:
        name = {100: 'Thin', 200: 'ExtraLight', 300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold', 900: 'Black'}[wt]
        blob = hb.Blob.from_file_path(os.path.join(BASE, '..', 'fonts', f'Alexandria-{name}.ttf'))
        f = hb.Font(hb.Face(blob))
        _HB[wt] = (f, f.face.upem)
    return _HB[wt]


def text_width(t, fs, wt=400):
    import uharfbuzz as hb
    f, upem = _font(wt)
    buf = hb.Buffer()
    buf.add_str(t)
    buf.guess_segment_properties()
    hb.shape(f, buf, {'kern': True, 'liga': True})
    w = sum(p.x_advance for p in buf.glyph_positions) * fs / upem
    # emoji are drawn by the colour-emoji fallback font (~1.2em each), not by Alexandria
    emo, prev = 0, ''
    for ch in t:
        if (ord(ch) >= 0x1F000 or 0x2600 <= ord(ch) <= 0x27BF) and prev != '\u200d':
            emo += 1
        prev = ch
    return w + emo * fs * 1.2


def est_lines(t, fs, w, wt=400, k=None):
    """Line count of t at size fs in a box of width w, wrapping greedily on spaces like the browser."""
    words = t.split(' ')
    sp = text_width(' ', fs, wt)
    lines, cur = 1, 0
    for wd in words:
        ww = text_width(wd, fs, wt)
        if cur and cur + sp + ww > w:
            lines += 1
            cur = ww
        else:
            cur = cur + (sp if cur else 0) + ww
    return lines


def ilist(items, xr, y, w, rowh=None, fs=30, mk=None, bold=(), d0=300, step=90, lh=1.45, color=None, sep=False, sepc=None,
          a='rise', marker='drop', gap=None, maxh=None, minfs=24):
    """Bulleted list with water-drop markers. xr = right offset of the column.
    rowh=None: rows take the height of their text; maxh shrinks the type until the list fits."""
    mk = mk or C['brand']
    gap = gap if gap is not None else (30 if sep else 16)
    if rowh is None and maxh:
        while fs > minfs:
            ms = int(fs * .62)
            tot = sum(est_lines(t, fs, w - ms - 22, 700 if k in bold else 400) * fs * lh for k, t in enumerate(items)) + gap * (len(items) - 1)
            if tot <= maxh:
                break
            fs -= 1
    out = ''
    yy = y
    for k, it in enumerate(items):
        d = d0 + k * step
        ms = int(fs * .62)
        my = yy + fs * lh / 2 - ms / 2
        cls = 'tile-drop' if marker == 'drop' else 'tile-circ'
        out += f'<div class="abs {cls}" data-x="shape" data-a="pop" data-d="{d}" style="right:{xr}px;top:{my:.0f}px;width:{ms}px;height:{ms}px;background:{mk}"></div>'
        wt = 'w7' if k in bold else 'w4'
        col = f'color:{color};' if color else ''
        out += text(xr + ms + 22, yy, w - ms - 22, e(it), cls=wt, a=a, d=d + 30, style=f'font-size:{fs}px;line-height:{lh};{col}')
        h = rowh if rowh else est_lines(it, fs, w - ms - 22, 700 if k in bold else 400) * fs * lh + gap
        if sep and k < len(items) - 1:
            out += box(xr, yy + h - (gap / 2 if not rowh else 14) - 1, w, 2, cls='abs', a='wipeR', d=d, style=f'background:{sepc or C["line"]}', right=True)
        yy += h
    return out


def numlist(items, xr, y, w, rowh, fs=31, numc=None, bold=(), d0=300, step=80, cols=1, colgap=60, lh=1.42, start=1, sep=True, color=None, sepc=None):
    """Numbered rows (thin numerals) with hairline separators, flowing into columns."""
    numc = numc or C['brand']
    per = math.ceil(len(items) / cols)
    cw = (w - colgap * (cols - 1)) / cols
    out = ''
    for k, it in enumerate(items):
        c, r = k // per, k % per
        x = xr + c * (cw + colgap)
        yy = y + r * rowh
        d = d0 + k * step
        out += text(x, yy - 4, 92, f'{k + start:02d}', cls='w2 num', a='rise', d=d, style=f'font-size:{int(fs * 1.45)}px;line-height:1.2;color:{numc}')
        col = f'color:{color};' if color else ''
        out += text(x + 100, yy + 2, cw - 100, e(it), cls='w7' if k in bold else 'w4', a='rise', d=d + 40, style=f'font-size:{fs}px;line-height:{lh};{col}')
        if sep and r < per - 1 and k < len(items) - 1:
            out += box(x, yy + rowh - 12, cw, 2, cls='abs', a='wipeR', d=d, style=f'background:{sepc or C["line"]}', right=True)
    return out


def chip(xr, y, txt, bg, fg, fs=26, a='pop', d=0, pad=26, h=None, w=None, weight='w6'):
    """Pill label: native rounded shape + centered text."""
    h = h or int(fs * 1.9)
    w = w or int(len(txt) * fs * .52 + pad * 2)
    return (box(xr, y, w, h, cls='abs pill', a=a, d=d, style=f'background:{bg}', right=True)
            + text(xr, y + (h - fs * 1.3) / 2, w, e(txt), cls=weight, a=a, d=d + 20, align='center', style=f'font-size:{fs}px;line-height:1.3;color:{fg}'))
