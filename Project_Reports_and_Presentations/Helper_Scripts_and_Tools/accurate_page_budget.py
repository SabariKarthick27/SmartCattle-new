import docx
import math

doc = docx.Document("SmartCattle_Mini_Project_Report_v4.docx")

PAGE_HEIGHT = 697.7  # usable height in pt (11.69" - 2.0" margins)
LINE_PITCH = 12.0 * 1.45  # 17.4 pt
CHARS_PER_LINE = 85

def calc_text_height(text, font_size=12, line_spacing=1.45, space_before=2, space_after=7):
    pitch = font_size * line_spacing
    num_chars = len(text)
    num_lines = max(1, math.ceil(num_chars / CHARS_PER_LINE))
    return space_before + (num_lines * pitch) + space_after

def calc_table_height(table):
    # Table height = sum of row heights + padding
    num_rows = len(table.rows)
    # Average data row with padding is ~24 pt, header is ~28 pt
    h = 28 + (num_rows - 1) * 26 + 15
    return h

# Let's inspect paragraphs from Chapter 1 onward
p_elements = []
in_ch1 = False

page = 1
cur_h = 0.0

events = []

for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if "CHAPTER 1" in txt and not in_ch1:
        in_ch1 = True
        page = 1
        cur_h = 0.0
        events.append((page, "CHAPTER 1: INTRODUCTION", "Ch 1 Start"))
        continue
    
    if not in_ch1:
        continue
    
    # Check for manual page break in paragraph
    has_break = any("<w:br" in r._r.xml and 'w:type="page"' in r._r.xml for r in p.runs)
    if has_break or "w:pageBreakBefore" in p._p.xml:
        page += 1
        cur_h = 0.0
        
    if not txt:
        continue
        
    h = 0
    if p.style.name.startswith('Heading 1') or (txt.startswith('CHAPTER ') or txt in ['REFERENCES', 'APPENDIX']):
        h = 65
    elif p.style.name.startswith('Heading 2') or (len(txt) > 3 and txt[0].isdigit() and txt[1] == '.' and txt[2].isdigit()):
        h = 38
    elif p.style.name.startswith('Heading 3') or (len(txt) > 5 and txt[0].isdigit() and txt[1] == '.' and txt[2].isdigit() and txt[3] == '.'):
        h = 32
    elif p.style.name == 'List Bullet':
        h = calc_text_height(txt, font_size=11.5, line_spacing=1.35, space_before=2, space_after=5)
    else:
        h = calc_text_height(txt, font_size=12, line_spacing=1.45, space_before=2, space_after=7)
        
    if cur_h + h > PAGE_HEIGHT:
        page += 1
        cur_h = h
    else:
        cur_h += h
        
    if txt.startswith("CHAPTER ") or (len(txt) > 3 and txt[0].isdigit() and txt[1] in ' .') or txt in ['REFERENCES', 'APPENDIX']:
        events.append((page, txt[:65], f"cur_h={cur_h:.1f}"))

print(f"Total simulated pages from Chapter 1 to end: {page}")
for pg, title, extra in events:
    print(f"Page {pg:2d}: {title:55} ({extra})")
