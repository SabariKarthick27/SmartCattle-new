import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r'c:\Project\SmartCattle new\QR MINI PROJECT REPORT.docx')

for p_i in range(378, 401):
    p = doc.paragraphs[p_i]
    blips = p._element.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
    embeds = [b.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed') for b in blips]
    targets = [doc.part.rels[e].target_ref for e in embeds if e in doc.part.rels]
    print(f"P[{p_i}]: runs={len(p.runs)}, images={targets}")
    if p.text.strip():
        print(f"       text: {p.text.strip()}")
