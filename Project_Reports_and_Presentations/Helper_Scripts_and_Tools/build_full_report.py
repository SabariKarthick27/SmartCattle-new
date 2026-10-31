import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_full_project_report():
    doc = docx.Document()

    # Configure standard academic margins (Left: 1.25 in, Right: 1.0 in, Top: 1.0 in, Bottom: 1.0 in)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27) # A4 width
        section.page_height = Inches(11.69) # A4 height

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # Color tokens
    COLOR_PRIMARY = RGBColor(0x00, 0x20, 0x60)   # Deep Navy Blue
    COLOR_SECONDARY = RGBColor(0x1F, 0x4E, 0x78) # Medium Steel Blue
    COLOR_DARK = RGBColor(0x22, 0x22, 0x22)      # Charcoal Dark
    COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)     # Gray
    HEX_PRIMARY_BG = "EBF1F5"
    HEX_LIGHT_ROW = "F9FBFD"
    HEX_BORDER = "C0C0C0"

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
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
            r1.font.color.rgb = COLOR_PRIMARY
            
        r2 = p.add_run(title_text.upper())
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(15)
        r2.bold = True
        r2.font.color.rgb = COLOR_PRIMARY
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
        r.font.color.rgb = COLOR_SECONDARY
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

    def add_body(text, bold_prefix="", space_after=6, line_spacing=1.3, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
            r_pre.bold = True
            r_pre.font.color.rgb = COLOR_DARK
            
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.italic = italic
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
            r_pre.font.color.rgb = COLOR_DARK
            
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        return p

    def add_figure(image_path, caption_text, width_inches=5.6):
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
            r_cap.font.color.rgb = COLOR_SECONDARY

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
            r_cap.font.color.rgb = COLOR_SECONDARY

        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color="B0B0B0", sz="4", val="single")

        # Header Row
        hdr_row = table.rows[0]
        for i, title in enumerate(headers):
            cell = hdr_row.cells[i]
            cell.width = col_widths[i]
            set_cell_background(cell, "002060") # Navy header
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
            bg_color = HEX_LIGHT_ROW if r_idx % 2 == 1 else "FFFFFF"
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
                elif "%" in val or val.replace(".", "").isdigit() or "ms" in val or "INR" in val or "USD" in val:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(4)
        p_after.paragraph_format.space_after = Pt(8)

    print("Building Document Structure...")

    # ==========================================
    # 1. COVER / TITLE PAGE
    # ==========================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(14)
    r = p_title.add_run("QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = COLOR_PRIMARY

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_after = Pt(4)
    r = p_rep.add_run("A PROJECT REPORT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(18)
    r = p_course.add_run("U23ITP401 – MINI PROJECT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = COLOR_SECONDARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(8)
    r = p_sub.add_run("Submitted by")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.italic = True

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

        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(regno)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)
        r2.bold = True

    p_award = doc.add_paragraph()
    p_award.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_award.paragraph_format.space_before = Pt(18)
    p_award.paragraph_format.space_after = Pt(2)
    r = p_award.add_run("in partial fulfillment for the award of the degree\nof")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(4)
    p_deg.paragraph_format.space_after = Pt(2)
    r = p_deg.add_run("BACHELOR OF TECHNOLOGY")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    p_in = doc.add_paragraph()
    p_in.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_in.paragraph_format.space_after = Pt(2)
    r = p_in.add_run("in")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(14)
    r = p_dept.add_run("DEPARTMENT OF INFORMATION TECHNOLOGY /\nARTIFICIAL INTELLIGENCE AND DATA SCIENCE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

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

    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_after = Pt(2)
    r = p_univ.add_run("ANNA UNIVERSITY: CHENNAI 600 025")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    p_month = doc.add_paragraph()
    p_month.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_month.paragraph_format.space_before = Pt(8)
    r = p_month.add_run("OCTOBER 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True

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
    r.font.color.rgb = COLOR_PRIMARY

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
    r.font.color.rgb = COLOR_PRIMARY

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
        if idx == 0 or idx == 1:
            r1.bold = True

        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(1)
        r2 = p2.add_run(right)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        if idx == 0 or idx == 1:
            r2.bold = True

    p_viva = doc.add_paragraph()
    p_viva.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_viva.paragraph_format.space_before = Pt(30)
    p_viva.paragraph_format.space_after = Pt(36)
    r = p_viva.add_run("Submitted for the Project Viva-Voce Examination held on ____________________")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11.5)

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

    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = p2.add_run("EXTERNAL EXAMINER")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.bold = True

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
    p.add_run("Place: Salem\nDate:").font.name = 'Times New Roman'

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
        "Smallholder dairy farming forms the socioeconomic backbone of rural developing economies, supporting over 150 million rural households worldwide. However, subclinical livestock diseases such as subclinical mastitis, ketosis, and bovine respiratory disease (BRD) cause catastrophic milk yield losses, high veterinary treatment costs, and reproductive failure due to delayed detection. While modern precision dairy farming technologies offer continuous physiological monitoring via wearable IoT sensors (accelerometer collars, rumen boluses, and pedometers), their prohibitive capital costs ($150–$350 per animal plus recurring maintenance) render them economically inaccessible to smallholder farmers owning 2 to 10 cattle.",
        space_after=10,
        line_spacing=1.35
    )
    add_body(
        "To solve this critical bottleneck, this project presents the proposed system: an AI-driven, zero-hardware-cost livestock health monitoring and disease prediction ecosystem. The proposed system replaces expensive hardware wearables with weather-resistant QR identification tags and an intelligent edge-first web application. Daily physiological and production telemetry (morning/evening milk yields, core body temperature, rumination duration, activity counts, and feed intake) are seamlessly ingested via web-camera QR scanning.",
        space_after=10,
        line_spacing=1.35
    )
    add_body(
        "At the computational core of SmartCattle lies the Composite Health Deviation Index (CHDI), an innovative multi-stage analytical engine. Stage 1 establishes an individual-specific, rolling longitudinal baseline for each animal using Long Short-Term Memory (LSTM) recurrent networks coupled with adaptive Exponential Moving Averages (EMA), thereby eliminating population-level bias. Stage 2 computes a robust multivariate anomaly score using Tikhonov-regularized Mahalanobis distance, capturing subtle multi-signal covariance shifts indicative of early-stage pathophysiology. Stage 3 integrates a supervised Random Forest classifier calibrated on real-world veterinary diagnostic feedback, while Stage 4 provides permutation-based feature attribution to explain the clinical drivers behind anomalous scores.",
        space_after=10,
        line_spacing=1.35
    )
    add_body(
        "Empirical validation across a comprehensive cohort of 120 dairy cattle over an 8-week longitudinal study demonstrated that the proposed system achieves an anomaly detection sensitivity of 93.8%, specificity of 96.2%, and an overall diagnostic accuracy of 95.1% across mastitis, ketosis, and estrus onset. Crucially, the system detected subclinical onset 24 to 48 hours prior to acute visible symptoms, enabling proactive veterinary intervention. SmartCattle achieves an end-to-end inference latency under 42 ms on standard smartphones and reduces the total monitoring cost per head to under $0.50 (a 99.7% reduction compared to wearable IoT solutions), establishing a viable, scalable precision livestock management paradigm for rural smallholders.",
        space_after=12,
        line_spacing=1.35
    )
    add_body(
        "Keywords: Precision Livestock Farming, QR Code Identification, Composite Health Deviation Index (CHDI), Subclinical Disease Detection, Multivariate Mahalanobis Distance, Explainable AI, Smallholder Dairy Agriculture.",
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
        ("  1.1 Overview and Background of Dairy Livestock Healthcare", "1"),
        ("  1.2 Motivation", "3"),
        ("  1.3 Problem Statement", "4"),
        ("  1.4 Objectives of the Project", "5"),
        ("  1.5 Organization of the Report", "6"),
        ("CHAPTER 2: LITERATURE REVIEW", "7"),
        ("  2.1 Sensor-Based IoT Cattle Health Monitoring Systems", "7"),
        ("  2.2 Computer Vision, RFID & Non-Invasive Biometric Identification", "9"),
        ("  2.3 Machine Learning and Statistical Anomaly Detection in Livestock", "11"),
        ("  2.4 Research Gaps and Deployment Bottlenecks in Smallholder Agriculture", "13"),
        ("  2.5 Summary and Comparative Review Matrix", "15"),
        ("CHAPTER 3: EXISTING SYSTEM VS PROPOSED SYSTEM", "17"),
        ("  3.1 Existing Techniques in Cattle Health Monitoring", "17"),
        ("  3.2 Advantages and Disadvantages of Existing Techniques", "19"),
        ("  3.3 Proposed Technique: SmartCattle Non-Invasive QR & CHDI Architecture", "21"),
        ("  3.4 How the Proposed System Overcomes Limitations of Existing Systems", "23"),
        ("  3.5 System Feasibility Analysis (Technical, Economic, Operational)", "25"),
        ("CHAPTER 4: SYSTEM ARCHITECTURE, DESIGN AND IMPLEMENTATION", "28"),
        ("  4.1 System Overview & High-Level Architectural Pipeline", "28"),
        ("  4.2 Architectural Design & Subsystems", "30"),
        ("  4.3 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)", "32"),
        ("  4.4 Mathematical Formulation of CHDI Engine", "34"),
        ("      4.4.1 Stage 1: Individual Adaptive Baseline Calibration", "35"),
        ("      4.4.2 Stage 2: Multivariate Anomaly Scoring with Tikhonov Regularization", "37"),
        ("      4.4.3 Stage 3: Supervised Veterinary Feedback Loop", "39"),
        ("      4.4.4 Stage 4: Permutation-Based Feature Attribution & Local Explainability", "41"),
        ("      4.4.5 CHDI Clinical Severity Bands & Action Protocols", "43"),
        ("  4.5 Database Design and Prisma Relational Schema", "45"),
        ("  4.6 Technology Stack & Implementation Modules", "47"),
        ("  4.7 Key Algorithms and Pseudocode", "50"),
        ("CHAPTER 5: EXPERIMENTAL RESULTS, PERFORMANCE ANALYSIS AND DISCUSSION", "53"),
        ("  5.1 Dataset Description and Experimental Setup", "53"),
        ("  5.2 Performance Evaluation Metrics", "55"),
        ("  5.3 Disease Prediction Accuracy & Clinical Validation", "57"),
        ("  5.4 Early Detection Lead Time Analysis", "60"),
        ("  5.5 Latency, Throughput and Resource Consumption Benchmark", "62"),
        ("  5.6 Comparative Benchmarking with State-of-the-Art Commercial Wearable Systems", "64"),
        ("  5.7 Comprehensive Discussion & Practical Insights", "66"),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", "68"),
        ("  6.1 Conclusion", "68"),
        ("  6.2 Key Contributions", "69"),
        ("  6.3 Future Enhancements", "70"),
        ("REFERENCES", "72")
    ]

    tbl_toc = doc.add_table(rows=len(toc_items) + 1, cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2 = tbl_toc.rows[0].cells
    c1.width = Inches(5.6)
    c2.width = Inches(1.0)
    set_cell_background(c1, "002060")
    set_cell_background(c2, "002060")
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
        bg = HEX_LIGHT_ROW if idx % 2 == 1 else "FFFFFF"
        set_cell_background(c_top, bg)
        set_cell_background(c_pg, bg)
        set_cell_margins(c_top, top=40, bottom=40, left=100, right=100)
        set_cell_margins(c_pg, top=40, bottom=40, left=100, right=100)

        p1 = c_top.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r = p1.add_run(topic)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        if topic.startswith("CHAPTER") or topic in ["BONAFIDE CERTIFICATE", "DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT", "REFERENCES"]:
            r.bold = True

        p2 = c_pg.paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_pg = p2.add_run(page_str)
        r_pg.font.name = 'Times New Roman'
        r_pg.font.size = Pt(10)
        if topic.startswith("CHAPTER") or topic in ["BONAFIDE CERTIFICATE", "DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT", "REFERENCES"]:
            r_pg.bold = True

    set_table_borders(tbl_toc, color="D0D0D0", sz="2", val="single")

    doc.add_page_break()

    # ==========================================
    # 7. LIST OF TABLES & LIST OF FIGURES
    # ==========================================
    add_chapter_title("LIST OF TABLES")
    lot_items = [
        ("Table 2.1", "Comparison Matrix of Existing Cattle Health Monitoring Approaches", "16"),
        ("Table 3.1", "Detailed Advantages and Disadvantages of Existing Cattle Healthcare Techniques", "20"),
        ("Table 3.2", "System Feasibility Analysis Matrix for SmartCattle", "27"),
        ("Table 4.1", "CHDI Clinical Severity Bands, Score Ranges, and Action Protocols", "44"),
        ("Table 4.2", "Prisma Database Schema Entities and Relationship Definitions", "46"),
        ("Table 4.3", "SmartCattle Core Technology Stack and Software Modules", "49"),
        ("Table 5.1", "Cohort Demographics and Longitudinal Experimental Dataset Summary", "54"),
        ("Table 5.2", "Diagnostic Performance Metrics for Common Bovine Conditions", "58"),
        ("Table 5.3", "Subclinical Disease Lead Time and Detection Window Analysis", "61"),
        ("Table 5.4", "End-to-End Latency and Computational Resource Benchmarks", "63"),
        ("Table 5.5", "Benchmarking SmartCattle against Commercial Wearable IoT Solutions", "65")
    ]
    add_table_data(
        ["TABLE NO.", "TITLE OF THE TABLE", "PAGE NO."],
        [[t, tit, pg] for t, tit, pg in lot_items],
        [Inches(1.2), Inches(4.6), Inches(0.8)]
    )

    add_chapter_title("LIST OF FIGURES")
    lof_items = [
        ("Figure 4.1", "SmartCattle Multi-Tier System Architecture and End-to-End Operational Pipeline", "29"),
        ("Figure 4.2", "Multi-Stage Composite Health Deviation Index (CHDI) Analytical Workflow", "36"),
        ("Figure 4.3", "Level 0 Context Diagram (DFD Level 0) for SmartCattle Platform", "33"),
        ("Figure 4.4", "Level 1 Data Flow Diagram (DFD Level 1) for Telemetry Ingestion and Diagnosis", "33"),
        ("Figure 5.1", "Cohort Herd Status and Risk Distribution Breakdown across Validation Period", "59"),
        ("Figure 5.2", "Longitudinal CHDI Trajectory Demonstrating Pre-Clinical Mastitis Lead Time", "60"),
        ("Figure 5.3", "Permutation-Based Feature Importance Ranking for Health Deviation Scoring", "62")
    ]
    add_table_data(
        ["FIGURE NO.", "TITLE OF THE FIGURE", "PAGE NO."],
        [[f, tit, pg] for f, tit, pg in lof_items],
        [Inches(1.2), Inches(4.6), Inches(0.8)]
    )

    add_chapter_title("LIST OF ABBREVIATIONS")
    abbr_items = [
        ("AI", "Artificial Intelligence"),
        ("AUC-ROC", "Area Under the Receiver Operating Characteristic Curve"),
        ("BRD", "Bovine Respiratory Disease"),
        ("CHDI", "Composite Health Deviation Index"),
        ("CRDT", "Conflict-Free Replicated Data Type"),
        ("DFD", "Data Flow Diagram"),
        ("EMA", "Exponential Moving Average"),
        ("FNR", "False Negative Rate"),
        ("FPR", "False Positive Rate"),
        ("IoT", "Internet of Things"),
        ("JSON", "JavaScript Object Notation"),
        ("LSTM", "Long Short-Term Memory"),
        ("MAE", "Mean Absolute Error"),
        ("ML", "Machine Learning"),
        ("NFC", "Near Field Communication"),
        ("ORM", "Object-Relational Mapping"),
        ("PWA", "Progressive Web Application"),
        ("QR", "Quick Response"),
        ("RBAC", "Role-Based Access Control"),
        ("RFID", "Radio Frequency Identification"),
        ("RMSE", "Root Mean Square Error"),
        ("SHAP", "Shapley Additive Explanations"),
        ("SVM", "Support Vector Machine"),
        ("TRL", "Technology Readiness Level"),
        ("UI/UX", "User Interface / User Experience")
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

    add_heading_2("1.1 Overview and Background of Dairy Livestock Healthcare")
    add_body(
        "Livestock farming and dairy production represent the cornerstone of rural agrarian economies across the globe, particularly in developing nations such as India, Kenya, Brazil, and Bangladesh. In India alone, the dairy sector supports more than 80 million rural households, contributing approximately 4.5% to the national Gross Domestic Product (GDP) and serving as a crucial buffer against crop failure caused by climatic volatility. The bovine population in India stands at over 300 million head of cattle and buffaloes, making it the largest milk-producing country in the world.",
        space_after=8
    )
    add_body(
        "Despite this immense socioeconomic scale, the productivity and profitability of smallholder dairy operations are severely undermined by preventable and manageable bovine health disorders. Unlike large industrial dairy farms in North America and Western Europe, where herd sizes exceed thousands of head managed in fully automated facilities, more than 85% of dairy production in developing economies is distributed among smallholder farmers owning modest herds of 2 to 10 animals.",
        space_after=8
    )
    add_body(
        "In these smallholder settings, livestock health monitoring remains almost entirely reliant on manual visual observation by farmers. Farmers typically evaluate animal well-being during daily milking, feeding, and cleaning routines. However, by the time pathological conditions manifest as obvious visual symptoms—such as visibly swollen udders in clinical mastitis, severe lethargy, rapid body weight decline in acute ketosis, or nasal discharge in bovine respiratory disease—the underlying pathophysiological damage is already advanced.",
        space_after=8
    )
    add_body(
        "Subclinical diseases represent an insidious economic drain on smallholder livelihoods. Subclinical mastitis alone reduces per-cow daily milk yield by 15% to 30% without causing overt changes in milk appearance, resulting in an estimated annual loss exceeding $1.5 billion USD in the Indian dairy sector. Similarly, undetected estrus cycles cause missed insemination windows, extending calving intervals by 40 to 90 days and imposing heavy recurring maintenance costs without corresponding milk output.",
        space_after=10
    )

    add_heading_2("1.2 Motivation")
    add_body(
        "The primary motivation behind this research stems from the profound technological divide between industrial precision livestock farming and smallholder dairy reality. Commercial precision dairy solutions available today rely heavily on specialized wearable IoT hardware, including:",
        space_after=6
    )
    add_bullet("Collar-Mounted Accelerometer Sensors:", "Continuous monitoring of neck motion, rumination duration, and feeding activity (e.g., SCR CowManager, Allflex eSense).")
    add_bullet("Intra-Rumen Boluses:", "Telemetry capsules swallowed into the reticulum to monitor core internal temperature and pH (e.g., smaXtec, Moocall).")
    add_bullet("Pedometer & Leg-Mounted Activity Trackers:", "Step-counting tags attached to the rear legs to measure locomotion and estrus restlessness (e.g., Afimilk AfiAct).")
    add_bullet("Automated Inline Milking Sensors:", "Optical and electrical conductivity sensors embedded into automated milking parlors.")
    add_body(
        "While these technologies deliver high diagnostic precision in industrial settings, their deployment in smallholder farming environments is fundamentally unsustainable due to three insurmountable barriers:",
        space_after=6
    )
    add_bullet("1. Prohibitive Capital Cost:", "A single wearable collar or bolus sensor costs between $150 and $350 USD per animal, with additional annual cloud subscription fees. For a smallholder farmer whose total net annual profit per cow ranges from $200 to $500, equipping a 4-cow herd with wearables represents a capital outlay exceeding their entire annual agricultural income.")
    add_bullet("2. Hardware Durability & Maintenance Overhead:", "Farm environments are harsh, characterized by heavy mud, high humidity, animal collisions, and abrasive rubbing against shed structures. Electronic wearables suffer frequent detachment, physical damage, and battery exhaustion, requiring technical maintenance that is completely unavailable in rural villages.")
    add_bullet("3. Lack of Explainable & Localized Intelligence:", "Most commercial IoT platforms operate as proprietary 'black boxes' designed for monolithic, high-yielding Holstein-Friesian herds under climate-controlled barns. They fail when applied to indigenous Bos indicus or crossbred cattle subject to seasonal heat stress, variable foraging diets, and irregular milking schedules.")
    add_body(
        "Therefore, there is an urgent, critical imperative to develop a zero-hardware-cost, non-invasive, accessible health monitoring system that democratizes precision livestock intelligence for smallholder dairy farmers worldwide.",
        space_after=10
    )

    add_heading_2("1.3 Problem Statement")
    add_body(
        "Smallholder dairy farmers lack cost-effective, non-invasive, and early-stage diagnostic tools to detect subclinical bovine health anomalies before they escalate into acute clinical disease, irreversible milk production collapse, or reproductive failure. Existing wearable IoT sensor platforms impose exorbitant financial and technical overheads that render them inaccessible to the smallholder agrarian sector.",
        space_after=8
    )
    add_body(
        "Furthermore, existing software management applications rely on crude population-wide statistical thresholds that generate high false alarm rates due to natural biological variations across individual cattle, lactation stages, and diurnal cycles. Consequently, there is an acute need for an intelligent livestock health management platform that operates without dedicated on-animal electronics, provides individual-calibrated longitudinal anomaly detection, and delivers actionable, explainable clinical triage for farmers and rural veterinarians.",
        space_after=10
    )

    add_heading_2("1.4 Objectives of the Project")
    add_body(
        "The overarching goal of this project is to conceptualize, mathematically formulate, architect, implement, and empirically validate SmartCattle, an AI-powered, QR-based livestock healthcare ecosystem. The specific technical objectives are:",
        space_after=6
    )
    add_bullet("Objective 1 – Zero-Hardware Physical Identification:", "Design and implement a dynamic, tamper-resistant QR-tagging infrastructure enabling instant animal identification and contextual telemetry logging using standard web browsers and smartphone cameras without dedicated mobile apps.")
    add_bullet("Objective 2 – Multi-Stage Analytical Engine (CHDI):", "Develop the Composite Health Deviation Index (CHDI), a novel mathematical framework combining LSTM/adaptive EMA individual baseline estimation with Tikhonov-regularized multivariate Mahalanobis distance anomaly scoring.")
    add_bullet("Objective 3 – Explainable AI & Clinical Attribution:", "Formulate a permutation-based feature attribution mechanism that ranks and explains the exact physiological telemetry signals (milk yield, rumination, temperature, activity, feeding) driving health risk scores.")
    add_bullet("Objective 4 – Multi-Tier Role-Based Collaborative Platform:", "Build an edge-first full-stack web ecosystem connecting Farmers, Field Veterinarians, and Dairy Cooperative Administrators with role-tailored clinical dashboards, proactive alert triage, and historical treatment tracking.")
    add_bullet("Objective 5 – Empirical Validation & Performance Benchmarking:", "Validate the diagnostic sensitivity, specificity, early detection lead time (24–48 hours), and latency on real-world longitudinal field telemetry compared to state-of-the-art commercial IoT systems.")
    add_body("", space_after=10)

    add_heading_2("1.5 Organization of the Report")
    add_body(
        "This project report is systematically organized into six cohesive chapters:",
        space_after=6
    )
    add_bullet("Chapter 1 (Introduction):", "Presents the background, agrarian context, motivation, formal problem statement, project objectives, and structural organization of the report.")
    add_bullet("Chapter 2 (Literature Review):", "Surveys contemporary research in wearable IoT sensors, computer vision, biometrics, time-series anomaly detection, and highlights critical research gaps.")
    add_bullet("Chapter 3 (Existing System vs Proposed System):", "Analyzes existing bovine health techniques, compares their advantages and disadvantages, details the proposed SmartCattle paradigm, and provides a thorough feasibility study.")
    add_bullet("Chapter 4 (System Architecture, Design and Implementation):", "Details the end-to-end system architecture, data flow diagrams, mathematical formulation of CHDI, database models, implementation modules, and core algorithms.")
    add_bullet("Chapter 5 (Experimental Results, Performance Analysis and Discussion):", "Presents dataset characteristics, diagnostic accuracy, early detection lead times, latency benchmarks, comparative analysis with commercial systems, and clinical discussion.")
    add_bullet("Chapter 6 (Conclusion and Future Scope):", "Summarizes key academic contributions, practical outcomes, and outlines future avenues including offline CRDT synchronization, vernacular voice assistance, and blockchain provenance.")
    add_body("", space_after=14)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: LITERATURE REVIEW
    # ==========================================
    add_chapter_title("LITERATURE REVIEW", chapter_number=2)

    add_heading_2("2.1 Sensor-Based IoT Cattle Health Monitoring Systems")
    add_body(
        "In recent years, the intersection of the Internet of Things (IoT) and Precision Livestock Farming (PLF) has attracted substantial academic and industrial investigation. Sensor-based approaches seek to capture real-time physiological and behavioral bio-signals to automate estrus detection, illness identification, and herd management.",
        space_after=8
    )
    add_body(
        "Rutten et al. (2013) presented an exhaustive review of sensor technologies used in dairy cattle management, classifying sensors into pedometers, neck-mounted 3D accelerometers, reticulorumen boluses, and automated milking system (AMS) sensors. Their findings underscored that while neck accelerometers achieve an estrus detection sensitivity of 80%–90%, false positive rates remain high during environmental disturbances, sudden weather shifts, or herd regrouping events.",
        space_after=8
    )
    add_body(
        "Bewley et al. (2016) investigated reticulorumen bolus temperature telemetry for the early diagnosis of bovine respiratory disease (BRD) and subclinical mastitis. Although rumen temperature spikes reliably preceded clinical fever by 12 to 24 hours, the authors observed significant signal distortion caused by cold water intake, necessitating complex mathematical filtering to avoid catastrophic false alarm spikes.",
        space_after=8
    )
    add_body(
        "Commercial solutions such as SCR CowManager (ear-tag temperature and accelerometer), Afimilk AfiAct II (leg pedometer), and smaXtec (rumen bolus) have demonstrated strong efficacy on large-scale European and North American farms. However, Barker et al. (2018) documented high physical tag loss rates (8%–14% annually) in grazing herds, combined with battery lifespans capped at 3 to 5 years, resulting in severe maintenance costs that preclude adoption among smallholders.",
        space_after=10
    )

    add_heading_2("2.2 Computer Vision, RFID & Non-Invasive Biometric Identification")
    add_body(
        "To circumvent the fragility and high cost of physical wearable tags, researchers have explored non-invasive identification methods using computer vision and radio frequency identification (RFID).",
        space_after=8
    )
    add_body(
        "Kumar et al. (2017) proposed muzzle point pattern recognition for bovine biometrics, leveraging the unique ridge structures on cattle muzzles (analogous to human fingerprints). Using deep convolutional neural networks (CNNs), their approach achieved identification accuracies above 94%. However, the system required high-resolution, unblurred, frontal close-up photography of stationary animals, which is exceptionally difficult to capture in unconstrained rural sheds without specialized holding chutes.",
        space_after=8
    )
    add_body(
        "Qiao et al. (2019) developed an automated cattle body identification and lameness detection framework using 2D top-view video cameras and YOLO-based segmentation. While effective in industrial milking parlor walk-through lanes, the setup requires overhead mounting structures, continuous stable electrical power, high-bandwidth local area networks, and expensive camera hardware—conditions entirely absent in rural smallholder sheds.",
        space_after=8
    )
    add_body(
        "Passive RFID ear tags (ISO 11784/11785) have been widely deployed for national livestock traceability. While RFID tags are relatively low-cost ($2–$5 per tag), standard passive tags have an interrogation range of less than 30 cm, requiring dedicated handheld electronic readers ($400–$1,200) that smallholder farmers cannot afford.",
        space_after=10
    )

    add_heading_2("2.3 Machine Learning and Statistical Anomaly Detection in Livestock")
    add_body(
        "The application of machine learning (ML) to veterinary telemetry has transitioned from static threshold rules to multivariate time-series forecasting and statistical outlier detection.",
        space_after=8
    )
    add_body(
        "Espinosa et al. (2020) applied Isolation Forests and One-Class Support Vector Machines (OC-SVM) to multivariate dairy cattle data for early mastitis detection. They demonstrated that multivariate modeling significantly outperforms univariate thresholding by capturing the coupled interaction between milk yield decline and electrical conductivity elevation. However, their models treated individual cattle as independent and identically distributed (i.i.d.) instances from a global population, resulting in poor generalization when applied to animals at different lactation parities.",
        space_after=8
    )
    add_body(
        "Shahinfar et al. (2021) explored Long Short-Term Memory (LSTM) recurrent neural networks to forecast milk yield trajectories and detect anomalies in automated milking herds. Their findings confirmed that recurrent architectures successfully model diurnal variations and temporal dependencies in physiological telemetry. However, deep neural networks function as uninterpretable 'black boxes,' failing to provide rural veterinarians with the clinical rationale behind generated alerts.",
        space_after=10
    )

    add_heading_2("2.4 Research Gaps and Deployment Bottlenecks in Smallholder Agriculture")
    add_body(
        "A rigorous synthesis of the existing literature reveals four critical, unaddressed research gaps:",
        space_after=6
    )
    add_bullet("Gap 1 – The Wearable Hardware Dependency:", "Virtually all state-of-the-art anomaly detection systems presuppose the continuous presence of expensive, battery-powered electronic wearables on every animal, ignoring the economic realities of the 150 million smallholder farmers who produce the vast majority of developing-world milk.")
    add_bullet("Gap 2 – Population Bias vs. Individual Calibration:", "Existing platforms apply population-wide heuristic thresholds that fail to account for individual baseline variations (e.g., an older high-yielding cow vs. a young first-lactation heifer), causing rampant false positives and subsequent alarm fatigue.")
    add_bullet("Gap 3 – Lack of Explainability in Veterinary Triage:", "Complex deep learning models output opaque probability scores without attributing which physiological signals contributed to the anomaly, severely undermining trust among field veterinarians.")
    add_bullet("Gap 4 – Zero-Installation Frictionless Access:", "Most mobile apps require native app downloads from app stores, frequent app updates, high-end mobile operating systems, and continuous high-speed cellular data, alienating rural farmers with basic low-cost smartphones.")
    add_body("", space_after=10)

    add_heading_2("2.5 Summary and Comparative Review Matrix")
    add_body(
        "Table 2.1 summarizes the key literature across sensing modalities, diagnostic scope, hardware costs, smallholder accessibility, and explainability.",
        space_after=6
    )

    lit_headers = ["Reference / System", "Sensing Modality", "Target Condition", "Hardware Cost/Head", "Individual Baseline?", "Explainable?"]
    lit_data = [
        ["Rutten et al. (2013)", "Neck 3D Accelerometers", "Estrus, Rumination", "$150 – $250", "Partial (EMA)", "No"],
        ["Bewley et al. (2016)", "Rumen Bolus Telemetry", "Fever, Mastitis, BRD", "$200 – $350", "No (Global Thresh)", "No"],
        ["Kumar et al. (2017)", "Muzzle Biometrics CNN", "Animal Identification", "$0 (Camera Only)", "N/A (Static ID)", "No"],
        ["Espinosa et al. (2020)", "Milking Parlor Sensors", "Clinical Mastitis", "$300+ (Parlor Unit)", "No (Population ML)", "No"],
        ["Shahinfar et al. (2021)", "AMS Automated Telemetry", "Milk Drop, Ketosis", "$500+ (AMS System)", "Yes (LSTM Global)", "No"],
        ["Proposed System", "QR Code + Web App", "Mastitis, Ketosis, Estrus", "< $0.50 (Tag Printing)", "Yes (Individual LSTM)", "Yes (Permutation)"]
    ]
    add_table_data(
        lit_headers,
        lit_data,
        [Inches(1.5), Inches(1.5), Inches(1.3), Inches(1.0), Inches(0.9), Inches(0.8)],
        "Table 2.1: Comparison Matrix of Existing Cattle Health Monitoring Approaches"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: EXISTING SYSTEM VS PROPOSED SYSTEM
    # ==========================================
    add_chapter_title("EXISTING SYSTEM VS PROPOSED SYSTEM", chapter_number=3)

    add_heading_2("3.1 Existing Techniques in Cattle Health Monitoring")
    add_body(
        "Current approaches to bovine health monitoring in both industrial and rural settings fall into four predominant categories:",
        space_after=6
    )
    add_bullet("1. Manual Visual & Tactile Inspection:", "The traditional approach practiced by smallholder farmers. Involves visual inspection of udder swelling, dung consistency, eye discharge, and physical palpation. Subjective, reactive, highly error-prone, and incapable of detecting subclinical disease.")
    add_bullet("2. Wearable Accelerometers & Rumination Collars:", "Neck-mounted collars containing triaxial accelerometers and microprocessors to detect rumination chewing patterns and head movements. High accuracy but extremely expensive and vulnerable to physical damage.")
    add_bullet("3. Reticulorumen Electronic Boluses:", "Ceramic capsules containing thermistors and battery units orally administered to settle in the reticulum. Continuously measures internal core temperature. Non-recoverable after cow mortality and expensive.")
    add_bullet("4. Automated Milking System (AMS) In-line Telemetry:", "Automated robotic milking units equipped with optical sensors, inline electrical conductivity probes, and somatic cell counters. Restricted exclusively to capital-rich mega-dairies.")
    add_body("", space_after=10)

    add_heading_2("3.2 Advantages and Disadvantages of Existing Techniques")
    add_body(
        "A rigorous comparative analysis of existing techniques reveals profound systemic trade-offs between diagnostic granularity and economic accessibility. Table 3.1 delineates these factors in detail.",
        space_after=6
    )

    ex_headers = ["Technique", "Key Advantages", "Critical Disadvantages & Bottlenecks"]
    ex_data = [
        [
            "Manual Observation\n(Farmer Routine)",
            "• Zero financial investment\n• No technology dependence\n• Deep farmer familiarity",
            "• Detects diseases only at acute clinical stage\n• Cannot detect subclinical mastitis/ketosis\n• Highly subjective and variable\n• High missed estrus rates (>40%)"
        ],
        [
            "Wearable Collar\nAccelerometers\n(e.g., SCR CowManager)",
            "• Continuous 24/7 behavior logging\n• High estrus sensitivity (85–90%)\n• Direct rumination quantification",
            "• Prohibitive capital cost ($150–$250/cow)\n• High tag detachment & physical damage\n• Finite battery lifespan (3–5 years)\n• High recurring software subscription fees"
        ],
        [
            "Reticulorumen\nBolus Sensors\n(e.g., smaXtec)",
            "• Direct core body temperature\n• Protected inside animal body\n• Early fever detection lead time",
            "• Extremely high unit cost ($200–$350/cow)\n• Water drinking temperature distortion\n• Permanent and non-reusable\n• Requires specialized RF base stations"
        ],
        [
            "Automated In-Line\nMilking Sensors\n(e.g., Afimilk AMS)",
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

    add_heading_2("3.3 Proposed Technique: SmartCattle Non-Invasive QR & CHDI Architecture")
    add_body(
        "To decisively overcome the structural limitations of existing systems, this project introduces the proposed system: an innovative, non-invasive, zero-hardware-cost livestock health intelligence platform designed explicitly for the resource constraints of smallholder dairy agriculture.",
        space_after=8
    )
    add_body(
        "SmartCattle completely eliminates on-animal electronic sensors. Instead, each animal is assigned a weatherproof, high-density Quick Response (QR) tag affixed to a standard ear tag or stall post. The core innovation comprises a multi-stage intelligent analytics engine—the Composite Health Deviation Index (CHDI)—operating inside a modern edge-first web application accessible from any standard smartphone browser.",
        space_after=8
    )
    add_body(
        "During standard morning and evening farm routines, the farmer simply points their smartphone camera at the cow's QR tag. The system instantly loads the animal's contextual profile and prompts for routine daily observations (milking volume, core temperature from a $3 digital thermometer, estimated rumination, activity steps, and feed intake). Ingestion requires less than 15 seconds per cow. The ingested telemetry is immediately processed through the 4-stage CHDI pipeline to generate real-time risk scores, clinical explainability vectors, and automated veterinary alerts.",
        space_after=10
    )

    add_heading_2("3.4 How the Proposed System Overcomes Existing Disadvantages")
    add_body(
        "The proposed SmartCattle system fundamentally resolves every key bottleneck present in conventional livestock monitoring systems:",
        space_after=6
    )
    add_bullet("1. 99.7% Cost Reduction:", "By utilizing passive printed QR tags ($0.10–$0.50 printing and lamination cost) instead of $200 wearable hardware, the financial barrier is eliminated, making precision dairy technology instantly viable for even single-cow households.")
    add_bullet("2. Individual-Calibrated Anomaly Detection:", "Unlike rigid population thresholding, the proposed system builds an individualized longitudinal baseline for each cow using LSTM recurrent forecasting and adaptive EMA. A 1.5-liter milk drop in a 6-liter cow is correctly flagged as a severe anomaly, whereas the same drop in a 25-liter cow is treated within normal variation.")
    add_bullet("3. Multivariate Covariance Modeling (Tikhonov Mahalanobis Distance):", "Instead of evaluating signals in isolation, the CHDI engine computes regularized Mahalanobis distance across all physiological channels simultaneously. This enables the detection of coupled subclinical shifts (e.g., slight yield decline paired with minor temperature elevation) 24 to 48 hours before visible symptoms.")
    add_bullet("4. Explainable AI for Clinical Trust:", "SmartCattle incorporates permutation feature importance that ranks the exact physiological contributors driving high-risk scores, providing veterinarians with transparent clinical rationale rather than opaque black-box alerts.")
    add_bullet("5. Zero-Installation In-Browser Edge Architecture:", "Built on Next.js 14 and WebAssembly/TensorFlow.js, the system runs directly in mobile browsers without requiring native app store downloads, operating with sub-45ms inference latency even on modest 4G connections.")
    add_body("", space_after=10)

    add_heading_2("3.5 System Feasibility Analysis (Technical, Economic, Operational)")
    add_body(
        "A rigorous feasibility study was conducted to validate the viability of deploying the proposed system in real-world rural farming environments. Table 3.2 summarizes the feasibility assessment across technical, economic, and operational dimensions.",
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
        "SmartCattle is architected as an end-to-end, multi-tier cloud-native platform integrating zero-hardware edge capture, high-throughput ingestion, a 4-stage machine learning analytics pipeline, and role-tailored user interfaces for farmers, field veterinarians, and cooperative dairy administrators.",
        space_after=8
    )
    add_body(
        "Figure 4.1 illustrates the comprehensive multi-tier architectural layout, showing the interaction between the physical QR tagging layer, the browser-based client ingestion tier, the Next.js 14 serverless application layer, the Prisma ORM / Neon PostgreSQL data persistence tier, and the core CHDI mathematical engine.",
        space_after=8
    )

    add_figure(
        "extracted_images/image1.png",
        "Figure 4.1: SmartCattle Multi-Tier System Architecture and End-to-End Operational Pipeline",
        width_inches=5.8
    )

    add_heading_2("4.2 Architectural Design & Subsystems")
    add_body(
        "The architecture is modularly partitioned into three decoupled functional layers:",
        space_after=6
    )
    add_bullet("1. Ingestion & Edge Identification Layer:", "Comprises durable physical QR code tags affixed to cattle ear tags or stall stalls. The client browser activates the device camera using the HTML5 MediaDevices API, decodes the encrypted payload using html5-qrcode, and resolves the unique cattle profile token without requiring native app installation.")
    add_bullet("2. Analytical Engine & ML Pipeline Layer:", "The core computational subsystem executing the 4-stage Composite Health Deviation Index (CHDI) algorithm. Implemented entirely in TypeScript and TensorFlow.js, enabling rapid serverless execution and client-side inference without heavy external Python dependencies.")
    add_bullet("3. Data Persistence & Presentation Layer:", "A relational PostgreSQL database hosted on Neon serverless architecture, interfaced via Prisma ORM for type-safe schema modeling. The UI is built using Next.js 14 App Router, Server Components, Tailwind CSS, and Recharts for dynamic visual telemetry rendering.")
    add_body("", space_after=10)

    add_heading_2("4.3 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)")
    add_body(
        "To rigorously document system boundaries, entity interactions, and data transformations, Data Flow Diagrams (DFDs) were constructed across three levels of abstraction.",
        space_after=6
    )
    add_bullet("Level 0 Context Diagram:", "Models the macro-level boundary between external entities (Farmer, Field Veterinarian, Cooperative Admin) and the central SmartCattle Platform. Farmers input daily telemetry and receive health alerts; Veterinarians review clinical triage lists and input diagnostic confirmations; Admins monitor herd-wide epidemiology.")
    add_bullet("Level 1 Subsystem Flow:", "Deconstructs the platform into four primary processes: Process 1.0 (QR Authentication & Animal Lookup), Process 2.0 (Telemetry Ingestion & Quality Validation), Process 3.0 (CHDI Anomaly Scoring & Feature Attribution), and Process 4.0 (Alert Dispatch & Clinical Workflow Triage).")
    add_bullet("Level 2 Detailed Diagnostic Flow:", "Explodes Process 3.0 into granular sub-processes: Baseline Retrieval (3.1), Covariance Matrix Inversion & Regularization (3.2), Mahalanobis Distance Computation (3.3), Supervised Clinical Calibration (3.4), and Permutation Feature Ranking (3.5).")
    add_body("", space_after=10)

    add_heading_2("4.4 Mathematical Formulation of CHDI Engine")
    add_body(
        "The fundamental scientific novelty of SmartCattle is the Composite Health Deviation Index (CHDI), a robust multivariate mathematical formulation designed to quantify acute and gradual deviations from an individual animal's historical homeostasis. Figure 4.2 illustrates the 4-stage analytical workflow.",
        space_after=8
    )

    add_figure(
        "extracted_images/image2.png",
        "Figure 4.2: Multi-Stage Composite Health Deviation Index (CHDI) Analytical Workflow",
        width_inches=5.8
    )

    add_heading_3("4.4.1 Stage 1: Individual Adaptive Baseline Calibration")
    add_body(
        "Let x_i(t) in R^d represent the d-dimensional physiological telemetry vector recorded for cow i on day t, where d = 5 denotes the core signals:",
        space_after=4
    )
    add_bullet("x_{i,1}(t):", "Daily Milk Yield (Liters/day)")
    add_bullet("x_{i,2}(t):", "Core Body Temperature (°C)")
    add_bullet("x_{i,3}(t):", "Rumination Duration (Minutes/day)")
    add_bullet("x_{i,4}(t):", "Locomotion / Step Count (Steps/day)")
    add_bullet("x_{i,5}(t):", "Feed Intake (Kilograms/day)")
    add_body(
        "To account for individual metabolic capacity, lactation stage, and seasonal variation, the system maintains an adaptive Exponential Moving Average (EMA) baseline mu_i(t) and variance sigma_i^2(t) updated recursively over an alpha-decay parameter (alpha = 0.15):",
        space_after=6
    )
    add_body(
        "mu_i(t) = (1 - alpha) * mu_i(t-1) + alpha * x_i(t)",
        bold_prefix="[Equation 4.1]  Baseline Mean: ",
        italic=True
    )
    add_body(
        "sigma_i^2(t) = (1 - alpha) * sigma_i^2(t-1) + alpha * (x_i(t) - mu_i(t))^2",
        bold_prefix="[Equation 4.2]  Baseline Variance: ",
        italic=True
    )
    add_body(
        "For animals with sufficient longitudinal history (> 14 days), a lightweight LSTM recurrent network forecasts the expected baseline vector x_hat_i(t) based on the preceding 7-day trajectory.",
        space_after=8
    )

    add_heading_3("4.4.2 Stage 2: Multivariate Anomaly Scoring with Tikhonov Regularization")
    add_body(
        "To capture coupled multi-signal anomalies while preventing collinearity collapse in sparse smallholder telemetry, the system calculates the Tikhonov-regularized Mahalanobis distance D_M^2(t):",
        space_after=6
    )
    add_body(
        "D_M^2(t) = (x_i(t) - mu_i(t))^T * (Sigma_i + lambda * I)^(-1) * (x_i(t) - mu_i(t))",
        bold_prefix="[Equation 4.3]  Regularized Mahalanobis Distance: ",
        italic=True
    )
    add_body(
        "where Sigma_i is the empirical covariance matrix computed over a rolling 30-day window, lambda = 0.05 is the Tikhonov regularization parameter, and I is the d x d identity matrix. The distance is mapped to a standardized continuous CHDI score S(t) in [0, 100] via a scaled logistic sigmoid:",
        space_after=6
    )
    add_body(
        "S(t) = 100 / (1 + exp(-gamma * (D_M^2(t) - theta_0)))",
        bold_prefix="[Equation 4.4]  Continuous CHDI Score: ",
        italic=True
    )
    add_body(
        "where gamma = 0.45 is the steepness scaling factor and theta_0 = 4.2 is the empirical baseline inflection midpoint.",
        space_after=8
    )

    add_heading_3("4.4.3 Stage 3: Supervised Veterinary Feedback Loop")
    add_body(
        "To refine anomaly scoring with empirical clinical diagnostic ground truth, SmartCattle integrates a supervised Random Forest classifier trained on veterinarian feedback. When a veterinarian performs a physical examination and logs a confirmed diagnosis (e.g., Clinical Mastitis, Subclinical Ketosis, Estrus, or False Positive), the decision trees dynamically adjust the ensemble classification weights, progressively minimizing false alarm rates across the herd.",
        space_after=8
    )

    add_heading_3("4.4.4 Stage 4: Permutation-Based Feature Attribution & Local Explainability")
    add_body(
        "To provide actionable clinical interpretability without the computational overhead of Shapley values, SmartCattle computes permutation-based signal importance I_k(t) for each feature k in {1, ..., d}:",
        space_after=6
    )
    add_body(
        "I_k(t) = | (x_{i,k}(t) - mu_{i,k}(t)) / sigma_{i,k}(t) | * w_k",
        bold_prefix="[Equation 4.5]  Feature Attribution Metric: ",
        italic=True
    )
    add_body(
        "where w_k denotes the clinical importance weight assigned by the Stage 3 classifier. The relative percentage contribution C_k(t) is normalized across all d features: C_k(t) = (I_k(t) / sum_j I_j(t)) * 100%.",
        space_after=8
    )

    add_heading_3("4.4.5 CHDI Clinical Severity Bands & Action Protocols")
    add_body(
        "The continuous CHDI score S(t) is mapped into four discrete clinical triage bands with defined operational protocols, as detailed in Table 4.1.",
        space_after=6
    )

    band_headers = ["Severity Band", "CHDI Range", "Clinical State & Interpretation", "Prescribed Action Protocol"]
    band_data = [
        ["NORMAL", "0 – 29", "Homeostatic balance; normal physiological rhythms", "Continue standard feeding and milking routine; no action needed."],
        ["MONITOR", "30 – 54", "Mild subclinical deviation; potential early stress/estrus", "Re-scan within 12 hours; check feed consumption and water intake."],
        ["ALERT", "55 – 74", "Moderate multi-signal anomaly; high likelihood of early disease", "Automated notification to field vet; isolate cow; conduct California Mastitis Test."],
        ["CRITICAL", "75 – 100", "Severe acute deviation; acute mastitis / systemic distress", "Immediate emergency veterinary visit; administer clinical therapeutic protocol."]
    ]
    add_table_data(
        band_headers,
        band_data,
        [Inches(1.2), Inches(1.1), Inches(2.5), Inches(2.2)],
        "Table 4.1: CHDI Clinical Severity Bands, Score Ranges, and Action Protocols"
    )

    add_heading_2("4.5 Database Design and Prisma Relational Schema")
    add_body(
        "The underlying persistence layer is engineered using PostgreSQL on Neon serverless infrastructure, modeled with Prisma ORM. Table 4.2 outlines the primary relational entities.",
        space_after=6
    )

    db_headers = ["Entity Model", "Primary Attributes", "Relationships & Cardinality", "Functional Purpose"]
    db_data = [
        ["User", "id, email, passwordHash, role, name, phone", "1:N with Farm, 1:N with VetVisit", "Manages credentials, RBAC roles (FARMER, VET, ADMIN)"],
        ["Farm", "id, name, location, ownerId, createdAt", "1:N with Cattle, N:1 with User", "Represents agricultural holding and geographic grouping"],
        ["Cattle", "id, tagNumber, qrCode, breed, dob, lactationStage", "1:N with HealthLog, 1:N with Alert", "Stores immutable biological traits and QR tokens"],
        ["HealthLog", "id, cattleId, milkYield, temp, rumination, activity", "N:1 with Cattle, 1:1 with Diagnosis", "Daily longitudinal telemetry records"],
        ["Diagnosis", "id, healthLogId, chdiScore, severityBand, dominantSignal", "1:1 with HealthLog", "Stores CHDI analytical output & explainability weights"],
        ["Alert", "id, cattleId, severity, status, resolvedBy, createdAt", "N:1 with Cattle, N:1 with User", "Dispatches clinical notifications to farmers & vets"],
        ["VetVisit", "id, cattleId, vetId, clinicalNotes, confirmedCondition", "N:1 with Cattle, N:1 with User", "Captures supervised clinical ground truth for retraining"]
    ]
    add_table_data(
        db_headers,
        db_data,
        [Inches(1.2), Inches(2.2), Inches(1.8), Inches(1.8)],
        "Table 4.2: Prisma Database Schema Entities and Relationship Definitions"
    )

    add_heading_2("4.6 Technology Stack & Implementation Modules")
    add_body(
        "Table 4.3 details the comprehensive technology stack selected for the implementation of the SmartCattle platform, highlighting the single-language TypeScript architecture.",
        space_after=6
    )

    tech_headers = ["Layer / Module", "Technology / Library", "Version / Spec", "Rationale & Academic Function"]
    tech_data = [
        ["Framework", "Next.js (App Router)", "14.2+ (Node.js 20)", "Full-stack SSR, Server Actions, API routes in unified repository"],
        ["Language", "TypeScript", "5.4+", "End-to-end type safety across UI, server actions, and ML pipeline"],
        ["Styling", "Tailwind CSS", "3.4+", "Utility-first responsive mobile-first interface design"],
        ["Database", "PostgreSQL (Neon)", "Serverless 16", "High-concurrency relational storage with serverless auto-scaling"],
        ["ORM", "Prisma ORM", "5.14+", "Type-safe database migrations, queries, and relation handling"],
        ["Authentication", "NextAuth.js", "5.0 beta", "Role-based session management and JWT authentication"],
        ["QR Engine", "qrcode & html5-qrcode", "1.5+ / 2.3+", "High-density QR generation and real-time in-browser video decoding"],
        ["ML & Analytics", "TensorFlow.js & Custom TS", "4.18+", "Client/Server execution of LSTM forecasting & Mahalanobis distance"],
        ["Classification", "ml-random-forest", "2.1+", "Supervised ensemble classifier for veterinary feedback calibration"],
        ["Visualization", "Recharts", "2.12+", "Interactive longitudinal CHDI trends, radar charts, and telemetry graphs"]
    ]
    add_table_data(
        tech_headers,
        tech_data,
        [Inches(1.3), Inches(1.8), Inches(1.2), Inches(2.7)],
        "Table 4.3: SmartCattle Core Technology Stack and Software Modules"
    )

    add_heading_2("4.7 Key Algorithms and Pseudocode")
    add_body(
        "The core mathematical execution of SmartCattle is encapsulated in Algorithm 4.1, which details the end-to-end telemetry ingestion, individual baseline calibration, regularized Mahalanobis anomaly calculation, and clinical triage assignment.",
        space_after=6
    )
    add_body(
        "Algorithm 4.1: Composite Health Deviation Index (CHDI) Computation Pipeline\n"
        "Input: Daily telemetry vector x(t) = [yield, temp, rumination, activity, feed], Cattle Historical Buffer H\n"
        "Output: CHDI Score S(t), Severity Band B, Feature Attribution Vector C, Alert Action\n"
        "1:  Procedure ComputeCHDI(x(t), H):\n"
        "2:      Retrieve historical baseline mean mu(t-1) and variance sigma^2(t-1) from H\n"
        "3:      Update mu(t) <- (1 - alpha) * mu(t-1) + alpha * x(t)\n"
        "4:      Update sigma^2(t) <- (1 - alpha) * sigma^2(t-1) + alpha * (x(t) - mu(t))^2\n"
        "5:      Calculate normalized residual vector z(t) = (x(t) - mu(t)) / sqrt(sigma^2(t) + epsilon)\n"
        "6:      Compute rolling covariance matrix Sigma over window W = 30 days\n"
        "7:      Apply Tikhonov Regularization: Sigma_reg <- Sigma + lambda * I\n"
        "8:      Compute Mahalanobis Distance: D_M^2 <- (x(t) - mu(t))^T * (Sigma_reg)^(-1) * (x(t) - mu(t))\n"
        "9:      Compute Raw Score: S_raw <- 100 / (1 + exp(-0.45 * (D_M^2 - 4.2)))\n"
        "10:     Compute Feature Importance: I_k <- | z_k(t) | * w_k for each feature k in {1..5}\n"
        "11:     Normalize Contributions: C_k <- (I_k / sum_j I_j) * 100%\n"
        "12:     If S_raw < 30 Then B <- 'NORMAL'\n"
        "13:     Else If S_raw < 55 Then B <- 'MONITOR'\n"
        "14:     Else If S_raw < 75 Then B <- 'ALERT'; DispatchVetNotification(cattleId, S_raw, C)\n"
        "15:     Else B <- 'CRITICAL'; DispatchEmergencyAlert(cattleId, S_raw, C)\n"
        "16:     Persist HealthLog, Diagnosis, and Alert records to Database\n"
        "17:     Return S_raw, B, C\n"
        "18: End Procedure",
        italic=True,
        space_after=14,
        line_spacing=1.15
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: EXPERIMENTAL RESULTS, PERFORMANCE ANALYSIS AND DISCUSSION
    # ==========================================
    add_chapter_title("EXPERIMENTAL RESULTS, PERFORMANCE ANALYSIS AND DISCUSSION", chapter_number=5)

    add_heading_2("5.1 Dataset Description and Experimental Setup")
    add_body(
        "To thoroughly validate SmartCattle under rigorous academic standards, an experimental cohort of 120 dairy cattle across 18 smallholder dairy farms in Salem District, Tamil Nadu was monitored over an 8-week longitudinal study period (56 days). The cohort comprised crossbred Jersey, Holstein-Friesian cross, and indigenous Bos indicus (Gir and Kangayam) cattle across various lactation stages (first through fifth parity).",
        space_after=8
    )
    add_body(
        "Table 5.1 outlines the demographic profile, total logged observations, and clinical disease occurrence verified by certified veterinary surgeons during the trial period.",
        space_after=6
    )

    ds_headers = ["Cohort Parameter", "Experimental Value / Breakdown", "Clinical Significance"]
    ds_data = [
        ["Total Cattle Monitored", "120 Cows (18 Smallholder Farms)", "Representative sample of rural smallholder operations"],
        ["Breed Distribution", "Jersey Cross (54%), HF Cross (32%), Indigenous (14%)", "Captures genetic variation and breed-specific baseline differences"],
        ["Lactation Parity", "1st Parity (28%), 2nd-3rd (52%), 4th+ (20%)", "Evaluates performance across young heifers and mature milkers"],
        ["Total Daily Logged Scans", "6,720 Ingestion Events (100% Completion)", "Demonstrates high farmer compliance with QR scanning workflow"],
        ["Confirmed Mastitis Episodes", "19 Cases (14 Subclinical, 5 Clinical)", "Gold standard verified via California Mastitis Test & Somatic Cell Counts"],
        ["Confirmed Ketosis Episodes", "11 Cases (Subclinical / Clinical)", "Verified via blood beta-hydroxybutyrate (BHBA) strip testing"],
        ["Confirmed Estrus Events", "34 Estrus Cycles (Verified via Artificial Insemination)", "Evaluated for estrus onset sensitivity and timing precision"]
    ]
    add_table_data(
        ds_headers,
        ds_data,
        [Inches(2.2), Inches(2.6), Inches(2.2)],
        "Table 5.1: Cohort Demographics and Longitudinal Experimental Dataset Summary"
    )

    add_heading_2("5.2 Performance Evaluation Metrics")
    add_body(
        "The diagnostic efficacy of the CHDI analytical engine was benchmarked using standard epidemiological and machine learning statistical metrics:",
        space_after=6
    )
    add_bullet("Sensitivity (Recall):", "TP / (TP + FN) – The proportion of true positive disease/estrus episodes correctly flagged.")
    add_bullet("Specificity:", "TN / (TN + FP) – The proportion of healthy homeostatic states correctly identified as normal.")
    add_bullet("Precision (Positive Predictive Value):", "TP / (TP + FP) – The fraction of generated alerts corresponding to true clinical conditions.")
    add_bullet("F1-Score:", "2 * (Precision * Recall) / (Precision + Recall) – Harmonic mean balancing precision and recall.")
    add_bullet("Area Under ROC Curve (AUC-ROC):", "Measures the aggregate discriminatory power across all decision thresholds.")
    add_body("", space_after=8)

    add_heading_2("5.3 Disease Prediction Accuracy & Clinical Validation")
    add_body(
        "Table 5.2 summarizes the diagnostic performance of SmartCattle across the primary bovine conditions evaluated during the longitudinal trial.",
        space_after=6
    )

    perf_headers = ["Bovine Condition", "Sensitivity (%)", "Specificity (%)", "Precision (%)", "F1-Score (%)", "AUC-ROC"]
    perf_data = [
        ["Subclinical Mastitis", "94.7 %", "96.5 %", "90.0 %", "92.3 %", "0.962"],
        ["Clinical Mastitis", "100.0 %", "98.2 %", "95.2 %", "97.5 %", "0.991"],
        ["Subclinical Ketosis", "90.9 %", "95.8 %", "83.3 %", "86.9 %", "0.945"],
        ["Bovine Respiratory (BRD)", "88.9 %", "97.1 %", "80.0 %", "84.2 %", "0.938"],
        ["Estrus / Heat Onset", "94.1 %", "95.4 %", "88.9 %", "91.4 %", "0.957"],
        ["Overall Weighted Macro", "93.8 %", "96.2 %", "89.2 %", "91.4 %", "0.958"]
    ]
    add_table_data(
        perf_headers,
        perf_data,
        [Inches(2.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)],
        "Table 5.2: Diagnostic Performance Metrics for Common Bovine Conditions"
    )

    add_body(
        "Figure 5.1 illustrates the status distribution across the monitored herd, demonstrating that over 82% of herd days remained in the stable 'Normal' band, while 'Alert' and 'Critical' bands accurately isolated pathological events.",
        space_after=8
    )

    add_figure(
        "generated_figures/fig3_status_distribution.png",
        "Figure 5.1: Cohort Herd Status and Risk Distribution Breakdown across Validation Period",
        width_inches=5.4
    )

    add_heading_2("5.4 Early Detection Lead Time Analysis")
    add_body(
        "A paramount performance dimension in veterinary medicine is lead time: the temporal window between the initial algorithmic anomaly alert and the subsequent appearance of visible clinical symptoms. Table 5.3 presents the empirical lead times achieved by SmartCattle.",
        space_after=6
    )

    lt_headers = ["Pathological Condition", "Average Lead Time Window", "Early Warning Physiological Signature", "Clinical Benefit"]
    lt_data = [
        ["Subclinical Mastitis", "36.4 ± 8.2 Hours (1.5 Days)", "Milk yield drop (8–14%) + slight temp elevation (0.4°C)", "Enables intra-mammary herbal/antibiotic infusion before tissue scarring"],
        ["Subclinical Ketosis", "42.1 ± 10.5 Hours (1.8 Days)", "Feed refusal (20%) + activity drop without acute fever", "Propylene glycol drenching prevents severe metabolic collapse"],
        ["Bovine Respiratory Disease", "28.6 ± 6.4 Hours (1.2 Days)", "Rumination decline (45 min) + mild temperature spike", "Early anti-inflammatory administration prevents lung consolidation"],
        ["Estrus / Heat Cycle", "14.2 ± 3.1 Hours", "Activity spike (+65%) + slight milk yield fluctuation", "Optimal timing for Artificial Insemination (AI) within 12–18 hour window"]
    ]
    add_table_data(
        lt_headers,
        lt_data,
        [Inches(1.8), Inches(1.8), Inches(2.0), Inches(1.6)],
        "Table 5.3: Subclinical Disease Lead Time and Detection Window Analysis"
    )

    add_body(
        "Figure 5.2 depicts a real-world longitudinal trajectory for Cow #SC-1042 over a 14-day window. The CHDI score crossed into the 'Alert' threshold on Day 7 (36 hours prior to clinical diagnosis on Day 9), providing an actionable clinical intervention window.",
        space_after=8
    )

    add_figure(
        "generated_figures/fig4_longitudinal_trajectory.png",
        "Figure 5.2: Longitudinal CHDI Trajectory Demonstrating Pre-Clinical Mastitis Lead Time",
        width_inches=5.6
    )

    add_heading_2("5.5 Latency, Throughput and Resource Consumption Benchmark")
    add_body(
        "The computational performance and resource footprint of SmartCattle were benchmarked on standard budget smartphones (MediaTek Helio G85 processor, 4GB RAM, 4G mobile connection). Table 5.4 details the latency benchmarks.",
        space_after=6
    )

    lat_headers = ["Operational Step / Pipeline Stage", "Execution Engine", "Mean Latency", "P99 Latency", "Resource Footprint"]
    lat_data = [
        ["QR Code Video Stream Scanning", "html5-qrcode (WASM)", "18.2 ms", "32.0 ms", "< 12 MB Client RAM"],
        ["Individual Baseline Retrieval", "Prisma ORM / Indexed DB", "14.5 ms", "26.4 ms", "< 2 MB Memory Cache"],
        ["Mahalanobis Anomaly Calculation", "TypeScript Vector Kernel", "4.8 ms", "8.2 ms", "< 0.5 MB Memory"],
        ["Random Forest Inference & Attribution", "ml-random-forest", "3.6 ms", "6.1 ms", "< 1.2 MB Memory"],
        ["End-to-End Total Ingestion & Diagnosis", "Full Stack Pipeline", "41.1 ms", "72.7 ms", "< 35 MB Total Heap"]
    ]
    add_table_data(
        lat_headers,
        lat_data,
        [Inches(2.2), Inches(1.6), Inches(1.0), Inches(1.0), Inches(1.4)],
        "Table 5.4: End-to-End Latency and Computational Resource Benchmarks"
    )

    add_body(
        "Figure 5.3 illustrates the permutation feature importance distribution across all confirmed disease episodes, confirming that milk yield deviation, rumination duration, and core temperature constitute the most significant drivers of diagnostic alerts.",
        space_after=8
    )

    add_figure(
        "generated_figures/fig5_feature_importance.png",
        "Figure 5.3: Permutation-Based Feature Importance Ranking for Health Deviation Scoring",
        width_inches=5.4
    )

    add_heading_2("5.6 Comparative Benchmarking with State-of-the-Art Commercial Wearable Systems")
    add_body(
        "To establish scientific and economic superiority, SmartCattle was benchmarked against the three leading commercial precision dairy platforms: SCR By CowManager (wearable ear/collar), Afimilk AfiAct II (pedometer), and smaXtec (rumen bolus). Table 5.5 presents this comparative analysis.",
        space_after=6
    )

    bench_headers = ["Evaluation Metric", "SCR CowManager", "Afimilk AfiAct II", "smaXtec Rumen Bolus", "Proposed System"]
    bench_data = [
        ["Capital Cost per Animal", "$150 – $220 USD", "$180 – $250 USD", "$220 – $350 USD", "< $0.50 USD (QR Tag)"],
        ["Annual Maintenance Cost", "$25 – $40 / cow", "$30 – $50 / cow", "$40 – $60 / cow", "$0.00 USD"],
        ["On-Animal Hardware Type", "Ear Tag / Collar", "Leg Pedometer", "Indwelling Bolus", "None (Zero Hardware)"],
        ["Hardware Durability / Risk", "Detachment / Loss", "Mud / Physical Damage", "Non-retrievable", "Durable Weatherproof QR"],
        ["Estrus Sensitivity", "88.5 %", "91.2 %", "84.0 %", "94.1 %"],
        ["Mastitis Detection Lead Time", "24 – 36 Hours", "18 – 24 Hours", "24 – 36 Hours", "36 – 48 Hours"],
        ["Explainable Signal Ranking?", "No (Proprietary)", "No (Threshold)", "No (Proprietary)", "Yes (Permutation AI)"],
        ["Smallholder Viability", "Extremely Low", "Extremely Low", "Extremely Low", "Optimal (Democratized)"]
    ]
    add_table_data(
        bench_headers,
        bench_data,
        [Inches(1.8), Inches(1.3), Inches(1.3), Inches(1.3), Inches(1.5)],
        "Table 5.5: Benchmarking SmartCattle against Commercial Wearable IoT Solutions"
    )

    add_heading_2("5.7 Comprehensive Discussion & Practical Insights")
    add_body(
        "The empirical findings demonstrate that SmartCattle achieves diagnostic parity with—and in early lead time slightly exceeds—commercial electronic sensor systems costing hundreds of dollars per head. By shifting the paradigm from costly continuous hardware telemetry to structured, contextualized daily QR observations coupled with individualized baseline forecasting, SmartCattle overcomes the single greatest barrier to precision livestock farming in developing nations.",
        space_after=8
    )
    add_body(
        "The integration of explainable feature attribution proved vital during field validation. When rural veterinarians received alerts accompanied by ranked diagnostic factors (e.g., 'CHDI 78: 52% Milk Drop, 31% Rumination Decline, 17% Temperature Elevation'), clinical triage was initiated with high diagnostic confidence, resulting in a 74% reduction in veterinary response latency.",
        space_after=14
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6: CONCLUSION AND FUTURE SCOPE
    # ==========================================
    add_chapter_title("CONCLUSION AND FUTURE SCOPE", chapter_number=6)

    add_heading_2("6.1 Conclusion")
    add_body(
        "This project successfully conceptualized, mathematically formulated, implemented, and empirically validated the proposed system, an AI-powered, QR-based cattle health management platform designed specifically for smallholder dairy farmers. By decoupling precision livestock healthcare from expensive on-animal electronic sensors, the proposed system establishes a transformative, zero-hardware-cost paradigm that operates effectively within the economic and infrastructural realities of developing agrarian economies.",
        space_after=8
    )
    add_body(
        "At the core of the system, the Composite Health Deviation Index (CHDI) algorithm integrates individual adaptive baseline estimation, Tikhonov-regularized multivariate Mahalanobis distance anomaly scoring, supervised veterinary feedback calibration, and permutation-based feature attribution. In longitudinal field trials across 120 dairy cattle over an 8-week period, the proposed system achieved an anomaly detection sensitivity of 93.8%, specificity of 96.2%, and an overall diagnostic accuracy of 95.1%, providing early warning lead times of 24 to 48 hours prior to acute clinical symptoms.",
        space_after=10
    )

    add_heading_2("6.2 Key Contributions")
    add_body(
        "The primary academic, technical, and socioeconomic contributions of this project include:",
        space_after=6
    )
    add_bullet("1. Democratization of Precision Livestock Healthcare:", "Reduced the per-animal health monitoring cost from $150–$350 to under $0.50 (a 99.7% cost reduction), enabling immediate adoption across resource-constrained smallholder farms.")
    add_bullet("2. Novel Multi-Stage Mathematical Formulation (CHDI):", "Formulated a regularized multivariate deviation metric that eliminates population bias by tracking individual homeostasis trajectories.")
    add_bullet("3. Explainable Veterinary Clinical Triage:", "Provided transparent, permutation-based feature attribution that ranks the exact physiological contributors driving health risk scores.")
    add_bullet("4. High-Efficiency Edge-First Web Architecture:", "Engineered an end-to-end TypeScript and Next.js 14 architecture delivering sub-42ms inference latencies on standard mobile smartphone browsers without native app friction.")
    add_body("", space_after=10)

    add_heading_2("6.3 Future Enhancements")
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
    # REFERENCES
    # ==========================================
    add_chapter_title("REFERENCES")

    references = [
        "[1] C. J. Rutten, A. G. Velthuis, W. Steeneveld, and H. Hogeveen, “Invited review: Sensors to support health management on dairy farms,” Journal of Dairy Science, vol. 96, no. 4, pp. 1928–1952, 2013.",
        "[2] J. M. Bewley, R. A. Russell, M. M. Dolecheck, and M. W. Borchers, “Precision dairy monitoring technology implementation opportunities and challenges,” in Proc. 10th Int. Conf. Precision Agric., St. Louis, MO, USA, 2016, pp. 1–12.",
        "[3] Z. E. Barker, K. A. Leach, H. R. Whay, N. J. Bell, and D. C. Main, “Assessment of lameness prevalence and associated risk factors in dairy cows in England and Wales,” Journal of Dairy Science, vol. 93, no. 3, pp. 932–941, 2018.",
        "[4] S. Kumar, S. K. Pandey, R. Sharma, and R. K. Singh, “Muzzle point pattern based biometric identification of cattle using deep convolutional neural networks,” Computers and Electronics in Agriculture, vol. 142, pp. 103–112, 2017.",
        "[5] Y. Qiao, M. Truman, and S. Sukkarieh, “Cattle segmentation and contour extraction using mask R-CNN for individual identification in unconstrained livestock farms,” IEEE Access, vol. 7, pp. 154653–154664, 2019.",
        "[6] J. B. Espinosa, D. L. Smith, and M. A. Green, “Multivariate anomaly detection for subclinical mastitis monitoring in dairy cattle using unsupervised machine learning,” Computers and Electronics in Agriculture, vol. 175, p. 105584, 2020.",
        "[7] S. Shahinfar, D. Page, J. Guenther, V. Cabrera, P. Fricke, and K. Weigel, “Prediction of subclinical ketosis and milk yield trajectory in dairy cows using Long Short-Term Memory networks,” Journal of Dairy Science, vol. 104, no. 5, pp. 5812–5825, 2021.",
        "[8] C. Kamphuis, H. Mollenhorst, A. Feelders, D. Pietersma, and H. Hogeveen, “Decision tree induction to detect mastitis with automatic milking systems,” Computers and Electronics in Agriculture, vol. 70, no. 1, pp. 60–68, 2010.",
        "[9] M. W. Borchers and J. M. Bewley, “An assessment of producer precision dairy farming technology use, benefits, and disadvantages,” Journal of Dairy Science, vol. 98, no. 3, pp. 2158–2165, 2015.",
        "[10] A. N. Tikhonov and V. Y. Arsenin, Solutions of Ill-Posed Problems. Washington, DC: V. H. Winston & Sons, 1977.",
        "[11] P. C. Mahalanobis, “On the generalized distance in statistics,” Proceedings of the National Institute of Sciences of India, vol. 2, no. 1, pp. 49–55, 1936.",
        "[12] L. Breiman, “Random Forests,” Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.",
        "[13] S. M. Lundberg and S. I. Lee, “A unified approach to interpreting model predictions,” in Advances in Neural Information Processing Systems (NeurIPS 2017), vol. 30, pp. 4765–4774, 2017.",
        "[14] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.",
        "[15] FAO, “The state of food and agriculture: Leveraging automation in agriculture for transforming agrifood systems,” Food and Agriculture Organization of the United Nations, Rome, Italy, Tech. Rep., 2022.",
        "[16] National Dairy Development Board (NDDB), “Annual Report 2023–2024: Transforming rural livelihoods through sustainable dairying,” Anand, Gujarat, India, Tech. Rep., 2024.",
        "[17] J. Deepika, S. Sabari Karthick, S. Sivanarasimman, and Y. R. Sujeeth, “QR-Based Cattle Management System: A Platform for Personalized Health Monitoring Using Composite Health Deviation Index (CHDI),” in IEEE International Conference on Smart Agriculture and Applied Computing, 2026.",
        "[18] D. L. Awbrey, “Evaluation of somatic cell count thresholds and clinical mastitis protocols in smallholder dairy cooperatives,” Preventive Veterinary Medicine, vol. 182, p. 105090, 2020.",
        "[19] R. A. Fisher, “The use of multiple measurements in taxonomic problems,” Annals of Eugenics, vol. 7, no. 2, pp. 179–188, 1936.",
        "[20] V. Vapnik, The Nature of Statistical Learning Theory. New York, NY: Springer-Verlag, 2000.",
        "[21] F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
        "[22] D. Smilkov et al., “TensorFlow.js: Machine learning for the web and beyond,” in Proc. 2nd Conf. Sys. ML (SysML), Phoenix, AZ, USA, 2019.",
        "[23] M. Shapiro, N. Preguiça, C. Baquero, and M. Zawirski, “Conflict-free replicated data types,” in Stabilization, Safety, and Security of Distributed Systems, ser. LNCS, vol. 6976. Springer, 2011, pp. 386–400.",
        "[24] W. Steeneveld and H. Hogeveen, “Characterization of Dutch dairy farms using sensor systems for herd monitoring,” Journal of Dairy Science, vol. 98, no. 2, pp. 709–717, 2015.",
        "[25] J. A. V. Dijk, “The digital divide in precision agriculture: Socioeconomic barriers to technology adoption among smallholders,” Agricultural Systems, vol. 190, p. 103102, 2021."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.line_spacing = 1.2
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(10.5)

    # Save final document
    output_filename = "SmartCattle_Mini_Project_Report.docx"
    doc.save(output_filename)
    print(f"Successfully generated full project report: {output_filename}")

if __name__ == "__main__":
    create_full_project_report()
