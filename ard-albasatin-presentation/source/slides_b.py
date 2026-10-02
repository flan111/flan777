# -*- coding: utf-8 -*-
"""Sections 4 (study), 5 (audience), 6 (competitors)."""
from slides_a import *


def hl(s, phrase, color='var(--forest)', w='w8'):
    return s.replace(e(phrase), f'<b class="{w}" style="color:{color}">{e(phrase)}</b>')


# ------------------------------------------------------------------ 4. study
def s_desc(n):
    b = frame(n, 'L', sec=SEC(4))
    b += heading(T(56), k=2)
    b += text(110, 300, 1060, hl(e(T(57)), 'أرض البساتين'), cls='w3', a='rise', d=300, style='font-size:39px;line-height:1.65')
    b += box(110, 650, 1060, 330, cls='card mint2 leafcard', a='rise', d=600, right=True)
    b += text(160, 690, 960, e(T(58)), cls='body', a='rise', d=700, style='font-size:32px;line-height:1.62')
    prods = ['drop', 'pipe', 'drop-half', 'umbrella', 'shield-check', 'plant']
    for k, ic in enumerate(prods):
        b += ico(ic, 1920 - 160 - 960 + k * 120 + 250, 875, s=84, tile='w', a='pop', d=900 + k * 80)
    # factory column
    b += box(110, 140, 540, 840, cls='card teal leafcard', a='rise', d=500, right=False)
    b += ico('factory', 110 + 40, 190, s=130, tile='lime', a='pop', d=800)
    b += text(1920 - 110 - 540 + 40, 360, 460, hl(e(T(59)), 'مصنع دريب أكوا', 'var(--lime)'), cls='w4', a='rise', d=850, style='font-size:31px;line-height:1.62;color:#fff')
    return slide('L', b)


def s_problem(n):
    b = frame(n, 'E', sec=SEC(4))
    b += heading(T(60), k=1)
    # problem (earth)
    b += box(110, 310, 820, 670, cls='card leafcard', a='rise', d=300, right=True, style='background:#EADCC8')
    b += ico('warning', 1920 - 110 - 40 - 110, 350, s=110, tile='w', fg=C['brown'], du=C['clay'], a='pop', d=500)
    b += text(150, 500, 740, e(T(61)), cls='w5', a='rise', d=550, style='font-size:36px;line-height:1.62;color:var(--soil)')
    # drip connector
    b += dripline(950, 645, 60, color=C['clay'], emit=C['brown'], step=20, sw=2, a='wipeR', d=800)
    # solution (green)
    b += box(990, 310, 820, 670, cls='card forest leafcard', a='rise', d=900, right=True)
    b += ico('seal-check', 1920 - 990 - 40 - 110, 350, s=110, tile='lime', a='pop', d=1100)
    b += text(1030, 490, 740, hl(e(T(62)), 'أرض البساتين', 'var(--lime)'), cls='w4', a='rise', d=1150, style='font-size:31px;line-height:1.6;color:#fff')
    b += box(1030, 745, 740, 2, cls='abs', a='wipeR', d=1300, right=True, style='background:rgba(255,255,255,.25)')
    b += text(1030, 770, 740, hl(e(T(63)), 'مصنع دريب أكوا', 'var(--lime)'), cls='w3', a='rise', d=1350, style='font-size:29px;line-height:1.6;color:rgba(255,255,255,.92)')
    return slide('E', b)


def s_value(n):
    b = frame(n, 'L', sec=SEC(4))
    b += heading(T(64), k=1)
    items = [T(i) for i in range(65, 76)]
    icons = ['grains', 'stack', 'list-magnifying-glass', 'shield-check', 'drop', 'factory', 'seal-check', 'list-plus', 'hand-pointing', 'hourglass-medium', 'chat-circle-dots']
    cw, ch, gx, gy = 553, 150, 20, 18
    for k, (it, ic) in enumerate(zip(items, icons)):
        c, r = k % 3, k // 3
        xr = 110 + c * (cw + gx)
        y = 300 + r * (ch + gy)
        d = 300 + k * 70
        strong = k == 5
        b += box(xr, y, cw, ch, cls='card leafcard ' + ('teal' if strong else 'mint2'), a='rise', d=d, right=True)
        b += ico(ic, 1920 - xr - 26 - 88, y + 31, s=88, tile='lime' if strong else 'w', a='pop', d=d + 120)
        b += text(xr + 136, y + 18, cw - 160, e(it), cls='w7' if strong else 'w5', a='rise', d=d + 80,
                  style='font-size:28px;line-height:1.4;height:114px;display:flex;align-items:center;' + ('color:#fff;' if strong else ''))
    # 12th cell: brand leaves
    xr = 110 + 2 * (cw + gx); y = 300 + 3 * (ch + gy)
    b += box(xr, y, cw, ch, cls='card leafcard lime', a='rise', d=1200, right=True)
    b += leaves(1920 - xr - cw + 170, y + 22, 106, rot=0, v='dk', names=('', ''), a='grow', d=1400)
    return slide('L', b)


# ------------------------------------------------------------------ 5. audience
def s_demo(n):
    b = frame(n, 'L', sec=SEC(5))
    b += heading(T(78), k=1)
    rows = [kv(T(i)) for i in range(79, 84)]
    # map (left)
    mw = 700
    sc = mw / YEM['w']
    mh = YEM['h'] * sc
    mx, my = 100, 360
    paths = ''.join(f'<path d="{d}"/>' for d in YEM['d'])
    svg = (f'<svg width="{mw}" height="{mh:.0f}" viewBox="0 0 {YEM["w"]} {YEM["h"]}">'
           f'<g fill="#E3F3E9" stroke="#35B86E" stroke-width="3" stroke-linejoin="round">{paths}</g></svg>')
    b += snap(mx, my, mw, int(mh) + 2, svg, a='fade', d=300)
    for k, (city, (cx, cy)) in enumerate(YEM['cities'].items()):
        px, py = mx + cx * sc, my + cy * sc
        b += snap(px - 21, py - 56, 42, 56, drop_svg(C['brown'], 42), a='drop', d=900 + k * 220)
        lx = {'صنعاء': (px + 26, py - 60), 'الحديدة': (px - 30, py + 6), 'ذمار': (px + 26, py - 4)}[city]
        b += textl(lx[0], lx[1], 220, e(city), cls='w7', a='fade', d=1050 + k * 220, style=f'font-size:28px;line-height:1.3;color:{C["soil"]}')
    # facts (right)
    y = 300
    ages = rows[0][1]
    b += text(110, y, 300, e(rows[0][0]), cls='w6', a='fade', d=300, style='font-size:28px;line-height:1.3;color:var(--leaf)')
    num, unit = ages.split(' ', 1)
    b += text(110, y + 38, 900, f'<span class="w9 num">{e(num)}</span> <span class="w3">{e(unit)}</span>', cls='', a='zoomOut', d=400, style='font-size:76px;line-height:1.2;color:var(--ink)')
    y = 470
    for k, (lab, val) in enumerate(rows[1:]):
        d = 600 + k * 140
        b += box(110, y - 14, 930, 2, cls='abs', a='wipeR', d=d, right=True, style=f'background:{C["line"]}')
        b += text(110, y, 250, e(lab), cls='w6', a='rise', d=d, style='font-size:28px;line-height:1.45;color:var(--leaf)')
        b += text(380, y, 660, e(val), cls='w4', a='rise', d=d + 40, style='font-size:30px;line-height:1.45')
        y += max(est_lines(val, 30, 660), est_lines(lab, 28, 250)) * 44 + 42
    return slide('L', b)


def s_interests(n):
    b = frame(n, 'D', sec=SEC(5))
    b += heading(T(84), k=1)
    items = [T(i) for i in range(85, 95)]
    icons = ['plant', 'tractor', 'drop', 'drop-half-bottom', 'cloud-sun', 'shield-check', 'seal-check', 'tree', 'map-pin', 'chart-line-up']
    cw, ch, gx, gy = 326, 300, 17, 26
    for k, (it, ic) in enumerate(zip(items, icons)):
        c, r = k % 5, k // 5
        xr = 110 + c * (cw + gx)
        y = 320 + r * (ch + gy)
        d = 300 + k * 90
        b += box(xr, y, cw, ch, cls='card glass leafcard', a='rise', d=d, right=True)
        b += ico(ic, 1920 - xr - 30 - 96, y + 32, s=96, tile='lime' if k % 3 == 0 else 'rgba(255,255,255,.12)',
                 fg=None if k % 3 == 0 else '#fff', du=None if k % 3 == 0 else C['lime'], a='pop', d=d + 140)
        b += text(xr + 30, y + 150, cw - 56, e(it), cls='w6', a='rise', d=d + 100, style='font-size:29px;line-height:1.42;color:#fff')
    return slide('D', b)


def s_needs(n):
    b = frame(n, 'E', sec=SEC(5))
    b += heading(T(95), k=1)
    items = [T(i) for i in range(96, 104)]
    icons = ['seal-check', 'storefront', 'plant', 'list-magnifying-glass', 'drop', 'wrench', 'package', 'question']
    cw, ch, gx, gy = 840, 140, 20, 20
    for k, (it, ic) in enumerate(zip(items, icons)):
        c, r = k % 2, k // 2
        xr = 110 + c * (cw + gx)
        y = 310 + r * (ch + gy)
        d = 300 + k * 90
        b += box(xr, y, cw, ch, cls='card leafcard', a='rise', d=d, right=True, style='background:#FFFFFF')
        b += ico(ic, 1920 - xr - 24 - 92, y + 24, s=92, tile='sand2', fg=C['brown'], du=C['clay'], a='pop', d=d + 120)
        b += text(xr + 140, y + 20, cw - 170, e(it), cls='w5', a='rise', d=d + 80,
                  style='font-size:30px;line-height:1.42;height:100px;display:flex;align-items:center;color:var(--soil)')
    return slide('E', b)


def s_behavior(n):
    b = frame(n, 'L', sec=SEC(5))
    b += heading(T(104), k=1)
    items = [T(i) for i in range(105, 112)]
    strong = {0, 4, 6}
    # insight cards for the three emphasised behaviours (left)
    b += box(110, 300, 760, 680, cls='card teal leafcard', a='rise', d=300)
    ics = {0: 'scales', 4: 'chats-circle', 6: 'handshake'}
    y = 340
    for j, k in enumerate(sorted(strong)):
        d = 500 + j * 200
        b += ico(ics[k], 150, y, s=92, tile='lime', a='pop', d=d)
        b += textl(270, y - 2, 560, e(items[k]), cls='w6', a='rise', d=d + 60, style='font-size:30px;line-height:1.48;color:#fff')
        if k == 4:
            for q, pi in enumerate(['facebook-logo', 'whatsapp-logo']):
                b += snap(270 + q * 64, y + 92, 48, 48, icon(pi, '#C3E36B', 'rgba(195,227,107,.25)', 48), a='pop', d=d + 200 + q * 80)
        y += 210
    # the other behaviours (right)
    rest = [items[k] for k in range(len(items)) if k not in strong]
    b += ilist(rest, 110, 340, 820, None, fs=33, d0=900, step=120, sep=True, gap=70)
    return slide('L', b)


# ------------------------------------------------------------------ 6. competitors
def s_comp_id(n):
    b = frame(n, 'L', sec=SEC(6))
    b += heading(T(114), k=1)
    T(119)          # a stray "." paragraph in the source
    cards = [(T(115, colon=False), T(116), 'storefront'), (T(117, colon=False), T(118), 'truck')]
    for k, (h, t, ic) in enumerate(cards):
        xr = 110 + k * 870
        d = 300 + k * 300
        num, h2 = h.split(' ', 1)
        b += box(xr, 330, 830, 640, cls=f'card leafcard {"mint" if k == 0 else "mint2"}', a='rise', d=d, right=True)
        b += text(xr + 50, 360, 300, num.rstrip('.'), cls='w1 num', a='zoomOut', d=d + 150, style=f'font-size:200px;line-height:1;color:{C["brand"]}')
        b += ico(ic, 1920 - xr - 830 + 60, 380, s=140, tile='w' if k == 0 else 'lime', a='pop', d=d + 250)
        b += text(xr + 50, 620, 730, e(h2), cls='w8', a='wipeR', d=d + 200, style='font-size:46px;line-height:1.35')
        b += text(xr + 50, 720, 730, e(t), cls='w4', a='rise', d=d + 300, style='font-size:33px;line-height:1.6;color:var(--mut)')
    return slide('L', b)


def s_comp_sw(n):
    b = frame(n, 'L', sec=SEC(6))
    st = [T(i) for i in range(121, 125)]
    wk = [T(i) for i in range(126, 132)]
    # strengths (right column)
    b += box(110, 140, 820, 840, cls='card mint leafcard', a='rise', d=200, right=True)
    b += ico('trend-up', 990 + 40, 175, s=96, tile='w', a='pop', d=400)
    h = ORD.sub('', T(120, colon=False))
    b += text(110 + 50, 210, 600, e(h), cls='w8', a='wipeR', d=350, style='font-size:42px;line-height:1.3')
    b += text(110 + 50, 168, 600, e(ORD.match(T(120)).group(1)), cls='w6', a='fade', d=300, style='font-size:26px;line-height:1.3;color:var(--leaf)')
    b += ilist(st, 160, 330, 720, None, fs=32, d0=500, step=110, sep=True, sepc='#C9E5D3', gap=60)
    # weaknesses (left column)
    b += box(990, 140, 820, 840, cls='card sand leafcard', a='rise', d=500, right=True)
    b += ico('trend-down', 110 + 40, 175, s=96, tile='w', fg=C['brown'], du=C['clay'], a='pop', d=700)
    h = ORD.sub('', T(125, colon=False))
    b += text(990 + 50, 210, 640, e(h), cls='w8', a='wipeR', d=650, style='font-size:38px;line-height:1.3;color:var(--soil);white-space:nowrap')
    b += text(990 + 50, 168, 600, e(ORD.match(T(125)).group(1)), cls='w6', a='fade', d=600, style='font-size:26px;line-height:1.3;color:var(--brown)')
    b += ilist(wk, 1040, 330, 720, None, fs=31, mk=C['brown'], d0=800, step=100, sep=True, sepc='#E6D8C4', color=C['soil'], gap=34, maxh=620)
    return slide('L', b)


def s_comp_style(n):
    b = frame(n, 'L', sec=SEC(6))
    b += heading(T(132), k=1)
    items = [T(i) for i in range(133, 138)]
    icons = ['handshake', 'truck', 'chats-circle', 'tag', 'package']
    cw, gx = 326, 17
    b += dripline(140, 455, 1640, color='#BFE0CC', emit=C['brand'], step=41, sw=2, a='wipeR', d=300)
    for k, (it, ic) in enumerate(zip(items, icons)):
        xr = 110 + k * (cw + gx)
        d = 450 + k * 150
        b += ico(ic, 1920 - xr - cw / 2 - 70, 385, s=140, tile='lime' if k == 4 else 'mint', a='pop', d=d)
        b += box(xr, 580, cw, 380, cls='card mint2 leafcard', a='rise', d=d + 60, right=True)
        b += text(xr + 30, 610, 70, f'{k + 1:02d}', cls='w2 num', a='rise', d=d + 100, style=f'font-size:40px;line-height:1.2;color:{C["brand"]}')
        b += text(xr + 30, 680, cw - 60, e(it), cls='w5', a='rise', d=d + 140, style='font-size:31px;line-height:1.5')
    return slide('L', b)


def s_comp_opp(n):
    b = frame(n, 'D', sec=SEC(6))
    b += heading(T(138), k=1)
    t = e(T(139))
    for ph in ['تنوع المنتجات', 'المحتوى الزراعي المفيد', 'وضوح المواصفات', 'جودة اختيار المنتجات', 'وسهولة التواصل والشراء']:
        t = t.replace(ph, f'<b class="w7" style="color:var(--lime)">{ph}</b>', 1)
    b += text(110, 310, 1700, t, cls='w3', a='rise', d=300, style='font-size:44px;line-height:1.62;color:#fff')
    b += box(110, 690, 1700, 290, cls='card glass leafcard', a='rise', d=700, right=True)
    b += ico('factory', 1920 - 110 - 50 - 130, 770, s=130, tile='lime', a='pop', d=900)
    b += text(330, 730, 1420, hl(e(T(140)), 'مصنع دريب أكوا', 'var(--lime)'), cls='w4', a='rise', d=850, style='font-size:33px;line-height:1.62;color:rgba(255,255,255,.92)')
    return slide('D', b)
