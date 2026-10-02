# Pulls every paragraph / table of the source .docx into paras.json (index -> exact text), so the slides quote the file verbatim.
import zipfile, json, sys, os
import xml.etree.ElementTree as ET
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
src = sys.argv[1]
body = ET.fromstring(zipfile.ZipFile(src).read('word/document.xml')).find(W + 'body')
def ptext(p):
    t = ''
    for r in p.iter(W + 'r'):
        for c in r:
            if c.tag == W + 't': t += c.text or ''
            elif c.tag == W + 'tab': t += '\t'
            elif c.tag == W + 'br': t += '\n'
    return t
P, T = {}, {}
for i, el in enumerate(body):
    if el.tag == W + 'p':
        P[i] = ptext(el)
    elif el.tag == W + 'tbl':
        T[i] = [[ '\n'.join(ptext(p) for p in tc.findall('.//' + W + 'p')) for tc in tr.findall(W + 'tc')] for tr in el.iter(W + 'tr')]
json.dump({'p': P, 't': T}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paras.json'), 'w'), ensure_ascii=False, indent=0)
print(len(P), 'paragraphs', len(T), 'tables')
