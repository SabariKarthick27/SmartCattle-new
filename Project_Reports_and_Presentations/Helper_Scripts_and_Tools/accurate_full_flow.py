import docx
import math

doc = docx.Document("SmartCattle_Mini_Project_Report_v4.docx")

PAGE_HEIGHT = 697.7  # usable height in pt (11.69" - 2.0" margins)
LINE_PITCH = 12.0 * 1.45  # 17.4 pt
CHARS_PER_LINE = 85

def calc_p_height(p):
    txt = p.text.strip()
    if not txt:
        sp_b = p.paragraph_format.space_before.pt if p.paragraph_format.space_before else 0
        sp_a = p.paragraph_format.space_after.pt if p.paragraph_format.space_after else 4
        return sp_b + sp_a
        
    has_pic = '<w:drawing>' in p._p.xml or '<w:pict>' in p._p.xml
    if has_pic:
        if "Figure" in txt:
            return 210.0
        return 110.0

    if p.style.name.startswith('Heading 1') or (txt.startswith('CHAPTER ') or txt in ['REFERENCES', 'APPENDIX']):
        return 72.0
    elif p.style.name.startswith('Heading 2') or (len(txt) > 3 and txt[0].isdigit() and txt[1] == '.' and txt[2].isdigit()):
        return 42.0
    elif p.style.name.startswith('Heading 3') or (len(txt) > 5 and txt[0].isdigit() and txt[1] == '.' and txt[2].isdigit() and txt[3] == '.'):
        return 34.0
    elif p.style.name == 'List Bullet':
        num_lines = max(1, math.ceil(len(txt) / CHARS_PER_LINE))
        return 2.0 + (num_lines * 11.5 * 1.35) + 5.0
    else:
        num_lines = max(1, math.ceil(len(txt) / CHARS_PER_LINE))
        return 2.0 + (num_lines * LINE_PITCH) + 7.0

def calc_tbl_height(tbl_elem):
    rows = tbl_elem.xpath('.//w:tr')
    num_rows = len(rows)
    if num_rows == 1:
        txt_len = sum(len(node.text or '') for node in tbl_elem.xpath('.//w:t'))
        if txt_len > 200:
            return 135.0
        return 80.0
    return 32.0 + (num_rows - 1) * 28.0 + 15.0

body = doc._element.body
page = 1
cur_h = 0.0
in_main = False

findings = []

for child in body:
    tag = child.tag.split('}')[-1]
    
    if tag == 'p':
        p = docx.text.paragraph.Paragraph(child, doc)
        txt = p.text.strip()
        
        if "CHAPTER 1" in txt and not in_main:
            in_main = True
            page = 1
            cur_h = 0.0
            
        if not in_main:
            continue
            
        has_break = any('<w:br' in r._r.xml and 'w:type="page"' in r._r.xml for r in p.runs)
        if has_break or 'w:pageBreakBefore' in p._p.xml:
            page += 1
            cur_h = 0.0
            
        h = calc_p_height(p)
        if cur_h + h > PAGE_HEIGHT:
            page += 1
            cur_h = h
        else:
            cur_h += h
            
        if txt.startswith("CHAPTER ") or (len(txt) > 3 and txt[0].isdigit() and txt[1] in ' .') or txt in ['REFERENCES', 'APPENDIX'] or txt.startswith('Table ') or txt.startswith('Figure '):
            findings.append((page, txt[:65]))
            
    elif tag == 'tbl':
        if not in_main:
            continue
        h = calc_tbl_height(child)
        if cur_h + h > PAGE_HEIGHT:
            page += 1
            cur_h = h
        else:
            cur_h += h

print(f"=== EXACT PAGE NUMBERS FROM CHAPTER 1 (Page 1) TO APPENDIX (Page {page}) ===")
for pg, title in findings:
    print(f"Page {pg:2d}: {title}")
