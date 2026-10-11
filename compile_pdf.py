import markdown
import subprocess
import pymupdf
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
md_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, '1_milestone', '1_merfoldko_dokumentacio.md')
pdf_out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(script_dir, '1_milestone', '1_merfoldko_dokumentacio.pdf')

md_file = os.path.abspath(md_file)
pdf_out = os.path.abspath(pdf_out)
html_out = os.path.splitext(pdf_out)[0] + '_temp_render.html'

if not os.path.exists(md_file):
    raise FileNotFoundError(f"Markdown fájl nem található: {md_file}")

with open(md_file, mode='r', encoding='utf-8') as f:
    raw_md = f.read()

if '</style>' in raw_md:
    style_part, body_md = raw_md.split('</style>', 1)
    style_html = style_part.split('---', 2)[-1] + '</style>'
else:
    style_html = ""
    body_md = raw_md

html_body = markdown.markdown(body_md.strip(), extensions=['tables', 'fenced_code'])
md_dir = os.path.dirname(md_file).replace(os.sep, '/')

full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<base href="file:///{md_dir}/">
{style_html}
</head>
<body class="markdown-preview">
{html_body}
</body>
</html>"""

with open(html_out, 'w', encoding='utf-8') as f:
    f.write(full_html)

browser_candidates = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
]
browser_path = next((b for b in browser_candidates if os.path.exists(b)), None)
if not browser_path:
    raise FileNotFoundError("Nem található támogatott Chromium böngésző (Edge vagy Chrome)!")

cmd = [
    browser_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_out}",
    f"file:///{html_out.replace(os.sep, '/')}"
]

print(f"PDF fordítása folyamatban ({os.path.basename(browser_path)})...")
res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(html_out):
    os.remove(html_out)

if os.path.exists(pdf_out):
    doc = pymupdf.open(pdf_out)
    print(f"SIKER! A kimeneti PDF elkészült ({len(doc)} oldal): {pdf_out}")
    for i, p in enumerate(doc):
        txt = [l.strip() for l in p.get_text().split('\n') if l.strip()]
        start_t = txt[0][:35] if txt else 'ÜRES'
        end_t = txt[-1][:35] if txt else 'ÜRES'
        print(f"  {i+1}. oldal: {len(txt)} sor | Kezdés: '{start_t}' | Vége: '{end_t}'")
    doc.close()
else:
    print(f"A fordítás sikertelen:\n{res.stderr}")