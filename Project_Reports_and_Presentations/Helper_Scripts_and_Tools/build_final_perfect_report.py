import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_perfect_academic_report():
    doc = docx.Document()

    # Academic margins: Left 1.25 in (ruler 1.25"), Right 1.0 in, Top 1.0 in, Bottom 1.0 in
    # Printable content width = 8.27 - 2.25 = 6.02 in = 8668 dxa
    TAB_STOP_RIGHT = 8640  # 6.0 inches right margin tab
    TAB_STOP_ABBR = 2160   # 1.5 inches abbreviation tab

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4 width
        section.page_height = Inches(11.69) # A4 height

    # 100% Strict Monochrome Palette - Zero Blue
    COLOR_BLACK = RGBColor(0x00, 0x00, 0x00)
    COLOR_DARK = RGBColor(0x1A, 0x1A, 0x1A)      # Charcoal
    COLOR_MUTED = RGBColor(0x33, 0x33, 0x33)     # Dark Neutral

    # Clean Table Tokens
    HEX_NORMAL_HDR_BG = "EFEFEF"   # Standard light gray header
    HEX_NORMAL_ALT_BG = "FAFAFA"   # Clean alternating row
    HEX_NORMAL_BORDER = "888888"   # Standard clean border
    HEX_ALGO_BG = "F8F9FA"         # Light background for algorithm

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = COLOR_BLACK

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def prevent_row_split(row):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    def set_repeat_header(row):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    def set_table_borders(table, color=HEX_NORMAL_BORDER, sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_chapter_heading(title_text, chapter_number=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(22)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.keep_with_next = True
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        if chapter_number is not None:
            r1 = p.add_run(f"CHAPTER {chapter_number}\n")
            r1.font.name = 'Times New Roman'
            r1.font.size = Pt(16)
            r1.bold = True
            r1.font.color.rgb = COLOR_BLACK
            
        r2 = p.add_run(title_text.upper())
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(15)
        r2.bold = True
        r2.font.color.rgb = COLOR_BLACK
        return p

    def add_sec_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True
        r.font.color.rgb = COLOR_BLACK
        return p

    def add_sec_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        r.italic = True
        r.font.color.rgb = COLOR_DARK
        return p

    def add_body_p(text, bold_prefix="", space_after=7, space_before=2, line_spacing=1.45, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
            r_pre.bold = True
            r_pre.font.color.rgb = COLOR_BLACK
            
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.italic = italic
        r.font.color.rgb = COLOR_BLACK
        return p

    def add_list_item(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.35
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(11.5)
            r_pre.bold = True
            r_pre.font.color.rgb = COLOR_BLACK
            
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.font.color.rgb = COLOR_BLACK
        return p

    def add_figure_item(image_path, caption_text, width_inches=5.6):
        if os.path.exists(image_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            run_img = p_img.add_run()
            run_img.add_picture(image_path, width=Inches(width_inches))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(14)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10.5)
            r_cap.bold = True
            r_cap.italic = True
            r_cap.font.color.rgb = COLOR_DARK

    def add_equation_block(eq_image_path, eq_number_str, title_str, meaning_str, vars_dict, why_str):
        p_eq = doc.add_paragraph()
        p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.paragraph_format.space_before = Pt(10)
        p_eq.paragraph_format.space_after = Pt(3)
        p_eq.paragraph_format.keep_with_next = True
        
        if os.path.exists(eq_image_path):
            run_img = p_eq.add_run()
            run_img.add_picture(eq_image_path, width=Inches(4.6))
            
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(6)
        p_cap.paragraph_format.keep_with_next = True
        r_num = p_cap.add_run(f"Equation ({eq_number_str}): {title_str}")
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(11)
        r_num.bold = True
        r_num.font.color.rgb = COLOR_BLACK

        # Structured plain-English explanation card
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="CCCCCC", sz="4", val="single")
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.0)
        set_cell_background(cell, "FAFAFA")
        set_cell_margins(cell, top=90, bottom=90, left=130, right=130)
        prevent_row_split(tbl.rows[0])

        p_desc = cell.paragraphs[0]
        p_desc.paragraph_format.space_after = Pt(3)
        p_desc.paragraph_format.line_spacing = 1.3
        r1 = p_desc.add_run("• What this formula calculates: ")
        r1.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        r2 = p_desc.add_run(meaning_str + "\n")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)

        r3 = p_desc.add_run("• Variable Breakdown: ")
        r3.bold = True
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(10)
        var_items = [f"{k} = {v}" for k, v in vars_dict.items()]
        r4 = p_desc.add_run("; ".join(var_items) + "\n")
        r4.font.name = 'Times New Roman'
        r4.font.size = Pt(10)

        r5 = p_desc.add_run("• Practical Importance: ")
        r5.bold = True
        r5.font.name = 'Times New Roman'
        r5.font.size = Pt(10)
        r6 = p_desc.add_run(why_str)
        r6.font.name = 'Times New Roman'
        r6.font.size = Pt(10)

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(8)

    def add_normal_table(headers, data, col_widths, caption_text=""):
        if caption_text:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(12)
            p_cap.paragraph_format.space_after = Pt(5)
            p_cap.paragraph_format.keep_with_next = True
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(11)
            r_cap.bold = True
            r_cap.font.color.rgb = COLOR_BLACK

        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color=HEX_NORMAL_BORDER, sz="4", val="single")

        # Header Row
        hdr_row = table.rows[0]
        set_repeat_header(hdr_row)
        prevent_row_split(hdr_row)

        for i, title in enumerate(headers):
            cell = hdr_row.cells[i]
            cell.width = col_widths[i]
            set_cell_background(cell, HEX_NORMAL_HDR_BG)
            set_cell_margins(cell, top=100, bottom=100, left=130, right=130)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(title)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)
            r.bold = True
            r.font.color.rgb = COLOR_BLACK

        # Data Rows
        for r_idx, row_data in enumerate(data):
            row = table.rows[r_idx + 1]
            prevent_row_split(row)
            bg_color = HEX_NORMAL_ALT_BG if r_idx % 2 == 1 else "FFFFFF"

            for c_idx, val in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.width = col_widths[c_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=85, bottom=85, left=120, right=120)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.25
                
                if c_idx == 0 and len(headers) > 2 and len(val) < 25:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif "%" in val or val.replace(".", "").isdigit() or "ms" in val or "USD" in val or "$" in val or "INR" in val:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

                r = p.add_run(val)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
                r.font.color.rgb = COLOR_BLACK

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(2)
        p_after.paragraph_format.space_after = Pt(10)

    # Helper for Non-Table List of Tables / Figures / TOC with Dot Leaders
    def add_dot_leader_line(title_text, page_str, is_bold=False, indent_spaces=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.35
        pPr = p._p.get_or_add_pPr()
        tabs = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:leader="dot" w:pos="{TAB_STOP_RIGHT}"/></w:tabs>')
        pPr.append(tabs)

        prefix = "    " * indent_spaces
        r1 = p.add_run(prefix + title_text)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        if is_bold:
            r1.bold = True
        r1.font.color.rgb = COLOR_BLACK

        r2 = p.add_run(f"\t{page_str}")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        if is_bold:
            r2.bold = True
        r2.font.color.rgb = COLOR_BLACK
        return p

    def add_dot_leader_header(left_title="TITLE", right_title="PAGE NO."):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(8)
        pPr = p._p.get_or_add_pPr()
        tabs = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:pos="{TAB_STOP_RIGHT}"/></w:tabs>')
        pPr.append(tabs)

        r1 = p.add_run(left_title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11.5)
        r1.bold = True
        r1.font.color.rgb = COLOR_BLACK

        r2 = p.add_run(f"\t{right_title}")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11.5)
        r2.bold = True
        r2.font.color.rgb = COLOR_BLACK

    print("Synthesizing Full Academic Project Report with Tabbed TOC/LOT/LOF/Abbr & Clean Spacing...")

    # ==========================================
    # FRONT MATTER: COVER PAGE
    # ==========================================
    tbl_hdr = doc.add_table(rows=1, cols=3)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_hdr, color="FFFFFF", sz="0", val="none")
    prevent_row_split(tbl_hdr.rows[0])

    c_left, c_mid, c_right = tbl_hdr.rows[0].cells
    c_left.width = Inches(1.15)
    c_mid.width = Inches(3.72)
    c_right.width = Inches(1.15)

    # Left Logo: Anna University Crest
    p_left = c_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_left.paragraph_format.space_before = Pt(4)
    p_left.paragraph_format.space_after = Pt(0)
    if os.path.exists("extracted_header_logos/col_0_image1.jpeg"):
        p_left.add_run().add_picture("extracted_header_logos/col_0_image1.jpeg", width=Inches(1.0))
    elif os.path.exists("template_images/image1.jpeg"):
        p_left.add_run().add_picture("template_images/image1.jpeg", width=Inches(1.0))

    # Center: Project Title
    p_mid = c_mid.paragraphs[0]
    p_mid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid.paragraph_format.space_before = Pt(4)
    p_mid.paragraph_format.space_after = Pt(0)
    p_mid.paragraph_format.line_spacing = 1.25
    r_tit = p_mid.add_run("QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)")
    r_tit.font.name = 'Times New Roman'
    r_tit.font.size = Pt(13.5)
    r_tit.bold = True
    r_tit.font.color.rgb = COLOR_BLACK

    # Right Logo: Sona College of Technology Banner
    p_right = c_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_right.paragraph_format.space_before = Pt(12)
    p_right.paragraph_format.space_after = Pt(0)
    if os.path.exists("extracted_header_logos/col_2_image2.jpeg"):
        p_right.add_run().add_picture("extracted_header_logos/col_2_image2.jpeg", width=Inches(1.15))
    elif os.path.exists("template_images/image2.jpeg"):
        p_right.add_run().add_picture("template_images/image2.jpeg", width=Inches(1.15))

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(38)
    p_rep.paragraph_format.space_after = Pt(4)
    r = p_rep.add_run("A Project Report")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True
    r.italic = True
    r.font.color.rgb = COLOR_BLACK

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(22)
    r = p_course.add_run("U23ITP401 – MINI PROJECT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12.5)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(10)
    r = p_sub.add_run("Submitted by")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    r.italic = True
    r.font.color.rgb = COLOR_BLACK

    table_cand = doc.add_table(rows=3, cols=2)
    table_cand.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_cand, color="FFFFFF", sz="0", val="none")
    cand_data = [
        ("SABARI KARTHICK A", "(61782323104056)"),
        ("SIVANARASIMMAN S", "(61782323104059)"),
        ("SUJEETH Y R", "(61782323104051)")
    ]
    for idx, (name, regno) in enumerate(cand_data):
        row = table_cand.rows[idx]
        prevent_row_split(row)
        c1, c2 = row.cells
        c1.width = Inches(2.8)
        c2.width = Inches(2.2)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(name)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.bold = True
        r1.font.color.rgb = COLOR_BLACK

        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_after = Pt(3)
        r2 = p2.add_run(regno)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)
        r2.bold = True
        r2.font.color.rgb = COLOR_BLACK

    p_award = doc.add_paragraph()
    p_award.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_award.paragraph_format.space_before = Pt(28)
    p_award.paragraph_format.space_after = Pt(2)
    r = p_award.add_run("in partial fulfillment for the award of the degree\nof")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.italic = True
    r.font.color.rgb = COLOR_BLACK

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(6)
    p_deg.paragraph_format.space_after = Pt(2)
    r = p_deg.add_run("BACHELOR OF TECHNOLOGY")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    p_in = doc.add_paragraph()
    p_in.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_in.paragraph_format.space_after = Pt(2)
    r = p_in.add_run("in")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.italic = True
    r.font.color.rgb = COLOR_BLACK

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(30)
    r = p_dept.add_run("DEPARTMENT OF INFORMATION TECHNOLOGY /\nARTIFICIAL INTELLIGENCE AND DATA SCIENCE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    p_coll = doc.add_paragraph()
    p_coll.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_coll.paragraph_format.space_after = Pt(2)
    r = p_coll.add_run("SONA COLLEGE OF TECHNOLOGY (AUTONOMOUS), SALEM – 636 005")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_after = Pt(2)
    r = p_univ.add_run("ANNA UNIVERSITY: CHENNAI 600 025")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    p_month = doc.add_paragraph()
    p_month.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_month.paragraph_format.space_before = Pt(8)
    r = p_month.add_run("OCTOBER 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # ==========================================
    # BONAFIDE CERTIFICATE
    # ==========================================
    p_c_coll = doc.add_paragraph()
    p_c_coll.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c_coll.paragraph_format.space_before = Pt(6)
    p_c_coll.paragraph_format.space_after = Pt(2)
    r = p_c_coll.add_run("SONA COLLEGE OF TECHNOLOGY (AUTONOMOUS)\nANNA UNIVERSITY: CHENNAI – 600 025")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    if os.path.exists("template_images/image1.jpeg"):
        p_logo_c = doc.add_paragraph()
        p_logo_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo_c.paragraph_format.space_before = Pt(4)
        p_logo_c.paragraph_format.space_after = Pt(6)
        p_logo_c.add_run().add_picture("template_images/image1.jpeg", width=Inches(1.05))

    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(6)
    p_cert_title.paragraph_format.space_after = Pt(16)
    r = p_cert_title.add_run("BONAFIDE CERTIFICATE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    add_body_p(
        "Certified that this Project titled “QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)” is the bonafide work of “SABARI KARTHICK A (61782323104056), SIVANARASIMMAN S (61782323104059), SUJEETH Y R (61782323104051)” who carried out the project work Course Code & Course Name U23ITP401 – MINI PROJECT under my supervision.",
        space_after=24,
        line_spacing=1.45
    )

    tbl_sig = doc.add_table(rows=6, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_sig, color="FFFFFF", sz="0", val="none")
    sig_info = [
        ("Signature of the Supervisor", "Head of the Department"),
        ("Mrs. J. Deepika, M.E., (Ph.D.)", "Dr. J. Akilandeswari, M.E., Ph.D."),
        ("Assistant Professor", "Professor & Head"),
        ("Department of Information Technology", "Department of Information Technology"),
        ("Sona College of Technology,", "Sona College of Technology,"),
        ("Salem – 636 005", "Salem – 636 005")
    ]
    for idx, (left, right) in enumerate(sig_info):
        row = tbl_sig.rows[idx]
        prevent_row_split(row)
        c1, c2 = row.cells
        c1.width = Inches(3.0)
        c2.width = Inches(3.0)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(left)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_BLACK
        if idx == 0 or idx == 1:
            r1.bold = True

        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(1)
        r2 = p2.add_run(right)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_BLACK
        if idx == 0 or idx == 1:
            r2.bold = True

    p_viva = doc.add_paragraph()
    p_viva.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_viva.paragraph_format.space_before = Pt(30)
    p_viva.paragraph_format.space_after = Pt(36)
    r = p_viva.add_run("Submitted for the Project Viva-Voce Examination held on ____________________")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11.5)
    r.font.color.rgb = COLOR_BLACK

    tbl_exam = doc.add_table(rows=1, cols=2)
    tbl_exam.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_exam, color="FFFFFF", sz="0", val="none")
    prevent_row_split(tbl_exam.rows[0])
    c1, c2 = tbl_exam.rows[0].cells
    c1.width = Inches(3.0)
    c2.width = Inches(3.0)
    p1 = c1.paragraphs[0]
    r1 = p1.add_run("INTERNAL EXAMINER")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    r1.bold = True
    r1.font.color.rgb = COLOR_BLACK

    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = p2.add_run("EXTERNAL EXAMINER")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.bold = True
    r2.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # ==========================================
    # DECLARATION & ACKNOWLEDGEMENT
    # ==========================================
    add_chapter_heading("DECLARATION")

    add_body_p(
        "We hereby declare that the project work entitled “QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)” submitted to ANNA UNIVERSITY, CHENNAI, in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology in Information Technology / Artificial Intelligence and Data Science, is a record of original research work done by us under the supervision and guidance of Mrs. J. Deepika, Assistant Professor, Department of Information Technology, Sona College of Technology, Salem.",
        space_after=14,
        line_spacing=1.45
    )
    add_body_p(
        "We further declare that this project report has not been submitted previously in part or in full to any other University or Institution for the award of any degree, diploma, fellowship, or other similar titles.",
        space_after=32,
        line_spacing=1.45
    )

    tbl_dec = doc.add_table(rows=4, cols=2)
    tbl_dec.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_dec, color="FFFFFF", sz="0", val="none")
    c_p1, c_p2 = tbl_dec.rows[0].cells
    c_p1.width = Inches(3.0)
    c_p2.width = Inches(3.0)
    p = c_p1.paragraphs[0]
    r_dec = p.add_run("Place: Salem\nDate: 04-10-2026")
    r_dec.font.name = 'Times New Roman'
    r_dec.font.color.rgb = COLOR_BLACK

    dec_members = [
        "1. SABARI KARTHICK A (61782323104056)",
        "2. SIVANARASIMMAN S (61782323104059)",
        "3. SUJEETH Y R (61782323104051)"
    ]
    for i, mem in enumerate(dec_members):
        row = tbl_dec.rows[i+1]
        prevent_row_split(row)
        cell = row.cells[1]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(mem)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.bold = True
        r.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    add_chapter_heading("ACKNOWLEDGEMENT")
    add_body_p("First and foremost, we express our profound gratitude to the Almighty for showering his immense blessings upon us throughout the successful completion of this project.", space_after=12)
    add_body_p("We extend our heartfelt gratitude to our Chairman, Vice-Chairmen, and Executive Director for providing exceptional state-of-the-art laboratory and computing infrastructure.", space_after=12)
    add_body_p("We express our deep sense of gratitude and sincere thanks to our respected Principal, Dr. S. R. R. Senthil Kumar, for his continuous encouragement and academic support throughout our course of study.", space_after=12)
    add_body_p("We are highly indebted and express our sincere thanks to Dr. J. Akilandeswari, Professor & Head, Department of Information Technology, for her invaluable guidance, visionary encouragement, and academic leadership.", space_after=12)
    add_body_p("We express our deepest sense of gratitude, respect, and indebtedness to our esteemed Project Supervisor, Mrs. J. Deepika, Assistant Professor, Department of Information Technology, whose profound technical insights, constant inspiration, constructive critiques, and meticulous guidance made this research possible.", space_after=12)
    add_body_p("We also convey our gratitude to all teaching and non-teaching faculty members of the Department of Information Technology, the veterinary clinicians who offered clinical feedback during field validation, and our loving parents and peers for their unwavering moral and emotional support.", space_after=16)

    doc.add_page_break()

    # ==========================================
    # ABSTRACT
    # ==========================================
    add_chapter_heading("ABSTRACT")
    add_body_p(
        "The smallholder dairy farming sector is a critical socio-economic pillar in rural developing economies, supporting over 150 million farming households worldwide. However, livestock health management on a small scale is severely limited by delayed disease detection, reliance on subjective manual inspection, and the exorbitant cost of commercial wearable Internet of Things (IoT) sensors ($150–$350 per animal). This economic divide leaves smallholder farmers vulnerable to subclinical diseases such as mastitis, ketosis, and bovine respiratory disease (BRD), which cause severe milk yield collapses and reproductive losses before visible symptoms emerge.",
        space_after=12,
        line_spacing=1.45
    )
    add_body_p(
        "To solve this critical bottleneck, this project presents the proposed system: an AI-powered, zero-hardware-cost livestock health management platform based on weatherproof Quick Response (QR) matrices and a multi-stage analytical engine called the Composite Health Deviation Index (CHDI). In this framework, cattle are identified via low-cost laser-etched thermoplastic polyurethane (TPU) ear tags scanned by standard commodity smartphones. Daily physiological and production observations (milk yield, core temperature, rumination duration, activity counts, and feed consumption) are ingested and analyzed through a dedicated three-stage mathematical engine.",
        space_after=12,
        line_spacing=1.45
    )
    add_body_p(
        "Stage 1 establishes an individualized, rolling longitudinal baseline for each animal using sample variance with Bessel's correction, eliminating population-wide bias. Stage 2 computes a robust multivariate anomaly score using Tikhonov-regularized Mahalanobis distance, capturing subtle coupled covariance shifts indicative of pre-clinical pathophysiology while preventing matrix singularity. Stage 3 provides local explainability using Leave-One-Covariate-Out (LOCO) permutation feature attribution and incorporates supervised veterinary clinical diagnostic feedback to refine predictive accuracy over time.",
        space_after=12,
        line_spacing=1.45
    )
    add_body_p(
        "The platform is architected as an edge-first full-stack application using Next.js 14, TypeScript, Server Actions, PostgreSQL on Neon serverless infrastructure, and a Python FastAPI ML microservice. Empirical validation on a longitudinal dataset comprising 120 dairy cattle across 18 smallholder farms demonstrated that the proposed system achieves an overall anomaly detection sensitivity of 93.8%, specificity of 96.2%, and an AUC-ROC of 0.958. Crucially, the system detected subclinical mastitis and metabolic anomalies 24 to 48 hours prior to acute clinical symptoms, while reducing the per-animal monitoring cost to under $0.50 (a 99.7% reduction compared to wearable IoT solutions), establishing an accessible precision livestock management paradigm for smallholder farmers.",
        space_after=14,
        line_spacing=1.45
    )
    add_body_p(
        "Keywords: Precision Livestock Farming, QR Code Identification, Composite Health Deviation Index (CHDI), Multivariate Mahalanobis Distance, Tikhonov Regularization, Explainable AI, Veterinary Triage.",
        bold_prefix="Keywords: ",
        italic=True
    )

    doc.add_page_break()

    # ==========================================
    # PRELIMINARY LISTS (NON-TABLE FORMAT WITH DOT LEADERS)
    # ==========================================
    add_chapter_heading("TABLE OF CONTENTS")
    add_dot_leader_header("TOPIC / CHAPTER TITLE", "PAGE NO.")

    toc_structure = [
        ("BONAFIDE CERTIFICATE", "ii", True, 0),
        ("DECLARATION", "iii", True, 0),
        ("ACKNOWLEDGEMENT", "iv", True, 0),
        ("ABSTRACT", "v", True, 0),
        ("LIST OF TABLES", "vii", True, 0),
        ("LIST OF FIGURES", "viii", True, 0),
        ("LIST OF ABBREVIATIONS", "ix", True, 0),
        ("CHAPTER 1: INTRODUCTION", "1", True, 0),
        ("1.1 Background of Smallholder Dairy Healthcare", "1", False, 1),
        ("1.2 Challenges in Conventional Livestock Monitoring", "2", False, 1),
        ("1.3 Motivation & Research Gaps in Precision Dairy Farming", "3", False, 1),
        ("1.4 Problem Statement", "4", False, 1),
        ("1.5 Objectives of the Project", "4", False, 1),
        ("1.6 Scope and Contributions", "5", False, 1),
        ("1.7 Overview of the Proposed Approach", "6", False, 1),
        ("1.8 Organisation of the Report", "7", False, 1),
        ("CHAPTER 2: LITERATURE REVIEW", "8", True, 0),
        ("2.1 Information, Communication and Networking Systems in PLF", "8", False, 1),
        ("2.2 Sensors and Physiological Monitoring for Wearable IoT Devices", "9", False, 1),
        ("2.3 Computer Vision and Optical Identification Systems", "10", False, 1),
        ("2.4 Digital Platforms and Veterinary Health Records", "11", False, 1),
        ("2.5 Summary of the Literature and Research Gap", "12", False, 1),
        ("2.6 Feature Comparison: Proposed System vs. Related Approaches", "13", False, 1),
        ("CHAPTER 3: EXISTING SYSTEM VS PROPOSED SYSTEM", "14", True, 0),
        ("3.1 Existing Techniques in Cattle Health Monitoring", "14", False, 1),
        ("3.2 Advantages and Disadvantages of Existing Techniques", "15", False, 1),
        ("3.3 Proposed Technique: SmartCattle QR & CHDI Platform", "17", False, 1),
        ("3.4 How SmartCattle Overcomes Existing Limitations", "18", False, 1),
        ("3.5 System Feasibility Analysis (Technical, Economic, Operational)", "19", False, 1),
        ("CHAPTER 4: PROPOSED FRAMEWORK, ARCHITECTURE AND IMPLEMENTATION", "21", True, 0),
        ("4.1 Overview of the SmartCattle Framework", "21", False, 1),
        ("4.2 System Architecture and Threat / Data Integrity Model", "22", False, 1),
        ("4.3 Four-Tier Architectural Subsystems", "24", False, 1),
        ("4.4 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)", "26", False, 1),
        ("4.5 Mathematical Formulation of the CHDI Analytical Engine", "28", False, 1),
        ("4.5.1 Stage 1: Individual Baseline Calibration (Equations 4.1, 4.2, 4.3)", "28", False, 2),
        ("4.5.2 Stage 2: Regularized Mahalanobis Distance (Equations 4.4, 4.5, 4.6)", "30", False, 2),
        ("4.5.3 Stage 3: LOCO Feature Attribution (Equations 4.7, 4.8, 4.9)", "32", False, 2),
        ("4.5.4 CHDI Clinical Severity Bands and Action Protocols", "34", False, 2),
        ("4.6 Database Design & Prisma Schema Entities", "35", False, 1),
        ("4.7 Technology Stack of the Prototype", "37", False, 1),
        ("4.8 Core Algorithmic Procedures & Pseudocode (Algorithm 4.1)", "38", False, 1),
        ("4.9 Source Code Listings & Implementations", "40", False, 1),
        ("CHAPTER 5: EXPERIMENTAL RESULTS AND DISCUSSION", "42", True, 0),
        ("5.1 Experimental Setup & Benchmark Cohort Provenance", "42", False, 1),
        ("5.2 Evaluation Metrics", "43", False, 1),
        ("5.3 Detection and Diagnostic Results Across Bovine Conditions", "44", False, 1),
        ("5.4 Longitudinal Clinical Case Trace & Explainability Walkthrough", "46", False, 1),
        ("5.5 Algorithmic Ablation Study", "48", False, 1),
        ("5.6 Predictive Lead Time & Early Intervention Advantage", "49", False, 1),
        ("5.7 Response Time, Computational Latency and Edge Footprint", "50", False, 1),
        ("5.8 Benchmarking with Commercial Wearable IoT Platforms", "51", False, 1),
        ("5.9 Limitations of the Evaluation", "52", False, 1),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", "53", True, 0),
        ("6.1 Conclusion", "53", False, 1),
        ("6.2 Summary of Key Contributions", "54", False, 1),
        ("6.3 Future Scope", "55", False, 1),
        ("REFERENCES", "56", True, 0),
        ("APPENDIX", "58", True, 0),
        ("A.1 Summary of Mathematical Notation", "58", False, 1),
        ("A.2 Evaluation Protocol Summary", "59", False, 1),
        ("A.3 Reproducibility Checklist", "60", False, 1)
    ]

    for title, pg, is_b, ind in toc_structure:
        add_dot_leader_line(title, pg, is_bold=is_b, indent_spaces=ind)

    doc.add_page_break()

    # LIST OF TABLES (NON-TABLE FORMAT)
    add_chapter_heading("LIST OF TABLES")
    add_dot_leader_header("TABLE NO. & TITLE", "PAGE NO.")

    lot_items = [
        ("Table 2.1  Feature Comparison: Proposed System vs. Related Approaches", "13"),
        ("Table 3.1  Comparison of Existing Cattle Healthcare Techniques", "16"),
        ("Table 3.2  System Feasibility Analysis Matrix for SmartCattle Deployment", "20"),
        ("Table 4.1  CHDI Severity Bands, Score Ranges, and Clinical Protocols", "34"),
        ("Table 4.2  Prisma Database Schema Entities and Relational Mappings", "36"),
        ("Table 4.3  Technology Stack of the SmartCattle Research Prototype", "37"),
        ("Table 4.4  Core Algorithmic Procedures of the SmartCattle CHDI Framework", "39"),
        ("Table 5.1  Benchmark Experimental Cohort Breakdown and Ground Truth", "43"),
        ("Table 5.2  Diagnostic Performance Metrics for Common Bovine Pathologies", "45"),
        ("Table 5.3  Anomaly Detection Performance Metrics & Algorithmic Ablation", "48"),
        ("Table 5.4  Subclinical Disease Lead Time and Early Intervention Advantage", "49"),
        ("Table 5.5  End-to-End Latency and Computational Footprint Breakdown", "50"),
        ("Table 5.6  Benchmarking SmartCattle against Commercial Wearable IoT Solutions", "51"),
        ("Table A.1  Summary of Mathematical Notations and Variable Definitions", "58")
    ]
    for item_tit, pg in lot_items:
        add_dot_leader_line(item_tit, pg, is_bold=False, indent_spaces=0)

    doc.add_page_break()

    # LIST OF FIGURES (NON-TABLE FORMAT)
    add_chapter_heading("LIST OF FIGURES")
    add_dot_leader_header("FIGURE NO. & TITLE", "PAGE NO.")

    lof_items = [
        ("Figure 4.1  Multi-Tier System Architecture of the Proposed QR-Based Platform", "23"),
        ("Figure 4.2  Three-Stage CHDI Analytics Engine Operational Workflow", "25"),
        ("Figure 4.3  Level 0 Context Diagram (DFD Level 0) for SmartCattle Platform", "26"),
        ("Figure 4.4  Level 1 Data Flow Diagram (DFD Level 1) for Telemetry Ingestion", "27"),
        ("Figure 5.1  Cohort Herd Status and Risk Distribution Breakdown across Trial", "46"),
        ("Figure 5.2  Longitudinal CHDI Score Trajectory Demonstrating Pre-Clinical Lead Time", "47"),
        ("Figure 5.3  Leave-One-Covariate-Out (LOCO) Feature Attribution Ranking", "48")
    ]
    for item_tit, pg in lof_items:
        add_dot_leader_line(item_tit, pg, is_bold=False, indent_spaces=0)

    doc.add_page_break()

    # LIST OF ABBREVIATIONS (NON-TABLE FORMAT)
    add_chapter_heading("LIST OF ABBREVIATIONS")
    
    p_abh = doc.add_paragraph()
    p_abh.paragraph_format.space_before = Pt(8)
    p_abh.paragraph_format.space_after = Pt(8)
    p_abhPr = p_abh._p.get_or_add_pPr()
    tabs_abh = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="left" w:pos="{TAB_STOP_ABBR}"/></w:tabs>')
    p_abhPr.append(tabs_abh)
    r1 = p_abh.add_run("ABBREVIATION")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11.5)
    r1.bold = True
    r1.font.color.rgb = COLOR_BLACK
    r2 = p_abh.add_run("\tEXPANSION / DESCRIPTION")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11.5)
    r2.bold = True
    r2.font.color.rgb = COLOR_BLACK

    abbr_items = [
        ("AI", "Artificial Intelligence"),
        ("AMS", "Automated Milking System"),
        ("AUC-ROC", "Area Under the Receiver Operating Characteristic Curve"),
        ("BHBA", "Beta-Hydroxybutyrate"),
        ("BRD", "Bovine Respiratory Disease"),
        ("CHDI", "Composite Health Deviation Index"),
        ("CMT", "California Mastitis Test"),
        ("EMA", "Exponential Moving Average"),
        ("IoT", "Internet of Things"),
        ("LOCO", "Leave-One-Covariate-Out"),
        ("LSTM", "Long Short-Term Memory"),
        ("mAP", "Mean Average Precision"),
        ("ORM", "Object-Relational Mapping"),
        ("PLF", "Precision Livestock Farming"),
        ("QR", "Quick Response"),
        ("RBAC", "Role-Based Access Control"),
        ("SCC", "Somatic Cell Count"),
        ("TPU", "Thermoplastic Polyurethane"),
        ("UUID", "Universally Unique Identifier"),
        ("YOLO", "You Only Look Once")
    ]

    for a, d in abbr_items:
        p_ab = doc.add_paragraph()
        p_ab.paragraph_format.space_before = Pt(2)
        p_ab.paragraph_format.space_after = Pt(4)
        p_ab.paragraph_format.line_spacing = 1.35
        pPr = p_ab._p.get_or_add_pPr()
        tabs = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="left" w:pos="{TAB_STOP_ABBR}"/></w:tabs>')
        pPr.append(tabs)

        r_a = p_ab.add_run(a)
        r_a.font.name = 'Times New Roman'
        r_a.font.size = Pt(11)
        r_a.bold = True
        r_a.font.color.rgb = COLOR_BLACK

        r_d = p_ab.add_run(f"\t{d}")
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(11)
        r_d.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    add_chapter_heading("INTRODUCTION", chapter_number=1)

    add_sec_heading_2("1.1 Background of Smallholder Dairy Healthcare")
    add_body_p("Livestock farming and dairy production constitute the socio-economic backbone of rural agrarian economies across the developing world, supporting over 150 million smallholder households worldwide. In India, the dairy sector contributes approximately 4.5% to the national Gross Domestic Product (GDP), serving as a vital buffer against crop failure caused by climatic volatility. The national bovine population exceeds 300 million head of cattle and buffaloes, making India the largest milk-producing nation globally.")
    add_body_p("Unlike large-scale industrial dairy farms in North America and Western Europe, where thousands of cattle are managed in climate-controlled barns using automated milking parlors, more than 85% of dairy production in developing agrarian nations is distributed across smallholder farmers maintaining modest herds of 2 to 10 cattle. In these settings, livestock are typically managed in tie-stalls or semi-intensive grazing systems.")

    add_sec_heading_2("1.2 Challenges in Conventional Livestock Monitoring")
    add_body_p("Smallholder livestock health management is constrained by structural, economic, and logistical factors:")
    add_list_item("1. Delayed Clinical Detection:", "Farmers rely almost exclusively on visual observation during milking and feeding routines. By the time visual symptoms appear—such as severe udder swelling in clinical mastitis, severe lethargy in ketosis, or nasal discharge in bovine respiratory disease—the underlying pathophysiological damage is already advanced, causing irreversible tissue scarring and long-term milk yield decline.")
    add_list_item("2. Subclinical Disease Losses:", "Subclinical diseases represent an invisible financial drain. Subclinical mastitis reduces per-cow daily milk production by 15% to 30% without visible changes in milk appearance, causing an estimated annual loss exceeding $1.5 billion USD in the Indian dairy sector.")
    add_list_item("3. Missed Estrus Cycles:", "Undetected estrus cycles lead to missed artificial insemination windows, extending calving intervals by 40 to 90 days and imposing high non-productive feeding costs.")
    add_list_item("4. Disconnected Veterinary Support:", "Rural veterinary surgeons cover vast geographical clusters, visiting farms only upon emergency callouts rather than for early-stage preventive triage.")

    add_sec_heading_2("1.3 Motivation & Research Gaps in Precision Dairy Farming")
    add_body_p("The advent of Precision Livestock Farming (PLF) has spurred extensive academic and commercial development in wearable electronic biosensors, including collar-mounted 3D accelerometers (e.g., SCR CowManager), intra-rumen telemetry boluses (e.g., smaXtec), and leg pedometers (e.g., Afimilk AfiAct). While these wearable devices provide continuous real-time telemetry, they present three fundamental barriers when applied to smallholder farming:")
    add_list_item("Prohibitive Capital Outlay ($150–$350 per cow):", "Equipping a modest 4-cow herd with commercial sensor collars costs between $600 and $1,400 USD, exceeding the farmer's entire net annual agricultural income.")
    add_list_item("High Hardware Damage & Battery Overhead:", "Physical collisions, tag detachment, and finite battery lifespans (3–5 years) impose recurring replacement costs that smallholders cannot afford.")
    add_list_item("Population-Wide Heuristic Thresholding:", "Existing systems apply rigid global population thresholds that fail to account for individual biological baselines, breed variations, and lactation parities, causing high false alarm rates and alarm fatigue.")
    add_body_p("Therefore, an urgent imperative exists to develop a zero-hardware-cost, non-invasive platform that leverages ubiquitous commodity smartphones and physical QR tags to deliver personalized, longitudinal health intelligence for smallholder dairy farmers.")

    add_sec_heading_2("1.4 Problem Statement")
    add_body_p("Smallholder dairy farmers lack cost-effective, non-invasive, and early-stage diagnostic tools to detect subclinical bovine health anomalies before they escalate into acute clinical disease, irreversible milk production collapse, or reproductive failure. Existing wearable IoT sensor platforms impose exorbitant financial and technical overheads that render them inaccessible to the smallholder agrarian sector.")
    add_body_p("Furthermore, existing software management applications rely on crude population-wide statistical thresholds that generate high false alarm rates due to natural biological variations across individual cattle, lactation stages, and diurnal cycles. Consequently, there is an acute need for an intelligent livestock health management platform that operates without dedicated on-animal electronics, provides individual-calibrated longitudinal anomaly detection, and delivers actionable, explainable clinical triage for farmers and rural veterinarians.")

    add_sec_heading_2("1.5 Objectives of the Project")
    add_body_p("The specific technical objectives of this project are as follows:")
    add_list_item("1. Physical QR Identification:", "To design a secure, zero-hardware edge identification framework using laser-etched TPU QR ear tags containing cryptographic UUIDs, decoded via standard mobile smartphone browsers without dedicated app installation.")
    add_list_item("2. Individual Adaptive Baseline Calibration:", "To develop an automated longitudinal baseline calibration algorithm utilizing rolling moving averages with Bessel's correction to eliminate population-wide bias.")
    add_list_item("3. Regularized Multivariate Anomaly Scoring:", "To formulate and implement the Composite Health Deviation Index (CHDI) combining Tikhonov-regularized covariance inversion and Mahalanobis distance calculation to detect coupled physiological anomalies.")
    add_list_item("4. Explainable AI & Feature Attribution:", "To build a Leave-One-Covariate-Out (LOCO) permutation attribution engine that quantifies and ranks the exact physiological drivers behind elevated risk scores.")
    add_list_item("5. Closed-Loop Clinical Triage Queue:", "To implement an automated veterinary triage workflow with role-based access control (Farmer, Veterinarian, Admin), instant push notifications, and supervised diagnostic override logging.")
    add_list_item("6. Edge-First Cloud Architecture:", "To engineer an end-to-end full-stack web ecosystem using Next.js 14, React Server Components, TypeScript, Prisma ORM, and a dedicated Python FastAPI ML microservice.")
    add_list_item("7. Empirical Benchmark Validation:", "To validate diagnostic accuracy, early detection lead times (24–48 hours), and latency on a real-world benchmark cohort of 120 dairy cattle across 18 smallholder farms.")

    add_sec_heading_2("1.6 Scope and Contributions")
    add_body_p("The scope of this project is an end-to-end, field-validated livestock health intelligence platform designed explicitly for the resource constraints of smallholder dairy farming. The primary scientific and engineering contributions are:")
    add_list_item("Democratized Precision Livestock Healthcare:", "Elimination of on-animal electronic sensors, reducing the per-cow monitoring cost to under $0.50 (a 99.7% cost reduction compared to commercial IoT collars).")
    add_list_item("Novel Mathematical CHDI Formulation:", "A multi-stage regularized distance formulation that tracks individual physiological homeostasis and prevents matrix singularity during sparse data logging.")
    add_list_item("Transparent LOCO Feature Attribution:", "Actionable clinical interpretability that translates complex multivariate anomaly vectors into plain-language summaries for farmers and veterinarians.")
    add_list_item("Reproducible Benchmark Evaluation:", "Comprehensive longitudinal evaluation across 120 dairy cattle over an 8-week period, achieving 93.8% sensitivity, 96.2% specificity, and a 36.4-hour lead time for subclinical mastitis.")

    add_sec_heading_2("1.7 Overview of the Proposed Approach")
    add_body_p("The proposed system operates as an integrated closed loop connecting edge data acquisition, serverless cloud processing, scientific anomaly detection, and clinical veterinary action. When a farmer scans an animal's weatherproof QR tag using a standard smartphone web browser, the encrypted UUID resolves the animal's identity without requiring native app installation. The farmer logs daily routine observations (milk yield, core body temperature, rumination duration, activity counts, feed intake).")
    add_body_p("The ingested telemetry vector is processed by the CHDI analytical engine. Stage 1 estimates personalized baseline means and variances. Stage 2 applies Tikhonov regularization and calculates the multivariate Mahalanobis anomaly distance. Stage 3 computes LOCO feature contributions. If CHDI exceeds clinical alert thresholds (CHDI ≥ 51), automated triage notifications dispatch to regional veterinarians, who review explainable feature rankings and log confirmed diagnoses.")

    add_sec_heading_2("1.8 Organisation of the Report")
    add_body_p("The remainder of this report is structured as follows:")
    add_list_item("Chapter 2:", "Reviews the literature on precision livestock communication systems, wearable IoT sensors, computer vision, and veterinary records, presenting a comprehensive comparison matrix.")
    add_list_item("Chapter 3:", "Examines existing techniques, contrasts their advantages and disadvantages, outlines the proposed system paradigm, and presents a three-dimensional feasibility study.")
    add_list_item("Chapter 4:", "Presents the complete architectural design, DFDs, mathematical formulation, database models, implementation modules, algorithms, and source code listings.")
    add_list_item("Chapter 5:", "Discusses the experimental benchmark results, longitudinal case traces, ablation studies, lead time advantages, latency benchmarks, and commercial comparisons.")
    add_list_item("Chapter 6:", "Concludes the report and outlines future research avenues including offline CRDT synchronization and multilingual voice interfaces.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: LITERATURE REVIEW
    # ==========================================
    add_chapter_heading("LITERATURE REVIEW", chapter_number=2)

    add_sec_heading_2("2.1 Information, Communication and Networking Systems in PLF")
    add_body_p("The digital transformation of agriculture relies on robust Information and Communication Technology (ICT) architectures capable of operating across remote, low-connectivity rural landscapes. Subach and Shmeleva [4] surveyed the digital modernization of livestock farming, emphasizing that cloud-based data pipelines are essential for converting raw on-farm observations into actionable clinical intelligence.")
    add_body_p("Curti et al. [6] formalized precision livestock data flow into a 5-step operational lifecycle: acquisition, transfer, cloud storage, statistical modeling, and decision delivery. In pastoral grazing environments, Barriuso et al. [9] developed a multi-agent Wireless Sensor Network (WSN) architecture using PANGEA orchestration and MQTT messaging. While effective in maintaining distributed telemetry sync, such architectures require local gateway hardware, solar repeaters, and continuous maintenance that exceed smallholder capabilities.")

    add_sec_heading_2("2.2 Sensors and Physiological Monitoring for Wearable IoT Devices")
    add_body_p("Wearable biosensors represent the most extensively researched paradigm in precision dairy healthcare. Kaur and Virk [5] designed an IoT-based neck collar equipped with triaxial accelerometers, digital thermistors, and pulse sensors transmitting data to a Raspberry Pi gateway. Tested across 150 cattle over 2 months in Punjab, India, their system achieved classification accuracies of 92% and 91% using Random Forest and Decision Tree models for BRD and mastitis, respectively.")
    add_body_p("Kamphuis et al. [12] investigated automated mastitis detection using decision trees in automated milking systems, demonstrating that multivariate coupling between milk yield, electrical conductivity, and temperature significantly outperforms single-threshold heuristic rules. Aquilani et al. [7] reviewed PLF technologies across pasture livestock, highlighting walk-over weigh scales, GPS collars, and thermography cameras.")
    add_body_p("Despite their diagnostic capabilities, all wearable platforms suffer from three severe operational failure modes: finite battery life (requiring tag replacement every 3–5 years), physical detachment or crushing caused by animal social interactions, and high unit capital costs ($150–$350/cow) [5], [7].")

    add_sec_heading_2("2.3 Computer Vision and Optical Identification Systems")
    add_body_p("To eliminate expensive electronic tags, non-invasive optical identification techniques have been explored. Bumbálek et al. [3] conducted a comprehensive comparative study evaluating YOLOv8-based body-texture biometric recognition, numerical ear-tag optical character recognition (OCR), and collar-mounted QR codes in dynamic dairy herds.")
    add_body_p("Their experimental results revealed that QR-based identification achieved an mAP50–95 score of 0.71, compared to 0.78 for body texture biometrics and 0.84 for numerical OCR. Crucially, QR identification exhibited a distinct operational advantage: deep CNN weights for biometric texture require retraining when new cattle join the herd, whereas QR matrices use fixed universal decoding standards, allowing instant zero-retraining enrollment. However, Bumbálek et al. noted that optical systems face occlusion from barn mud and variable lighting, underscoring the necessity for durable laser-etched tags and manual search fallbacks [3].")

    add_sec_heading_2("2.4 Digital Platforms and Veterinary Health Records")
    add_body_p("In clinical practice, Ahmad and Salamat [8] developed a web-based veterinary clinic management system at GeBuu Clinic, implementing role-based access control, treatment histories, and automated vaccination reminders to reduce administrative overhead and enhance medical compliance.")
    add_body_p("However, contemporary veterinary software systems operate as purely passive electronic medical record (EMR) repositories. They lack integrated analytical engines capable of modeling historical baselines or detecting subtle multi-signal physiological deviations from sparse, heterogeneous field observations [4], [8]. Existing systems either demand heavy capital investment in specialized IoT hardware [1], [2], [5] or provide passive optical identification without health analytics [3]. The proposed system explicitly bridges this gap.")

    add_sec_heading_2("2.5 Summary of the Literature and Research Gap")
    add_body_p("A critical synthesis of the literature reveals four unaddressed research gaps:")
    add_list_item("1. The Wearable Cost Bottleneck:", "Virtually all state-of-the-art anomaly detection systems assume continuous electronic sensors on every cow, ignoring the economic realities of 150 million smallholder farmers.")
    add_list_item("2. Population Threshold Bias:", "Existing software platforms apply population-wide static thresholds that fail to account for individual baseline differences across breeds and lactation stages.")
    add_list_item("3. Lack of Explainability in Triage:", "Complex deep learning models act as uninterpretable black boxes, outputting opaque risk scores without clinical attribution.")
    add_list_item("4. Native App Installation Friction:", "Native mobile apps require frequent updates, large storage, and app store dependencies that alienate rural smallholder users.")

    add_sec_heading_2("2.6 Feature Comparison: Proposed System vs. Related Approaches")
    add_body_p("Table 2.1 summarizes the key literature across sensing modalities, diagnostic scope, hardware costs, smallholder accessibility, and explainability (IEEE Paper Table I).")

    tbl1_headers = ["Platform / Study", "Identification Mechanism", "Hardware Requirement", "Analytical Engine", "Explainability", "Target Audience"]
    tbl1_data = [
        ["Kaur & Virk [5]", "Wearable Collar Sensor", "High ($150–$250 / cow)", "Random Forest / DT", "None (Black-box)", "Industrial Farms"],
        ["Bumbálek et al. [3]", "YOLOv8 Vision / QR", "Medium (High-res Cameras)", "Object Detection Only", "None (Vision Bounding)", "Large-Scale Herds"],
        ["Kamphuis et al. [12]", "Milking Parlor Sensors", "High ($15,000+ Parlor)", "Decision Tree Rules", "Partial (Rule Splits)", "Robotic Dairies"],
        ["Ahmad & Salamat [8]", "Manual ID / Barcode", "Low (PC / Mobile)", "None (Passive EMR)", "None (Static Records)", "Veterinary Clinics"],
        ["Barriuso et al. [9]", "GPS / ZigBee Collars", "High (WSN Gateways)", "PANGEA Multi-Agent", "None (Agent Rules)", "Pasture Ranches"],
        ["Proposed System", "Laser-Etched QR Ear Tag", "Zero (< $0.50 / tag)", "Three-Stage CHDI (Mahalanobis + Tikhonov)", "Yes (LOCO Feature Attribution)", "Smallholder Farmers & Rural Vets"]
    ]
    add_normal_table(
        tbl1_headers,
        tbl1_data,
        [Inches(1.0), Inches(1.1), Inches(0.9), Inches(1.1), Inches(0.9), Inches(1.0)],
        "Table 2.1: Feature Comparison: Proposed System vs. Related Approaches (IEEE Paper Table I)"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: EXISTING SYSTEM VS PROPOSED SYSTEM
    # ==========================================
    add_chapter_heading("EXISTING SYSTEM VS PROPOSED SYSTEM", chapter_number=3)

    add_sec_heading_2("3.1 Existing Techniques in Cattle Health Monitoring")
    add_body_p("Current approaches to bovine health monitoring fall into four primary categories:")
    
    add_sec_heading_3("3.1.1 Manual Visual Inspection")
    add_body_p("The traditional approach practiced by smallholder farmers. Involves visual inspection of udder swelling, dung consistency, eye discharge, and physical palpation during milking. It is completely non-technical, reactive, highly subjective, and incapable of detecting subclinical disease.")

    add_sec_heading_3("3.1.2 Wearable Collar Sensors & Accelerometers")
    add_body_p("Neck-mounted collars containing triaxial accelerometers and microprocessors to detect rumination chewing patterns and head movements (e.g., SCR CowManager). They provide high accuracy but are extremely expensive and vulnerable to physical damage in rural tie-stalls.")

    add_sec_heading_3("3.1.3 Intra-Rumen Telemetry Boluses")
    add_body_p("Ceramic capsules containing thermistors and battery units orally administered to settle in the reticulum (e.g., smaXtec). Continuously measures internal core temperature. They are non-recoverable after cow mortality, expensive, and subject to water drinking temperature distortions.")

    add_sec_heading_3("3.1.4 Automated Milking System In-Line Sensors")
    add_body_p("Automated robotic milking units equipped with optical sensors, inline electrical conductivity probes, and somatic cell counters. They require massive capital expenditure ($15,000+) and are restricted exclusively to large industrial dairies.")

    add_sec_heading_2("3.2 Advantages and Disadvantages of Existing Techniques")
    add_body_p("A rigorous comparative analysis reveals severe systemic trade-offs between diagnostic granularity and economic accessibility, as delineated in Table 3.1.")

    ex_headers = ["Technique", "Key Advantages", "Critical Disadvantages & Bottlenecks"]
    ex_data = [
        [
            "Manual Observation\n(Smallholder Standard)",
            "• Zero financial investment\n• No technology dependence\n• Deep farmer familiarity",
            "• Detects diseases only at acute clinical stage\n• Cannot detect subclinical mastitis/ketosis\n• Highly subjective and variable\n• High missed estrus rates (>40%)"
        ],
        [
            "Wearable Collar\nSensors [5], [7]\n(e.g., CowManager)",
            "• Continuous 24/7 behavior logging\n• High estrus sensitivity (85–90%)\n• Direct rumination quantification",
            "• Prohibitive capital cost ($150–$250/cow)\n• High tag detachment & physical damage\n• Finite battery lifespan (3–5 years)\n• High recurring software subscription fees"
        ],
        [
            "Reticulorumen\nBoluses [2], [7]\n(e.g., smaXtec)",
            "• Direct core body temperature\n• Protected inside animal body\n• Early fever detection lead time",
            "• Extremely high unit cost ($200–$350/cow)\n• Water drinking temperature distortion\n• Permanent and non-reusable\n• Requires specialized RF base stations"
        ],
        [
            "Automated In-Line\nMilking Sensors [12]\n(e.g., Afimilk AMS)",
            "• Real-time milk conductivity & yield\n• Automated somatic cell estimation\n• Zero human manual data entry",
            "• Massive capital expenditure ($15,000+)\n• Requires permanent milking parlor setup\n• Infeasible for grazing / tie-stall smallholders\n• Extreme maintenance requirements"
        ]
    ]
    add_normal_table(
        ex_headers,
        ex_data,
        [Inches(1.6), Inches(2.1), Inches(2.3)],
        "Table 3.1: Comparison of Existing Cattle Healthcare Techniques (Advantages vs Disadvantages)"
    )

    add_sec_heading_2("3.3 Proposed Technique: Proposed System QR & CHDI Platform")
    add_body_p("To decisively overcome the structural limitations of existing systems, this project introduces the proposed system: an innovative, non-invasive, zero-hardware-cost livestock health intelligence platform designed explicitly for the resource constraints of smallholder dairy agriculture.")
    add_body_p("The proposed system completely eliminates on-animal electronic sensors. Instead, each animal is assigned a weatherproof, laser-etched TPU QR ear tag. The core innovation comprises a three-stage intelligent analytics engine—the Composite Health Deviation Index (CHDI)—operating inside a modern edge-first web application accessible from any standard smartphone browser.")
    add_body_p("During standard morning and evening milking and feeding routines, the farmer scans the cow's QR tag using a smartphone camera. The system instantly authenticates the animal and prompts for routine daily observations (milk yield, core temperature via digital thermometer, estimated rumination duration, activity counts, feed intake). Ingestion requires less than 15 seconds per cow. The ingested telemetry is immediately processed through the CHDI pipeline to generate real-time risk scores, clinical explainability vectors, and automated veterinary alerts.")

    add_sec_heading_2("3.4 How the Proposed System Overcomes Existing Limitations")
    add_body_p("The proposed system fundamentally resolves every key bottleneck present in conventional livestock monitoring systems:")
    add_list_item("1. 99.7% Cost Reduction:", "By utilizing passive printed QR tags ($0.10–$0.50) instead of $200 wearable hardware, the financial barrier is eliminated, making precision dairy technology instantly viable for even single-cow households.")
    add_list_item("2. Individual-Calibrated Baseline Modeling:", "Unlike rigid population thresholding, the proposed system builds an individualized longitudinal baseline for each cow using rolling moving averages with Bessel's correction, eliminating breed and parity biases.")
    add_list_item("3. Multivariate Covariance Modeling (Tikhonov Mahalanobis Distance):", "Instead of evaluating signals in isolation, the CHDI engine computes regularized Mahalanobis distance across all physiological channels simultaneously, enabling early detection of coupled subclinical shifts 24 to 48 hours before visible symptoms.")
    add_list_item("4. Explainable AI for Clinical Trust (LOCO):", "The proposed system incorporates LOCO feature attribution that ranks the exact physiological contributors driving high-risk scores, providing veterinarians with transparent clinical rationale rather than opaque black-box alerts.")
    add_list_item("5. Zero-Installation In-Browser Edge Architecture:", "Built on Next.js 14 React Server Components, the system runs directly in mobile browsers without requiring native app downloads, operating with sub-45ms inference latency even on modest 4G connections.")

    add_sec_heading_2("3.5 System Feasibility Analysis (Technical, Economic, Operational)")
    add_body_p("A rigorous feasibility study was conducted to validate the viability of deploying the proposed system in real-world rural farming environments. Table 3.2 summarizes the feasibility assessment across technical, economic, and operational dimensions.")

    feas_headers = ["Feasibility Dimension", "Evaluation Criteria", "Proposed System Capability & Validation Outcome"]
    feas_data = [
        [
            "Technical Feasibility",
            "• Computational complexity\n• Mobile browser execution\n• Camera QR decoding\n• Network resilience",
            "• FEASIBLE: Edge TypeScript ML execution consumes < 35MB RAM\n• In-browser camera scanning via html5-qrcode runs at 30 FPS\n• Inference latency < 42 ms per cow on basic Android devices\n• Client-side caching enables uninterrupted data entry"
        ],
        [
            "Economic Feasibility",
            "• Capital cost per animal\n• Operational & server cost\n• Return on Investment (ROI)\n• Maintenance overhead",
            "• FEASIBLE: Capital cost < $0.50 per cow (printed QR tag)\n• Serverless Postgres (Neon) and Vercel edge runtime minimizes hosting\n• ROI achieved in < 14 days by preventing a single clinical mastitis episode\n• Zero electronic hardware replacement or battery costs"
        ],
        [
            "Operational Feasibility",
            "• Farmer digital literacy\n• Daily data entry burden\n• Veterinary workflow alignment\n• Language accessibility",
            "• FEASIBLE: QR scan takes < 3 seconds; daily logging takes < 15 seconds\n• Intuitive color-coded clinical bands (Normal, Monitor, Alert, Critical)\n• Directly aligns with standard morning/evening milking routines\n• Clean responsive UI tailored for mobile screens and regional languages"
        ]
    ]
    add_normal_table(
        feas_headers,
        feas_data,
        [Inches(1.6), Inches(2.0), Inches(2.4)],
        "Table 3.2: System Feasibility Analysis Matrix for Proposed System Deployment"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: PROPOSED FRAMEWORK, ARCHITECTURE AND IMPLEMENTATION
    # ==========================================
    add_chapter_heading("PROPOSED FRAMEWORK, ARCHITECTURE AND IMPLEMENTATION", chapter_number=4)

    add_sec_heading_2("4.1 Overview of the Proposed System Framework")
    add_body_p("SmartCattle is architected as an end-to-end, four-tier cloud-native platform integrating zero-hardware edge capture, high-throughput ingestion, a 3-stage machine learning analytics pipeline, and role-tailored user interfaces for farmers, field veterinarians, and cooperative dairy administrators.")
    
    add_sec_heading_3("Design Goals")
    add_body_p("The architectural engineering of SmartCattle was guided by four strict design principles:")
    add_list_item("1. Zero Capital Barrier:", "No active electronic hardware on the animal; all edge identification is handled via passive optical QR tags.")
    add_list_item("2. Sub-50ms Inference Latency:", "End-to-end telemetry ingestion and multivariate anomaly calculation must execute within 50 ms to provide instantaneous feedback to farmers.")
    add_list_item("3. Strict Role-Based Security:", "Multi-tenant isolation ensuring farmers access only their herd, while veterinarians access regional clinical queues.")
    add_list_item("4. Explainable Clinical Output:", "Every diagnostic prediction must be decomposed into human-readable signal attribution percentages for clinical trust.")

    add_sec_heading_2("4.2 System Architecture and Threat / Data Integrity Model")
    add_body_p("Figure 4.1 depicts the four-tier system architecture, illustrating the flow of telemetry from physical QR tags through cloud security, the analytical engine, and clinical triage.")

    add_figure_item(
        "extracted_images/image1.png",
        "Figure 4.1: Multi-Tier System Architecture of the Proposed QR-Based Cattle Platform (IEEE Paper Fig. 1)",
        width_inches=5.6
    )

    add_sec_heading_3("Threat and Data Integrity Model")
    add_body_p("To ensure data privacy and prevent unauthorized tampering in rural farming clusters, the QR payload contains only an opaque 128-bit cryptographic universally unique identifier (UUID v4) and an HTTPS endpoint URI. No clinical, financial, or ownership data is stored on the physical tag. Telemetry ingestion requires active session authentication. All API payloads are validated against strict Zod schemas, and database queries use parameterized Prisma ORM calls to prevent SQL injection.")

    add_sec_heading_2("4.3 Four-Tier Architectural Subsystems")

    add_sec_heading_3("4.3.1 Tier 1: Identification & Edge Data Acquisition Layer")
    add_body_p("Comprises durable thermoplastic polyurethane (TPU) ear tags laser-etched with high-contrast 2-D QR matrices. When scanned using any smartphone browser, the HTML5 MediaDevices API decodes the UUID via html5-qrcode, loading the cow's logging portal. Daily observations (milk yield in liters, core body temperature in °C, rumination duration in minutes, activity steps, feed intake in kg) are logged by farmers. Veterinarians log clinical diagnoses and treatment logs. Every entry contains a source metadata tag (manual | qr_scan | sensor).")

    add_sec_heading_3("4.3.2 Tier 2: Cloud Platform, API Gateway, and Security Layer")
    add_body_p("Engineered using Next.js 14, React Server Components (RSC), and Server Actions, communicating with a dedicated Python FastAPI ML microservice via RESTful APIs. Role-Based Access Control (RBAC) manages three roles: Farmers, Veterinarians, and Administrators. All communication is encrypted via TLS 1.3.")

    add_sec_heading_3("4.3.3 Tier 3: Three-Stage CHDI Analytics Engine")
    add_body_p("The analytical core executing the Three-Stage CHDI sequence: Stage 1 (Personalized Rolling Baselines), Stage 2 (Tikhonov-Regularized Mahalanobis Distance), and Stage 3 (LOCO Permutation Feature Attribution). Figure 4.2 illustrates the operational workflow.")

    add_figure_item(
        "extracted_images/image2.png",
        "Figure 4.2: Three-Stage CHDI Analytics Engine Operational Workflow (IEEE Paper Fig. 2)",
        width_inches=5.6
    )

    add_sec_heading_3("4.3.4 Tier 4: Clinical Triage and Veterinary Feedback Loop")
    add_body_p("When CHDI crosses into the 'At-Risk' threshold (CHDI ≥ 51), automated alerts dispatch to the regional veterinarian. Clinical feedback from physical veterinary examinations is logged to retrain ensemble weights, continuously refining specificity.")

    add_sec_heading_2("4.4 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)")
    add_body_p("The operational lifecycle of SmartCattle is formally modeled across three DFD levels:")
    add_list_item("Level 0 Context Diagram (DFD Level 0):", "Models the boundary between external entities (Farmer, Veterinarian, Admin) and the central SmartCattle Platform. Telemetry flows in; clinical alerts and triage queues flow out.")
    add_list_item("Level 1 Subsystem Flow (DFD Level 1):", "Deconstructs the platform into four primary processes: Process 1.0 (QR Ingestion & Authentication), Process 2.0 (Historical Baseline Retrieval), Process 3.0 (CHDI Anomaly Scoring & LOCO Attribution), and Process 4.0 (Clinical Alert Dispatch).")
    add_list_item("Level 2 Diagnostic Sub-Process (DFD Level 2):", "Deconstructs Process 3.0 into granular sub-steps: Variance Calculation with Bessel's Correction (3.1), Tikhonov Ridge Regularization (3.2), Matrix Inversion & Mahalanobis Distance (3.3), Sigmoidal Mapping (3.4), and LOCO Permutation (3.5).")

    add_sec_heading_2("4.5 Mathematical Formulation of the CHDI Analytical Engine")
    add_body_p("To ensure complete transparency and reproducibility, the mathematical formulations of the Composite Health Deviation Index (CHDI) are presented below with high-resolution visual equations, variable definitions, and plain-English operational interpretations:")

    add_sec_heading_3("4.5.1 Stage 1: Individual Baseline Calibration & Normalized Deviations")
    add_body_p("Let x_i(t) in R^d represent the daily physiological telemetry vector for cow i across d available vital channels (milk yield, temperature, rumination duration, activity counts, feed intake). Rather than comparing animals against arbitrary population thresholds, Stage 1 builds an individualized historical baseline:")

    # Equation 1: Rolling Baseline Mean
    add_equation_block(
        "generated_equations/eq_1.png",
        "4.1",
        "Personalized Rolling Baseline Mean",
        "Calculates the historical average normal value for a specific cow across a rolling window of W = 14 observations. For example, if Cow #1042 produces an average of 12.4 liters of milk over the past 14 days, mu_i,k(t) is established as 12.4 L.",
        {"x_i,k(t-j)": "Observed value of vital signal k at time offset j", "W = 14": "Rolling history window (14 observations)", "mu_i,k(t)": "Calculated baseline mean for that specific cow"},
        "Eliminates population bias, ensuring high-producing cows and low-producing cows are evaluated strictly against their own biological normal."
    )

    # Equation 2: Sample Variance with Bessel's Correction
    add_equation_block(
        "generated_equations/eq_2.png",
        "4.2",
        "Bessel-Corrected Sample Variance",
        "Measures how much the cow's vitals naturally fluctuate from day to day under normal healthy conditions. Using Bessel's correction (dividing by W - 1 = 13 instead of W = 14) removes statistical bias in small sample sizes.",
        {"sigma_i,k^2(t)": "Rolling sample variance for signal k", "W - 1 = 13": "Bessel correction degrees of freedom (ddof = 1)", "mu_i,k(t)": "Cow's baseline mean from Eq. 4.1"},
        "Accounts for natural day-to-day fluctuations so that minor, harmless variations are not mistaken for disease."
    )

    # Equation 3: Normalized Deviation Z-Score
    add_equation_block(
        "generated_equations/eq_3.png",
        "4.3",
        "Standardized Normalized Deviation Z-Score",
        "Converts the difference between today's reading and the historical average into standard deviation units (z-score). A reading of z = -2.5 means today's milk yield is 2.5 standard deviations below the cow's normal average.",
        {"z_i,k(t)": "Standardized deviation score for signal k", "epsilon = 1e-4": "Small numerical guard preventing division by zero during static logging"},
        "Normalizes heterogeneous physical units (liters, °C, minutes, steps) into a unified dimensionless scale so they can be compared mathematically."
    )

    add_sec_heading_3("4.5.2 Stage 2: Multivariate Covariance & Regularized Mahalanobis Distance")
    add_body_p("Diseases rarely affect a single vital in isolation; subclinical mastitis typically causes a mild milk drop coupled with a slight temperature elevation. Stage 2 evaluates the multivariate relationship across all signals simultaneously:")

    # Equation 4: Tikhonov Regularized Covariance
    add_equation_block(
        "generated_equations/eq_4.png",
        "4.4",
        "Tikhonov-Regularized Covariance Matrix",
        "Computes how different physiological vitals interact with each other (e.g. how milk yield correlates with feed intake). The Tikhonov ridge parameter (lambda = 1e-3) adds a tiny value to the diagonal of the matrix, preventing mathematical division errors or matrix collapse when data is sparse.",
        {"Sigma_i(t)": "Empirical covariance matrix across all d signals", "lambda = 1e-3": "Tikhonov regularization ridge shrinkage factor", "I": "d x d identity matrix"},
        "Guarantees that the covariance matrix can always be safely inverted, making the algorithm 100% immune to crashes during real-world farm operations."
    )

    # Equation 5: Multivariate Mahalanobis Distance
    add_equation_block(
        "generated_equations/eq_5.png",
        "4.5",
        "Tikhonov-Regularized Mahalanobis Distance",
        "Calculates the total multidimensional distance between today's combined vitals and the cow's healthy normal state, factoring in signal correlations. A high distance indicates a coupled abnormal shift across multiple bodily functions.",
        {"D_M(t)": "Multivariate statistical anomaly distance", "z_i(t)": "Standardized deviation vector from Eq. 4.3", "(Sigma_reg)^(-1)": "Inverted regularized covariance matrix"},
        "Detects subtle subclinical disease shifts 24 to 48 hours before any single vital breaches an obvious visual threshold."
    )

    # Equation 6: Calibrated CHDI Score Mapping
    add_equation_block(
        "generated_equations/eq_6.png",
        "4.6",
        "Calibrated Composite Health Deviation Index (CHDI)",
        "Transforms the raw statistical Mahalanobis distance D_M(t) into an intuitive, standardized health score ranging from 0 to 100. A score of 0 means perfect health, while 100 indicates severe critical illness.",
        {"CHDI(t)": "Standardized health index score (0 to 100)", "D_max = 4.0": "Upper distance saturation boundary (representing 4.0 standard deviations of extreme deviation)"},
        "Provides an easily understandable percentage score for farmers and veterinarians without requiring statistical expertise."
    )

    add_sec_heading_3("4.5.3 Stage 3: LOCO Feature Attribution & Confidence Gating")
    add_body_p("To build clinical trust, the system must explain exactly which vitals caused a high risk score and verify that sufficient data exists:")

    # Equation 7: Confidence Gating
    add_equation_block(
        "generated_equations/eq_7.png",
        "4.7",
        "Historical Data Confidence & Abstention Gating",
        "Calculates how mature the cow's historical profile is. If a cow has fewer than 7 days of logs, the system safely abstains from diagnosing (CHDI = null) to prevent false alarms during enrollment. Confidence scales up to 1.0 at 14 days of data.",
        {"rho(t)": "Confidence factor (0.0 to 1.0)", "N_obs": "Number of distinct historical logging days", "N_saturation = 14": "Number of days required for full baseline confidence"},
        "Protects farmers from premature false alarms during the first week when a newly enrolled cow is still building its profile."
    )

    # Equation 8: LOCO Marginal Attribution
    add_equation_block(
        "generated_equations/eq_8.png",
        "4.8",
        "Leave-One-Covariate-Out (LOCO) Marginal Attribution",
        "Measures how much the anomaly distance drops when a specific vital signal k is omitted from the calculation. If removing 'Milk Yield' causes the distance to plummet, then milk drop is the primary driver of the illness.",
        {"Delta D_k(t)": "Marginal distance drop attributed to signal k", "D_{M, -k}(t)": "Mahalanobis distance recalculated without signal k"},
        "Isolates the exact contribution of each bodily signal in real time with zero black-box obscurity."
    )

    # Equation 9: Percentage Feature Contribution
    add_equation_block(
        "generated_equations/eq_9.png",
        "4.9",
        "Normalized Percentage Feature Contribution",
        "Converts the marginal attribution drops into clear percentage contributions summing to 100%. For example: 52.4% Milk Drop, 28.1% Rumination Decline, 14.5% Temperature Rise.",
        {"C_k(t)": "Percentage contribution of signal k to the total health score", "sum Delta D_j": "Sum of attribution drops across all active signals"},
        "Generates clear, human-readable explanations that tell the veterinarian exactly what physiological problem to examine upon arrival."
    )

    add_sec_heading_3("4.5.4 CHDI Clinical Severity Bands and Action Protocols")
    add_body_p("Table 4.1 outlines the standardized clinical severity triage bands and prescribed action protocols (IEEE Paper Table II).")

    tbl2_headers = ["Severity Band", "CHDI Range", "Clinical State & Interpretation", "Prescribed Action Protocol"]
    tbl2_data = [
        ["HEALTHY", "0 – 25", "Homeostatic stability; physiological signals within baseline bounds", "Continue standard feeding, milking, and management routine; no intervention required."],
        ["WATCH", "26 – 50", "Mild subclinical deviation; potential early stress, estrus, or diet shift", "Re-scan within 12 hours; inspect feed consumption, water intake, and locomotion."],
        ["AT-RISK", "51 – 75", "Moderate multi-signal anomaly; strong likelihood of early-stage disease", "Automated notification to regional veterinarian; isolate animal; conduct CMT."],
        ["CRITICAL", "76 – 100", "Severe acute deviation; acute mastitis / systemic metabolic distress", "Emergency veterinary visit; administer clinical therapeutic antibiotic protocol."],
        ["ABSTAIN", "N/A (N < 7)", "Insufficient baseline depth (< 7 observations across distinct days)", "Enrollment phase; safely withhold health scoring until baseline data threshold is met."]
    ]
    add_normal_table(
        tbl2_headers,
        tbl2_data,
        [Inches(1.2), Inches(1.1), Inches(1.8), Inches(1.9)],
        "Table 4.1: CHDI Severity Bands, Score Ranges, and Clinical Protocols (IEEE Paper Table II)"
    )

    add_sec_heading_2("4.6 Database Design & Prisma Schema Entities")
    add_body_p("The relational data model is implemented on PostgreSQL using Prisma ORM. Table 4.2 describes the core schema entities and relational mappings.")

    tbl_db_headers = ["Entity Model", "Primary Attributes", "Relationships & Cardinality", "Functional Purpose"]
    tbl_db_data = [
        ["User", "id, email, passwordHash, role, name, phone", "1:N with Farm, 1:N with VetCase", "Manages credentials and RBAC roles (FARMER, VET, ADMIN)"],
        ["Farm", "id, name, location, ownerId, createdAt", "1:N with Cattle, N:1 with User", "Represents agricultural holding and geographic grouping"],
        ["Cattle", "id, tagNumber, qrCode, breed, dob, purpose", "1:N with Logs, 1:N with CHDIEntry", "Stores immutable biological traits and QR UUID tokens"],
        ["MilkLog / FeedLog", "id, cattleId, value, timestamp, source", "N:1 with Cattle", "Captures longitudinal production and feeding telemetry"],
        ["ActivityLog / WeightLog", "id, cattleId, value, timestamp, source", "N:1 with Cattle", "Stores physical locomotion and body weight measurements"],
        ["CHDIEntry", "id, cattleId, score, confidence, status, deviations", "N:1 with Cattle, 1:1 with VetCase", "Persists CHDI analytical output & LOCO factor attributions"],
        ["VetCase", "id, cattleId, chdiEntryId, vetId, clinicalNotes", "N:1 with Cattle, N:1 with User", "Tracks clinical triage lifecycle and diagnostic overrides"]
    ]
    add_normal_table(
        tbl_db_headers,
        tbl_db_data,
        [Inches(1.2), Inches(1.8), Inches(1.5), Inches(1.5)],
        "Table 4.2: Prisma Database Schema Entities and Relational Mappings"
    )

    add_sec_heading_2("4.7 Technology Stack of the Prototype")
    add_body_p("Table 4.3 details the comprehensive technology stack selected for the implementation of the SmartCattle platform.")

    tbl_tech_headers = ["Layer / Module", "Technology / Library", "Version / Spec", "Rationale & Academic Function"]
    tbl_tech_data = [
        ["Full-Stack Framework", "Next.js (App Router)", "14.2+ (Node.js 20)", "Full-stack SSR, Server Actions, API routes in unified repository"],
        ["Programming Language", "TypeScript & Python", "TS 5.4+ / Python 3.11", "End-to-end type safety in web app; high-performance NumPy/SciPy in ML service"],
        ["ML Microservice", "FastAPI / Uvicorn", "FastAPI 0.111+", "High-throughput REST API serving /compute-chdi endpoint"],
        ["Scientific Computing", "NumPy & SciPy", "NumPy 1.26+ / SciPy 1.13+", "Bessel-corrected variance, Tikhonov regularization, Mahalanobis distance"],
        ["Database", "PostgreSQL (Neon)", "Serverless 16", "High-concurrency relational storage with serverless auto-scaling"],
        ["ORM", "Prisma ORM", "5.14+", "Type-safe database migrations, queries, and relation handling"],
        ["Authentication", "NextAuth.js", "5.0 beta", "Role-based session management and JWT authentication"],
        ["QR Code Engine", "qrcode & html5-qrcode", "1.5+ / 2.3+", "High-density QR generation and real-time in-browser video decoding"],
        ["Visualization", "Recharts", "2.12+", "Interactive longitudinal CHDI trends, radar charts, and telemetry graphs"]
    ]
    add_normal_table(
        tbl_tech_headers,
        tbl_tech_data,
        [Inches(1.2), Inches(1.6), Inches(1.2), Inches(2.0)],
        "Table 4.3: Technology Stack of the Proposed System Research Prototype"
    )

    add_sec_heading_2("4.8 Core Algorithmic Procedures & Pseudocode")
    add_body_p("To make the algorithmic workflow completely understandable, Table 4.4 breaks down the 6 execution steps of the CHDI engine into plain-English operational descriptions:")

    algo_breakdown_headers = ["Step", "Procedure Name", "Input & Math Operation", "Plain-English Operational Function"]
    algo_breakdown_data = [
        ["Step 1", "Abstention Gating", "Check if N_history < 7 days", "Verifies baseline maturity; safely abstains from scoring if cow has < 7 days of logs."],
        ["Step 2", "Individual Baseline", "Compute mu (Eq 4.1) & sigma (Eq 4.2)", "Calculates the cow's personal 14-day average and natural variation with Bessel correction."],
        ["Step 3", "Z-Score Normalization", "Compute z_k = (x_k - mu) / sigma (Eq 4.3)", "Converts daily readings into standardized standard deviation units."],
        ["Step 4", "Regularized Distance", "Invert (Sigma + lambda*I) and compute D_M (Eq 4.5)", "Calculates multivariate anomaly distance while Tikhonov ridge prevents crashes."],
        ["Step 5", "CHDI Mapping & Banding", "Score = (D_M / 4.0) * 100 (Eq 4.6)", "Scales distance into a clean 0 to 100 score and assigns clinical band (Healthy/Watch/At-Risk/Critical)."],
        ["Step 6", "LOCO Explainability", "Omit signal k and calculate Delta D_k (Eq 4.8)", "Determines exact percentage contribution of each vital and dispatches triage alerts if CHDI >= 51."]
    ]
    add_normal_table(
        algo_breakdown_headers,
        algo_breakdown_data,
        [Inches(0.8), Inches(1.3), Inches(1.8), Inches(2.1)],
        "Table 4.4: Core Algorithmic Procedures of the Proposed System CHDI Framework"
    )

    # Formatted Algorithm Box
    p_alg_title = doc.add_paragraph()
    p_alg_title.paragraph_format.space_before = Pt(8)
    p_alg_title.paragraph_format.space_after = Pt(2)
    p_alg_title.paragraph_format.keep_with_next = True
    r_at = p_alg_title.add_run("Algorithm 4.1: Composite Health Deviation Index (CHDI) Complete Execution Workflow")
    r_at.font.name = 'Times New Roman'
    r_at.font.size = Pt(11)
    r_at.bold = True
    r_at.font.color.rgb = COLOR_BLACK

    tbl_algo = doc.add_table(rows=1, cols=1)
    tbl_algo.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_algo, color="888888", sz="4", val="single")
    c_algo = tbl_algo.rows[0].cells[0]
    c_algo.width = Inches(6.0)
    set_cell_background(c_algo, HEX_ALGO_BG)
    set_cell_margins(c_algo, top=90, bottom=90, left=120, right=120)
    prevent_row_split(tbl_algo.rows[0])

    p_ac = c_algo.paragraphs[0]
    p_ac.paragraph_format.space_after = Pt(0)
    p_ac.paragraph_format.line_spacing = 1.15
    
    algo_code = (
        "INPUT:  Today's Vitals Vector x(t) = [milk, temp, rumination, activity, feed]\n"
        "        Historical Observations Buffer H = {x(t-1), ..., x(t-N)}\n"
        "OUTPUT: CHDI Score S(t) in [0, 100], Confidence rho(t), Severity Band B, Feature Attributions C\n"
        "----------------------------------------------------------------------------------------\n"
        " 1:  PROCEDURE ComputeCHDI(x(t), H):\n"
        " 2:      IF length(H) < 7 THEN\n"
        " 3:          RETURN { Score: NULL, Confidence: length(H)/14, Status: 'ABSTAIN', Band: 'Enrollment Phase' }\n"
        " 4:      FOR EACH active vital signal k in {1..d} DO:\n"
        " 5:          mu_k    <- Average of last 14 historical observations (Equation 4.1)\n"
        " 6:          sigma_k <- Sample standard deviation with Bessel ddof=1 (Equation 4.2)\n"
        " 7:          z_k(t)  <- (x_k(t) - mu_k) / sqrt(sigma_k^2 + 1e-4)    (Equation 4.3)\n"
        " 8:      Sigma_reg   <- Empirical Covariance Matrix + (1e-3 * Identity Matrix) (Equation 4.4)\n"
        " 9:      D_M(t)      <- sqrt( z(t)^T * inv(Sigma_reg) * z(t) )      (Equation 4.5)\n"
        "10:      S_raw       <- min( 100, (D_M(t) / 4.0) * 100 )            (Equation 4.6)\n"
        "11:      FOR EACH active vital signal k in {1..d} DO:\n"
        "12:          D_minus_k <- Recompute Mahalanobis distance omitting signal k\n"
        "13:          Delta_D_k <- max( 0, D_M(t) - D_minus_k )              (Equation 4.8)\n"
        "14:      FOR EACH active vital signal k in {1..d} DO:\n"
        "15:          C_k       <- (Delta_D_k / Sum of all Delta_D) * 100%   (Equation 4.9)\n"
        "16:      IF S_raw < 26 THEN B <- 'HEALTHY'\n"
        "17:      ELSE IF S_raw < 51 THEN B <- 'WATCH'\n"
        "18:      ELSE IF S_raw < 76 THEN B <- 'AT-RISK'; DispatchVeterinarianTriageAlert(cattleId, S_raw, C)\n"
        "19:      ELSE B <- 'CRITICAL'; DispatchEmergencyVeterinarianAlert(cattleId, S_raw, C)\n"
        "20:      RETURN { Score: S_raw, Confidence: min(1.0, length(H)/14), Band: B, Contributions: C }\n"
        "21:  END PROCEDURE"
    )
    r_ac = p_ac.add_run(algo_code)
    r_ac.font.name = 'Consolas'
    r_ac.font.size = Pt(9.5)
    r_ac.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: EXPERIMENTAL RESULTS AND DISCUSSION
    # ==========================================
    add_chapter_heading("EXPERIMENTAL RESULTS AND DISCUSSION", chapter_number=5)

    add_sec_heading_2("5.1 Experimental Setup & Benchmark Cohort Provenance")
    add_body_p("To thoroughly validate SmartCattle under authentic agricultural field conditions, an 8-week longitudinal study (56 days) was conducted across 18 smallholder dairy farms in Salem District, Tamil Nadu, India. The benchmark cohort comprised 120 dairy cattle representing typical smallholder breed compositions. Certified veterinary surgeons provided clinical diagnostic ground truth through California Mastitis Tests (CMT), somatic cell counts (SCC), blood beta-hydroxybutyrate (BHBA) strips, and rectal palpation.")
    add_body_p("Table 5.1 details the experimental cohort demographics, logging completion, and clinical ground truth provenance.")

    tbl_ds_headers = ["Cohort Parameter", "Experimental Value / Breakdown", "Clinical Significance & Provenance"]
    tbl_ds_data = [
        ["Total Cattle Monitored", "120 Cows (18 Smallholder Farms)", "Representative sample of rural smallholder dairy operations"],
        ["Breed Composition", "Jersey Cross (54%), HF Cross (32%), Indigenous (14%)", "Captures genetic variation and breed-specific baseline profiles"],
        ["Lactation Parity", "1st Parity (28%), 2nd–3rd (52%), 4th+ (20%)", "Evaluates performance across young heifers and mature milkers"],
        ["Total Telemetry Ingestion Events", "6,720 Daily Scans (100% Protocol Completion)", "Demonstrates high farmer compliance with mobile QR workflow"],
        ["Confirmed Mastitis Episodes", "19 Cases (14 Subclinical, 5 Clinical)", "Gold standard verified via California Mastitis Test & Somatic Cell Counts"],
        ["Confirmed Ketosis Episodes", "11 Cases (Subclinical / Clinical)", "Verified via blood beta-hydroxybutyrate (BHBA) strip testing"],
        ["Confirmed Bovine Respiratory (BRD)", "9 Cases (Confirmed via Auscultation)", "Verified through clinical veterinary pulmonary auscultation"],
        ["Confirmed Estrus Events", "34 Estrus Cycles (Verified via Artificial Insemination)", "Evaluated for estrus onset sensitivity and timing precision"]
    ]
    add_normal_table(
        tbl_ds_headers,
        tbl_ds_data,
        [Inches(1.8), Inches(2.2), Inches(2.0)],
        "Table 5.1: Benchmark Experimental Cohort Breakdown and Ground Truth Provenance"
    )

    add_sec_heading_2("5.2 Evaluation Metrics")
    add_body_p("The diagnostic efficacy of the CHDI analytical engine was benchmarked using standard statistical and clinical epidemiological metrics:")
    add_list_item("Sensitivity (Recall):", "TP / (TP + FN) – The proportion of true positive disease/estrus episodes correctly flagged.")
    add_list_item("Specificity:", "TN / (TN + FP) – The proportion of healthy homeostatic states correctly identified as normal.")
    add_list_item("Precision (Positive Predictive Value):", "TP / (TP + FP) – The fraction of generated alerts corresponding to true clinical conditions.")
    add_list_item("F1-Score:", "2 * (Precision * Recall) / (Precision + Recall) – Harmonic mean balancing precision and recall.")
    add_list_item("Area Under ROC Curve (AUC-ROC):", "Measures the aggregate discriminatory power across all decision thresholds.")

    add_sec_heading_2("5.3 Detection and Diagnostic Results Across Bovine Conditions")
    add_body_p("Table 5.2 summarizes the diagnostic performance of SmartCattle across all evaluated bovine pathological conditions.")

    perf_headers = ["Bovine Condition", "Sensitivity (%)", "Specificity (%)", "Precision (%)", "F1-Score (%)", "AUC-ROC"]
    perf_data = [
        ["Subclinical Mastitis", "94.7 %", "96.5 %", "90.0 %", "92.3 %", "0.962"],
        ["Clinical Mastitis", "100.0 %", "98.2 %", "95.2 %", "97.5 %", "0.991"],
        ["Subclinical Ketosis", "90.9 %", "95.8 %", "83.3 %", "86.9 %", "0.945"],
        ["Bovine Respiratory (BRD)", "88.9 %", "97.1 %", "80.0 %", "84.2 %", "0.938"],
        ["Estrus / Heat Onset", "94.1 %", "95.4 %", "88.9 %", "91.4 %", "0.957"],
        ["Overall Weighted Macro", "93.8 %", "96.2 %", "89.2 %", "91.4 %", "0.958"]
    ]
    add_normal_table(
        perf_headers,
        perf_data,
        [Inches(1.5), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9)],
        "Table 5.2: Diagnostic Performance Metrics for Common Bovine Pathologies"
    )

    add_sec_heading_2("5.4 Longitudinal Clinical Case Trace & Explainability Walkthrough")
    add_body_p("Figure 5.1 illustrates the aggregate herd risk distribution over the 8-week trial. Approximately 82.4% of all animal-days remained securely within the 'Healthy' band (CHDI 0–25), 11.2% in 'Watch', 4.8% in 'At-Risk', and 1.6% in 'Critical', proving that the regularized CHDI baseline eliminates false alarm saturation.")

    add_figure_item(
        "generated_figures/fig3_status_distribution.png",
        "Figure 5.1: Cohort Herd Status and Risk Distribution Breakdown across Validation Period (IEEE Paper Fig. 3)",
        width_inches=5.4
    )

    add_body_p("Figure 5.2 traces a longitudinal case study for Cow #SC-1042 developing subclinical mastitis over a 14-day window. The baseline established over Days 1–6 showed stable CHDI scores (< 20). On Day 7, CHDI spiked to 58 ('At-Risk') due to a coupled 11% milk yield drop and a 0.4°C temperature rise. On Day 8, CHDI reached 78 ('Critical'), prompting automated veterinary dispatch. Formal clinical CMT confirmed subclinical mastitis on Day 9, validating a 36-hour pre-clinical early warning lead time.")

    add_figure_item(
        "generated_figures/fig4_longitudinal_trajectory.png",
        "Figure 5.2: Longitudinal CHDI Score Trajectory Demonstrating Pre-Clinical Mastitis Lead Time (IEEE Paper Fig. 4)",
        width_inches=5.6
    )

    add_body_p("Figure 5.3 shows the LOCO feature attribution breakdown for Cow #SC-1042 on Day 8, attributing 52.4% of the anomaly to milk yield drop, 28.1% to rumination duration decline, and 14.5% to temperature elevation, providing clear clinical interpretability.")

    add_figure_item(
        "generated_figures/fig5_feature_importance.png",
        "Figure 5.3: Leave-One-Covariate-Out (LOCO) Feature Attribution Ranking for Health Deviation (IEEE Paper Fig. 5)",
        width_inches=5.4
    )

    add_sec_heading_2("5.5 Algorithmic Ablation Study")
    add_body_p("To quantify the contribution of each mathematical component, SmartCattle was benchmarked against three baseline ablation models (IEEE Paper Table III):")

    tbl3_headers = ["Model / Algorithm", "Sensitivity (%)", "Specificity (%)", "Precision (%)", "F1-Score (%)", "AUC-ROC"]
    tbl3_data = [
        ["Univariate Z-Score Baseline", "76.3 %", "81.4 %", "68.2 %", "72.0 %", "0.788"],
        ["Isolation Forest (Population)", "82.1 %", "87.6 %", "74.5 %", "78.1 %", "0.852"],
        ["Mahalanobis (No Regularization)", "88.4 %", "91.2 %", "81.0 %", "84.5 %", "0.904"],
        ["SmartCattle CHDI (Proposed)", "93.8 %", "96.2 %", "89.2 %", "91.4 %", "0.958"]
    ]
    add_normal_table(
        tbl3_headers,
        tbl3_data,
        [Inches(2.0), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.8)],
        "Table 5.3: Anomaly Detection Performance Metrics & Algorithmic Ablation (IEEE Paper Table III)"
    )

    add_sec_heading_2("5.6 Predictive Lead Time & Early Intervention Advantage")
    add_body_p("Table 5.4 presents the empirical lead times achieved by the proposed system across all confirmed pathological events.")

    tbl_lt_headers = ["Pathological Condition", "Average Lead Time Window", "Early Warning Physiological Signature", "Clinical Benefit"]
    tbl_lt_data = [
        ["Subclinical Mastitis", "36.4 ± 8.2 Hours (1.5 Days)", "Milk yield drop (8–14%) + slight temp elevation (0.4°C)", "Enables intra-mammary herbal/antibiotic infusion before tissue scarring"],
        ["Subclinical Ketosis", "42.1 ± 10.5 Hours (1.8 Days)", "Feed refusal (20%) + activity drop without acute fever", "Propylene glycol drenching prevents severe metabolic collapse"],
        ["Bovine Respiratory (BRD)", "28.6 ± 6.4 Hours (1.2 Days)", "Rumination decline (45 min) + mild temperature spike", "Early anti-inflammatory administration prevents lung consolidation"],
        ["Estrus / Heat Cycle", "14.2 ± 3.1 Hours", "Activity spike (+65%) + slight milk yield fluctuation", "Optimal timing for Artificial Insemination (AI) within 12–18 hour window"]
    ]
    add_normal_table(
        tbl_lt_headers,
        tbl_lt_data,
        [Inches(1.6), Inches(1.5), Inches(1.6), Inches(1.3)],
        "Table 5.4: Subclinical Disease Lead Time and Early Intervention Advantage"
    )

    add_sec_heading_2("5.7 Response Time, Computational Latency and Edge Footprint")
    add_body_p("The system's computational performance was benchmarked on standard budget smartphones (MediaTek Helio G85 processor, 4GB RAM, 4G mobile connection). Table 5.5 provides the latency breakdown.")

    tbl_lat_headers = ["Operational Step / Pipeline Stage", "Execution Engine", "Mean Latency", "P99 Latency", "Resource Footprint"]
    tbl_lat_data = [
        ["QR Code Video Stream Scanning", "html5-qrcode (WASM)", "18.2 ms", "32.0 ms", "< 12 MB Client RAM"],
        ["Individual Baseline Retrieval", "Prisma ORM / Indexed DB", "14.5 ms", "26.4 ms", "< 2 MB Memory Cache"],
        ["Mahalanobis Anomaly Calculation", "Python FastAPI / SciPy", "4.8 ms", "8.2 ms", "< 0.5 MB Memory"],
        ["LOCO Feature Attribution", "Python FastAPI / NumPy", "3.6 ms", "6.1 ms", "< 1.2 MB Memory"],
        ["End-to-End Total Ingestion & Diagnosis", "Full Stack Pipeline", "41.1 ms", "72.7 ms", "< 35 MB Total Heap"]
    ]
    add_normal_table(
        tbl_lat_headers,
        tbl_lat_data,
        [Inches(1.8), Inches(1.4), Inches(0.9), Inches(0.9), Inches(1.0)],
        "Table 5.5: End-to-End Latency and Computational Footprint Breakdown"
    )

    add_sec_heading_2("5.8 Benchmarking with Commercial Wearable IoT Platforms")
    add_body_p("Table 5.6 presents a direct comparative evaluation between the proposed system and leading commercial precision dairy solutions.")

    tbl_bench_headers = ["Evaluation Metric", "SCR CowManager", "Afimilk AfiAct II", "smaXtec Rumen Bolus", "Proposed System"]
    tbl_bench_data = [
        ["Capital Cost per Animal", "$150 – $220 USD", "$180 – $250 USD", "$220 – $350 USD", "< $0.50 USD (QR Tag)"],
        ["Annual Maintenance Cost", "$25 – $40 / cow", "$30 – $50 / cow", "$40 – $60 / cow", "$0.00 USD"],
        ["On-Animal Hardware Type", "Ear Tag / Collar", "Leg Pedometer", "Indwelling Bolus", "None (Zero Hardware)"],
        ["Hardware Durability / Risk", "Detachment / Loss", "Mud / Physical Damage", "Non-retrievable", "Durable Weatherproof QR"],
        ["Estrus Sensitivity", "88.5 %", "91.2 %", "84.0 %", "94.1 %"],
        ["Mastitis Detection Lead Time", "24 – 36 Hours", "18 – 24 Hours", "24 – 36 Hours", "36 – 48 Hours"],
        ["Explainable Signal Ranking?", "No (Proprietary)", "No (Threshold)", "No (Proprietary)", "Yes (LOCO Permutation)"],
        ["Smallholder Viability", "Extremely Low", "Extremely Low", "Extremely Low", "Optimal (Democratized)"]
    ]
    add_normal_table(
        tbl_bench_headers,
        tbl_bench_data,
        [Inches(1.6), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)],
        "Table 5.6: Benchmarking the Proposed System against Commercial Wearable IoT Solutions"
    )

    add_sec_heading_2("5.9 Limitations of the Evaluation")
    add_body_p("While the empirical validation demonstrated strong diagnostic efficacy, three limitations are noted:")
    add_list_item("1. Semi-Supervised Baseline Period:", "The system requires an initial enrollment phase (minimum 7 observation days) to establish baseline maturity, during which automated scoring is safely withheld.")
    add_list_item("2. Farmer Compliance Dependency:", "Accurate predictions rely on regular daily logging during morning and evening farm routines.")
    add_list_item("3. Single Agro-Climatic Zone:", "The 8-week trial was conducted within Salem District, Tamil Nadu; wider multi-state trials across varied climatic zones are planned.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6: CONCLUSION AND FUTURE SCOPE
    # ==========================================
    add_chapter_heading("CONCLUSION AND FUTURE SCOPE", chapter_number=6)

    add_sec_heading_2("6.1 Conclusion")
    add_body_p("This project successfully conceptualized, mathematically formulated, implemented, and empirically validated the proposed system, an AI-powered, QR-based cattle health management platform designed specifically for smallholder dairy farmers. By decoupling precision livestock healthcare from expensive on-animal electronic sensors, the proposed system establishes a transformative, zero-hardware-cost paradigm that operates effectively within the economic and infrastructural realities of developing agrarian economies.")
    add_body_p("At the core of the system, the Composite Health Deviation Index (CHDI) algorithm integrates individual adaptive baseline estimation, Tikhonov-regularized multivariate Mahalanobis distance anomaly scoring, supervised veterinary feedback calibration, and LOCO feature attribution. In longitudinal field trials across 120 dairy cattle over an 8-week period, the proposed system achieved an anomaly detection sensitivity of 93.8%, specificity of 96.2%, and an overall diagnostic accuracy of 95.1%, providing early warning lead times of 24 to 48 hours prior to acute clinical symptoms.")

    add_sec_heading_2("6.2 Summary of Key Contributions")
    add_body_p("The primary academic, technical, and socioeconomic contributions of this project include:")
    add_list_item("1. Democratization of Precision Livestock Healthcare:", "Reduced the per-animal health monitoring cost from $150–$350 to under $0.50 (a 99.7% cost reduction), enabling immediate adoption across resource-constrained smallholder farms.")
    add_list_item("2. Novel Multi-Stage Mathematical Formulation (CHDI):", "Formulated a regularized multivariate deviation metric that eliminates population bias by tracking individual homeostasis trajectories.")
    add_list_item("3. Explainable Veterinary Clinical Triage:", "Provided transparent, LOCO-based feature attribution that ranks the exact physiological contributors driving health risk scores.")
    add_list_item("4. High-Efficiency Edge-First Web Architecture:", "Engineered an end-to-end TypeScript and Next.js 14 architecture delivering sub-42ms inference latencies on standard mobile smartphone browsers without native app friction.")

    add_sec_heading_2("6.3 Future Scope")
    add_body_p("Building upon the successful foundational outcomes of the proposed system, several promising research avenues are planned for future expansion:")
    add_list_item("1. Offline-First Synchronization via CRDTs:", "Implementing Conflict-Free Replicated Data Types (CRDTs) and local browser storage (IndexedDB) to enable seamless, offline-first data logging in remote rural areas with zero cellular connectivity, automatically reconciling data upon reconnecting.")
    add_list_item("2. Multilingual Vernacular Voice Assistant:", "Integrating edge-based automatic speech recognition (ASR) in regional languages (Tamil, Hindi, Telugu, Kannada) to allow illiterate or semi-literate farmers to log telemetry via simple spoken voice commands.")
    add_list_item("3. Satellite & Microclimate Environmental Correlation:", "Correlating farm-level CHDI anomalies with regional weather telemetry (temperature-humidity index, heat waves, rainfall anomalies) to forecast regional disease outbreaks and heat stress.")
    add_list_item("4. Blockchain-Enabled Vaccination & Milk Provenance:", "Integrating a decentralized ledger (e.g., Ethereum / Polygon L2) to issue tamper-proof vaccination certificates and milk quality audit trails, facilitating direct premium market access for smallholder producers.")

    doc.add_page_break()

    # ==========================================
    # REFERENCES
    # ==========================================
    add_chapter_heading("REFERENCES")

    ieee_references = [
        "[1] C. J. Rutten, A. G. Velthuis, W. Steeneveld, and H. Hogeveen, “Invited review: Sensors to support health management on dairy farms,” Journal of Dairy Science, vol. 96, no. 4, pp. 1928–1952, 2013.",
        "[2] J. M. Bewley, R. A. Russell, M. M. Dolecheck, and M. W. Borchers, “Precision dairy monitoring technology implementation opportunities and challenges,” in Proc. 10th Int. Conf. Precision Agric., St. Louis, MO, USA, 2016, pp. 1–12.",
        "[3] J. Bumbálek, J. Pytel, and J. Císař, “Comparison of individual dairy cow identification methods based on YOLOv8 and optical tags,” Computers and Electronics in Agriculture, vol. 215, p. 108432, 2023.",
        "[4] F. Subach and E. Shmeleva, “Digital transformation of livestock farming: A survey of IoT architectures and cloud data pipelines,” Agronomy Research, vol. 20, no. 3, pp. 810–825, 2022.",
        "[5] R. Kaur and N. S. Virk, “IoT-based cattle health monitoring and disease classification using machine learning,” IEEE Transactions on AgriFood Electronics, vol. 1, no. 2, pp. 112–121, 2023.",
        "[6] E. Curti, M. Brambilla, C. Bisaglia, and S. Ferrari, “A five-stage precision livestock farming framework for dairy herd telemetry,” Biosystems Engineering, vol. 220, pp. 45–59, 2022.",
        "[7] C. Aquilani, F. Confessore, R. Bozzi, C. Sirtori, and A. Pugliese, “Precision livestock farming technologies in pasture-based livestock systems: A review,” Animal, vol. 16, no. 1, p. 100429, 2022.",
        "[8] M. Ahmad and R. Salamat, “Web-based clinical management and role-based veterinary health records,” Journal of Veterinary Medical Informatics, vol. 8, no. 1, pp. 23–34, 2021.",
        "[9] A. L. Barriuso, G. Villarrubia, F. De Paz, and J. M. Corchado, “Multi-agent architecture for livestock monitoring using WSN and edge orchestration,” Sensors, vol. 18, no. 9, p. 2890, 2018.",
        "[10] A. N. Tikhonov and V. Y. Arsenin, Solutions of Ill-Posed Problems. Washington, DC: V. H. Winston & Sons, 1977.",
        "[11] P. C. Mahalanobis, “On the generalized distance in statistics,” Proceedings of the National Institute of Sciences of India, vol. 2, no. 1, pp. 49–55, 1936.",
        "[12] C. Kamphuis, H. Mollenhorst, A. Feelders, D. Pietersma, and H. Hogeveen, “Decision tree induction to detect mastitis with automatic milking systems,” Computers and Electronics in Agriculture, vol. 70, no. 1, pp. 60–68, 2010.",
        "[13] S. M. Lundberg and S. I. Lee, “A unified approach to interpreting model predictions,” in Advances in Neural Information Processing Systems (NeurIPS 2017), vol. 30, pp. 4765–4774, 2017.",
        "[14] M. W. Borchers and J. M. Bewley, “An assessment of producer precision dairy farming technology use, benefits, and disadvantages,” Journal of Dairy Science, vol. 98, no. 3, pp. 2158–2165, 2015.",
        "[15] J. B. Espinosa, D. L. Smith, and M. A. Green, “Multivariate anomaly detection for subclinical mastitis monitoring in dairy cattle using unsupervised machine learning,” Computers and Electronics in Agriculture, vol. 175, p. 105584, 2020.",
        "[16] S. Shahinfar, D. Page, J. Guenther, V. Cabrera, P. Fricke, and K. Weigel, “Prediction of subclinical ketosis and milk yield trajectory in dairy cows using Long Short-Term Memory networks,” Journal of Dairy Science, vol. 104, no. 5, pp. 5812–5825, 2021.",
        "[17] FAO, “The state of food and agriculture: Leveraging automation in agriculture for transforming agrifood systems,” Food and Agriculture Organization of the United Nations, Rome, Italy, Tech. Rep., 2022.",
        "[18] National Dairy Development Board (NDDB), “Annual Report 2023–2024: Transforming rural livelihoods through sustainable dairying,” Anand, Gujarat, India, Tech. Rep., 2024."
    ]

    for ref in ieee_references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(7)
        p_ref.paragraph_format.line_spacing = 1.3
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(10.5)
        r_ref.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # ==========================================
    # APPENDIX
    # ==========================================
    add_chapter_heading("APPENDIX")

    add_sec_heading_2("A.1 Summary of Mathematical Notation")
    not_headers = ["Symbol", "Domain / Type", "Definition & Operational Meaning"]
    not_data = [
        ["x_i(t)", "R^d Vector", "Daily physiological telemetry vector for cow i at observation t"],
        ["mu_i(t)", "R^d Vector", "Rolling moving-average baseline vector over window W = 14"],
        ["sigma_i^2(t)", "R^d Vector", "Sample variance vector with Bessel's correction (ddof = 1)"],
        ["z_i(t)", "R^d Vector", "Standardized normalized deviation z-score vector"],
        ["Sigma_i(t)", "R^(d x d) Matrix", "Empirical covariance matrix computed over historical observations"],
        ["lambda", "Scalar (1e-3)", "Tikhonov regularization ridge parameter preventing singularity"],
        ["D_M(t)", "Scalar (R+)", "Tikhonov-regularized multivariate Mahalanobis distance"],
        ["D_max", "Scalar (4.0)", "Upper distance boundary for sigmoidal normalization to 0–100"],
        ["CHDI(t)", "Scalar [0, 100]", "Composite Health Deviation Index score"],
        ["Delta D_k(t)", "Scalar (R+)", "Marginal distance drop when omitting feature k (LOCO attribution)"],
        ["C_k(t)", "Percentage (%)", "Relative contribution percentage of signal k to overall deviation"],
        ["rho(t)", "Scalar [0, 1]", "Confidence metric scaling with historical data maturity"]
    ]
    add_normal_table(
        not_headers,
        not_data,
        [Inches(1.2), Inches(1.3), Inches(3.5)],
        "Table A.1: Summary of Mathematical Notations and Variable Definitions"
    )

    add_sec_heading_2("A.2 Evaluation Protocol Summary")
    add_body_p("The longitudinal field evaluation was conducted under the following standardized protocol:")
    add_list_item("Cohort Size:", "120 dairy cattle across 18 smallholder dairy farms in Salem District, Tamil Nadu.")
    add_list_item("Duration:", "56 continuous days (8 calendar weeks) covering 6,720 daily observation events.")
    add_list_item("Observation Routine:", "Daily morning (06:00–08:00) and evening (17:00–19:00) scanning via mobile web browser.")
    add_list_item("Clinical Verification:", "Gold standard verification via California Mastitis Test (CMT), somatic cell counts, and BHBA strip tests.")

    add_sec_heading_2("A.3 Reproducibility Checklist")
    add_list_item("✓ Code Availability:", "Full Next.js 14 web application and Python FastAPI microservice open for academic audit.")
    add_list_item("✓ Type Safety:", "100% end-to-end TypeScript interfaces and Zod schema validations across the data pipeline.")
    add_list_item("✓ Reproducible ML:", "Deterministic mathematical formulations (NumPy, SciPy) with exact regularization constants (lambda = 1e-3, W = 14, D_max = 4.0).")
    add_list_item("✓ Zero External Dependencies on Animal:", "Uses standard ISO-compliant QR matrices readable by any generic HTML5 camera device.")

    output_filename = "SmartCattle_Mini_Project_Report_v4.docx"
    doc.save(output_filename)
    print(f"Successfully generated clean academic report: {output_filename}")

    for fn in ["SmartCattle_Mini_Project_Report_v3.docx", "SmartCattle_Mini_Project_Report_v2.docx", "SmartCattle_Mini_Project_Report_Final.docx", "SmartCattle_Mini_Project_Report.docx"]:
        try:
            doc.save(fn)
            print(f"Also updated: {fn}")
        except Exception as e:
            print(f"Note: {fn} is currently open ({e})")

if __name__ == "__main__":
    generate_perfect_academic_report()
