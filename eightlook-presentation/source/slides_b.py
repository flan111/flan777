# -*- coding: utf-8 -*-
from slides_a import *


def head_items(i):
    """paragraph whose first line is a heading and the rest are bullet lines"""
    ls = L(i)
    return ls[0].rstrip(':').strip(), ls[1:]


def card_list(x, y, w, h, tone, heading, items, ic, size=32, d=0, hcol=None, txt=None, dot=None, chipbg=None, fg=None, du=None, gap=16, extra=''):
    dark = tone in ('b',)
    txt = txt or ('#fff' if dark else 'var(--ink)')
    hcol = hcol or ('var(--y)' if dark else 'var(--o2)')
    dot = dot or ('var(--y)' if dark else 'var(--o)')
    chipbg = chipbg or ('rgba(255,255,255,.16)' if dark else '#fff')
    fg = fg or ('#fff' if dark else 'var(--b)')
    du = du or 'var(--y)'
    return f'''
 <div class="card {tone}" style="right:{x}px;top:{y}px;width:{w}px;height:{h}px;color:{txt};{extra}" data-x="shape" {A("rise", d)}>
   <div style="display:flex;align-items:center;gap:22px;margin-bottom:28px">
     {chip_icon(ic, 88, 54, chipbg, fg, du, 26, A("pop", d + 250))}
     <div class="h3 w7 f-head" style="color:{hcol};font-size:40px" data-x="text" {A("rise", d + 150)}>{e(heading)}</div></div>
   {bullet_list(items, size, gap, dot, txt, d + 300, 80)}
 </div>'''


# ================================================================ 4. audience
def s_aud1(n):
    h1, it1 = head_items(79)
    h2, it2 = head_items(80)
    inner = f'''
 <p class="abs" style="right:110px;top:285px;width:1700px;font-size:42px;line-height:1.55" data-x="text" {A("rise", 150)}>{e(clean(P[78]))}</p>
 {card_list(110, 430, 820, 550, 'b', h1, it1, 'map-pin-area', 36, 300)}
 {card_list(960, 430, 850, 550, 'yt', h2, it2, 'heart', 33, 450, gap=12, chipbg='var(--y)', fg='var(--ink)', du='#fff')}'''
    return frame(n, 4, e(SEC[4]), inner, 'aud1', extra_css=EXTRA_CSS)


def s_aud2(n):
    h1, it1 = head_items(81)
    h2, it2 = head_items(82)
    inner = f'''
 {card_list(110, 300, 835, 680, 'ot', h1, it1, 'question', 38, 200, gap=24, chipbg='var(--o)', fg='#fff', du='var(--y)')}
 {card_list(975, 300, 835, 680, 'w', h2, it2, 'magnifying-glass', 36, 400, gap=24, chipbg='var(--bt)')}'''
    return frame(n, 4, e(SEC[4]), inner, 'aud2', extra_css=EXTRA_CSS)


# ================================================================ 5. competitors
COMP = [(85, 87, 89, 91, 92, 93), (94, 96, 99, 101, 102, 103), (105, 107, 110, 112, 113, 114), (116, 118, 121, 123, 124, 125)]


def s_comp(n, idx):
    hp, s0, s1, w0, w1, sp = COMP[idx]
    name = strip_num(T(hp))
    strengths = [T(i) for i in range(s0, s1 + 1)]
    weaks = [T(i) for i in range(w0, w1 + 1)]
    st_lab, st_txt = [clean(x) for x in P[sp].split('\n')]
    parts = [p.strip().rstrip('.') for p in st_txt.split('+')]
    chips = ''
    for i, p in enumerate(parts):
        if i:
            chips += f'<div class="plus w7" data-x="text" {A("pop", 1100 + i * 110)}>+</div>'
        chips += (f'<div class="chip w5" style="background:#fff;font-size:{31 if len(parts) < 6 else 28}px;justify-content:center;text-align:center;padding:{10 if len(parts) < 5 else 7}px 20px" data-x="shape" {A("pop", 1050 + i * 110)}>'
                  f'<span data-x="text">{e(p)}</span></div>')
    sz = 35 if sum(len(s) for s in strengths) < 200 else 33
    inner = f'''
 <div class="abs" style="right:110px;top:140px;width:104px;height:104px;border-radius:50%;background:var(--o);display:flex;align-items:center;justify-content:center" data-x="shape" {A("pop", 0)}>
   <span class="w9 f-num" style="font-size:52px;color:#fff;line-height:1" data-x="text">{idx + 1:02d}</span></div>
 {card_list(110, 300, 700, 680, 'b', T(86 if idx == 0 else [86, 95, 106, 117][idx]), strengths, 'trophy', sz, 200, gap=14)}
 {card_list(840, 300, 520, 680, 'ot', T([90, 100, 111, 122][idx]), weaks, 'warning', 33, 450, gap=14, chipbg='var(--o)', fg='#fff')}
 <div class="card yt" style="left:110px;top:300px;width:450px;height:680px;padding:40px 36px" data-x="shape" {A("rise", 700)}>
   <div style="display:flex;align-items:center;gap:18px;margin-bottom:26px">
     {chip_icon('megaphone-simple', 80, 50, 'var(--y)', 'var(--ink)', '#fff', 24, A("pop", 950))}
     <div class="w7 f-head" style="font-size:36px;color:var(--o2)" data-x="text" {A("rise", 850)}>{e(st_lab)}</div></div>
   <div style="display:flex;flex-direction:column;align-items:stretch;gap:10px">{chips}</div>
 </div>'''
    css = EXTRA_CSS + '.comp .plus{text-align:center;font-size:30px;line-height:.75}'
    return frame(n, 5, e(name), inner, 'comp', extra_css=css, title_style='right:250px;top:136px')


# ================================================================ 6. SWOT
def swot_panel(x, y, w, h, tone, letter, heading, items, d, size=31, gap=12):
    dark = tone == 'b'
    txt = '#fff' if dark else 'var(--ink)'
    hcol = 'var(--y)' if dark else ('var(--o2)' if tone in ('ot', 'w') else 'var(--ink)')
    lcol = 'var(--y)' if dark else ('var(--o)' if tone == 'ot' else ('var(--y)' if tone == 'yt' else 'var(--b2)'))
    return f'''
 <div class="card {tone}" style="right:{x}px;top:{y}px;width:{w}px;height:{h}px;color:{txt};overflow:hidden" data-x="shape" {A("rise", d)}>
   <div class="abs w9 lat" style="left:40px;top:6px;font-size:170px;line-height:1;color:{lcol}" data-x="text" {A("zoomOut", d + 100, 900)}>{letter}</div>
   <div class="h3 w7 f-head" style="color:{hcol};margin:6px 0 64px;position:relative;font-size:46px" data-x="text" {A("rise", d + 150)}>{e(heading)}</div>
   <div style="position:relative">{bullet_list(items, size, gap, 'var(--y)' if dark else 'var(--o)', txt, d + 250, 70)}</div>
 </div>'''


def s_swot1(n):
    inner = (swot_panel(110, 290, 840, 700, 'b', 'S', T(128), [T(i) for i in range(129, 134)], 200, 32, 12) +
             swot_panel(970, 290, 840, 700, 'ot', 'W', T(134), [T(i) for i in range(135, 140)], 450, 32, 12))
    return frame(n, 6, e(SEC[6]), inner, 'swot', extra_css=EXTRA_CSS)


def s_swot2(n):
    inner = (swot_panel(110, 290, 840, 700, 'yt', 'O', T(140), [T(i) for i in range(141, 147)], 200, 31, 8) +
             swot_panel(970, 290, 840, 700, 'w', 'T', T(147), [T(i) for i in range(148, 154)], 450, 31, 8))
    return frame(n, 6, e(SEC[6]), inner, 'swot', extra_css=EXTRA_CSS)


def s_growth(n):
    lab, word = [x.strip() for x in T(154).split(':')]
    inner = f'''
 <div class="abs" style="left:-200px;top:180px;width:1000px;height:1000px;border-radius:50%;background:rgba(255,255,255,.14)" data-x="shape" data-name="!!lens2" {A("zoom", 0, 900)}></div>
 <img class="abs" style="left:180px;top:250px;width:440px" src="assets/mark/full_w.svg" data-x="asset" data-src="mark/full_w" {A("spinIn", 500, 1100)}>
 <div class="abs w5" style="right:110px;top:220px;font-size:46px;color:var(--ink)" data-x="text" {A("rise", 150)}>{e(lab)}</div>
 <div class="abs w9 f-disp" style="right:100px;top:250px;font-size:300px;line-height:1.25;color:#fff;-webkit-text-stroke:.03em #fff" data-x="snap" {A("zoomOut", 300, 1000)}>{e(word)}</div>
 <div class="card w" style="right:110px;top:640px;width:1060px;height:340px;display:flex;align-items:flex-start;gap:34px;padding:44px 48px" data-x="shape" {A("rise", 700)}>
   {chip_icon('trend-up', 110, 70, 'var(--o)', '#fff', 'var(--y)', 32, A("pop", 950))}
   <p style="font-size:37px;line-height:1.6" data-x="text" {A("rise", 900)}>{e(T(155))}</p></div>'''
    css = EXTRA_CSS + '.growth .hud-c i{border-color:rgba(255,255,255,.55)} .growth .kicker{color:var(--ink)} .growth .kicker .n{color:#fff} .growth .rec .t{color:var(--ink)} .growth .rec .dot{background:#fff}'
    return frame(n, 6, '', inner, 'growth', extra_css=css, bg='orange')


# ================================================================ 7. strategy
def s_goal_main(n):
    inner = f'''
 <div class="abs" style="left:130px;top:300px;width:620px;height:620px;border-radius:50%;background:var(--bt)" data-x="shape" {A("zoom", 150, 900)}></div>
 <div class="abs" style="left:215px;top:385px;width:450px;height:450px;border-radius:50%;background:#fff" data-x="shape" {A("zoom", 300, 900)}></div>
 <div class="abs" style="left:300px;top:470px;width:280px;height:280px;border-radius:50%;background:var(--o)" data-x="shape" {A("zoom", 450, 900)}></div>
 <div class="abs" style="left:385px;top:555px;width:110px;height:110px;border-radius:50%;background:var(--y)" data-x="shape" {A("pop", 650, 600)}></div>
 {focus(110, 280, 660, 660, 'var(--b)', A("zoom", 800, 700))}
 <div class="abs w7 f-head" style="right:110px;top:330px;font-size:44px;color:var(--o2)" data-x="text" {A("rise", 200)}>{e(strip_num(T(158)))}</div>
 <p class="abs" style="right:110px;top:420px;width:960px;font-size:46px;line-height:1.65" data-x="text" {A("rise", 400)}>{e(T(159))}</p>'''
    return frame(n, 7, e(strip_num(T(157))), inner, 'gmain', extra_css=EXTRA_CSS)


def s_goals8(n):
    icons = ['megaphone', 'users-three', 'cursor-click', 'whatsapp-logo', 'shopping-cart', 'wrench', 'seal-check', 'stack-plus']
    tiles = ''
    for i, pi in enumerate(range(161, 169)):
        r, c = divmod(i, 4)
        x = 110 + c * 430
        y = 300 + r * 345
        tone = 'b' if i in (0, 6) else ('ot' if i in (3,) else 'w')
        dark = tone == 'b'
        tiles += (f'<div class="card {tone}" style="right:{x}px;top:{y}px;width:405px;height:322px;color:{"#fff" if dark else "var(--ink)"};padding:34px 34px;display:flex;flex-direction:column;justify-content:space-between" data-x="shape" {A("rise", 150 + i * 80)}>'
                  f'<div style="display:flex;justify-content:space-between;align-items:center">'
                  f'{chip_icon(icons[i], 84, 52, "rgba(255,255,255,.16)" if dark else ("var(--o)" if tone == "ot" else "var(--bt)"), "#fff" if tone in ("b", "ot") else "var(--b)", "var(--y)", 24, A("pop", 400 + i * 80))}'
                  f'<span class="w9 f-num" style="font-size:54px;line-height:1;color:{"rgba(255,255,255,.45)" if dark else "var(--bl)" if tone == "w" else "rgba(233,114,12,.35)"}" data-x="text">{i + 1:02d}</span></div>'
                  f'<p class="w5" style="font-size:{32 if len(T(pi)) < 45 else 30}px;line-height:1.45" data-x="text">{e(T(pi).rstrip("."))}</p></div>')
    return frame(n, 7, e(strip_num(T(160))), tiles, 'goals8', extra_css=EXTRA_CSS)


def s_platwhy(n):
    title = strip_num(T(169)).replace('ولماذاه', 'ولماذا')
    rows = ''
    names = ['Instagram', 'TikTok', 'Snapchat', 'Facebook', 'Google', 'WhatsApp Business', 'المتجر الإلكتروني']
    icons = ['instagram-logo', 'tiktok-logo', 'snapchat-logo', 'facebook-logo', 'google-logo', 'whatsapp-logo', 'storefront']
    for i, pi in enumerate(range(170, 177)):
        nm, ds = kv(T(pi))
        col = 0 if i < 4 else 1
        r = i if i < 4 else i - 4
        x = 110 if col == 0 else 975
        y = 300 + r * 172
        hl = i == 6
        rows += (f'<div class="card {"b" if hl else "w"}" style="right:{x}px;top:{y}px;width:835px;height:156px;padding:22px 28px;display:flex;align-items:center;gap:26px;color:{"#fff" if hl else "var(--ink)"}" data-x="shape" {A("rise", 150 + i * 90)}>'
                 f'{chip_icon(icons[i], 104, 62, "rgba(255,255,255,.16)" if hl else ("var(--o)" if i % 2 else "var(--b)"), "#fff", "var(--y)", 30, A("pop", 350 + i * 90))}'
                 f'<div style="flex:1"><div class="w7 {"lat" if nm[0] < "ؠ" else ""}" style="font-size:31px;line-height:1.3;color:{"var(--y)" if hl else "var(--o2)"};{"text-align:right" if nm[0] < "ؠ" else ""}" data-x="text">{e(nm)}</div>'
                 f'<div style="font-size:{27 if len(ds) > 75 else 28}px;line-height:1.45" data-x="text">{e(ds)}</div></div></div>')
    # last row on the left column: empty slot used for a visual
    rows += f'''<div class="card yt" style="right:975px;top:{300 + 3 * 172}px;width:835px;height:156px;display:flex;align-items:center;justify-content:center;gap:30px" data-x="shape" {A("rise", 900)}>
      {''.join(chip_icon(ic, 72, 44, '#fff', 'var(--b)' if j % 2 == 0 else 'var(--o2)', 'var(--y)', 36, A("pop", 1000 + j * 60)) for j, ic in enumerate(icons))}</div>'''
    return frame(n, 7, e(title), rows, 'platwhy', extra_css=EXTRA_CSS)


def s_style(n):
    cards = ''
    icons = ['book-open-text', 'chats-circle', 'seal-check', 'shopping-bag', 'hand-tap']
    tones = ['b', 'w', 'ot', 'w', 'yt']
    for i, pi in enumerate(range(179, 184)):
        nm, ds = kv(T(pi))
        x = 110 + i * 344
        tone = tones[i]
        dark = tone == 'b'
        cards += (f'<div class="card {tone}" style="right:{x}px;top:350px;width:324px;height:440px;padding:34px 30px;color:{"#fff" if dark else "var(--ink)"}" data-x="shape" {A("rise", 200 + i * 100)}>'
                  f'{chip_icon(icons[i], 88, 54, "rgba(255,255,255,.16)" if dark else ("var(--o)" if tone == "ot" else ("var(--y)" if tone == "yt" else "var(--bt)")), "#fff" if tone in ("b", "ot") else ("var(--ink)" if tone == "yt" else "var(--b)"), "var(--y)" if tone != "yt" else "#fff", 26, A("pop", 450 + i * 100), "margin-bottom:24px")}'
                  f'<div class="w7" style="font-size:36px;line-height:1.3;margin-bottom:12px;color:{"var(--y)" if dark else "var(--o2)"}" data-x="text">{e(nm)}</div>'
                  f'<div style="font-size:29px;line-height:1.5" data-x="text">{e(ds)}</div></div>')
    formula = clean(P[184]).rstrip('.')
    parts = [p.strip() for p in formula.split('+')]
    fx = ''
    for i, p in enumerate(parts):
        if i:
            fx += f'<span class="plus w9" style="font-size:54px;color:var(--o)" data-x="text" {A("pop", 1150 + i * 120)}>+</span>'
        fx += f'<span class="chip w7" style="background:#fff;font-size:40px;padding:12px 40px" data-x="shape" {A("pop", 1100 + i * 120)}><span data-x="text">{e(p)}</span></span>'
    inner = f'''
 <p class="abs mut" style="right:110px;top:270px;font-size:36px" data-x="text" {A("rise", 100)}>{e(T(178))}</p>
 {cards}
 <div class="card y" style="right:110px;top:820px;width:1700px;height:160px;display:flex;align-items:center;justify-content:center;gap:28px" data-x="shape" {A("rise", 1000)}>{fx}</div>'''
    return frame(n, 7, e(strip_num(T(177))), inner, 'style', extra_css=EXTRA_CSS)


def s_journey(n):
    steps = []
    for pi in (186, 188, 190, 192, 194, 196):
        a, b = [clean(x) for x in P[pi].split('\n')]
        steps.append((a.replace('التعرفعه', 'التعرف'), b))
    icons = ['eye', 'sparkle', 'scales', 'chat-circle-dots', 'handshake', 'shopping-cart-simple']
    nodes = ''
    for i, (a, b) in enumerate(steps):
        x = 110 + i * 290
        last = i == 5
        nodes += (f'<div class="abs" style="right:{x}px;top:330px;width:270px;display:flex;flex-direction:column;align-items:center;text-align:center" {A("rise", 300 + i * 160)}>'
                  f'<div style="width:150px;height:150px;border-radius:50%;background:{"var(--o)" if last else ("var(--b)" if i % 2 == 0 else "#fff")};border:{"0" if (last or i % 2 == 0) else "5px solid var(--b)"};display:flex;align-items:center;justify-content:center" data-x="snap" {A("pop", 300 + i * 160)}>'
                  f'{icon(icons[i], "#fff" if (last or i % 2 == 0) else "var(--b)", "var(--y)", 76)}</div>'
                  f'<span class="w9 f-num" style="font-size:34px;color:var(--o);margin-top:18px" data-x="text">{i + 1:02d}</span>'
                  f'<div class="w7" style="font-size:36px;line-height:1.3;margin-top:4px;min-height:94px;display:flex;align-items:center" data-x="text">{e(a)}</div>'
                  f'<div style="font-size:28px;line-height:1.5;margin-top:10px" data-x="text">{e(b)}</div></div>')
    track = f'<div class="abs" style="right:245px;top:401px;width:1450px;height:8px;border-radius:4px;background:repeating-linear-gradient(270deg,var(--bl) 0 22px,transparent 22px 36px)" data-x="snap" {A("wipeR", 150, 1400)}></div>'
    return frame(n, 7, e(strip_num(T(185))), track + nodes, 'journey', extra_css=EXTRA_CSS)


def s_chain(n):
    lab = T(197)
    parts = [p.strip() for p in T(198).split('←')]
    icons = ['magnet', 'shield-check', 'ear', 'lightbulb', 'shopping-cart']
    nodes = ''
    for i, p in enumerate(parts):
        x = 110 + i * 346
        nodes += (f'<div class="card" style="right:{x}px;top:380px;width:300px;height:480px;background:{"var(--o)" if i == 4 else "rgba(255,255,255,.1)"};color:{"var(--ink)" if i == 4 else "#fff"};padding:36px 30px;display:flex;flex-direction:column;gap:22px" data-x="shape" {A("rise", 300 + i * 180)}>'
                  f'{chip_icon(icons[i], 96, 58, "rgba(255,255,255,.18)" if i < 4 else "#fff", "#fff" if i < 4 else "var(--o2)", "var(--y)", 30, A("pop", 450 + i * 180))}'
                  f'<span class="w9 f-num" style="font-size:40px;color:{"var(--y)" if i < 4 else "#fff"}" data-x="text">{i + 1:02d}</span>'
                  f'<div class="w7" style="font-size:36px;line-height:1.45" data-x="text">{e(p)}</div></div>')
        if i < 4:
            nodes += (f'<div class="abs" style="right:{x + 300 + 2}px;top:590px;width:42px;height:60px;display:flex;align-items:center;justify-content:center" data-x="snap" {A("fade", 500 + i * 180)}>'
                      f'{icon("caret-left", "var(--y)", "var(--y)", 42)}</div>')
    return frame(n, 7, e(lab), nodes, 'chain', dark=True, extra_css=EXTRA_CSS)
