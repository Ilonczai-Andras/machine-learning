import markdown
import subprocess
import pymupdf
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, '..'))

md_file = os.path.join(base_dir, '1_merfoldko_dokumentacio.md')
html_out = os.path.join(base_dir, '1_merfoldko_dokumentacio_5oldal.html')
pdf_out = os.path.join(base_dir, '1_merfoldko_dokumentacio_5oldal.pdf')

if not os.path.exists(md_file):
    raise FileNotFoundError(f"Markdown fájl nem található: {md_file}")

with open(md_file, mode='r', encoding='utf-8') as f:
    raw_md = f.read()

# Separate frontmatter and style
if '</style>' in raw_md:
    style_part, body_md = raw_md.split('</style>', 1)
    style_html = style_part.split('---', 2)[-1] + '</style>'
else:
    style_html = ""
    body_md = raw_md

# Convert to HTML with tables extension
html_body = markdown.markdown(body_md.strip(), extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{style_html}
</head>
<body class="markdown-preview">
{html_body}
</body>
</html>"""

with open(html_out, 'w', encoding='utf-8') as f:
    f.write(full_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_out}",
    f"file:///{html_out.replace(os.sep, '/')}"
]

print("Compiling 5-page PDF using Chrome headless...")
res = subprocess.run(cmd, capture_output=True, text=True)

# Clean up temp HTML
if os.path.exists(html_out):
    os.remove(html_out)

if os.path.exists(pdf_out):
    doc = pymupdf.open(pdf_out)
    print(f"SUCCESS! Output PDF has {len(doc)} pages: {pdf_out}")
    for i, p in enumerate(doc):
        txt = [l.strip() for l in p.get_text().split('\n') if l.strip()]
        print(f"  Page {i+1}: {len(txt)} lines | Start: '{txt[0][:35]}' | End: '{txt[-1][:35]}'")
else:
    print("Compilation failed!")
