# Builds static weights of Alexandria (OFL) with Windows-friendly family names, so PowerPoint can pick each weight by name.
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
import os
BASE = os.path.dirname(os.path.abspath(__file__))
W = [(100, 'Thin'), (200, 'ExtraLight'), (300, 'Light'), (400, 'Regular'), (500, 'Medium'),
     (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold'), (900, 'Black')]
for wt, st in W:
    f = TTFont(os.path.join(BASE, 'assets/Alexandria-VF.ttf'))
    f = instancer.instantiateVariableFont(f, {'wght': wt}, updateFontNames=False)
    fam = 'Alexandria' if st in ('Regular', 'Bold') else f'Alexandria {st}'
    sub = st if st in ('Regular', 'Bold') else 'Regular'
    full = 'Alexandria' + ('' if st == 'Regular' else ' ' + st)
    ps = 'Alexandria-' + st
    name = f['name']
    for nid in (16, 17, 21, 22, 25):
        name.removeNames(nameID=nid)
    for rec in list(name.names):
        if rec.nameID == 1: rec.string = fam
        elif rec.nameID == 2: rec.string = sub
        elif rec.nameID == 3: rec.string = f'Alexandria-{st};static'
        elif rec.nameID == 4: rec.string = full
        elif rec.nameID == 6: rec.string = ps
    name.setName('Alexandria', 16, 3, 1, 0x409); name.setName(st, 17, 3, 1, 0x409)
    os2 = f['OS/2']; os2.usWeightClass = wt
    sel = os2.fsSelection & ~(0x1 | 0x20 | 0x40)
    sel |= 0x20 if st == 'Bold' else 0x40
    os2.fsSelection = sel
    f['head'].macStyle = 1 if st == 'Bold' else 0
    for t in ('STAT', 'fvar', 'gvar', 'avar', 'HVAR', 'MVAR'):
        if t in f: del f[t]
    f.save(os.path.join(BASE, '..', 'fonts', f'Alexandria-{st}.ttf'))
    print(st, fam, '/', sub)
