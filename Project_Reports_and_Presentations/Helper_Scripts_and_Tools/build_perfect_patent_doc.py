import docx
import zipfile
import os
import shutil
from smartcattle_patent_texts import SMARTCATTLE_PARAGRAPHS

def apply_clean_text_to_paragraph(p, text):
    """Sets text on paragraph while preserving its style and first run's font properties."""
    if not p.runs:
        p.text = text
        return
        
    # Get first run font attributes
    r0 = p.runs[0]
    f_name = r0.font.name
    f_size = r0.font.size
    bold = r0.bold
    italic = r0.italic
    
    # Check if there are any drawings (e.g. inline images/checkboxes)
    drawing_runs = [r for r in p.runs if 'drawing' in r._element.xml]
    
    # Clear all runs
    p.text = text
    
    # Reapply font attributes to the single consolidated run
    if p.runs:
        new_r = p.runs[0]
        if f_name:
            new_r.font.name = f_name
        if f_size:
            new_r.font.size = f_size
        if bold is not None:
            new_r.bold = bold
        if italic is not None:
            new_r.italic = italic

def clean_cell_text(cell, new_text):
    """Updates cell text while preserving cell paragraph styles and drawings."""
    if not cell.paragraphs:
        cell.text = new_text
        return
    
    # If cell has drawings (e.g., checkboxes), preserve them
    has_drawing = any('drawing' in r._element.xml for p in cell.paragraphs for r in p.runs)
    if has_drawing:
        return
        
    p0 = cell.paragraphs[0]
    apply_clean_text_to_paragraph(p0, new_text)
    # Clear subsequent paragraphs if any
    for p in cell.paragraphs[1:]:
        if not any('drawing' in r._element.xml for r in p.runs):
            p.text = ""

def build_perfect_patent_docx():
    template_file = 'Patent Sample (1).docx'
    
    # Load base template
    template_doc = docx.Document(template_file)
    print(f"Template paragraphs: {len(template_doc.paragraphs)}")
    
    # 1. Update all mapped paragraphs
    for p_idx, p in enumerate(template_doc.paragraphs):
        if p_idx in SMARTCATTLE_PARAGRAPHS:
            apply_clean_text_to_paragraph(p, SMARTCATTLE_PARAGRAPHS[p_idx])

    # 2. Update Table 0: Details of the Invention
    t0 = template_doc.tables[0]
    clean_cell_text(t0.rows[1].cells[0], "a.  Title of the invention: QR-Based Cattle Management System for Personalized Health Monitoring and Decision Support")
    clean_cell_text(t0.rows[2].cells[0], "b. Field of the invention [Broader subject area of the invention]: Precision Livestock Farming, Internet of Things (IoT), Machine Learning, and Agricultural Veterinary Informatics")
    clean_cell_text(t0.rows[5].cells[0], "e. What is/are the Novel/New aspects of the invention: [Provide point-wise summary of what is new in the invention that is not known/practiced/reported previously]\n1. Zero-cost infrastructure-light animal identification using commodity smartphone-readable cryptographic 128-bit UUID QR ear tags.\n2. Adaptive Three-Stage Composite Health Deviation Index (CHDI) based on dynamic rolling EWMA baselines and covariance-weighted Mahalanobis distance.\n3. Temporal trajectory slope regression over 7-day windows to detect subclinical mastitis, lameness, and metabolic disorders up to four days prior to acute onset.\n4. Dual-tier Leave-One-Covariate-Out (LOCO) permutation feature explainability generating plain-language farmer advisories and granular veterinary z-score triage tables.\n5. Automated closed-loop clinical triage pipeline generating prioritized VetCase tickets with continuous ML model feedback refinement.")
    clean_cell_text(t0.rows[6].cells[0], "f. Is there any prior art for this invention: [Has the problem been solved/ Is the problem being solved in any other manner by others? Limitations and drawbacks of prior art]\nPrior art relies on expensive RFID transponders/readers, battery-constrained wearable IoT neck collars, or passive optical vision without health analytics. They apply rigid population-wide diagnostic thresholds, lack individualized baselines, lack explainability, and do not integrate automated closed-loop veterinary triage feedback.")

    # 3. Update Table 1: Detailed Scenario & Drawings
    t1 = template_doc.tables[1]
    scenario_text = (
        "8. Operational Scenario & Verification Workflow:\n\n"
        "A smallholder dairy farmer scans Cow #C-08's TPU ear tag with a standard mobile browser. The farmer logs daily milk yield (23.1 L), rumination time (415 min), and core body temperature (39.2 °C). "
        "The CHDI analytics engine compares these multi-signal vitals against Cow #C-08's personalized 14-day baseline and sample covariance matrix, identifying a significant multivariate departure. "
        "The 7-day temporal trajectory detects an acute deteriorating slope (-2.1), and the LOCO permutation attribution module identifies milk yield drop (34%) and rumination suppression (28%) as primary contributors. "
        "As the score enters the critical At-Risk band (CHDI < 50), the system automatically creates a prioritized VetCase ticket and notifies the regional veterinarian. "
        "The attending veterinarian conducts an on-site clinical examination, confirms early-stage Acute Mastitis, prescribes targeted antibiotic therapy, and logs the clinical outcome. "
        "This confirmed ground-truth diagnosis is stored in the animal's permanent electronic health record and ingested into the ML feedback repository for continuous model refinement."
    )
    clean_cell_text(t1.rows[0].cells[0], scenario_text)

    # 4. Table 3: Funding & Commercial Potential
    t3 = template_doc.tables[3]
    t3_r0 = (
        "Funding & Sponsorship\n"
        "Was this invention developed with any external funding or sponsorship?: No (Institutional Research & Development, Sona College of Technology)\n"
        "Potential applications / Industries: Dairy farms, smallholder livestock cooperatives, rural veterinary hospitals, animal-health extension centers, precision livestock farming platforms, and livestock insurance agencies.\n"
        "Known Competing technologies: Proprietary RFID electronic ear tag systems, wearable IoT neck collars/accelerometers, sensor-network nodes, standalone desktop dairy registries, and computer-vision animal monitoring tools.\n"
        "3. Companies that may be interested in licensing this technology: Dairy cooperatives (e.g., AAVIN, Amul, NDDB, Hatsun), livestock herd management software companies, veterinary health providers, agricultural IoT solution providers, and cattle identification tag manufacturers.\n"
        "Principal investigator (PI): Mrs. J. Deepika\n"
        "Are there any third-party obligations (e.g. collaborations, industry partners (if yes, provide details): No"
    )
    t3_r1 = (
        "Commercial potential:\n"
        "Potential applications / Industries: Precision livestock farming, cooperative milk production societies, rural veterinary health extension networks, automated cattle insurance validation, and commercial dairy herd health management.\n"
        "Known Competing technologies: Proprietary RFID ear tags with costly readers, high-cost wearable IoT neck collars, manual paper-based health ledgers, and standalone herd software lacking adaptive multivariate anomaly analytics."
    )
    clean_cell_text(t3.rows[0].cells[0], t3_r0)
    clean_cell_text(t3.rows[1].cells[0], t3_r1)

    # 5. Table 4: Licensing Companies & Inventorship Declaration
    t4 = template_doc.tables[4]
    t4_r0 = "3. Companies that may be interested in licensing this technology: Dairy cooperatives (Aavin, Amul, NDDB), veterinary health organizations, livestock farm management software companies, and agricultural IoT device providers."
    for cell in t4.rows[0].cells:
        clean_cell_text(cell, t4_r0)

    t4_decl = (
        "6. Inventorship declaration:\n"
        "I/ we declare that the information provided in this form is accurate and complete to the best of my/our knowledge. "
        "I/ we agree to assign rights in this invention to Sona College of Technology, in accordance with institutional policy.\n"
        "Inventor Signature(s) [If there are more than two inventors enter the details below]:"
    )
    for cell in t4.rows[1].cells:
        clean_cell_text(cell, t4_decl)

    # Inventor names & affiliations
    t4.rows[2].cells[2].text = "Inventor 1"
    t4.rows[2].cells[3].text = "Inventor 2"
    
    t4.rows[3].cells[1].text = "a.  Full Name"
    t4.rows[3].cells[2].text = "Mrs. J. Deepika"
    t4.rows[3].cells[3].text = "Sabari Karthick A"
    
    t4.rows[4].cells[1].text = "b.  Designation &Department"
    t4.rows[4].cells[2].text = "Assistant Professor, Department of Information Technology"
    t4.rows[4].cells[3].text = "Student / Researcher, Department of Information Technology"
    
    t4.rows[5].cells[1].text = "c.  Signature"
    t4.rows[6].cells[1].text = "d.  Date"

    # Save to intermediate docx
    temp_out = 'temp_built.docx'
    template_doc.save(temp_out)
    print(f"Saved {temp_out}")

    # 6. Inject the updated high-res SmartCattle modules diagram with arrows into media/image2.png
    output_docx = 'QR_Based_Cattle_Management_Patent_Disclosure.docx'
    new_diagram_png = 'smartcattle_system_modules_diagram.png'
    
    with zipfile.ZipFile(temp_out, 'r') as zin:
        with zipfile.ZipFile(output_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/media/image2.png':
                    print(f"Injecting {new_diagram_png} -> {item.filename}")
                    with open(new_diagram_png, 'rb') as img_f:
                        zout.writestr(item.filename, img_f.read())
                else:
                    zout.writestr(item, zin.read(item.filename))

    print(f"SUCCESS: Created perfectly formatted patent document at: {output_docx}")
    
    # Also save standalone named copy
    shutil.copyfile(output_docx, 'SmartCattle_Patent_Disclosure_Final.docx')
    print("Backup copy created at: SmartCattle_Patent_Disclosure_Final.docx")

if __name__ == "__main__":
    build_perfect_patent_docx()
