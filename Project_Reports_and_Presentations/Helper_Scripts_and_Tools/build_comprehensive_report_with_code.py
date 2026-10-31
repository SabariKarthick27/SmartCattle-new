import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_report_with_full_implementation_code():
    doc = docx.Document()

    TAB_STOP_RIGHT = 8640  # 6.0 inches right margin tab
    TAB_STOP_ABBR = 2160   # 1.5 inches abbreviation tab

    # Configure Section 1 (Front Matter)
    sec1 = doc.sections[0]
    sec1.top_margin = Inches(1.0)
    sec1.bottom_margin = Inches(1.0)
    sec1.left_margin = Inches(1.25)
    sec1.right_margin = Inches(1.0)
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    
    sectPr1 = sec1._sectPr
    pgNumType1 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="1" w:fmt="lowerRoman"/>')
    sectPr1.append(pgNumType1)

    COLOR_BLACK = RGBColor(0x00, 0x00, 0x00)
    COLOR_DARK = RGBColor(0x1A, 0x1A, 0x1A)      # Charcoal
    COLOR_MUTED = RGBColor(0x33, 0x33, 0x33)     # Dark Neutral

    HEX_NORMAL_HDR_BG = "EFEFEF"
    HEX_NORMAL_ALT_BG = "FAFAFA"
    HEX_NORMAL_BORDER = "888888"
    HEX_ALGO_BG = "F8F9FA"
    HEX_CODE_BG = "F5F6F8"

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

    def add_code_block(title_caption, code_str):
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(4)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(title_caption)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(11)
        r_cap.bold = True
        r_cap.font.color.rgb = COLOR_BLACK

        tbl_code = doc.add_table(rows=1, cols=1)
        tbl_code.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl_code, color=HEX_NORMAL_BORDER, sz="4", val="single")
        cell_code = tbl_code.rows[0].cells[0]
        cell_code.width = Inches(6.0)
        set_cell_background(cell_code, HEX_CODE_BG)
        set_cell_margins(cell_code, top=90, bottom=90, left=120, right=120)
        prevent_row_split(tbl_code.rows[0])

        p_code = cell_code.paragraphs[0]
        p_code.paragraph_format.space_after = Pt(2)
        p_code.paragraph_format.line_spacing = 1.15
        
        r_c = p_code.add_run(code_str)
        r_c.font.name = 'Courier New'
        r_c.font.size = Pt(8.5)
        r_c.font.color.rgb = COLOR_BLACK

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(8)

    def add_dot_leader_line(title_text, page_str, is_bold=False, indent_spaces=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.3
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
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
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

    print("Synthesizing Full Academic Project Report with Complete Implementation Code...")

    # ==========================================
    # FRONT MATTER: COVER PAGE (Page i)
    # ==========================================
    tbl_hdr = doc.add_table(rows=1, cols=3)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_hdr, color="FFFFFF", sz="0", val="none")
    prevent_row_split(tbl_hdr.rows[0])

    c_left, c_mid, c_right = tbl_hdr.rows[0].cells
    c_left.width = Inches(1.15)
    c_mid.width = Inches(3.72)
    c_right.width = Inches(1.15)

    p_left = c_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_left.paragraph_format.space_before = Pt(4)
    p_left.paragraph_format.space_after = Pt(0)
    if os.path.exists("extracted_header_logos/col_0_image1.jpeg"):
        p_left.add_run().add_picture("extracted_header_logos/col_0_image1.jpeg", width=Inches(1.0))
    elif os.path.exists("template_images/image1.jpeg"):
        p_left.add_run().add_picture("template_images/image1.jpeg", width=Inches(1.0))

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
    # BONAFIDE CERTIFICATE (Page ii)
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
    # DECLARATION (Page iii)
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

    # ==========================================
    # ACKNOWLEDGEMENT (Page iv)
    # ==========================================
    add_chapter_heading("ACKNOWLEDGEMENT")
    add_body_p("First and foremost, we express our profound gratitude to the Almighty for showering his immense blessings upon us throughout the successful completion of this project.", space_after=12)
    add_body_p("We extend our heartfelt gratitude to our Chairman, Vice-Chairmen, and Executive Director for providing exceptional state-of-the-art laboratory and computing infrastructure.", space_after=12)
    add_body_p("We express our deep sense of gratitude and sincere thanks to our respected Principal, Dr. S. R. R. Senthil Kumar, for his continuous encouragement and academic support throughout our course of study.", space_after=12)
    add_body_p("We are highly indebted and express our sincere thanks to Dr. J. Akilandeswari, Professor & Head, Department of Information Technology, for her invaluable guidance, visionary encouragement, and academic leadership.", space_after=12)
    add_body_p("We express our deepest sense of gratitude, respect, and indebtedness to our esteemed Project Supervisor, Mrs. J. Deepika, Assistant Professor, Department of Information Technology, whose profound technical insights, constant inspiration, constructive critiques, and meticulous guidance made this research possible.", space_after=12)
    add_body_p("We also convey our gratitude to all teaching and non-teaching faculty members of the Department of Information Technology, the veterinary clinicians who offered clinical feedback during field validation, and our loving parents and peers for their unwavering moral and emotional support.", space_after=16)

    doc.add_page_break()

    # ==========================================
    # ABSTRACT (Page v)
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
    # PRELIMINARY LISTS: TABLE OF CONTENTS (Pages vi - vii)
    # ==========================================
    add_chapter_heading("TABLE OF CONTENTS")
    add_dot_leader_header("TOPIC / CHAPTER TITLE", "PAGE NO.")

    toc_structure = [
        ("BONAFIDE CERTIFICATE", "ii", True, 0),
        ("DECLARATION", "iii", True, 0),
        ("ACKNOWLEDGEMENT", "iv", True, 0),
        ("ABSTRACT", "v", True, 0),
        ("LIST OF TABLES", "viii", True, 0),
        ("LIST OF FIGURES", "ix", True, 0),
        ("LIST OF ABBREVIATIONS", "x", True, 0),
        ("CHAPTER 1: INTRODUCTION", "1", True, 0),
        ("1.1 Background of Smallholder Dairy Healthcare", "1", False, 1),
        ("1.2 Challenges in Conventional Livestock Monitoring", "1", False, 1),
        ("1.3 Motivation & Research Gaps in Precision Dairy Farming", "1", False, 1),
        ("1.4 Problem Statement", "2", False, 1),
        ("1.5 Objectives of the Project", "2", False, 1),
        ("1.6 Scope and Contributions", "2", False, 1),
        ("1.7 Overview of the Proposed Approach", "3", False, 1),
        ("1.8 Organisation of the Report", "3", False, 1),
        ("CHAPTER 2: LITERATURE REVIEW", "4", True, 0),
        ("2.1 Information, Communication and Networking Systems in PLF", "4", False, 1),
        ("2.2 Sensors and Physiological Monitoring for Wearable IoT Devices", "4", False, 1),
        ("2.3 Computer Vision and Optical Identification Systems", "4", False, 1),
        ("2.4 Digital Platforms and Veterinary Health Records", "5", False, 1),
        ("2.5 Summary of the Literature and Research Gap", "5", False, 1),
        ("2.6 Feature Comparison: Proposed System vs. Related Approaches", "5", False, 1),
        ("CHAPTER 3: EXISTING SYSTEM VS PROPOSED SYSTEM", "6", True, 0),
        ("3.1 Existing Techniques in Cattle Health Monitoring", "6", False, 1),
        ("3.1.1 Manual Visual Inspection", "6", False, 2),
        ("3.1.2 Wearable Collar Sensors & Accelerometers", "6", False, 2),
        ("3.1.3 Intra-Rumen Telemetry Boluses", "6", False, 2),
        ("3.1.4 Automated Milking System In-Line Sensors", "6", False, 2),
        ("3.2 Advantages and Disadvantages of Existing Techniques", "6", False, 1),
        ("3.3 Proposed Technique: SmartCattle QR & CHDI Platform", "7", False, 1),
        ("3.4 How SmartCattle Overcomes Existing Limitations", "7", False, 1),
        ("3.5 System Feasibility Analysis (Technical, Economic, Operational)", "8", False, 1),
        ("CHAPTER 4: PROPOSED FRAMEWORK, ARCHITECTURE AND IMPLEMENTATION", "9", True, 0),
        ("4.1 Overview of the SmartCattle Framework", "9", False, 1),
        ("4.2 System Architecture and Threat / Data Integrity Model", "9", False, 1),
        ("4.3 Four-Tier Architectural Subsystems", "10", False, 1),
        ("4.3.1 Tier 1: Identification & Edge Data Acquisition Layer", "10", False, 2),
        ("4.3.2 Tier 2: Cloud Platform, API Gateway, and Security Layer", "10", False, 2),
        ("4.3.3 Tier 3: Three-Stage CHDI Analytics Engine", "10", False, 2),
        ("4.3.4 Tier 4: Clinical Triage and Veterinary Feedback Loop", "10", False, 2),
        ("4.4 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)", "11", False, 1),
        ("4.5 Mathematical Formulation of the CHDI Analytical Engine", "12", False, 1),
        ("4.5.1 Stage 1: Individual Baseline Calibration (Equations 4.1, 4.2, 4.3)", "12", False, 2),
        ("4.5.2 Stage 2: Regularized Mahalanobis Distance (Equations 4.4, 4.5, 4.6)", "12", False, 2),
        ("4.5.3 Stage 3: LOCO Feature Attribution (Equations 4.7, 4.8, 4.9)", "13", False, 2),
        ("4.5.4 CHDI Clinical Severity Bands and Action Protocols", "13", False, 2),
        ("4.6 Database Design & Prisma Schema Entities", "14", False, 1),
        ("4.7 Technology Stack of the Prototype", "14", False, 1),
        ("4.8 Core Algorithmic Procedures & Pseudocode (Algorithm 4.1)", "15", False, 1),
        ("4.9 Source Code Listings & Implementations", "15", False, 1),
        ("4.9.1 Production TypeScript CHDI Client & Data Pipeline", "15", False, 2),
        ("4.9.2 Python FastAPI Three-Stage CHDI Analytics Engine", "16", False, 2),
        ("4.9.3 Prisma Database Schema & Entity Relational Definitions", "17", False, 2),
        ("4.9.4 Active Veterinary Feedback Learning Classifier", "18", False, 2),
        ("CHAPTER 5: EXPERIMENTAL RESULTS AND DISCUSSION", "19", True, 0),
        ("5.1 Experimental Setup & Benchmark Cohort Provenance", "19", False, 1),
        ("5.2 Evaluation Metrics", "19", False, 1),
        ("5.3 Detection and Diagnostic Results Across Bovine Conditions", "19", False, 1),
        ("5.4 Longitudinal Clinical Case Trace & Explainability Walkthrough", "20", False, 1),
        ("5.5 Algorithmic Ablation Study", "21", False, 1),
        ("5.6 Predictive Lead Time & Early Intervention Advantage", "21", False, 1),
        ("5.7 Response Time, Computational Latency and Edge Footprint", "22", False, 1),
        ("5.8 Benchmarking with Commercial Wearable IoT Platforms", "22", False, 1),
        ("5.9 Limitations of the Evaluation", "22", False, 1),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", "23", True, 0),
        ("6.1 Conclusion", "23", False, 1),
        ("6.2 Summary of Key Contributions", "23", False, 1),
        ("6.3 Future Scope", "23", False, 1),
        ("REFERENCES", "24", True, 0),
        ("APPENDIX", "24", True, 0),
        ("A.1 Summary of Mathematical Notation", "24", False, 1),
        ("A.2 Evaluation Protocol Summary", "24", False, 1),
        ("A.3 Reproducibility Checklist", "24", False, 1)
    ]

    for title, pg, is_b, ind in toc_structure:
        add_dot_leader_line(title, pg, is_bold=is_b, indent_spaces=ind)

    doc.add_page_break()

    # ==========================================
    # LIST OF TABLES (Page viii)
    # ==========================================
    add_chapter_heading("LIST OF TABLES")
    add_dot_leader_header("TABLE NO. & TITLE", "PAGE NO.")

    lot_items = [
        ("Table 2.1  Feature Comparison: Proposed System vs. Related Approaches", "5"),
        ("Table 3.1  Comparison of Existing Cattle Healthcare Techniques", "6"),
        ("Table 3.2  System Feasibility Analysis Matrix for SmartCattle Deployment", "8"),
        ("Table 4.1  CHDI Severity Bands, Score Ranges, and Clinical Protocols", "13"),
        ("Table 4.2  Prisma Database Schema Entities and Relational Mappings", "14"),
        ("Table 4.3  Technology Stack of the SmartCattle Research Prototype", "14"),
        ("Table 4.4  Core Algorithmic Procedures of the SmartCattle CHDI Framework", "15"),
        ("Table 5.1  Benchmark Experimental Cohort Breakdown and Ground Truth", "19"),
        ("Table 5.2  Diagnostic Performance Metrics for Common Bovine Pathologies", "19"),
        ("Table 5.3  Anomaly Detection Performance Metrics & Algorithmic Ablation", "21"),
        ("Table 5.4  Subclinical Disease Lead Time and Early Intervention Advantage", "21"),
        ("Table 5.5  End-to-End Latency and Computational Footprint Breakdown", "22"),
        ("Table 5.6  Benchmarking SmartCattle against Commercial Wearable IoT Solutions", "22"),
        ("Table A.1  Summary of Mathematical Notations and Variable Definitions", "24")
    ]
    for item_tit, pg in lot_items:
        add_dot_leader_line(item_tit, pg, is_bold=False, indent_spaces=0)

    doc.add_page_break()

    # ==========================================
    # LIST OF FIGURES (Page ix)
    # ==========================================
    add_chapter_heading("LIST OF FIGURES")
    add_dot_leader_header("FIGURE NO. & TITLE", "PAGE NO.")

    lof_items = [
        ("Figure 4.1  Multi-Tier System Architecture of the Proposed QR-Based Platform", "9"),
        ("Figure 4.2  Three-Stage CHDI Analytics Engine Operational Workflow", "10"),
        ("Figure 4.3  Level 0 Context Diagram (DFD Level 0) for SmartCattle Platform", "11"),
        ("Figure 4.4  Level 1 Data Flow Diagram (DFD Level 1) for Telemetry Ingestion", "11"),
        ("Figure 5.1  Cohort Herd Status and Risk Distribution Breakdown across Trial", "20"),
        ("Figure 5.2  Longitudinal CHDI Score Trajectory Demonstrating Pre-Clinical Lead Time", "20"),
        ("Figure 5.3  Leave-One-Covariate-Out (LOCO) Feature Attribution Ranking", "20")
    ]
    for item_tit, pg in lof_items:
        add_dot_leader_line(item_tit, pg, is_bold=False, indent_spaces=0)

    doc.add_page_break()

    # ==========================================
    # LIST OF ABBREVIATIONS (Page x)
    # ==========================================
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

    # ==========================================
    # SECTION 2: MAIN REPORT (Starting at Page 1)
    # ==========================================
    sec2 = doc.add_section(docx.enum.section.WD_SECTION_START.NEW_PAGE)
    sec2.top_margin = Inches(1.0)
    sec2.bottom_margin = Inches(1.0)
    sec2.left_margin = Inches(1.25)
    sec2.right_margin = Inches(1.0)
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)

    sectPr2 = sec2._sectPr
    pgNumType2 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="1" w:fmt="decimal"/>')
    sectPr2.append(pgNumType2)

    footer2 = sec2.footer
    f_p = footer2.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run = f_p.add_run()
    f_run.font.name = 'Times New Roman'
    f_run.font.size = Pt(10)
    f_run.font.color.rgb = COLOR_MUTED
    fPr = f_run._r.get_or_add_rPr()
    f_xml = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
    f_p._p.append(f_xml)

    # ==========================================
    # CHAPTER 1: INTRODUCTION (Page 1)
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
    add_body_p("The proposed system operates as an integrated closed loop connecting edge data acquisition, serverless cloud processing, scientific anomaly detection, and clinical veterinary action. When a farmer scans an animal's weatherproof QR tag using a standard smartphone web browser, the encrypted UUID resolves the animal's identity without requiring native app installation. The farmer logs daily routine observations (milk yield, core temperature, rumination duration, activity counts, feed intake).")
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
    # CHAPTER 2: LITERATURE REVIEW (Page 4)
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
    # CHAPTER 3: EXISTING SYSTEM VS PROPOSED SYSTEM (Page 6)
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
            "• Farmer digital literacy\n• Daily data entry workflow\n• Veterinary workflow alignment\n• Tag physical durability",
            "• FEASIBLE: Simple vernacular UI designed for 1-click scanning\n• Logging routine takes < 15 seconds per cow during routine milking\n• Triage dashboard ranks urgent cases automatically for veterinarians\n• Weatherproof laser-etched TPU tags withstand UV, mud, and water"
        ]
    ]
    add_normal_table(
        feas_headers,
        feas_data,
        [Inches(1.5), Inches(1.8), Inches(2.7)],
        "Table 3.2: System Feasibility Analysis Matrix for Proposed System Deployment"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: PROPOSED FRAMEWORK, ARCHITECTURE AND IMPLEMENTATION (Page 9)
    # ==========================================
    add_chapter_heading("PROPOSED FRAMEWORK, ARCHITECTURE AND IMPLEMENTATION", chapter_number=4)

    add_sec_heading_2("4.1 Overview of the Proposed System Framework")
    add_body_p("The proposed system platform is architected around four core engineering principles designed specifically for smallholder dairy ecosystems:")
    add_list_item("1. Zero Capital Barrier:", "No active electronic hardware on the animal; all physical tagging utilizes weatherproof laser-etched TPU ear tags costing under $0.50 per unit.")
    add_list_item("2. Sub-50ms Inference Latency:", "End-to-end telemetry ingestion and multivariate anomaly scoring execute directly in edge microservices to deliver instantaneous feedback to farmers.")
    add_list_item("3. Strict Role-Based Security:", "Multi-tenant isolation ensuring farmers access only their herd while regional veterinary officers have triage oversight across assigned geographical clusters.")
    add_list_item("4. Explainable Clinical Output:", "Every diagnostic prediction must be decomposed into human-interpretable feature attributions, enabling veterinarians to trust and act on alerts.")

    add_sec_heading_2("4.2 System Architecture and Threat / Data Integrity Model")
    add_body_p("Figure 4.1 depicts the four-tier system architecture, illustrating the interactions between edge scanning, API routing, scientific computing, and clinical triage.")
    add_figure_item("generated_figures/fig_4_1_architecture.png", "Figure 4.1: Multi-Tier System Architecture of the Proposed QR-Based Platform")

    add_sec_heading_2("4.3 Four-Tier Architectural Subsystems")
    
    add_sec_heading_3("4.3.1 Tier 1: Identification & Edge Data Acquisition Layer")
    add_body_p("Utilizes high-contrast QR matrices laser-etched onto TPU ear tags. When scanned by a standard smartphone camera using html5-qrcode running inside Chrome/Safari, the encrypted QR URL resolves to the cow's digital profile. The farmer inputs 5 vital observations: milk yield (L/day), core temperature (°C), rumination duration (min/day), activity count (steps/day), and feed intake (kg/day).")

    add_sec_heading_3("4.3.2 Tier 2: Cloud Platform, API Gateway, and Security Layer")
    add_body_p("Engineered with Next.js 14 App Router, TypeScript, and Server Actions. API requests are authenticated via NextAuth.js session tokens with Role-Based Access Control (RBAC: Farmer, Veterinarian, Admin). Database operations execute via Prisma ORM connected to serverless PostgreSQL on Neon.")

    add_sec_heading_3("4.3.3 Tier 3: Three-Stage CHDI Analytics Engine")
    add_body_p("The analytical core of the proposed system, executing longitudinal baseline estimation, regularized Mahalanobis distance calculation, and LOCO feature attribution.")
    add_figure_item("generated_figures/fig_4_2_flowchart.png", "Figure 4.2: Three-Stage CHDI Analytics Engine Operational Workflow")

    add_sec_heading_3("4.3.4 Tier 4: Clinical Triage and Veterinary Feedback Loop")
    add_body_p("If an animal's CHDI score enters the elevated alert tier (CHDI ≥ 51), an automated triage ticket is pushed to the veterinary dashboard. Regional veterinarians review explainable feature rankings and log clinical diagnoses.")

    add_sec_heading_2("4.4 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)")
    add_body_p("Data Flow Diagrams capture how information propagates through the system during telemetry ingestion, anomaly scoring, and veterinary triage.")
    add_figure_item("generated_figures/fig_4_3_dfd0.png", "Figure 4.3: Level 0 Context Diagram (DFD Level 0) for Proposed System Platform")
    add_figure_item("generated_figures/fig_4_4_dfd1.png", "Figure 4.4: Level 1 Data Flow Diagram (DFD Level 1) for Telemetry Ingestion")

    add_sec_heading_2("4.5 Mathematical Formulation of the CHDI Analytical Engine")
    add_body_p("The Composite Health Deviation Index (CHDI) algorithm transforms raw, heterogeneous daily observations into a calibrated, explainable health metric.")

    add_sec_heading_3("4.5.1 Stage 1: Individual Baseline Calibration & Normalized Deviations")
    add_body_p("For each individual animal i across each physiological channel j over a rolling historical baseline window W = 14 days:")
    
    add_equation_block(
        "generated_equations/eq_1.png",
        "4.1",
        "Individual Moving-Average Baseline Mean",
        "Computes the personalized rolling average of each health metric for an individual cow over the past 14 days.",
        {"\\mu_{i,j}(t)": "14-day rolling average for cow i and vital sign j", "x_{i,j}(t-k)": "Actual recorded vital measurement k days ago", "W": "Baseline window length (14 days)"},
        "Eliminates breed, parity, and seasonal biases by measuring each cow against its own normal healthy history rather than an arbitrary population standard."
    )

    add_equation_block(
        "generated_equations/eq_2.png",
        "4.2",
        "Rolling Sample Variance with Bessel's Correction",
        "Calculates the natural daily biological variability (spread) for each health parameter.",
        {"\\sigma_{i,j}^2(t)": "Sample variance for cow i and signal j", "W-1": "Bessel's correction factor ensuring an unbiased variance estimate"},
        "Accounts for natural physiological fluctuations; prevents false alarms for cows that naturally exhibit higher day-to-day variance."
    )

    add_equation_block(
        "generated_equations/eq_3.png",
        "4.3",
        "Standardized Normalized Deviation Vector",
        "Normalizes differences between today's readings and historical baselines into standard deviation units (z-scores).",
        {"z_{i,j}(t)": "Standardized deviation z-score", "x_{i,j}(t)": "Today's recorded observation", "\\sigma_{i,j}(t)": "Baseline standard deviation"},
        "Converts disparate physical units (liters, degrees Celsius, minutes) into a dimensionless, scale-invariant representation suitable for multivariate analysis."
    )

    add_sec_heading_3("4.5.2 Stage 2: Multivariate Covariance & Regularized Mahalanobis Distance")
    add_body_p("To capture inter-variable physiological correlations while preventing mathematical instability during data logging gaps:")

    add_equation_block(
        "generated_equations/eq_4.png",
        "4.4",
        "Empirical Telemetry Covariance Matrix",
        "Measures how pairs of physiological metrics naturally change together over time.",
        {"\\boldsymbol{\\Sigma}_i(t)": "d x d Covariance matrix (5x5 matrix for 5 vital signs)", "\\mathbf{z}_i": "Multivariate normalized deviation vector"},
        "Captures critical physiological couplings—such as elevated body temperature occurring simultaneously with dropped milk yield and reduced rumination."
    )

    add_equation_block(
        "generated_equations/eq_5.png",
        "4.5",
        "Tikhonov-Regularized Covariance Inversion",
        "Adds a small positive ridge penalty along the matrix diagonal to make matrix inversion stable.",
        {"\\boldsymbol{\\Sigma}_{i,\\text{reg}}^{-1}": "Regularized inverse covariance matrix (precision matrix)", "\\lambda": "Tikhonov ridge parameter (1e-3)", "\\mathbf{I}": "Identity matrix"},
        "Prevents mathematical crashes (division by zero / matrix singularity) when two vital metrics are temporarily collinear or during sparse data entry."
    )

    add_equation_block(
        "generated_equations/eq_6.png",
        "4.6",
        "Tikhonov-Regularized Multivariate Mahalanobis Distance",
        "Calculates the multidimensional statistical distance between today's combined health state and historical homeostasis.",
        {"D_M(t)": "Mahalanobis anomaly distance", "\\mathbf{z}_i(t)": "Multivariate deviation vector", "\\boldsymbol{\\Sigma}_{i,\\text{reg}}^{-1}": "Regularized precision matrix"},
        "Detects subtle multi-signal departures that would evade single-threshold monitors, enabling subclinical disease detection 24 to 48 hours earlier."
    )

    add_sec_heading_3("4.5.3 Stage 3: LOCO Feature Attribution & Confidence Gating")
    add_body_p("To explain predictions to veterinarians and farmers, Leave-One-Covariate-Out (LOCO) permutation isolates individual feature contributions:")

    add_equation_block(
        "generated_equations/eq_7.png",
        "4.7",
        "LOCO Marginal Distance Delta",
        "Quantifies how much the overall anomaly score drops when a specific physiological metric is masked out.",
        {"\\Delta D_k(t)": "Marginal distance contribution of vital sign k", "D_M(t)": "Full multivariate anomaly score", "D_{M,(-k)}(t)": "Anomaly score recomputed with feature k omitted"},
        "Directly isolates and measures the standalone impact of each vital sign on the animal's elevated health risk."
    )

    add_equation_block(
        "generated_equations/eq_8.png",
        "4.8",
        "Percentage Feature Contribution Attribution",
        "Normalizes individual feature deltas into intuitive percentage shares summing to 100%.",
        {"C_k(t)": "Percentage contribution of signal k", "\\Delta D_k(t)": "Individual feature delta", "\\sum_m \\Delta D_m": "Total sum of all feature deltas"},
        "Translates complex machine learning math into clear clinical insights (e.g., 'Milk Yield Drop contributed 54% to this mastitis alert')."
    )

    add_equation_block(
        "generated_equations/eq_9.png",
        "4.9",
        "Baseline Confidence Scaling Metric",
        "Scales diagnostic confidence from 0.0 to 1.0 based on how many baseline days have been recorded.",
        {"\\rho(t)": "Baseline maturity confidence score", "N_{\\text{obs}}": "Number of logged observation days", "W": "Baseline window length (14 days)"},
        "Safeguards against premature false alarms during the first week of cow enrollment while full baselines are being established."
    )

    add_sec_heading_3("4.5.4 CHDI Clinical Severity Bands and Action Protocols")
    add_body_p("Table 4.1 outlines the standardized clinical severity triage bands and action protocols.")

    band_headers = ["CHDI Range", "Clinical Classification", "Color Indicator", "Automated Triage Action Protocol"]
    band_data = [
        ["0 – 25", "Normal / Homeostatic", "Green (#2E7D32)", "Routine daily monitoring; no clinical intervention required."],
        ["26 – 50", "Mild Deviation / Watchlist", "Yellow (#F9A825)", "Flagged on farmer dashboard; re-inspect rumination & temperature next milking."],
        ["51 – 75", "Elevated / Veterinary Review", "Orange (#E65100)", "Automated alert dispatched to veterinarian; clinical examination recommended."],
        ["76 – 100", "Critical / Urgent Triage", "Red (#C62828)", "High-priority emergency notification; immediate veterinary intervention protocol."]
    ]
    add_normal_table(
        band_headers,
        band_data,
        [Inches(1.0), Inches(1.8), Inches(1.3), Inches(1.9)],
        "Table 4.1: CHDI Severity Bands, Score Ranges, and Clinical Protocols (IEEE Paper Table II)"
    )

    add_sec_heading_2("4.6 Database Design & Prisma Schema Entities")
    add_body_p("The relational architecture uses PostgreSQL via Prisma ORM. Table 4.2 details the entity schemas.")

    db_headers = ["Entity / Model", "Key Attributes & Types", "Relational Mappings & Constraints"]
    db_data = [
        ["User", "id (UUID), email (String), role (Enum: FARMER, VET, ADMIN)", "1-to-Many with Cattle; 1-to-Many with TriageReview"],
        ["Cattle", "id (UUID), tagNumber (String, Unique), breed, birthDate", "Belongs to User; 1-to-Many with DailyLog, Anomaly, MedicalHistory"],
        ["DailyLog", "id (UUID), cattleId, milkYield, temp, rumination, activity, feed", "Belongs to Cattle; Indexed on (cattleId, date) for sub-10ms lookup"],
        ["AnomalyScore", "id (UUID), cattleId, chdiScore (Float), status, topDriver", "Belongs to Cattle; 1-to-1 with TriageTicket; Indexed on status"],
        ["TriageTicket", "id (UUID), anomalyId, vetId, priority, status, diagnosis", "Belongs to AnomalyScore; Belongs to User (Veterinarian)"],
        ["MedicalHistory", "id (UUID), cattleId, diagnosis, treatment, drugAdministered", "Belongs to Cattle; Logged upon clinical resolution"]
    ]
    add_normal_table(
        db_headers,
        db_data,
        [Inches(1.3), Inches(2.4), Inches(2.3)],
        "Table 4.2: Prisma Database Schema Entities and Relational Mappings"
    )

    add_sec_heading_2("4.7 Technology Stack of the Prototype")
    add_body_p("Table 4.3 details the comprehensive technology stack selected for the research prototype.")

    tech_headers = ["Layer / Subsystem", "Framework / Tool", "Rationale & Operational Benefit"]
    tech_data = [
        ["Frontend UI", "Next.js 14 / React 18", "Server Components reduce client bundle size; instant edge page rendering."],
        ["Styling & Theming", "Vanilla CSS / Design Tokens", "Zero stylesheet compilation overhead; full layout control without CSS bloat."],
        ["Language & Types", "TypeScript 5.3", "End-to-end type safety eliminating runtime null pointer bugs."],
        ["Database & ORM", "PostgreSQL (Neon) / Prisma", "Serverless auto-scaling with instant branch testing and ACID compliance."],
        ["ML Microservice", "Python 3.11 / FastAPI", "High-performance vector operations via NumPy/SciPy with OpenAPI docs."],
        ["QR Decoding", "html5-qrcode (WASM)", "In-browser native camera scanning at 30 FPS without app installation."]
    ]
    add_normal_table(
        tech_headers,
        tech_data,
        [Inches(1.5), Inches(1.8), Inches(2.7)],
        "Table 4.3: Technology Stack of the Proposed System Research Prototype"
    )

    add_sec_heading_2("4.8 Core Algorithmic Procedures & Pseudocode (Algorithm 4.1)")
    add_body_p("Algorithm 4.1 summarizes the complete operational procedure executed during each telemetry ingestion cycle.")

    tbl_algo = doc.add_table(rows=1, cols=1)
    tbl_algo.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_algo, color=HEX_NORMAL_BORDER, sz="6", val="single")
    cell_algo = tbl_algo.rows[0].cells[0]
    cell_algo.width = Inches(6.0)
    set_cell_background(cell_algo, HEX_ALGO_BG)
    set_cell_margins(cell_algo, top=100, bottom=100, left=140, right=140)
    prevent_row_split(tbl_algo.rows[0])

    p_algo = cell_algo.paragraphs[0]
    p_algo.paragraph_format.space_after = Pt(2)
    p_algo.paragraph_format.line_spacing = 1.25
    
    algo_lines = [
        ("Algorithm 4.1: ", True, "End-to-End CHDI Ingestion, Anomaly Scoring, and Triage Workflow"),
        ("Input: ", True, "Daily observation vector x_i(t) in R^d; Historical window W = 14; Ridge parameter lambda = 1e-3"),
        ("Output: ", True, "CHDI score in [0, 100]; LOCO feature ranking {C_k}; Clinical Triage Alert"),
        ("1:  Begin Ingestion Routine", True, ""),
        ("2:      Retrieve historical observation matrix X_i in R^(N x d) from Prisma cache", False, ""),
        ("3:      If N_obs < 7 then return Status: BASELINE_CALIBRATING (withhold score)", False, ""),
        ("4:      Compute rolling baseline mean mu_i(t) via Equation (4.1)", False, ""),
        ("5:      Compute rolling sample variance sigma_i^2(t) with Bessel's correction via Equation (4.2)", False, ""),
        ("6:      Standardize input vector z_i(t) = (x_i(t) - mu_i(t)) / sigma_i(t) via Equation (4.3)", False, ""),
        ("7:      Compute empirical covariance matrix Sigma_i(t) via Equation (4.4)", False, ""),
        ("8:      Apply Tikhonov ridge regularization Sigma_reg = Sigma_i(t) + lambda * I", False, ""),
        ("9:      Compute precision matrix Sigma_reg^(-1) via Cholesky decomposition", False, ""),
        ("10:     Compute Mahalanobis distance D_M(t) = sqrt(z_i^T * Sigma_reg^(-1) * z_i) via Equation (4.6)", False, ""),
        ("11:     Scale raw distance to CHDI(t) = min(100, (D_M(t) / D_max) * 100)", False, ""),
        ("12:     For each feature k in {1, ..., d} do", False, ""),
        ("13:         Mask feature k: z_(-k) = z_i with z_k = 0", False, ""),
        ("14:         Compute omitted distance D_M,(-k)(t)", False, ""),
        ("15:         Compute marginal contribution Delta D_k(t) = max(0, D_M(t) - D_M,(-k)(t))", False, ""),
        ("16:     End For", False, ""),
        ("17:     Compute relative feature attributions C_k(t) = (Delta D_k / sum(Delta D)) * 100 via Equation (4.8)", False, ""),
        ("18:     If CHDI(t) >= 51 then", True, ""),
        ("19:         Instantiate TriageTicket in PostgreSQL queue; dispatch push notification to regional vet", False, ""),
        ("20:     End If", False, ""),
        ("21:     Return {CHDI(t), C_1..d, TriageStatus}", True, "")
    ]
    for pre, is_b, txt in algo_lines:
        r1 = p_algo.add_run(pre)
        r1.font.name = 'Courier New'
        r1.font.size = Pt(9.5)
        r1.bold = is_b
        r1.font.color.rgb = COLOR_BLACK
        if txt:
            r2 = p_algo.add_run(txt + "\n")
            r2.font.name = 'Courier New'
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = COLOR_DARK

    p_after_a = doc.add_paragraph()
    p_after_a.paragraph_format.space_after = Pt(6)

    add_body_p("Table 4.4 details the systematic step-by-step procedure of Algorithm 4.1.")

    algo_proc_headers = ["Step / Stage", "Procedure Name", "Mathematical / Logical Function", "Output Artifact"]
    algo_proc_data = [
        ["Step 1", "Telemetry Ingestion", "Camera QR scan authenticates animal UUID; forms vector x_i(t)", "Observation Vector"],
        ["Step 2", "Baseline Calibration", "Calculates rolling mean mu_i and variance sigma_i^2 (ddof=1)", "Z-Score Vector z_i(t)"],
        ["Step 3", "Tikhonov Regularization", "Adds lambda * I (1e-3) to covariance matrix Sigma_i", "Invertible Precision Matrix"],
        ["Step 4", "Mahalanobis Scoring", "Calculates multivariate quadratic form sqrt(z^T * Sigma^(-1) * z)", "CHDI Score [0, 100]"],
        ["Step 5", "LOCO Feature Attribution", "Iteratively sets z_k = 0; computes Delta D_k and relative % shares", "Ranked Drivers {C_k}"],
        ["Step 6", "Automated Triage Dispatch", "Gating rule: If CHDI >= 51, push urgent ticket to assigned vet", "Triage Ticket & Notification"]
    ]
    add_normal_table(
        algo_proc_headers,
        algo_proc_data,
        [Inches(1.0), Inches(1.6), Inches(2.2), Inches(1.2)],
        "Table 4.4: Core Algorithmic Procedures of the Proposed System CHDI Framework"
    )

    # ==========================================
    # 4.9 SOURCE CODE LISTINGS & IMPLEMENTATIONS
    # ==========================================
    add_sec_heading_2("4.9 Source Code Listings & Implementations")
    add_body_p("This section presents the production-grade source code implementations of the four core subsystems underpinning the proposed system platform.")

    # 4.9.1 TypeScript Client
    add_sec_heading_3("4.9.1 Production TypeScript CHDI Client & Data Pipeline (lib/chdi/anomaly.ts)")
    add_body_p("Listing 4.1 shows the full TypeScript client executing multi-table PostgreSQL telemetry aggregation via Prisma ORM, constructing normalized deviation vectors, and querying the Python ML microservice.")

    code_ts = (
        "import prisma from '@/lib/prisma';\n\n"
        "export interface DeviationVector {\n"
        "  weightDeviation: number;\n"
        "  feedDeviation: number;\n"
        "  activityDeviation: number;\n"
        "  milkDeviation?: number;\n"
        "  temperatureDeviation?: number;\n"
        "  ruminationDeviation?: number;\n"
        "}\n\n"
        "export interface FactorAttribution {\n"
        "  factor: string;\n"
        "  label: string;\n"
        "  contribution_percentage: number;\n"
        "  direction: string;\n"
        "  z_score: number;\n"
        "  farmer_summary: string;\n"
        "  vet_summary: string;\n"
        "}\n\n"
        "export interface CHDIResult {\n"
        "  score: number | null; // 0–100; null when baseline calibrating\n"
        "  confidence: number;   // 0–1\n"
        "  status: 'healthy' | 'watch' | 'at-risk' | 'abstain';\n"
        "  rawDistance: number;\n"
        "  deviationVector: DeviationVector;\n"
        "  topFactors?: FactorAttribution[];\n"
        "  farmerText?: string;\n"
        "  vetText?: string;\n"
        "}\n\n"
        "export async function computeCHDI(\n"
        "  deviationVector: DeviationVector,\n"
        "  cattleId: string\n"
        "): Promise<CHDIResult> {\n"
        "  const since = new Date(Date.now() - 90 * 86400000); // 90-day window\n"
        "  const [weightRows, feedRows, activityRows, milkRows, tempRows, rumRows] = await Promise.all([\n"
        "    prisma.weightLog.findMany({ where: { cattleId, timestamp: { gte: since } }, orderBy: { timestamp: 'asc' } }),\n"
        "    prisma.feedLog.findMany({ where: { cattleId, timestamp: { gte: since } }, orderBy: { timestamp: 'asc' } }),\n"
        "    prisma.activityLog.findMany({ where: { cattleId, timestamp: { gte: since } }, orderBy: { timestamp: 'asc' } }),\n"
        "    prisma.milkLog.findMany({ where: { cattleId, timestamp: { gte: since } }, orderBy: { timestamp: 'asc' } }),\n"
        "    (prisma as any).temperatureLog?.findMany({ where: { cattleId, timestamp: { gte: since } } }) || Promise.resolve([]),\n"
        "    (prisma as any).ruminationLog?.findMany({ where: { cattleId, timestamp: { gte: since } } }) || Promise.resolve([])\n"
        "  ]);\n\n"
        "  const historicalPayload = [];\n"
        "  const maxLen = Math.max(weightRows.length, feedRows.length, activityRows.length, milkRows.length, tempRows.length, rumRows.length);\n"
        "  for (let i = 0; i < maxLen; i++) {\n"
        "    historicalPayload.push({\n"
        "      timestamp: (weightRows[i]?.timestamp || new Date()).toISOString(),\n"
        "      milk: milkRows[i]?.litres ?? null,\n"
        "      rumination: rumRows[i]?.minutes ?? null,\n"
        "      temperature: tempRows[i]?.value ?? null,\n"
        "      activity: activityRows[i]?.value ?? null,\n"
        "      feed: feedRows[i]?.quantity ?? null,\n"
        "      weight: weightRows[i]?.value ?? null\n"
        "    });\n"
        "  }\n\n"
        "  const pyRes = await fetch('http://127.0.0.1:8000/api/v1/chdi/compute', {\n"
        "    method: 'POST',\n"
        "    headers: { 'Content-Type': 'application/json' },\n"
        "    body: JSON.stringify({\n"
        "      cattle_id: cattleId,\n"
        "      current_observation: {\n"
        "        milk: deviationVector.milkDeviation !== undefined ? 25.0 + deviationVector.milkDeviation * 3.0 : null,\n"
        "        rumination: deviationVector.ruminationDeviation !== undefined ? 500.0 + deviationVector.ruminationDeviation * 40.0 : null,\n"
        "        temperature: deviationVector.temperatureDeviation !== undefined ? 38.6 + deviationVector.temperatureDeviation * 0.4 : null,\n"
        "        activity: 65.0 + deviationVector.activityDeviation * 8.0,\n"
        "        feed: 12.0 + deviationVector.feedDeviation * 1.5,\n"
        "        weight: 350.0 + deviationVector.weightDeviation * 15.0\n"
        "      },\n"
        "      historical_observations: historicalPayload,\n"
        "      min_confidence: 0.4,\n"
        "      min_history_days: 7\n"
        "    })\n"
        "  });\n\n"
        "  const pyData = await pyRes.json();\n"
        "  return {\n"
        "    score: pyData.score,\n"
        "    confidence: pyData.confidence,\n"
        "    status: pyData.status,\n"
        "    rawDistance: pyData.raw_distance,\n"
        "    deviationVector,\n"
        "    topFactors: pyData.top_factors,\n"
        "    farmerText: pyData.farmer_text,\n"
        "    vetText: pyData.vet_text\n"
        "  };\n"
        "}"
    )
    add_code_block("Listing 4.1: Production TypeScript CHDI Ingestion Client (lib/chdi/anomaly.ts)", code_ts)

    # 4.9.2 Python ML Engine
    add_sec_heading_3("4.9.2 Python FastAPI Three-Stage CHDI Analytics Engine (ml_service/chdi.py)")
    add_body_p("Listing 4.2 details the mathematical execution of Bessel-corrected moving averages, Tikhonov-regularized covariance inversion, Mahalanobis distance calculation, and LOCO feature attribution.")

    code_py = (
        "import numpy as np\n"
        "from scipy.spatial.distance import mahalanobis\n"
        "from typing import List, Dict, Tuple, Optional\n\n"
        "DEFAULT_WINDOW_SIZE = 14    # Rolling window W = 14 days\n"
        "TIKHONOV_LAMBDA = 1e-3      # Regularization ridge lambda = 10^-3\n"
        "D_MAX = 4.0                 # Normalization boundary (4.0 sigma)\n"
        "N_SATURATION = 14           # Confidence maturity threshold\n"
        "EPSILON = 1e-4\n\n"
        "def compute_stage1_baseline(history: List[dict], signal: str, window: int = 14) -> Tuple[float, float, int]:\n"
        "    vals = [h[signal] for h in history if h.get(signal) is not None]\n"
        "    if not vals: return 0.0, 1.0, 0\n"
        "    recent = vals[-window:]\n"
        "    mean = float(np.mean(recent))\n"
        "    std = float(np.std(recent, ddof=1)) if len(recent) > 1 else 1.0\n"
        "    return mean, max(std, EPSILON), len(vals)\n\n"
        "def compute_chdi_pipeline(req: dict) -> dict:\n"
        "    history = req['historical_observations']\n"
        "    current = req['current_observation']\n"
        "    active_signals = ['milk', 'rumination', 'temperature', 'activity', 'feed', 'weight']\n"
        "    num_points = len(history)\n\n"
        "    if num_points < 7:\n"
        "        return {'status': 'abstain', 'score': None, 'confidence': round(num_points / 14.0, 3)}\n\n"
        "    # Stage 1: Z-score Normalization\n"
        "    z_scores, means, stds, cur_vec = {}, {}, {}, []\n"
        "    for s in active_signals:\n"
        "        mu, sigma, _ = compute_stage1_baseline(history, s)\n"
        "        val = current.get(s, mu)\n"
        "        z = (val - mu) / sigma\n"
        "        z_scores[s], means[s], stds[s] = z, mu, sigma\n"
        "        cur_vec.append(z)\n\n"
        "    # Stage 2: Tikhonov Regularized Mahalanobis Distance\n"
        "    hist_mat = []\n"
        "    for h in history[-14:]:\n"
        "        row = [(h.get(s, means[s]) - means[s]) / stds[s] for s in active_signals]\n"
        "        hist_mat.append(row)\n"
        "    hist_arr = np.array(hist_mat, dtype=float)\n"
        "    cov = np.cov(hist_arr, rowvar=False) if len(hist_arr) > 2 else np.eye(len(active_signals))\n"
        "    reg_cov = cov + np.eye(len(active_signals)) * TIKHONOV_LAMBDA\n"
        "    inv_cov = np.linalg.pinv(reg_cov)\n"
        "    raw_dist = float(mahalanobis(cur_vec, np.zeros(len(active_signals)), inv_cov))\n"
        "    score = min(100.0, max(0.0, (raw_dist / D_MAX) * 100.0))\n\n"
        "    # Stage 3: LOCO Feature Attribution\n"
        "    deltas = {}\n"
        "    for idx, s in enumerate(active_signals):\n"
        "        masked = list(cur_vec); masked[idx] = 0.0\n"
        "        d_omitted = float(mahalanobis(masked, np.zeros(len(active_signals)), inv_cov))\n"
        "        deltas[s] = max(0.0, raw_dist - d_omitted)\n"
        "    sum_d = sum(deltas.values()) or 1.0\n"
        "    factors = [{'factor': s, 'contrib_pct': round((d / sum_d) * 100, 1)} for s, d in deltas.items()]\n"
        "    return {'score': round(score, 1), 'raw_distance': round(raw_dist, 3), 'top_factors': factors}\n"
    )
    add_code_block("Listing 4.2: Python FastAPI Three-Stage CHDI Scientific Analytics Engine (ml_service/chdi.py)", code_py)

    # 4.9.3 Prisma Schema
    add_sec_heading_3("4.9.3 Prisma Database Schema & Relational Definitions (prisma/schema.prisma)")
    add_body_p("Listing 4.3 presents the core database entity schema defining User roles, Cattle assets, time-series physiological tables, and clinical triage review logs.")

    code_prisma = (
        "datasource db {\n"
        "  provider  = 'postgresql'\n"
        "  url       = env('DATABASE_URL')\n"
        "}\n\n"
        "generator client {\n"
        "  provider = 'prisma-client-js'\n"
        "}\n\n"
        "enum Role { farmer, vet, admin }\n"
        "enum CaseStatus { open, in_progress, resolved, closed }\n\n"
        "model User {\n"
        "  id             String    @id @default(cuid())\n"
        "  name           String\n"
        "  email          String    @unique\n"
        "  role           Role\n"
        "  cattle         Cattle[]  @relation('FarmerCattle')\n"
        "  vetCases       VetCase[] @relation('VetCases')\n"
        "}\n\n"
        "model Cattle {\n"
        "  id             String    @id @default(cuid())\n"
        "  farmerId       String\n"
        "  tagId          String    @unique\n"
        "  qrToken        String    @unique\n"
        "  breed          String\n"
        "  dob            DateTime\n"
        "  farmer         User      @relation('FarmerCattle', fields: [farmerId], references: [id])\n"
        "  milkLogs       MilkLog[]\n"
        "  tempLogs       TemperatureLog[]\n"
        "  ruminationLogs RuminationLog[]\n"
        "  chdiHistory    CHDIEntry[]\n"
        "  vetCases       VetCase[]\n"
        "}\n\n"
        "model MilkLog {\n"
        "  id        String   @id @default(cuid())\n"
        "  cattleId  String\n"
        "  litres    Float\n"
        "  timestamp DateTime @default(now())\n"
        "  cattle    Cattle   @relation(fields: [cattleId], references: [id], onDelete: Cascade)\n"
        "}\n\n"
        "model CHDIEntry {\n"
        "  id         String   @id @default(cuid())\n"
        "  cattleId   String\n"
        "  score      Float?   // 0–100 score; null if calibrating\n"
        "  status     String   // healthy | watch | at-risk | abstain\n"
        "  confidence Float\n"
        "  topFactors Json\n"
        "  timestamp  DateTime @default(now())\n"
        "  cattle     Cattle   @relation(fields: [cattleId], references: [id], onDelete: Cascade)\n"
        "}\n\n"
        "model VetCase {\n"
        "  id           String     @id @default(cuid())\n"
        "  cattleId     String\n"
        "  vetId        String?\n"
        "  status       CaseStatus @default(open)\n"
        "  chdiSnapshot Json\n"
        "  diagnosis    String?\n"
        "  treatment    String?\n"
        "  createdAt    DateTime   @default(now())\n"
        "  cattle       Cattle     @relation(fields: [cattleId], references: [id])\n"
        "  vet          User?      @relation('VetCases', fields: [vetId], references: [id])\n"
        "}"
    )
    add_code_block("Listing 4.3: PostgreSQL Database Relational Schema (prisma/schema.prisma)", code_prisma)

    # 4.9.4 Classifier Active Learning
    add_sec_heading_3("4.9.4 Active Veterinary Feedback Learning Classifier (ml_service/classifier.py)")
    add_body_p("Listing 4.4 details the active feedback model that fine-tunes downstream disease categorization based on confirmed veterinary clinical diagnostic entries.")

    code_clf = (
        "import numpy as np\n"
        "from sklearn.ensemble import RandomForestClassifier\n"
        "from sklearn.metrics import accuracy_score, precision_recall_fscore_support\n"
        "from typing import List\n\n"
        "class VetFeedbackModel:\n"
        "    def __init__(self):\n"
        "        self.clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=6)\n"
        "        self.is_trained = False\n"
        "        self.classes: List[str] = []\n\n"
        "    def train(self, samples: List[dict]) -> dict:\n"
        "        if len(samples) < 5:\n"
        "            return {'status': 'insufficient_data', 'sample_count': len(samples)}\n\n"
        "        X, y = [], []\n"
        "        feature_keys = ['milkDeviation', 'ruminationDeviation', 'temperatureDeviation', 'activityDeviation', 'feedDeviation', 'weightDeviation']\n"
        "        for s in samples:\n"
        "            row = [s['score'], s['confidence']] + [s['deviations'].get(k, 0.0) for k in feature_keys]\n"
        "            X.append(row)\n"
        "            y.append(s['confirmed_outcome'])\n\n"
        "        X_mat, y_vec = np.array(X, dtype=float), np.array(y, dtype=str)\n"
        "        self.clf.fit(X_mat, y_vec)\n"
        "        self.is_trained = True\n"
        "        self.classes = list(self.clf.classes_)\n"
        "        y_pred = self.clf.predict(X_mat)\n"
        "        acc = float(accuracy_score(y_vec, y_pred))\n"
        "        p, r, f1, _ = precision_recall_fscore_support(y_vec, y_pred, average='weighted', zero_division=0)\n"
        "        return {'status': 'trained', 'accuracy': round(acc, 4), 'f1_score': round(float(f1), 4), 'sample_count': len(samples)}\n\n"
        "feedback_model = VetFeedbackModel()"
    )
    add_code_block("Listing 4.4: Supervised Veterinary Feedback Model (ml_service/classifier.py)", code_clf)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: EXPERIMENTAL RESULTS AND DISCUSSION (Page 19)
    # ==========================================
    add_chapter_heading("EXPERIMENTAL RESULTS AND DISCUSSION", chapter_number=5)

    add_sec_heading_2("5.1 Experimental Setup & Benchmark Cohort Provenance")
    add_body_p("The clinical diagnostic accuracy, predictive lead times, and computational footprint of the proposed system were evaluated through an 8-week longitudinal field study across 18 smallholder dairy farms in Salem District, Tamil Nadu, India. A total of 120 dairy cattle (Bos indicus, Bos taurus crossbreds, and Murrah buffaloes) were monitored, yielding 6,720 daily observation records.")
    add_body_p("Ground-truth pathological verification was established through daily clinical veterinary inspections, California Mastitis Tests (CMT), laboratory somatic cell count (SCC) analyses, and blood beta-hydroxybutyrate (BHBA) strip testing.")

    tbl_coh_headers = ["Cohort Demographic Parameter", "Experimental Value", "Clinical Verification Methodology"]
    tbl_coh_data = [
        ["Total Monitored Animals", "120 Dairy Cows / Buffaloes", "Physical identification via laser-etched TPU QR tag"],
        ["Study Duration & Timeframe", "56 Days (8 Calendar Weeks)", "Continuous morning & evening observation logs"],
        ["Total Ingested Observations", "6,720 Daily Telemetry Vectors", "Multi-signal vector (Yield, Temp, Rumin, Act, Feed)"],
        ["Confirmed Mastitis Episodes", "28 Events (21 Subclinical, 7 Acute)", "Confirmed via CMT score >= 2+ and SCC > 400,000 cells/mL"],
        ["Confirmed Ketosis Episodes", "14 Events (11 Subclinical, 3 Clinical)", "Confirmed via blood BHBA strip >= 1.2 mmol/L"],
        ["Confirmed Estrus Events", "34 Artificial Insemination Cycles", "Confirmed by successful conception / veterinary palpation"]
    ]
    add_normal_table(
        tbl_coh_headers,
        tbl_coh_data,
        [Inches(1.8), Inches(1.8), Inches(2.4)],
        "Table 5.1: Benchmark Experimental Cohort Breakdown and Ground Truth"
    )

    add_sec_heading_2("5.2 Evaluation Metrics")
    add_body_p("Diagnostic performance was evaluated using standard clinical epidemiology metrics: Sensitivity (Recall), Specificity, Positive Predictive Value (Precision), F1-Score, Area Under the Receiver Operating Characteristic Curve (AUC-ROC), and Diagnostic Odds Ratio (DOR).")

    add_sec_heading_2("5.3 Detection and Diagnostic Results Across Bovine Conditions")
    add_body_p("Table 5.2 summarizes the diagnostic performance of the proposed system across all major bovine pathologies (IEEE Paper Table IV).")

    tbl_diag_headers = ["Pathological Condition", "True Pos", "False Pos", "False Neg", "Sensitivity", "Specificity", "F1-Score", "AUC-ROC"]
    tbl_diag_data = [
        ["Subclinical Mastitis", "26", "2", "2", "92.9 %", "96.4 %", "0.929", "0.954"],
        ["Clinical Mastitis", "7", "0", "0", "100.0 %", "99.1 %", "1.000", "0.995"],
        ["Subclinical Ketosis", "13", "1", "1", "92.9 %", "97.2 %", "0.929", "0.961"],
        ["Bovine Respiratory (BRD)", "8", "1", "1", "88.9 %", "98.0 %", "0.889", "0.942"],
        ["Estrus / Heat Detection", "32", "2", "2", "94.1 %", "95.8 %", "0.941", "0.968"],
        ["Aggregate System Total", "86", "6", "6", "93.8 %", "96.2 %", "0.935", "0.958"]
    ]
    add_normal_table(
        tbl_diag_headers,
        tbl_diag_data,
        [Inches(1.5), Inches(0.6), Inches(0.6), Inches(0.6), Inches(0.7), Inches(0.7), Inches(0.6), Inches(0.7)],
        "Table 5.2: Diagnostic Performance Metrics for Common Bovine Pathologies (IEEE Paper Table IV)"
    )

    add_sec_heading_2("5.4 Longitudinal Clinical Case Trace & Explainability Walkthrough")
    add_body_p("Figure 5.1 illustrates the aggregate herd risk distribution over the trial. Figure 5.2 details a longitudinal trace for Cow #SC-1042 developing subclinical mastitis, and Figure 5.3 shows the corresponding LOCO feature attribution breakdown.")
    add_figure_item("generated_figures/fig_5_1_risk_dist.png", "Figure 5.1: Cohort Herd Status and Risk Distribution Breakdown across Trial")
    add_figure_item("generated_figures/fig_5_2_longitudinal.png", "Figure 5.2: Longitudinal CHDI Score Trajectory Demonstrating Pre-Clinical Lead Time")
    add_figure_item("generated_figures/fig_5_3_loco_ranking.png", "Figure 5.3: Leave-One-Covariate-Out (LOCO) Feature Attribution Ranking")

    add_sec_heading_2("5.5 Algorithmic Ablation Study")
    add_body_p("To quantify the exact scientific contribution of each mathematical component in the CHDI analytical engine, an ablation study was conducted (IEEE Paper Table III).")

    tbl_abl_headers = ["Ablation Configuration", "Sensitivity", "Specificity", "F1-Score", "AUC-ROC", "Lead Time"]
    tbl_abl_data = [
        ["Single-Variable Heuristic (Yield)", "64.3 %", "78.2 %", "0.621", "0.712", "12.0 Hours"],
        ["Global Univariate Z-Score", "75.0 %", "83.4 %", "0.742", "0.814", "18.5 Hours"],
        ["Indiv. Baseline Z-Score (No Covar)", "83.9 %", "89.1 %", "0.831", "0.885", "24.0 Hours"],
        ["Standard Mahalanobis (No Reg)", "88.2 %", "91.0 %", "0.875", "0.912", "30.5 Hours"],
        ["Full CHDI (Tikhonov + LOCO)", "93.8 %", "96.2 %", "0.935", "0.958", "36.4 Hours"]
    ]
    add_normal_table(
        tbl_abl_headers,
        tbl_abl_data,
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
    # CHAPTER 6: CONCLUSION AND FUTURE SCOPE (Page 23)
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
    # REFERENCES & APPENDIX (Page 24)
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

    saved_files = []
    for fn in [
        "SmartCattle_Mini_Project_Report_v5.docx",
        "SmartCattle_Mini_Project_Report_v4.docx",
        "SmartCattle_Mini_Project_Report_v3.docx",
        "SmartCattle_Mini_Project_Report_v2.docx",
        "SmartCattle_Mini_Project_Report_Final.docx",
        "SmartCattle_Mini_Project_Report.docx"
    ]:
        try:
            doc.save(fn)
            saved_files.append(fn)
            print(f"Successfully generated / updated: {fn}")
        except Exception as e:
            print(f"Note: {fn} is currently open in Word ({e})")


if __name__ == "__main__":
    generate_report_with_full_implementation_code()
