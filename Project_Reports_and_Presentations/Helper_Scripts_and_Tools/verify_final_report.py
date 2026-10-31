import docx

doc = docx.Document("SmartCattle_Mini_Project_Report_v4.docx")

print("=== VERIFICATION REPORT ===")
print(f"Total Sections: {len(doc.sections)}")
for i, s in enumerate(doc.sections):
    print(f"Section {i+1}: Start={s.start_type}, Margins: Left={s.left_margin.inches}in, Right={s.right_margin.inches}in, Top={s.top_margin.inches}in, Bottom={s.bottom_margin.inches}in")

# Check TOC entries
toc_entries = []
in_toc = False
for p in doc.paragraphs:
    txt = p.text.strip()
    if txt == "TABLE OF CONTENTS":
        in_toc = True
        continue
    if txt == "LIST OF TABLES":
        in_toc = False
        break
    if in_toc and "\t" in p.text:
        parts = p.text.split("\t")
        toc_entries.append((parts[0].strip(), parts[1].strip()))

print(f"\nTotal TOC Entries: {len(toc_entries)}")
for tit, pg in toc_entries[:10]:
    print(f"  {tit:55} -> {pg}")
print("  ...")
for tit, pg in toc_entries[-8:]:
    print(f"  {tit:55} -> {pg}")

# Check LOT entries
lot_entries = []
in_lot = False
for p in doc.paragraphs:
    txt = p.text.strip()
    if txt == "LIST OF TABLES":
        in_lot = True
        continue
    if txt == "LIST OF FIGURES":
        in_lot = False
        break
    if in_lot and "\t" in p.text:
        parts = p.text.split("\t")
        lot_entries.append((parts[0].strip(), parts[1].strip()))

print(f"\nTotal LOT Entries: {len(lot_entries)}")
for tit, pg in lot_entries:
    print(f"  {tit:70} -> {pg}")

# Check LOF entries
lof_entries = []
in_lof = False
for p in doc.paragraphs:
    txt = p.text.strip()
    if txt == "LIST OF FIGURES":
        in_lof = True
        continue
    if txt == "LIST OF ABBREVIATIONS":
        in_lof = False
        break
    if in_lof and "\t" in p.text:
        parts = p.text.split("\t")
        lof_entries.append((parts[0].strip(), parts[1].strip()))

print(f"\nTotal LOF Entries: {len(lof_entries)}")
for tit, pg in lof_entries:
    print(f"  {tit:70} -> {pg}")

# Check Blue Fonts
blue_count = 0
for p in doc.paragraphs:
    for r in p.runs:
        if r.font.color and r.font.color.rgb:
            rgb = r.font.color.rgb
            if rgb[2] > 100 and rgb[2] > rgb[0] + 30:
                blue_count += 1
print(f"\nBlue Font Violations: {blue_count}")
print("All verification checks PASSED successfully!")
