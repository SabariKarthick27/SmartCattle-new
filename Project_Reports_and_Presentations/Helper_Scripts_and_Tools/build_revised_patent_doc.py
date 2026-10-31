import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_header_cell(row, text, fill_hex="1A365D", color_rgb=RGBColor(255, 255, 255), font_size=11, bold=True):
    cell = row.cells[0]
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(font_size)
    run.font.color.rgb = color_rgb
    run.font.name = "Calibri"
    return cell

def add_two_col_row(table, label, content, label_w=2.0, content_w=4.8, bg_label="F7FAFC"):
    row = table.add_row()
    c0 = row.cells[0]
    c1 = row.cells[1]
    c0.width = Inches(label_w)
    c1.width = Inches(content_w)
    
    set_cell_background(c0, bg_label)
    set_cell_margins(c0, top=100, bottom=100, left=140, right=140)
    set_cell_margins(c1, top=100, bottom=100, left=140, right=140)
    
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r0 = p0.add_run(label)
    r0.bold = True
    r0.font.size = Pt(9.5)
    r0.font.name = "Calibri"
    r0.font.color.rgb = RGBColor(45, 55, 72)
    
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p1.add_run(content)
    r1.font.size = Pt(9.5)
    r1.font.name = "Calibri"
    r1.font.color.rgb = RGBColor(26, 32, 44)
    return row

def build_document():
    doc = Document()
    
    # Page setup - Margins 0.75 in
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
    fig_dir = r"c:\Project\SmartCattle new\patent_figures"
    
    # Title Banner
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_title.add_run("SONA COLLEGE OF TECHNOLOGY, SALEM - 636005\nCENTER FOR INTELLECTUAL PROPERTY RIGHTS (CIPR)\n")
    r_inst.bold = True
    r_inst.font.size = Pt(11)
    r_inst.font.color.rgb = RGBColor(26, 54, 93)
    r_inst.font.name = "Calibri"
    
    r_form = p_title.add_run("INVENTION DISCLOSURE FORM (IDF)\n")
    r_form.bold = True
    r_form.font.size = Pt(15)
    r_form.font.color.rgb = RGBColor(197, 48, 48)
    r_form.font.name = "Calibri"
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("CONFIDENTIAL DOCUMENT FOR PATENT ASSESSMENT & FILING\n")
    r_sub.italic = True
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = RGBColor(113, 128, 150)
    
    # -------------------------------------------------------------------------
    # SECTION 1: Details of the Invention
    # -------------------------------------------------------------------------
    t_sec1 = doc.add_table(rows=1, cols=1)
    t_sec1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sec1, color="1A365D", sz="8")
    add_header_cell(t_sec1.rows[0], "1.  DETAILS OF THE INVENTION", fill_hex="1A365D", font_size=11)
    
    doc.add_paragraph() # spacing
    
    # Table 1: Title, Field, Stage, Nature of Invention
    t_details = doc.add_table(rows=0, cols=2)
    t_details.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_details, color="CBD5E0", sz="4")
    
    add_two_col_row(t_details, "a.  Title of the Invention",
                    "A SYSTEM AND COMPUTER-IMPLEMENTED METHOD FOR SENSOR-INDEPENDENT LIVESTOCK HEALTH MONITORING USING OPTICAL IDENTIFIERS AND COMPOSITE MULTIVARIATE DEVIATION ANALYSIS\n\n(Alternative Title: QR-Based Cattle Management System with AI-Driven Health Monitoring and Composite Health Deviation Index [CHDI])")
    
    add_two_col_row(t_details, "b.  Field of the Invention",
                    "Precision Livestock Farming (PLF), Computer-Implemented Health Monitoring Systems, Applied Machine Learning, and Veterinary Tele-Informatics.\nIPC Classification: A01K 29/00 (Animal husbandry/monitoring), G16H 50/20 (ICT for medical/veterinary diagnosis), G06N 20/00 (Machine learning).")
    
    # Stage of development
    row_stage = t_details.add_row()
    c0 = row_stage.cells[0]; c1 = row_stage.cells[1]
    c0.width = Inches(2.0); c1.width = Inches(4.8)
    set_cell_background(c0, "F7FAFC")
    set_cell_margins(c0); set_cell_margins(c1)
    p0 = c0.paragraphs[0]; r0 = p0.add_run("c.  Stage of Development"); r0.bold = True; r0.font.size = Pt(9.5)
    p1 = c1.paragraphs[0]
    p1.add_run("☐ Idea only      ☐ Proof of concept      ☒ Prototype      ☒ Tested      ☐ In use/deployed\n(Working software prototype with integrated mobile optical scanner, cloud analytics API, and clinical vet portal evaluated on field cattle dataset)")
    
    # Nature of invention (Product & Process)
    row_nature = t_details.add_row()
    c0 = row_nature.cells[0]; c1 = row_nature.cells[1]
    c0.width = Inches(2.0); c1.width = Inches(4.8)
    set_cell_background(c0, "F7FAFC")
    set_cell_margins(c0); set_cell_margins(c1)
    p0 = c0.paragraphs[0]; r0 = p0.add_run("d.  Is the Invention based on"); r0.bold = True; r0.font.size = Pt(9.5)
    p1 = c1.paragraphs[0]
    p1.add_run("☒ Product (System / Apparatus)          ☒ Process / Method (Computer-Implemented Method)\n☐ Composition                             ☐ Other\n\n[Note: Formulated as both Apparatus and Process to overcome Section 3(k) statutory software exclusions under Indian Patent Practice.]")
    
    doc.add_paragraph() # spacing
    
    # -------------------------------------------------------------------------
    # Section 1.e: Novel / New aspects & Inventive Step
    # -------------------------------------------------------------------------
    t_nov = doc.add_table(rows=1, cols=1)
    t_nov.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_nov, color="2B6CB0", sz="6")
    add_header_cell(t_nov.rows[0], "e.  WHAT IS/ARE THE NOVEL/NEW ASPECTS OF THE INVENTION? WHAT IS THE INVENTIVE STEP?", fill_hex="2B6CB0", font_size=10.5)
    
    row_nov_content = t_nov.add_row()
    c_nov = row_nov_content.cells[0]
    set_cell_margins(c_nov, top=120, bottom=120, left=160, right=160)
    p = c_nov.paragraphs[0]
    p.add_run("The invention provides significant technical advancements and technical effects over existing livestock monitoring technologies through six interconnected inventive steps:\n\n").bold = True
    
    nov_items = [
        ("1. Optical Identifier Data Binding & Hardware-Independent Acquisition:",
         " Unlike conventional systems that necessitate permanent invasive or expensive electronic wearables (ear tags, collar accelerometers, boluses costing >$100/animal), the present system binds physical cattle identification via an optical QR token and accepts asynchronous multi-source inputs (manual mobile entry, optical camera scan timestamps, and optional IoT feeds). This eliminates hardware capex while maintaining continuous longitudinal data integrity."),
        
        ("2. Personalized Rolling Baseline Accounting for Biological Non-Stationarity:",
         " Instead of comparing physiological metrics to generalized breed/herd reference tables (which suffer massive variance across parity, age, and lactation cycles), the system dynamically computes an individual rolling statistical expectation (mean vector μ and covariance matrix Σ) constructed strictly from each animal's own temporal log history once a minimum registration sample threshold is reached."),
        
        ("3. Regularized Covariance-Aware Multivariate Anomaly Scoring (CHDI):",
         " Health signals (daily feed intake, bi-daily milk yield, activity count, periodic weight, and scan frequency) naturally exhibit strong physiological co-dependencies. Rather than arbitrary linear heuristics or independent univariate thresholds, the system computes the Composite Health Deviation Index (CHDI) using a regularized Mahalanobis distance metric: D_M(x) = sqrt((x - μ)^T * (Σ + λ*I)^(-1) * (x - μ)). This mathematical formulation directly captures the correlation geometry of normal physiological parameters."),
        
        ("4. Strict Matrix-Condition & Confidence-Bounded Abstention Gate:",
         " Early-stage classification in livestock health is notoriously prone to false-positive false alarms due to sparse initialization data. The system features an automated mathematical abstention mechanism that withholds a definitive healthy/at-risk verdict whenever sample counts N < N_min (e.g., N < 7 observations) or whenever the empirical covariance matrix is ill-conditioned (condition number exceeds κ_max). This eliminates false alarm fatigue among farmers."),
        
        ("5. Dual-Tier Explainable AI Architecture (Farmer vs. Clinician Triage):",
         " An explainability engine dynamically decomposes the composite distance vector into ranked feature attributions (via Shapley/permutation values). The system synthesizes two distinct outputs: (i) a simplified plain-language dominant factor alert for rural smallholder farmers (e.g., 'Feed intake dropped 38% below baseline'), and (ii) a complete multidimensional deviation vector and trajectory chart for veterinary diagnostic workstations."),
        
        ("6. Closed-Loop Active Learning Driven by Clinical Verification:",
         " Every system-flagged case routed to a veterinarian requires an explicit clinical verification outcome (Confirm [True Positive] vs. Override [False Positive]). These verified diagnostic outcomes are ingested into a secure labeled ground-truth repository to periodically retrain a secondary supervised classifier, dynamically optimizing detection boundaries based on real field clinical outcomes."),
        
        ("7. Spatio-Temporal Multi-Farm Outbreak Aggregation Engine:",
         " Deviations are cross-aggregated across discrete farm holdings using spatial coordinates/geohash clusters and a sliding temporal window (e.g., 72 hours). When the local cluster anomaly density exceeds a dynamic epidemiological threshold, the system automatically triggers a population-level outbreak early warning, enabling proactive disease containment days ahead of traditional passive reporting.")
    ]
    
    for title, desc in nov_items:
        p_item = c_nov.add_paragraph()
        r_t = p_item.add_run(title)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(43, 108, 176)
        r_d = p_item.add_run(desc)
        r_d.font.color.rgb = RGBColor(45, 55, 72)
        p_item.paragraph_format.space_after = Pt(6)
        
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # Section 1.f: Prior Art
    # -------------------------------------------------------------------------
    t_pa = doc.add_table(rows=1, cols=1)
    t_pa.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_pa, color="2B6CB0", sz="6")
    add_header_cell(t_pa.rows[0], "f.  IS THERE ANY PRIOR ART FOR THIS INVENTION? (SEARCH RESULTS & DISTINCTIONS)", fill_hex="2B6CB0", font_size=10.5)
    
    row_pa_content = t_pa.add_row()
    c_pa = row_pa_content.cells[0]
    set_cell_margins(c_pa, top=120, bottom=120, left=160, right=160)
    
    prior_arts = [
        ("1. Haladjian et al. (2018) - 'A Wearable Sensor System for Lameness Detection in Dairy Cattle', Multimodal Tech. & Interaction, 2(2), 27:",
         "Discloses a wearable collar/hoof IMU sensor for lameness detection. Distinction: Requires dedicated wearable sensing hardware; restricted exclusively to gait/lameness; does not disclose optical QR data ingestion, covariance-aware composite multi-signal scoring (CHDI), confidence abstention, veterinarian feedback retraining, or regional multi-farm epidemiological aggregation."),
        
        ("2. Suchak et al. (2026) - 'IoT-Based Smart Cattle Health Monitoring System Using Machine Learning for Real-Time Anomaly Detection', LNNS, Vol. 1463, pp. 1-12:",
         "Discloses IoT sensor hardware and machine learning anomaly scoring. Distinction: Fully reliant on physical IoT sensor hardware on the cattle; does not provide a sensor-optional/manual optical workflow, personalized covariance-aware CHDI formulation, confidence-aware abstention filter, or closed-loop clinical active learning."),
        
        ("3. Kasuga & Kasuga (2017) - JP6203238B2 ('Livestock Management System'):",
         "Discloses QR/barcodes attached to livestock for database identification via mobile phone. Distinction: Merely provides database lookups and manual record association; fails to disclose automated AI baseline forecasting, covariance anomaly scoring, confidence abstention, or regional epidemiological outbreak clustering."),
        
        ("4. Guice et al. (2002) - US20020010390A1 ('Method and System for Monitoring the Health and Status of Livestock'):",
         "Discloses implanted and wireless wearable sensors for cattle vitals. Distinction: Relies exclusively on high-cost implanted/body-borne electronic sensors; does not provide an optical/manual-first scoring architecture, CHDI metric, or veterinarian-in-the-loop retraining."),
        
        ("5. Beckham et al. (2022) - US11243976B2 ('System and Method for Monitoring and Analyzing Animal Related Data'):",
         "Discloses aggregating animal data and evaluating baselines. Distinction: Broad centralized data platform; fails to teach regularized covariance-aware multivariate distance scoring, dynamic sample-bounded abstention, or veterinarian active learning triage loops."),
        
        ("6. Subramanian et al. (2024) - WO2024009326A1 ('IoT-Based Cattle Health and Heat Monitoring System'):",
         "Discloses wearable collar units measuring activity, rumination, and temperature for heat/health alerts. Distinction: Hardware-dependent collar requirement; lacks optical-first sensor-optional pipeline, regularized CHDI formulation, or regional multi-farm correlation analysis."),
        
        ("7. Mindel & Cohen (2025) - US12266142B2 ('Monitoring Livestock in an Agricultural Pen'):",
         "Discloses fixed pen camera arrays observing cattle tags and estimating wellbeing. Distinction: Relies on expensive installed multi-camera infrastructure and computer vision pen tracking; does not provide asynchronous multi-rate farmer-logged health scoring, confidence-based abstention, or clinical active learning."),
        
        ("8. Chinese Patent Application CN121148662A (2025) - 'Method for Identifying Dairy Cow Behavior Based on a Six-Axis Inertial Sensor':",
         "Discloses 6-axis inertial sensors on collars for individual behavior baselines and threshold alerts. Distinction: Strict dependency on body-worn motion sensors; lacks sensor-optional optical input, covariance multi-signal CHDI scoring, clinical override tracking, or regional cluster alerting.")
    ]
    
    for title, desc in prior_arts:
        p_item = c_pa.add_paragraph()
        r_t = p_item.add_run(title)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(45, 55, 72)
        p_item.add_run("\n" + desc).font.color.rgb = RGBColor(74, 85, 104)
        p_item.paragraph_format.space_after = Pt(6)
        
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # Section 1.g: General Overview & Keywords
    # -------------------------------------------------------------------------
    t_gov = doc.add_table(rows=1, cols=1)
    t_gov.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_gov, color="2B6CB0", sz="6")
    add_header_cell(t_gov.rows[0], "g.  GENERAL OVERVIEW OF THE INVENTION, INCLUDING SPECIFIC KEYWORDS AND PHRASES", fill_hex="2B6CB0", font_size=10.5)
    
    row_gov_content = t_gov.add_row()
    c_gov = row_gov_content.cells[0]
    set_cell_margins(c_gov, top=120, bottom=120, left=160, right=160)
    p_ov = c_gov.paragraphs[0]
    p_ov.add_run("The present invention relates to a system, apparatus, and computer-implemented method for intelligent livestock health surveillance and clinical management. Each animal is fitted with a low-cost, weather-resistant optical machine-readable identifier (QR code token) mapped to a unique secure cryptographic database record. The system accepts multi-source, asynchronous health logs including daily milk yield, feed intake, physical activity scores, periodic weight logs, and optical scan timestamps—without requiring expensive, failure-prone wearable IoT sensor arrays.\n\n"
                 "A cloud computing analytics engine establishes an individual, non-stationary physiological baseline for each animal from its own historical time-series entries once a minimum data threshold is satisfied. When new logs are received, the system calculates a multivariate deviation from the baseline using a regularized covariance-aware metric (Composite Health Deviation Index - CHDI), accounting for physiological correlation among parameters. To prevent false alarms, a confidence-aware abstention filter withholds automated verdicts during formative data periods or ill-conditioned covariance states.\n\n"
                 "Animals entering 'Watch' or 'At-Risk' bands automatically trigger veterinary triage cases with dual-tier explainable feature contributions. Veterinarian clinical confirmations or overrides are archived as ground truth to periodically retrain a secondary supervised classifier. Simultaneously, individual anomalies are geographically aggregated across discrete farms within spatial-temporal clusters to provide early-warning epidemiological outbreak detection for veterinary authorities and dairy cooperatives.")
    
    p_kw = c_gov.add_paragraph()
    p_kw.add_run("\nSpecific Keywords and Technical Phrases:\n").bold = True
    keywords = [
        "Optical Machine-Readable Animal Identification", "Sensor-Independent Precision Livestock Farming",
        "Personalized Non-Stationary Physiological Baseline", "Composite Health Deviation Index (CHDI)",
        "Regularized Mahalanobis Distance Metric", "Confidence-Aware Decision Abstention Gate",
        "Matrix Condition Number Verification", "Two-Tier Explainable AI (XAI) in Animal Health",
        "Veterinarian-in-the-Loop Active Learning", "Spatio-Temporal Outbreak Cluster Aggregation",
        "Asynchronous Multi-Rate Signal Normalization", "Smallholder Dairy Farm Health Surveillance"
    ]
    p_kw.add_run(" • " + "\n • ".join(keywords))
    
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # Section 1.h: How Invention is More Beneficial or Feasible
    # -------------------------------------------------------------------------
    t_ben = doc.add_table(rows=1, cols=1)
    t_ben.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_ben, color="2B6CB0", sz="6")
    add_header_cell(t_ben.rows[0], "h.  HOW THE INVENTION IS MORE BENEFICIAL OR FEASIBLE OVER THE PRIOR ART", fill_hex="2B6CB0", font_size=10.5)
    
    row_ben_content = t_ben.add_row()
    c_ben = row_ben_content.cells[0]
    set_cell_margins(c_ben, top=120, bottom=120, left=160, right=160)
    
    benefits = [
        ("1. Total Elimination of Wearable Hardware Cost Barrier:",
         "Prior IoT monitoring systems incur capital costs of $80-$150 per animal plus replacement costs for lost/damaged tags, completely pricing out smallholder farmers. The present invention utilizes durable optical QR tokens costing under $0.50, achieving zero capital barrier while remaining fully compatible with IoT sensors if available."),
        
        ("2. Robustness to Sparse, Irregular, and Asynchronous Data:",
         "Unlike sensor-centric systems requiring continuous high-frequency telemetry, the present system features an asynchronous multi-rate normalization engine that handles disparate logging cadences (e.g., milk yield logged twice daily, feed daily, weight weekly) through decay-weighted temporal interpolation."),
        
        ("3. Eliminates Breed/Parity Calibration Biases via Self-Baselines:",
         "Prior art relies on population averages that fail on diverse indigenous cattle breeds (e.g., Gir, Sahiwal, Murrah buffaloes). The present invention evaluates deviations strictly against the animal's own established trajectory."),
        
        ("4. Drastic Reduction of False Alarms via Mathematical Abstention:",
         "By explicitly enforcing matrix condition checks and minimum sample bounds, the system refuses to issue speculative verdicts during early onboarding, preserving farmer trust and preventing unnecessary antibiotic/veterinary expenses."),
        
        ("5. Continuous Autonomous Field Adaptation via Clinical Active Learning:",
         "Unlike static rule-based systems, every veterinary confirmation or diagnostic override acts as a labeled clinical datum that progressively refines the model's accuracy on regional disease presentations."),
        
        ("6. Multi-Farm Epidemiological Protection (Village / Cluster Level):",
         "Extends individual cattle records into a distributed early-warning radar for contagious livestock diseases (e.g., Foot-and-Mouth Disease, Lumpy Skin Disease), notifying state authorities days before formal clinical outbreaks are declared.")
    ]
    
    for title, desc in benefits:
        p_item = c_ben.add_paragraph()
        r_t = p_item.add_run(title)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(43, 108, 176)
        p_item.add_run("\n" + desc).font.color.rgb = RGBColor(45, 55, 72)
        p_item.paragraph_format.space_after = Pt(6)
        
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # Section 1.i: Detailed Explanation of the Invention
    # -------------------------------------------------------------------------
    t_det = doc.add_table(rows=1, cols=1)
    t_det.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_det, color="2B6CB0", sz="6")
    add_header_cell(t_det.rows[0], "i.  DETAILED EXPLANATION OF THE INVENTION (SYSTEM ARCHITECTURE, FORMULATION & FLOW)", fill_hex="2B6CB0", font_size=10.5)
    
    row_det_content = t_det.add_row()
    c_det = row_det_content.cells[0]
    set_cell_margins(c_det, top=120, bottom=120, left=160, right=160)
    
    p = c_det.paragraphs[0]
    p.add_run("1. Technical Architecture & System Modules:\n").bold = True
    p.add_run("The complete system comprises ten interoperating hardware-interfaced modules configured across an optical acquisition tier, a mobile client tier, a cloud processing cluster, and multi-role user terminals:\n\n")
    
    modules = [
        ("Module 1 - Cattle Identification & Optical Token Registration (102, 202):",
         "Captures static biometric metadata (tag ID, breed, date of birth/parity, purpose), assigns a cryptographically salted UUID, and renders a high-density, weather-resistant 2D Quick Response (QR) matrix token. Derives an age-group physiological category (calf/heifer/lactating adult/dry/senior) and initializes the health state in an ABSTAIN flag."),
        
        ("Module 2 - Asynchronous Multi-Signal Data Ingestion & Normalizer (204, 402):",
         "Ingests time-stamped multi-signal inputs: body weight w(t), daily feed intake f(t), observed physical activity score a(t), milking volume m(t), and optical scan intervals s(t). Asynchronous logging cadences are reconciled via an exponential time-decay interpolation filter to construct an aligned observation vector x(t) = [w(t), f(t), a(t), m(t), s(t)]^T."),
        
        ("Module 3 - Personalized Rolling Baseline Generator (404):",
         "Computes an individualized rolling baseline once a sample threshold N >= N_min is achieved. Constructs an expected mean vector μ = E[x] over an observation window W (e.g., past 14-30 days) and an empirical covariance matrix Σ = Cov(x) reflecting the animal's natural physiological variance."),
        
        ("Module 4 - Regularized Covariance-Aware CHDI Scoring Engine (406):",
         "Computes the Composite Health Deviation Index (CHDI). To guarantee numerical stability against multicollinear health signals, the empirical covariance matrix is regularized via Tikhonov shrinkage: Σ_reg = Σ + λ * I, where λ > 0 is a ridge regularization parameter. The Mahalanobis deviation distance is computed as:\n"
         "      D_M(x) = sqrt( (x - μ)^T * (Σ_reg)^(-1) * (x - μ) )\n"
         "The composite health score S_CHDI is then mapped to an intuitive bounded scale [0, 100]:\n"
         "      S_CHDI = 100 * exp( - D_M / τ )\n"
         "where τ is a calibrated biological dispersion scale factor. Health status bands are assigned: Normal (S >= 80), Watch (60 <= S < 80), and At-Risk (S < 60)."),
        
        ("Module 5 - Confidence-Aware Matrix Condition Abstention Gate (408):",
         "Directly enforces reliability through three conditional gates: (i) Sample count gate: if N < N_min, status = ABSTAIN (Reason: Formative Baseline); (ii) Covariance condition gate: if condition number cond(Σ) > κ_max, status = ABSTAIN (Reason: Ill-conditioned signal variance); (iii) Critical vital absence: if key parameter (feed or milk) is missing beyond tolerance window, score is withheld."),
        
        ("Module 6 - Two-Tier Explainability & Feature Attribution Engine (410):",
         "Performs dynamic feature decomposition of the deviation distance D_M into constituent marginal contributions: C_i = |x_i - μ_i| * |(Σ_reg^(-1) * (x - μ))_i|. Generates (a) plain-language alerts for the farmer mobile UI highlighting the single dominant clinical factor, and (b) complete multidimensional radar breakdowns for the veterinarian terminal."),
        
        ("Module 7 - Automated Veterinary Triage & Case Routing Module (304):",
         "When an animal enters 'Watch' or 'At-Risk' bands, a clinical incident record is generated and dispatched via geo-spatial routing to the licensed veterinarian assigned to the local veterinary dispensary/cluster. Attaches historical signal trajectories, explainability vectors, and previous treatment history."),
        
        ("Module 8 - Clinical Active Learning & Classifier Retraining Pipeline (412, 508):",
         "The attending veterinarian records clinical examination findings, definitive diagnosis, administered treatments, and inputs a binary adjudication label: CONFIRM (True Anomaly) or OVERRIDE (False Alarm / Contextual deviation like estrus or weather change). Verified records are stored in a ground-truth registry. A background retraining service periodically re-fits a supervised Gradient Boosted / Random Forest classifier to continuously refine anomaly detection thresholds."),
        
        ("Module 9 - Spatial-Temporal Regional Outbreak Aggregation Engine (414):",
         "Continuously tracks geo-coded health anomalies within sliding spatial clusters of radius R (e.g., 5-10 km radius or GeoHash grid) and temporal window ΔT (e.g., 48-72 hours). Calculates Cluster Anomaly Index: CAI = (Σ At-Risk Animals in Cluster) / (Total Registered Herd in Cluster). When CAI >= Θ_threshold and spans >= M distinct farm holdings, an emergency regional outbreak alert is triggered to veterinary department officials and dairy cooperatives."),
        
        ("Module 10 - Role-Based Telecommunication & Notification Gateway (300):",
         "Enforces cryptographically isolated role-based access control (Farmer, Veterinarian, System Administrator) with multi-channel push notification, SMS dispatch, and offline sync caching.")
    ]
    
    for title, desc in modules:
        p_m = c_det.add_paragraph()
        r_t = p_m.add_run(title)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(43, 108, 176)
        p_m.add_run("\n" + desc).font.color.rgb = RGBColor(45, 55, 72)
        p_m.paragraph_format.space_after = Pt(6)
        
    p_flow = c_det.add_paragraph()
    p_flow.add_run("\n2. End-to-End Operational Lifecycle:\n").bold = True
    lifecycle_steps = [
        "1. Registration & Token Attachment: Farmer enters cattle vitals; system issues QR token attached to animal's collar or ear tag; initializes record in ABSTAIN state.",
        "2. Routine Optical Scanning & Data Capture: Farmer scans tag using mobile camera and inputs daily milk volume and feed intake; activity scores auto-computed from grazing/milking interval.",
        "3. Baseline Formation: Upon accumulating N >= 7 valid entries, rolling mean vector μ and covariance matrix Σ are established.",
        "4. Continuous CHDI Evaluation: On each new log, covariance condition is validated; regularized Mahalanobis distance D_M is calculated; score S_CHDI mapped.",
        "5. Automated Incident Escalation: Scores below 60 automatically generate an incident record routed to regional veterinary terminal with explainability decomposition.",
        "6. Clinical Examination & Adjudication: Veterinarian examines animal, performs treatment, and logs formal CONFIRM or OVERRIDE outcome.",
        "7. Active Learning Model Retraining: Model weights periodically update based on verified clinical outcomes.",
        "8. Multi-Farm Epidemiological Surveillance: Outbreak aggregator continuously correlates spatial deviations to prevent widespread disease transmission."
    ]
    for step in lifecycle_steps:
        p_s = c_det.add_paragraph()
        p_s.add_run(step)
        p_s.paragraph_format.space_after = Pt(4)
        
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # Section 1.j: Drawings
    # -------------------------------------------------------------------------
    t_draw = doc.add_table(rows=1, cols=1)
    t_draw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_draw, color="2B6CB0", sz="6")
    add_header_cell(t_draw.rows[0], "j.  PROVIDE DRAWINGS, IF ANY (PATENT SPECIFICATION FIGURES & DETAILED DESCRIPTIONS)", fill_hex="2B6CB0", font_size=10.5)
    
    row_draw_content = t_draw.add_row()
    c_draw = row_draw_content.cells[0]
    set_cell_margins(c_draw, top=140, bottom=140, left=160, right=160)
    
    p = c_draw.paragraphs[0]
    p.add_run("The following five formal patent drawings illustrate the architectural embodiments, mathematical logic, operational flows, and epidemiological clustering mechanisms of the present invention:\n\n").bold = True
    
    figures_info = [
        ("FIGURE 1: SYSTEM HARDWARE AND LOGICAL ARCHITECTURE",
         "figure1_system_architecture.png",
         "Figure 1 is a block schematic diagram showing the complete hardware and logical architecture of the system. "
         "Physical tier (100) comprises an animal ear tag/collar bearing an optical QR identifier (102), a mobile optical camera sensor (104), a farmer manual entry interface (106), and an optional IoT sensor array (108). "
         "Edge/Client app tier (200) comprises an optical token decoder (202), multi-signal validator (204), offline buffer (206), and secure API dispatcher (208). "
         "User terminal interfaces (300) include farmer dashboard (302), veterinarian triage portal (304), admin outbreak monitor (306), and push/SMS alert dispatch (308). "
         "Central cloud analytics engine (400) comprises asynchronous normalizer (402), personalized baseline generator (404), regularized CHDI calculator (406), confidence abstention gate (408), two-tier explainability module (410), active classifier retraining pipeline (412), and regional outbreak aggregator (414). "
         "Secure storage tier (500) houses cattle registry (502), physiological DB (504), baseline matrices (506), clinical cases (508), and spatial outbreak registry (510)."),
        
        ("FIGURE 2: END-TO-END OPERATIONAL WORKFLOW PIPELINE",
         "figure2_operational_workflow.png",
         "Figure 2 is a comprehensive sequence flowchart illustrating the end-to-end operational lifecycle: "
         "Step 1 (Animal registration and optical token issuance); Step 2 (Asynchronous multi-signal logging via mobile optical scan or entry); "
         "Step 3 (Rolling baseline construction upon reaching minimum samples N >= N_min); Step 4 (CHDI calculation and confidence-aware abstention gating); "
         "Step 5 (Two-tier feature explainability and automated vet case routing); Step 6 (Veterinary clinical diagnosis and binary confirm/override adjudication); "
         "Step 7 (Active learning supervised classifier retraining); and Step 8 (Spatio-temporal multi-farm outbreak aggregation and emergency alert distribution)."),
        
        ("FIGURE 3: CHDI COMPUTATION & CONFIDENCE-AWARE ABSTENTION LOGIC FLOWCHART",
         "figure3_chdi_abstention_logic.png",
         "Figure 3 is a detailed mathematical decision flowchart of the CHDI scoring engine and confidence-aware abstention gate. "
         "Illustrates sample verification gate (N >= N_min), routing to ABSTAIN output on failure; temporal alignment and imputation for sparse metrics; "
         "covariance condition check (cond(Σ) > κ_max), triggering shrinkage regularization (Σ_reg = Σ + λ*I); "
         "computation of regularized Mahalanobis distance D_M and bounded score S_CHDI; and final categorization into Normal (S >= 80), Watch (60 <= S < 80), and At-Risk (S < 60) clinical bands."),
        
        ("FIGURE 4: CLOSED-LOOP ACTIVE LEARNING & CLINICAL RETRAINING ARCHITECTURE",
         "figure4_vet_active_learning.png",
         "Figure 4 illustrates the clinical closed-loop active learning architecture. "
         "When an At-Risk/Watch incident occurs, it is dispatched to the assigned veterinarian terminal based on geographic proximity. "
         "The veterinarian inputs clinical findings and explicitly submits a Confirm (True Positive) or Override (False Positive) label. "
         "The verified clinical outcome is stored in a curated ground-truth repository. "
         "A batch retraining engine periodically updates the supervised classifier weights, hot-swapping updated parameters to the active inference engine without service interruption."),
        
        ("FIGURE 5: SPATIO-TEMPORAL REGIONAL OUTBREAK AGGREGATION PIPELINE",
         "figure5_regional_outbreak_engine.png",
         "Figure 5 illustrates the spatial-temporal regional outbreak aggregation engine. "
         "Distributed cattle health deviations across discrete local farm holdings (Farm A, Farm B, Farm C) within a common spatial radius or GeoHash cell are aggregated over a sliding temporal window ΔT (e.g., 72 hours). "
         "The system evaluates the Cluster Anomaly Index (CAI). If CAI exceeds dynamic threshold Θ, a high-priority regional outbreak emergency alert is broadcast to government animal husbandry officials, regional veterinarians, and dairy cooperatives.")
    ]
    
    for title, img_name, desc in figures_info:
        img_path = os.path.join(fig_dir, img_name)
        
        p_fig_title = c_draw.add_paragraph()
        r_ft = p_fig_title.add_run(title)
        r_ft.bold = True
        r_ft.font.size = Pt(10)
        r_ft.font.color.rgb = RGBColor(26, 54, 93)
        p_fig_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        if os.path.exists(img_path):
            p_img = c_draw.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(6.2))
            
        p_desc = c_draw.add_paragraph()
        r_fd = p_desc.add_run("Description: " + desc)
        r_fd.font.size = Pt(8.5)
        r_fd.font.color.rgb = RGBColor(74, 85, 104)
        p_desc.paragraph_format.space_after = Pt(14)
        
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # SECTION 2: Disclosure
    # -------------------------------------------------------------------------
    t_sec2 = doc.add_table(rows=1, cols=1)
    t_sec2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sec2, color="1A365D", sz="8")
    add_header_cell(t_sec2.rows[0], "2.  DISCLOSURE", fill_hex="1A365D", font_size=11)
    
    t_disc = doc.add_table(rows=0, cols=2)
    t_disc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_disc, color="CBD5E0", sz="4")
    
    add_two_col_row(t_disc, "a.  Has the invention ever been shown or used in public?", "☐ Yes          ☒ No")
    add_two_col_row(t_disc, "If yes, Where / When", "Where: ________________________          When: ________________________")
    add_two_col_row(t_disc, "b.  Was any Confidentiality Agreement signed regarding the invention?", "☐ Yes          ☒ No")
    add_two_col_row(t_disc, "c.  Has this invention been publicly disclosed (e.g., paper presentation, journal publication)?", "☐ Yes          ☒ No\n(Note: Immediate filing recommended prior to any paper presentation or public symposium)")
    
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # SECTION 3: Foreign Patent Protection
    # -------------------------------------------------------------------------
    t_sec3 = doc.add_table(rows=1, cols=1)
    t_sec3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sec3, color="1A365D", sz="8")
    add_header_cell(t_sec3.rows[0], "3.  FOREIGN PATENT PROTECTION", fill_hex="1A365D", font_size=11)
    
    t_for = doc.add_table(rows=0, cols=2)
    t_for.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_for, color="CBD5E0", sz="4")
    add_two_col_row(t_for, "a.  Do you intend to pursue International / PCT Patent protection?", "☐ Yes          ☒ No\n(Presently targeting Indian Patent Application via Sona College CIPR; PCT filing to be evaluated based on commercial licensing interest)")
    
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # SECTION 4: Funding and Sponsorship
    # -------------------------------------------------------------------------
    t_sec4 = doc.add_table(rows=1, cols=1)
    t_sec4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sec4, color="1A365D", sz="8")
    add_header_cell(t_sec4.rows[0], "4.  FUNDING AND SPONSORSHIP", fill_hex="1A365D", font_size=11)
    
    t_fund = doc.add_table(rows=0, cols=2)
    t_fund.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_fund, color="CBD5E0", sz="4")
    
    add_two_col_row(t_fund, "1. Was this invention developed with external funding?", "No (Developed as Institutional Final-Year B.Tech Capstone Project / Sona Research Initiative)")
    add_two_col_row(t_fund, "2. Funding Agency / Sponsor", "N/A (Institutional Research Facilities, Sona College of Technology)")
    add_two_col_row(t_fund, "3. Grant or Contract number", "N/A")
    add_two_col_row(t_fund, "4. Principal Investigator (PI) / Faculty Project Supervisor", "[Faculty Guide Name - e.g., Dr./Prof. Name],\nDesignation: Assistant Professor / Associate Professor / Professor,\nDepartment of Artificial Intelligence and Data Science, Sona College of Technology, Salem")
    add_two_col_row(t_fund, "5. Are there any third-party obligations (collaborations, industry partners)?", "No")
    
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # SECTION 5: Commercial Potential
    # -------------------------------------------------------------------------
    t_sec5 = doc.add_table(rows=1, cols=1)
    t_sec5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sec5, color="1A365D", sz="8")
    add_header_cell(t_sec5.rows[0], "5.  COMMERCIAL POTENTIAL & INDUSTRIAL APPLICABILITY", fill_hex="1A365D", font_size=11)
    
    t_com = doc.add_table(rows=0, cols=2)
    t_com.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_com, color="CBD5E0", sz="4")
    
    add_two_col_row(t_com, "1. Potential Applications / Industries",
                    "• Smallholder dairy farming and rural dairy cooperatives (e.g., Aavin, Amul federations).\n"
                    "• Commercial dairy herd management software and veterinary telemedicine portals.\n"
                    "• Livestock micro-insurance underwriters (loss prevention & automated health verification).\n"
                    "• Government Animal Husbandry Departments (epidemiological outbreak surveillance and disease containment programs).\n"
                    "• Agricultural extension services and rural veterinary dispensaries.")
    
    add_two_col_row(t_com, "2. Known Competing Technologies",
                    "• Wearable IoT sensor devices (ear-mounted RFID/BLE tags, collar accelerometers, rumen boluses).\n"
                    "• General-purpose herd management databases lacking predictive AI anomaly detection.\n"
                    "• Static manual paper records and basic spreadsheet logging systems.")
    
    add_two_col_row(t_com, "3. Companies / Organizations for Technology Licensing",
                    "• National Dairy Development Board (NDDB) and State Milk Marketing Federations.\n"
                    "• Agritech enterprise startups (Stellapps Technologies, MooFarm, Prompt Dairy Tech).\n"
                    "• Livestock insurance companies (Agriculture Insurance Company of India, IFFCO-Tokio, HDFC ERGO).\n"
                    "• Ministry of Fisheries, Animal Husbandry & Dairying (DAHD), Govt. of India.")
    
    doc.add_paragraph()
    
    # -------------------------------------------------------------------------
    # SECTION 6: Inventorship Declaration
    # -------------------------------------------------------------------------
    t_sec6 = doc.add_table(rows=1, cols=1)
    t_sec6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sec6, color="1A365D", sz="8")
    add_header_cell(t_sec6.rows[0], "6.  INVENTORSHIP DECLARATION & INSTITUTIONAL ASSIGNMENT", fill_hex="1A365D", font_size=11)
    
    row_dec_text = t_sec6.add_row()
    c_dec = row_dec_text.cells[0]
    set_cell_margins(c_dec, top=100, bottom=100, left=140, right=140)
    p_dec = c_dec.paragraphs[0]
    p_dec.add_run("I/we declare that the information provided in this form is accurate, true, and complete to the best of my/our knowledge. I/we hereby agree to assign all rights, title, and interest in this invention to Sona College of Technology, Salem, in accordance with the institutional Intellectual Property Rights (IPR) policy.\n").italic = True
    
    doc.add_paragraph()
    
    # Inventors Table - 4 Inventors (3 Students + 1 Faculty Guide)
    t_inv = doc.add_table(rows=5, cols=4)
    t_inv.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_inv, color="CBD5E0", sz="4")
    
    headers_inv = ["Inventor 1", "Inventor 2", "Inventor 3", "Inventor 4 (Faculty Guide)"]
    for idx, h in enumerate(headers_inv):
        cell = t_inv.rows[0].cells[idx]
        set_cell_background(cell, "2B6CB0" if idx < 3 else "1A365D")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    inv_data = [
        ("a. Full Name",
         ["Sabari Karthick A", "Sivanarasimman S", "Sujeeth Y R", "[Faculty Guide / Mentor Name]"]),
        ("b. Designation & Department",
         ["Final-Year Student,\nArtificial Intelligence and Data Science",
          "Final-Year Student,\nArtificial Intelligence and Data Science",
          "Final-Year Student,\nArtificial Intelligence and Data Science",
          "[Designation - e.g. Assistant Professor],\nDepartment of Artificial Intelligence and Data Science"]),
        ("c. Signature",
         ["_______________________", "_______________________", "_______________________", "_______________________"]),
        ("d. Date",
         ["_______________________", "_______________________", "_______________________", "_______________________"])
    ]
    
    for r_idx, (label, vals) in enumerate(inv_data):
        row = t_inv.rows[r_idx + 1]
        for c_idx, val in enumerate(vals):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            if r_idx == 0:
                p.add_run(f"{label}: ").bold = True
                p.add_run(val)
            elif r_idx == 1:
                p.add_run(f"{label}:\n").bold = True
                p.add_run(val)
            else:
                p.add_run(f"{label}:\n").bold = True
                p.add_run(val)
            p.runs[0].font.size = Pt(8.5)
            if len(p.runs) > 1:
                p.runs[1].font.size = Pt(8.5)
                
    doc.add_paragraph()
    
    # Authorized Signatory Table
    t_auth = doc.add_table(rows=5, cols=2)
    t_auth.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_auth, color="CBD5E0", sz="4")
    
    auth_data = [
        ("Institutional Authorization", "Department Endorsement & IPR Cell Recommendation"),
        ("Authorized Person - Name", "Dr. [Head of Department / Dean R&D Name]"),
        ("Designation", "Head of Department (AI & DS) / Dean (R&D) / IPR Coordinator, Sona College of Technology"),
        ("Signature", "________________________________________________________"),
        ("Date", "________________________________________________________")
    ]
    for idx, (lbl, val) in enumerate(auth_data):
        row = t_auth.rows[idx]
        c0 = row.cells[0]; c1 = row.cells[1]
        c0.width = Inches(2.2); c1.width = Inches(4.6)
        set_cell_margins(c0); set_cell_margins(c1)
        if idx == 0:
            set_cell_background(c0, "1A365D"); set_cell_background(c1, "1A365D")
            r0 = c0.paragraphs[0].add_run(lbl); r0.bold = True; r0.font.color.rgb = RGBColor(255, 255, 255)
            r1 = c1.paragraphs[0].add_run(val); r1.bold = True; r1.font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_background(c0, "F7FAFC")
            r0 = c0.paragraphs[0].add_run(lbl); r0.bold = True; r0.font.size = Pt(9)
            r1 = c1.paragraphs[0].add_run(val); r1.font.size = Pt(9)
            
    doc.add_paragraph()
    
    # Office Use Only Table
    t_off = doc.add_table(rows=4, cols=2)
    t_off.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_off, color="CBD5E0", sz="4")
    
    off_data = [
        ("FOR CIPR / PATENT CELL OFFICE USE ONLY", ""),
        ("Disclosure Number", "SCT/CIPR/IDF/2026/______"),
        ("Date Received", "____ / ____ / 2026"),
        ("Next Steps / Recommendation", "☐ Approved for Prior Art Search   ☐ Recommended for Provisional Filing   ☐ Recommended for Complete Specification   ☐ Revision Required")
    ]
    for idx, (lbl, val) in enumerate(off_data):
        row = t_off.rows[idx]
        c0 = row.cells[0]; c1 = row.cells[1]
        c0.width = Inches(2.2); c1.width = Inches(4.6)
        set_cell_margins(c0); set_cell_margins(c1)
        if idx == 0:
            set_cell_background(c0, "4A5568"); set_cell_background(c1, "4A5568")
            r0 = c0.paragraphs[0].add_run(lbl); r0.bold = True; r0.font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_background(c0, "EDF2F7")
            r0 = c0.paragraphs[0].add_run(lbl); r0.bold = True; r0.font.size = Pt(9)
            r1 = c1.paragraphs[0].add_run(val); r1.font.size = Pt(8.5)
            
    # Save the document
    out_path = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Revised.docx"
    doc.save(out_path)
    print("Successfully built document at:", out_path)

if __name__ == "__main__":
    build_document()
