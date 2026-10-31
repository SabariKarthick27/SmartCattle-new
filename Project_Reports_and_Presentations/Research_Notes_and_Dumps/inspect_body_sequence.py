import docx

doc = docx.Document('SaltLens_DSS_Final_Project_Report_Final_With_Cover_ORIGINAL_BACKUP.docx')

tbl_counter = 0
p_counter = 0

with open('saltlens_body_sequence.txt', 'w', encoding='utf-8') as f:
    for idx, el in enumerate(doc.element.body):
        tag = el.tag.split('}')[-1]
        if tag == 'p':
            p = docx.text.paragraph.Paragraph(el, doc)
            txt = p.text.strip()
            f.write(f"BODY_{idx} [P_{p_counter}]: {txt[:100]}\n")
            p_counter += 1
        elif tag == 'tbl':
            t = docx.table.Table(el, doc)
            hdr = [c.text.strip().replace('\n', ' ') for c in t.rows[0].cells]
            f.write(f"BODY_{idx} [TBL_{tbl_counter}]: rows={len(t.rows)}, cols={len(t.columns)} | {hdr[:2]}\n")
            tbl_counter += 1
        elif tag == 'sectPr':
            f.write(f"BODY_{idx} [SECT_PR]\n")

print(f"Total body elements: {idx+1}, Paragraphs: {p_counter}, Tables: {tbl_counter}")
