# Contact sheets (2x2) of the preview PNGs for review
import glob, os, sys
from PIL import Image, ImageDraw
B = os.path.dirname(os.path.abspath(__file__))
fs = sorted(glob.glob(os.path.join(B, 'deck/prev/p*.png')))
only = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 and sys.argv[1] else None
if only: fs = [f for f in fs if int(os.path.basename(f)[1:3]) in only]
os.makedirs(os.path.join(B, 'deck/sheets'), exist_ok=True)
for i in range(0, len(fs), 4):
    sh = Image.new('RGB', (1930, 1090), '#888')
    for j, f in enumerate(fs[i:i + 4]):
        im = Image.open(f).convert('RGB').resize((960, 540))
        sh.paste(im, ((j % 2) * 970, (j // 2) * 550))
        ImageDraw.Draw(sh).text(((j % 2) * 970 + 6, (j // 2) * 550 + 4), os.path.basename(f), fill='red')
    sh.save(os.path.join(B, f'deck/sheets/sh_{i // 4 + 1:02d}.jpg'), quality=88)
print('sheets', (len(fs) + 3) // 4)
