# Side-by-side QA: browser reference (top) vs PowerPoint render via LibreOffice (bottom).
import sys, os, glob
from PIL import Image
B = os.path.dirname(os.path.abspath(__file__))
qa = os.path.join(B, 'pptx_build/qa')
only = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 and sys.argv[1] else None
files = sorted(glob.glob(os.path.join(qa, 's-*.jpg')), key=lambda f: int(f.split('-')[-1].split('.')[0]))
for f in files:
    n = int(f.split('-')[-1].split('.')[0])
    if only and n not in only: continue
    ref = Image.open(os.path.join(B, f'pptx_build/ref_{n:02d}.png')).convert('RGB').resize((960, 540))
    pp = Image.open(f).convert('RGB').resize((960, 540))
    out = Image.new('RGB', (960, 1084), 'red'); out.paste(ref, (0, 0)); out.paste(pp, (0, 544))
    out.save(os.path.join(qa, f'cmp_{n:02d}.jpg'), quality=85)
print('ok')
