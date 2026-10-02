# -*- coding: utf-8 -*-
"""Post-process the pptxgenjs output:
   * one <a:pPr> per paragraph (pptxgenjs repeats it per run) + RTL flags, complex-script fonts
   * preset geometry adjustments (leaf cards, water-drop tiles)
   * Morph transitions (fade fallback) and a choreographed, auto-playing animation timeline per slide
   * Arabic theme fonts, duplicate media merged
"""
import hashlib, json, os, re, shutil, sys, zipfile
from lxml import etree

SRC, DST, OUTDIR = sys.argv[1], sys.argv[2], sys.argv[3]
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
A = '{%s}' % NS['a']
PNS = '{%s}' % NS['p']

work = DST + '.dir'
shutil.rmtree(work, ignore_errors=True)
with zipfile.ZipFile(SRC) as z:
    z.extractall(work)
anims = {i + 1: a for i, a in enumerate(json.load(open(os.path.join(OUTDIR, 'anims.json'))))}
geo = {i + 1: g for i, g in enumerate(json.load(open(os.path.join(OUTDIR, 'geo.json'))))}

DUR = {'fade': 700, 'rise': 800, 'wipeR': 900, 'wipeL': 900, 'wipeU': 900, 'wipeD': 1100, 'zoom': 900, 'zoomOut': 1000,
       'pop': 650, 'spinIn': 1400, 'wheel': 1400, 'drop': 900, 'grow': 1200, 'swayL': 3200, 'swayR': 3600, 'spinLoop': 60000,
       'float': 3000}


class Ids:
    def __init__(self): self.n = 2

    def __call__(self):
        self.n += 1
        return self.n


def tgt(spid):
    return f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'


def setvis(nid, spid):
    return (f'<p:set><p:cBhvr><p:cTn id="{nid()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>{tgt(spid)}'
            f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>')


def fx(nid, spid, flt, dur, delay=0):
    st = f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst>' if delay else ''
    return f'<p:animEffect transition="in" filter="{flt}"><p:cBhvr><p:cTn id="{nid()}" dur="{dur}">{st}</p:cTn>{tgt(spid)}</p:cBhvr></p:animEffect>'


def prop(nid, spid, attr, keys, dur, decel=100000, num=False, accel=0):
    tav = ''.join(f'<p:tav tm="{tm}"><p:val>' + (f'<p:fltVal val="{v}"/>' if num else f'<p:strVal val="{v}"/>') + '</p:val></p:tav>' for tm, v in keys)
    dc = (f' decel="{decel}"' if decel else '') + (f' accel="{accel}"' if accel else '')
    return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{nid()}" dur="{dur}" fill="hold"{dc}/>{tgt(spid)}'
            f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst>{tav}</p:tavLst></p:anim>')


def scale(nid, spid, keys, dur, decel=100000):
    kw = [(tm, f'#ppt_w*{f}' if f != 1 else '#ppt_w') for tm, f in keys]
    kh = [(tm, f'#ppt_h*{f}' if f != 1 else '#ppt_h') for tm, f in keys]
    return prop(nid, spid, 'ppt_w', kw, dur, decel) + prop(nid, spid, 'ppt_h', kh, dur, decel)


def rot_loop(nid, spid, by, dur):
    return (f'<p:animRot by="{by}"><p:cBhvr><p:cTn id="{nid()}" dur="{dur}" fill="hold" accel="50000" decel="50000" autoRev="1"/>{tgt(spid)}'
            f'<p:attrNameLst><p:attrName>r</p:attrName></p:attrNameLst></p:cBhvr></p:animRot>')


def effect(nid, spid, kind, dur):
    """returns (presetID, presetClass, subtype, behaviours, extra cTn attrs)"""
    if kind == 'fade':
        return 10, 'entr', 0, setvis(nid, spid) + fx(nid, spid, 'fade', dur), ''
    if kind == 'rise':          # soft float-in: fade + rise with a long ease-out
        return 42, 'entr', 0, (setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .75)) +
                               prop(nid, spid, 'ppt_x', [(0, '#ppt_x'), (100000, '#ppt_x')], dur) +
                               prop(nid, spid, 'ppt_y', [(0, '#ppt_y+.03'), (100000, '#ppt_y')], dur)), ''
    if kind == 'wipeR':         # reveal in Arabic reading direction (right -> left) with a soft fade
        return 22, 'entr', 2, setvis(nid, spid) + fx(nid, spid, 'wipe(right)', dur) + fx(nid, spid, 'fade', int(dur * .7)), ''
    if kind == 'wipeL':
        return 22, 'entr', 8, setvis(nid, spid) + fx(nid, spid, 'wipe(left)', dur) + fx(nid, spid, 'fade', int(dur * .7)), ''
    if kind == 'wipeU':         # sprouts upward out of the soil
        return 22, 'entr', 4, setvis(nid, spid) + fx(nid, spid, 'wipe(down)', dur) + fx(nid, spid, 'fade', int(dur * .5)), ''
    if kind == 'wipeD':         # water running down the drip line
        return 22, 'entr', 1, setvis(nid, spid) + fx(nid, spid, 'wipe(up)', dur), ''
    if kind == 'zoom':          # focus pull: 85% -> 100% + fade
        return 53, 'entr', 16, setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .7)) + scale(nid, spid, [(0, .85), (100000, 1)], dur), ''
    if kind == 'zoomOut':       # lands from 125%
        return 53, 'entr', 32, setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .6)) + scale(nid, spid, [(0, 1.25), (100000, 1)], dur), ''
    if kind == 'pop':           # elastic pop with a small overshoot
        return 53, 'entr', 16, setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .45)) + scale(nid, spid, [(0, .3), (62000, 1.08), (100000, 1)], dur, 0), ''
    if kind == 'drop':          # a water drop falls and settles with a tiny bounce
        return 2, 'entr', 1, (setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .3)) +
                              prop(nid, spid, 'ppt_x', [(0, '#ppt_x'), (100000, '#ppt_x')], dur, 0) +
                              prop(nid, spid, 'ppt_y', [(0, '#ppt_y-.12'), (62000, '#ppt_y+.006'), (82000, '#ppt_y-.004'), (100000, '#ppt_y')], dur, 0)), ''
    if kind == 'grow':          # a seedling: grows from 20% while turning upright
        return 31, 'entr', 0, (setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .4)) + scale(nid, spid, [(0, .2), (100000, 1)], dur) +
                               prop(nid, spid, 'style.rotation', [(0, -25), (100000, 0)], dur, 100000, True)), ''
    if kind == 'spinIn':        # an irrigation ring that turns into place
        return 31, 'entr', 0, (setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .5)) + scale(nid, spid, [(0, .7), (100000, 1)], dur) +
                               prop(nid, spid, 'style.rotation', [(0, -90), (100000, 0)], dur, 100000, True)), ''
    if kind == 'wheel':
        return 21, 'entr', 1, setvis(nid, spid) + fx(nid, spid, 'wheel(1)', dur), ''
    if kind in ('swayL', 'swayR'):   # leaves moving in a breeze (endless, very slow)
        by = 150000 if kind == 'swayL' else -120000
        return 8, 'emph', 0, rot_loop(nid, spid, by, dur // 2), ' repeatCount="indefinite"'
    if kind == 'spinLoop':
        return 8, 'emph', 0, (f'<p:animRot by="21600000"><p:cBhvr><p:cTn id="{nid()}" dur="{dur}" fill="hold"/>{tgt(spid)}'
                              f'<p:attrNameLst><p:attrName>r</p:attrName></p:attrNameLst></p:cBhvr></p:animRot>'), ' repeatCount="indefinite"'
    if kind == 'float':
        return 42, 'emph', 0, (f'<p:animMotion origin="layout" path="M 0 0 L 0 -0.012 E" pathEditMode="relative" ptsTypes="">'
                               f'<p:cBhvr><p:cTn id="{nid()}" dur="{dur // 2}" fill="hold" accel="50000" decel="50000" autoRev="1"/>{tgt(spid)}'
                               f'<p:attrNameLst><p:attrName>ppt_x</p:attrName><p:attrName>ppt_y</p:attrName></p:attrNameLst></p:cBhvr></p:animMotion>'), ' repeatCount="indefinite"'
    raise ValueError(kind)


def timing_xml(items, ids, kinds_of):
    nid = Ids()
    pars, bld, seen = [], [], set()
    for it in sorted(items, key=lambda x: x['d']):
        spid = ids.get(it['name'])
        if not spid:
            continue
        kind = it['a']
        dur = it.get('t') or DUR[kind]
        pid, pcls, sub, beh, extra = effect(nid, spid, kind, dur)
        delay = int(it['d'])
        if it.get('loop'):
            delay = max(delay, 2200)
        pars.append(f'<p:par><p:cTn id="{nid()}" presetID="{pid}" presetClass="{pcls}" presetSubtype="{sub}"{extra} fill="hold" grpId="{1 if pcls == "emph" else 0}" nodeType="withEffect">'
                    f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>{beh}</p:childTnLst></p:cTn></p:par>')
        g = 1 if pcls == 'emph' else 0
        if (spid, g) in seen:
            continue
        seen.add((spid, g))
        k = kinds_of.get(spid)
        if k == 'sp':
            bld.append(f'<p:bldP spid="{spid}" grpId="{g}" animBg="1"/>')
        elif k == 'txsp':
            bld.append(f'<p:bldP spid="{spid}" grpId="{g}"/>')
        elif k == 'graphicFrame':
            bld.append(f'<p:bldGraphic spid="{spid}" grpId="{g}"><p:bldAsOne/></p:bldGraphic>')
    if not pars:
        return ''
    body = ''.join(pars)
    xml = ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
           '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
           '<p:par><p:cTn id="__A__" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
           '<p:par><p:cTn id="__B__" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
           + body +
           '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
           '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
           '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
           '</p:childTnLst></p:cTn></p:par></p:tnLst>'
           + (f'<p:bldLst>{"".join(bld)}</p:bldLst>' if bld else '') + '</p:timing>')
    xml = xml.replace('__A__', str(nid())).replace('__B__', str(nid()))
    cnt = [0]

    def rn(m):
        cnt[0] += 1
        return f'<p:cTn id="{cnt[0]}"'
    return re.sub(r'<p:cTn id="\d+"', rn, xml)


def transition_xml(kind, dur):
    if kind == 'fade':
        return f'<p:transition spd="slow" p14:dur="{dur}"><p:fade/></p:transition>'
    return ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
            '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
            f'<p:transition spd="slow" p14:dur="{dur}"><p159:morph option="byObject"/></p:transition></mc:Choice>'
            f'<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')


sl_dir = os.path.join(work, 'ppt', 'slides')
files = sorted([f for f in os.listdir(sl_dir) if re.match(r'slide\d+\.xml$', f)], key=lambda f: int(re.findall(r'\d+', f)[0]))
for f in files:
    n = int(re.findall(r'\d+', f)[0])
    fp = os.path.join(sl_dir, f)
    tree = etree.parse(fp)
    root = tree.getroot()
    # --- paragraphs: single pPr first, RTL
    for p in root.iter(A + 'p'):
        pprs = p.findall(A + 'pPr')
        for extra in pprs[1:]:
            p.remove(extra)
        if pprs:
            first = pprs[0]
            if p.index(first) != 0:
                p.remove(first)
                p.insert(0, first)
            langs = [r.get('lang') for r in p.iter(A + 'rPr')]
            if langs and langs[0] == 'ar-SA':
                first.set('rtl', '1')
    # --- fonts: latin + cs carry the weight's family; no east-asian override
    for rpr in root.iter(A + 'rPr'):
        lat = rpr.find(A + 'latin')
        for tag in ('latin', 'ea', 'cs', 'sym'):
            for el in rpr.findall(A + tag):
                for at in ('pitchFamily', 'charset'):
                    if at in el.attrib:
                        del el.attrib[at]
        for el in rpr.findall(A + 'ea'):
            rpr.remove(el)
        if lat is not None and rpr.find(A + 'cs') is None:
            cs = etree.SubElement(rpr, A + 'cs')
            cs.set('typeface', lat.get('typeface'))
            # schema order: latin, ea, cs, sym, hlinkClick...
            rpr.remove(cs)
            rpr.insert(list(rpr).index(lat) + 1, cs)
    # --- ids / kinds / geometry adjustments
    ids, kinds = {}, {}
    shp_geo = geo.get(n, {}).get('shapes', {})
    for el in root.iter(PNS + 'cNvPr'):
        nm, i = el.get('name'), el.get('id')
        ids[nm] = i
        holder = el.getparent().getparent()
        tag = etree.QName(holder).localname
        if tag == 'sp':
            kinds[i] = 'txsp' if holder.find('.//' + A + 't') is not None else 'sp'
            if nm in shp_geo:
                g = shp_geo[nm]
                pg = holder.find('.//' + A + 'prstGeom')
                if pg is not None:
                    pg.set('prst', g['prst'])
                    av = pg.find(A + 'avLst')
                    if av is None:
                        av = etree.SubElement(pg, A + 'avLst')
                    for c in list(av):
                        av.remove(c)
                    for k, v in g['adj'].items():
                        gd = etree.SubElement(av, A + 'gd')
                        gd.set('name', k)
                        gd.set('fmla', f'val {v}')
        else:
            kinds[i] = tag
    xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True).decode('utf8')
    if 'xmlns:p14=' not in xml:
        xml = xml.replace('<p:sld ', '<p:sld xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" ', 1)
    an = anims.get(n, {'tr': 'morph', 'items': []})
    tr = transition_xml(an['tr'], {'fade': 1000, 'morph-slow': 1800}.get(an['tr'], 1150))
    tm = timing_xml(an['items'], ids, kinds)
    xml = re.sub(r'<p:transition.*?</p:transition>|<p:timing>.*?</p:timing>', '', xml, flags=re.S)
    if '</p:clrMapOvr>' in xml:
        xml = xml.replace('</p:clrMapOvr>', '</p:clrMapOvr>' + tr + tm, 1)
    else:
        xml = xml.replace('</p:cSld>', '</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>' + tr + tm, 1)
    open(fp, 'w', encoding='utf8').write(xml)

# --- theme fonts (new text typed in PowerPoint uses the brand font)
th = os.path.join(work, 'ppt', 'theme', 'theme1.xml')
if os.path.exists(th):
    t = open(th, encoding='utf8').read()
    for tag, face in (('majorFont', 'Alexandria ExtraBold'), ('minorFont', 'Alexandria')):
        t = re.sub(rf'(<a:{tag}>)<a:latin typeface="[^"]*"( panose="[^"]*")?/><a:ea typeface="[^"]*"/><a:cs typeface="[^"]*"/>',
                   rf'\1<a:latin typeface="{face}"/><a:ea typeface=""/><a:cs typeface="{face}"/>', t)
    t = re.sub(r'<a:font script="Arab" typeface="[^"]*"/>', '<a:font script="Arab" typeface="Alexandria"/>', t)
    open(th, 'w', encoding='utf8').write(t)

# --- merge identical media (pptxgenjs writes one copy per placement)
med = os.path.join(work, 'ppt', 'media')
canon, remap = {}, {}
for fn in sorted(os.listdir(med)):
    h = hashlib.md5(open(os.path.join(med, fn), 'rb').read()).hexdigest()
    if h in canon:
        remap[fn] = canon[h]
    else:
        canon[h] = fn
rel_dirs = [os.path.join(work, 'ppt', d, '_rels') for d in ('slides', 'slideLayouts', 'slideMasters')]
for rd in rel_dirs:
    if not os.path.isdir(rd):
        continue
    for rf in os.listdir(rd):
        p = os.path.join(rd, rf)
        s = open(p, encoding='utf8').read()
        s2 = re.sub(r'Target="\.\./media/([^"]+)"', lambda m: f'Target="../media/{remap.get(m.group(1), m.group(1))}"', s)
        if s2 != s:
            open(p, 'w', encoding='utf8').write(s2)
for fn in remap:
    os.remove(os.path.join(med, fn))

# --- zip ([Content_Types].xml first)
if os.path.exists(DST):
    os.remove(DST)
with zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(work, '[Content_Types].xml'), '[Content_Types].xml')
    for base, _, fs in os.walk(work):
        for fn in fs:
            full = os.path.join(base, fn)
            arc = os.path.relpath(full, work)
            if arc == '[Content_Types].xml':
                continue
            z.write(full, arc)
shutil.rmtree(work)
print('ok', DST, 'media merged:', len(remap))
