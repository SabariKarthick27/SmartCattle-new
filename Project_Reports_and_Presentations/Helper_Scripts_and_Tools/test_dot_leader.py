import docx
from docx.shared import Inches, Pt
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()
section = doc.sections[0]
section.left_margin = Inches(1.25)
section.right_margin = Inches(1.0)

# Printable width: 8.27 - 2.25 = 6.02 inches = 8668 dxa
TAB_POS = 8640

p_hdr = doc.add_paragraph()
p_hdrPr = p_hdr._p.get_or_add_pPr()
tabs_hdr = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:pos="{TAB_POS}"/></w:tabs>')
p_hdrPr.append(tabs_hdr)
r_h1 = p_hdr.add_run("TITLE")
r_h1.bold = True
r_h2 = p_hdr.add_run("\tPAGE NO.")
r_h2.bold = True

items = [
    ("CHAPTER 1 INTRODUCTION", "1", True),
    ("  1.1 Background of Smallholder Dairy Healthcare", "1", False),
    ("  1.2 Challenges in Conventional Livestock Monitoring", "2", False),
    ("CHAPTER 2 LITERATURE REVIEW", "8", True),
    ("  2.1 Information, Communication and Networking Systems in PLF", "8", False),
]

for title, pg, is_b in items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.3
    pPr = p._p.get_or_add_pPr()
    tabs = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:leader="dot" w:pos="{TAB_POS}"/></w:tabs>')
    pPr.append(tabs)
    r = p.add_run(title)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    if is_b:
        r.bold = True
    r_pg = p.add_run(f"\t{pg}")
    r_pg.font.name = 'Times New Roman'
    r_pg.font.size = Pt(11)
    if is_b:
        r_pg.bold = True

doc.save("test_dot_leader.docx")
print("Saved test_dot_leader.docx successfully.")
