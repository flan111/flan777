# -*- coding: utf-8 -*-
from slides_b import *

WEEKS = [(202, [203, 204, 205, 206], 207), (209, [210, 211, 212, 213], 214),
         (216, [217, 218, 219, 220], 221), (223, [224, 225, 226, 227], 228)]


def fmt_icon(f):
    f = f.lower()
    if 'reel' in f: return 'film-strip'
    if 'carousel' in f: return 'cards-three'
    if 'b2b' in f: return 'buildings'
    if 'conversion' in f: return 'cursor-click'
    return 'package'


# ================================================================ 8. content plan
def s_plan(n):
    cards = ''
    tones = ['b', 'w', 'w', 'o']
    for i, (hp, _, _) in enumerate(WEEKS):
        lab, theme = kv(T(hp))
        x = 110 + i * 430
        tone = tones[i]
        dark = tone == 'b'
        cards += (f'<div class="card {tone}" style="right:{x}px;top:500px;width:405px;height:380px;color:{"#fff" if dark else "var(--ink)"};display:flex;flex-direction:column;justify-content:space-between" data-x="shape" {A("rise", 400 + i * 150)}>'
                  f'<span class="w9 f-num" style="font-size:96px;line-height:1;color:{"rgba(255,255,255,.4)" if dark else ("rgba(255,255,255,.55)" if tone == "o" else "var(--bl)")}" data-x="text">{i + 1:02d}</span>'
                  f'<div><div class="w5" style="font-size:30px;color:{"var(--y)" if dark else ("var(--ink)" if tone == "o" else "var(--o2)")}" data-x="text">{e(lab)}</div>'
                  f'<div class="w7" style="font-size:38px;line-height:1.4;margin-top:6px" data-x="text">{e(theme)}</div></div></div>')
    track = (f'<div class="abs" style="right:110px;top:925px;width:1700px;height:14px;border-radius:7px;background:linear-gradient(270deg,var(--b),var(--y),var(--o))" data-x="snap" {A("wipeR", 900, 1200)}></div>')
    inner = f'''
 <p class="abs" style="right:110px;top:285px;width:1700px;font-size:40px;line-height:1.6" data-x="text" {A("rise", 150)}>{e(T(201))}</p>
 {cards}{track}'''
    return frame(n, 8, e(strip_num(T(200))), inner, 'plan', extra_css=EXTRA_CSS)


def s_week(n, wi):
    hp, posts, sp = WEEKS[wi]
    lab, theme = kv(T(hp))
    cards = ''
    for i, pi in enumerate(posts):
        ls = [clean(x) for x in P[pi].split('\n') if clean(x)]
        day, fmt = [x.strip() for x in ls[0].split('–', 1)]
        hook = ls[1]
        g_l, g_t = kv(ls[2])
        c_l, c_t = kv(ls[3])
        r, c = divmod(i, 2)
        x = 110 + c * 865
        y = 262 + r * 312
        cards += f'''
 <div class="card {'w' if i % 3 else 'bt'}" style="right:{x}px;top:{y}px;width:845px;height:296px;padding:28px 34px" data-x="shape" {A("rise", 200 + i * 130)}>
   <div style="display:flex;align-items:center;gap:14px;margin-bottom:12px">
     <span class="chip w7" style="background:var(--o);color:var(--ink);font-size:27px;padding:6px 22px" data-x="shape"><span data-x="text">{e(day)}</span></span>
     <span class="chip w5 lat" style="background:var(--b);color:#fff;font-size:25px;padding:6px 20px;gap:10px" data-x="shape">{icon(fmt_icon(fmt), '#fff', 'var(--y)', 30)}<span data-x="text">{e(fmt)}</span></span>
   </div>
   <div class="w7" style="font-size:35px;line-height:1.4;margin-bottom:8px" data-x="text">{e(hook)}</div>
   <div style="display:flex;gap:14px;align-items:baseline;margin-bottom:4px"><span class="w7" style="font-size:25px;color:var(--b);flex:none;width:76px" data-x="text">{e(g_l)}</span><span style="font-size:29px;line-height:1.45" data-x="text">{e(g_t)}</span></div>
   <div style="display:flex;gap:14px;align-items:baseline"><span class="w7 lat" style="font-size:25px;color:var(--o2);flex:none;width:76px;text-align:right" data-x="text">{e(c_l)}</span><span style="font-size:29px;line-height:1.45" data-x="text">{e(c_t)}</span></div>
 </div>'''
    s_lab, s_txt = kv(T(sp))
    parts = [p.strip() for p in s_txt.split(' – ')]
    chips = ''.join(f'<span class="chip" style="background:#fff;font-size:{25 if len(parts) > 6 else 26}px;padding:6px 18px" data-x="shape" {A("pop", 900 + j * 60)}><span data-x="text">{e(p)}</span></span>' for j, p in enumerate(parts))
    strip = (f'<div class="card y" style="right:110px;top:892px;width:1700px;height:92px;padding:0 28px;display:flex;align-items:center;gap:14px" data-x="shape" {A("rise", 800)}>'
             f'<span class="chip w7 lat" style="background:var(--ink);color:#fff;font-size:26px;padding:6px 20px;gap:10px" data-x="shape">{icon("circle-dashed", "var(--y)", "var(--y)", 28)}<span data-x="text">{e(s_lab)}</span></span>{chips}</div>')
    title = f'{e(lab)} <span style="color:var(--o2)">:</span> <em>{e(theme)}</em>'
    return frame(n, 8, title, cards + strip, 'week', extra_css=EXTRA_CSS, title_style='font-size:62px;top:128px')


DONUT = ['var(--b)', 'var(--o)', 'var(--y)', '#A1B2A5', 'var(--ink)']
DONUT_HEX = ['43644B', 'FF8D26', 'F6C342', 'A1B2A5', '1E2A36']


def s_dist(n):
    import math
    items = []
    for pi in range(230, 235):
        m = re.match(r'(\d+%)\s*(.*)$', T(pi))
        items.append((m.group(1), m.group(2).rstrip('.')))
    # donut svg
    R, r0 = 300, 185
    cx = cy = 320
    ang = -90
    segs = ''
    for i, (p, _) in enumerate(items):
        v = int(p[:-1])
        a0, a1 = math.radians(ang), math.radians(ang + v * 3.6 - 1.2)
        large = 1 if v * 3.6 > 180 else 0
        x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
        x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        x2, y2 = cx + r0 * math.cos(a1), cy + r0 * math.sin(a1)
        x3, y3 = cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)
        segs += f'<path d="M{x0:.1f},{y0:.1f} A{R},{R} 0 {large} 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} A{r0},{r0} 0 {large} 0 {x3:.1f},{y3:.1f}Z" fill="#{DONUT_HEX[i]}"/>'
        ang += v * 3.6
    chart_json = json.dumps({'labels': [b for _, b in items], 'values': [int(a[:-1]) for a, _ in items], 'colors': DONUT_HEX})
    donut = (f'<div class="abs" style="left:150px;top:300px;width:640px;height:640px" data-x="chart" data-chart=\'{chart_json}\' {A("wheel", 300, 1400)}>'
             f'<svg width="640" height="640" viewBox="0 0 640 640">{segs}</svg></div>'
             f'<div class="abs" style="left:150px;top:300px;width:640px;height:640px;display:flex;align-items:center;justify-content:center;flex-direction:column">'
             f'{icon("chart-donut", "var(--b)", "var(--y)", 120, "", .6)}</div>')
    donut = donut.replace(f'{icon("chart-donut", "var(--b)", "var(--y)", 120, "", .6)}', f'<img src="assets/mark/full_o.svg" style="height:150px" data-x="asset" data-src="mark/full_o" {A("pop", 1500)}>')
    legend = ''
    for i, (p, lab) in enumerate(items):
        y = 300 + i * 132
        v = int(p[:-1])
        legend += (f'<div class="abs" style="right:110px;top:{y}px;width:930px;height:116px;display:flex;align-items:center;gap:30px" {A("rise", 400 + i * 150)}>'
                   f'<span class="w9 f-num" style="font-size:72px;line-height:1;color:{DONUT[i] if i != 2 else "var(--o2)"};width:170px" data-x="text">{p}</span>'
                   f'<div style="flex:1"><div class="w5" style="font-size:38px;line-height:1.3" data-x="text">{e(lab)}</div>'
                   f'<div style="margin-top:12px;height:16px;border-radius:8px;background:var(--bt);position:relative" data-x="shape"><div style="position:absolute;right:0;top:0;bottom:0;width:{v / 30 * 100:.0f}%;border-radius:8px;background:{DONUT[i]}" data-x="shape" {A("wipeR", 600 + i * 150, 700)}></div></div></div></div>')
    return frame(n, 8, e(T(229)), donut + legend, 'dist', extra_css=EXTRA_CSS)


def s_path(n):
    lab, txt = [clean(x) for x in P[235].split('\n')]
    parts = [p.strip().rstrip('.') for p in txt.split('←')]
    icons = ['warning-circle', 'megaphone', 'crosshair', 'lightbulb', 'seal-check', 'package', 'cursor-click', 'chat-circle-dots', 'shopping-cart']
    out = ''
    for i, p in enumerate(parts):
        row = 0 if i < 5 else 1
        col = i if i < 5 else i - 5
        x = 110 + col * 344 + (172 if row else 0)
        y = 300 + row * 340
        last = i == len(parts) - 1
        tone = 'o' if last else ('b' if i in (0, 5) else 'w')
        dark = tone == 'b'
        out += (f'<div class="card {tone}" style="right:{x}px;top:{y}px;width:316px;height:300px;padding:30px 28px;color:{"#fff" if dark else "var(--ink)"};display:flex;flex-direction:column;justify-content:space-between" data-x="shape" {A("rise", 200 + i * 120)}>'
                f'<div style="display:flex;justify-content:space-between;align-items:center">{chip_icon(icons[i], 84, 50, "rgba(255,255,255,.16)" if dark else ("#fff" if tone == "o" else "var(--bt)"), "#fff" if dark else ("var(--o2)" if tone == "o" else "var(--b)"), "var(--y)", 24, A("pop", 350 + i * 120))}'
                f'<span class="w9 f-num" style="font-size:46px;line-height:1;color:{"rgba(255,255,255,.45)" if dark else ("rgba(255,255,255,.7)" if tone == "o" else "var(--bl)")}" data-x="text">{i + 1:02d}</span></div>'
                f'<div class="w7" style="font-size:{36 if len(p) < 16 else 32}px;line-height:1.4" data-x="text">{e(p)}</div></div>')
    return frame(n, 8, e(lab.rstrip(':')), out, 'path', extra_css=EXTRA_CSS)


# ================================================================ 9. content writing
def phone(x, y, w, h, label, headline, d=0, tone='b', hsize=58):
    bg = 'linear-gradient(160deg,#597660,#3A5841)' if tone == 'b' else 'linear-gradient(160deg,#FFA040,#F57B14)'
    col = '#fff' if tone == 'b' else 'var(--ink)'
    return f'''
 <div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:56px;background:#fff;box-shadow:0 30px 70px rgba(30,42,54,.16),0 0 0 10px var(--ink) inset" data-x="snap" {A("rise", d, 900)}>
   <div style="position:absolute;left:50%;top:22px;transform:translateX(-50%);width:120px;height:24px;border-radius:12px;background:var(--ink)"></div>
   <div style="position:absolute;inset:66px 34px auto 34px;display:flex;align-items:center;gap:14px;direction:rtl">
     <div style="width:58px;height:58px;border-radius:50%;background:var(--ot);display:flex;align-items:center;justify-content:center"><img src="assets/mark/full_o.svg" style="height:36px"></div>
     <div style="flex:1;height:14px;border-radius:7px;background:var(--line)"></div><div style="width:40px;height:14px;border-radius:7px;background:var(--line)"></div>
   </div>
   <div style="position:absolute;left:34px;right:34px;top:150px;bottom:130px;border-radius:30px;background:{bg};overflow:hidden">
     <div style="position:absolute;left:-60px;bottom:-80px;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,.1)"></div>
   </div>
   <div style="position:absolute;left:34px;right:34px;bottom:52px;display:flex;justify-content:space-between;direction:ltr">
     <div style="display:flex;gap:22px">{icon('heart', 'var(--o)', 'var(--o)', 44)}{icon('chat-circle', 'var(--ink)', 'var(--line)', 44)}{icon('paper-plane-tilt', 'var(--ink)', 'var(--line)', 44)}</div>{icon('bookmark-simple', 'var(--ink)', 'var(--y)', 44)}</div>
 </div>
 <div class="abs" style="left:{x + 70}px;top:{y + 190}px;width:{w - 140}px;height:{h - 360}px;display:flex;flex-direction:column;justify-content:center;gap:18px;color:{col}">
   {f'<span class="chip w7" style="align-self:flex-start;background:rgba(255,255,255,.2);color:{col};font-size:26px;padding:6px 20px" data-x="shape" {A("pop", d + 300)}><span data-x="text">{e(label)}</span></span>' if label else ''}
   <div class="w9 f-swash" style="font-size:{hsize}px;line-height:1.4" data-x="text" {A("rise", d + 400)}>{headline}</div>
 </div>'''


def ctabar(txt, x=110, y=870, w=1100, h=None, d=0, ic='whatsapp-logo', size=31):
    hh = f'height:{h}px;' if h else ''
    return (f'<div class="card o" style="right:{x}px;top:{y}px;width:{w}px;{hh}padding:24px 32px;display:flex;align-items:center;gap:24px" data-x="shape" {A("rise", d)}>'
            f'{chip_icon(ic, 76, 46, "#fff", "var(--o2)", "var(--y)", 38, A("pop", d + 200))}'
            f'<p class="w5" style="font-size:{size}px;line-height:1.45;color:var(--ink)" data-x="text">{e(txt)}</p></div>')


def chips_grid(items, cols=2, size=30, d=0, bg='var(--bt)', ic='check-circle', icc='var(--b)'):
    out = ''
    for i, it in enumerate(items):
        out += (f'<div class="chip" style="background:{bg};font-size:{size}px;padding:10px 22px 10px 26px;gap:12px;border-radius:22px" data-x="shape" {A("pop", d + i * 70)}>'
                f'{icon(ic, icc, "var(--y)", size + 6)}<span data-x="text">{e(it.rstrip("."))}</span></div>')
    return f'<div style="display:grid;grid-template-columns:repeat({cols},auto);justify-content:start;gap:12px 14px">{out}</div>'


def num_title(k, title):
    return f'<span class="f-num w9" style="color:var(--o)">{k:02d}</span> {e(title)}'


def s_cw1(n):
    ls = L(242)
    lab, head = kv(ls[0])
    inner = phone(110, 245, 560, 740, lab, e(head), 100) + f'''
 <div class="abs" style="right:110px;top:270px;width:1080px">
   <p class="w7" style="font-size:40px;line-height:1.5;color:var(--b)" data-x="text" {A("rise", 300)}>{e(ls[1])}</p>
   <p style="font-size:34px;line-height:1.55;margin:10px 0 18px" data-x="text" {A("rise", 400)}>{e(ls[2])}</p>
   {chips_grid([T(i) for i in range(243, 248)], 3, 31, 500, ic='map-pin', icc='var(--o2)')}
   <p style="font-size:33px;line-height:1.55;margin-top:22px" data-x="text" {A("rise", 900)}>{e(T(248))}</p>
   <div style="margin-top:16px;padding:18px 26px;border-radius:26px;background:var(--yt)" data-x="shape" {A("rise", 1000)}>
     <p class="w5" style="font-size:33px;line-height:1.5" data-x="text">{e(L(249)[0])}</p>
     <p class="w7" style="font-size:33px;line-height:1.5;color:var(--o2)" data-x="text">{e(L(249)[1])}</p></div>
 </div>
 {ctabar(L(249)[2], 110, 880, 1080, None, 1200, size=29)}'''
    return frame(n, 9, num_title(1, strip_num(T(241))), inner, 'cw', extra_css=EXTRA_CSS)


def s_cw2(n):
    ls = L(252)
    comp = [p.strip().rstrip('.') for p in L(260)[1].split('+')]
    fx = ''.join((f'<span class="plus w9" data-x="text" style="font-size:34px">+</span>' if i else '') +
                 f'<span class="chip w5" style="background:#fff;font-size:28px;padding:6px 18px" data-x="shape" {A("pop", 1000 + i * 70)}><span data-x="text">{e(p)}</span></span>'
                 for i, p in enumerate(comp))
    inner = phone(110, 245, 520, 740, '', e(ls[0]), 100, 'o', 62) + f'''
 <div class="abs" style="right:110px;top:262px;width:1130px">
   <p class="w7" style="font-size:36px;line-height:1.45;color:var(--b)" data-x="text" {A("rise", 300)}>{e(ls[1])}</p>
   <p style="font-size:31px;line-height:1.5;margin:4px 0 14px" data-x="text" {A("rise", 380)}>{e(ls[2])}</p>
   <p class="w5" style="font-size:30px;line-height:1.5;margin-bottom:10px" data-x="text" {A("rise", 450)}>{e(T(253))}</p>
   {chips_grid([T(i) for i in range(254, 259)], 3, 27, 500, 'var(--ot)', 'warning', 'var(--o2)')}
   <p style="font-size:30px;line-height:1.5;margin-top:16px" data-x="text" {A("rise", 900)}>{e(T(259))}</p>
   <div style="margin-top:12px;padding:16px 22px;border-radius:26px;background:var(--bt);display:flex;flex-wrap:wrap;align-items:center;gap:8px" data-x="shape" {A("rise", 950)}>
     <span class="w7" style="font-size:30px;color:var(--b);margin-left:8px" data-x="text">{e(L(260)[0])}</span>{fx}</div>
   <p style="font-size:30px;line-height:1.5;margin-top:14px" data-x="text" {A("rise", 1300)}>{e(T(261))}</p>
 </div>
 {ctabar(clean(P[262]), 110, 892, 1130, None, 1400, 'scales', 29)}'''
    return frame(n, 9, num_title(2, strip_num(T(251))), inner, 'cw', extra_css=EXTRA_CSS)


def s_cw3(n):
    b_l, b_t = [clean(x) for x in P[265].split('\n') if clean(x)]
    a_l, a_t = [clean(x) for x in P[266].split('\n') if clean(x)]
    inner = f'''
 <div class="card ot" style="right:110px;top:280px;width:835px;height:250px" data-x="shape" {A("rise", 200)}>
   <div style="display:flex;align-items:center;gap:16px">{chip_icon('door', 72, 44, 'var(--o)', '#fff', 'var(--y)', 22)}<span class="w7" style="font-size:34px;color:var(--o2)" data-x="text">{e(b_l)}</span></div>
   <p class="w7" style="font-size:44px;line-height:1.5;margin-top:22px" data-x="text" {A("rise", 400)}>{e(b_t)}</p></div>
 <div class="card b" style="right:975px;top:280px;width:835px;height:250px" data-x="shape" {A("rise", 600)}>
   <div style="display:flex;align-items:center;gap:16px">{chip_icon('device-mobile-camera', 72, 44, 'rgba(255,255,255,.16)', '#fff', 'var(--y)', 22)}<span class="w7" style="font-size:34px;color:var(--y)" data-x="text">{e(a_l)}</span></div>
   <p class="w7" style="font-size:44px;line-height:1.5;margin-top:22px" data-x="text" {A("rise", 800)}>{e(a_t)}</p></div>
 <div class="abs" style="right:880px;top:360px;width:120px;height:120px;border-radius:50%;background:var(--y);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 12px #fff" data-x="snap" {A("pop", 700)}>{icon('arrow-left', 'var(--ink)', 'var(--ink)', 58)}</div>
 <p class="abs" style="right:110px;top:570px;width:1700px;font-size:36px;line-height:1.55" data-x="text" {A("rise", 1000)}>{e(clean(P[267]))}</p>
 <p class="abs w5" style="right:110px;top:650px;font-size:33px;line-height:1.5" data-x="text" {A("rise", 1100)}>{e(T(268))}</p>
 <div class="abs" style="right:110px;top:715px;width:1700px">{chips_grid([T(i) for i in range(269, 273)], 4, 31, 1200, ic='check-circle')}</div>
 <div class="card y" style="right:110px;top:840px;width:1700px;height:140px;display:flex;align-items:center;gap:26px;padding:0 40px" data-x="shape" {A("rise", 1500)}>
   {chip_icon('chats-teardrop', 84, 52, '#fff', 'var(--o2)', 'var(--y)', 42)}
   <p class="w7" style="font-size:40px" data-x="text">{e(clean(P[273]))}</p></div>'''
    return frame(n, 9, num_title(3, strip_num(T(264))), inner, 'cw', extra_css=EXTRA_CSS)


def s_cw4(n):
    ls = L(277)
    opts = ''
    widths = [86, 72, 60, 48, 66]
    for i, o in enumerate(ls[1:]):
        letter = o[0]
        txt = clean(o[1:].replace('️', '').replace('⃣', ''))
        y = 300 + i * 116
        opts += (f'<div class="abs" style="left:110px;top:{y}px;width:860px;height:96px;border-radius:30px;background:var(--bt);overflow:hidden" data-x="shape" {A("rise", 300 + i * 120)}>'
                 f'<div style="position:absolute;right:0;top:0;bottom:0;width:{widths[i]}%;background:{"var(--o)" if i == 0 else "var(--bl)"};border-radius:30px" data-x="shape" {A("wipeR", 500 + i * 120, 800)}></div>'
                 f'<div style="position:absolute;inset:0;display:flex;align-items:center;gap:22px;padding:0 18px">'
                 f'<span class="w9 lat" style="width:64px;height:64px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:34px;color:var(--b)" data-x="shape"><span data-x="text">{letter}</span></span>'
                 f'<span class="w5" style="font-size:36px" data-x="text">{e(txt)}</span></div></div>')
    l278 = L(278)
    inner = f'''
 <div class="card b" style="right:110px;top:290px;width:780px;height:380px;display:flex;flex-direction:column;justify-content:space-between" data-x="shape" {A("rise", 150)}>
   {chip_icon('chart-bar-horizontal', 96, 58, 'rgba(255,255,255,.16)', '#fff', 'var(--y)', 30)}
   <p class="w7" style="font-size:44px;line-height:1.5;color:#fff" data-x="text">{e(clean(P[276]))}</p></div>
 <div class="abs w7" style="left:110px;top:240px;font-size:30px;color:var(--o2)" data-x="text" {A("fade", 250)}>{e(ls[0])}</div>
 {opts}
 <div class="card yt" style="right:110px;top:700px;width:780px;height:280px" data-x="shape" {A("rise", 1000)}>
   <p style="font-size:33px;line-height:1.55" data-x="text">{e(l278[0])}</p>
   <p class="w7" style="font-size:33px;line-height:1.55;margin-top:10px;color:var(--o2)" data-x="text">{e(l278[1])}</p></div>'''
    return frame(n, 9, num_title(4, strip_num(T(275))), inner, 'cw', extra_css=EXTRA_CSS)


def s_cw5(n):
    comps = [T(i) for i in range(284, 291)]
    icons = ['security-camera', 'hard-drives', 'database', 'plugs-connected', 'wrench', 'gear', 'headset']
    grid = ''
    for i, (c, ic) in enumerate(zip(comps, icons)):
        grid += (f'<div class="chip w5" style="background:var(--bt);font-size:32px;padding:10px 24px 10px 14px;gap:14px;border-radius:24px" data-x="shape" {A("pop", 600 + i * 80)}>'
                 f'<span style="width:56px;height:56px;border-radius:18px;background:#fff;display:flex;align-items:center;justify-content:center" data-x="snap">{icon(ic, "var(--b)", "var(--y)", 36)}</span><span data-x="text">{e(c)}</span></div>')
    l291 = L(291)
    inner = phone(110, 245, 520, 740, '', e(clean(P[281])), 100, 'b', 50) + f'''
 <div class="abs" style="right:110px;top:270px;width:1130px">
   <p class="w5" style="font-size:38px;line-height:1.55" data-x="text" {A("rise", 300)}>{e(clean(P[282]))}</p>
   <p class="w7" style="font-size:34px;margin:22px 0 16px;color:var(--b)" data-x="text" {A("rise", 450)}>{e(T(283))}</p>
   <div style="display:flex;flex-wrap:wrap;gap:14px">{grid}</div>
   <div style="margin-top:24px;padding:20px 28px;border-radius:26px;background:var(--yt)" data-x="shape" {A("rise", 1200)}>
     <p style="font-size:34px;line-height:1.5" data-x="text">{e(l291[0])}</p>
     <p class="w7" style="font-size:36px;line-height:1.5;color:var(--o2)" data-x="text">{e(l291[1])}</p></div>
 </div>
 {ctabar(clean(P[292]), 110, 880, 1130, None, 1400, size=30)}'''
    return frame(n, 9, num_title(5, strip_num(T(280))), inner, 'cw', extra_css=EXTRA_CSS)


def s_cw6(n):
    l296 = L(296)
    fields = [T(i) for i in range(297, 302)]
    icons = ['buildings', 'map-pin', 'crosshair', 'house-line', 'wrench']
    form = ''
    for i, (f, ic) in enumerate(zip(fields, icons)):
        form += (f'<div style="display:flex;align-items:center;gap:20px;padding:14px 22px;border-radius:24px;background:#fff;border:3px solid var(--line)" data-x="shape" {A("rise", 600 + i * 100)}>'
                 f'<span style="width:60px;height:60px;border-radius:18px;background:var(--ot);display:flex;align-items:center;justify-content:center" data-x="snap">{icon(ic, "var(--o2)", "var(--o3)", 38)}</span>'
                 f'<span class="w5" style="font-size:33px" data-x="text">{e(f)}</span>'
                 f'<span style="margin-right:auto;width:180px;height:14px;border-radius:7px;background:var(--line)"></span></div>')
    inner = phone(110, 245, 520, 740, '', e(clean(P[295])), 100, 'o', 52) + f'''
 <div class="abs" style="right:110px;top:268px;width:1130px">
   <div style="display:flex;align-items:center;gap:18px;margin-bottom:16px">
     <span class="chip w7" style="background:var(--b);color:#fff;font-size:27px;padding:6px 20px" data-x="shape" {A("pop", 300)}><span data-x="text">{e(l296[0].rstrip(':'))}</span></span>
     <span class="w7" style="font-size:36px" data-x="text" {A("rise", 400)}>{e(l296[1])}</span></div>
   <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">{form}</div>
   <p style="font-size:32px;line-height:1.55;margin-top:22px" data-x="text" {A("rise", 1100)}>{e(T(302))}</p>
 </div>
 {ctabar(clean(P[303]), 110, 870, 1130, 110, 1300, size=34)}'''
    return frame(n, 9, num_title(6, strip_num(T(294))), inner, 'cw', extra_css=EXTRA_CSS)
