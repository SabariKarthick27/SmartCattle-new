import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

doc = docx.Document(r'c:\Project\SmartCattle new\QR MINI PROJECT REPORT.docx')

print(f"Total inline shapes: {len(doc.inline_shapes)}")

# Check media parts in docx package
part_images = []
for rel in doc.part.rels.values():
    if "image" in rel.target_ref:
        part_images.append(rel.target_ref)

print(f"Total media image parts referenced: {len(part_images)}")

# Check each paragraph drawing
drawing_count = 0
for i, p in enumerate(doc.paragraphs):
    for r in p.runs:
        drawings = r._element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing')
        if drawings:
            drawing_count += len(drawings)
            print(f"P[{i}] has {len(drawings)} image/drawing. Text around it: {p.text[:60]}")

print(f"Total drawings found in paragraphs: {drawing_count}")
