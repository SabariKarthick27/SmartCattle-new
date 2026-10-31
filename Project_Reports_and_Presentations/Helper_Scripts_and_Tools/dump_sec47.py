import docx

doc = docx.Document(r'Project_Report_Final_20_10_26 (1).docx')
with open('sec47_full.txt', 'w', encoding='utf-8') as f:
    in_47 = False
    for i, p in enumerate(doc.paragraphs):
        if '4.7 Algorithms/Techniques Used' in p.text:
            in_47 = True
        if '4.8 Dataset/Data Collection' in p.text:
            in_47 = False
            f.write(f"\n[P{i}] END OF 4.7: {p.text}\n")
        if in_47:
            f.write(f"[P{i}] {p.text}\n")
print("Section 4.7 dumped successfully!")
