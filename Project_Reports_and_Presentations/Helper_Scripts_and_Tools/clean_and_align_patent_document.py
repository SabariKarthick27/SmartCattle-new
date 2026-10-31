import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import zipfile
import shutil
import os

def set_run_font(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    # Ensure complex script font is also set to Times New Roman
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)

def clean_paragraph_spacing(p, space_before=0, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def clean_and_reformat_patent():
    input_docx = "SmartCattle_Patent_Disclosure_Perfect.docx"
    temp_docx = "temp_cleaned_patent.docx"
    final_docx = "SmartCattle_Patent_Disclosure_Perfect.docx"
    alt_final_docx = "QR_Based_Cattle_Management_Patent_Disclosure.docx"
    backup_docx = "SmartCattle_Patent_Disclosure_Final.docx"
    
    doc = docx.Document(input_docx)
    
    # 1. Remove redundant empty paragraphs
    # Keep track of paragraphs to remove (from back to front to avoid index shifting)
    paragraphs_to_remove = []
    
    # We want to remove paragraphs that have no text and no drawing/images
    for i, p in enumerate(doc.paragraphs):
        has_text = bool(p.text.strip())
        has_drawing = len(p._element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing')) > 0
        if not has_text and not has_drawing:
            paragraphs_to_remove.append(p)
            
    print(f"Removing {len(paragraphs_to_remove)} blank paragraphs...")
    for p in paragraphs_to_remove:
        p_elem = p._element
        parent = p_elem.getparent()
        if parent is not None:
            parent.remove(p_elem)
            
    print(f"Remaining active paragraphs: {len(doc.paragraphs)}")

    # 2. Iterate through all remaining paragraphs and apply uniform font, size, and alignment
    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue
            
        # Classify paragraph type
        is_main_heading = (
            txt.startswith("Specific Keywords") or 
            txt.startswith("1.") or 
            txt.startswith("2.") or 
            txt.startswith("3.") or 
            txt.startswith("6.") or 
            "Module" in txt and len(txt) < 80 and not txt.startswith("Components") or
            txt.startswith("End-to-End") or
            txt.startswith("Automated VetCase Dispatch")
        )
        
        is_sub_heading = (
            txt in ["Components:", "Function:"] or 
            txt.endswith(":") and len(txt) < 40 or
            "et al.," in txt or
            txt in [
                "Infrastructure-Light, Zero-Cost Optical Identification",
                "Adaptive Personalized Baseline vs. Rigid Population Norms",
                "Multivariate Covariance-Weighted Anomaly Detection (CHDI)",
                "Early Subclinical Disease Onset Detection (4 Days in Advance)",
                "Dual-Tier Explainability and Closed-Loop Veterinary Feedback"
            ]
        )
        
        is_list_item = (
            p.style.name == "List Paragraph" or 
            txt.startswith("1. ") or txt.startswith("2. ") or txt.startswith("3. ") or
            txt.startswith("4. ") or txt.startswith("5. ") or txt.startswith("6. ") or
            txt.startswith("7. ") or txt.startswith("8. ") or
            (len(p.runs) > 0 and txt in [
                "QR-Based Cattle Identification", "Smartphone-Readable Ear Tag", "Personalized Health Baseline",
                "Composite Health Deviation Index (CHDI)", "Multivariate Anomaly Detection",
                "Mahalanobis Distance with Tikhonov Regularization", "Temporal Trajectory Tracking & Slope Regression",
                "Subclinical Disease Early Detection", "Dual-Tier Explainability & Permutation Attribution",
                "Data-Sufficiency Abstention Gate", "Closed-Loop Veterinary Case Dispatch",
                "Role-Based Farm & Cooperative Portal", "Longitudinal Electronic Medical Records",
                "Precision Livestock Farming (PLF)", "Supervised Feedback Machine Learning Refinement",
                "Multi-tenant tenant isolation engine", "Role-Based Access Control (RBAC) coordinator (Farmer, Veterinarian, Admin)",
                "Argon2id password hashing and JWT authentication gateway", "Cooperative hierarchy and farm tenancy mapping database",
                "Cattle profile registry (Breed taxonomy, date of birth, parity, reproductive status)",
                "Cryptographic 128-bit UUID v4 token generator", "High-density 2-D QR matrix vector generator (SVG/PNG)",
                "Tag-to-profile binding and lifecycle registry", "Mobile web logging interface with offline caching",
                "Multi-signal data capture fields (Milk Yield, Feed Intake, Rumination, Temp, Activity)",
                "Biological plausibility validator and outlier filter", "Automatic UTC timestamping and GPS metadata tagger",
                "Data-source fidelity classifier (manual | qr_scan | sensor)", "Clinical diagnosis and treatment prescription logger",
                "Vaccination schedule engine with automated booster interval calculator", "Mandatory drug withdrawal period countdown monitor",
                "Preventive health compliance reminder system", "Dynamic rolling moving-average baseline calculator (Window W=14)",
                "Empirical 4x4 covariance matrix builder with Tikhonov regularization (lambda=1e-3)",
                "Multivariate Mahalanobis distance calculator (D_M)", "0–100 bounded CHDI normalization and severity band classifier",
                "7-day rolling least-squares linear regression solver", "Health slope (S) and trajectory velocity calculator",
                "Trajectory state classifier (Improving, Stable, Deteriorating, Fluctuating)", "Subclinical early-warning flag generator",
                "Leave-One-Covariate-Out (LOCO) permutation feature decomposition engine", "Relative percentage factor contribution ranker",
                "Dual-tier explanation translator (Plain Farmer Advisory & Clinical Vet Z-Score Matrix)",
                "Visualization chart and attribution badge generator", "Historical sample counter (Minimum N >= 7 over 5+ calendar days)",
                "Analytical confidence scoring engine (Saturation constant W=14)", "Explicit abstention protocol gatekeeper",
                "Data-sufficiency status reporter", "Farmer mobile portal with herd summary and quick QR logger",
                "Regional veterinarian triage dashboard with prioritized alert queue", "Interactive longitudinal CHDI trajectory and telemetry charts",
                "Multi-farm administrative herd health analytics console"
            ])
        )
        
        is_prompt = txt.startswith("Provide a general overview") or txt.startswith("Describe how the invention") or txt.startswith("i.Provide a detailed explanation")
        
        if is_main_heading:
            clean_paragraph_spacing(p, space_before=8, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
            for r in p.runs:
                set_run_font(r, font_name="Times New Roman", size_pt=13, bold=True)
        elif is_sub_heading:
            clean_paragraph_spacing(p, space_before=5, space_after=2, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
            for r in p.runs:
                set_run_font(r, font_name="Times New Roman", size_pt=12, bold=True)
        elif is_prompt:
            clean_paragraph_spacing(p, space_before=6, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
            for r in p.runs:
                set_run_font(r, font_name="Times New Roman", size_pt=11.5, bold=False, italic=True)
        elif is_list_item:
            clean_paragraph_spacing(p, space_before=1, space_after=2, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
            for r in p.runs:
                set_run_font(r, font_name="Times New Roman", size_pt=11.5, bold=False)
        else:
            # Standard body paragraph
            clean_paragraph_spacing(p, space_before=0, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
            for r in p.runs:
                # Keep bold if it was bold, otherwise regular
                was_bold = bool(r.font.bold)
                set_run_font(r, font_name="Times New Roman", size_pt=12, bold=was_bold)

    # 3. Format all tables consistently
    for t_idx, table in enumerate(doc.tables):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                for p in cell.paragraphs:
                    txt = p.text.strip()
                    if not txt:
                        continue
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.15
                    
                    # Clean up multiple consecutive line breaks within cell
                    if "\n\n\n" in p.text:
                        p.text = p.text.replace("\n\n\n", "\n\n")
                        
                    for r in p.runs:
                        is_header = (
                            r_idx == 0 or 
                            txt.startswith("1.") or 
                            txt.startswith("2.") or 
                            txt.startswith("3.") or 
                            txt.startswith("6.") or 
                            txt.startswith("a.") or 
                            txt.startswith("b.") or 
                            txt.startswith("e.") or 
                            txt.startswith("f.") or 
                            txt.startswith("8.") or
                            "Inventor" in txt or 
                            "Funding" in txt or 
                            "Commercial potential" in txt
                        )
                        # Keep bold for headers, 11pt for tables
                        was_bold = r.font.bold or is_header
                        set_run_font(r, font_name="Times New Roman", size_pt=11, bold=was_bold)

    doc.save(temp_docx)
    print(f"Saved cleaned intermediate file: {temp_docx}")

    # 4. Inject diagram back into image2.png
    diagram_png = 'smartcattle_system_modules_diagram.png'
    with zipfile.ZipFile(temp_docx, 'r') as zin:
        with zipfile.ZipFile(final_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/media/image2.png':
                    with open(diagram_png, 'rb') as img_f:
                        zout.writestr(item.filename, img_f.read())
                else:
                    zout.writestr(item, zin.read(item.filename))
                    
    print(f"SUCCESS: Formatted and aligned clean patent document at: {final_docx}")
    
    # Try updating alternative filenames
    for alt_name in [alt_final_docx, backup_docx]:
        try:
            shutil.copyfile(final_docx, alt_name)
            print(f"Updated: {alt_name}")
        except PermissionError:
            print(f"Notice: {alt_name} is currently open in Word.")

if __name__ == "__main__":
    clean_and_reformat_patent()
