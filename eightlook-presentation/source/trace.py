import numpy as np, potrace, sys
from PIL import Image

def trace_mask(mask, scale_back):
    bm = potrace.Bitmap(~mask)
    path = bm.trace(turdsize=8, alphamax=1.0, opticurve=True, opttolerance=0.2)
    parts=[]
    s=1.0/scale_back
    f=lambda p: f"{p.x*s:.2f},{p.y*s:.2f}"
    for curve in path:
        d=[f"M{f(curve.start_point)}"]
        for seg in curve:
            if seg.is_corner:
                d.append(f"L{f(seg.c)}L{f(seg.end_point)}")
            else:
                d.append(f"C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}")
        d.append("Z")
        parts.append(''.join(d))
    return ' '.join(parts)

def load(fn, up):
    im=Image.open(fn).convert('RGBA')
    bg=Image.new('RGBA',im.size,(255,255,247,255)); bg.alpha_composite(im)
    im=bg.convert('RGB')
    im=im.resize((im.width*up, im.height*up), Image.LANCZOS)
    return np.asarray(im).astype(float)

# eight look logo
up=4
a=load('src/zai/docx/word/media/image1.jpeg', up)
R,G,B=a[...,0],a[...,1],a[...,2]
bgc=np.array([255,255,247.])
orange=np.array([246,142,47.]); ink=np.array([9,35,34.])
# projection-based coverage
def cov(col):
    d=bgc-col
    t=((bgc-a)@d)/(d@d)
    return t
# classify: orange pixels have R high, B low; ink pixels dark
o_mask=(R>200)&(B<150)&(G<200)
i_mask=(R<120)&(G<130)&(B<130)
po=trace_mask(o_mask, up); pi=trace_mask(i_mask, up)
W,H=1042,1042
open('assets/eightlook_paths.txt','w').write(po+'\n'+pi)
# bounding boxes
ys,xs=np.where(o_mask); print('orange bbox',xs.min()/up,ys.min()/up,xs.max()/up,ys.max()/up)
ys,xs=np.where(i_mask); print('ink bbox',xs.min()/up,ys.min()/up,xs.max()/up,ys.max()/up)
# text rows split
rows=np.where(i_mask.any(axis=1))[0]
gaps=np.where(np.diff(rows)>4)[0]
print('ink row groups', [(rows[0]/up)]+[ (rows[g]/up, rows[g+1]/up) for g in gaps], rows[-1]/up)

# basmat logo
up2=6
b=load('src/zai/docx/word/media/image2.png', up2)
R,G,B=b[...,0],b[...,1],b[...,2]
teal_mask=(R<120)&(B>40)&(G<140)
yel_mask=(R>180)&(G>130)&(B<120)
pt=trace_mask(teal_mask, up2); py=trace_mask(yel_mask, up2)
open('assets/basmat_paths.txt','w').write(pt+'\n'+py)
ys,xs=np.where(teal_mask); print('teal bbox',xs.min()/up2,ys.min()/up2,xs.max()/up2,ys.max()/up2)
ys,xs=np.where(yel_mask); print('yel bbox',xs.min()/up2,ys.min()/up2,xs.max()/up2,ys.max()/up2)
