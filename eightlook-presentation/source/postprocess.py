# -*- coding: utf-8 -*-
"""Post-process the pptxgenjs output:
   * one <a:pPr> per paragraph (pptxgenjs repeats it per run) + RTL flags
   * clean font references, Arabic theme fonts
   * Morph transitions (fade fallback) and a choreographed, auto-playing animation timeline per slide
"""
import json, os, re, shutil, sys, zipfile
from lxml import etree

SRC, DST, ANIMS = sys.argv[1], sys.argv[2], sys.argv[3]
FONT = 'Sakkal Saad TN Trial Light'
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
A = '{%s}' % NS['a']
PNS = '{%s}' % NS['p']

work = DST + '.dir'
shutil.rmtree(work, ignore_errors=True)
with zipfile.ZipFile(SRC) as z:
    z.extractall(work)
anims = {i + 1: a for i, a in enumerate(json.load(open(ANIMS)))}  # by slide order

DUR = {'fade': 600, 'rise': 750, 'wipeR': 850, 'zoom': 850, 'zoomOut': 950, 'pop': 600, 'spinIn': 1200, 'wheel': 1300, 'blink': 1200}


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


def prop(nid, spid, attr, keys, dur, decel=100000, num=False):
    tav = ''.join(f'<p:tav tm="{tm}"><p:val>' + (f'<p:fltVal val="{v}"/>' if num else f'<p:strVal val="{v}"/>') + '</p:val></p:tav>' for tm, v in keys)
    dc = f' decel="{decel}"' if decel else ''
    return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{nid()}" dur="{dur}" fill="hold"{dc}/>{tgt(spid)}'
            f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst>{tav}</p:tavLst></p:anim>')


def scale(nid, spid, keys, dur, decel=100000):
    kw = [(tm, f'#ppt_w*{f}' if f != 1 else '#ppt_w') for tm, f in keys]
    kh = [(tm, f'#ppt_h*{f}' if f != 1 else '#ppt_h') for tm, f in keys]
    return prop(nid, spid, 'ppt_w', kw, dur, decel) + prop(nid, spid, 'ppt_h', kh, dur, decel)


def effect(nid, spid, kind, delay, dur):
    """returns (presetID, presetClass, subtype, behaviours, extra cTn attrs)"""
    if kind == 'fade':
        return 10, 'entr', 0, setvis(nid, spid) + fx(nid, spid, 'fade', dur), ''
    if kind == 'rise':          # soft float-in: fade + 36px rise with ease-out
        return 42, 'entr', 0, (setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .8)) +
                               prop(nid, spid, 'ppt_x', [(0, '#ppt_x'), (100000, '#ppt_x')], dur) +
                               prop(nid, spid, 'ppt_y', [(0, '#ppt_y+.034'), (100000, '#ppt_y')], dur)), ''
    if kind == 'wipeR':         # reveal in Arabic reading direction (right -> left) with a soft fade
        return 22, 'entr', 2, setvis(nid, spid) + fx(nid, spid, 'wipe(right)', dur) + fx(nid, spid, 'fade', int(dur * .7)), ''
    if kind == 'zoom':          # "focus pull": 82% -> 100% + fade
        return 53, 'entr', 16, setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .7)) + scale(nid, spid, [(0, .82), (100000, 1)], dur), ''
    if kind == 'zoomOut':       # lands from 130%
        return 53, 'entr', 32, setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .6)) + scale(nid, spid, [(0, 1.3), (100000, 1)], dur), ''
    if kind == 'pop':           # elastic pop with a small overshoot
        return 53, 'entr', 16, setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .45)) + scale(nid, spid, [(0, .3), (62000, 1.08), (100000, 1)], dur, 0), ''
    if kind == 'spinIn':        # lens-aperture swirl: grow + turn + fade
        return 31, 'entr', 0, (setvis(nid, spid) + fx(nid, spid, 'fade', int(dur * .5)) + scale(nid, spid, [(0, .55), (100000, 1)], dur) +
                               prop(nid, spid, 'style.rotation', [(0, -110), (100000, 0)], dur, 100000, True)), ''
    if kind == 'wheel':
        return 21, 'entr', 1, setvis(nid, spid) + fx(nid, spid, 'wheel(1)', dur), ''
    if kind == 'blink':         # camera REC light
        b = (f'<p:anim calcmode="discrete" valueType="str"><p:cBhvr><p:cTn id="{nid()}" dur="{dur}" fill="hold"/>{tgt(spid)}'
             f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst>'
             f'<p:tav tm="0"><p:val><p:strVal val="hidden"/></p:val></p:tav><p:tav tm="40000"><p:val><p:strVal val="visible"/></p:val></p:tav></p:tavLst></p:anim>')
        return 35, 'emph', 0, b, ' repeatCount="indefinite"'
    raise ValueError(kind)


def timing_xml(items, ids, kinds_of):
    nid = Ids()
    pars = []
    bld = []
    for it in sorted(items, key=lambda x: x['d']):
        spid = ids.get(it['name'])
        if not spid:
            continue
        kind = it['a']
        dur = it.get('t') or DUR[kind]
        pid, pcls, sub, beh, extra = effect(nid, spid, kind, it['d'], dur)
        cid = nid()
        pars.append(f'<p:par><p:cTn id="{cid}" presetID="{pid}" presetClass="{pcls}" presetSubtype="{sub}"{extra} fill="hold" grpId="0" nodeType="withEffect">'
                    f'<p:stCondLst><p:cond delay="{int(it["d"])}"/></p:stCondLst><p:childTnLst>{beh}</p:childTnLst></p:cTn></p:par>')
        k = kinds_of.get(spid)
        if k == 'sp':
            bld.append(f'<p:bldP spid="{spid}" grpId="0" animBg="1"/>')
        elif k == 'txsp':
            bld.append(f'<p:bldP spid="{spid}" grpId="0"/>')
        elif k == 'graphicFrame':
            bld.append(f'<p:bldGraphic spid="{spid}" grpId="0"><p:bldAsOne/></p:bldGraphic>')
    if not pars:
        return ''
    # ids inside the effect pars were allocated before the container ids; renumber to keep them unique & ordered
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
    # renumber all cTn ids in document order (PowerPoint expects a depth-first sequence)
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
    # --- paragraphs
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
    # --- fonts
    for tag in ('latin', 'ea', 'cs'):
        for el in root.iter(A + tag):
            for at in ('pitchFamily', 'charset'):
                if at in el.attrib:
                    del el.attrib[at]
            if tag == 'ea' and el.get('typeface') == FONT:
                el.getparent().remove(el)
    # --- ids / kinds
    ids, kinds = {}, {}
    for el in root.iter(PNS + 'cNvPr'):
        nm, i = el.get('name'), el.get('id')
        ids[nm] = i
        holder = el.getparent().getparent()
        tag = etree.QName(holder).localname
        if tag == 'sp':
            kinds[i] = 'txsp' if holder.find('.//' + A + 't') is not None else 'sp'
        else:
            kinds[i] = tag
    xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True).decode('utf8')
    # namespaces for transitions
    if 'xmlns:p14=' not in xml:
        xml = xml.replace('<p:sld ', '<p:sld xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" ', 1)
    an = anims.get(n, {'tr': 'morph', 'items': []})
    tr = transition_xml(an['tr'], 900 if an['tr'] == 'fade' else 1300)
    tm = timing_xml(an['items'], ids, kinds)
    xml = re.sub(r'<p:transition.*?</p:transition>|<p:timing>.*?</p:timing>', '', xml, flags=re.S)
    if '</p:clrMapOvr>' in xml:
        xml = xml.replace('</p:clrMapOvr>', '</p:clrMapOvr>' + tr + tm, 1)
    else:
        xml = xml.replace('</p:cSld>', '</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>' + tr + tm, 1)
    open(fp, 'w', encoding='utf8').write(xml)

# --- theme fonts (so any new text typed in PowerPoint uses the brand font)
th = os.path.join(work, 'ppt', 'theme', 'theme1.xml')
if os.path.exists(th):
    t = open(th, encoding='utf8').read()
    t = re.sub(r'(<a:(?:major|minor)Font>)<a:latin typeface="[^"]*"( panose="[^"]*")?/><a:ea typeface="[^"]*"/><a:cs typeface="[^"]*"/>',
               rf'\1<a:latin typeface="{FONT}"/><a:ea typeface=""/><a:cs typeface="{FONT}"/>', t)
    t = re.sub(r'<a:font script="Arab" typeface="[^"]*"/>', f'<a:font script="Arab" typeface="{FONT}"/>', t)
    open(th, 'w', encoding='utf8').write(t)

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
print('ok', DST)
