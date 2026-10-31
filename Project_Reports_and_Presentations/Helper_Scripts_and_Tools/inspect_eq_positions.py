import docx

doc = docx.Document(r'Project_Report_Final_20_10_26 (1).docx')
for i in range(180, 241):
    p = doc.paragraphs[i]
    has_pic = 'pic:pic' in p._p.xml or 'w:drawing' in p._p.xml
    txt = p.text.strip().encode('ascii', errors='replace').decode('ascii')
    print(f"P{i:3d} [pic={has_pic}]: {txt[:70]}")
