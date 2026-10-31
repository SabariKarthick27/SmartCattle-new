import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_academic_report():
    doc = docx.Document()

    # Configure standard academic margins (Left: 1.25 in, Right: 1.0 in, Top: 1.0 in, Bottom: 1.0 in)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27) # A4
        section.page_height = Inches(11.69) # A4

    # Strict Monochromatic / Dark Neutral Color Palette - ABSOLUTELY NO BLUE
    COLOR_BLACK = RGBColor(0x00, 0x00, 0x00)
    COLOR_DARK = RGBColor(0x1A, 0x1A, 0x1A)      # Deep Charcoal
    COLOR_GRAY = RGBColor(0x40, 0x40, 0x40)      # Medium Slate Dark

    HEX_HEADER_BG = "1A1A1A"  # Solid dark charcoal header background
    HEX_ALT_ROW = "F5F5F5"    # Clean light grey alternating row
    HEX_BORDER = "A0A0A0"     # Neutral grey borders

    # Set normal style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = COLOR_BLACK

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color=HEX_BORDER, sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_chapter_title(title_text, chapter_number=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
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

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True
        r.font.color.rgb = COLOR_BLACK
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        r.italic = True
        r.font.color.rgb = COLOR_DARK
        return p

    def add_body(text, bold_prefix="", space_after=6, line_spacing=1.35, italic=False):
        p = doc.add_paragraph()
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

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
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

    def add_figure(image_path, caption_text, width_inches=5.8):
        if os.path.exists(image_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(3)
            run_img = p_img.add_run()
            run_img.add_picture(image_path, width=Inches(width_inches))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10.5)
            r_cap.bold = True
            r_cap.italic = True
            r_cap.font.color.rgb = COLOR_DARK

    def add_table_data(headers, data, col_widths, caption_text=""):
        if caption_text:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(10)
            p_cap.paragraph_format.space_after = Pt(4)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(11)
            r_cap.bold = True
            r_cap.font.color.rgb = COLOR_BLACK

        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color=HEX_BORDER, sz="4", val="single")

        # Header Row (Black/Dark Charcoal fill with White Text)
        hdr_row = table.rows[0]
        for i, title in enumerate(headers):
            cell = hdr_row.cells[i]
            cell.width = col_widths[i]
            set_cell_background(cell, HEX_HEADER_BG)
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(title)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Data Rows
        for r_idx, row_data in enumerate(data):
            row = table.rows[r_idx + 1]
            bg_color = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.width = col_widths[c_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=90, bottom=90, left=130, right=130)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
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
        p_after.paragraph_format.space_before = Pt(4)
        p_after.paragraph_format.space_after = Pt(8)

    print("Generating IEEE Aligned Academic Report (Zero Blue Color)...")

    # ==========================================
    # 1. COVER / TITLE PAGE
    # ==========================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(14)
    r = p_title.add_run("QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_after = Pt(4)
    r = p_rep.add_run("A PROJECT REPORT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(18)
    r = p_course.add_run("Course Code & Course Name: U23ITP401 – MINI PROJECT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(8)
    r = p_sub.add_run("Submitted by")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.italic = True
    r.font.color.rgb = COLOR_BLACK

    # Candidate table
    table_cand = doc.add_table(rows=3, cols=2)
    table_cand.alignment = WD_TABLE_ALIGNMENT.CENTER
    cand_data = [
        ("SABARI KARTHICK A", "(61782323104056)"),
        ("SIVANARASIMMAN S", "(61782323104059)"),
        ("SUJEETH Y R", "(61782323104051)")
    ]
    for idx, (name, regno) in enumerate(cand_data):
        c1, c2 = table_cand.rows[idx].cells
        c1.width = Inches(2.8)
        c2.width = Inches(2.2)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(name)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.bold = True
        r1.font.color.rgb = COLOR_BLACK

        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(regno)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)
        r2.bold = True
        r2.font.color.rgb = COLOR_BLACK

    p_award = doc.add_paragraph()
    p_award.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_award.paragraph_format.space_before = Pt(18)
    p_award.paragraph_format.space_after = Pt(2)
    r = p_award.add_run("in partial fulfillment for the award of the degree\nof")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.color.rgb = COLOR_BLACK

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(4)
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
    r.font.color.rgb = COLOR_BLACK

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(14)
    r = p_dept.add_run("DEPARTMENT OF INFORMATION TECHNOLOGY /\nARTIFICIAL INTELLIGENCE AND DATA SCIENCE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    # College Logo
    if os.path.exists("template_images/image1.jpeg"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(10)
        run_logo = p_logo.add_run()
        run_logo.add_picture("template_images/image1.jpeg", width=Inches(1.2))

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
    # 2. BONAFIDE CERTIFICATE
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
        run_logo_c = p_logo_c.add_run()
        run_logo_c.add_picture("template_images/image1.jpeg", width=Inches(1.05))

    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(6)
    p_cert_title.paragraph_format.space_after = Pt(16)
    r = p_cert_title.add_run("BONAFIDE CERTIFICATE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    add_body(
        "Certified that this Project titled “QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)” is the bonafide work of “SABARI KARTHICK A (61782323104056), SIVANARASIMMAN S (61782323104059), SUJEETH Y R (61782323104051)” who carried out the project work Course Code & Course Name U23ITP401 – MINI PROJECT under my supervision.",
        space_after=24,
        line_spacing=1.4
    )

    # Supervisor & HOD Table
    tbl_sig = doc.add_table(rows=6, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_info = [
        ("Signature of the Supervisor", "Head of the Department"),
        ("Mrs. J. Deepika, M.E., (Ph.D.)", "Dr. J. Akilandeswari, M.E., Ph.D."),
        ("Assistant Professor", "Professor & Head"),
        ("Department of Information Technology", "Department of Information Technology"),
        ("Sona College of Technology,", "Sona College of Technology,"),
        ("Salem – 636 005", "Salem – 636 005")
    ]
    for idx, (left, right) in enumerate(sig_info):
        c1, c2 = tbl_sig.rows[idx].cells
        c1.width = Inches(3.2)
        c2.width = Inches(3.2)
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
    c1, c2 = tbl_exam.rows[0].cells
    c1.width = Inches(3.2)
    c2.width = Inches(3.2)
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
    # 3. DECLARATION
    # ==========================================
    add_chapter_title("DECLARATION")

    add_body(
        "We hereby declare that the project work entitled “QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)” submitted to ANNA UNIVERSITY, CHENNAI, in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology in Information Technology / Artificial Intelligence and Data Science, is a record of original research work done by us under the supervision and guidance of Mrs. J. Deepika, Assistant Professor, Department of Information Technology, Sona College of Technology, Salem.",
        space_after=12,
        line_spacing=1.35
    )
    add_body(
        "We further declare that this project report has not been submitted previously in part or in full to any other University or Institution for the award of any degree, diploma, fellowship, or other similar titles.",
        space_after=30,
        line_spacing=1.35
    )

    tbl_dec = doc.add_table(rows=4, cols=2)
    tbl_dec.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_p1, c_p2 = tbl_dec.rows[0].cells
    c_p1.width = Inches(3.0)
    c_p2.width = Inches(3.4)
    p = c_p1.paragraphs[0]
    r_dec = p.add_run("Place: Salem\nDate:")
    r_dec.font.name = 'Times New Roman'
    r_dec.font.color.rgb = COLOR_BLACK

    dec_members = [
        "1. SABARI KARTHICK A (61782323104056)",
        "2. SIVANARASIMMAN S (61782323104059)",
        "3. SUJEETH Y R (61782323104051)"
    ]
    for i, mem in enumerate(dec_members):
        cell = tbl_dec.rows[i+1].cells[1]
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
    # 4. ACKNOWLEDGEMENT
    # ==========================================
    add_chapter_title("ACKNOWLEDGEMENT")

    add_body(
        "First and foremost, we express our profound gratitude to the Almighty for showering his immense blessings upon us throughout the successful completion of this project.",
        space_after=10
    )
    add_body(
        "We extend our heartfelt gratitude to our Chairman, Vice-Chairmen, and Executive Director for providing exceptional state-of-the-art laboratory and computing infrastructure.",
        space_after=10
    )
    add_body(
        "We express our deep sense of gratitude and sincere thanks to our respected Principal, Dr. S. R. R. Senthil Kumar, for his continuous encouragement and academic support throughout our course of study.",
        space_after=10
    )
    add_body(
        "We are highly indebted and express our sincere thanks to Dr. J. Akilandeswari, Professor & Head, Department of Information Technology, for her invaluable guidance, visionary encouragement, and academic leadership.",
        space_after=10
    )
    add_body(
        "We express our deepest sense of gratitude, respect, and indebtedness to our esteemed Project Supervisor, Mrs. J. Deepika, Assistant Professor, Department of Information Technology, whose profound technical insights, constant inspiration, constructive critiques, and meticulous guidance made this research possible.",
        space_after=10
    )
    add_body(
        "We also convey our gratitude to all teaching and non-teaching faculty members of the Department of Information Technology, the veterinary clinicians who offered clinical feedback during field validation, and our loving parents and peers for their unwavering moral and emotional support.",
        space_after=14
    )

    doc.add_page_break()

    # ==========================================
    # 5. ABSTRACT
    # ==========================================
    add_chapter_title("ABSTRACT")

    add_body(
        "The smallholder dairy farming sector is a critical socio-economic backbone in rural developing economies, supporting more than 150 million farming households worldwide. However, managing livestock health on a small scale is severely limited by delayed disease detection, reliance on subjective manual inspection, and the exorbitant cost of commercial wearable Internet of Things (IoT) sensors ($150–$350 per animal). This economic divide leaves smallholder farmers vulnerable to subclinical diseases such as mastitis, ketosis, and bovine respiratory disease (BRD), which cause severe milk yield drops and reproductive losses before visible symptoms emerge.",
        space_after=10,
        line_spacing=1.35
    )
    add_body(
        "To solve this critical bottleneck, this project presents an AI-powered, zero-hardware-cost livestock health management platform based on weatherproof Quick Response (QR) matrices and a multi-stage analytical engine called the Composite Health Deviation Index (CHDI). In this framework, cattle are identified via low-cost laser-etched thermoplastic polyurethane (TPU) ear tags scanned by standard commodity smartphones. Daily physiological and production observations (milk yield, core temperature, rumination duration, activity counts, and feed consumption) are ingested and analyzed through a dedicated three-stage mathematical engine.",
        space_after=10,
        line_spacing=1.35
    )
    add_body(
        "Stage 1 establishes an individualized, rolling longitudinal baseline for each animal using sample variance with Bessel's correction, eliminating population-wide bias. Stage 2 computes a robust multivariate anomaly score using Tikhonov-regularized Mahalanobis distance, capturing subtle coupled covariance shifts indicative of pre-clinical pathophysiology while preventing matrix singularity. Stage 3 provides local explainability using Leave-One-Covariate-Out (LOCO) permutation feature attribution and incorporates supervised veterinary clinical diagnostic feedback to refine predictive accuracy over time.",
        space_after=10,
        line_spacing=1.35
    )
    add_body(
        "The platform is architected as an edge-first full-stack application using Next.js 14, TypeScript, Server Actions, PostgreSQL on Neon serverless infrastructure, and a Python FastAPI ML microservice. Empirical validation on a longitudinal dataset comprising 120 dairy cattle across 18 smallholder farms demonstrated that the proposed system achieves an overall anomaly detection sensitivity of 93.8%, specificity of 96.2%, and an AUC-ROC of 0.958. Crucially, the system detected subclinical mastitis and metabolic anomalies 24 to 48 hours prior to acute clinical symptoms, while reducing the per-animal monitoring cost to under $0.50 (a 99.7% reduction compared to wearable IoT solutions), establishing an accessible precision livestock management paradigm for smallholder farmers.",
        space_after=12,
        line_spacing=1.35
    )
    add_body(
        "Keywords: Precision Livestock Farming, QR Code Identification, Composite Health Deviation Index (CHDI), Multivariate Mahalanobis Distance, Tikhonov Regularization, Explainable AI, Veterinary Triage.",
        bold_prefix="Keywords: ",
        italic=True
    )

    doc.add_page_break()

    # ==========================================
    # 6. TABLE OF CONTENTS
    # ==========================================
    add_chapter_title("TABLE OF CONTENTS")

    toc_items = [
        ("BONAFIDE CERTIFICATE", "ii"),
        ("DECLARATION", "iii"),
        ("ACKNOWLEDGEMENT", "iv"),
        ("ABSTRACT", "v"),
        ("LIST OF TABLES", "viii"),
        ("LIST OF FIGURES", "ix"),
        ("LIST OF ABBREVIATIONS", "x"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("  1.1 Overview and Background of Dairy Healthcare", "1"),
        ("  1.2 Challenges in Smallholder Livestock Management", "3"),
        ("  1.3 Motivation & Research Gaps", "4"),
        ("  1.4 Problem Statement", "5"),
        ("  1.5 Objectives of the Project", "6"),
        ("  1.6 Organization of the Report", "7"),
        ("CHAPTER 2: LITERATURE REVIEW", "8"),
        ("  2.1 Information, Communication and Networking Systems in PLF", "8"),
        ("  2.2 Sensors and Physiological Monitoring for Wearable IoT Devices", "10"),
        ("  2.3 Computer Vision and Optical Identification Systems", "12"),
        ("  2.4 Digital Platforms and Veterinary Health Records", "14"),
        ("  2.5 Feature Comparison: Proposed System vs. Related Approaches", "16"),
        ("CHAPTER 3: EXISTING SYSTEM VS PROPOSED SYSTEM", "18"),
        ("  3.1 Existing Techniques in Cattle Health Monitoring", "18"),
        ("  3.2 Advantages and Disadvantages of Existing Techniques", "20"),
        ("  3.3 Proposed Technique: SmartCattle Non-Invasive QR & CHDI Platform", "22"),
        ("  3.4 How the Proposed System Overcomes Existing Disadvantages", "24"),
        ("  3.5 System Feasibility Analysis (Technical, Economic, Operational)", "26"),
        ("CHAPTER 4: SYSTEM ARCHITECTURE, DESIGN AND IMPLEMENTATION", "29"),
        ("  4.1 System Overview & High-Level Architectural Pipeline", "29"),
        ("  4.2 Four-Tier Architectural Subsystems", "31"),
        ("      4.2.1 Tier 1: Identification & Data Acquisition Layer", "31"),
        ("      4.2.2 Tier 2: Cloud Platform, API Gateway, and Security Layer", "33"),
        ("      4.2.3 Tier 3: Three-Stage CHDI Analytics Engine", "35"),
        ("      4.2.4 Tier 4: Clinical Triage and Veterinary Feedback Loop", "37"),
        ("  4.3 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)", "39"),
        ("  4.4 Mathematical Formulation of CHDI Engine", "41"),
        ("      4.4.1 Stage 1: Individual Baseline & Normalized Deviations", "42"),
        ("      4.4.2 Stage 2: Multivariate Covariance & Mahalanobis Distance with Regularization", "44"),
        ("      4.4.3 Stage 3: LOCO Permutation Explainability & Uncertainty Estimation", "47"),
        ("      4.4.4 Data Sufficiency and Confidence Gating", "49"),
        ("      4.4.5 CHDI Clinical Severity Bands & Action Protocols", "51"),
        ("  4.5 Database Schema & Entity Relationship Modeling", "53"),
        ("  4.6 Core Technology Stack & Implementation Modules", "55"),
        ("  4.7 Operational Algorithms and Pseudocode", "58"),
        ("CHAPTER 5: EXPERIMENTAL RESULTS, PERFORMANCE ANALYSIS AND DISCUSSION", "61"),
        ("  5.1 Real-World Benchmark Cohort and Provenance", "61"),
        ("  5.2 Longitudinal Clinical Case Trace & Explainability Walkthrough", "63"),
        ("  5.3 Anomaly Detection Performance & Algorithmic Ablation Study", "66"),
        ("  5.4 Predictive Lead Time & Early Intervention Advantage", "69"),
        ("  5.5 Computational Latency, Throughput & Edge Footprint", "71"),
        ("  5.6 Comparative Evaluation with Commercial Wearable IoT Solutions", "73"),
        ("  5.7 Comprehensive Discussion & Practical Insights", "75"),
        ("CHAPTER 6: CONCLUSION AND FUTURE WORK", "77"),
        ("  6.1 Conclusion", "77"),
        ("  6.2 Summary of Key Contributions", "78"),
        ("  6.3 Future Work", "79"),
        ("REFERENCES", "81")
    ]

    tbl_toc = doc.add_table(rows=len(toc_items) + 1, cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2 = tbl_toc.rows[0].cells
    c1.width = Inches(5.6)
    c2.width = Inches(1.0)
    set_cell_background(c1, HEX_HEADER_BG)
    set_cell_background(c2, HEX_HEADER_BG)
    r1 = c1.paragraphs[0].add_run("TABLE OF CONTENTS / TOPIC")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    r1.bold = True
    r1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    r2 = c2.paragraphs[0].add_run("PAGE NO.")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    r2.bold = True
    r2.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for idx, (topic, page_str) in enumerate(toc_items):
        row = tbl_toc.rows[idx + 1]
        c_top, c_pg = row.cells
        c_top.width = Inches(5.6)
        c_pg.width = Inches(1.0)
        bg = HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF"
        set_cell_background(c_top, bg)
        set_cell_background(c_pg, bg)
        set_cell_margins(c_top, top=40, bottom=40, left=100, right=100)
        set_cell_margins(c_pg, top=40, bottom=40, left=100, right=100)

        p1 = c_top.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r = p1.add_run(topic)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_BLACK
        if topic.startswith("CHAPTER") or topic in ["BONAFIDE CERTIFICATE", "DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT", "REFERENCES"]:
            r.bold = True

        p2 = c_pg.paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_pg = p2.add_run(page_str)
        r_pg.font.name = 'Times New Roman'
        r_pg.font.size = Pt(10)
        r_pg.font.color.rgb = COLOR_BLACK
        if topic.startswith("CHAPTER") or topic in ["BONAFIDE CERTIFICATE", "DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT", "REFERENCES"]:
            r_pg.bold = True

    set_table_borders(tbl_toc, color=HEX_BORDER, sz="2", val="single")

    doc.add_page_break()

    # ==========================================
    # 7. LIST OF TABLES & LIST OF FIGURES
    # ==========================================
    add_chapter_title("LIST OF TABLES")
    lot_items = [
        ("Table 2.1", "Feature Comparison: Proposed System vs. Related Approaches (IEEE Table I)", "17"),
        ("Table 3.1", "Detailed Advantages and Disadvantages of Existing Cattle Healthcare Techniques", "21"),
        ("Table 3.2", "System Feasibility Analysis Matrix for SmartCattle", "28"),
        ("Table 4.1", "CHDI Severity Bands, Score Ranges, and Clinical Protocols (IEEE Table II)", "52"),
        ("Table 4.2", "Prisma Database Schema Entities and Relational Mappings", "54"),
        ("Table 4.3", "SmartCattle Core Technology Stack and Module Allocation", "57"),
        ("Table 5.1", "Benchmark Experimental Cohort Breakdown and Ground Truth Provenance", "62"),
        ("Table 5.2", "Anomaly Detection Performance Metrics & Algorithmic Ablation (IEEE Table III)", "68"),
        ("Table 5.3", "Subclinical Disease Lead Time and Detection Window Analysis", "70"),
        ("Table 5.4", "End-to-End Latency and Computational Footprint Breakdown", "72"),
        ("Table 5.5", "Benchmarking SmartCattle against Commercial Wearable IoT Solutions", "74")
    ]
    add_table_data(
        ["TABLE NO.", "TITLE OF THE TABLE", "PAGE NO."],
        [[t, tit, pg] for t, tit, pg in lot_items],
        [Inches(1.2), Inches(4.6), Inches(0.8)]
    )

    add_chapter_title("LIST OF FIGURES")
    lof_items = [
        ("Figure 4.1", "Multi-Tier System Architecture of the Proposed QR-Based Cattle Management Platform", "30"),
        ("Figure 4.2", "Three-Stage CHDI Analytics Engine Operational Workflow", "36"),
        ("Figure 4.3", "Level 0 Context Diagram (DFD Level 0) for SmartCattle Platform", "40"),
        ("Figure 4.4", "Level 1 Data Flow Diagram (DFD Level 1) for Telemetry Ingestion and Diagnosis", "40"),
        ("Figure 5.1", "Cohort Herd Status and Risk Distribution Breakdown across Validation Period", "65"),
        ("Figure 5.2", "Longitudinal CHDI Score Trajectory Demonstrating Pre-Clinical Mastitis Lead Time", "66"),
        ("Figure 5.3", "Leave-One-Covariate-Out (LOCO) Feature Attribution Ranking for Health Deviation", "67")
    ]
    add_table_data(
        ["FIGURE NO.", "TITLE OF THE FIGURE", "PAGE NO."],
        [[f, tit, pg] for f, tit, pg in lof_items],
        [Inches(1.2), Inches(4.6), Inches(0.8)]
    )

    add_chapter_title("LIST OF ABBREVIATIONS")
    abbr_items = [
        ("AI", "Artificial Intelligence"),
        ("AMS", "Automated Milking System"),
        ("AUC-ROC", "Area Under the Receiver Operating Characteristic Curve"),
        ("BRD", "Bovine Respiratory Disease"),
        ("CHDI", "Composite Health Deviation Index"),
        ("CMT", "California Mastitis Test"),
        ("CNN", "Convolutional Neural Network"),
        ("CRDT", "Conflict-Free Replicated Data Type"),
        ("DFD", "Data Flow Diagram"),
        ("EMA", "Exponential Moving Average"),
        ("FNR", "False Negative Rate"),
        ("FPR", "False Positive Rate"),
        ("IoT", "Internet of Things"),
        ("LOCO", "Leave-One-Covariate-Out"),
        ("LSTM", "Long Short-Term Memory"),
        ("mAP", "Mean Average Precision"),
        ("NFC", "Near Field Communication"),
        ("ORM", "Object-Relational Mapping"),
        ("PLF", "Precision Livestock Farming"),
        ("PWA", "Progressive Web Application"),
        ("QR", "Quick Response"),
        ("RBAC", "Role-Based Access Control"),
        ("RFID", "Radio Frequency Identification"),
        ("RSC", "React Server Components"),
        ("SCC", "Somatic Cell Count"),
        ("TPU", "Thermoplastic Polyurethane"),
        ("TRL", "Technology Readiness Level"),
        ("UUID", "Universally Unique Identifier"),
        ("WSN", "Wireless Sensor Network"),
        ("YOLO", "You Only Look Once")
    ]
    add_table_data(
        ["ABBREVIATION", "EXPANSION / DESCRIPTION"],
        [[a, d] for a, d in abbr_items],
        [Inches(2.2), Inches(4.4)]
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    add_chapter_title("INTRODUCTION", chapter_number=1)

    add_heading_2("1.1 Overview and Background of Dairy Healthcare")
    add_body(
        "Livestock farming and dairy production constitute the economic backbone of rural developing economies, supporting more than 150 million smallholder households worldwide. In India, smallholder dairy operations contribute over 4.5% to the national GDP and serve as an indispensable source of nutrition, rural employment, and female empowerment. Unlike industrial dairy enterprises in developed nations—where thousands of cattle are managed in automated parlors—more than 85% of dairy production across developing agrarian nations is managed by smallholder farmers maintaining modest herds of 2 to 10 cattle.",
        space_after=8
    )
    add_body(
        "Despite its immense macroeconomic significance, smallholder dairy farming suffers from severe productivity constraints caused by endemic bovine diseases. Subclinical mastitis, ketosis, and bovine respiratory disease (BRD) cause severe milk yield drops, reproductive failure, and high involuntary culling rates. In subclinical mastitis alone, bacterial infection in the mammary gland reduces milk production by 15% to 30% per cow without producing overt visual abnormalities in milk appearance, costing the Indian dairy sector over $1.5 billion USD annually.",
        space_after=8
    )
    add_body(
        "Traditional smallholder livestock health monitoring relies entirely on visual observation during milking and feeding routines. However, by the time clinical symptoms become visually evident—such as swollen udder quarters, severe lethargy, rapid body condition score decline, or abnormal nasal discharge—the underlying pathophysiology has already caused tissue scarring, permanent lactation impairment, or systemic toxicity.",
        space_after=10
    )

    add_heading_2("1.2 Challenges in Smallholder Livestock Management")
    add_body(
        "Smallholder dairy farming is characterized by unique structural and operational challenges that prevent the direct adoption of industrial livestock management tools:",
        space_after=6
    )
    add_bullet("1. Resource Constraints & Low Margins:", "Smallholder farmers operate under narrow profit margins, where the annual net profit per cow ranges between $200 and $500 USD. Consequently, large capital expenditures cannot be justified.")
    add_bullet("2. Fragmented & Unstructured Field Telemetry:", "Data is captured across heterogeneous modalities (manual visual estimates, periodic bucket milk yields, spot digital thermometry) with variable observation frequencies.")
    add_bullet("3. Delayed Veterinary Clinical Triage:", "In rural villages, veterinary surgeons serve vast geographical jurisdictions, visiting individual farms only upon emergency callouts rather than for routine preventive triage.")
    add_bullet("4. Harsh Shed Environments:", "Rural barn conditions feature high humidity, abrasive tie-stalls, and mud accumulation, which rapidly damage delicate electronic equipment.")
    add_body("", space_after=10)

    add_heading_2("1.3 Motivation & Research Gaps")
    add_body(
        "The emerging paradigm of Precision Livestock Farming (PLF) has spurred extensive academic and commercial development in wearable biosensors, including collar-mounted 3D accelerometers (e.g., SCR CowManager), intra-rumen telemetry boluses (e.g., smaXtec), and leg pedometers (e.g., Afimilk AfiAct). While these wearable devices provide continuous real-time telemetry, they present three fatal flaws when applied to smallholder farming:",
        space_after=6
    )
    add_bullet("Prohibitive Capital Outlay ($150–$350 per cow):", "Equipping a modest 4-cow herd with commercial sensor collars costs between $600 and $1,400 USD, exceeding the farmer's total annual agricultural income.")
    add_bullet("High Sensor Loss & Maintenance Overhead:", "Physical collisions, tag detachment, and finite battery lifespans (3–5 years) impose recurring maintenance overheads that smallholders cannot afford.")
    add_bullet("Population-Wide Heuristic Thresholding:", "Existing systems apply rigid, global population thresholds that fail to account for individual biological baselines, breed variations, and lactation parities, causing high false alarm rates and alarm fatigue.")
    add_body(
        "Therefore, an urgent scientific and practical imperative exists to develop a zero-hardware-cost, non-invasive platform that leverages ubiquitous commodity smartphones and physical QR tags to deliver personalized, longitudinal health intelligence for smallholder dairy farmers.",
        space_after=10
    )

    add_heading_2("1.4 Problem Statement")
    add_body(
        "Smallholder dairy farmers lack cost-effective, non-invasive, and early-stage diagnostic tools to detect subclinical bovine health anomalies before they escalate into acute clinical disease, irreversible milk production collapse, or reproductive failure. Existing wearable IoT sensor platforms impose exorbitant financial and technical overheads that render them inaccessible to the smallholder agrarian sector.",
        space_after=8
    )
    add_body(
        "Furthermore, existing software management applications rely on crude population-wide statistical thresholds that generate high false alarm rates due to natural biological variations across individual cattle, lactation stages, and diurnal cycles. Consequently, there is an acute need for an intelligent livestock health management platform that operates without dedicated on-animal electronics, provides individual-calibrated longitudinal anomaly detection, and delivers actionable, explainable clinical triage for farmers and rural veterinarians.",
        space_after=10
    )

    add_heading_2("1.5 Objectives of the Project")
    add_body(
        "The overarching aim of this project is to develop and validate SmartCattle, an AI-powered, QR-based livestock healthcare ecosystem. The specific technical objectives are:",
        space_after=6
    )
    add_bullet("Objective 1 – Physical QR Identification Infrastructure:", "Design a secure, zero-hardware edge identification framework using laser-etched TPU QR ear tags containing cryptographic UUIDs, decoded via standard mobile smartphone browsers without dedicated app installation.")
    add_bullet("Objective 2 – Three-Stage CHDI Analytical Engine:", "Formulate and implement the Composite Health Deviation Index (CHDI), combining personalized rolling baselines with Bessel's correction, Tikhonov-regularized multivariate Mahalanobis distance anomaly scoring, and Leave-One-Covariate-Out (LOCO) explainability.")
    add_bullet("Objective 3 – Closed-Loop Veterinary Clinical Triage:", "Build a role-based clinical triage pipeline connecting Farmers, Field Veterinarians, and Administrators with automated alert dispatch, clinical override logging, and supervised model calibration.")
    add_bullet("Objective 4 – Cloud-Native Edge Architecture:", "Develop an end-to-end full-stack web ecosystem utilizing Next.js 14, React Server Components, TypeScript, Prisma ORM, and a dedicated Python FastAPI ML microservice.")
    add_bullet("Objective 5 – Empirical Field Validation & Benchmarking:", "Validate the diagnostic accuracy, pre-clinical lead time (24–48 hours), and latency on a real-world benchmark cohort of 120 dairy cattle across 18 smallholder farms.")
    add_body("", space_after=10)

    add_heading_2("1.6 Organization of the Report")
    add_body(
        "This project report is systematically organized into six cohesive chapters:",
        space_after=6
    )
    add_bullet("Chapter 1 (Introduction):", "Establishes the agricultural background, smallholder challenges, motivation, research gaps, problem statement, and objectives.")
    add_bullet("Chapter 2 (Literature Review):", "Surveys contemporary literature in PLF communication systems, wearable IoT sensors, computer vision, and digital veterinary records, presenting a comprehensive comparison matrix (IEEE Table I).")
    add_bullet("Chapter 3 (Existing System vs Proposed System):", "Analyzes existing techniques, contrasts their advantages and disadvantages, outlines the proposed system paradigm, and details a three-dimensional feasibility study.")
    add_bullet("Chapter 4 (System Architecture, Design and Implementation):", "Details the four-tier system architecture, DFDs, mathematical formulation of CHDI, database models, technology stack, and core algorithms.")
    add_bullet("Chapter 5 (Experimental Results, Performance Analysis and Discussion):", "Presents the benchmark cohort provenance, longitudinal clinical case traces, anomaly detection metrics, ablation studies, lead times, latency benchmarks, and commercial comparison.")
    add_bullet("Chapter 6 (Conclusion and Future Work):", "Summarizes key academic contributions and outlines future technical enhancements including offline CRDT synchronization and vernacular voice assistance.")
    add_body("", space_after=14)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: LITERATURE REVIEW
    # ==========================================
    add_chapter_title("LITERATURE REVIEW", chapter_number=2)

    add_heading_2("2.1 Information, Communication and Networking Systems in PLF")
    add_body(
        "The digital transformation of agriculture relies on robust Information and Communication Technology (ICT) architectures capable of operating across remote, low-connectivity rural landscapes. Subach and Shmeleva [4] surveyed the digital modernization of livestock farming, emphasizing that cloud-based data pipelines are essential for converting raw on-farm observations into actionable clinical intelligence.",
        space_after=8
    )
    add_body(
        "Curti et al. [6] formalized precision livestock data flow into a 5-step operational lifecycle: acquisition, transfer, cloud storage, statistical modeling, and decision delivery. In pastoral grazing environments, Barriuso et al. [9] developed a multi-agent Wireless Sensor Network (WSN) architecture using PANGEA orchestration and MQTT messaging. While effective in maintaining distributed telemetry sync, such architectures require local gateway hardware, solar repeaters, and continuous maintenance that exceed smallholder capabilities.",
        space_after=10
    )

    add_heading_2("2.2 Sensors and Physiological Monitoring for Wearable IoT Devices")
    add_body(
        "Wearable biosensors represent the most extensively researched paradigm in precision dairy healthcare. Kaur and Virk [5] designed an IoT-based neck collar equipped with triaxial accelerometers, digital thermistors, and pulse sensors transmitting data to a Raspberry Pi gateway. Tested across 150 cattle over 2 months in Punjab, India, their system achieved classification accuracies of 92% and 91% using Random Forest and Decision Tree models for BRD and mastitis, respectively.",
        space_after=8
    )
    add_body(
        "Kamphuis et al. [12] investigated automated mastitis detection using decision trees in automated milking systems, demonstrating that multivariate coupling between milk yield, electrical conductivity, and temperature significantly outperforms single-threshold heuristic rules. Aquilani et al. [7] reviewed PLF technologies across pasture livestock, highlighting walk-over weigh scales, GPS collars, and thermography cameras.",
        space_after=8
    )
    add_body(
        "Despite their diagnostic capabilities, all wearable platforms suffer from three severe operational failure modes: finite battery life (requiring tag replacement every 3–5 years), physical detachment or crushing caused by animal social interactions, and high unit capital costs ($150–$350/cow) [5], [7].",
        space_after=10
    )

    add_heading_2("2.3 Computer Vision and Optical Identification Systems")
    add_body(
        "To eliminate expensive electronic tags, non-invasive optical identification techniques have been explored. Bumbálek et al. [3] conducted a comprehensive comparative study evaluating YOLOv8-based body-texture biometric recognition, numerical ear-tag optical character recognition (OCR), and collar-mounted QR codes in dynamic dairy herds.",
        space_after=8
    )
    add_body(
        "Their experimental results revealed that QR-based identification achieved an mAP50–95 score of 0.71, compared to 0.78 for body texture biometrics and 0.84 for numerical OCR. Crucially, QR identification exhibited a distinct operational advantage: deep CNN weights for biometric texture require retraining when new cattle join the herd, whereas QR matrices use fixed universal decoding standards, allowing instant zero-retraining enrollment. However, Bumbálek et al. noted that optical systems face occlusion from barn mud and variable lighting, underscoring the necessity for durable laser-etched tags and manual search fallbacks [3].",
        space_after=10
    )

    add_heading_2("2.4 Digital Platforms and Veterinary Health Records")
    add_body(
        "In clinical practice, Ahmad and Salamat [8] developed a web-based veterinary clinic management system at GeBuu Clinic, implementing role-based access control, treatment histories, and automated vaccination reminders to reduce administrative overhead and enhance medical compliance.",
        space_after=8
    )
    add_body(
        "However, contemporary veterinary software systems operate as purely passive electronic medical record (EMR) repositories. They lack integrated analytical engines capable of modeling historical baselines or detecting subtle multi-signal physiological deviations from sparse, heterogeneous field observations [4], [8]. Existing systems either demand heavy capital investment in specialized IoT hardware [1], [2], [5] or provide passive optical identification without health analytics [3]. The proposed system explicitly bridges this gap.",
        space_after=10
    )

    add_heading_2("2.5 Feature Comparison: Proposed System vs. Related Approaches")
    add_body(
        "Table 2.1 presents a comprehensive comparative feature matrix benchmarking SmartCattle against prominent related works in livestock management (reproduced from IEEE Paper Table I).",
        space_after=6
    )

    tbl1_headers = ["Platform / Study", "Identification Mechanism", "Hardware Requirement", "Analytical Engine", "Explainability", "Target Audience"]
    tbl1_data = [
        ["Kaur & Virk [5]", "Wearable Collar Sensor", "High ($150–$250 / cow)", "Random Forest / DT", "None (Black-box)", "Industrial Farms"],
        ["Bumbálek et al. [3]", "YOLOv8 Vision / QR", "Medium (High-res Cameras)", "Object Detection Only", "None (Vision Bounding)", "Large-Scale Herds"],
        ["Kamphuis et al. [12]", "Milking Parlor Sensors", "High ($15,000+ Parlor)", "Decision Tree Rules", "Partial (Rule Splits)", "Robotic Dairies"],
        ["Ahmad & Salamat [8]", "Manual ID / Barcode", "Low (PC / Mobile)", "None (Passive EMR)", "None (Static Records)", "Veterinary Clinics"],
        ["Barriuso et al. [9]", "GPS / ZigBee Collars", "High (WSN Gateways)", "PANGEA Multi-Agent", "None (Agent Rules)", "Pasture Ranches"],
        ["Proposed System", "Laser-Etched QR Ear Tag", "Zero (< $0.50 / tag)", "Three-Stage CHDI (Mahalanobis + Tikhonov)", "Yes (LOCO Feature Attribution)", "Smallholder Farmers & Rural Vets"]
    ]
    add_table_data(
        tbl1_headers,
        tbl1_data,
        [Inches(1.4), Inches(1.5), Inches(1.4), Inches(1.5), Inches(1.2), Inches(1.4)],
        "Table 2.1: Feature Comparison: Proposed System vs. Related Approaches (IEEE Paper Table I)"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: EXISTING SYSTEM VS PROPOSED SYSTEM
    # ==========================================
    add_chapter_title("EXISTING SYSTEM VS PROPOSED SYSTEM", chapter_number=3)

    add_heading_2("3.1 Existing Techniques in Cattle Health Monitoring")
    add_body(
        "Livestock health monitoring methodologies in practice today fall into four distinct operational paradigms:",
        space_after=6
    )
    add_bullet("1. Manual Farmer Inspection:", "Periodic visual and physical assessment of animal demeanor, feed intake, milk quantity, and udder condition. Completely non-technical, reactive, and highly subjective.")
    add_bullet("2. Wearable Accelerometer & Temperature Collars:", "Neck-mounted electronic devices measuring rumination chewing rhythms, head tilt, and neck skin temperature.")
    add_bullet("3. Reticulorumen Telemetry Boluses:", "Ceramic-encapsulated electronic capsules orally administered to reside in the reticulum, measuring internal temperature and pH.")
    add_bullet("4. Automated Milking System (AMS) Inline Probes:", "Robotic milking sensors measuring optical clarity, electrical conductivity, and somatic cell count during milking.")
    add_body("", space_after=10)

    add_heading_2("3.2 Advantages and Disadvantages of Existing Techniques")
    add_body(
        "A rigorous comparative evaluation reveals stark trade-offs between diagnostic granularity and economic accessibility, as summarized in Table 3.1.",
        space_after=6
    )

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
    add_table_data(
        ex_headers,
        ex_data,
        [Inches(1.8), Inches(2.3), Inches(2.9)],
        "Table 3.1: Detailed Advantages and Disadvantages of Existing Cattle Healthcare Techniques"
    )

    add_heading_2("3.3 Proposed Technique: SmartCattle Non-Invasive QR & CHDI Platform")
    add_body(
        "To resolve the fundamental dichotomy between high-cost sensor precision and low-cost manual inaccuracy, SmartCattle introduces an AI-powered, zero-hardware-cost livestock health intelligence platform.",
        space_after=8
    )
    add_body(
        "SmartCattle replaces electronic wearables with low-cost, laser-etched thermoplastic polyurethane (TPU) ear tags bearing high-contrast 2-D QR matrices. When scanned using any commodity smartphone browser, the encrypted UUID payload authenticates the animal and loads its contextual logging portal.",
        space_after=8
    )
    add_body(
        "Daily observations (milk yield, core temperature via standard thermometer, rumination duration, activity counts, feed intake) are ingested and evaluated by the Three-Stage Composite Health Deviation Index (CHDI) engine. CHDI constructs personalized historical baselines, computes regularized multivariate Mahalanobis anomaly scores, provides LOCO feature attribution, and generates automated clinical triage alerts for veterinarians.",
        space_after=10
    )

    add_heading_2("3.4 How the Proposed System Overcomes Existing Disadvantages")
    add_body(
        "SmartCattle addresses each limitation of prior approaches through structural innovations:",
        space_after=6
    )
    add_bullet("1. 99.7% Hardware Cost Reduction:", "Eliminates on-animal electronics, reducing the per-cow cost from $150–$350 to under $0.50 (the cost of laser-etched TPU tag printing).")
    add_bullet("2. Elimination of Population Bias:", "Stage 1 constructs an individualized rolling moving-average baseline with Bessel's correction for every cow, evaluating each animal against its own historical homeostasis.")
    add_bullet("3. Multivariate Covariance Modeling with Regularization:", "Stage 2 computes Tikhonov-regularized Mahalanobis distance across all physiological signals simultaneously, detecting multi-signal subclinical shifts 24–48 hours prior to acute clinical symptoms.")
    add_bullet("4. Explainable Clinical Attribution (LOCO):", "Stage 3 quantifies the exact percentage contribution of each physiological parameter to the anomaly, providing transparent clinical justifications that build veterinarian trust.")
    add_bullet("5. Zero-Installation In-Browser Edge Execution:", "Built on Next.js 14 React Server Components and mobile-optimized web interfaces, eliminating app-store installation friction.")
    add_body("", space_after=10)

    add_heading_2("3.5 System Feasibility Analysis (Technical, Economic, Operational)")
    add_body(
        "A comprehensive feasibility study confirmed the high viability of SmartCattle for smallholder agricultural deployment across three dimensions (Table 3.2).",
        space_after=6
    )

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
    add_table_data(
        feas_headers,
        feas_data,
        [Inches(1.8), Inches(2.2), Inches(3.0)],
        "Table 3.2: System Feasibility Analysis Matrix for SmartCattle"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: SYSTEM ARCHITECTURE, DESIGN AND IMPLEMENTATION
    # ==========================================
    add_chapter_title("SYSTEM ARCHITECTURE, DESIGN AND IMPLEMENTATION", chapter_number=4)

    add_heading_2("4.1 System Overview & High-Level Architectural Pipeline")
    add_body(
        "SmartCattle is architected as an end-to-end, multi-tier cloud-native platform integrating zero-hardware edge capture, high-throughput ingestion, a 3-stage machine learning analytics pipeline, and role-tailored user interfaces for farmers, field veterinarians, and cooperative dairy administrators.",
        space_after=8
    )
    add_body(
        "Figure 4.1 depicts the four-tier system architecture, illustrating the flow of telemetry from physical QR tags through cloud security, the analytical engine, and clinical triage.",
        space_after=8
    )

    add_figure(
        "extracted_images/image1.png",
        "Figure 4.1: Multi-Tier System Architecture of the Proposed QR-Based Cattle Management Platform (IEEE Paper Fig. 1)",
        width_inches=5.8
    )

    add_heading_2("4.2 Four-Tier Architectural Subsystems")

    add_heading_3("4.2.1 Tier 1: Identification & Data Acquisition Layer")
    add_body(
        "The edge interface utilizes low-cost thermoplastic polyurethane (TPU) ear tags laser-etched with high-contrast 2-D QR matrices. To ensure data privacy and prevent tampering, the QR payload contains only an opaque 128-bit cryptographic universally unique identifier (UUID v4) and an HTTPS URI endpoint (e.g., https://livestock-health.org/scan?token=UUID). No clinical or ownership data is stored on the physical tag.",
        space_after=8
    )
    add_body(
        "When scanned by any smartphone browser, an authenticated handshake resolves the animal's identity. Farmers record daily milk yield (L), core body temperature (°C), rumination duration (min), activity steps, and feed intake (kg). Veterinarians log clinical diagnoses, treatments, and vaccination records. Every record includes a metadata source tag (manual | qr_scan | sensor) to maintain multi-modal data provenance.",
        space_after=8
    )

    add_heading_3("4.2.2 Tier 2: Cloud Platform, API Gateway, and Security Layer")
    add_body(
        "The application layer is engineered using Next.js 14, React Server Components (RSC), and Server Actions, communicating with a dedicated Python FastAPI ML microservice via RESTful APIs. Security is enforced via Role-Based Access Control (RBAC) across three roles: (1) Farmers (scoped to own farm tenancy); (2) Veterinarians (regional clinical queue, prescription logging, diagnostic override); and (3) System Administrators (multi-tenant farm provisioning, user verification, global threshold configuration). All traffic is encrypted via TLS 1.3, and database operations use parameterized Prisma ORM queries to prevent SQL injection.",
        space_after=8
    )

    add_heading_3("4.2.3 Tier 3: Three-Stage CHDI Analytics Engine")
    add_body(
        "The computational core of the system executes the Three-Stage CHDI analytical sequence: Stage 1 (Personalized Rolling Baseline Calibration), Stage 2 (Tikhonov-Regularized Covariance Inversion and Mahalanobis Anomaly Distance), and Stage 3 (LOCO Permutation Feature Attribution).",
        space_after=8
    )

    add_figure(
        "extracted_images/image2.png",
        "Figure 4.2: Three-Stage CHDI Analytics Engine Operational Workflow (IEEE Paper Fig. 2)",
        width_inches=5.8
    )

    add_heading_3("4.2.4 Tier 4: Clinical Triage and Veterinary Feedback Loop")
    add_body(
        "Diagnostic outputs are routed through a dynamic clinical triage queue. When CHDI crosses the 'At-Risk' threshold (CHDI ≥ 51), automated push notifications dispatch to the assigned regional veterinarian. When a veterinarian conducts a physical examination and logs a confirmed clinical diagnosis, the feedback is persisted to retrain ensemble weights, continuously refining system specificity.",
        space_after=10
    )

    add_heading_2("4.3 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)")
    add_body(
        "The operational lifecycle of SmartCattle is formally modeled across three DFD levels:",
        space_after=6
    )
    add_bullet("Level 0 Context Diagram:", "Models the macro-boundary between external actors (Farmer, Veterinarian, Admin) and the central SmartCattle platform. Telemetry flows in; clinical alerts and triage queues flow out.")
    add_bullet("Level 1 Subsystem Flow:", "Deconstructs the platform into four discrete processes: Process 1.0 (QR Ingestion & Authentication), Process 2.0 (Historical Baseline Retrieval), Process 3.0 (CHDI Anomaly Scoring & LOCO Attribution), and Process 4.0 (Clinical Alert Dispatch).")
    add_bullet("Level 2 Detailed Diagnostic Flow:", "Deconstructs Process 3.0 into granular sub-steps: Variance Calculation with Bessel's Correction (3.1), Tikhonov Regularization (3.2), Matrix Inversion & Mahalanobis Distance (3.3), Sigmoidal Mapping (3.4), and LOCO Permutation (3.5).")
    add_body("", space_after=10)

    add_heading_2("4.4 Mathematical Formulation of CHDI Engine")
    add_body(
        "The mathematical foundation of CHDI is formulated as follows (reproduced from Section IV of the IEEE paper):",
        space_after=6
    )

    add_heading_3("4.4.1 Stage 1: Individual Baseline & Normalized Deviations")
    add_body(
        "Let x_i(t) in R^d represent the physiological telemetry vector for cow i at observation t across d available signals (milk yield, temperature, rumination, activity, feed intake). The rolling moving-average baseline mu_i,k(t) and sample variance sigma_i,k^2(t) over a window W = 14 observations with Bessel's correction are defined as:",
        space_after=6
    )
    add_body(
        "mu_i,k(t) = (1 / W) * sum_{j=0}^{W-1} x_i,k(t - j)",
        bold_prefix="[Equation 4.1]  Rolling Baseline Mean: ",
        italic=True
    )
    add_body(
        "sigma_i,k^2(t) = (1 / (W - 1)) * sum_{j=0}^{W-1} (x_i,k(t - j) - mu_i,k(t))^2",
        bold_prefix="[Equation 4.2]  Sample Variance (Bessel Corrected): ",
        italic=True
    )
    add_body(
        "The normalized deviation vector z_i(t) = [z_i,1(t), ..., z_i,d(t)]^T is computed via standardized z-score normalization:",
        space_after=6
    )
    add_body(
        "z_i,k(t) = (x_i,k(t) - mu_i,k(t)) / sqrt(sigma_i,k^2(t) + epsilon)",
        bold_prefix="[Equation 4.3]  Normalized Deviation Z-Score: ",
        italic=True
    )
    add_body(
        "where epsilon = 1e-4 is a numerical stability guard against division by zero during periods of static physiological logging.",
        space_after=8
    )

    add_heading_3("4.4.2 Stage 2: Multivariate Covariance & Mahalanobis Distance with Regularization")
    add_body(
        "To capture coupled multi-signal interactions while preventing singularity during collinear or sparse observation periods, the empirical covariance matrix Sigma_i(t) is regularized using Tikhonov ridge regularization:",
        space_after=6
    )
    add_body(
        "Sigma_i,reg(t) = Sigma_i(t) + lambda * I",
        bold_prefix="[Equation 4.4]  Tikhonov-Regularized Covariance Matrix: ",
        italic=True
    )
    add_body(
        "where lambda = 1e-3 is the regularization ridge parameter and I is the d x d identity matrix. The multivariate Mahalanobis distance D_M(t) is then calculated as:",
        space_after=6
    )
    add_body(
        "D_M(t) = sqrt( z_i(t)^T * (Sigma_i,reg(t))^(-1) * z_i(t) )",
        bold_prefix="[Equation 4.5]  Mahalanobis Anomaly Distance: ",
        italic=True
    )
    add_body(
        "The multivariate distance is mapped into a calibrated, standardized continuous health deviation score CHDI(t) in [0, 100] via a bounded logistic function with an empirical upper boundary D_max = 4.0 sigma:",
        space_after=6
    )
    add_body(
        "CHDI(t) = min( 100, (D_M(t) / D_max) * 100 )",
        bold_prefix="[Equation 4.6]  Calibrated CHDI Score Mapping: ",
        italic=True
    )

    add_heading_3("4.4.3 Stage 3: LOCO Permutation Explainability & Uncertainty Estimation")
    add_body(
        "To explain the clinical drivers behind an elevated anomaly score without the exponential computational burden of Shapley values, SmartCattle implements Leave-One-Covariate-Out (LOCO) permutation attribution. The marginal distance drop Delta D_k(t) when feature k is excluded is defined as:",
        space_after=6
    )
    add_body(
        "Delta D_k(t) = max( 0, D_M(t) - D_{M, -k}(t) )",
        bold_prefix="[Equation 4.7]  LOCO Marginal Attribution: ",
        italic=True
    )
    add_body(
        "where D_{M, -k}(t) is the Mahalanobis distance recomputed on the (d - 1)-dimensional subspace excluding feature k. The relative percentage contribution C_k(t) is normalized across all d features:",
        space_after=6
    )
    add_body(
        "C_k(t) = ( Delta D_k(t) / sum_{j=1}^d Delta D_j(t) ) * 100%",
        bold_prefix="[Equation 4.8]  Normalized Percentage Feature Contribution: ",
        italic=True
    )

    add_heading_3("4.4.4 Data Sufficiency and Confidence Gating")
    add_body(
        "To prevent spurious false alarms during the initial enrollment period, the engine enforces an abstention gate. When total historical observations N_obs < N_min (N_min = 7 days across distinct observation sessions), the system abstains from generating a diagnostic score (CHDI = null, status = 'abstain'). The confidence metric rho(t) scales asymptotically toward unity:",
        space_after=6
    )
    add_body(
        "rho(t) = min( 1.0, N_obs / N_saturation )",
        bold_prefix="[Equation 4.9]  Confidence Gating Metric: ",
        italic=True
    )
    add_body("where N_saturation = 14 observations denotes full baseline maturity.", space_after=8)

    add_heading_3("4.4.5 CHDI Clinical Severity Bands & Action Protocols")
    add_body(
        "Table 4.1 outlines the standardized clinical severity triage bands and prescribed action protocols (reproduced from IEEE Paper Table II).",
        space_after=6
    )

    tbl2_headers = ["Severity Band", "CHDI Range", "Clinical State & Interpretation", "Prescribed Action Protocol"]
    tbl2_data = [
        ["HEALTHY", "0 – 25", "Homeostatic stability; physiological signals within baseline bounds", "Continue standard feeding, milking, and management routine; no intervention required."],
        ["WATCH", "26 – 50", "Mild subclinical deviation; potential early stress, estrus, or diet shift", "Re-scan within 12 hours; inspect feed consumption, water intake, and locomotion."],
        ["AT-RISK", "51 – 75", "Moderate multi-signal anomaly; strong likelihood of early-stage disease", "Automated notification to regional veterinarian; isolate animal; conduct CMT."],
        ["CRITICAL", "76 – 100", "Severe acute deviation; acute mastitis / systemic metabolic distress", "Emergency veterinary visit; administer clinical therapeutic antibiotic protocol."],
        ["ABSTAIN", "N/A (N < 7)", "Insufficient baseline depth (< 7 observations across distinct days)", "Enrollment phase; safely withhold health scoring until baseline data threshold is met."]
    ]
    add_table_data(
        tbl2_headers,
        tbl2_data,
        [Inches(1.2), Inches(1.1), Inches(2.5), Inches(2.2)],
        "Table 4.1: CHDI Severity Bands, Score Ranges, and Clinical Protocols (IEEE Paper Table II)"
    )

    add_heading_2("4.5 Database Schema & Entity Relationship Modeling")
    add_body(
        "The relational data model is implemented on PostgreSQL using Prisma ORM. Table 4.2 describes the core schema entities and relational mappings.",
        space_after=6
    )

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
    add_table_data(
        tbl_db_headers,
        tbl_db_data,
        [Inches(1.3), Inches(2.1), Inches(1.8), Inches(1.8)],
        "Table 4.2: Prisma Database Schema Entities and Relational Mappings"
    )

    add_heading_2("4.6 Core Technology Stack & Implementation Modules")
    add_body(
        "Table 4.3 details the comprehensive technology stack selected for the implementation of the SmartCattle platform.",
        space_after=6
    )

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
    add_table_data(
        tbl_tech_headers,
        tbl_tech_data,
        [Inches(1.3), Inches(1.8), Inches(1.2), Inches(2.7)],
        "Table 4.3: SmartCattle Core Technology Stack and Module Allocation"
    )

    add_heading_2("4.7 Operational Algorithms and Pseudocode")
    add_body(
        "Algorithm 4.1 formalizes the end-to-end operational execution of the CHDI analytical engine.",
        space_after=6
    )
    add_body(
        "Algorithm 4.1: Three-Stage Composite Health Deviation Index (CHDI) Execution\n"
        "Input: Current Observation Vector x(t), Historical Buffer H = {x(t-1), ..., x(t-N)}, Minimum Baseline Depth N_min = 7\n"
        "Output: CHDI Score S(t), Confidence rho(t), Severity Band B, Feature Contributions C\n"
        "1:  Procedure ComputeCHDI(x(t), H):\n"
        "2:      If length(H) < N_min Then:\n"
        "3:          Return {Score: null, Confidence: length(H)/14, Status: 'ABSTAIN', Band: 'Enrollment Phase'}\n"
        "4:      For each active signal k in {1..d} Do:\n"
        "5:          mu_k <- Mean(H_k[-14:])\n"
        "6:          sigma_k <- StdDev(H_k[-14:], ddof=1)\n"
        "7:          z_k(t) <- (x_k(t) - mu_k) / sqrt(sigma_k^2 + 1e-4)\n"
        "8:      Compute rolling empirical covariance matrix Sigma from H[-30:]\n"
        "9:      Apply Tikhonov Regularization: Sigma_reg <- Sigma + 1e-3 * Identity(d)\n"
        "10:     Compute Mahalanobis Distance: D_M(t) <- sqrt( z(t)^T * (Sigma_reg)^(-1) * z(t) )\n"
        "11:     Scale Raw CHDI: S_raw <- min(100, (D_M(t) / 4.0) * 100)\n"
        "12:     For each signal k in {1..d} Do:\n"
        "13:         D_M_minus_k <- Recompute Mahalanobis distance omitting signal k\n"
        "14:         Delta_D_k <- max(0, D_M(t) - D_M_minus_k)\n"
        "15:     For each signal k in {1..d} Do:\n"
        "16:         C_k <- (Delta_D_k / sum_j Delta_D_j) * 100%\n"
        "17:     Determine Severity Band B from Table 4.1 based on S_raw\n"
        "18:     If S_raw >= 51 Then DispatchVeterinaryTriageAlert(cattleId, S_raw, C)\n"
        "19:     Return {Score: S_raw, Confidence: min(1.0, length(H)/14), Band: B, Contributions: C}\n"
        "20: End Procedure",
        italic=True,
        space_after=14,
        line_spacing=1.15
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: EXPERIMENTAL RESULTS, PERFORMANCE ANALYSIS AND DISCUSSION
    # ==========================================
    add_chapter_title("EXPERIMENTAL RESULTS, PERFORMANCE ANALYSIS AND DISCUSSION", chapter_number=5)

    add_heading_2("5.1 Real-World Benchmark Cohort and Provenance")
    add_body(
        "To validate the diagnostic efficacy of SmartCattle under authentic agricultural field conditions, an 8-week longitudinal study (56 days) was conducted across 18 smallholder dairy farms in Salem District, Tamil Nadu, India. The benchmark cohort comprised 120 dairy cattle representing typical smallholder breed compositions. Certified veterinary surgeons provided clinical diagnostic ground truth through California Mastitis Tests (CMT), somatic cell counts (SCC), blood beta-hydroxybutyrate (BHBA) strips, and rectal palpation.",
        space_after=8
    )
    add_body(
        "Table 5.1 details the experimental cohort demographics, logging completion, and clinical ground truth provenance.",
        space_after=6
    )

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
    add_table_data(
        tbl_ds_headers,
        tbl_ds_data,
        [Inches(2.2), Inches(2.6), Inches(2.2)],
        "Table 5.1: Benchmark Experimental Cohort Breakdown and Ground Truth Provenance"
    )

    add_heading_2("5.2 Longitudinal Clinical Case Trace & Explainability Walkthrough")
    add_body(
        "Figure 5.1 illustrates the aggregate herd risk distribution over the 8-week trial. Approximately 82.4% of all animal-days remained securely within the 'Healthy' band (CHDI 0–25), 11.2% in 'Watch', 4.8% in 'At-Risk', and 1.6% in 'Critical', proving that the regularized CHDI baseline eliminates false alarm saturation.",
        space_after=8
    )

    add_figure(
        "generated_figures/fig3_status_distribution.png",
        "Figure 5.1: Cohort Herd Status and Risk Distribution Breakdown across Validation Period (IEEE Paper Fig. 3)",
        width_inches=5.4
    )

    add_body(
        "Figure 5.2 traces a longitudinal case study for Cow #SC-1042 developing subclinical mastitis over a 14-day window. The baseline established over Days 1–6 showed stable CHDI scores (< 20). On Day 7, CHDI spiked to 58 ('At-Risk') due to a coupled 11% milk yield drop and a 0.4°C temperature rise. On Day 8, CHDI reached 78 ('Critical'), prompting automated veterinary dispatch. Formal clinical CMT confirmed subclinical mastitis on Day 9, validating a 36-hour pre-clinical early warning lead time.",
        space_after=8
    )

    add_figure(
        "generated_figures/fig4_longitudinal_trajectory.png",
        "Figure 5.2: Longitudinal CHDI Score Trajectory Demonstrating Pre-Clinical Mastitis Lead Time (IEEE Paper Fig. 4)",
        width_inches=5.6
    )

    add_body(
        "Figure 5.3 shows the LOCO feature attribution breakdown for Cow #SC-1042 on Day 8, attributing 52.4% of the anomaly to milk yield drop, 28.1% to rumination duration decline, and 14.5% to temperature elevation, providing clear clinical interpretability.",
        space_after=8
    )

    add_figure(
        "generated_figures/fig5_feature_importance.png",
        "Figure 5.3: Leave-One-Covariate-Out (LOCO) Feature Attribution Ranking for Health Deviation (IEEE Paper Fig. 5)",
        width_inches=5.4
    )

    add_heading_2("5.3 Anomaly Detection Performance & Algorithmic Ablation Study")
    add_body(
        "To rigorously quantify the contribution of each mathematical component, SmartCattle was benchmarked against three baseline ablation models (reproduced from IEEE Paper Table III):",
        space_after=6
    )
    add_bullet("1. Univariate Z-Score Baseline:", "Evaluates each telemetry feature independently using standard thresholding (|z| > 2.5 sigma).")
    add_bullet("2. Unsupervised Isolation Forest:", "Standard isolation forest ensemble (n_estimators = 100) trained on population data.")
    add_bullet("3. Mahalanobis Distance (Without Regularization):", "Computes standard Mahalanobis distance without Tikhonov ridge shrinkage.")
    add_bullet("4. Proposed SmartCattle CHDI:", "Full three-stage pipeline combining personalized baselines, Tikhonov-regularized covariance inversion, and LOCO attribution.")
    add_body("", space_after=6)

    tbl3_headers = ["Model / Algorithm", "Sensitivity (%)", "Specificity (%)", "Precision (%)", "F1-Score (%)", "AUC-ROC"]
    tbl3_data = [
        ["Univariate Z-Score Baseline", "76.3 %", "81.4 %", "68.2 %", "72.0 %", "0.788"],
        ["Isolation Forest (Population)", "82.1 %", "87.6 %", "74.5 %", "78.1 %", "0.852"],
        ["Mahalanobis (No Regularization)", "88.4 %", "91.2 %", "81.0 %", "84.5 %", "0.904"],
        ["SmartCattle CHDI (Proposed)", "93.8 %", "96.2 %", "89.2 %", "91.4 %", "0.958"]
    ]
    add_table_data(
        tbl3_headers,
        tbl3_data,
        [Inches(2.4), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)],
        "Table 5.2: Anomaly Detection Performance Metrics & Algorithmic Ablation (IEEE Paper Table III)"
    )

    add_heading_2("5.4 Predictive Lead Time & Early Intervention Advantage")
    add_body(
        "The primary clinical value of SmartCattle lies in its early detection lead time prior to visible acute clinical signs. Table 5.3 presents the empirical lead times achieved across all confirmed pathological events.",
        space_after=6
    )

    tbl_lt_headers = ["Pathological Condition", "Average Lead Time Window", "Early Warning Physiological Signature", "Clinical Benefit"]
    tbl_lt_data = [
        ["Subclinical Mastitis", "36.4 ± 8.2 Hours (1.5 Days)", "Milk yield drop (8–14%) + slight temp elevation (0.4°C)", "Enables intra-mammary herbal/antibiotic infusion before tissue scarring"],
        ["Subclinical Ketosis", "42.1 ± 10.5 Hours (1.8 Days)", "Feed refusal (20%) + activity drop without acute fever", "Propylene glycol drenching prevents severe metabolic collapse"],
        ["Bovine Respiratory (BRD)", "28.6 ± 6.4 Hours (1.2 Days)", "Rumination decline (45 min) + mild temperature spike", "Early anti-inflammatory administration prevents lung consolidation"],
        ["Estrus / Heat Cycle", "14.2 ± 3.1 Hours", "Activity spike (+65%) + slight milk yield fluctuation", "Optimal timing for Artificial Insemination (AI) within 12–18 hour window"]
    ]
    add_table_data(
        tbl_lt_headers,
        tbl_lt_data,
        [Inches(1.8), Inches(1.8), Inches(2.0), Inches(1.6)],
        "Table 5.3: Subclinical Disease Lead Time and Detection Window Analysis"
    )

    add_heading_2("5.5 Computational Latency, Throughput & Edge Footprint")
    add_body(
        "The system's computational performance was benchmarked on standard budget smartphones (MediaTek Helio G85 processor, 4GB RAM, 4G mobile connection). Table 5.4 provides the latency breakdown.",
        space_after=6
    )

    tbl_lat_headers = ["Operational Step / Pipeline Stage", "Execution Engine", "Mean Latency", "P99 Latency", "Resource Footprint"]
    tbl_lat_data = [
        ["QR Code Video Stream Scanning", "html5-qrcode (WASM)", "18.2 ms", "32.0 ms", "< 12 MB Client RAM"],
        ["Individual Baseline Retrieval", "Prisma ORM / Indexed DB", "14.5 ms", "26.4 ms", "< 2 MB Memory Cache"],
        ["Mahalanobis Anomaly Calculation", "Python FastAPI / SciPy", "4.8 ms", "8.2 ms", "< 0.5 MB Memory"],
        ["LOCO Feature Attribution", "Python FastAPI / NumPy", "3.6 ms", "6.1 ms", "< 1.2 MB Memory"],
        ["End-to-End Total Ingestion & Diagnosis", "Full Stack Pipeline", "41.1 ms", "72.7 ms", "< 35 MB Total Heap"]
    ]
    add_table_data(
        tbl_lat_headers,
        tbl_lat_data,
        [Inches(2.2), Inches(1.6), Inches(1.0), Inches(1.0), Inches(1.4)],
        "Table 5.4: End-to-End Latency and Computational Footprint Breakdown"
    )

    add_heading_2("5.6 Comparative Evaluation with Commercial Wearable IoT Solutions")
    add_body(
        "Table 5.5 presents a direct comparative evaluation between the proposed system and leading commercial precision dairy solutions.",
        space_after=6
    )

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
    add_table_data(
        tbl_bench_headers,
        tbl_bench_data,
        [Inches(1.8), Inches(1.3), Inches(1.3), Inches(1.3), Inches(1.5)],
        "Table 5.5: Benchmarking SmartCattle against Commercial Wearable IoT Solutions"
    )

    add_heading_2("5.7 Comprehensive Discussion & Practical Insights")
    add_body(
        "The empirical findings demonstrate that SmartCattle achieves diagnostic parity with—and in early lead time slightly exceeds—commercial electronic sensor systems costing hundreds of dollars per head. By shifting the paradigm from costly continuous hardware telemetry to structured, contextualized daily QR observations coupled with individualized baseline forecasting, SmartCattle overcomes the single greatest barrier to precision livestock farming in developing nations.",
        space_after=8
    )
    add_body(
        "The integration of LOCO explainability proved essential during field validation. When rural veterinarians received alerts accompanied by ranked diagnostic factors (e.g., 'CHDI 78: 52% Milk Drop, 28% Rumination Decline, 15% Temperature Elevation'), clinical triage was initiated with high diagnostic confidence, resulting in a 74% reduction in veterinary response latency.",
        space_after=14
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6: CONCLUSION AND FUTURE WORK
    # ==========================================
    add_chapter_title("CONCLUSION AND FUTURE WORK", chapter_number=6)

    add_heading_2("6.1 Conclusion")
    add_body(
        "This project successfully conceptualized, mathematically formulated, implemented, and empirically validated the proposed system, an AI-powered, QR-based cattle health management platform designed specifically for smallholder dairy farmers. By decoupling precision livestock healthcare from expensive on-animal electronic sensors, the proposed system establishes a transformative, zero-hardware-cost paradigm that operates effectively within the economic and infrastructural realities of developing agrarian economies.",
        space_after=8
    )
    add_body(
        "At the core of the system, the Composite Health Deviation Index (CHDI) algorithm integrates individual adaptive baseline estimation, Tikhonov-regularized multivariate Mahalanobis distance anomaly scoring, supervised veterinary feedback calibration, and LOCO feature attribution. In longitudinal field trials across 120 dairy cattle over an 8-week period, the proposed system achieved an anomaly detection sensitivity of 93.8%, specificity of 96.2%, and an overall diagnostic accuracy of 95.1%, providing early warning lead times of 24 to 48 hours prior to acute clinical symptoms.",
        space_after=10
    )

    add_heading_2("6.2 Summary of Key Contributions")
    add_body(
        "The primary academic, technical, and socioeconomic contributions of this project include:",
        space_after=6
    )
    add_bullet("1. Democratization of Precision Livestock Healthcare:", "Reduced the per-animal health monitoring cost from $150–$350 to under $0.50 (a 99.7% cost reduction), enabling immediate adoption across resource-constrained smallholder farms.")
    add_bullet("2. Novel Multi-Stage Mathematical Formulation (CHDI):", "Formulated a regularized multivariate deviation metric that eliminates population bias by tracking individual homeostasis trajectories.")
    add_bullet("3. Explainable Veterinary Clinical Triage:", "Provided transparent, LOCO-based feature attribution that ranks the exact physiological contributors driving health risk scores.")
    add_bullet("4. High-Efficiency Edge-First Web Architecture:", "Engineered an end-to-end TypeScript and Next.js 14 architecture delivering sub-42ms inference latencies on standard mobile smartphone browsers without native app friction.")
    add_body("", space_after=10)

    add_heading_2("6.3 Future Work")
    add_body(
        "Building upon the successful foundational outcomes of the proposed system, several promising research avenues are planned for future expansion:",
        space_after=6
    )
    add_bullet("1. Offline-First Synchronization via CRDTs:", "Implementing Conflict-Free Replicated Data Types (CRDTs) and local browser storage (IndexedDB) to enable seamless, offline-first data logging in remote rural areas with zero cellular connectivity, automatically reconciling data upon reconnecting.")
    add_bullet("2. Multilingual Vernacular Voice Assistant:", "Integrating edge-based automatic speech recognition (ASR) in regional languages (Tamil, Hindi, Telugu, Kannada) to allow illiterate or semi-literate farmers to log telemetry via simple spoken voice commands.")
    add_bullet("3. Satellite & Microclimate Environmental Correlation:", "Correlating farm-level CHDI anomalies with regional weather telemetry (temperature-humidity index, heat waves, rainfall anomalies) to forecast regional disease outbreaks and heat stress.")
    add_bullet("4. Blockchain-Enabled Vaccination & Milk Provenance:", "Integrating a decentralized ledger (e.g., Ethereum / Polygon L2) to issue tamper-proof vaccination certificates and milk quality audit trails, facilitating direct premium market access for smallholder producers.")
    add_body("", space_after=14)

    doc.add_page_break()

    # ==========================================
    # REFERENCES (Directly from IEEE Paper)
    # ==========================================
    add_chapter_title("REFERENCES")

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
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.line_spacing = 1.2
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(10.5)
        r_ref.font.color.rgb = COLOR_BLACK

    # Save to final document
    output_filename = "SmartCattle_Mini_Project_Report.docx"
    doc.save(output_filename)
    print(f"Successfully generated IEEE-aligned report without blue font: {output_filename}")

if __name__ == "__main__":
    create_academic_report()
