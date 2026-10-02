# -*- coding: utf-8 -*-
"""Section 9 (content plan) and the marketing-content examples."""
from slides_c import *

TYPE_COL = {
    'تعريفي': (C['teal'], '#fff'), 'تعليمي': (C['forest'], '#fff'), 'منتج': (C['brand'], '#fff'),
    'فيديو قصير': (C['aqua'], C['teal9']), 'فيديو': (C['aqua'], C['teal9']), 'تفاعلي': (C['lime'], C['teal9']),
    'بيعي': (C['brown'], '#fff'), 'عرض': (C['brown'], '#fff'), 'دعوة للشراء': (C['brown'], '#fff'),
    'توعوي': (C['clay'], '#fff'), 'مقارنة توعوية': (C['clay'], '#fff'), 'ثقة': (C['teal9'], C['lime']),
    'موجه للمزارعين': (C['mint'], C['forest']), 'موجه للتجار': (C['mint'], C['forest']), 'موجه للمنظمات': (C['mint'], C['forest']),
}
WEEKS = [(232, 233, 'megaphone'), (234, 235, 'seal-check'), (236, 237, 'target'), (238, 239, 'handshake')]


def week_parts(pi):
    a, b_ = T(pi).split(':', 1)
    return a.strip(), b_.strip()


def s_plan(n):
    b = frame(n, 'L', sec=SEC(9))
    b += heading(sec_title(9), k=1)
    t = e(T(231)).replace('لمدة شهر كامل (4 أسابيع)', '<b class="w8" style="color:var(--forest)">لمدة شهر كامل (4 أسابيع)</b>')
    b += text(110, 300, 1700, t, cls='w3', a='rise', d=300, style='font-size:36px;line-height:1.62')
    b += dripline(150, 560, 1620, color='#BFE0CC', emit=C['brand'], step=40, sw=2, a='wipeR', d=600)
    for k, (pi, _, ic) in enumerate(WEEKS):
        wk, theme = week_parts(pi)
        xr = 110 + k * 430
        d = 700 + k * 200
        b += dot(1920 - xr - 205 - 30, 530, 60, C['lime'] if k == 0 else C['brand'], a='pop', d=d)
        b += text(1920 - (1920 - xr - 205 - 30) - 60, 538, 60, f'{k + 1}', cls='w8 num', a='pop', d=d + 30, align='center', style=f'font-size:30px;line-height:1.4;color:{C["teal9"] if k == 0 else "#fff"}')
        b += box(xr, 630, 410, 350, cls='card leafcard ' + ('teal' if k == 3 else 'mint2'), a='rise', d=d + 80, right=True)
        b += ico(ic, 1920 - xr - 34 - 88, 662, s=88, tile='lime' if k == 3 else 'w', a='pop', d=d + 200)
        dark = k == 3
        b += text(xr + 34, 780, 342, e(wk), cls='w5', a='rise', d=d + 150, style=f'font-size:27px;line-height:1.3;color:{C["lime"] if dark else C["leaf"]}')
        b += text(xr + 34, 824, 342, e(theme), cls='w8', a='rise', d=d + 200, style=f'font-size:33px;line-height:1.38;{"color:#fff" if dark else ""}')
    return slide('L', b)


def s_week(n, k):
    pi, ti, ic = WEEKS[k]
    wk, theme = week_parts(pi)
    rows = TB[ti]
    b = frame(n, 'L', sec=SEC(9))
    b += text(110, 128, 900, e(wk), cls='w6', a='fade', d=150, style='font-size:30px;line-height:1.3;color:var(--leaf)')
    b += title('', theme, top=168, size=72, d=200)
    # week progress drops (top-left)
    for j in range(4):
        b += dot(110 + j * 52, 200, 34, C['forest'] if j == k else C['line'], a='pop', d=300 + j * 60)
    hdr = rows[0]
    hy = 300
    b += text(130, hy, 170, e(hdr[0]), cls='w6', a='fade', d=300, style='font-size:24px;line-height:1.3;color:var(--mut)')
    b += text(330, hy, 280, e(hdr[1]), cls='w6', a='fade', d=300, align='center', style='font-size:24px;line-height:1.3;color:var(--mut)')
    b += text(660, hy, 1100, e(hdr[2]), cls='w6', a='fade', d=300, style='font-size:24px;line-height:1.3;color:var(--mut)')
    y, rh = 345, 90
    for r, (day, typ, idea) in enumerate(rows[1:]):
        d = 350 + r * 110
        b += box(110, y, 1700, rh - 10, cls='card ' + ('mint2' if r % 2 == 0 else ''), a='rise', d=d, right=True,
                 style='border-radius:22px;' + ('' if r % 2 == 0 else 'background:transparent'))
        b += text(140, y + 18, 170, e(day.strip()), cls='w8', a='rise', d=d + 40, style='font-size:30px;line-height:1.45')
        bg, fg = TYPE_COL[typ.strip()]
        b += chip(330, y + 15, typ.strip(), bg, fg, fs=24, w=280, h=50, d=d + 80)
        b += text(660, y + 4, 1120, e(idea.strip()), cls='w4', a='rise', d=d + 100, style='font-size:28px;line-height:1.4;height:72px;display:flex;align-items:center')
        y += rh
    return slide('L', b)


def s_dist(n):
    b = frame(n, 'L', sec=SEC(9))
    b += heading(T(241), k=1)
    items = [T(i) for i in range(242, 247)]
    vals = [int(re.match(r'(\d+)%', s).group(1)) for s in items]
    cols = [C['forest'], C['brand'], C['aqua'], C['lime'], C['brown']]
    # doughnut (SVG for the PDF, native chart in PowerPoint)
    R, sw, S = 230, 92, 620
    circ = 2 * math.pi * R
    arcs, acc = '', 0
    for v, c in zip(vals, cols):
        L_ = circ * v / 100
        arcs += (f'<circle cx="{S / 2}" cy="{S / 2}" r="{R}" fill="none" stroke="{c}" stroke-width="{sw}" '
                 f'stroke-dasharray="{L_ - 4:.2f} {circ - L_ + 4:.2f}" stroke-dashoffset="{-acc:.2f}" transform="rotate(-90 {S / 2} {S / 2})"/>')
        acc += L_
    chart = json.dumps({'labels': [re.sub(r'^\d+%\s*', '', s) for s in items], 'values': vals,
                        'colors': [c.lstrip('#') for c in cols], 'hole': 58, 'border': 'FFFFFF', 'name': T(241)}, ensure_ascii=False)
    b += (f'<div class="abs" data-x="chart" data-a="wheel" data-d="400" data-chart=\'{e(chart)}\' style="left:150px;top:330px;width:{S}px;height:{S}px">'
          f'<svg width="{S}" height="{S}">{arcs}</svg></div>')
    b += leaves(150 + S / 2 - 110, 330 + S / 2 - 62, 124, v='g', names=('', ''), a='grow', d=1400)
    for k, (s, c) in enumerate(zip(items, cols)):
        m = re.match(r'(\d+%)\s*(.*)$', s)
        y = 320 + k * 132
        d = 600 + k * 150
        b += box(110, y + 116, 900, 2, cls='abs', a='wipeR', d=d, right=True, style=f'background:{C["line"]}')
        b += text(110, y + 6, 230, e(m.group(1)), cls='w9 num lat', a='zoomOut', d=d, style=f'font-size:72px;line-height:1.3;color:{c if c != C["lime"] else "#8DB83A"};text-align:right')
        b += text(360, y + 30, 650, e(m.group(2)), cls='w6', a='rise', d=d + 60, style='font-size:34px;line-height:1.4')
    return slide('L', b)


def s_message(n):
    b = frame(n, 'D', sec=SEC(9), mark=False)
    b += text(110, 150, 900, e(T(248)), cls='w6', a='fade', d=200, style='font-size:32px;line-height:1.3;color:var(--lime)')
    b += text(110, 215, 1300, e(T(249)), cls='w8', a='wipeR', d=350, style='font-size:66px;line-height:1.4;color:#fff')
    b += box(110, 470, 1300, 2, cls='abs', a='wipeR', d=700, right=True, style='background:rgba(255,255,255,.18)')
    b += text(110, 510, 1300, e(T(250)), cls='w3', a='rise', d=800, style='font-size:36px;line-height:1.5;color:rgba(255,255,255,.85)')
    b += text(110, 580, 1300, e(T(251)), cls='w2', a='wipeR', d=1000, style='font-size:84px;line-height:1.35;color:var(--lime)')
    b += text(110, 800, 1100, e(T(252)), cls='w3', a='rise', d=1300, style='font-size:30px;line-height:1.55;color:rgba(255,255,255,.85)')
    for k, ic in enumerate(['facebook-logo', 'whatsapp-logo', 'tiktok-logo', 'instagram-logo']):
        b += ico(ic, 1920 - 1250 - 90 - k * 104 - 90, 820, s=84, tile='rgba(255,255,255,.12)', fg='#fff', du=C['lime'], shape='circle', a='pop', d=1500 + k * 90)
    b += leaves(120, 160, 260, rot=-10, v='g', a='grow', d=500, sway=True)
    return slide('D', b)


# ------------------------------------------------------------------ examples: social posts
PANEL = {
    'teal': 'radial-gradient(420px 380px at 80% 10%,rgba(195,227,107,.35),rgba(195,227,107,0) 70%),linear-gradient(160deg,#027068,#013B3E)',
    'forest': 'radial-gradient(420px 380px at 20% 0%,rgba(195,227,107,.45),rgba(195,227,107,0) 70%),linear-gradient(160deg,#029C3F,#01643B)',
    'earth': 'radial-gradient(420px 380px at 80% 0%,rgba(255,255,255,.35),rgba(255,255,255,0) 70%),linear-gradient(160deg,#B48A62,#7A5236)',
    'aqua': 'radial-gradient(420px 380px at 80% 0%,rgba(255,255,255,.4),rgba(255,255,255,0) 70%),linear-gradient(160deg,#5CC4BC,#027068)',
    'lime': 'radial-gradient(420px 380px at 20% 100%,rgba(2,156,63,.35),rgba(2,156,63,0) 70%),linear-gradient(160deg,#D6EC93,#9FCB4A)',
}


def panel(x, y, w, h, tone, ic, lines=(), d=300, video=False):
    """The 'creative' of a post: gradient, topographic lines, the brand leaves, one icon; optional overlay tagline."""
    fg = C['teal9'] if tone == 'lime' else '#fff'
    topo = 'assets/topo_dark.svg' if tone != 'lime' else 'assets/topo_light.svg'
    lv = 'w' if tone != 'lime' else 'dk'
    inner = (f'<div style="position:absolute;inset:0;border-radius:64px 10px 64px 10px;overflow:hidden;background:{PANEL[tone]}">'
             f'<img src="{topo}" style="position:absolute;left:-600px;top:-300px;width:2000px;opacity:1">'
             f'<img src="assets/gen/leafL_{lv}.svg" style="position:absolute;left:{w * .12:.0f}px;top:{h * .08:.0f}px;width:{w * .62:.0f}px;opacity:.16">'
             f'<img src="assets/gen/leafR_{lv}.svg" style="position:absolute;left:{w * .12:.0f}px;top:{h * .08:.0f}px;width:{w * .62:.0f}px;opacity:.16">'
             f'</div>')
    out = snap(x, y, w, h, inner, a='zoom', d=d)
    if video:
        out += dot(x + w / 2 - 60, y + h * .36 - 60, 120, 'rgba(255,255,255,.92)', a='pop', d=d + 300)
        out += snap(x + w / 2 - 26, y + h * .36 - 32, 64, 64, icon('play', C['forest'], C['lime'], 64), a='pop', d=d + 360)
        out += box(x + 40, y + h - 60, w - 80, 6, cls='abs pill', a='fade', d=d + 400, style='background:rgba(255,255,255,.3)')
        out += box(x + w - 40 - (w - 80) * .38, y + h - 60, (w - 80) * .38, 6, cls='abs pill', a='wipeR', d=d + 600, style=f'background:{C["lime"]}')
    else:
        out += ico(ic, x + w / 2 - 80, y + (h * .30 if lines else h / 2 - 80) - (0 if lines else 0), s=160, tile='rgba(255,255,255,.16)' if tone != 'lime' else 'w',
                   fg=fg if tone != 'lime' else C['forest'], du=C['lime'] if tone != 'lime' else C['brand'], a='pop', d=d + 300)
    yy = y + h * .58
    for k, (t, sz, wt) in enumerate(lines):
        col = fg if k == 0 else (C['lime'] if tone not in ('lime',) else C['forest'])
        out += textl(x + 40, yy, w - 80, e(t), cls=wt, a='rise', d=d + 500 + k * 120, align='center', style=f'font-size:{sz}px;line-height:1.35;color:{col}')
        yy += sz * 1.35 + 6
    return out


def post_head(xr, y, d):
    """Page avatar (the logo) + page name — the brand, as it would appear on a social post."""
    return (logo(1920 - xr - 72, y, 72, a='pop', d=d, name='') +
            text(xr + 90, y + 14, 400, 'أرض البساتين', cls='w8', a='fade', d=d + 60, style='font-size:28px;line-height:1.4'))


def flow(blocks, xr, y0, w, avail, base=0, d0=650, maxup=6):
    """Lays out post copy top-down; picks the largest type size (base +maxup .. -8 px) whose estimated height fits."""
    SPEC = {'hook': (36, 1.42, 'w8', 'var(--forest)'), 'p': (30, 1.55, 'w4', None), 'checks': (29, 1.55, 'w5', None),
            'sig': (30, 1.45, 'w8', 'var(--brown)'), 'label': (26, 1.3, 'w6', 'var(--leaf)')}

    def lay(delta):
        out, y = [], 0
        for blk in blocks:
            kind = blk[0]
            fs0, lh, wt, col = SPEC[kind]
            fs = fs0 + base + delta
            wcls = wt if not (kind == 'p' and len(blk) > 2) else blk[2]
            if kind == 'checks':
                cols = blk[2] if len(blk) > 2 else 2
                per = math.ceil(len(blk[1]) / cols)
                rows = [max(est_lines(blk[1][c * per + r], fs, w / cols - 20, 500) for c in range(cols) if c * per + r < len(blk[1])) for r in range(per)]
                h = sum(rows) * fs * lh
            else:
                h = est_lines(blk[1], fs, w, int(wcls[1]) * 100) * fs * lh
            out.append((blk, fs, lh, wcls, col, y, h))
            y += h + (22 if kind != 'label' else 6)
        return out, y - 22
    for delta in range(maxup, -9, -1):
        items, tot = lay(delta)
        if tot <= avail:
            break
    html_, d = '', d0
    for blk, fs, lh, wt, col, y, h in items:
        kind = blk[0]
        c = f'color:{col};' if col else ''
        if kind == 'checks':
            cols = blk[2] if len(blk) > 2 else 2
            per = math.ceil(len(blk[1]) / cols)
            for k, ln in enumerate(blk[1]):
                cc, r = k // per, k % per
                html_ += text(xr + cc * w / cols, y0 + y + r * fs * lh, w / cols - 20, e(ln), cls=wt, a='rise', d=d + k * 70, style=f'font-size:{fs}px;line-height:{lh}')
        else:
            html_ += text(xr, y0 + y, w, e(blk[1]), cls=wt, a='wipeR' if kind == 'hook' else 'rise', d=d, style=f'font-size:{fs}px;line-height:{lh};{c}')
        d += 140
    return html_


def post_slide(n, mode, head_pi, blocks, tone, ic, panel_lines=(), sec=None, k=1, video=False, intro=None):
    """Generic social-post example: title + a white post card (copy on the right, creative on the left)."""
    b = frame(n, mode, sec=sec)
    b += heading(T(head_pi), k=k)
    top = 300
    if intro:
        b += text(110, 300, 1700, e(T(intro)), cls='w3', a='rise', d=250, style='font-size:31px;line-height:1.55;color:var(--mut)')
        top = 410
    H = 990 - top
    b += box(110, top, 1700, H, cls='card shadow leafcard', a='rise', d=200, right=True)
    pw = 600
    b += panel(140, top + 30, pw, H - 60, tone, ic, panel_lines, d=400, video=video)
    xr, w = 160, 1700 - pw - 120
    b += post_head(xr, top + 40, 500)
    y0 = top + 128
    b += flow(blocks, xr, y0, w, top + H - 34 - y0)
    return slide(mode, b)


def s_ex1(n):
    return post_slide(n, 'L', 255, [('hook', T(256)), ('p', T(257)), ('p', T(258), 'w6'), ('sig', T(259))],
                      'forest', 'graduation-cap', sec=(None, T(254)))


def s_ex2(n):
    return post_slide(n, 'L', 261, [('hook', T(262)), ('p', T(263)), ('p', T(264), 'w6'), ('checks', L(265)), ('p', T(266), 'w7')],
                      'aqua', 'lightbulb', sec=(None, T(254)))


def s_ex3(n):
    l272 = L(272)
    return post_slide(n, 'L', 268, [('hook', T(269)), ('p', T(270)), ('p', T(271))],
                      'teal', 'eye', panel_lines=[(l272[0], 50, 'w9'), (l272[1], 30, 'w4')], sec=(None, T(254)))


def s_ex4(n):
    l277 = L(277)
    return post_slide(n, 'L', 274, [('hook', T(275)), ('checks', L(276)), ('p', l277[0]), ('p', l277[1]), ('sig', T(278))],
                      'lime', 'chat-circle-dots', sec=(None, T(254)))


def s_ex5(n):
    return post_slide(n, 'L', 280, [('hook', T(281)), ('p', T(282), 'w6'), ('checks', L(283)), ('p', T(284)), ('p', T(285)), ('sig', T(286))],
                      'earth', 'shopping-cart', sec=(None, T(254)))


def s_ex6(n):
    return post_slide(n, 'L', 288, [('hook', T(289)), ('p', T(290)), ('p', T(291), 'w6'), ('checks', L(292)), ('p', T(293)), ('p', T(294), 'w7')],
                      'teal', 'megaphone', panel_lines=[(T(295), 34, 'w8')], sec=(None, T(254)))


def s_ex7(n):
    l303 = L(303)
    return post_slide(n, 'L', 297, [('hook', T(298)), ('p', T(299)), ('p', T(300), 'w6'), ('checks', L(301)), ('p', T(302), 'w6')],
                      'forest', 'factory', panel_lines=[(l303[0], 44, 'w9'), (l303[1], 34, 'w3'), (l303[2], 30, 'w6')], sec=(None, T(254)), k=1)


def s_show1(n):
    b = frame(n, 'L', sec=(None, T(254)))
    b += heading(T(305), k=2)
    b += text(110, 345, 1700, e(T(306)), cls='w3', a='rise', d=250, style='font-size:31px;line-height:1.55;color:var(--mut)')
    b += show_card(460, (307, 308, 309, [310, 311, 312, 313]), 'storefront', 'forest')
    return slide('L', b)


def s_show2(n):
    b = frame(n, 'L', sec=(None, T(254)))
    b += heading(T(305), k=2)
    b += show_card(345, (314, 315, 316, [317, 318, 319]), 'factory', 'teal', tall=True)
    return slide('L', b)


def show_card(top, ids, ic, tone, tall=False):
    """Video storyboard: the scene description sits on the video frame, the proposed copy beside it."""
    hp, dp, lp, lines = ids
    H = 990 - top
    out = box(110, top, 1700, H, cls='card shadow leafcard', a='rise', d=300, right=True)
    pw = 560
    px, py, ph = 140, top + 30, H - 60
    out += panel(px, py, pw, ph, tone, ic, video=True, d=450)
    dt = T(dp)
    fs = 27
    while fs > 22 and est_lines(dt, fs, pw - 130) * fs * 1.5 > ph * .5 - 90:
        fs -= 1
    ty = py + ph * .52
    out += ico('video-camera', px + pw - 40 - 52, ty, s=52, tile='rgba(255,255,255,.18)', fg='#fff', du=C['lime'], shape='circle', a='pop', d=900)
    out += textl(px + 40, ty, pw - 150, e(dt), cls='w4', a='rise', d=950, style=f'font-size:{fs}px;line-height:1.5;color:#fff')
    xr, w = 160, 1700 - pw - 110
    y = top + 40
    out += text(xr, y, w, e(T(hp, colon=False)), cls='w8', a='wipeR', d=500, style='font-size:40px;line-height:1.4')
    y += 80
    out += box(xr, y, w, 2, cls='abs', a='wipeR', d=700, right=True, style=f'background:{C["line"]}')
    y += 26
    blocks = [('label', T(lp, colon=False)), ('hook', T(lines[0]))]
    blocks += [('p', T(li)) for li in lines[1:-1]]
    blocks += [('sig', T(lines[-1]))]
    out += flow(blocks, xr, y, w, top + H - 40 - y, d0=800, maxup=4)
    return out


def s_valueex(n):
    b = frame(n, 'L', sec=(None, T(254)))
    b += heading(T(321), k=2)
    b += text(110, 345, 1700, e(T(322)), cls='w3', a='rise', d=250, style='font-size:32px;line-height:1.55;color:var(--mut)')
    top = 430
    H = 990 - top
    b += box(110, top, 1700, H, cls='card shadow leafcard', a='rise', d=300, right=True)
    b += ico('lightbulb', 140 + 10, top + 40, s=120, tile='lime', a='pop', d=500)
    xr, w = 160, 1430
    y = top + 40
    b += text(xr, y, 300, e(T(323, colon=False)), cls='w6', a='fade', d=400, style='font-size:28px;line-height:1.3;color:var(--leaf)')
    b += text(xr, y + 46, w, e(T(324)), cls='w8', a='wipeR', d=500, style='font-size:40px;line-height:1.4;color:var(--forest)')
    b += text(xr, y + 122, w, e(T(325)), cls='w4', a='rise', d=650, style='font-size:31px;line-height:1.55')
    b += text(xr, y + 232, w, e(T(326)), cls='w6', a='rise', d=800, style='font-size:31px;line-height:1.55')
    steps = [s.strip() for s in T(327).rstrip('.').split('→')]
    sw_ = [270, 230, 260, 470]
    x = xr
    yy = y + 302
    for k, (s, ww) in enumerate(zip(steps, sw_)):
        d = 950 + k * 180
        b += chip(x, yy, s + ('.' if k == len(steps) - 1 else ''), C['forest'] if k < 3 else C['lime'], '#fff' if k < 3 else C['teal9'], fs=30, w=ww, h=70, d=d)
        if k < len(steps) - 1:
            b += dripline(1920 - x - ww - 52, yy + 35, 40, color=C['brand'], emit=C['brand'], step=20, sw=2, a='wipeR', d=d + 100)
        x += ww + 60
    b += text(xr, yy + 112, w, e(T(328)), cls='w8', a='rise', d=1700, style='font-size:32px;line-height:1.45;color:var(--brown)')
    return slide('L', b)


def s_adex(n):
    return post_slide(n, 'L', 330, [('hook', T(331)), ('p', T(332), 'w6'), ('checks', L(333)), ('p', T(334), 'w6'), ('p', T(335)), ('sig', T(336))],
                      'lime', 'megaphone-simple', sec=(None, T(254)), k=2)
