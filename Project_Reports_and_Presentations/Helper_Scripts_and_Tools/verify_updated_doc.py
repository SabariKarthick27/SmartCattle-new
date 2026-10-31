import docx

doc = docx.Document(r'Project_Report_Final_Updated.docx')
with open('verify_updated_sec47.txt', 'w', encoding='utf-8') as f:
    in_47 = False
    for i, p in enumerate(doc.paragraphs):
        if '4.7 Algorithms/Techniques Used' in p.text:
            in_47 = True
        if '4.8 Dataset/Data Collection' in p.text:
            in_47 = False
            f.write(f"\n[P{i}] END OF 4.7: {p.text}\n")
        if in_47:
            has_pic = 'pic:pic' in p._p.xml or 'w:drawing' in p._p.xml
            f.write(f"[P{i:3d}] [pic={has_pic}] {p.text}\n")
print("Verified successfully!")
