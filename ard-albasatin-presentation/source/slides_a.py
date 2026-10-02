# -*- coding: utf-8 -*-
"""Cover, contents, section dividers, sections 2-3."""
from core import *

SECTIONS = {2: 7, 3: 28, 4: 55, 5: 77, 6: 113, 7: 142, 8: 176, 9: 230}


def sec_title(k):
    """Section heading without its leading number: '2. دراسة المشروع' -> 'دراسة المشروع'."""
    return re.sub(r'^\s*\d+\.\s*', '', T(SECTIONS[k]))


def SEC(k):
    return (f'{k:02d}', sec_title(k))


# ------------------------------------------------------------------ cover
def s_cover(n):
    lab, name = L(1)[0].rstrip(':').strip(), L(1)[1]
    info = [L(2), L(3), L(4)]          # المتدرب / الدبلوم / الجهة المنفذة
    L(5)                                # «الشعار: أرض البساتين» -> the logo itself
    b = frame(n, 'D', pg=False, mark=False)
    b += dot(150, 190, 640, 'rgba(255,255,255,.05)', a='zoom', d=0, name='!!halo')
    ring = ''.join(f'<circle cx="{350 + 330 * math.cos(t / 48 * 2 * math.pi):.1f}" cy="{350 + 330 * math.sin(t / 48 * 2 * math.pi):.1f}" r="5" fill="#C3E36B" opacity="{.35 + .65 * (t % 4 == 0)}"/>' for t in range(48))
    b += snap(120, 160, 700, 700, f'<svg width="700" height="700"><circle cx="350" cy="350" r="330" fill="none" stroke="rgba(195,227,107,.35)" stroke-width="2"/>{ring}</svg>', a='spinIn', d=200, name='!!ring')
    b = b.replace('data-name="!!ring"', 'data-name="!!ring" data-a2="spinLoop"')
    b += logo(220, 260, 500, a='zoom', d=350)
    b += text(110, 112, 900, e(lab), cls='w5', a='wipeR', d=500, style='color:var(--lime);font-size:32px;line-height:1.3')
    a1, a2 = name.split(' ', 1)
    b += text(104, 228, 1000, e(a1), cls='w9', a='rise', d=650, style='font-size:250px;line-height:1.12;color:#fff', name='!!t1')
    b += text(104, 508, 1000, e(a2), cls='w1', a='wipeR', d=900, style='font-size:200px;line-height:1.1;color:var(--lime)', name='!!t2')
    xs, ws = [110, 680, 1250], [520, 520, 500]
    for k, (pair, x, w) in enumerate(zip(info, xs, ws)):
        l, v = pair[0].rstrip(':').strip(), pair[1]
        b += text(x, 850, w, e(l), cls='w4', a='rise', d=1200 + k * 140, style='font-size:28px;line-height:1.3;color:rgba(255,255,255,.62)')
        b += text(x, 892, w, e(v), cls='w7', a='rise', d=1260 + k * 140, style='font-size:38px;line-height:1.35;color:#fff')
        if k < 2:
            b += box(1920 - x - w - 40, 852, 2, 92, cls='abs', a='fade', d=1300, style='background:rgba(255,255,255,.22)')
    b += dripline(110, 1010, 1700, color='rgba(195,227,107,.45)', emit='#C3E36B', step=34, sw=2, a='wipeR', d=1500, name='!!drip')
    return slide('D', b, tr='morph-slow')


# ------------------------------------------------------------------ contents
def s_agenda(n):
    b = frame(n, 'L', sec=None)
    b += title('', 'المحتويات', a='wipeR')
    rows = [(f'{k:02d}', sec_title(k)) for k in range(2, 10)]
    rows += [('—', T(254)), ('—', T(340)), ('—', ORD.sub('', T(360)))]
    for c, items in enumerate([rows[:6], rows[6:]]):
        xr = 110 + c * 870
        b += dripline(1920 - xr - 22, 330, (len(items) - 1) * 108 + 20, vertical=True, color='#BFE0CC', emit=C['brand'], step=27, sw=2, a='wipeD', d=300 + c * 300)
        for r, (num, t) in enumerate(items):
            y = 318 + r * 108
            d = 450 + c * 500 + r * 90
            b += dot(1920 - xr - 22 - 15, y + 12, 30, C['lime'] if num != '—' else C['clay'], a='pop', d=d)
            b += text(xr + 50, y - 6, 110, num if num != '—' else '', cls='w2 num', a='rise', d=d, style=f'font-size:44px;line-height:1.2;color:{C["forest"]}')
            b += text(xr + 160 if num != '—' else xr + 60, y, 640, e(t), cls='w6', a='rise', d=d + 40, style='font-size:32px;line-height:1.35')
    return slide('L', b)


# ------------------------------------------------------------------ section divider
def s_divider(n, k, label=None, mode='D', sub=None):
    num = f'{k:02d}' if k else ''
    t = sec_title(k) if k else label
    b = frame(n, mode, pg=True, mark=False)
    b += leaves(70, 330, 470, rot=-8, v='g' if mode == 'D' else 'w', a=None)
    if num:
        b += text(100, 120, 900, num, cls='w1 num', a='zoomOut', d=200, style='font-size:400px;line-height:1;color:var(--lime);text-align:right', name='!!secnum')
    b += text(110, 600 if num else 420, 1060, e(t), cls='w8', a='wipeR', d=500, style='font-size:88px;line-height:1.3;color:#fff', name='!!sectitle')
    if sub:
        b += text(110, 560 if not num else 800, 1060, e(sub), cls='w2', a='rise', d=700, style='font-size:44px;line-height:1.4;color:var(--lime)')
    b += dripline(110, 960, 1060, color='rgba(195,227,107,.4)', emit='#C3E36B', step=34, sw=2, a='wipeR', d=800)
    return slide(mode, b, tr='morph-slow')


# ------------------------------------------------------------------ 2. idea / importance / goals
def s_idea(n):
    b = frame(n, 'L', sec=SEC(2))
    b += heading(T(8))
    t = e(T(9)).replace('مشروع أرض البساتين', '<b class="w8" style="color:var(--forest)">مشروع أرض البساتين</b>', 1)
    b += text(110, 330, 1000, t, cls='lead', a='rise', d=350, style='font-size:42px;line-height:1.7;font-weight:300')
    # illustration: the audiences named in the paragraph orbit the brand leaves
    cx, cy, R = 470, 640, 300
    b += dot(cx - 250, cy - 250, 500, C['mint'], a='zoom', d=250)
    b += snap(cx - R - 8, cy - R - 8, 2 * R + 16, 2 * R + 16,
              f'<svg width="{2 * R + 16}" height="{2 * R + 16}"><circle cx="{R + 8}" cy="{R + 8}" r="{R}" fill="none" stroke="#BFE0CC" stroke-width="3" stroke-dasharray="2 14" stroke-linecap="round"/></svg>', a='spinIn', d=300)
    b += leaves(cx - 200, cy - 135, 230, rot=-4, v='g', names=('', ''), a='grow', d=500)
    icons = ['farm', 'tractor', 'storefront', 'truck', 'buildings']
    for k, ic in enumerate(icons):
        ang = math.radians(-90 + k * 72)
        x, y = cx + R * math.cos(ang) - 56, cy + R * math.sin(ang) - 56
        b += ico(ic, x, y, s=112, tile='lime' if k % 2 == 0 else 'w', a='pop', d=800 + k * 120)
    return slide('L', b)


def s_idea2(n):
    b = frame(n, 'L', sec=SEC(2))
    b += heading(T(8))
    b += text(110, 300, 1700, e(T(10).replace('الزراعية،وغيرها', 'الزراعية، وغيرها')), cls='body', a='rise', d=300, style='font-size:36px;line-height:1.65')
    prods = [('shield-check', 'منتجات الحماية الزراعية'), ('drop', 'مستلزمات الري بالتقطير'), ('pipe', 'الأنابيب الرئيسية'),
             ('drop-half', 'أنابيب التقطير'), ('umbrella', 'الأغطية الزراعية')]
    for k, (ic, lab) in enumerate(prods):
        xr = 110 + k * 346
        b += box(xr, 495, 326, 230, cls='card mint2 leafcard', a='rise', d=450 + k * 110, right=True)
        b += ico(ic, 1920 - xr - 326 + 200, 520, s=96, tile='w', a='pop', d=600 + k * 110)
        b += text(xr + 34, 632, 260, e(lab), cls='w6', a='rise', d=650 + k * 110, style='font-size:29px;line-height:1.35')
    b += box(110, 765, 1700, 220, cls='card teal leafcard', a='rise', d=1100, right=True)
    b += ico('factory', 1920 - 110 - 170, 817, s=116, tile='lime', a='pop', d=1300)
    t = e(T(11)).replace('مصنع دريب أكوا', '<b class="w8" style="color:var(--lime)">مصنع دريب أكوا</b>')
    b += text(290, 805, 1340, t, cls='body', a='wipeR', d=1250, style='color:#fff;font-size:33px;line-height:1.6')
    return slide('L', b)


def s_importance(n):
    b = frame(n, 'D', sec=SEC(2))
    b += heading(T(12))
    b += text(110, 320, 1040, e(T(13)), cls='lead', a='rise', d=300, style='font-size:44px;line-height:1.62;font-weight:300;color:#fff')
    b += box(110, 700, 1040, 285, cls='card glass leafcard', a='rise', d=600, right=True)
    b += text(160, 735, 940, e(T(14)), cls='body', a='rise', d=700, style='font-size:31px;line-height:1.6;color:rgba(255,255,255,.9)')
    steps = ['megaphone', 'list-magnifying-glass', 'target', 'seal-check', 'shopping-cart']
    for k, ic in enumerate(steps):
        y = 300 + k * 140
        last = k == len(steps) - 1
        b += ico(ic, 330, y, s=110, tile='lime' if last else 'rgba(255,255,255,.1)', fg=None if last else '#fff', du=None if last else C['lime'], a='pop', d=900 + k * 140)
        if not last:
            b += snap(380, y + 112, 10, 26, '<svg width="10" height="26"><circle cx="5" cy="5" r="4" fill="#C3E36B"/><circle cx="5" cy="20" r="3" fill="#C3E36B" opacity=".5"/></svg>', a='fade', d=980 + k * 140)
    return slide('D', b)


def s_goals(n):
    b = frame(n, 'L', sec=SEC(2))
    b += heading(T(15))
    items = [T(i) for i in range(16, 27)]
    b += numlist(items, 110, 296, 1700, 114, fs=30, bold=(0, 6), cols=2, colgap=80, d0=300, step=70)
    return slide('L', b)


# ------------------------------------------------------------------ 3. project info
def s_info(n):
    b = frame(n, 'L', sec=SEC(3))
    # name card (left)
    b += box(110, 140, 600, 840, cls='card teal leafcard', a='rise', d=200)
    b += logo(255, 220, 310, a='zoom', d=450, name='!!logo')
    b += text(1920 - 110 - 600 + 60, 590, 480, e(T(29, colon=False)), cls='w5', a='rise', d=600, align='center', style='font-size:30px;line-height:1.3;color:var(--lime)')
    b += text(1920 - 110 - 600 + 20, 640, 560, e(T(30)), cls='w9', a='zoomOut', d=700, align='center', style='font-size:62px;line-height:1.3;color:#fff;white-space:nowrap')
    b += dripline(180, 800, 460, color='rgba(195,227,107,.5)', emit='#C3E36B', step=30, sw=2, a='wipeR', d=900)
    b += ico('storefront', 365, 840, s=96, tile='lime', a='pop', d=1000)
    # activity (right)
    b += text(110, 150, 1010, e(T(31, colon=False)), cls='w6', a='fade', d=300, style='font-size:30px;line-height:1.3;color:var(--leaf)')
    b += text(110, 200, 1010, e(T(32)), cls='w3', a='rise', d=400, style='font-size:42px;line-height:1.66;color:var(--ink)')
    b += box(110, 670, 1010, 310, cls='card mint leafcard', a='rise', d=700, right=True)
    b += ico('factory', 1920 - 110 - 150, 715, s=100, tile='w', a='pop', d=900)
    t = e(T(33)).replace('مصنع دريب أكوا', '<b class="w8" style="color:var(--forest)">مصنع دريب أكوا</b>')
    b += text(270, 712, 810, t, cls='body', a='rise', d=850, style='font-size:33px;line-height:1.62')
    return slide('L', b)


def s_audience(n):
    b = frame(n, 'L', sec=SEC(3))
    b += heading(T(34))
    items = [T(i) for i in range(35, 43)]
    icons = ['plant', 'briefcase', 'storefront', 'pipe-wrench', 'wrench', 'buildings', 'users-three', 'mountains']
    cw, ch, gx, gy = 410, 315, 20, 24
    for k, (it, ic) in enumerate(zip(items, icons)):
        c, r = k % 4, k // 4
        xr = 110 + c * (cw + gx)
        y = 310 + r * (ch + gy)
        d = 300 + k * 90
        tone = 'mint2' if (c + r) % 2 == 0 else 'mint'
        b += box(xr, y, cw, ch, cls=f'card {tone} leafcard', a='rise', d=d, right=True)
        b += ico(ic, 1920 - xr - 40 - 100, y + 36, s=100, tile='w' if tone == 'mint' else 'lime', a='pop', d=d + 150)
        b += text(xr + 40, y + 160, cw - 80, e(it), cls='w6', a='rise', d=d + 120, style='font-size:29px;line-height:1.42')
    return slide('L', b)


PLATFORM_ICON = {'فيسبوك': 'facebook-logo', 'واتساب': 'whatsapp-logo', 'تيك توك': 'tiktok-logo', 'إنستغرام': 'instagram-logo', 'Google Maps': 'map-pin-area'}


def s_platforms(n):
    b = frame(n, 'D', sec=SEC(3))
    b += heading(T(43), k=2)
    pairs = [(T(i, colon=False), T(i + 1)) for i in range(44, 53, 2)]
    cw, gx = 326, 17
    for k, (nm, desc) in enumerate(pairs):
        xr = 110 + k * (cw + gx)
        y = 320
        d = 300 + k * 140
        b += box(xr, y, cw, 600, cls='card glass leafcard', a='rise', d=d, right=True)
        b += ico(PLATFORM_ICON[nm], 1920 - xr - cw + 32, y + 40, s=110, tile='lime', a='pop', d=d + 200)
        latin = nm.isascii()
        b += text(xr + 34, y + 190, cw - 60, e(nm), cls='w8' + (' lat' if latin else ''), a='rise', d=d + 150,
                  style='font-size:38px;line-height:1.3;color:#fff;' + ('text-align:right;' if latin else ''))
        b += text(xr + 34, y + 260, cw - 60, e(desc), cls='w3', a='rise', d=d + 220, style='font-size:29px;line-height:1.58;color:rgba(255,255,255,.9)')
    return slide('D', b)
