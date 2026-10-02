# -*- coding: utf-8 -*-
from core import *

SEC = {int(re.match(r'(\d+)\.', s).group(1)): clean(re.sub(r'^\d+\.\s*', '', s)) for s in L(26)}
MN = {'top': '!!mt', 'bot': '!!mb', 'arc': '!!ma'}


def A(kind, d=0, t=None):
    return f'data-a="{kind}" data-d="{d}"' + (f' data-t="{t}"' if t else '')


def strip_num(s):
    return clean(re.sub(r'^\d+\s*\.\s*', '', s))


# ---------------------------------------------------------------- shared frame for content slides
def frame(n, k, title, inner, cls='', kicker=None, rot=None, title_anim=None, dark=False, extra_css='', title_style='', bg=None):
    rot = (n * 45) % 360 if rot is None else rot
    kn = f'{k:02d}' if isinstance(k, int) else ''
    kt = kicker if kicker is not None else (SEC[k] if isinstance(k, int) else '')
    ttl = ''
    if title:
        ttl = f'<h2 class="title w7 f-head" style="{title_style}" data-x="text" {title_anim or A("wipeR", 0, 700)}>{title}</h2>'
    bg = f'<div class="bgfill bg-{bg or "blue"}" data-x="bg"></div><div class="grain"></div>' if (dark or bg) else ''
    return f'''
<section class="slide {'dark ' if dark else ''}{cls}" data-tr="morph">
 {bg}<style>{extra_css}</style>
 <div class="abs" style="left:58px;top:20px;width:190px;height:190px;border-radius:50%;background:{'rgba(255,255,255,.07)' if dark else 'var(--bt)'}" data-x="shape" data-name="!!lens"></div>
 {mark(108, 50, 130, rot, 'o', glint='y' if dark else 'o', names=MN)}
 {hud(n, kn, kt, dark=dark)}
 {ttl}
 {inner}
</section>'''


def chip_icon(name, box=96, isz=56, bg='var(--bt)', fg='var(--b)', du='var(--y)', r=28, anim='', extra=''):
    return (f'<div class="ichip" style="width:{box}px;height:{box}px;background:{bg};border-radius:{r}px;{extra}" data-x="snap" {anim}>'
            f'{icon(name, fg, du, isz)}</div>')


def bullet_list(items, size=32, gap=18, dot='var(--o)', color='inherit', d0=0, step=90, lh=1.5, w=None):
    out = ''
    for i, it in enumerate(items):
        out += (f'<div class="bl" style="gap:20px;margin-bottom:{gap}px" {A("rise", d0 + i * step)}>'
                f'<span class="bd" style="background:{dot};margin-top:{size * lh / 2 - 7:.0f}px" data-x="shape"></span>'
                f'<span style="font-size:{size}px;line-height:{lh};color:{color}" data-x="text">{e(it)}</span></div>')
    return f'<div class="blist">{out}</div>'


EXTRA_CSS = r"""
.bl{display:flex;align-items:flex-start}
.bd{flex:none;width:14px;height:14px;border-radius:50%}
.lbl{font-size:30px;line-height:1.3}
.h3{font-size:42px;line-height:1.35}
.focus{position:absolute;pointer-events:none}
.focus i{position:absolute;width:40px;height:40px;border:0 solid var(--o)}
.focus i:nth-child(1){top:0;right:0;border-top-width:5px;border-right-width:5px;border-top-right-radius:12px}
.focus i:nth-child(2){top:0;left:0;border-top-width:5px;border-left-width:5px;border-top-left-radius:12px}
.focus i:nth-child(3){bottom:0;right:0;border-bottom-width:5px;border-right-width:5px;border-bottom-right-radius:12px}
.focus i:nth-child(4){bottom:0;left:0;border-bottom-width:5px;border-left-width:5px;border-bottom-left-radius:12px}
.plus{color:var(--o);font-size:40px;line-height:1}
.arrowR{width:64px;height:64px}
"""


def focus(x, y, w, h, color='var(--o)', anim='', name=''):
    return (f'<div class="focus" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" data-x="snap" {anim}'
            + (f' data-name="{name}"' if name else '') +
            f'><i style="border-color:{color}"></i><i style="border-color:{color}"></i><i style="border-color:{color}"></i><i style="border-color:{color}"></i></div>')


# ================================================================ cover
def s_cover(n):
    p0 = kv(T(0))[1].rstrip(' –').strip()
    p1 = kv(T(1)); p2 = kv(T(2)); p3 = kv(T(3))
    date = p3[1].replace('310/2026', '3/10/2026')
    meta = [('storefront', kv(T(0))[0], p0), ('user-circle', p1[0], p1[1]),
            ('graduation-cap', p2[0], p2[1]), ('calendar-check', p3[0], date)]
    rows = ''
    for i, (ic, lab, val) in enumerate(meta):
        rows += (f'<div class="cv-row" {A("rise", 1000 + i * 120)}>'
                 f'{chip_icon(ic, 84, 48, "var(--ot)", "var(--o2)", "var(--o3)", 26)}'
                 f'<div><div class="lbl mut" style="font-size:28px" data-x="text">{e(lab)}</div>'
                 f'<div class="w5" style="font-size:36px;line-height:1.35" data-x="text">{e(val)}</div></div></div>')
    t1, t2 = T(43).split(' لمشروع ')
    t2a, t2b = t2.split(' – ')
    return f'''
<section class="slide cover" data-tr="fade">
 <style>{EXTRA_CSS}
  .cover .ttl{{right:110px;top:215px;width:1020px}}
  .cover .t1{{font-size:168px;line-height:1.22;color:var(--ink)}}
  .cover .t2{{font-size:72px;line-height:1.4;color:var(--ink)}}
  .cover .t2 b{{font-weight:normal;color:var(--o2)}}
  .cover .meta{{right:110px;top:640px;width:1040px;display:grid;grid-template-columns:1.05fr 1fr;gap:40px 40px}}
  .cv-row{{display:flex;gap:22px;align-items:center}}
 </style>
 <div class="abs" style="left:-300px;top:-210px;width:1420px;height:1420px;border-radius:50%;background:var(--bt)" data-x="shape" data-name="!!lens" {A("zoom", 0, 1000)}></div>
 <div class="abs" style="left:40px;top:120px;width:840px;height:840px;border-radius:50%;background:#fff" data-x="shape" data-name="!!lens2" {A("zoom", 120, 1000)}></div>
 {focus(150, 175, 640, 730, 'var(--b)', A("zoom", 1300, 700))}
 {mark(222, 215, 650, 0, 'o', names=MN, anim={'top': A('spinIn', 250, 1200), 'bot': A('spinIn', 400, 1200), 'arc': A('pop', 1150, 600)})}
 <div class="abs" style="left:760px;top:190px;width:62px;height:62px;border-radius:50%;background:var(--y)" data-x="shape" data-name="!!dot" {A("pop", 1350, 500)}></div>
 <img class="abs" style="right:110px;top:74px;height:82px" src="assets/basmat_ink.svg" data-x="asset" data-src="basmat_ink" {A("fade", 300)}>
 <div class="hud-c" data-x="snap" data-name="!!hud"><i></i><i></i><i></i><i></i></div>
 <div class="rec"><span class="dot" data-x="shape" data-name="!!rec" data-a="blink"></span><span class="t" data-x="text" data-name="!!num">REC · 01</span></div>
 <div class="abs ttl">
   <div class="t1 w9 f-disp" data-x="snap" {A("wipeR", 500, 900)}>{e(t1)}</div>
   <div class="t2 w5" data-x="text" {A("rise", 800)}>لمشروع <b class="w7">{e(t2a)}</b> – <span class="lat">{e(t2b)}</span></div>
 </div>
 <div class="abs meta">{rows}</div>
</section>'''


# ================================================================ agenda
def s_agenda(n):
    items = ''
    for i in range(1, 15):
        items += (f'<div class="ag-it" {A("rise", 250 + i * 60)}>'
                  f'<span class="ag-n w7 f-num" data-x="text">{i:02d}</span>'
                  f'<span class="ag-t" data-x="text">{e(SEC[i])}</span></div>')
    css = EXTRA_CSS + '''
  .agenda .grid{right:110px;top:300px;width:1700px;display:grid;grid-template-columns:1fr 1fr;grid-auto-flow:column;grid-template-rows:repeat(7,98px);column-gap:110px}
  .ag-it{display:flex;align-items:center;gap:30px;border-bottom:3px solid var(--line)}
  .ag-n{font-size:46px;color:var(--o);width:80px}
  .ag-t{font-size:40px;line-height:1.3}'''
    return frame(n, None, 'المحتويات', f'<div class="abs grid">{items}</div>', 'agenda', kicker='', extra_css=css,
                 title_style='font-size:96px;top:120px')


# ================================================================ section divider
def s_divider(n, k):
    title = SEC[k]
    flip = k % 2 == 0
    rot = [0, 90, 180, 270][k % 4]
    cx = 1460 if flip else 460
    mh = 780 if rot in (0, 180) else 630
    side = 'left' if flip else 'right'
    return f'''
<section class="slide dark divider" data-tr="morph">
 <div class="bgfill bg-blue" data-x="bg"></div><div class="grain"></div>
 <style>
  .divider .num{{position:absolute;top:170px;font-size:300px;line-height:1}}
  .divider .dt{{position:absolute;top:520px;width:1000px;font-size:{140 if len(title) < 18 else 118}px;line-height:1.28;color:#fff}}
 </style>
 <div class="abs" style="left:{cx - 560}px;top:-20px;width:1120px;height:1120px;border-radius:50%;background:rgba(255,255,255,.07)" data-x="shape" data-name="!!lens"></div>
 {mark(cx - FW * (mh / FH) / 2, 540 - mh / 2, mh, rot, 'o', glint='y', names=MN)}
 {hud(n, dark=True)}
 <div class="num hollow f-num" style="{side}:130px" data-x="snap" {A("zoomOut", 250, 900)}>{k:02d}</div>
 <h2 class="dt w9 f-disp" style="{side}:130px;text-align:{side}" data-x="snap" {A("wipeR", 500, 900)}>{e(title)}</h2>
</section>'''


# ================================================================ 1. intro
def s_intro(n):
    inner = f'''
 <div class="card b" style="right:110px;top:300px;width:1000px;height:680px;padding:56px 60px" data-x="shape" {A("rise", 200)}>
   {chip_icon('storefront', 120, 70, 'rgba(255,255,255,.14)', '#fff', 'var(--y)', 34, A("pop", 500))}
   <p style="position:absolute;right:60px;bottom:56px;width:880px;color:#fff;font-size:50px;line-height:1.6" data-x="text" {A("rise", 450)}>{e(T(46))}</p>
 </div>
 {focus(1150 - 1040, 270, 0, 0)}
 <div class="card ot" style="left:110px;top:300px;width:670px;height:318px" data-x="shape" {A("rise", 350)}>
   {chip_icon('puzzle-piece', 84, 50, 'var(--o)', '#fff', 'var(--y)', 24, A("pop", 650), 'margin-bottom:22px')}
   <p style="font-size:36px;line-height:1.55" data-x="text" {A("rise", 600)}>{e(T(47))}</p>
 </div>
 <div class="card yt" style="left:110px;top:648px;width:670px;height:332px" data-x="shape" {A("rise", 500)}>
   <h3 class="h3 w7 f-head" style="color:var(--o2);margin-bottom:8px" data-x="text" {A("rise", 750)}>{e(T(48))}</h3>
   <p style="font-size:31px;line-height:1.55" data-x="text" {A("rise", 850)}>{e(T(49))}</p>
 </div>'''
    inner = inner.replace(focus(1150 - 1040, 270, 0, 0), '')
    return frame(n, 1, e(T(45)), inner, 'intro', extra_css=EXTRA_CSS)


def s_goals(n):
    icons = ['megaphone', 'user-plus', 'chart-line-up', 'seal-check', 'handshake']
    tones = ['b', 'w', 'o', 'w', 'y']
    tiles = ''
    for i, (pi, ic) in enumerate(zip(range(51, 56), icons)):
        tone = tones[i]
        dark = tone in ('b',)
        fg = '#fff' if tone in ('b', 'o') else 'var(--b)'
        du = 'var(--y)' if tone != 'y' else '#fff'
        txt = '#fff' if dark else 'var(--ink)'
        chipbg = 'rgba(255,255,255,.18)' if tone in ('b', 'o') else ('var(--bt)' if tone == 'w' else 'rgba(255,255,255,.6)')
        numc = 'rgba(255,255,255,.5)' if tone in ('b', 'o') else ('var(--bl)' if tone == 'w' else 'rgba(255,255,255,.75)')
        tiles += (f'<div class="card {tone} g-t" style="color:{txt};right:{110 + i * 348}px" data-x="shape" {A("rise", 200 + i * 120)}>'
                  f'<div class="g-top">{chip_icon(ic, 100, 60, chipbg, fg, du, 30, A("pop", 450 + i * 120))}'
                  f'<span class="g-n w9 f-num" data-x="text" style="color:{numc}">{i + 1:02d}</span></div>'
                  f'<p class="g-p w5" data-x="text">{e(T(pi).rstrip("."))}</p></div>')
    css = EXTRA_CSS + '''
  .g-t{position:absolute;top:340px;width:318px;height:520px;display:flex;flex-direction:column;justify-content:space-between;padding:40px 36px 44px}
  .g-top{display:flex;justify-content:space-between;align-items:flex-start}
  .g-n{font-size:72px;line-height:1}
  .g-p{font-size:44px;line-height:1.45}'''
    return frame(n, 1, e(T(50)), tiles, 'goals', extra_css=css)


# ================================================================ 2. info
def s_info(n):
    inner = f'''
 <div class="card o" style="right:110px;top:300px;width:760px;height:680px;overflow:hidden" data-x="shape" {A("rise", 200)}>
   <div class="lbl w5" style="color:var(--ink)" data-x="text" {A("rise", 400)}>{e(T(58))}</div>
   <div class="w9" style="font-size:96px;line-height:1.2;margin-top:18px;color:var(--ink)" data-x="text" {A("rise", 500)}>{e(T(59).split(' ')[0] + ' ' + T(59).split(' ')[1])}</div>
   <div class="w7 lat" style="font-size:72px;line-height:1.2;color:var(--ink);text-align:right" data-x="text" {A("rise", 600)}>{e(T(59).split(' ')[-1])}</div>
   <img class="abs" style="left:-40px;bottom:-60px;width:330px" src="assets/mark/full_w.svg" data-x="asset" data-src="mark/full_w" {A("spinIn", 700, 1000)}>
 </div>
 <div class="card bt" style="left:110px;top:300px;width:920px;height:680px;display:flex;flex-direction:column;justify-content:space-between" data-x="shape" {A("rise", 350)}>
   <div style="display:flex;align-items:center;gap:24px">
     {chip_icon('shopping-bag-open', 104, 62, 'var(--b)', '#fff', 'var(--y)', 30, A("pop", 650))}
     <div class="h3 w7 f-head" style="color:var(--b)" data-x="text" {A("rise", 600)}>{e(T(60))}</div>
   </div>
   <p style="font-size:44px;line-height:1.6" data-x="text" {A("rise", 750)}>{e(T(61))}</p>
 </div>'''
    return frame(n, 2, e(SEC[2]), inner, 'info', extra_css=EXTRA_CSS)


def s_products(n):
    items = L(63)
    icons = ['security-camera', 'hard-drives', 'bell-ringing', 'fingerprint', 'key', 'wifi-high', 'car-profile', 'plugs-connected', 'wrench', 'headset']
    tiles = ''
    for i, (it, ic) in enumerate(zip(items, icons)):
        r, c = divmod(i, 5)
        x = 110 + c * 344
        y = 300 + r * 345
        hl = i in (0, 8)
        bg = 'var(--b)' if hl else 'var(--bt)'
        col = '#fff' if hl else 'var(--ink)'
        tiles += (f'<div class="card" style="right:{x}px;top:{y}px;width:324px;height:325px;background:{bg};color:{col};padding:34px 30px" data-x="shape" {A("rise", 150 + i * 70)}>'
                  f'{chip_icon(ic, 92, 56, "rgba(255,255,255,.16)" if hl else "#fff", "#fff" if hl else "var(--b)", "var(--y)" if not hl else "var(--o)", 26, A("pop", 400 + i * 70), "margin-bottom:22px")}'
                  f'<p style="font-size:32px;line-height:1.45" data-x="text">{e(it)}</p></div>')
    return frame(n, 2, e(T(62)), tiles, 'products', extra_css=EXTRA_CSS)


def s_target(n):
    items = L(65)
    icons = ['house-line', 'storefront', 'buildings', 'warehouse', 'network', 'puzzle-piece']
    tiles = ''
    for i, (it, ic) in enumerate(zip(items, icons)):
        r, c = divmod(i, 3)
        x = 110 + c * 576
        y = 310 + r * 340
        tone = ['w', 'w', 'w', 'w', 'w', 'o'][i]
        tiles += (f'<div class="card {tone}" style="right:{x}px;top:{y}px;width:552px;height:310px;display:flex;flex-direction:column;justify-content:space-between" data-x="shape" {A("rise", 150 + i * 100)}>'
                  f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
                  f'{chip_icon(ic, 96, 58, "var(--ot)" if tone == "w" else "rgba(255,255,255,.3)", "var(--o2)" if tone == "w" else "var(--ink)", "var(--o3)" if tone == "w" else "#fff", 28, A("pop", 400 + i * 100))}'
                  f'<span class="w9 f-num" style="font-size:60px;line-height:1;color:{"var(--line)" if tone == "w" else "rgba(255,255,255,.6)"}" data-x="text">{i + 1:02d}</span></div>'
                  f'<p class="w5" style="font-size:{40 if len(it) < 50 else 35}px;line-height:1.45" data-x="text">{e(it)}</p></div>')
    return frame(n, 2, e(T(64)), tiles, 'target', extra_css=EXTRA_CSS)


PLATFORM_ICON = {'Website': 'globe', 'WhatsApp Business': 'whatsapp-logo', 'Instagram': 'instagram-logo', 'Facebook': 'facebook-logo',
                 'TikTok': 'tiktok-logo', 'Snapchat': 'snapchat-logo', 'Google': 'google-logo'}


def s_platforms(n):
    items = L(67)
    row = ''
    for i, it in enumerate(items):
        x = 110 + i * 246
        row += (f'<div class="abs" style="right:{x}px;top:330px;width:226px;display:flex;flex-direction:column;align-items:center;gap:20px" {A("rise", 150 + i * 90)}>'
                f'{chip_icon(PLATFORM_ICON[it], 190, 100, "var(--b)" if i % 2 == 0 else "var(--o)", "#fff", "var(--y)" if i % 2 == 0 else "var(--y2)", 95, A("pop", 300 + i * 90))}'
                f'<span class="w5 lat" style="font-size:31px;line-height:1.3;text-align:center" data-x="text">{e(it)}</span></div>')
    inner = row + f'''
 <div class="card yt" style="right:110px;top:690px;width:1700px;height:290px;display:flex;align-items:center;gap:44px;padding:44px 56px" data-x="shape" {A("rise", 900)}>
   {chip_icon('target', 130, 80, 'var(--y)', 'var(--ink)', '#fff', 36, A("pop", 1100))}
   <p style="font-size:42px;line-height:1.55" data-x="text" {A("rise", 1100)}>{e(T(68))}</p>
 </div>'''
    return frame(n, 2, e(T(66)), inner, 'platforms', extra_css=EXTRA_CSS)


# ================================================================ 3. study
def s_study(n):
    lab1, txt1 = P[72].split('\n')
    lab2, txt2 = P[73].split('\n')
    inner = f'''
 <p class="abs w3" style="right:110px;top:290px;width:1700px;font-size:44px;line-height:1.6" data-x="text" {A("rise", 150)}>{e(clean(P[71]))}</p>
 <div class="card ot" style="right:110px;top:470px;width:800px;height:510px" data-x="shape" {A("rise", 350)}>
   <div style="display:flex;align-items:center;gap:22px;margin-bottom:26px">
     {chip_icon('warning-circle', 96, 58, 'var(--o)', '#fff', 'var(--y)', 28, A("pop", 600))}
     <div class="h3 w7 f-head" style="color:var(--o2)" data-x="text" {A("rise", 550)}>{e(clean(lab1))}</div></div>
   <p style="font-size:42px;line-height:1.6" data-x="text" {A("rise", 700)}>{e(clean(txt1))}</p>
 </div>
 <div class="abs" style="right:938px;top:680px;width:84px;height:84px;border-radius:50%;background:var(--y);display:flex;align-items:center;justify-content:center" data-x="snap" {A("pop", 900)}>{icon('arrow-left', 'var(--ink)', 'var(--ink)', 48)}</div>
 <div class="card b" style="left:110px;top:470px;width:800px;height:510px" data-x="shape" {A("rise", 800)}>
   <div style="display:flex;align-items:center;gap:22px;margin-bottom:26px">
     {chip_icon('seal-check', 96, 58, 'rgba(255,255,255,.16)', '#fff', 'var(--y)', 28, A("pop", 1050))}
     <div class="h3 w7 f-head" style="color:var(--y)" data-x="text" {A("rise", 1000)}>{e(clean(lab2))}</div></div>
   <p style="font-size:40px;line-height:1.6;color:#fff" data-x="text" {A("rise", 1150)}>{e(clean(txt2))}</p>
 </div>'''
    return frame(n, 3, e(SEC[3]), inner, 'study', extra_css=EXTRA_CSS)
