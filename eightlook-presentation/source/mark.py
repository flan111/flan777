import numpy as np, json
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union
from shapely import affinity
N=1440
Ct=(518.3,364.0); rti,rto=39.5,89.4
Cb=(520.5,448.5); rbi,rbo=37.9,87.8
P0=np.array([454.0,347.7]); P1=np.array([581.5,466.5])
d=(P1-P0)/np.linalg.norm(P1-P0)
def ring(c,ri,ro): return Point(c).buffer(ro,resolution=N//4).difference(Point(c).buffer(ri,resolution=N//4))
# half-planes: big polygons on each side of line
far=2000; nrm=np.array([d[1],-d[0]])  # normal pointing "up-right"? check sign
A=P0-d*far; Bp=P0+d*far
upper=Polygon([A,Bp,Bp+nrm*far,A+nrm*far]); lower=Polygon([A,Bp,Bp-nrm*far,A-nrm*far])
# ensure upper contains a point clearly above (y smaller): (600,300)
if not upper.contains(Point(600,300)): upper,lower=lower,upper
top=ring(Ct,rti,rto).intersection(upper)
bot=ring(Cb,rbi,rbo).intersection(lower)
# highlight arc
r=26.2; w=11.2
angs=np.radians(np.linspace(-78.9,-22.3,200))
arcline=LineString([(Ct[0]+r*np.cos(a),Ct[1]+r*np.sin(a)) for a in angs])
arc=arcline.buffer(w/2,resolution=64)
def path(g):
    polys=[g] if g.geom_type=='Polygon' else list(g.geoms)
    out=[]
    for p in polys:
        for ring_ in [p.exterior]+list(p.interiors):
            pts=list(ring_.coords)
            out.append('M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'Z')
    return ''.join(out)
full=unary_union([top,bot,arc])
minx,miny,maxx,maxy=full.bounds
print('bounds',full.bounds)
data={'top':path(top),'bot':path(bot),'arc':path(arc),'bounds':[minx,miny,maxx,maxy]}
json.dump(data,open('assets/mark_geom.json','w'))
vb=f"{minx:.2f} {miny:.2f} {maxx-minx:.2f} {maxy-miny:.2f}"
O='#FF8D26'
open('assets/mark.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><path fill="{O}" fill-rule="evenodd" d="{data["top"]}{data["bot"]}{data["arc"]}"/></svg>')

# ---- piece files ----
import os
os.makedirs('assets/mark',exist_ok=True)
pieces={'top':top,'bot':bot,'arc':arc}
COLORS={'o':'#FF8D26','w':'#FFFFFF','y':'#F6C342','b':'#43644B','ink':'#1E2A36'}
meta={'full':[minx,miny,maxx,maxy]}
for k,g in pieces.items():
    a,b_,c,d_=g.bounds
    meta[k]=[a,b_,c,d_]
    for cn,cv in COLORS.items():
        open(f'assets/mark/{k}_{cn}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{a:.3f} {b_:.3f} {c-a:.3f} {d_-b_:.3f}"><path fill="{cv}" fill-rule="evenodd" d="{path(g)}"/></svg>')
for cn,cv in COLORS.items():
    open(f'assets/mark/full_{cn}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><path fill="{cv}" fill-rule="evenodd" d="{data["top"]}{data["bot"]}{data["arc"]}"/></svg>')
json.dump(meta,open('assets/mark/meta.json','w'))
print(meta)
