# -*- coding: utf-8 -*-
from slides_c import *

STEP_ICONS = {'📍': 'map-pin', '📐': 'ruler', '🔌': 'plug', '⚙️': 'gear', '📱': 'device-mobile', '📹': 'security-camera',
              '🎥': 'video-camera', '💾': 'hard-drive', '🔧': 'wrench'}


def split_emoji(s):
    for k, v in STEP_ICONS.items():
        if s.startswith(k):
            return v, clean(s[len(k):].replace('️', ''))
    return None, s


def ad_frame(n, sub_p, ex_p, fm_p, hook, body_html, cta, kicker_sub=True):
    sub = T(sub_p)
    ex_l, ex_t = kv(T(ex_p))
    fl = [clean(x) for x in P[fm_p].split('\n') if clean(x)]
    f_l, f_v = kv(fl[0])
    a_l, a_v = kv(fl[1])
    left = f'''
 <div class="card b" style="left:110px;top:270px;width:520px;height:300px;display:flex;flex-direction:column;justify-content:space-between" data-x="shape" {A("rise", 150)}>
   <div style="display:flex;align-items:center;gap:16px">{chip_icon('function', 76, 46, 'rgba(255,255,255,.16)', '#fff', 'var(--y)', 22)}<span class="w5" style="font-size:32px;color:var(--y)" data-x="text">{e(f_l)}</span></div>
   <div class="w9 lat" style="font-size:{86 if len(f_v) < 8 else (52 if len(f_v) < 20 else 40)}px;line-height:1.2;color:#fff;text-align:right" data-x="text" {A("zoom", 350, 700)}>{e(f_v)}</div></div>
 <div class="card yt" style="left:110px;top:590px;width:520px;height:390px" data-x="shape" {A("rise", 300)}>
   <div style="display:flex;align-items:center;gap:16px;margin-bottom:22px">{chip_icon('crosshair', 76, 46, 'var(--y)', 'var(--ink)', '#fff', 22)}<span class="w5" style="font-size:32px;color:var(--o2)" data-x="text">{e(a_l)}</span></div>
   {''.join(f'<div class="w7" style="font-size:38px;line-height:1.45" data-x="text" {A("rise", 450 + j * 100)}>{("+ " if j else "") + e(p.strip().rstrip("."))}</div>' for j, p in enumerate(a_v.split('+')))}
 </div>'''
    title = f'<span class="chip w5" style="background:var(--b);color:#fff;font-size:30px;padding:8px 24px;vertical-align:middle">{e(sub)}</span>'
    inner = left + f'''
 <div class="abs" style="right:110px;top:236px;display:flex;align-items:center;gap:20px" {A("rise", 50)}>
   <span class="chip w7" style="background:var(--o);color:var(--ink);font-size:30px;padding:8px 24px" data-x="shape"><span data-x="text">{e(ex_l)}</span></span>
   <span class="w7 f-head" style="font-size:46px" data-x="text">{e(ex_t)}</span></div>
 {hook}
 {body_html}
 {ctabar(cta, 110, 880, 1120, 100, 1400, size=31)}'''
    return frame(n, 10, '', inner, 'ad', extra_css=EXTRA_CSS + '.ad .kicker .n{color:var(--b)}', kicker=f'{SEC[10]} · {sub}')


def hook_card(label, text, y=330, h=170):
    lab = (f'<span class="chip w7 lat" style="background:var(--ink);color:var(--y);font-size:26px;padding:4px 18px;margin-bottom:10px" data-x="shape">'
           f'<span data-x="text">{e(label)}</span></span>') if label else ''
    return (f'<div class="card y" style="right:110px;top:{y}px;width:1120px;height:{h}px;padding:24px 36px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start" data-x="shape" {A("rise", 250)}>'
            f'{lab}<div class="w7 f-swash" style="font-size:44px;line-height:1.45" data-x="text">{e(text)}</div></div>')


def body_block(y, parts):
    return f'<div class="abs" style="right:110px;top:{y}px;width:1120px">{parts}</div>'


def s_ad1(n):
    hl = L(309)
    cl = L(310)
    body = body_block(525, f'''
   <p style="font-size:34px;line-height:1.5;margin-bottom:16px" data-x="text" {A("rise", 450)}><span class="w7" style="color:var(--b)">{e(cl[0])}</span> {e(cl[1])}</p>
   {chips_grid([T(i) for i in range(311, 317)], 3, 32, 550, ic='check-circle')}
   <p class="w5" style="font-size:33px;line-height:1.5;margin-top:20px" data-x="text" {A("rise", 1100)}>{e(T(317))}</p>''')
    return ad_frame(n, 306, 307, 308, hook_card(hl[0].rstrip(':'), hl[1]), body, clean(P[318])).replace('<div class="abs" style="right:110px;width:1120px;top:0px"></div>', '')


def s_ad2(n):
    cl = L(323)
    steps = ''
    for i, ln in enumerate(L(325)):
        ic, txt = split_emoji(ln)
        steps += (f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center" {A("rise", 650 + i * 110)}>'
                  f'<span style="width:84px;height:84px;border-radius:50%;background:{"var(--o)" if i == 4 else "var(--b)"};display:flex;align-items:center;justify-content:center" data-x="snap">{icon(ic, "#fff", "var(--y)", 48)}</span>'
                  f'<span class="w5" style="font-size:30px;line-height:1.35" data-x="text">{e(txt)}</span></div>')
    body = body_block(525, f'''
   <p style="font-size:34px;line-height:1.5" data-x="text" {A("rise", 450)}><span class="w7" style="color:var(--b)">{e(cl[0])}</span> {e(cl[1])}</p>
   <p class="w5" style="font-size:31px;margin:8px 0 18px;color:var(--mut)" data-x="text" {A("rise", 550)}>{e(T(324))}</p>
   <div style="display:flex;gap:10px">{steps}</div>
   <p class="w5" style="font-size:33px;line-height:1.5;margin-top:20px" data-x="text" {A("rise", 1250)}>{e(T(326))}</p>''')
    return ad_frame(n, 306, 320, 321, hook_card('', clean(P[322]), 330, 150), body, clean(P[327])).replace('<div class="abs" style="right:110px;width:1120px;top:0px"></div>', '')


def s_ad3(n):
    body = body_block(505, f'''
   <p class="w7" style="font-size:36px;line-height:1.5;color:var(--b)" data-x="text" {A("rise", 450)}>{e(clean(P[333]))}</p>
   <p style="font-size:33px;line-height:1.5;margin:8px 0 16px" data-x="text" {A("rise", 520)}>{e(T(334))}</p>
   {chips_grid([T(i) for i in range(335, 340)], 3, 31, 600, 'var(--ot)', 'warning', 'var(--o2)')}
   <p class="w5" style="font-size:34px;line-height:1.5;margin-top:22px" data-x="text" {A("rise", 1100)}>{e(T(340))}</p>''')
    return ad_frame(n, 329, 330, 331, hook_card('', clean(P[332]), 330, 150), body, clean(P[341])).replace('<div class="abs" style="right:110px;width:1120px;top:0px"></div>', '')


def s_ad4(n):
    body = body_block(505, f'''
   <p class="w7" style="font-size:34px;line-height:1.5;margin-bottom:16px;color:var(--b)" data-x="text" {A("rise", 450)}>{e(clean(P[346]))}</p>
   {chips_grid([T(i) for i in range(347, 352)], 3, 31, 550, ic='database', icc='var(--b)')}
   <p style="font-size:33px;line-height:1.5;margin-top:20px" data-x="text" {A("rise", 1000)}>{e(T(352))}</p>
   <p class="w5" style="font-size:33px;line-height:1.5;margin-top:10px" data-x="text" {A("rise", 1100)}>{e(T(353))}</p>''')
    return ad_frame(n, 329, 343, 344, hook_card('', clean(P[345]), 330, 150), body, clean(P[354])).replace('<div class="abs" style="right:110px;width:1120px;top:0px"></div>', '')


def s_ad5(n):
    body = body_block(505, f'''
   <p style="font-size:35px;line-height:1.55" data-x="text" {A("rise", 450)}>{e(clean(P[360]))}</p>
   <div style="display:flex;gap:16px;margin-top:18px">
     <div style="flex:1;padding:22px 26px;border-radius:28px;background:var(--bt)" data-x="shape" {A("rise", 650)}>{chip_icon('house-line', 64, 40, '#fff', 'var(--b)', 'var(--y)', 20, '', 'margin-bottom:10px')}<p style="font-size:33px;line-height:1.5" data-x="text">{e(T(361))}</p></div>
     <div style="flex:1;padding:22px 26px;border-radius:28px;background:var(--ot)" data-x="shape" {A("rise", 850)}>{chip_icon('puzzle-piece', 64, 40, '#fff', 'var(--o2)', 'var(--y)', 20, '', 'margin-bottom:10px')}<p class="w5" style="font-size:33px;line-height:1.5" data-x="text">{e(T(362))}</p></div>
   </div>''')
    return ad_frame(n, 356, 357, 358, hook_card('', clean(P[359]), 330, 150), body, clean(P[363])).replace('<div class="abs" style="right:110px;width:1120px;top:0px"></div>', '')


def s_ad6(n):
    factors = L(369)
    icons = ['ruler', 'crosshair', 'door-open', 'network', 'clock-countdown', 'arrows-out']
    grid = ''
    for i, (f, ic) in enumerate(zip(factors, icons)):
        grid += (f'<div class="chip w5" style="background:var(--bt);font-size:31px;padding:8px 20px 8px 12px;gap:12px;border-radius:22px" data-x="shape" {A("pop", 600 + i * 80)}>'
                 f'<span style="width:52px;height:52px;border-radius:16px;background:#fff;display:flex;align-items:center;justify-content:center" data-x="snap">{icon(ic, "var(--b)", "var(--y)", 34)}</span><span data-x="text">{e(f)}</span></div>')
    body = body_block(505, f'''
   <p class="w7" style="font-size:34px;line-height:1.5;margin-bottom:16px;color:var(--b)" data-x="text" {A("rise", 450)}>{e(T(368))}</p>
   <div style="display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:12px 14px">{grid}</div>
   <p class="w5" style="font-size:33px;line-height:1.5;margin-top:22px" data-x="text" {A("rise", 1150)}>{e(T(370))}</p>''')
    return ad_frame(n, 356, 365, 366, hook_card('', clean(P[367]), 330, 150), body, clean(P[371])).replace('<div class="abs" style="right:110px;width:1120px;top:0px"></div>', '')


# ================================================================ personas
def profile_card(x, y, w, h, lines, d=0):
    rows = ''
    nm = ''
    for ln in lines:
        k, v = kv(ln)
        if k == 'الاسم':
            nm = v
            continue
        rows += (f'<div style="display:flex;justify-content:space-between;gap:20px;padding:12px 0;border-top:2px solid rgba(255,255,255,.18)">'
                 f'<span style="font-size:28px;color:rgba(255,255,255,.75)" data-x="text">{e(k)}</span>'
                 f'<span class="w5" style="font-size:30px;text-align:left" data-x="text">{e(v.rstrip("."))}</span></div>')
    return f'''
 <div class="card b" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;padding:40px 44px" data-x="shape" {A("rise", d)}>
   <div style="display:flex;align-items:center;gap:26px;margin-bottom:22px">
     <div style="width:150px;height:150px;border-radius:50%;background:var(--y);display:flex;align-items:center;justify-content:center;flex:none" data-x="snap" {A("pop", d + 250)}>{icon('user', 'var(--ink)', '#fff', 96)}</div>
     <div><div style="font-size:28px;color:rgba(255,255,255,.75)" data-x="text">الاسم</div>
     <div class="w9 f-disp" style="font-size:84px;line-height:1.2" data-x="text" {A("rise", d + 300)}>{e(nm)}</div></div></div>
   {rows}
 </div>'''


def s_pers1a(n):
    lines = L(375)
    inner = profile_card(110, 290, 560, 690, lines, 150) + \
        card_list(110, 290, 540, 690, 'w', T(376).rstrip(':'), [T(i) for i in range(377, 382)], 'heart', 33, 400, gap=16) + \
        card_list(680, 290, 540, 690, 'ot', T(382).rstrip(':'), [T(i) for i in range(383, 388)], 'warning', 33, 650, gap=16, chipbg='var(--o)', fg='#fff')
    return frame(n, None, e(T(374)), inner, 'pers', kicker=T(373), extra_css=EXTRA_CSS)


def quote_card(x, y, w, h, label, text, d, tone='o', size=42):
    return f'''
 <div class="card {tone}" style="right:{x}px;top:{y}px;width:{w}px;height:{h}px;display:flex;flex-direction:column;justify-content:center" data-x="shape" {A("rise", d)}>
   <div style="display:flex;align-items:center;gap:16px;margin-bottom:14px">{chip_icon('quotes', 72, 46, '#fff', 'var(--o2)', 'var(--y)', 36)}<span class="w5" style="font-size:30px;color:var(--ink)" data-x="text">{e(label)}</span></div>
   <p class="w9 f-swash" style="font-size:{size}px;line-height:1.5;color:var(--ink)" data-x="text">{e(text)}</p></div>'''


def info_card(x, y, w, h, label, text, ic, d, tone='w', size=31):
    dark = tone == 'b'
    return f'''
 <div class="card {tone}" style="right:{x}px;top:{y}px;width:{w}px;height:{h}px;color:{'#fff' if dark else 'var(--ink)'}" data-x="shape" {A("rise", d)}>
   <div style="display:flex;align-items:center;gap:18px;margin-bottom:14px">{chip_icon(ic, 72, 44, 'rgba(255,255,255,.16)' if dark else 'var(--bt)', '#fff' if dark else 'var(--b)', 'var(--y)', 22)}<span class="w7" style="font-size:33px;color:{'var(--y)' if dark else 'var(--o2)'}" data-x="text">{e(label)}</span></div>
   <p style="font-size:{size}px;line-height:1.55" data-x="text">{e(text)}</p></div>'''


def s_pers1b(n):
    fac = [T(i).rstrip('.') for i in range(389, 395)]
    icons = ['scales', 'medal', 'package', 'star', 'chat-circle-dots', 'wrench']
    grid = ''
    for i, (f, ic) in enumerate(zip(fac, icons)):
        grid += (f'<div class="chip w5" style="background:#fff;font-size:27px;padding:6px 16px 6px 10px;gap:10px;border-radius:20px" data-x="shape" {A("pop", 350 + i * 80)}>'
                 f'<span style="width:46px;height:46px;border-radius:14px;background:var(--bt);display:flex;align-items:center;justify-content:center" data-x="snap">{icon(ic, "var(--b)", "var(--y)", 30)}</span><span data-x="text">{e(f)}</span></div>')
    att_l, att_t = [clean(x) for x in P[395].split('\n')]
    ang_l, ang_t = [clean(x) for x in P[396].split('\n')]
    msg_l, msg_t = [clean(x) for x in P[397].split('\n')]
    inner = f'''
 <div class="card yt" style="right:110px;top:290px;width:860px;height:330px" data-x="shape" {A("rise", 150)}>
   <div style="display:flex;align-items:center;gap:18px;margin-bottom:18px">{chip_icon('scales', 72, 44, 'var(--y)', 'var(--ink)', '#fff', 22)}<span class="w7" style="font-size:33px;color:var(--o2)" data-x="text">{e(T(388).rstrip(':'))}</span></div>
   <div style="display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:12px 10px">{grid}</div></div>
 {info_card(990, 290, 820, 330, att_l, att_t, 'eye', 500, 'w', 29)}
 {info_card(110, 645, 860, 335, ang_l.rstrip(':'), ang_t, 'crosshair', 700, 'b', 42)}
 {quote_card(990, 645, 820, 335, msg_l.rstrip(':'), msg_t, 900, 'o', 38)}'''
    return frame(n, None, e(T(374)), inner, 'pers', kicker=T(373), extra_css=EXTRA_CSS)


def s_pers2a(n):
    lines = L(400)
    inner = profile_card(110, 290, 560, 690, lines, 150) + \
        card_list(110, 290, 540, 690, 'w', T(401).rstrip(':'), [T(i) for i in range(402, 407)], 'heart', 33, 400, gap=16) + \
        card_list(680, 290, 540, 690, 'ot', T(407).rstrip(':'), [T(i) for i in range(408, 412)], 'warning', 33, 650, gap=16, chipbg='var(--o)', fg='#fff')
    return frame(n, None, e(T(399)), inner, 'pers', kicker=T(373), extra_css=EXTRA_CSS)


def s_pers2b(n):
    att_l, att_t = [clean(x) for x in P[412].split('\n')]
    ang_l, ang_t = [clean(x) for x in P[413].split('\n')]
    msg_l, msg_t = [clean(x) for x in P[414].split('\n')]
    inner = f'''
 {info_card(110, 290, 1700, 300, att_l, att_t, 'eye', 150, 'w', 34)}
 {info_card(980, 620, 830, 360, ang_l.rstrip(':'), ang_t, 'crosshair', 450, 'b', 42)}
 {quote_card(110, 620, 840, 360, msg_l.rstrip(':'), msg_t, 700, 'o', 46)}'''
    return frame(n, None, e(T(399)), inner, 'pers', kicker=T(373), extra_css=EXTRA_CSS)


# ================================================================ 11. AI
def s_ai(n):
    icons = ['lightbulb-filament', 'pen-nib', 'paint-brush-broad', 'film-slate', 'magic-wand']
    rows = ''
    for i, pi in enumerate(range(418, 423)):
        lab, ds = kv(T(pi))
        y = 335 + i * 130
        rows += (f'<div class="card {"b" if i == 0 else "w"}" style="right:110px;top:{y}px;width:1700px;height:118px;padding:0 30px;display:flex;align-items:center;gap:26px;color:{"#fff" if i == 0 else "var(--ink)"}" data-x="shape" {A("rise", 300 + i * 120)}>'
                 f'{chip_icon(icons[i], 76, 46, "rgba(255,255,255,.16)" if i == 0 else ("var(--o)" if i % 2 else "var(--bt)"), "#fff" if i in (0, 1, 3) else "var(--b)", "var(--y)", 24, A("pop", 450 + i * 120))}'
                 f'<span class="w7" style="font-size:33px;width:330px;flex:none;color:{"var(--y)" if i == 0 else "var(--o2)"}" data-x="text">{e(lab)}</span>'
                 f'<span style="font-size:{29 if len(ds) > 110 else 31}px;line-height:1.4" data-x="text">{e(ds)}</span></div>')
    inner = f'''
 <div class="abs" style="right:110px;top:248px;display:flex;align-items:center;gap:18px" {A("rise", 100)}>
   {chip_icon('robot', 62, 40, 'var(--y)', 'var(--ink)', '#fff', 31)}
   <p class="w5" style="font-size:31px;line-height:1.4" data-x="text">{e(T(417))}</p></div>
 {rows}'''
    return frame(n, 11, e(strip_num(T(416))), inner, 'ai', extra_css=EXTRA_CSS)


# ================================================================ 12. campaign
def s_camp(n):
    c_l, c_t = [clean(x) for x in P[426].split('\n')]
    g_l, g_t = [clean(x) for x in P[427].split('\n')]
    a_l, a_t = [clean(x) for x in P[461].split('\n')]
    b_l, b_t = [clean(x) for x in P[462].split('\n')]
    num, cur = b_t.split(' ', 1)
    inner = f'''
 <div class="abs" style="right:110px;top:140px;width:104px;height:104px;border-radius:50%;background:var(--b);display:flex;align-items:center;justify-content:center" data-x="snap" {A("pop", 0)}>{icon('meta-logo', '#fff', 'var(--y)', 64)}</div>
 {info_card(110, 290, 1060, 330, c_l.rstrip(':'), c_t, 'film-strip', 150, 'b', 34)}
 {info_card(1200, 290, 610, 330, g_l.rstrip(':'), g_t, 'target', 350, 'yt', 36)}
 <div class="card w" style="right:110px;top:650px;width:600px;height:330px" data-x="shape" {A("rise", 550)}>
   <div style="display:flex;align-items:center;gap:18px;margin-bottom:22px">{chip_icon('house-line', 72, 44, 'var(--bt)', 'var(--b)', 'var(--y)', 22)}<span class="w7" style="font-size:33px;color:var(--o2)" data-x="text">{e(T(428).rstrip(':'))}</span></div>
   <p class="w7" style="font-size:44px;line-height:1.45" data-x="text">{e(T(429).rstrip('.'))}</p></div>
 <div class="card ot" style="right:740px;top:650px;width:620px;height:330px" data-x="shape" {A("rise", 750)}>
   <div style="display:flex;align-items:center;gap:18px;margin-bottom:22px">{chip_icon('crosshair', 72, 44, 'var(--o)', '#fff', 'var(--y)', 22)}<span class="w7" style="font-size:33px;color:var(--o2)" data-x="text">{e(a_l.rstrip(': '))}</span></div>
   {''.join(f'<div class="w7" style="font-size:36px;line-height:1.45" data-x="text">{("+ " if j else "") + e(p.strip().rstrip("."))}</div>' for j, p in enumerate(a_t.split('+')) if p.strip().rstrip('.'))}</div>
 <div class="card o" style="left:110px;top:650px;width:420px;height:330px;display:flex;flex-direction:column;justify-content:space-between" data-x="shape" {A("rise", 950)}>
   <span class="w7" style="font-size:33px;color:var(--ink)" data-x="text">{e(b_l.rstrip(':'))}</span>
   <div><span class="w9 f-num" style="font-size:150px;line-height:.95;color:#fff" data-x="text" {A("zoom", 1150, 700)}>{num}</span>
   <div class="w5" style="font-size:36px;color:var(--ink)" data-x="text">{e(cur)}</div></div></div>'''
    return frame(n, 12, e(strip_num(T(425))), inner, 'camp', extra_css=EXTRA_CSS, title_style='right:250px;top:136px')


def s_msg(n, mi):
    sub = T(430).rstrip(':')
    if mi == 0:
        label = T(431); hook = T(432); body = [T(433), T(434), T(435)]; pk = list(range(436, 441)); cta = T(441)
    elif mi == 1:
        label = T(443); hook = T(444); body = [T(445)]; pk = list(range(446, 451)); cta = T(451)
    else:
        ls = L(453); label = ls[0]; hook = ls[1]; body = [T(454)]; pk = list(range(455, 460)); cta = T(460)
    m = re.match(r'(\d+)\s*\.\s*(.*)', label)
    num, lab = int(m.group(1)), m.group(2)
    items = ''
    for i, pi in enumerate(pk):
        ic, txt = split_emoji(T(pi))
        items += (f'<div style="display:flex;align-items:center;gap:20px;padding:12px 0;border-bottom:2px solid rgba(255,255,255,.16)" {A("rise", 700 + i * 110)}>'
                  f'<span style="width:68px;height:68px;border-radius:20px;background:rgba(255,255,255,.14);display:flex;align-items:center;justify-content:center;flex:none" data-x="snap">{icon(ic, "#fff", "var(--y)", 42)}</span>'
                  f'<span class="w5" style="font-size:33px" data-x="text">{e(txt)}</span></div>')
    bsize = 44 if mi else 40
    bl = ''.join(f'<p style="font-size:{bsize}px;line-height:1.55;margin-top:14px" data-x="text" {A("rise", 450 + j * 100)}>{e(b)}</p>' for j, b in enumerate(body))
    inner = f'''
 <div class="abs" style="right:110px;top:140px;width:104px;height:104px;border-radius:50%;background:var(--o);display:flex;align-items:center;justify-content:center" data-x="shape" {A("pop", 0)}>
   <span class="w9 f-num" style="font-size:52px;color:var(--ink);line-height:1" data-x="text">{num:02d}</span></div>
 <div class="card w" style="right:110px;top:285px;width:1060px;height:575px" data-x="shape" {A("rise", 150)}>
   <p class="w9 f-swash" style="font-size:{62 if len(hook) < 60 else 54}px;line-height:1.45;color:var(--b);margin-bottom:14px" data-x="text" {A("rise", 300)}>{e(hook)}</p>
   {bl}</div>
 <div class="card b" style="left:110px;top:285px;width:620px;height:695px;padding:34px 40px" data-x="shape" {A("rise", 550)}>
   <div style="display:flex;align-items:center;gap:16px;margin-bottom:8px">{chip_icon('package', 70, 44, 'var(--y)', 'var(--ink)', '#fff', 22)}<span class="w7" style="font-size:31px;color:var(--y)" data-x="text">{e(lab)}</span></div>
   {items}</div>
 <div class="card o" style="right:110px;top:885px;width:1060px;height:95px;padding:0 30px;display:flex;align-items:center;gap:20px" data-x="shape" {A("pop", 1400)}>
   {chip_icon('whatsapp-logo', 64, 40, '#fff', 'var(--o2)', 'var(--y)', 32)}
   <span class="w7" style="font-size:36px;color:var(--ink)" data-x="text">{e(cta)}</span></div>'''
    return frame(n, 12, f'{e(sub)} <em>· {e(lab)}</em>', inner, 'msg', extra_css=EXTRA_CSS, title_style='right:250px;top:136px')


# ================================================================ 13. KPIs
def s_kpi(n):
    icons = ['broadcast', 'eye', 'cursor-click', 'coins', 'whatsapp-logo', 'users-three', 'receipt', 'arrows-clockwise', 'hand-coins', 'shopping-cart', 'chart-line-up']
    tiles = ''
    for i, pi in enumerate(range(466, 477)):
        t = T(pi).rstrip(':').strip()
        if ' – ' in t:
            en, ar = [x.strip() for x in t.split(' – ', 1)]
        else:
            en, ar = '', t
        r = i // 4
        c = i % 4
        x = 110 + c * 430
        y = 380 + r * 205
        tone = 'b' if i == 0 else ('o' if i == 10 else 'w')
        dark = tone == 'b'
        tiles += (f'<div class="card {tone}" style="right:{x}px;top:{y}px;width:405px;height:185px;padding:24px 28px;display:flex;align-items:center;gap:20px;color:{"#fff" if dark else "var(--ink)"}" data-x="shape" {A("rise", 300 + i * 80)}>'
                  f'{chip_icon(icons[i], 80, 48, "rgba(255,255,255,.16)" if dark else ("#fff" if tone == "o" else "var(--bt)"), "#fff" if dark else ("var(--o2)" if tone == "o" else "var(--b)"), "var(--y)", 24, A("pop", 450 + i * 80))}'
                  f'<div>' + (f'<div class="w9 lat" style="font-size:{40 if len(en) < 12 else 27}px;line-height:1.2;text-align:right;color:{"var(--y)" if dark else ("#fff" if tone == "o" else "var(--b)")}" data-x="text">{e(en)}</div>' if en else '') +
                  f'<div class="w5" style="font-size:{30 if en else 33}px;line-height:1.35" data-x="text">{e(ar)}</div></div></div>')
    inner = f'''
 <div class="abs w5" style="right:110px;top:268px;display:flex;align-items:center;gap:16px" {A("rise", 100)}>
   {chip_icon('gauge', 72, 44, 'var(--y)', 'var(--ink)', '#fff', 22)}<span style="font-size:36px;color:var(--o2)" data-x="text">{e(T(464).rstrip(': '))}</span></div>
 {tiles}'''
    return frame(n, 13, e(T(465)), inner, 'kpi', extra_css=EXTRA_CSS)


# ================================================================ closing
def s_close(n):
    t1, t2 = T(43).split(' لمشروع ')
    t2a, t2b = t2.split(' – ')
    return f'''
<section class="slide dark closing" data-tr="morph">
 <div class="bgfill bg-blue" data-x="bg"></div><div class="grain"></div>
 <style>.closing .hud-c i{{border-color:rgba(255,255,255,.35)}}</style>
 <div class="abs" style="left:-300px;top:-210px;width:1420px;height:1420px;border-radius:50%;background:rgba(255,255,255,.06)" data-x="shape" data-name="!!lens"></div>
 <div class="abs" style="left:40px;top:120px;width:840px;height:840px;border-radius:50%;background:rgba(255,255,255,.08)" data-x="shape" data-name="!!lens2"></div>
 {mark(222, 215, 650, 0, 'o', glint='y', names=MN)}
 <div class="abs" style="left:760px;top:190px;width:62px;height:62px;border-radius:50%;background:var(--y)" data-x="shape" data-name="!!dot"></div>
 {hud(n, dark=True)}
 <img class="abs" style="right:110px;top:210px;height:220px" src="assets/word_w.svg" data-x="asset" data-src="word_w" {A("rise", 300, 900)}>
 <div class="abs" style="right:110px;top:470px;width:1000px">
   <div class="w9 f-disp" style="font-size:120px;line-height:1.25;color:#fff" data-x="snap" {A("wipeR", 600, 900)}>{e(t1)}</div>
   <div class="w5" style="font-size:60px;line-height:1.4;color:#fff" data-x="text" {A("rise", 900)}>لمشروع <span class="w7" style="color:var(--y)">{e(t2a)}</span> – <span class="lat">{e(t2b)}</span></div>
 </div>
 <div class="abs" style="right:110px;top:830px;display:flex;align-items:center;gap:22px" {A("rise", 1200)}>
   {chip_icon('user-circle', 84, 50, 'rgba(255,255,255,.14)', '#fff', 'var(--y)', 26)}
   <div><div style="font-size:28px;color:rgba(255,255,255,.75)" data-x="text">{e(kv(T(1))[0])}</div><div class="w5" style="font-size:38px" data-x="text">{e(kv(T(1))[1])}</div></div></div>
 <img class="abs" style="right:110px;top:70px;height:74px" src="assets/basmat_w.svg" data-x="asset" data-src="basmat_w" {A("fade", 1400)}>
</section>'''
