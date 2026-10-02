#!/bin/bash
# Full PPTX build: measure HTML -> build pptx -> animations/transitions -> validate -> LibreOffice render for QA
set -e
cd "$(dirname "$0")"
SK=${SK:-/root/.claude/skills/synced/803a421d-8efa-414e-a0ab-0c107bac4082_3f058a2f-17e6-4956-aa28-cfc78abadf5e/pptx}
rm -rf pptx_build/img pptx_build/ref_*.png
node extract.js
node build_pptx.js
python3 postprocess.py pptx_build/raw.pptx pptx_build/deck.pptx pptx_build
python3 $SK/scripts/office/validate.py pptx_build/deck.pptx | tail -3
if [ "$1" != "noqa" ]; then
  mkdir -p pptx_build/qa && cd pptx_build/qa && rm -f s-*.jpg cmp_*.jpg deck.pdf && cp ../deck.pptx .
  timeout 900 python3 $SK/scripts/office/soffice.py --headless --convert-to pdf deck.pptx >/dev/null 2>&1
  pdftoppm -jpeg -r 72 deck.pdf s && cd ../.. && python3 compare.py
fi
