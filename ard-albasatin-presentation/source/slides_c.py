# -*- coding: utf-8 -*-
"""Sections 7 (SWOT) and 8 (marketing strategy)."""
from slides_b import *

SWOT = {  # heading paragraph -> (items, letter, tone)
    'S': (143, range(144, 152), C['forest'], C['mint'], 'w'),
    'W': (152, range(153, 158), C['brown'], C['sand'], 'sand2'),
    'O': (158, range(159, 167), C['teal'], '#DDF0EE', 'w'),
    'T': (167, range(168, 175), C['soil'], C['sand2'], 'w'),
}


def swot_half(xr, key, d0, rowh, fs):
    hp, rng, ink, bg, _ = SWOT[key]
    head = T(hp, colon=False)
    ordn = ORD.match(head).group(1)
    head = ORD.sub('', head)
    ar, en = re.match(r'^(.*?)\s*\((.*?)\)\s*$', head).groups()
    out = box(xr, 140, 830, 840, cls='card leafcard', a='rise', d=d0, right=True, style=f'background:{bg}')
    # giant initial, very thin, as a watermark
    out += textl(1920 - xr - 830 + 30, 120, 300, key, cls='w1 lat', a='zoomOut', d=d0 + 150, style=f'font-size:300px;line-height:1;color:{ink};opacity:.18')
    out += text(xr + 50, 172, 600, e(ordn), cls='w6', a='fade', d=d0 + 100, style=f'font-size:26px;line-height:1.3;color:{ink}')
    out += text(xr + 50, 212, 700, f'{e(ar)} <span class="w3 lat" style="font-size:30px">({e(en)})</span>', cls='w8', a='wipeR', d=d0 + 150, style=f'font-size:44px;line-height:1.3;color:{ink}')
    items = [T(i) for i in rng]
    bold = tuple(k for k, i in enumerate(rng) if i in (146,))
    out += ilist(items, xr + 50, 318, 740, None, fs=30, mk=ink, bold=bold, d0=d0 + 300, step=90, color=C['ink'] if key in 'SO' else C['soil'], gap=rowh, maxh=640)
    return out


def s_swot1(n):
    b = frame(n, 'L', sec=SEC(7))
    b += swot_half(110, 'S', 200, 18, 29)
    b += swot_half(980, 'W', 700, 40, 30)
    return slide('L', b)


def s_swot2(n):
    b = frame(n, 'L', sec=SEC(7))
    b += swot_half(110, 'O', 200, 18, 29)
    b += swot_half(980, 'T', 700, 24, 29)
    return slide('L', b)


# ------------------------------------------------------------------ 8. strategy
def s_goal_main(n):
    b = frame(n, 'G', sec=SEC(8))
    b += heading(T(177), k=2)
    t = e(T(178))
    t = t.replace('بناء حضور رقمي قوي', '<b class="w8">بناء حضور رقمي قوي</b>', 1)
    t = t.replace('وتحويل الاهتمام الرقمي إلى استفسارات وطلبات ومبيعات', '<b class="w8" style="color:var(--lime)">وتحويل الاهتمام الرقمي إلى استفسارات وطلبات ومبيعات</b>', 1)
    b += text(110, 330, 1240, t, cls='w3', a='rise', d=300, style='font-size:46px;line-height:1.66;color:#fff')
    # target rings
    cx, cy = 300, 640
    for k, (r, op) in enumerate([(230, .10), (165, .16), (100, .24)]):
        b += dot(cx - r, cy - r, 2 * r, f'rgba(255,255,255,{op})', a='zoom', d=500 + k * 150)
    b += ico('target', cx - 60, cy - 60, s=120, tile='lime', shape='circle', a='pop', d=1000)
    b += snap(cx + 70, cy - 230, 110, 145, drop_svg(C['lime'], 110), a='drop', d=1300)
    return slide('G', b)


def s_goals8(n):
    b = frame(n, 'L', sec=SEC(8))
    b += heading(T(179), k=1)
    items = [T(i) for i in range(180, 191)]
    b += numlist(items, 110, 316, 1700, 112, fs=30, bold=(0, 4), cols=2, colgap=80, d0=300, step=70)
    return slide('L', b)


def s_platwhy(n):
    b = frame(n, 'L', sec=SEC(8))
    b += heading(T(191), k=2)
    rows = TB[192]
    hdr = rows[0]
    b += text(110, 300, 380, e(hdr[0]), cls='w6', a='fade', d=250, style='font-size:26px;line-height:1.3;color:var(--mut)')
    b += text(560, 300, 1200, e(hdr[1]), cls='w6', a='fade', d=250, style='font-size:26px;line-height:1.3;color:var(--mut)')
    y = 350
    for k, (nm, why) in enumerate(rows[1:]):
        d = 350 + k * 130
        h = 118
        b += box(110, y, 1700, h, cls='card leafcard ' + ('mint2' if k % 2 == 0 else 'mint'), a='rise', d=d, right=True)
        b += ico(PLATFORM_ICON[nm.strip()], 1920 - 110 - 24 - 80, y + 19, s=80, tile='lime' if k % 2 == 0 else 'w', a='pop', d=d + 100)
        latin = nm.strip().isascii()
        b += text(240, y + 32, 300, e(nm.strip()), cls='w8' + (' lat' if latin else ''), a='rise', d=d + 60, style='font-size:34px;line-height:1.3;' + ('text-align:right;' if latin else ''))
        b += text(560, y + 16, 1210, e(why.strip()), cls='w4', a='rise', d=d + 100, style='font-size:30px;line-height:1.45;height:86px;display:flex;align-items:center')
        y += h + 14
    return slide('L', b)


STYLES = [(195, 196, 'graduation-cap'), (197, 198, 'package'), (199, 200, 'seal-check'),
          (201, 202, 'scales'), (203, (204, 205, 206, 207), 'chat-circle-dots'), (208, 209, 'shopping-cart')]


def style_card(xr, y, w, h, hp, bp, ic, d, dark=False, big=False):
    head = T(hp, colon=False)
    num, hd = head.split(' ', 1)
    out = box(xr, y, w, h, cls='card leafcard ' + ('teal' if dark else 'mint2'), a='rise', d=d, right=True)
    out += ico(ic, 1920 - xr - 36 - 92, y + 34, s=92, tile='lime' if dark else 'w', a='pop', d=d + 150)
    out += textl(1920 - xr - w + 36, y + 30, 120, num.rstrip('.'), cls='w1 num', a='zoomOut', d=d + 100, style=f'font-size:84px;line-height:1;color:{C["lime"] if dark else C["brand"]};text-align:left')
    hs, bs = (42, 32) if big else (36, 29)
    out += text(xr + 36, y + 150, w - 72, e(hd), cls='w8', a='wipeR', d=d + 120, style=f'font-size:{hs}px;line-height:1.3;' + ('color:#fff;' if dark else ''))
    col = 'color:rgba(255,255,255,.9);' if dark else ''
    if isinstance(bp, tuple):
        out += text(xr + 36, y + 150 + hs * 1.3 + 22, w - 72, e(T(bp[0])), cls='w4', a='rise', d=d + 200, style=f'font-size:{bs}px;line-height:1.5;{col}')
        yq = y + 150 + hs * 1.3 + 22 + bs * 1.5 + 18
        for j, q in enumerate(bp[1:]):
            out += text(xr + 36, yq, w - 72, e(T(q)), cls='w6', a='rise', d=d + 280 + j * 90, style=f'font-size:{bs - 1}px;line-height:1.5;color:{C["forest"]}')
            yq += est_lines(T(q), bs - 1, w - 72) * (bs - 1) * 1.5 + 12
    else:
        out += text(xr + 36, y + 150 + hs * 1.3 + 22, w - 72, e(T(bp)), cls='w4', a='rise', d=d + 200, style=f'font-size:{bs}px;line-height:1.55;{col}')
    return out


def s_style1(n):
    b = frame(n, 'L', sec=SEC(8))
    b += heading(T(193), k=2)
    t = e(T(194))
    t = t.replace('التسويق التعليمي + التوعوي + الاستعراضي + التفاعلي + البيعي', '<b class="w8" style="color:var(--forest)">التسويق التعليمي + التوعوي + الاستعراضي + التفاعلي + البيعي</b>')
    b += text(110, 345, 1700, t, cls='w3', a='rise', d=300, style='font-size:34px;line-height:1.6')
    for k, (hp, bp, ic) in enumerate(STYLES[:3]):
        b += style_card(110 + k * 573, 500, 553, 480, hp, bp, ic, 500 + k * 180, dark=(k == 2))
    return slide('L', b)


def s_style2(n):
    b = frame(n, 'L', sec=SEC(8))
    b += heading(T(193), k=2)
    for k, (hp, bp, ic) in enumerate(STYLES[3:]):
        b += style_card(110 + k * 573, 345, 553, 635, hp, bp, ic, 300 + k * 180, dark=(k == 2), big=True)
    return slide('L', b)


def s_journey(n):
    b = frame(n, 'D', sec=SEC(8))
    b += heading(T(211), k=2, size=72)
    stages = [(212, 213, 'eye'), (215, 216, 'storefront'), (218, 219, 'scales'), (221, 222, 'chat-circle-dots'), (224, 225, 'shopping-cart'), (227, 228, 'heart')]
    for k in (214, 217, 220, 223, 226):
        T(k)    # the arrows between stages become the drip line itself
    cw, gx = 540, 40
    ly = (330, 676)
    # one drip line snaking through the six stages: row 1 right->left, row 2 left->right
    b += dripline(150, ly[0], 1620, color='rgba(195,227,107,.55)', emit='#C3E36B', step=40, sw=2, a='wipeR', d=300)
    b += snap(96, ly[0] - 2, 60, ly[1] - ly[0] + 4, f'<svg width="60" height="{ly[1] - ly[0] + 4}"><path d="M56 2 C 0 2 0 {ly[1] - ly[0] + 2} 56 {ly[1] - ly[0] + 2}" fill="none" stroke="rgba(195,227,107,.55)" stroke-width="2"/></svg>', a='wipeD', d=1000)
    b += dripline(150, ly[1], 1620, color='rgba(195,227,107,.55)', emit='#C3E36B', step=40, sw=2, a='wipeL', d=1300)
    for k, (hp, bp, ic) in enumerate(stages):
        r, c = k // 3, k % 3
        if r == 1:
            c = 2 - c
        xr = 110 + c * (cw + gx)
        y = ly[r]
        d = 400 + k * 260 + (500 if r else 0)
        head = T(hp)
        num, rest = head.split(' ', 1)
        ar, en = [x.strip() for x in rest.split('–')]
        hi = k in (0, 4)
        b += ico(ic, 1920 - xr - 88, y - 44, s=88, tile='lime' if hi else '#0F6E6B', shape='circle',
                 fg=None if hi else '#fff', du=None if hi else C['lime'], a='pop', d=d)
        b += text(xr, y + 62, cw, f'<span class="w2 num" style="color:var(--lime)">{e(num.rstrip("."))}</span> {e(ar)} <span class="w3" style="color:var(--lime);font-size:26px">–</span> <span class="w3 lat" style="color:var(--lime);font-size:26px">{e(en)}</span>', cls='w8', a='wipeR', d=d + 60, style='font-size:34px;line-height:1.3;color:#fff')
        b += text(xr, y + 116, cw, e(T(bp)), cls='w3', a='rise', d=d + 120, style='font-size:27px;line-height:1.5;color:rgba(255,255,255,.9)')
    return slide('D', b)
