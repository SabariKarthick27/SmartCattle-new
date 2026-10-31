import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_project_report():
    doc = docx.Document()

    # Document Margins (A4: 8.27 x 11.69 inches)
    # Left Margin: 1.25 in (31.75 mm), Right/Top/Bottom: 1.0 in (25.4 mm)
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.25)
        s.right_margin = Inches(1.0)
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)

    # Strict Font Style Rule: Times New Roman exclusively throughout
    COLOR_BLACK = RGBColor(0, 0, 0)
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(14)
    normal_style.font.color.rgb = COLOR_BLACK

    # XML Helper Utilities
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def prevent_row_split(row):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    def set_table_borders(table, color="888888", sz="4", val="single"):
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

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.5, bold=False, italic=False, size_pt=14):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(size_pt)
            r.bold = bold
            r.italic = italic
            r.font.color.rgb = COLOR_BLACK
        return p

    def add_heading_chapter(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title_text.upper())
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.bold = True
        r.font.color.rgb = COLOR_BLACK
        return p

    def add_heading_sec(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.bold = True
        r.font.color.rgb = COLOR_BLACK
        return p

    def add_heading_subsec(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.bold = True
        r.italic = True
        r.font.color.rgb = COLOR_BLACK
        return p

    def add_fig_image(img_path, caption, width=Inches(5.5)):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            r_img = p_img.add_run()
            r_img.add_picture(img_path, width=width)

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(12)
            r_cap.bold = True
            r_cap.font.color.rgb = COLOR_BLACK

    def add_equation_block(eq_image_path, eq_num_str, title_str, explanation_text=""):
        if os.path.exists(eq_image_path):
            p_eq = doc.add_paragraph()
            p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_eq.paragraph_format.space_before = Pt(8)
            p_eq.paragraph_format.space_after = Pt(2)
            p_eq.paragraph_format.keep_with_next = True
            r_img = p_eq.add_run()
            r_img.add_picture(eq_image_path, width=Inches(4.6))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(1)
            p_cap.paragraph_format.space_after = Pt(4)
            p_cap.paragraph_format.keep_with_next = True
            r_cap = p_cap.add_run(f"Equation ({eq_num_str}): {title_str}")
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(11.5)
            r_cap.bold = True
            r_cap.font.color.rgb = COLOR_BLACK

        if explanation_text:
            add_p(explanation_text, space_before=2, space_after=8)

    def add_page_break():
        doc.add_page_break()

    # =========================================================================
    # 1. COVER / TITLE PAGE
    # =========================================================================
    add_p("QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)", 
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=18, space_after=18, bold=True, size_pt=15)
    
    add_p("A PROJECT REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6, bold=True, size_pt=14)
    add_p("U23ITP401 – MINI PROJECT", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=16, bold=True, size_pt=14)
    add_p("Submitted by", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=8, italic=True, size_pt=14)

    # Student Table
    t_stud = doc.add_table(rows=3, cols=2)
    t_stud.alignment = WD_TABLE_ALIGNMENT.CENTER
    students = [
        ("SABARI KARTHICK A", "(61782323110093)"),
        ("SIVANARASIMMAN S", "(61782323110103)"),
        ("SUJEETH Y R", "(617823231100107)")
    ]
    for row_idx, (name, regno) in enumerate(students):
        row = t_stud.rows[row_idx]
        prevent_row_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(3.0)
        c1.width = Inches(2.2)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(name)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(14)
        r0.bold = True

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(regno)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(14)
        r1.bold = True

    add_p("in partial fulfillment for the award of the degree", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=2, size_pt=14)
    add_p("of", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, size_pt=14)
    add_p("BACHELOR OF TECHNOLOGY", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, bold=True, size_pt=14)
    add_p("in", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, size_pt=14)
    add_p("INFORMATION TECHNOLOGY", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=12, bold=True, size_pt=14)

    # Logos on Title Page
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(6)
    p_logo.paragraph_format.space_after = Pt(6)
    if os.path.exists('extracted_template_logos/image1.jpeg') and os.path.exists('extracted_template_logos/image2.jpeg'):
        r_l1 = p_logo.add_run()
        r_l1.add_picture('extracted_template_logos/image1.jpeg', height=Inches(0.95))
        r_sp = p_logo.add_run("       ")
        r_sp.font.name = 'Times New Roman'
        r_l2 = p_logo.add_run()
        r_l2.add_picture('extracted_template_logos/image2.jpeg', height=Inches(0.95))

    add_p("SONA COLLEGE OF TECHNOLOGY (AUTONOMOUS), SALEM – 636005", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=2, bold=True, size_pt=13)
    add_p("ANNA UNIVERSITY: CHENNAI 600 025", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, bold=True, size_pt=13)
    add_p("OCTOBER 2026", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=0, bold=True, size_pt=13)

    add_page_break()

    # =========================================================================
    # 2. BONAFIDE CERTIFICATE
    # =========================================================================
    add_p("SONA COLLEGE OF TECHNOLOGY (AUTONOMOUS)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2, bold=True, size_pt=14)
    add_p("ANNA UNIVERSITY: CHENNAI – 600 025", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=18, bold=True, size_pt=14)
    add_p("BONAFIDE CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=18, bold=True, size_pt=15)

    cert_text = (
        "Certified that this project titled “QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR "
        "PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)” is the bonafide "
        "work of “SABARI KARTHICK A (61782323110093), SIVANARASIMMAN S (61782323110103), SUJEETH Y R (617823231100107)” "
        "who carried out the project work Course Code & Course Name U23ITP401 – MINI PROJECT under my supervision."
    )
    add_p(cert_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=12, space_after=36, line_spacing=2.0, size_pt=14)

    # Signatures Table (Supervisor and HOD)
    t_sig = doc.add_table(rows=6, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_info = [
        ("Signature of the Supervisor", "Head of the Department"),
        ("Mrs. J. Deepika", "Dr. J. Akilandeswari"),
        ("SUPERVISOR", "HEAD OF THE DEPARTMENT"),
        ("Assistant Professor", "Professor & Head"),
        ("Department of Information Technology", "Department of Information Technology"),
        ("Sona College of Technology,\nSalem – 636005", "Sona College of Technology,\nSalem – 636005")
    ]
    for row_idx, (col0, col1) in enumerate(sig_info):
        row = t_sig.rows[row_idx]
        prevent_row_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(3.0)
        c1.width = Inches(3.0)
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        
        r0 = p0.add_run(col0)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(13)
        r0.bold = (row_idx in [0, 1, 2])
        
        r1 = p1.add_run(col1)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(13)
        r1.bold = (row_idx in [0, 1, 2])

    add_p("Submitted for the Project Viva-Voce Examination held on ___________________", 
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=36, space_after=30, size_pt=13)

    t_exam = doc.add_table(rows=1, cols=2)
    t_exam.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0, c1 = t_exam.rows[0].cells[0], t_exam.rows[0].cells[1]
    c0.width = Inches(3.0)
    c1.width = Inches(3.0)
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r0 = p0.add_run("INTERNAL EXAMINER")
    r0.font.name = 'Times New Roman'
    r0.font.size = Pt(13)
    r0.bold = True
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r1 = p1.add_run("EXTERNAL EXAMINER")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(13)
    r1.bold = True

    add_page_break()

    # =========================================================================
    # 3. DECLARATION FORM
    # =========================================================================
    add_p("Sona College of Technology", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=2, bold=True, size_pt=14)
    add_p("Department of Information Technology", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6, bold=True, size_pt=14)
    add_p("U23ITP401 - MINI PROJECT - DECLARATION FORM", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14, bold=True, size_pt=14)
    add_p("Declaration by the Student(s)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=14, bold=True, size_pt=14)

    decl_p1 = (
        "We hereby declare that the project titled “QR-BASED CATTLE MANAGEMENT SYSTEM: A PLATFORM FOR "
        "PERSONALIZED HEALTH MONITORING USING COMPOSITE HEALTH DEVIATION INDEX (CHDI)” is an original "
        "work carried out by me/us under the guidance of Mrs. J. Deepika, Assistant Professor, Department of "
        "Information Technology, Sona College of Technology, Salem. This project has not been submitted elsewhere "
        "for the award of any degree."
    )
    add_p(decl_p1, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=10, line_spacing=1.5, size_pt=14)

    decl_p2 = (
        "We also affirm that all the data and information used in this project are genuine and properly acknowledged. "
        "This project work is carried out with reference to the United Nations Sustainable Development Goal: "
        "SDG 2 – Zero Hunger."
    )
    add_p(decl_p2, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=18, line_spacing=1.5, size_pt=14)

    # Student Declaration Table
    t_decl = doc.add_table(rows=4, cols=4)
    t_decl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_decl)
    decl_headers = ["S.No", "Register Number", "Name", "Signature"]
    decl_rows_data = [
        ["1.", "61782323110093", "SABARI KARTHICK A", ""],
        ["2.", "61782323110103", "SIVANARASIMMAN S", ""],
        ["3.", "617823231100107", "SUJEETH Y R", ""]
    ]
    for col_idx, h_text in enumerate(decl_headers):
        cell = t_decl.rows[0].cells[col_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True
    
    for r_idx, row_data in enumerate(decl_rows_data, start=1):
        row = t_decl.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 1] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)

    add_p("Date: 15.10.2026", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=24, space_after=2, size_pt=13)
    add_p("Place: Sona College of Technology", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=12, size_pt=13)

    add_page_break()

    # =========================================================================
    # 4. ACKNOWLEDGMENT
    # =========================================================================
    add_heading_chapter("ACKNOWLEDGMENT")
    
    ack_1 = (
        "First and foremost, we thank the Almighty for His blessings, guidance, and the inner peace that gave us the "
        "strength and determination to complete this project. We also express our heartfelt gratitude to our parents "
        "for their unconditional love, constant support, and encouragement throughout our journey."
    )
    add_p(ack_1, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=10, space_after=10, line_spacing=1.5, size_pt=14)

    ack_2 = (
        "We express our sincere gratitude to our beloved Chairman, Sri. C. Valliappa, and our dynamic Vice-Chairmen, "
        "Sri. Chocko Valliappa and Sri. Thyagu Valliappa, for providing us with the necessary facilities and support "
        "to successfully complete this project."
    )
    add_p(ack_2, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=10, line_spacing=1.5, size_pt=14)

    ack_3 = (
        "We are immensely grateful to our Principal, Dr. S. R. R. Senthilkumar, for his constant inspiration and "
        "encouragement throughout our academic journey."
    )
    add_p(ack_3, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=10, line_spacing=1.5, size_pt=14)

    ack_4 = (
        "We extend our sincere thanks to Dr. J. Akilandeswari, Professor and Head of the Department of Information "
        "Technology, for providing the necessary laboratory facilities and academic support to carry out this project successfully."
    )
    add_p(ack_4, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=10, line_spacing=1.5, size_pt=14)

    ack_5 = (
        "We express our heartfelt gratitude to our Project Coordinator, Dr. J. Jeba Emilyn, Associate Professor, "
        "Department of Information Technology, for her continuous guidance, valuable suggestions, and constant "
        "encouragement throughout the project."
    )
    add_p(ack_5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=10, line_spacing=1.5, size_pt=14)

    ack_6 = (
        "We are also deeply grateful to Mrs. J. Deepika, Assistant Professor, Department of Information Technology, "
        "for her invaluable mentorship, insightful guidance, and unwavering support throughout the project. Her expertise "
        "and constructive suggestions have played a significant role in shaping our work and helping us achieve our objectives."
    )
    add_p(ack_6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=10, line_spacing=1.5, size_pt=14)

    ack_7 = (
        "Finally, we take this opportunity to express our sincere appreciation to all the faculty members, non-teaching "
        "staff, and friends who supported us, either directly or indirectly, in completing this project successfully. "
        "Their cooperation and encouragement have contributed greatly to the successful completion of our work."
    )
    add_p(ack_7, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=18, line_spacing=1.5, size_pt=14)

    add_page_break()

    # =========================================================================
    # 5. ABSTRACT
    # =========================================================================
    add_heading_chapter("ABSTRACT")

    abstract_content = (
        "In smallholder dairy farming, precision livestock health monitoring is often constrained by the high cost "
        "of specialized RFID readers, proprietary wearable sensors, and rigid population-wide thresholds. These conventional "
        "approaches frequently trigger false alarms by failing to account for individual cattle physiological variations and sparse field data.\n\n"
        "To address this challenge, this project presents a QR-Based Cattle Management System, an infrastructure-light, "
        "cloud-based platform for personalized dairy health monitoring using the Composite Health Deviation Index (CHDI). "
        "The system eliminates the need for expensive hardware by utilizing weather-resistant QR passports accessible via "
        "standard smartphones and secured with Role-Based Access Control (RBAC). At its computational core, the platform integrates "
        "a Three-Stage Adaptive CHDI engine that establishes an individual 14-day baseline, evaluates multivariate Mahalanobis "
        "distance deviations, computes 7-day temporal trend slopes, provides explainable feature attributions, and applies an "
        "uncertainty gate to suppress false alarms during early enrollment.\n\n"
        "The application is implemented as a full-stack solution using Next.js 16 (App Router, Server Actions), PostgreSQL "
        "with Prisma ORM, a FastAPI Python analytical microservice, and a Progressive Web App (PWA) supporting offline synchronization. "
        "System evaluation demonstrates 90.48% sensitivity, 96.27% specificity, 62.30% precision, and an F1-score of 73.79% in detecting "
        "sub-clinical health anomalies, delivering an advance clinical lead time of 2.4 days prior to observable symptoms."
    )
    add_p(abstract_content, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=12, space_after=18, line_spacing=2.0, size_pt=14)

    add_page_break()

    # =========================================================================
    # 6. TABLE OF CONTENTS
    # =========================================================================
    add_heading_chapter("TABLE OF CONTENTS")

    toc_items = [
        ("ABSTRACT", "iv"),
        ("LIST OF FIGURES", "vii"),
        ("LIST OF TABLES", "viii"),
        ("LIST OF ABBREVIATIONS", "ix"),
        ("1. INTRODUCTION", "1"),
        ("    1.1 Background of the Project", "1"),
        ("    1.2 Problem Statement", "2"),
        ("    1.3 Motivation", "3"),
        ("    1.4 Objectives", "4"),
        ("    1.5 Scope of the Project", "5"),
        ("2. LITERATURE REVIEW", "6"),
        ("    2.1 Introduction", "6"),
        ("    2.2 Review of Related Studies", "7"),
        ("    2.3 Techniques and Technologies Used in Existing Systems", "10"),
        ("    2.4 Research Gap", "11"),
        ("    2.5 Summary", "12"),
        ("3. CHAPTER 1 – NEED FOR PROPOSED TECHNIQUE", "13"),
        ("    3.1 Existing Techniques", "13"),
        ("    3.2 Limitations of Existing Techniques", "14"),
        ("    3.3 Proposed Technique", "15"),
        ("    3.4 Objectives of the Proposed Technique", "16"),
        ("    3.5 Advantages of the Proposed Technique", "17"),
        ("4. CHAPTER 2 – DESIGN OF PROPOSED SYSTEM AND ITS IMPLEMENTATION", "18"),
        ("    4.1 Introduction", "18"),
        ("    4.2 System Requirements", "18"),
        ("        4.2.1 Hardware Requirements", "18"),
        ("        4.2.2 Software Requirements", "19"),
        ("    4.3 System Architecture", "20"),
        ("    4.4 System Components/Modules", "21"),
        ("        4.4.1 Module 1: Authentication & Role-Based Access Control (RBAC)", "21"),
        ("        4.4.2 Module 2: Animal Husbandry & QR Identification Module", "22"),
        ("        4.4.3 Module 3: Longitudinal Multi-Signal Health Logging Module", "22"),
        ("        4.4.4 Module 4: Medical, Vaccination & Deworming Management Module", "23"),
        ("        4.4.5 Module 5: Adaptive Baseline & CHDI Computation Module", "23"),
        ("        4.4.6 Module 6: Temporal Trend & Slope Regression Module", "24"),
        ("        4.4.7 Module 7: Explainability & Permutation Attribution Module", "24"),
        ("        4.4.8 Module 8: Automated VetCase Dispatch & Feedback Learning Module", "24"),
        ("    4.5 Proposed Methodology", "25"),
        ("    4.6 System Workflow", "26"),
        ("    4.7 Algorithms/Techniques Used", "27"),
        ("    4.8 Dataset/Data Collection", "29"),
        ("    4.9 Data Preprocessing", "30"),
        ("    4.10 Model/System Development", "31"),
        ("    4.11 System Design Diagrams", "32"),
        ("    4.12 Implementation", "34"),
        ("    4.13 Coding/Program Implementation", "35"),
        ("    4.14 User Interface / Application Screens", "42"),
        ("    4.15 Chapter Summary", "46"),
        ("5. CHAPTER 3 – RESULTS AND DISCUSSION", "47"),
        ("    5.1 Introduction", "47"),
        ("    5.2 Experimental Setup", "47"),
        ("    5.3 Evaluation Metrics", "48"),
        ("    5.4 Experimental Results", "49"),
        ("    5.5 Comparison with Existing Techniques", "52"),
        ("    5.6 Discussion of Results", "54"),
        ("    5.7 Chapter Summary", "55"),
        ("6. CHAPTER 4 – CONCLUSION AND FUTURE SCOPE", "56"),
        ("    6.1 Summary of the Project", "56"),
        ("    6.2 Conclusion", "57"),
        ("    6.3 Future Scope", "58"),
        ("SDG GOALS", "59"),
        ("PUBLICATIONS", "61"),
        ("REFERENCES", "62")
    ]

    t_toc = doc.add_table(rows=len(toc_items), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, (title, pg) in enumerate(toc_items):
        row = t_toc.rows[r_idx]
        prevent_row_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.3)
        c1.width = Inches(0.9)
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)

        is_major = not title.startswith("    ") and not title.startswith("        ")
        r0 = p0.add_run(title)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(13)
        r0.bold = is_major

        r1 = p1.add_run(pg)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(13)
        r1.bold = is_major

    add_page_break()

    # =========================================================================
    # 7. LIST OF FIGURES
    # =========================================================================
    add_heading_chapter("LIST OF FIGURES")

    figures_list = [
        ("Figure 4.1", "Comprehensive System Architecture of SmartCattle Multi-Tier Framework", "20"),
        ("Figure 4.2", "End-to-End Operational and Analytical Flow of Sensor Ingestion and Clinical Triage", "26"),
        ("Figure 4.3", "Composite Health Deviation Index (CHDI) Dynamic Baseline and Anomaly Bounds", "28"),
        ("Figure 4.4", "Veterinary Active Learning and Closed-Loop Feedback Pipeline", "33"),
        ("Figure 4.5", "Spatial Heatmap and Regional Outbreak Detection Engine", "34"),
        ("Figure 4.6", "Farmer Multi-Cattle Monitoring Dashboard UI", "42"),
        ("Figure 4.7", "Decentralized Cattle QR Scanner and Digital Identity Modal UI", "43"),
        ("Figure 4.8", "Longitudinal Health Records, Temperature Trends, and CHDI History UI", "44"),
        ("Figure 4.9", "Veterinary Clinical Triage Interface with Active Learning Verification UI", "45"),
        ("Figure 4.10", "Cattle Herd Roster and Vital Status Overview UI", "46"),
        ("Figure 5.1", "CHDI Health Status Distribution Across 674 Benchmark Observation Records", "50"),
        ("Figure 5.2", "Longitudinal 30-Day CHDI Trajectory for Cow #C-08 Showing Early Subclinical Watch Alert", "51"),
        ("Figure 5.3", "Permutation Feature Importance Attribution Ranking Driving Anomaly Scores for Cow #C-08", "52")
    ]

    t_lof = doc.add_table(rows=len(figures_list) + 1, cols=3)
    t_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_lof)
    lof_headers = ["Figure No.", "Figure Title", "Page No."]
    for c_idx, h in enumerate(lof_headers):
        cell = t_lof.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    col_widths = [Inches(1.2), Inches(4.2), Inches(0.8)]
    for r_idx, (fno, ftitle, fpg) in enumerate(figures_list, start=1):
        row = t_lof.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate([fno, ftitle, fpg]):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)

    add_page_break()

    # =========================================================================
    # 8. LIST OF TABLES
    # =========================================================================
    add_heading_chapter("LIST OF TABLES")

    tables_list = [
        ("Table 4.1", "Hardware Requirements and Node Specifications", "18"),
        ("Table 4.2", "Software Stack, Frameworks, and Cloud Dependencies", "19"),
        ("Table 4.3", "CHDI Severity Bands, Distance Thresholds, and Clinical Protocols", "28"),
        ("Table 4.4", "Multi-Signal Telemetry Features and Normal Physiological Baselines", "29"),
        ("Table 4.5", "GitHub Repository Directory and File Organization", "36"),
        ("Table 5.1", "Anomaly Detection Performance Metrics Across Classification Thresholds", "50"),
        ("Table 5.2", "Comparative Benchmark against Standard Fixed-Threshold and Univariate Systems", "53"),
        ("Table 5.3", "Ablation Study of CHDI Mathematical Components", "54")
    ]

    t_lot = doc.add_table(rows=len(tables_list) + 1, cols=3)
    t_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_lot)
    lot_headers = ["Table No.", "Table Title", "Page No."]
    for c_idx, h in enumerate(lot_headers):
        cell = t_lot.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    for r_idx, (tno, ttitle, tpg) in enumerate(tables_list, start=1):
        row = t_lot.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate([tno, ttitle, tpg]):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)

    add_page_break()

    # =========================================================================
    # 9. LIST OF ABBREVIATIONS
    # =========================================================================
    add_heading_chapter("LIST OF ABBREVIATIONS")

    abbr_list = [
        ("AI", "Artificial Intelligence"),
        ("API", "Application Programming Interface"),
        ("BLE", "Bluetooth Low Energy"),
        ("BRD", "Bovine Respiratory Disease"),
        ("CHDI", "Composite Health Deviation Index"),
        ("CNN", "Convolutional Neural Network"),
        ("CSS", "Cascading Style Sheets"),
        ("DFD", "Data Flow Diagram"),
        ("ER", "Entity Relationship"),
        ("EWMA", "Exponentially Weighted Moving Average"),
        ("F1", "Harmonic Mean of Precision and Recall"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("HTTPS", "Hypertext Transfer Protocol Secure"),
        ("IMU", "Inertial Measurement Unit"),
        ("IoT", "Internet of Things"),
        ("JSON", "JavaScript Object Notation"),
        ("JWT", "JSON Web Token"),
        ("LF", "Low Frequency (RFID)"),
        ("ML", "Machine Learning"),
        ("MQTT", "Message Queuing Telemetry Transport"),
        ("OCR", "Optical Character Recognition"),
        ("OLS", "Ordinary Least Squares"),
        ("ORM", "Object-Relational Mapping"),
        ("PLF", "Precision Livestock Farming"),
        ("PWA", "Progressive Web Application"),
        ("QR", "Quick Response Code"),
        ("RBAC", "Role-Based Access Control"),
        ("REST", "Representational State Transfer"),
        ("RFID", "Radio-Frequency Identification"),
        ("SDG", "Sustainable Development Goals"),
        ("SHAP", "SHapley Additive exPlanations"),
        ("THI", "Temperature-Humidity Index"),
        ("UHF", "Ultra-High Frequency (RFID)"),
        ("UI", "User Interface"),
        ("UN", "United Nations"),
        ("URL", "Uniform Resource Locator"),
        ("UUID", "Universally Unique Identifier"),
        ("W3C", "World Wide Web Consortium"),
        ("WSN", "Wireless Sensor Network")
    ]

    t_abbr = doc.add_table(rows=len(abbr_list) + 1, cols=2)
    t_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_abbr)
    abbr_headers = ["Abbreviation", "Full Expansion"]
    for c_idx, h in enumerate(abbr_headers):
        cell = t_abbr.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    for r_idx, (short_txt, full_txt) in enumerate(abbr_list, start=1):
        row = t_abbr.rows[r_idx]
        prevent_row_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(1.8)
        c1.width = Inches(4.4)
        set_cell_margins(c0, top=70, bottom=70, left=80, right=80)
        set_cell_margins(c1, top=70, bottom=70, left=80, right=80)
        
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(short_txt)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(13)
        r0.bold = True

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p1.add_run(full_txt)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(13)

    add_page_break()

    # =========================================================================
    # 10. CHAPTER 1: 1. INTRODUCTION
    # =========================================================================
    add_heading_chapter("1. INTRODUCTION")

    add_heading_sec("1.1 Background of the Project")
    p_intro1 = (
        "In global livestock agriculture and rural economies, smallholder dairy farming represents a vital socio-economic "
        "backbone for over 150 million rural farming households. In India alone, livestock husbandry contributes significantly "
        "to agricultural GDP, providing daily nutritional security and direct income. Despite the vital economic role of dairy herds, "
        "smallholder pastoralists face persistent productivity challenges caused by silent sub-clinical disease onset, delayed "
        "veterinary diagnosis, and the prohibitive expense of commercial Precision Livestock Farming (PLF) systems. In particular, "
        "sub-clinical bovine mastitis, bovine respiratory disease (BRD), and metabolic ketosis lead to severe drops in milk production "
        "(25%–40% per lactation cycle), substantial veterinary bills, and premature culling of high-value cows (Bowling et al. 2008; "
        "Kamphuis et al. 2010)."
    )
    add_p(p_intro1)

    p_intro2 = (
        "While modern electronic identification and wearable biosensors have been investigated extensively, commercial systems "
        "depend on costly proprietary RFID tags, specialized reading wands, and expensive wearable sensor collars. For smallholder "
        "farmers owning fewer than 10 animals, investing thousands of dollars in proprietary hardware is economically unviable. "
        "Furthermore, existing platforms rely on rigid, population-wide fixed thresholds that ignore natural individual variations, "
        "triggering high rates of false-positive alarms that quickly erode farmer trust (Pereira et al. 2024; Kaur & Virk 2024). "
        "There is an urgent necessity for an infrastructure-light, sensor-optional, and mathematically adaptive health monitoring "
        "solution designed for commodity mobile devices."
    )
    add_p(p_intro2)

    add_heading_sec("1.2 Problem Statement")
    p_prob = (
        "Smallholder dairy farmers and rural veterinary officers lack an accessible, cost-effective, and noise-resilient digital "
        "health monitoring infrastructure. Current state-of-the-art precision livestock farming systems suffer from three fundamental "
        "operational and economic barriers:\n"
        "1. High Infrastructure and Hardware Cost: Existing cattle tracking systems require expensive passive Low-Frequency (LF) or "
        "Ultra-High-Frequency (UHF) RFID ear tags and dedicated handheld or portal reader antennas, making deployment economically "
        "infeasible for smallholders without automated parlors.\n"
        "2. Fixed Static Thresholds and Spurious False Alarms: Standard monitoring platforms evaluate vital signs against static global "
        "limits. Because baseline body weight, milk yield, feed intake, and temperature naturally vary across individual cows, breeds, "
        "and lactation stages, static thresholds generate excessive false alarms.\n"
        "3. Inadequate Handling of Sparse Data and Environmental Uncertainty: Rural farm data collection is frequently sparse or intermittent. "
        "Existing systems lack uncertainty-aware abstention mechanisms to prevent false alarms on newly registered cows with insufficient "
        "historical baseline depth."
    )
    add_p(p_prob)

    add_heading_sec("1.3 Motivation")
    p_mot = (
        "The primary motivation of this project is to democratize precision livestock health intelligence for smallholder dairy "
        "farmers by developing an infrastructure-light, cloud-native software platform. By replacing expensive proprietary hardware "
        "with weather-resistant, smartphone-scannable QR digital passports and substituting rigid thresholds with a personalized, "
        "Three-Stage Composite Health Deviation Index (CHDI) engine, SmartCattle provides early clinical warning, explainable diagnostic "
        "attributions, and automated veterinary triage at zero specialized hardware cost (Subach & Shmeleva 2024; Curti et al. 2024)."
    )
    add_p(p_mot)

    add_heading_sec("1.4 Objectives")
    p_obj = (
        "The major objectives of the SmartCattle project are:\n"
        "1. Infrastructure-Independent Livestock Identification: To implement decentralized, tamper-evident dynamic QR passports "
        "that link physical animals to secure cloud health records using commodity smartphone cameras without proprietary RFID readers.\n"
        "2. Personalized Longitudinal Baseline Modeling: To formulate and implement the Three-Stage Composite Health Deviation Index (CHDI) "
        "engine that establishes an individual 14-day rolling baseline and evaluates multivariate Mahalanobis distance deviations across "
        "empirical signal covariances.\n"
        "3. Explainability and Uncertainty Estimation: To incorporate ordinary least-squares temporal slope regression (7-day trend), "
        "permutation feature importance decompositions for transparent veterinary insights, and a data-sufficiency gate (N_min = 7) "
        "that safely suppresses false alarms during early enrollment.\n"
        "4. Automated Clinical Triage Pipeline: To build a closed-loop veterinary case dispatch workflow that prioritizes critical cases, "
        "tracks drug withdrawal periods to prevent antibiotic residue in milk, and captures verified diagnostic labels for continuous model refinement.\n"
        "5. Full-Stack Web Application Prototype: To engineer a decoupled, production-grade web system utilizing Next.js 16 (App Router, "
        "Server Actions), Prisma ORM, PostgreSQL, FastAPI Python microservice, and a Progressive Web App (PWA) supporting offline synchronization."
    )
    add_p(p_obj)

    add_heading_sec("1.5 Scope of the Project")
    p_scope = (
        "The project encompasses the end-to-end design, mathematical formulation, software engineering, and experimental evaluation "
        "of the SmartCattle platform. The software covers decentralized QR identity resolution, multi-signal longitudinal health logging "
        "(daily body weight, feed intake, milk production, core temperature, and rumination/activity), CHDI mathematical anomaly detection, "
        "temporal slope analysis, clinical triage management, and responsive role-based web dashboards. The platform is validated against "
        "a real-world multimodal benchmark cohort of 16 Holstein-Friesian cows comprising 674 longitudinal observation records, with the "
        "architecture ready for direct integration with physical IoT gateways and sensor streams."
    )
    add_p(p_scope)

    add_page_break()

    # =========================================================================
    # 11. CHAPTER 2: 2. LITERATURE REVIEW
    # =========================================================================
    add_heading_chapter("2. LITERATURE REVIEW")

    add_heading_sec("2.1 Introduction")
    p_lit_intro = (
        "Livestock identification, biosecurity tracking, and precision health monitoring have evolved over the past two decades. "
        "This chapter surveys the foundational literature across four key domains: electronic livestock traceability, wearable IoT "
        "physiological sensing, optical and computer vision biometrics, and digital veterinary management systems, establishing the "
        "research gaps that motivate the SmartCattle system architecture."
    )
    add_p(p_lit_intro)

    add_heading_sec("2.2 Review of Related Studies")
    lit_reviews = [
        "Bowling et al. (2008) presented an international review of national livestock traceability systems across the EU, Australia, and Japan. "
        "Their study demonstrated that lifetime traceability databases are essential for controlling epidemic disease outbreaks, but noted that "
        "passive RFID transponders incur high infrastructure expenses, reader hardware dependencies, and ear-tag retention loss.",

        "Pereira et al. (2024) conducted a comprehensive literature and patent analysis on passive UHF RFID animal tracking. While UHF RFID offers "
        "non-line-of-sight reading ranges in industrial feedlots, the substantial capital expenditure of fixed reader portals and specialized hand scanners "
        "makes the technology inaccessible to smallholder farmers with small herds.",

        "Bumbálek et al. (2024) performed a comparative study using YOLOv8 for cattle body-texture biometric identification, numerical ear-tag OCR, "
        "and optical QR collars. Their results showed that QR tags offer instant identification without requiring complex deep convolutional neural "
        "network retraining for each new animal, although optical approaches require weather-resistant tags and manual fallback workflows.",

        "Subach & Shmeleva (2024) investigated the adoption of digital technologies in dairy farming, emphasizing that software simplicity, "
        "low capital requirements, and mobile accessibility are the primary determinants of technology adoption among small-scale agrarian producers.",

        "Kaur & Virk (2024) developed an IoT-based smart neck collar integrating 3-axis accelerometers, digital thermometers, and pulse sensors for "
        "real-time disease detection in 150 dairy cows. Their Random Forest and Decision Tree models achieved 92% and 91% accuracy for mastitis and "
        "BRD, but they noted major operational limitations including high sensor replacement costs, battery degradation, and physical damage from social grooming.",

        "Curti et al. (2024) evaluated machine learning approaches for individual livestock health records, demonstrating that multi-parametric "
        "covariance modeling provides superior anomaly sensitivity over univariate threshold rules.",

        "Aquilani et al. (2022) surveyed precision livestock farming technologies for pasture-based ruminants, reviewing walk-over weigh scales, "
        "GPS collars, and thermal imaging. They emphasized that multi-signal telemetry is essential for accurate health evaluation, but noted that "
        "high maintenance costs remain a persistent barrier.",

        "Ahmad & Salamat (2023) developed a web-based veterinary clinic management system, demonstrating the necessity of structured digital "
        "medical histories, vaccination scheduling, and role-based access control for clinical workflows.",

        "Barriuso et al. (2018) presented a multi-agent Wireless Sensor Network (WSN) using MQTT messaging for pasture cattle monitoring, validating "
        "the effectiveness of asynchronous message queuing for agricultural sensor data dispatch.",

        "Hostens et al. (2024) published a comprehensive longitudinal multimodal dataset on Zenodo covering daily milk yield, feeding intake, "
        "and body weight metrics for dairy cows, establishing standardized benchmark reference distributions for precision health algorithms.",

        "Jensen & Bennedsen (2023) published high-resolution accelerometer time-series telemetry in lactating cows, demonstrating that rumination "
        "and movement drop significantly 48–72 hours prior to acute clinical symptoms of infectious bovine mastitis.",

        "Kamphuis et al. (2010) analyzed automated mastitis detection using decision trees and proved that combining electrical conductivity with "
        "historical longitudinal deviation scores substantially reduces false alarm rates compared to static population thresholds.",

        "Kim et al. (2024) curated the 'MmCows' multimodal dairy cattle dataset, demonstrating that cross-variable physiological coupling enables "
        "early sub-clinical anomaly detection in commercial herds.",

        "Ankitha, Manjaiah & Kartik (2024) evaluated udder surface temperature variations in clinical mastitis, showing that localized inflammatory "
        "fever precedes systemic thermal spikes by 2 to 3 days."
    ]
    for r_item in lit_reviews:
        add_p(r_item, space_before=4, space_after=6)

    add_heading_sec("2.3 Techniques and Technologies Used in Existing Systems")
    p_tech_exist = (
        "Existing precision livestock management systems predominantly employ three technological categories:\n"
        "1. Passive LF/UHF RFID Identification: Electronic ear tags requiring specialized handheld readers or portal antennas costing thousands of dollars.\n"
        "2. Proprietary Sensor Collars & Boluses: Battery-powered edge IoT devices transmitting raw accelerometer and thermistor readings via proprietary base stations.\n"
        "3. Static Rule-Based Threshold Software: Monolithic farm software evaluating single vitals against fixed population thresholds (e.g., temperature > 39.5°C)."
    )
    add_p(p_tech_exist)

    add_heading_sec("2.4 Research Gap")
    p_gap = (
        "Despite extensive research, four critical gaps remain unaddressed in precision dairy management:\n"
        "1. Heavy Infrastructure Dependency: Existing systems require specialized electronic RFID readers or mandatory wearable hardware, leaving smallholders excluded.\n"
        "2. Rigid Static Thresholds: Current commercial systems ignore individual baseline variance, causing high false alarm rates during heat waves or normal diurnal fluctuations.\n"
        "3. Lack of Explainability & Uncertainty Gates: Existing algorithms output black-box alerts without explaining which physiological signals caused the alarm, and lack safeguards to prevent false alarms on newly registered cows with sparse history.\n"
        "4. Absence of Closed-Loop Veterinary Feedback: No existing platform connects automated anomaly detection with clinical veterinary triage and prescription drug withdrawal tracking."
    )
    add_p(p_gap)

    add_heading_sec("2.5 Summary")
    p_lit_sum = (
        "This chapter reviewed electronic traceability, wearable biosensing, optical QR recognition, and digital veterinary management. "
        "The identified limitations in infrastructure cost, rigid thresholding, lack of explainability, and absence of closed-loop triage "
        "directly justify the infrastructure-light, Three-Stage CHDI architecture implemented in SmartCattle."
    )
    add_p(p_lit_sum)

    add_page_break()

    # =========================================================================
    # 12. CHAPTER 3: 3. CHAPTER 1 – NEED FOR PROPOSED TECHNIQUE
    # =========================================================================
    add_heading_chapter("3. CHAPTER 1 – NEED FOR PROPOSED TECHNIQUE")

    add_heading_sec("3.1 Existing Techniques")
    p_exist_tech = (
        "Conventional livestock health management in smallholder dairy farming relies primarily on visual manual observation by farmers "
        "(e.g., observing dull eyes, reduced cud chewing, gait changes, or swollen udders) supplemented by periodic visits by veterinary "
        "officers. In larger commercial herds, automated monitoring uses passive RFID tags, walk-through antenna gates, and proprietary "
        "wearable collars operating on fixed numerical thresholds."
    )
    add_p(p_exist_tech)

    add_heading_sec("3.2 Limitations of Existing Techniques")
    p_exist_lim = (
        "The limitations of existing techniques are profound and directly harm smallholder productivity:\n"
        "1. Delayed Detection: Visual symptoms of sub-clinical mastitis and ketosis appear only after substantial tissue inflammation or "
        "severe milk loss has occurred, rendering treatments less effective.\n"
        "2. Prohibitive Capital Cost: Commercial RFID and IoT sensor collar systems require expensive initial investments, recurring battery "
        "replacements, and vendor lock-in.\n"
        "3. High Spurious Alarm Rates: Fixed population thresholds trigger excessive false alarms during hot afternoons or seasonal changes, "
        "causing alarm fatigue.\n"
        "4. Fragmented Paper Records: Veterinary histories, vaccination dates, and drug withdrawal periods are recorded on loose paper slips, "
        "risking antibiotic residue entering commercial milk supplies."
    )
    add_p(p_exist_lim)

    add_heading_sec("3.3 Proposed Technique")
    p_prop_tech = (
        "The proposed technique introduces 'SmartCattle' (QR-Cattle-Health)—an infrastructure-light, sensor-optional, cloud-native dairy "
        "health management system. The platform replaces expensive hardware with weather-resistant dynamic QR digital passports scannable "
        "by any standard smartphone camera. Daily multi-signal health logs (body weight, feed intake, milk yield, temperature, and activity) "
        "are evaluated by an adaptive Three-Stage Composite Health Deviation Index (CHDI) engine. CHDI tracks personalized 14-day rolling "
        "baselines, calculates multivariate Mahalanobis distance anomalies across empirical signal covariances, evaluates 7-day temporal slope "
        "trajectories, decomposes feature attributions, and enforces an uncertainty gate (N_min = 7) to safely suppress false alarms."
    )
    add_p(p_prop_tech)

    add_heading_sec("3.4 Objectives of the Proposed Technique")
    p_prop_obj = (
        "The key objectives of the proposed technique are:\n"
        "1. Infrastructure-Light Traceability: Zero dependency on specialized RFID wands; 100% commodity smartphone QR scanning.\n"
        "2. Adaptive Anomaly Scoring: Compute continuous CHDI scores (0–100) normalized to individual cow baselines.\n"
        "3. 2.4-Day Early Warning Lead Time: Detect pre-symptomatic physiological shifts days before visible clinical signs emerge.\n"
        "4. Dual-Tier Explainability: Deliver plain-language summaries for farmers and technical Z-score decompositions for veterinarians.\n"
        "5. Closed-Loop Clinical Triage: Automate priority VetCase dispatch, diagnosis confirmation, and drug withdrawal safety tracking."
    )
    add_p(p_prop_obj)

    add_heading_sec("3.5 Advantages of the Proposed Technique")
    p_prop_adv = (
        "The proposed technique offers distinct operational, clinical, and economic advantages:\n"
        "• Near-Zero Hardware Cost: Relies on printable QR tags and mobile web browsers already owned by farmers.\n"
        "• High Diagnostic Specificity: Mahalanobis multi-signal covariance modeling achieves 96.27% specificity, eliminating false alarms.\n"
        "• Milk Biosecurity: Integrated withdrawal tracking prevents antibiotic residue contamination in commercial dairy supplies.\n"
        "• Robust Offline Operation: PWA architecture with IndexedDB ensures seamless data recording in remote rural barns."
    )
    add_p(p_prop_adv)

    add_page_break()

    # =========================================================================
    # 13. CHAPTER 4: 4. CHAPTER 2 – DESIGN OF PROPOSED SYSTEM AND ITS IMPLEMENTATION
    # =========================================================================
    add_heading_chapter("4. CHAPTER 2 – DESIGN OF PROPOSED SYSTEM AND ITS IMPLEMENTATION")

    add_heading_sec("4.1 Introduction")
    p_des_intro = (
        "This chapter details the system architecture, mathematical formulations, hardware/software specifications, 8 core component "
        "modules, operational workflows, database schemas, and implementation details of the SmartCattle platform."
    )
    add_p(p_des_intro)

    add_heading_sec("4.2 System Requirements")
    
    add_heading_subsec("4.2.1 Hardware Requirements")
    p_hw_desc = (
        "The SmartCattle platform is specifically engineered to eliminate proprietary hardware requirements for end users. Table 4.1 "
        "specifies the commodity client hardware and cloud server infrastructure utilized by the system."
    )
    add_p(p_hw_desc)

    # Table 4.1
    t_hw = doc.add_table(rows=4, cols=3)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_hw)
    hw_headers = ["Hardware Component", "Specifications & Configuration", "Functional Role in SmartCattle"]
    for c_idx, h in enumerate(hw_headers):
        cell = t_hw.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    hw_data = [
        ["Client Smartphone / Tablet", "Any Android / iOS smartphone with standard camera and HTML5 browser", "Instant optical scanning of QR passports, daily multi-signal health logging, and PWA dashboard access."],
        ["Weather-Resistant QR Tags", "Laminated, UV-coated optical QR ear tag / neck strap tag (ISO/IEC 18004)", "Affordable, non-electronic physical identifier encoding unique decentralized token."],
        ["Cloud Backend Server", "Ubuntu Linux 22.04 LTS, 4 vCPUs, 16GB RAM, 100GB SSD Storage", "Hosts Next.js web application, FastAPI Python analytical microservice, and PostgreSQL database cluster."]
    ]
    for r_idx, row_vals in enumerate(hw_data, start=1):
        row = t_hw.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = Inches(1.8) if c_idx == 0 else (Inches(2.5) if c_idx == 1 else Inches(2.0))
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)

    add_p("Table 4.1: Hardware Requirements and Node Specifications", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12, bold=True, size_pt=12)

    add_heading_subsec("4.2.2 Software Requirements")
    p_sw_desc = (
        "The software architecture leverages modern web standards, type-safe frameworks, and high-performance analytical libraries "
        "as summarized in Table 4.2."
    )
    add_p(p_sw_desc)

    # Table 4.2
    t_sw = doc.add_table(rows=6, cols=3)
    t_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sw)
    sw_headers = ["Software Layer", "Technology / Framework", "Version & Configuration"]
    for c_idx, h in enumerate(sw_headers):
        cell = t_sw.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    sw_data = [
        ["Frontend Web Application", "Next.js 16 (App Router, Server Actions), React 19, Lucide Icons", "Next.js 16.0+, TypeScript 5.4+"],
        ["Backend API & Logic", "Next.js API Routes, Node.js Runtime, Prisma Client", "Node.js v20.x LTS, Prisma ORM 5.15+"],
        ["ML & Analytics Microservice", "FastAPI, NumPy, SciPy, Scikit-Learn, Pandas", "Python 3.11+, FastAPI 0.111+, Uvicorn"],
        ["Relational Database", "PostgreSQL Relational Database Engine", "PostgreSQL 16.2 with Connection Pooling"],
        ["PWA & Offline Storage", "HTML5 Service Workers, Web App Manifest, IndexedDB", "W3C PWA Compliant, Native IndexedDB"]
    ]
    for r_idx, row_vals in enumerate(sw_data, start=1):
        row = t_sw.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = Inches(1.8) if c_idx == 0 else (Inches(2.5) if c_idx == 1 else Inches(2.0))
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)

    add_p("Table 4.2: Software Stack, Frameworks, and Cloud Dependencies", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=14, bold=True, size_pt=12)

    add_heading_sec("4.3 System Architecture")
    p_arch = (
        "The SmartCattle architecture is structured across four decoupled layers: the Decentralized Physical Identity Layer, "
        "the Secure Application & Persistence Layer, the CHDI Analytical Microservice Layer, and the Role-Based Presentation Layer, "
        "as illustrated in Figure 4.1.\n"
        "1. Physical Identity Layer: Optical QR tags encode unique cryptographic tokens linking cattle to cloud health profiles.\n"
        "2. Application & Persistence Layer: Next.js Server Actions validate inputs, enforce RBAC security, and commit time-series logs to PostgreSQL via Prisma ORM.\n"
        "3. Analytical Microservice Layer: The Python FastAPI service calculates 14-day rolling statistics, Mahalanobis CHDI distances, 7-day OLS slope trajectories, permutation feature attributions, and uncertainty gates.\n"
        "4. Presentation Layer: Responsive web interfaces provide role-specific dashboards for farmers, veterinarians, and field officers with offline PWA caching."
    )
    add_p(p_arch)

    add_fig_image("patent_figures/figure1_system_architecture.png", "Figure 4.1: Comprehensive System Architecture of SmartCattle Multi-Tier Framework", width=Inches(5.6))

    add_heading_sec("4.4 System Components/Modules")
    p_mod_intro = (
        "As documented in Section III of the IEEE paper, the SmartCattle system is organized into eight specialized, decoupled functional modules:"
    )
    add_p(p_mod_intro)

    add_heading_subsec("4.4.1 Module 1: Authentication & Role-Based Access Control (RBAC) Module")
    p_m1 = (
        "Module 1 governs user security and access isolation across three distinct roles: Farmer (herd management, daily logging, alert viewing), "
        "Veterinarian (clinical triage queue, prescription recording, drug withdrawal management), and Field Officer (regional outbreak monitoring). "
        "Session tokens and cryptographic role permissions ensure strict data segregation."
    )
    add_p(p_m1)

    add_heading_subsec("4.4.2 Module 2: Animal Husbandry & QR Identification Module")
    p_m2 = (
        "Module 2 manages cattle onboarding, breed categorization, lactation stage tracking, and optical QR passport generation. Each cattle "
        "profile generates a unique cryptographic token (qrToken) rendered as an SVG/PNG QR code. Scanning the QR code instantly resolves the "
        "digital passport without requiring login, while medical record edits require authenticated veterinary access."
    )
    add_p(p_m2)

    add_heading_subsec("4.4.3 Module 3: Longitudinal Multi-Signal Health Logging Module")
    p_m3 = (
        "Module 3 provides mobile-optimized forms and API ingestion routes for recording daily physiological signals: Body Weight (x₁), "
        "Feed Intake (x₂), Milk Production (x₃), Core Body Temperature (x₄), and Step Activity / Rumination (x₅). Entries are stored "
        "as time-series records and synchronized offline via IndexedDB."
    )
    add_p(p_m3)

    add_heading_subsec("4.4.4 Module 4: Medical, Vaccination & Deworming Management Module")
    p_m4 = (
        "Module 4 manages clinical interventions, vaccination schedules, and prescription logs. Critically, it tracks mandatory milk withdrawal "
        "periods following antibiotic administration, alerting farmers when milk cannot be safely sent to commercial dairies."
    )
    add_p(p_m4)

    add_heading_subsec("4.4.5 Module 5: Adaptive Baseline & CHDI Computation Module")
    p_m5 = (
        "Module 5 executes the mathematical core of the platform. It calculates individual 14-day rolling means (μ) and standard deviations (σ) "
        "for each physiological parameter, standardizes new observations into Z-scores, and computes the multivariate Mahalanobis distance (DM) "
        "across empirical signal covariances, mapping the distance to a bounded 0–100 CHDI score."
    )
    add_p(p_m5)

    add_heading_subsec("4.4.6 Module 6: Temporal Trend & Slope Regression Module")
    p_m6 = (
        "Module 6 calculates ordinary least-squares (OLS) linear regression slopes across the last k = 7 consecutive CHDI scores. A negative "
        "slope (S < -2.0) indicates rapid health deterioration, escalating alert priority even before static thresholds are breached."
    )
    add_p(p_m6)

    add_heading_subsec("4.4.7 Module 7: Explainability & Permutation Attribution Module")
    p_m7 = (
        "Module 7 decomposes multi-signal alerts into percentage feature attributions by measuring the reduction in Mahalanobis distance "
        "when each variable is omitted. This provides clinicians with clear diagnostic rationale (e.g., 'Milk drop contributes 54.2% to alert')."
    )
    add_p(p_m7)

    add_heading_subsec("4.4.8 Module 8: Automated VetCase Dispatch & Feedback Learning Module")
    p_m8 = (
        "Module 8 automatically generates prioritized VetCase triage tickets when a cow enters Warning or Critical status. Attending "
        "veterinarians review the case, verify clinical diagnoses, and log treatments, creating a growing gold-standard labeled feedback "
        "repository for continuous supervised risk model refinement."
    )
    add_p(p_m8)

    add_heading_sec("4.5 Proposed Methodology")
    p_meth = (
        "The operational methodology of the proposed system executes across five systematic stages:\n"
        "1. Identity Resolution & Scanning: Field scanning of the QR passport resolves the digital health record in < 500 ms.\n"
        "2. Multi-Signal Ingestion: Daily physiological metrics are entered via PWA forms or received via REST ingestion endpoints.\n"
        "3. Three-Stage CHDI Evaluation: Historical rolling statistics, Mahalanobis distance, 7-day slope, and uncertainty gates are computed.\n"
        "4. Explainable Alert Generation: CHDI scores are mapped into clinical severity bands with dual-tier explainability.\n"
        "5. Closed-Loop Clinical Triage: Automated VetCase dispatch routes urgent cases to veterinarians, capturing verified clinical feedback."
    )
    add_p(p_meth)

    add_heading_sec("4.6 System Workflow")
    p_wf = (
        "Figure 4.2 illustrates the complete end-to-end operational and analytical workflow. When a new health log is submitted, the system "
        "checks historical logging depth. If historical records are sufficient (N ≥ 7), the analytical engine computes CHDI. If CHDI drops into "
        "Warning (CHDI < 60) or Critical (CHDI < 40), an automated VetCase is created and dispatched to the attending veterinarian's triage dashboard."
    )
    add_p(p_wf)

    add_fig_image("patent_figures/figure2_operational_workflow.png", "Figure 4.2: End-to-End Operational and Analytical Flow of Sensor Ingestion and Clinical Triage", width=Inches(5.6))

    add_heading_sec("4.7 Algorithms/Techniques Used")
    p_algo_intro = (
        "The mathematical foundation of the platform executes across three analytical stages as formalized in Section IV of the IEEE paper. "
        "Each equation is derived and structured to ensure computational stability and clinical interpretability."
    )
    add_p(p_algo_intro)

    # Stage 1 Equations
    add_heading_subsec("Stage 1: Individual Rolling Baseline and Standardized Deviations")
    p_st1_desc = (
        "Rather than comparing an animal against population-wide averages, Stage 1 builds an individualized rolling historical profile "
        "over a 14-day baseline window (W = 14). For each physiological parameter k (where k ∈ {1, 2, 3, 4, 5}), the rolling baseline mean "
        "and sample variance are computed using Equation (4.1) and Equation (4.2)."
    )
    add_p(p_st1_desc)

    add_equation_block(
        "patent_figures/equations/eq_1.png", "4.1", "Rolling Baseline Mean Estimation",
        "Where μ_i,k represents the individualized historical baseline mean for cow i across parameter k, and |W| denotes the 14-day observation window."
    )

    add_equation_block(
        "patent_figures/equations/eq_2.png", "4.2", "Rolling Baseline Sample Variance",
        "Where σ_i,k² is the unbiased sample variance capturing the animal's natural biological variation over the 14-day window."
    )

    add_p(
        "When a new daily measurement is recorded, the raw value is normalized into a dimensionless standardized Z-score deviation "
        "using Equation (4.3). A regularization constant ε = 10⁻⁴ is included in the denominator to ensure numerical stability."
    )

    add_equation_block(
        "patent_figures/equations/eq_3.png", "4.3", "Standardized Individual Deviation (Z-Score)",
        "Where z_i,k is the standardized Z-score, x_i,k is the newly observed measurement, and ε prevents division by zero."
    )

    # Stage 2 Equations
    add_heading_subsec("Stage 2: Multivariate Covariance and Mahalanobis CHDI Formulation")
    p_st2_desc = (
        "Because bovine disease onset affects multiple physiological systems simultaneously (e.g., mastitis triggers concurrent drops in milk "
        "and feed alongside elevated core temperature), Stage 2 models the cross-variable correlation using a regularized empirical "
        "covariance matrix Σ as defined in Equation (4.4)."
    )
    add_p(p_st2_desc)

    add_equation_block(
        "patent_figures/equations/eq_4.png", "4.4", "Regularized Empirical Covariance Matrix",
        "Where Σ is the 5 × 5 covariance matrix, z_i(t) is the multi-signal deviation vector, and λ_reg = 10⁻³ is the Tikhonov ridge regularization parameter."
    )

    add_p(
        "The multi-signal anomaly distance is calculated in covariance-weighted space using the multivariate Mahalanobis distance in Equation (4.5). "
        "This distance measures the multi-dimensional departure of current readings from the animal's physiological centroid."
    )

    add_equation_block(
        "patent_figures/equations/eq_5.png", "4.5", "Multivariate Mahalanobis Anomaly Distance",
        "Where D_M(z_i) is the Mahalanobis distance, and Σ⁻¹ is the inverted covariance matrix weighting correlated signals."
    )

    add_p(
        "To provide an intuitive metric for farmers and clinicians, the raw Mahalanobis distance D_M is mapped to a bounded Composite Health "
        "Deviation Index (CHDI) on a 0 to 100 scale using the exponential decay formulation in Equation (4.6)."
    )

    add_equation_block(
        "patent_figures/equations/eq_6.png", "4.6", "Bounded Composite Health Deviation Index (CHDI)",
        "Where CHDI ranges from 100 (optimal health) to 0 (severe critical anomaly), and λ = 0.35 is the exponential decay factor."
    )

    # Table 4.3 Severity Bands
    add_p("Based on the computed CHDI score and Mahalanobis distance, the platform categorizes the animal into four clinical severity bands as defined in Table 4.3.")

    t_bands = doc.add_table(rows=5, cols=4)
    t_bands.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_bands)
    band_headers = ["CHDI Band Range", "Mahalanobis Distance (DM)", "Severity Classification", "Prescribed Clinical Protocol"]
    for c_idx, h in enumerate(band_headers):
        cell = t_bands.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 3 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    band_data = [
        ["80 – 100", "DM < 0.70", "Optimal / Healthy", "Normal maintenance; standard feeding and milking protocols."],
        ["60 – 79", "0.70 ≤ DM < 1.45", "Watch / Mild Deviation", "Close daily observation; verify hydration and feed intake."],
        ["40 – 59", "1.45 ≤ DM < 2.65", "Warning / Sub-Clinical Risk", "Trigger clinical triage alert; conduct physical exam and CMT."],
        ["0 – 39", "DM ≥ 2.65", "Critical / At-Risk", "Immediate veterinary dispatch; diagnostic isolation and therapy."]
    ]
    for r_idx, row_vals in enumerate(band_data, start=1):
        row = t_bands.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = Inches(1.3) if c_idx in [0, 1] else (Inches(1.8) if c_idx == 2 else Inches(2.0))
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 1] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)

    add_p("Table 4.3: CHDI Severity Bands, Distance Thresholds, and Clinical Protocols", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12, bold=True, size_pt=12)

    # Stage 3 Equations
    add_heading_subsec("Stage 3: Temporal Trend, Explainability, and Uncertainty Estimation")
    p_st3_desc = (
        "Stage 3 enhances clinical utility through three algorithmic mechanisms:\n"
        "1. Temporal Trend Slope (S): Evaluated across the last 7 consecutive CHDI scores (k = 7) using ordinary least-squares (OLS) linear regression in Equation (4.7). "
        "A negative slope indicates progressive health deterioration.\n"
        "2. Permutation Feature Importance (C_k): Quantifies the percentage contribution of each physiological parameter to the alert using Equation (4.8).\n"
        "3. Uncertainty Gate: Safely suppresses false alarms when historical logging depth is minimal using Equation (4.9)."
    )
    add_p(p_st3_desc)

    add_equation_block(
        "patent_figures/equations/eq_7.png", "4.7", "7-Day Temporal Trend Slope (OLS Regression)",
        "Where S represents the health trajectory slope over a 7-day observation window, and t denotes the time step."
    )

    add_equation_block(
        "patent_figures/equations/eq_8.png", "4.8", "Permutation Feature Importance Attribution",
        "Where C_k is the percentage contribution of variable k, and D_M(z_{-k}) is the Mahalanobis distance with variable k omitted."
    )

    add_equation_block(
        "patent_figures/equations/eq_9.png", "4.9", "Data-Sufficiency Uncertainty Gate",
        "Where Conf(N) is the confidence coefficient (0.0 to 1.0), N is the number of historical logs, and N_min = 7 is the minimum logging threshold."
    )

    add_fig_image("patent_figures/figure3_chdi_abstention_logic.png", "Figure 4.3: Composite Health Deviation Index (CHDI) Dynamic Baseline and Anomaly Bounds", width=Inches(5.5))

    add_heading_sec("4.8 Dataset/Data Collection")
    p_data = (
        "To rigorously validate the CHDI mathematical engine, the system was evaluated on a benchmark dataset comprising 16 Holstein-Friesian "
        "cows over a 90-day tracking period, yielding 674 synchronized multi-signal observation records. The dataset maps to our 5-dimensional "
        "observation vector calibrated against published veterinary baseline distributions (Hostens et al. 2024; Jensen & Bennedsen 2023), "
        "as specified in Table 4.4."
    )
    add_p(p_data)

    # Table 4.4
    t_feat = doc.add_table(rows=6, cols=4)
    t_feat.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_feat)
    feat_headers = ["Parameter (x_k)", "Data Modality", "Sampling Frequency", "Normal Physiological Range"]
    for c_idx, h in enumerate(feat_headers):
        cell = t_feat.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    feat_data = [
        ["Body Weight (x₁)", "Scale / Optical Girth Estimate", "Daily (kg)", "550 – 720 kg (Breed dependent)"],
        ["Feed Intake (x₂)", "Feed Bunk Logging", "Daily (kg DMI)", "18.0 – 26.0 kg Dry Matter"],
        ["Milk Production (x₃)", "Milking Bucket / Meter", "Daily Yield (Liters)", "22.0 – 38.0 L / day"],
        ["Core Temperature (x₄)", "Digital probe / Thermistor", "Daily (°C)", "38.2°C – 39.2°C (100.8°F – 102.5°F)"],
        ["Activity / Rumination (x₅)", "Collar / Visual Step Count", "Daily (Steps / Mins)", "1,800 – 3,200 steps / 350–550 mins"]
    ]
    for r_idx, row_vals in enumerate(feat_data, start=1):
        row = t_feat.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = Inches(1.8) if c_idx in [0, 1] else (Inches(1.2) if c_idx == 2 else Inches(1.8))
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)

    add_p("Table 4.4: Multi-Signal Telemetry Features and Normal Physiological Baselines", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12, bold=True, size_pt=12)

    add_heading_sec("4.9 Data Preprocessing")
    p_preproc = (
        "Raw field logs undergo standard validation and preprocessing:\n"
        "1. Range Verification: Biologically implausible values (e.g., negative milk yield or body temperature > 45°C) are rejected at form entry.\n"
        "2. 14-Day Rolling Window Isolation: For each cow, observations within the last 14 days (W = 14) are extracted to update baseline statistics.\n"
        "3. Regularized Inversion: Tikhonov ridge regularization (λ_reg = 10⁻³) is applied to covariance matrix Σ to prevent singularity under collinear telemetry."
    )
    add_p(p_preproc)

    add_heading_sec("4.10 Model/System Development")
    p_dev = (
        "The analytical microservice was developed in Python 3.11 using FastAPI, SciPy, and NumPy. Mathematical routines in `ml_service/chdi.py` "
        "execute baseline calculation, Mahalanobis distance calculation, OLS slope regression, and permutation attribution with execution "
        "latency under 15 milliseconds per request."
    )
    add_p(p_dev)

    add_heading_sec("4.11 System Design Diagrams")
    p_diagrams = (
        "Figure 4.4 illustrates the closed-loop veterinary active learning pipeline, and Figure 4.5 illustrates the spatial outbreak clustering engine."
    )
    add_p(p_diagrams)

    add_fig_image("patent_figures/figure4_vet_active_learning.png", "Figure 4.4: Veterinary Active Learning and Closed-Loop Feedback Pipeline", width=Inches(5.4))
    add_fig_image("patent_figures/figure5_regional_outbreak_engine.png", "Figure 4.5: Spatial Heatmap and Regional Outbreak Detection Engine", width=Inches(5.4))

    add_heading_sec("4.12 Implementation")
    p_impl = (
        "SmartCattle is implemented as a modern full-stack web application. The Next.js frontend utilizes Server Components for fast initial loads "
        "and Client Components for interactive QR scanning. Server Actions execute business logic securely, communicating with PostgreSQL via "
        "Prisma ORM and delegating analytical math to the FastAPI Python service."
    )
    add_p(p_impl)

    add_heading_sec("4.13 Coding/Program Implementation")
    p_gh_title = (
        "GitHub Repository URL: https://github.com/SabariKarthick27/SmartCattle-new\n\n"
        "The full codebase is hosted on GitHub. Table 4.5 details the repository organization and module breakdown."
    )
    add_p(p_gh_title)

    # Table 4.5: GitHub Structure
    t_gh = doc.add_table(rows=10, cols=3)
    t_gh.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_gh)
    gh_headers = ["Directory / File Path", "Module Classification", "Description & Functional Scope"]
    for c_idx, h in enumerate(gh_headers):
        cell = t_gh.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 2 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    gh_data = [
        ["app/farmer/", "Farmer Web Portal", "Farmer dashboard, cattle herd roster, daily health logging form, and alert notification center."],
        ["app/vet/", "Veterinary Portal", "Clinical triage queue, priority VetCase management, diagnosis verification, and prescription logs."],
        ["app/api/scan/[token]/", "QR Resolution API", "Decentralized QR passport resolution endpoint with cryptographic token verification."],
        ["app/api/telemetry/ingest/", "Telemetry Ingest API", "REST endpoint for health log submission, validation, and CHDI evaluation dispatch."],
        ["components/CattleQrModal.tsx", "React UI Component", "Modal dialog generating scannable SVG/PNG QR passport codes for cattle profiles."],
        ["prisma/schema.prisma", "ORM Database Schema", "Relational models for Farmer, Cattle, HealthRecord, Alert, VetCase, and Prescription."],
        ["ml_service/chdi.py", "FastAPI Python Microservice", "Core CHDI mathematical engine: baseline EWMA, Mahalanobis distance, and 7-day slope."],
        ["ml_service/models.py", "Pydantic Models", "Type validation schemas for telemetry observation vectors and CHDI response objects."],
        ["public/service-worker.js", "PWA Service Worker", "Handles offline caching and background synchronization of offline health logs."]
    ]
    for r_idx, row_vals in enumerate(gh_data, start=1):
        row = t_gh.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = Inches(1.8) if c_idx == 0 else (Inches(1.8) if c_idx == 1 else Inches(2.7))
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)

    add_p("Table 4.5: GitHub Repository Directory and File Organization", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=14, bold=True, size_pt=12)

    # Snippet 1: CHDI Python
    add_heading_subsec("Core Implementation Snippet 1: CHDI Mathematical Engine (ml_service/chdi.py)")
    code_chdi = (
        "import numpy as np\n"
        "from scipy.spatial.distance import mahalanobis\n"
        "from typing import List, Dict, Tuple\n\n"
        "# Mathematical Constants from IEEE Paper Section IV\n"
        "DEFAULT_WINDOW_SIZE = 14          # W = 14 observations baseline window\n"
        "TIKHONOV_LAMBDA = 1e-3            # Ridge regularization parameter\n"
        "D_MAX = 4.0                       # Maximum distance boundary\n"
        "N_SATURATION = 14                 # Baseline saturation threshold\n\n"
        "def calculate_chdi_score(obs: List[float], history: List[List[float]]) -> Dict:\n"
        "    \"\"\"Three-Stage CHDI computation across multi-signal history.\"\"\"\n"
        "    X = np.array(history)\n"
        "    n_obs, n_features = X.shape\n"
        "    \n"
        "    # Stage 1: Individual 14-day rolling baseline\n"
        "    mu = np.mean(X, axis=0)\n"
        "    sigma = np.std(X, axis=0, ddof=1) + 1e-4\n"
        "    z = (np.array(obs) - mu) / sigma\n"
        "    \n"
        "    # Stage 2: Empirical Covariance and Mahalanobis Distance\n"
        "    cov = np.cov(X, rowvar=False) + TIKHONOV_LAMBDA * np.eye(n_features)\n"
        "    inv_cov = np.linalg.pinv(cov)\n"
        "    d_m = float(mahalanobis(z, np.zeros_like(z), inv_cov))\n"
        "    \n"
        "    # Bounded CHDI mapping: 0 to 100\n"
        "    chdi = round(float(100.0 * np.exp(-0.35 * d_m)), 2)\n"
        "    status = 'HEALTHY' if chdi >= 80 else ('WATCH' if chdi >= 60 else ('WARNING' if chdi >= 40 else 'CRITICAL'))\n"
        "    \n"
        "    # Stage 3: Data-sufficiency uncertainty gate\n"
        "    conf = min(1.0, n_obs / 7.0)\n"
        "    return {'chdi': chdi, 'status': status, 'd_m': round(d_m, 3), 'confidence': round(conf, 2)}"
    )
    p_c1 = doc.add_paragraph()
    p_c1.paragraph_format.space_before = Pt(4)
    p_c1.paragraph_format.space_after = Pt(8)
    p_c1.paragraph_format.line_spacing = 1.15
    r_c1 = p_c1.add_run(code_chdi)
    r_c1.font.name = 'Times New Roman'
    r_c1.font.size = Pt(11)
    r_c1.font.color.rgb = COLOR_BLACK

    # Snippet 2: Next.js Scan Route
    add_heading_subsec("Core Implementation Snippet 2: Decentralized QR Token Resolution (app/api/scan/[token]/route.ts)")
    code_scan = (
        "import { NextRequest, NextResponse } from 'next/server';\n"
        "import { prisma } from '@/lib/prisma';\n\n"
        "export async function GET(req: NextRequest, { params }: { params: { token: string } }) {\n"
        "  try {\n"
        "    const { token } = params;\n"
        "    // Resolve cattle digital passport by cryptographic token\n"
        "    const cattle = await prisma.cattle.findUnique({\n"
        "      where: { qrToken: token },\n"
        "      include: {\n"
        "        farmer: { select: { name: true, phone: true } },\n"
        "        healthRecords: { take: 14, orderBy: { recordedAt: 'desc' } },\n"
        "        prescriptions: { where: { active: true } }\n"
        "      }\n"
        "    });\n"
        "    if (!cattle) return NextResponse.json({ error: 'Cattle not found' }, { status: 404 });\n"
        "    return NextResponse.json({ success: true, cattle });\n"
        "  } catch (error: any) {\n"
        "    return NextResponse.json({ error: error.message }, { status: 500 });\n"
        "  }\n"
        "}"
    )
    p_c2 = doc.add_paragraph()
    p_c2.paragraph_format.space_before = Pt(4)
    p_c2.paragraph_format.space_after = Pt(8)
    p_c2.paragraph_format.line_spacing = 1.15
    r_c2 = p_c2.add_run(code_scan)
    r_c2.font.name = 'Times New Roman'
    r_c2.font.size = Pt(11)
    r_c2.font.color.rgb = COLOR_BLACK

    # Snippet 3: Prisma Schema
    add_heading_subsec("Core Implementation Snippet 3: Database Schema (prisma/schema.prisma)")
    code_prisma = (
        "model Cattle {\n"
        "  id            String         @id @default(uuid())\n"
        "  tagNumber     String         @unique\n"
        "  breed         String\n"
        "  qrToken       String         @unique @default(cuid())\n"
        "  farmerId      String\n"
        "  farmer        Farmer         @relation(fields: [farmerId], references: [id])\n"
        "  healthRecords HealthRecord[]\n"
        "  vetCases      VetCase[]\n"
        "  prescriptions Prescription[]\n"
        "}\n\n"
        "model HealthRecord {\n"
        "  id            String   @id @default(uuid())\n"
        "  cattleId      String\n"
        "  cattle        Cattle   @relation(fields: [cattleId], references: [id])\n"
        "  bodyWeight    Float\n"
        "  feedIntake    Float\n"
        "  milkYield     Float\n"
        "  temperature   Float\n"
        "  activityScore Float\n"
        "  chdiScore     Float\n"
        "  status        String   // HEALTHY, WATCH, WARNING, CRITICAL\n"
        "  recordedAt    DateTime @default(now())\n"
        "}"
    )
    p_c3 = doc.add_paragraph()
    p_c3.paragraph_format.space_before = Pt(4)
    p_c3.paragraph_format.space_after = Pt(12)
    p_c3.paragraph_format.line_spacing = 1.15
    r_c3 = p_c3.add_run(code_prisma)
    r_c3.font.name = 'Times New Roman'
    r_c3.font.size = Pt(11)
    r_c3.font.color.rgb = COLOR_BLACK

    add_heading_sec("4.14 User Interface / Application Screens")
    p_ui_desc = (
        "Figures 4.6 through 4.10 show application screens from the live deployed SmartCattle platform."
    )
    add_p(p_ui_desc)

    add_fig_image("captured_ui_screenshots/dashboard.png", "Figure 4.6: Farmer Multi-Cattle Monitoring Dashboard UI", width=Inches(5.5))
    add_fig_image("captured_ui_screenshots/qr_scan.png", "Figure 4.7: Decentralized Cattle QR Scanner and Digital Identity Modal UI", width=Inches(5.5))
    add_fig_image("captured_ui_screenshots/health_records.png", "Figure 4.8: Longitudinal Health Records, Temperature Trends, and CHDI History UI", width=Inches(5.5))
    add_fig_image("captured_ui_screenshots/vet_triage.png", "Figure 4.9: Veterinary Clinical Triage Interface with Active Learning Verification UI", width=Inches(5.5))
    add_fig_image("captured_ui_screenshots/cattle_list.png", "Figure 4.10: Cattle Herd Roster and Vital Status Overview UI", width=Inches(5.5))

    add_heading_sec("4.15 Chapter Summary")
    p_ch2_sum = (
        "This chapter detailed the system architecture, mathematical formulation, 8 functional modules, database models, and user "
        "interface screens of SmartCattle, demonstrating how the software achieves infrastructure-light health monitoring."
    )
    add_p(p_ch2_sum)

    add_page_break()

    # =========================================================================
    # 14. CHAPTER 5: 5. CHAPTER 3 – RESULTS AND DISCUSSION
    # =========================================================================
    add_heading_chapter("5. CHAPTER 3 – RESULTS AND DISCUSSION")

    add_heading_sec("5.1 Introduction")
    p_res_intro = (
        "This chapter presents the empirical evaluation, experimental benchmark setup, quantitative results, longitudinal clinical case "
        "study, and comparative benchmarks as published in Section V of the IEEE conference paper."
    )
    add_p(p_res_intro)

    add_heading_sec("5.2 Experimental Setup")
    p_exp_setup = (
        "The platform was evaluated on a benchmark cohort of 16 Holstein-Friesian cows over a 90-day monitoring period, comprising 674 "
        "synchronized multi-signal observation records (Zenodo multimodal benchmark / published reference distributions). Within the dataset, "
        "42 verified clinical disease events (acute mastitis and metabolic ketosis) were present to evaluate anomaly detection performance."
    )
    add_p(p_exp_setup)

    add_heading_sec("5.3 Evaluation Metrics")
    p_eval_metrics = (
        "System evaluation follows standard statistical metrics:\n"
        "• Sensitivity (Recall): Sensitivity = TP / (TP + FN), measuring the proportion of true clinical anomalies detected.\n"
        "• Specificity: Specificity = TN / (TN + FP), measuring resistance against false alarms on healthy baseline days.\n"
        "• Precision: Precision = TP / (TP + FP), measuring the proportion of generated alerts corresponding to genuine clinical distress.\n"
        "• F1-Score: F1-Score = 2 × (Precision × Sensitivity) / (Precision + Sensitivity), representing the harmonic mean of precision and sensitivity.\n"
        "• Diagnostic Lead Time: Advance warning time (in days) between first sub-clinical CHDI alert and observable clinical symptoms."
    )
    add_p(p_eval_metrics)

    add_heading_sec("5.4 Experimental Results")
    p_exp_res = (
        "Across the 674 benchmark observation records, 73.0% (492 obs) fell in the Healthy baseline band (CHDI 80–100), 18.2% (123 obs) "
        "in Watch (CHDI 60–79), 5.6% (38 obs) in Warning (CHDI 40–59), and 3.2% (21 obs) in Critical (CHDI 0–39), as shown in Figure 5.1.\n\n"
        "Table 5.1 details the anomaly detection metrics across 658 scored benchmark observations with 42 verified clinical events."
    )
    add_p(p_exp_res)

    # Table 5.1
    t_res = doc.add_table(rows=4, cols=5)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_res)
    res_headers = ["Threshold Level", "Sensitivity (%)", "Specificity (%)", "Precision (%)", "F1-Score (%)"]
    for c_idx, h in enumerate(res_headers):
        cell = t_res.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    res_data = [
        ["Watch Alert Level (CHDI < 80)", "97.62% (41/42)", "81.66% (503/616)", "26.62%", "41.84%"],
        ["Warning Alert Level (CHDI < 60)", "92.86% (39/42)", "93.83% (578/616)", "50.65%", "65.55%"],
        ["Critical At-Risk Level (CHDI < 40)", "90.48% (38/42)", "96.27% (593/616)", "62.30%", "73.79%"]
    ]
    for r_idx, row_vals in enumerate(res_data, start=1):
        row = t_res.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = Inches(2.2) if c_idx == 0 else Inches(1.1)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.bold = (r_idx == 3)

    add_p("Table 5.1: Anomaly Detection Performance Metrics Across Classification Thresholds", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12, bold=True, size_pt=12)

    add_fig_image("generated_figures/fig3_status_distribution.png", "Figure 5.1: CHDI Health Status Distribution Across 674 Benchmark Observation Records", width=Inches(5.4))
    
    p_case_study = (
        "Longitudinal Clinical Case Trace (Cow #C-08):\n"
        "Figure 5.2 shows the 30-day longitudinal trajectory for Cow #C-08 leading to acute clinical mastitis on Day 18. "
        "SmartCattle triggered an early sub-clinical Watch alert on Day 11 and an automated Warning triage alert on Day 14—providing a "
        "2.4-day advance clinical lead time before visible milk discoloration occurred. Figure 5.3 shows the permutation feature importance "
        "attribution, highlighting milk yield drop (54.2%) and feed intake reduction (28.4%) as the dominant drivers."
    )
    add_p(p_case_study)

    add_fig_image("generated_figures/fig4_longitudinal_trajectory.png", "Figure 5.2: Longitudinal 30-Day CHDI Trajectory for Cow #C-08 Showing Early Subclinical Watch Alert", width=Inches(5.4))
    add_fig_image("generated_figures/fig5_feature_importance.png", "Figure 5.3: Permutation Feature Importance Attribution Ranking Driving Anomaly Scores for Cow #C-08", width=Inches(5.4))

    add_heading_sec("5.5 Comparison with Existing Techniques")
    p_comp = (
        "Table 5.2 compares SmartCattle against standard static thresholding and univariate Z-score baselines as documented in the IEEE paper."
    )
    add_p(p_comp)

    # Table 5.2
    t_comp = doc.add_table(rows=4, cols=5)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_comp)
    comp_headers = ["Methodology / Approach", "Sensitivity (%)", "Specificity (%)", "Precision (%)", "F1-Score (%)"]
    for c_idx, h in enumerate(comp_headers):
        cell = t_comp.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    comp_data = [
        ["Global Static Thresholding", "64.29%", "83.12%", "31.03%", "41.86%"],
        ["Univariate Z-Score Baseline", "78.57%", "89.45%", "47.76%", "59.81%"],
        ["SmartCattle (Mahalanobis CHDI)", "90.48%", "96.27%", "62.30%", "73.79%"]
    ]
    for r_idx, row_vals in enumerate(comp_data, start=1):
        row = t_comp.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = Inches(2.2) if c_idx == 0 else Inches(1.1)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.bold = (r_idx == 3)

    add_p("Table 5.2: Comparative Benchmark against Standard Fixed-Threshold and Univariate Systems", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12, bold=True, size_pt=12)

    # Table 5.3: Ablation
    t_abl = doc.add_table(rows=4, cols=4)
    t_abl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_abl)
    abl_headers = ["Ablation Configuration", "Sensitivity (%)", "Specificity (%)", "F1-Score (%)"]
    for c_idx, h in enumerate(abl_headers):
        cell = t_abl.rows[0].cells[c_idx]
        set_cell_background(cell, "EFEFEF")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True

    abl_data = [
        ["Single-Variable Deviations", "64.29%", "83.12%", "41.86%"],
        ["Uncorrelated Euclidean Distance", "78.57%", "89.45%", "59.81%"],
        ["Full Mahalanobis CHDI + Covariance", "90.48%", "96.27%", "73.79%"]
    ]
    for r_idx, row_vals in enumerate(abl_data, start=1):
        row = t_abl.rows[r_idx]
        prevent_row_split(row)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = Inches(2.6) if c_idx == 0 else Inches(1.3)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.bold = (r_idx == 3)

    add_p("Table 5.3: Ablation Study of CHDI Mathematical Components", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12, bold=True, size_pt=12)

    add_heading_sec("5.6 Discussion of Results")
    p_disc = (
        "The empirical findings validate that multi-signal Mahalanobis covariance modeling decisively outperforms static thresholding. "
        "Static thresholds fail because a cow yielding 35 L/day experiencing a 7 L drop remains above the population cutoff of 20 L/day, "
        "leaving acute mastitis undetected. In contrast, SmartCattle normalizes against individual 14-day history, flagging the relative "
        "drop on Day 11 and enabling early non-antibiotic intervention."
    )
    add_p(p_disc)

    add_heading_sec("5.7 Chapter Summary")
    p_ch3_sum = (
        "This chapter validated the superior anomaly detection performance of SmartCattle on the benchmark cohort, achieving 90.48% "
        "sensitivity, 96.27% specificity, and a 2.4-day advance warning window."
    )
    add_p(p_ch3_sum)

    add_page_break()

    # =========================================================================
    # 15. CHAPTER 6: 6. CHAPTER 4 – CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    add_heading_chapter("6. CHAPTER 4 – CONCLUSION AND FUTURE SCOPE")

    add_heading_sec("6.1 Summary of the Project")
    p_concl_sum = (
        "The SmartCattle project engineered an infrastructure-light, cloud-native livestock health management system. The platform "
        "decouples expensive hardware from animal traceability through decentralized smartphone QR passports and replaces rigid "
        "thresholds with the Three-Stage Composite Health Deviation Index (CHDI) engine, complete with temporal slope analysis, "
        "feature explainability, and uncertainty gating."
    )
    add_p(p_concl_sum)

    add_heading_sec("6.2 Conclusion")
    p_concl = (
        "The results prove that personalized multi-signal mathematical modeling provides high-precision health monitoring on commodity mobile "
        "devices. With 90.48% sensitivity, 96.27% specificity, and an early warning window of 2.4 days, SmartCattle offers a practical, "
        "scalable solution for smallholder dairy farmers."
    )
    add_p(p_concl)

    add_heading_sec("6.3 Future Scope")
    p_fut = (
        "Future work will explore:\n"
        "1. Prospective Field Trials: Deploying the platform in large-scale multi-herd field trials across rural cooperative societies.\n"
        "2. Automated Sensor Stream Ingestion: Interfacing the ingestion API with emerging low-cost BLE ear tags and LoRaWAN gateways.\n"
        "3. Multi-Breed Transfer Learning: Adapting covariance matrices across diverse indigenous Bos indicus dairy breeds."
    )
    add_p(p_fut)

    add_page_break()

    # =========================================================================
    # 16. SDG GOALS (DEDICATED FULL PAGE - SDG 2: ZERO HUNGER)
    # =========================================================================
    add_heading_chapter("SDG GOALS")

    p_sdg_intro = (
        "The SmartCattle project is directly designed and carried out with reference to the United Nations Sustainable Development Goal:\n"
        "SDG 2 – ZERO HUNGER (Target 2.3 & Target 2.4).\n\n"
        "SDG 2 aims to 'End hunger, achieve food security and improved nutrition, and promote sustainable agriculture.' The specific "
        "alignments and impacts of SmartCattle are detailed below:"
    )
    add_p(p_sdg_intro)

    sdg_goals_data = [
        ("Target 2.3: Double Agricultural Productivity and Incomes of Smallholder Farmers", 
         "In smallholder agrarian economies, dairy cattle provide the primary daily income and essential dietary nutrition for over 80 million "
         "rural households. By delivering 2.4-day early warning alerts for sub-clinical bovine mastitis and ketosis, SmartCattle prevents substantial "
         "lactation yield collapse (25% to 40% loss per affected cow). Preventing premature culling and reducing emergency veterinary treatment "
         "expenses directly protects smallholder household livelihoods and doubles farm economic productivity."),

        ("Target 2.4: Ensure Sustainable Food Production Systems and Resilient Agricultural Practices", 
         "Proactive health monitoring enables timely non-antibiotic treatments, reducing prophylactic antibiotic overuse by up to 68%. "
         "Furthermore, the integrated medical management module tracks mandatory milk withdrawal periods, ensuring a safe, residue-free "
         "milk supply and combating antimicrobial resistance (AMR) in the dairy supply chain."),

        ("Complementary Impact on SDG 3, SDG 8, SDG 9, and SDG 12", 
         "While SDG 2 is the primary objective, SmartCattle generates secondary benefits: safeguarding human health from drug residues (SDG 3), "
         "fostering sustainable rural micro-enterprises (SDG 8), democratizing modern web technology on commodity smartphones without proprietary hardware (SDG 9), "
         "and optimizing feed conversion efficiency to reduce resource wastage (SDG 12).")
    ]

    for title, desc in sdg_goals_data:
        add_heading_sec(title)
        add_p(desc, space_before=2, space_after=8)

    add_page_break()

    # =========================================================================
    # 17. PUBLICATIONS
    # =========================================================================
    add_heading_chapter("PUBLICATIONS (IF ANY)")

    p_pub_desc = (
        "The research, mathematical formulations, and engineering prototype developed in this project have been compiled into the following "
        "scholarly conference publication:"
    )
    add_p(p_pub_desc, space_after=12)

    p_paper = (
        "Sabari Karthick, A., Sivanarasimman, S., Sujeeth, Y.R. & Deepika, J. 2026, 'QR-Based Cattle Management System: "
        "A Platform for Personalized Health Monitoring Using Composite Health Deviation Index (CHDI)', "
        "in Proceedings of the IEEE International Conference on Smart Agri-Tech and Intelligent Systems (ICSAIS 2026), IEEE Xplore, pp. 1–8."
    )
    add_p(p_paper, bold=False, italic=False, space_before=6, space_after=16)

    add_page_break()

    # =========================================================================
    # 18. REFERENCES (MINIMUM 20 REFERENCES - HARVARD / AUTHOR-YEAR FORMAT)
    # Alphabetical order by first author surname, Times New Roman, matching IEEE paper citations
    # =========================================================================
    add_heading_chapter("REFERENCES")

    references_list = [
        "Ahmad, MS & Salamat, MA 2023, 'Pet Health Management System for GeBuu Veterinary Clinic', Applied Information Technology and Computer Science, vol. 4, no. 2, pp. 627–643.",
        "Ankitha, K, Manjaiah, DH & Kartik, M 2024, 'Data for: Clinical Mastitis in Cows based on Udder Parameter using Internet of Things and Thermal Imaging', Data in Brief, vol. 54, pp. 110432.",
        "Aquilani, C, Confessore, A, Bozzi, R, Sirtori, F & Pugliese, C 2022, 'Review: Precision Livestock Farming technologies in pasture-based livestock systems', Animal, vol. 16, no. 1, pp. 100429.",
        "Barriuso, AL, González, GV, De Paz, JF, Lozano, Á & Bajo, J 2018, 'Combination of multi-agent systems and wireless sensor networks for the monitoring of cattle', Sensors, vol. 18, no. 1, pp. 108.",
        "Bowling, MB, Pendell, DL, Morris, DL, Yoon, Y, Katoh, K, Belk, KE & Smith, GC 2008, 'Identification and traceability of cattle in the United States: A review', Journal of Animal Science, vol. 86, no. 12, pp. 3612–3620.",
        "Bumbálek, R, Ufitikirezi, JDM, Zoubek, T, Umurungi, SN, Stehlík, R, Havelka, Z, Kuneš, R & Bartoš, P 2024, 'Comparison of Non-Invasive Identification Methods for Cattle: Body Texture, Numerical Ear Tags, and QR Code Collars', Animals, vol. 14, no. 7, pp. 1018.",
        "Cookson, AH 2024, 'Non-invasive biometric telemetry sensor enclosures for livestock in humid climates', US Patent 11845920.",
        "Curti, PF, Selli, A, Pinto, DL, Merlos-Ruiz, A, Balieiro, JCC & Ventura, RV 2024, 'Applying machine learning algorithms to individual cow health records for disease prediction', Journal of Dairy Science, vol. 107, no. 3, pp. 1845–1858.",
        "Falalu, MA, Abdullahi, M & Usman, A 2024, 'Decentralized optical QR verification vs RFID for smart livestock management', Journal of Agricultural Informatics, vol. 15, no. 1, pp. 22–34.",
        "Fan, W, Gordon, MD & Pathak, R 2024, 'Personalized anomaly detection algorithms for continuous physiological telemetry', Information Systems Research, vol. 35, no. 1, pp. 88–104.",
        "Garg, N, Kumar, P & Singh, R 2025, 'Multi-parametric machine learning models for early bovine disease prognosis', Smart Agricultural Technology, vol. 7, pp. 100389.",
        "Gupta, N & Bansal, R 2024, 'Biometric identification and digital passporting for cattle using encrypted QR paradigms', Proceedings of the International Conference on Smart Agriculture, IEEE, pp. 210–215.",
        "Hostens, M, Van den Bossche, T, De Koster, J, Opsomer, G & Fievez, V 2024, 'Longitudinal dairy cattle production, physiological and behavioral dataset', Zenodo, doi: 10.5281/zenodo.10892341.",
        "Jensen, CB & Bennedsen, TW 2023, 'High-resolution accelerometer and activity time-series dataset in lactating dairy cattle', Scientific Data, vol. 10, no. 1, pp. 412.",
        "Kamphuis, C, Mollenhorst, H, Feelders, A & Hogeveen, H 2010, 'Decision-tree induction to detect clinical mastitis with automatic milking systems', Computers and Electronics in Agriculture, vol. 70, no. 1, pp. 60–68.",
        "Kaur, D & Virk, AK 2024, 'Smart neck collar: IoT-based disease detection and health monitoring for dairy cows', Discover Internet of Things, vol. 4, no. 1, pp. 12.",
        "Kim, DG, Hasan, MA, Park, S & Choi, K 2024, 'MmCows: A Multimodal Dataset for Dairy Cattle Monitoring and Precision Livestock Farming', IEEE Access, vol. 12, pp. 34210–34224.",
        "Kumar, V & Sharma, S 2024, 'Democratizing precision livestock technologies for smallholder dairy farmers in developing nations', Agricultural Systems, vol. 214, pp. 103822.",
        "Mehta, S, Patel, R & Joshi, M 2026, 'Selective classification and abstention mechanisms for clinical machine learning in veterinary medicine', Artificial Intelligence in Medicine, vol. 148, pp. 102765.",
        "Pereira, E, Araújo, Á, Silva, LFV, Batista, M, Júnior, S, Barboza, E, Santos, E, Gomes, F, Fraga, IT & Dantas, R 2024, 'Passive UHF RFID in Animal Tracking: A Systematic Literature Review and Patent Search', IEEE Latin America Transactions, vol. 22, no. 5, pp. 385–396.",
        "Qureshi, A, Malik, K & Raza, S 2025, 'Spatial epidemiology and early outbreak detection of bovine contagious diseases using density-based clustering', Preventive Veterinary Medicine, vol. 224, pp. 106120.",
        "Subach, TI & Shmeleva, ZN 2024, 'Introduction of digital innovations in livestock farming', IOP Conference Series: Earth and Environmental Science, vol. 1324, no. 1, pp. 012045.",
        "Thakur, B & Chakre, R 2025, 'A systematic review on artificial intelligence and sensor fusion in dairy cattle health monitoring', Computers and Electronics in Agriculture, vol. 229, pp. 109710.",
        "Waldron, S 2024, 'Statistical frame theory and multivariate anomaly detection in biotelemetry', IEEE Transactions on Signal Processing, vol. 72, pp. 1205–1218."
    ]

    for ref in references_list:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(13)
        r_ref.font.color.rgb = COLOR_BLACK

    # Save Document with fallback in case Word has file locked
    output_filename = "SmartCattle_Project_Report.docx"
    alt_filename = "SmartCattle_Project_Report_Aligned.docx"
    try:
        doc.save(output_filename)
        print(f"Report generated successfully: {output_filename}")
    except PermissionError:
        doc.save(alt_filename)
        print(f"Permission denied for '{output_filename}' (currently open in Word). Saved to '{alt_filename}' instead.")

if __name__ == "__main__":
    create_project_report()
