#!/usr/bin/env python3
"""Render each JSX draft at the repository root to a vector PDF of the same name, with headless
Chrome (React 18 + Recharts 2 UMD, Babel standalone; downloaded once to ~/.cache/jsx_pdf).
Page = the component's own bounding box; width = the old v2.1 screenshot's width / 2 (they were
taken at 2x). Fonts: Helvetica/Arial when installed, otherwise the system substitute.

    python3 render_jsx_pdf.py [SRC_DIR [OUT_DIR]]      (default: repository root for both)
"""
import os, re, subprocess, sys, tempfile, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SRC = sys.argv[1] if len(sys.argv) > 1 else ROOT
OUT = sys.argv[2] if len(sys.argv) > 2 else ROOT
CACHE = os.path.expanduser('~/.cache/jsx_pdf')
URLS = ['https://unpkg.com/react@18.3.1/umd/react.production.min.js',
        'https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js',
        'https://unpkg.com/prop-types@15.8.1/prop-types.min.js',
        'https://unpkg.com/react-is@18.3.1/umd/react-is.production.min.js',
        'https://unpkg.com/recharts@2.12.7/umd/Recharts.js',
        'https://unpkg.com/@babel/standalone@7.25.6/babel.min.js']
os.makedirs(CACHE, exist_ok=True)
for u in URLS:
    p = os.path.join(CACHE, os.path.basename(u))
    if not os.path.exists(p):
        urllib.request.urlretrieve(u, p)
TMP = tempfile.mkdtemp()
WIDTH = {'CophaseGroupCompare': 1060, 'HifiCompare': 770, 'HifiCompare3': 770, 'MethPhaserCompare': 620,
         'PhasingBenchmarkBars': 1156, 'PhasingBenchmarkBarsRow': 809, 'PhasingBenchmarkCompare': 1071,
         'UnphaseVenn3': 1215, 'UnphasedComposition': 640}
LIBS = [os.path.basename(u) for u in URLS]

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0;background:#fff}} #root{{width:{w}px}}
*{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style>{libs}</head><body><div id="root"></div>
<script type="text/babel" data-presets="react">
const {{ {names} }} = Recharts;
{code}
ReactDOM.createRoot(document.getElementById('root')).render(<{comp} />);
setTimeout(() => document.fonts.ready.then(() => {{
  const r = document.getElementById('root');
  const b = r.getBoundingClientRect();
  const s = document.createElement('style');
  s.textContent = '@page{{size:' + Math.ceil(b.width) + 'px ' + Math.ceil(b.height) + 'px;margin:0}}';
  document.head.appendChild(s);
  document.title = 'ready ' + Math.ceil(b.width) + 'x' + Math.ceil(b.height);
}}), 3000);   // after the web font (Libre Franklin, two drafts) has loaded
</script></body></html>"""

for f in sorted(os.listdir(SRC)):
    if not f.endswith('.jsx'):
        continue
    name = f[:-4]
    src = open(os.path.join(SRC, f)).read()
    imports = re.findall(r'import\s*\{([^}]*)\}\s*from\s*"recharts";', src)
    names = sorted({n.strip() for grp in imports for n in grp.split(',') if n.strip()})
    code = re.sub(r'import\s+React[^;]*;', 'const { useState, useMemo } = React;', src)
    code = re.sub(r'import\s*\{[^}]*\}\s*from\s*"recharts";', '', code)
    comp = re.search(r'export default function (\w+)', code).group(1)
    code = code.replace('export default function', 'function')
    # no animation, so the print shows the final state
    code = re.sub(r'<(Line|Bar|Area|Pie|Scatter)(\s)', r'<\1 isAnimationActive={false}\2', code)
    libs = ''.join(f'<script src="file://{CACHE}/{l}"></script>' for l in LIBS)
    html = os.path.join(TMP, f'{name}.html')
    open(html, 'w').write(PAGE.format(w=WIDTH.get(name, 1000), libs=libs, names=', '.join(names), code=code, comp=comp))
    pdf = os.path.join(OUT, f'{name}.pdf')
    r = subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--no-sandbox',
                        '--allow-file-access-from-files', '--no-pdf-header-footer',
                        '--virtual-time-budget=8000', f'--print-to-pdf={pdf}', f'file://{html}'],
                       capture_output=True, text=True, timeout=120)
    print(name, 'ok' if os.path.exists(pdf) else 'FAILED', r.stderr.strip().splitlines()[-1:] if r.returncode else '')
