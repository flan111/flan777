# -*- coding: utf-8 -*-
"""PAS ad, buyer persona, closing."""
from slides_d import *

PAS_SEC = (None, 'PAS')


def s_pas(n):
    T(338); T(339)      # "PAS" + the stray "المشكلة:" label (its content is the P slide)
    b = frame(n, 'G', pg=True, mark=False)
    b += leaves(70, 360, 420, rot=-8, v='w', a=None)
    letters = [('P', 341), ('A', 344), ('S', 353)]
    for k, (ch, pi) in enumerate(letters):
        x = 1810 - 330 - (2 - k) * 300
        b += textl(x, 110, 330, ch, cls='w9 lat', a='zoomOut', d=200 + k * 200, align='center', style=f'font-size:330px;line-height:1.1;color:{"#fff" if k != 1 else C["lime"]}')
        en = T(pi).split()[-1]
        b += textl(x, 470, 330, en, cls='w3 lat', a='rise', d=500 + k * 200, align='center', style='font-size:34px;line-height:1.3;color:rgba(255,255,255,.85)')
    b += text(110, 620, 1100, e(T(340)), cls='w8', a='wipeR', d=900, style='font-size:84px;line-height:1.3;color:#fff', name='!!sectitle')
    b += dripline(110, 960, 1060, color='rgba(195,227,107,.5)', emit='#C3E36B', step=34, sw=2, a='wipeR', d=1100)
    return slide('G', b, tr='morph-slow')


def pas_title(pi, ink, d=150):
    h = T(pi)
    m = re.match(r'^([PAS])\s*—\s*(.*?)\s+([A-Za-z]+)$', h)
    letter, ar, en = m.groups()
    return text(110, 132, 1300, f'<span class="w2 lat" style="color:{ink}">{letter}</span> <span class="w2" style="color:{ink}">—</span> {e(ar)} <span class="w2 lat" style="font-size:48px;color:{ink}">{e(en)}</span>',
                cls='w8', a='wipeR', d=d, style='font-size:80px;line-height:1.28;white-space:nowrap')


def s_pas_p(n):
    b = frame(n, 'E', sec=PAS_SEC)
    b += pas_title(341, C['brown'])
    b += textl(70, 170, 640, 'P', cls='w1 lat', a='zoomOut', d=300, align='center', style=f'font-size:760px;line-height:1;color:{C["clay"]};opacity:.45')
    b += ico('pipe', 300, 560, s=200, tile='w', fg=C['brown'], du=C['clay'], a='pop', d=700)
    b += snap(560, 760, 46, 60, drop_svg(C['aqua'], 46), a='drop', d=1200)
    b += text(110, 330, 1080, e(T(342)), cls='w8', a='rise', d=400, style='font-size:52px;line-height:1.5;color:var(--soil)')
    b += box(110, 640, 1080, 2, cls='abs', a='wipeR', d=700, right=True, style='background:#E0CFB8')
    b += text(110, 680, 1080, e(T(343)), cls='w4', a='rise', d=800, style='font-size:36px;line-height:1.62;color:var(--soil)')
    return slide('E', b)


def s_pas_a(n):
    b = frame(n, 'E', sec=PAS_SEC)
    b += pas_title(344, C['brown'])
    b += text(110, 290, 1700, e(T(345)), cls='w4', a='rise', d=300, style='font-size:34px;line-height:1.55;color:var(--soil)')
    items = [T(i) for i in range(346, 352)]
    icons = ['lightning', 'drop-slash', 'repeat', 'coins', 'chart-line-down', 'hourglass-medium']
    cw, ch, gx, gy = 553, 170, 20, 20
    for k, (it, ic) in enumerate(zip(items, icons)):
        c, r = k % 3, k // 3
        xr = 110 + c * (cw + gx)
        y = 380 + r * (ch + gy)
        d = 450 + k * 120
        b += box(xr, y, cw, ch, cls='card leafcard', a='rise', d=d, right=True, style='background:#fff')
        b += ico(ic, 1920 - xr - 30 - 100, y + 35, s=100, tile='sand2', fg=C['brown'], du=C['clay'], a='pop', d=d + 120)
        b += text(xr + 160, y + 20, cw - 190, e(it), cls='w6', a='rise', d=d + 80, style='font-size:31px;line-height:1.42;height:130px;display:flex;align-items:center;color:var(--soil)')
    b += box(110, 780, 1700, 200, cls='card brown leafcard', a='rise', d=1300, right=True)
    b += ico('warning', 1920 - 110 - 50 - 110, 825, s=110, tile='w', fg=C['brown'], du=C['clay'], a='pop', d=1500)
    b += text(330, 840, 1420, e(T(352)), cls='w7', a='wipeR', d=1450, style='font-size:38px;line-height:1.5;color:#fff')
    return slide('E', b)


def s_pas_s(n):
    b = frame(n, 'G', sec=PAS_SEC)
    b += pas_title(353, C['lime'])
    b = b.replace('class="abs ttl"', 'class="abs ttl"')
    b += text(110, 300, 1150, e(T(354)), cls='w8', a='rise', d=300, style='font-size:46px;line-height:1.5;color:#fff')
    b += text(110, 455, 1150, e(T(355)), cls='w3', a='rise', d=500, style='font-size:31px;line-height:1.62;color:rgba(255,255,255,.92)')
    l356 = L(356)
    b += box(110, 760, 1150, 220, cls='card lime leafcard', a='rise', d=900, right=True)
    b += ico('factory', 1920 - 110 - 40 - 120, 810, s=120, tile='w', a='pop', d=1100)
    b += text(330, 800, 880, e(l356[0]), cls='w9', a='rise', d=1050, style=f'font-size:44px;line-height:1.35;color:{C["teal9"]}')
    b += text(330, 866, 880, e(l356[1]), cls='w3', a='wipeR', d=1200, style=f'font-size:44px;line-height:1.4;color:{C["forest"]}')
    # right column (left side): slogan + CTA
    b += leaves(150, 300, 200, rot=-6, v='w', names=('', ''), a='grow', d=700)
    b += textl(110, 560, 520, e(T(357)), cls='w7', a='rise', d=1300, style='font-size:31px;line-height:1.5;color:#fff')
    b += textl(110, 720, 520, e(T(358)), cls='w4', a='rise', d=1500, style='font-size:28px;line-height:1.55;color:rgba(255,255,255,.9)')
    return slide('G', b)


# ------------------------------------------------------------------ persona
def s_persona1(n):
    b = frame(n, 'L', sec=(None, ORD.sub('', T(360))))
    b += heading(T(360), k=2, size=76)
    # profile card
    b += box(110, 330, 720, 650, cls='card teal leafcard', a='rise', d=300)
    b += ico('user', 150, 370, s=150, tile='lime', shape='circle', a='pop', d=500)
    b += textl(330, 380, 460, e(T(361, colon=False)), cls='w5', a='fade', d=600, style='font-size:26px;line-height:1.3;color:var(--lime)')
    b += textl(330, 420, 460, e(T(362)), cls='w9', a='wipeR', d=650, style='font-size:68px;line-height:1.3;color:#fff')
    rows = [(363, 364), (365, 366), (367, 368)]
    y = 560
    for k, (lp, vp) in enumerate(rows):
        d = 800 + k * 140
        b += textl(150, y, 640, e(T(lp, colon=False)), cls='w6', a='rise', d=d, style='font-size:25px;line-height:1.3;color:var(--lime)')
        v = T(vp)
        b += textl(150, y + 36, 640, e(v), cls='w4' if k else 'w8', a='rise', d=d + 50, style=f'font-size:{27 if k else 34}px;line-height:1.5;color:#fff')
        y += 36 + (52 if k == 0 else 44 * math.ceil(len(v) / 44)) + 22
    # needs
    b += text(110, 335, 900, e(T(369, colon=False)), cls='w8', a='wipeR', d=500, style='font-size:40px;line-height:1.3')
    items = [T(i) for i in range(370, 379)]
    b += ilist(items, 110, 410, 920, None, fs=30, d0=700, step=80, gap=20, maxh=570)
    return slide('L', b)


def s_persona2(n):
    b = frame(n, 'L', sec=(None, ORD.sub('', T(360))))
    b += heading(T(360), k=2, size=76)
    b += text(110, 300, 1700, e(T(379, colon=False)), cls='w7', a='fade', d=300, style='font-size:32px;line-height:1.3;color:var(--leaf)')
    steps = [s.strip().rstrip('.') for s in T(380).split('→')]
    w_ = 310
    for k, s in enumerate(steps):
        xr = 110 + k * (w_ + 37)
        d = 400 + k * 150
        last = k == len(steps) - 1
        b += chip(xr, 360, s + ('.' if last else ''), C['forest'] if k == 0 else (C['lime'] if last else C['mint']),
                  '#fff' if k == 0 else (C['teal9'] if last else C['forest']), fs=30, w=w_, h=74, d=d, weight='w7')
        if not last:
            b += dripline(1920 - xr - w_ - 34, 397, 30, color=C['brand'], emit=C['brand'], step=15, sw=2, a='wipeR', d=d + 80)
    # problem it solves
    b += box(110, 480, 840, 500, cls='card sand leafcard', a='rise', d=1000, right=True)
    b += text(150, 515, 760, e(T(381, colon=False)), cls='w8', a='wipeR', d=1100, style='font-size:31px;line-height:1.4;color:var(--brown)')
    b += text(150, 580, 760, e(T(382)), cls='w5', a='rise', d=1200, style='font-size:29px;line-height:1.55;color:var(--soil)')
    b += box(150, 735, 760, 2, cls='abs', a='wipeR', d=1250, right=True, style='background:#E3D3BD')
    b += text(150, 755, 760, e(T(383)), cls='w4', a='rise', d=1300, style='font-size:28px;line-height:1.55;color:var(--soil)')
    # message
    b += box(110, 480, 820, 500, cls='card teal leafcard', a='rise', d=1400)
    b += textl(150, 515, 740, e(T(384, colon=False)), cls='w6', a='fade', d=1500, style='font-size:28px;line-height:1.4;color:var(--lime)')
    b += textl(150, 575, 740, e(T(385)), cls='w7', a='wipeR', d=1600, style='font-size:42px;line-height:1.5;color:#fff')
    b += textl(150, 880, 740, e(T(386)), cls='w3', a='rise', d=1900, style='font-size:34px;line-height:1.3;color:var(--lime)')
    b += leaves(150, 875, 64, v='g', names=('', ''), a='grow', d=2000)
    return slide('L', b)


def s_close(n):
    b = frame(n, 'D', pg=False, mark=False)
    b += dot(150, 190, 640, 'rgba(255,255,255,.05)', a='zoom', d=0, name='!!halo')
    ring = ''.join(f'<circle cx="{350 + 330 * math.cos(t / 48 * 2 * math.pi):.1f}" cy="{350 + 330 * math.sin(t / 48 * 2 * math.pi):.1f}" r="5" fill="#C3E36B" opacity="{.35 + .65 * (t % 4 == 0)}"/>' for t in range(48))
    b += snap(120, 160, 700, 700, f'<svg width="700" height="700"><circle cx="350" cy="350" r="330" fill="none" stroke="rgba(195,227,107,.35)" stroke-width="2"/>{ring}</svg>', a=None, name='!!ring')
    b = b.replace('data-name="!!ring"', 'data-name="!!ring" data-a2="spinLoop"')
    b += logo(220, 260, 500, a=None)
    t = T(249)
    nm, rest = t.split('—', 1)
    a1, a2 = nm.strip().split(' ', 1)
    b += text(104, 205, 1000, e(a1), cls='w9', a=None, style='font-size:250px;line-height:1.12;color:#fff', name='!!t1')
    b += text(104, 488, 1000, e(a2), cls='w1', a=None, style='font-size:200px;line-height:1.1;color:var(--lime)', name='!!t2')
    b += text(110, 790, 1000, '— ' + e(rest.strip()), cls='w3', a='wipeR', d=900, style='font-size:46px;line-height:1.4;color:#fff')
    b += dripline(110, 1010, 1700, color='rgba(195,227,107,.45)', emit='#C3E36B', step=34, sw=2, a=None, name='!!drip')
    return slide('D', b, tr='morph-slow')
