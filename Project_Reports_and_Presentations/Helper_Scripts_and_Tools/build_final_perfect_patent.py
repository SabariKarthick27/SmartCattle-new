import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def apply_tnr_black(run, font_size=11, bold=False, italic=False):
    """Enforces Times New Roman font and pure black color on a run."""
    run.font.name = "Times New Roman"
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0) # 100% PURE BLACK ONLY
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(r'<w:rFonts %s w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>' % nsdecls('w'))
    rPr.append(rFonts)

def clear_cell_and_get_first_p(cell):
    p_first = cell.paragraphs[0]
    p_first.text = ""
    for p in cell.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    return p_first

def add_black_p(cell, text="", font_size=11, bold=False, italic=False, space_before=0, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, indent=0):
    p = cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    if text:
        r = p.add_run(text)
        apply_tnr_black(r, font_size=font_size, bold=bold, italic=italic)
    return p

def main():
    backup_path = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent-1-backup.docx"
    eq_dir = r"c:\Project\SmartCattle new\patent_figures\equations"
    pro_fig_path = r"c:\Project\SmartCattle new\patent_figures\figure_master_pro_no_numbers.png"

    doc = Document(backup_path)
    print("Loaded original tabular document.")

    # 1. Normal style to Times New Roman, Black
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)
    style.font.color.rgb = RGBColor(0, 0, 0)

    # -------------------------------------------------------------------------
    # Document Title (Paragraph 0)
    # -------------------------------------------------------------------------
    p0 = doc.paragraphs[0]
    p0.text = ""
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = p0.add_run("INVENTION DISCLOSURE FORM")
    apply_tnr_black(r0, font_size=13, bold=True)

    # -------------------------------------------------------------------------
    # Table 0: Section 1 Header
    # -------------------------------------------------------------------------
    p = doc.tables[0].rows[0].cells[0].paragraphs[0]
    p.text = ""
    r = p.add_run("1.  Details of the Invention")
    apply_tnr_black(r, font_size=12, bold=True)

    # -------------------------------------------------------------------------
    # Table 1: Title of the invention
    # -------------------------------------------------------------------------
    doc.tables[1].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[1].rows[0].cells[0].paragraphs[0].add_run("a.  Title of the invention"), font_size=11, bold=True)

    p = clear_cell_and_get_first_p(doc.tables[1].rows[0].cells[1])
    r1 = p.add_run("A SYSTEM AND COMPUTER-IMPLEMENTED METHOD FOR SENSOR-INDEPENDENT LIVESTOCK HEALTH MONITORING USING OPTICAL IDENTIFIERS AND COMPOSITE MULTIVARIATE DEVIATION ANALYSIS\n\n")
    apply_tnr_black(r1, font_size=11, bold=True)
    r2 = p.add_run("(Also referred to as: QR-Based Cattle Management System with AI-Driven Health Monitoring and Composite Health Deviation Index - CHDI)")
    apply_tnr_black(r2, font_size=10, italic=True)

    # -------------------------------------------------------------------------
    # Table 2: Field of the invention
    # -------------------------------------------------------------------------
    doc.tables[2].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[2].rows[0].cells[0].paragraphs[0].add_run("b.  Field of the invention"), font_size=11, bold=True)

    p = clear_cell_and_get_first_p(doc.tables[2].rows[0].cells[1])
    r = p.add_run("Precision Livestock Farming (Animal Husbandry Technology), Artificial Intelligence, Machine Learning, and Veterinary Tele-Informatics\n"
                  "(International Patent Classification [IPC]: A01K 29/00, G16H 50/20, G06N 20/00)")
    apply_tnr_black(r, font_size=11)

    # -------------------------------------------------------------------------
    # Table 3: Stage of development
    # -------------------------------------------------------------------------
    p = clear_cell_and_get_first_p(doc.tables[3].rows[0].cells[0])
    r = p.add_run("c.  Stage of development\n\n☐ Idea only        ☐ Proof of concept        ☒ Prototype        ☒ Tested        ☐ In use/deployed\n"
                  "(Functional software prototype integrated with mobile optical camera scanner, cloud analytics API, and clinical vet portal evaluated on field cattle datasets)")
    apply_tnr_black(r, font_size=11)

    # -------------------------------------------------------------------------
    # Table 4: Nature of the invention (BOTH Product and Process checked for CRI defense)
    # -------------------------------------------------------------------------
    p = clear_cell_and_get_first_p(doc.tables[4].rows[0].cells[0])
    r = p.add_run("d.  Is the invention based on\n\n☒ Product        ☒ Process / Method        ☐ Design        ☐ Others\n"
                  "(Product: Integrated multi-tier clinical diagnostic system and optical token platform;\n"
                  "Process/Method: Computer-implemented method for regularized multivariate distance scoring, confidence abstention, and closed-loop clinical active learning)")
    apply_tnr_black(r, font_size=11)

    # -------------------------------------------------------------------------
    # Table 5: Novelty / Invention Summary (NO EXPLICIT COST/DOLLAR MENTIONS)
    # -------------------------------------------------------------------------
    c = doc.tables[5].rows[0].cells[0]
    p = clear_cell_and_get_first_p(c)
    apply_tnr_black(p.add_run("e.  What is/are the Novel/New aspects of the invention? What makes it different from existing solutions?\n"), font_size=11.5, bold=True)

    novelty_intro = (
        "The present invention provides a sensor-independent, AI-driven livestock health monitoring and clinical case management system that replaces dedicated on-animal electronic sensors with durable optical machine-readable identifiers (2D QR code tags) and a multi-stage Composite Health Deviation Index (CHDI) analytical engine. "
        "The principal novel aspects comprise:"
    )
    add_black_p(c, novelty_intro, font_size=10.5, space_after=4)

    novelty_points = [
        ("1. Optical-First, Hardware-Independent Health Ingestion Architecture",
         "The system uniquely pairs an animal-mounted optical identifier (weatherproof 2D QR token) with multi-signal telemetry ingestion from standard mobile devices and milking records, achieving continuous precision health monitoring without requiring dedicated on-animal wearable electronic sensor hardware."),

        ("2. Multi-Stage Longitudinal Baseline Calibration with Sample-Variance Correction",
         "Rather than comparing an animal against generalized population norms or arbitrary static thresholds, the system establishes a personalized rolling baseline for each physiological channel (milk yield, feed intake, rumination/activity, body weight) over a rolling 14-day observation window with Bessel's correction, eliminating breed, lactation-cycle, and seasonal bias."),

        ("3. Tikhonov-Regularized Covariance-Aware Mahalanobis Distance Scoring (CHDI)",
         "The system maps multi-source telemetry into a dimensionless normalized deviation vector and computes a composite Mahalanobis distance weighted by the animal's empirical covariance matrix, stabilized via Tikhonov ridge regularization (λ·I). This reliably detects coupled subclinical anomalies (e.g., concurrent appetite loss and milk yield depression) even under sparse or asynchronous data entry."),

        ("4. Confidence-Aware Decision Abstention Protocol",
         "The invention integrates an analytical confidence metric based on historical observation maturity and empirical matrix condition number (cond(Σ)). When observation history is immature (< 7 days) or the covariance matrix is ill-conditioned, the system suppresses speculative verdicts and explicitly outputs an ABSTAIN state, eliminating onboarding false alarms."),

        ("5. Dual-Tier Explainability & Permutation Feature Attribution",
         "A Leave-One-Covariate-Out (LOCO) permutation attribution engine decomposes multivariate anomaly scores into individual feature contributions, generating plain-language operational summaries for smallholder farmers alongside granular multidimensional radar vectors and clinical trajectory graphs for veterinarians."),

        ("6. Closed-Loop Clinical Active Learning with Feedback-Driven Retraining",
         "When an animal enters an At-Risk band, the system automatically routes an incident ticket to regional veterinary terminals. Attending veterinarian clinical diagnoses and treatment adjudications (CONFIRM vs OVERRIDE) are captured as audited ground-truth labels, automatically retraining a secondary supervised classifier to progressively adapt to regional pathology patterns."),

        ("7. Spatio-Temporal Multi-Farm Epidemiological Outbreak Aggregation",
         "Deviations are cross-aggregated across discrete farm holdings in spatial-temporal clusters (radius R and temporal window ΔT). When cluster anomaly density exceeds a dynamic threshold across multiple independent holdings, a regional outbreak alert is automatically distributed to animal husbandry authorities.")
    ]
    for title, desc in novelty_points:
        add_black_p(c, title, font_size=11, bold=True, space_before=4, space_after=1)
        add_black_p(c, desc, font_size=10.5, space_after=4)

    # -------------------------------------------------------------------------
    # Table 6: Prior Art (Section f)
    # -------------------------------------------------------------------------
    c = doc.tables[6].rows[0].cells[0]
    p = clear_cell_and_get_first_p(c)
    apply_tnr_black(p.add_run("f.  Is there any prior art for this invention?\n"), font_size=11.5, bold=True)

    prior_arts_continuous = [
        ("Haladjian, J.; Haug, J.; Nüske, S.; and Bruegge, B. (2018). “A Wearable Sensor System for Lameness Detection in Dairy Cattle,” Multimodal Technologies and Interaction, 2(2), 27.",
         "This work uses a wearable motion sensor attached to the cow and builds an individual gait model to detect deviations associated with lameness. It is limited to gait/lameness monitoring and requires per-animal wearable hardware; it does not describe QR/manual-data-only operation, a composite multi-signal CHDI score, confidence-aware abstention, veterinarian-feedback retraining, or regional outbreak aggregation."),

        ("Suchak, V.; Rana, H.; Verma, A.; Dubey, N. K.; Jayswal, H. S.; Damodar, D.; and Patel, C. I. (2026). “IoT-Based Smart Cattle Health Monitoring System Using Machine Learning for Real-Time Anomaly Detection,” Lecture Notes in Networks and Systems, Vol. 1463, pp. 1-12.",
         "This work concerns IoT- and machine-learning-based cattle health monitoring. It relies on sensor-derived inputs and does not disclose the proposed QR/sensor-optional workflow, per-animal CHDI formulation with covariance-aware scoring, confidence abstention, or veterinarian-confirmed adaptive retraining."),

        ("Modak et al. (2025). “Internet of Things-Based Health Surveillance Systems for Livestock: A Review of Recent Advances and Challenges,” IET Wireless Sensor Systems.",
         "This review describes the general wearable-livestock-monitoring field, including smart collars, temperature sensors, accelerometers, heart-rate sensors, microcontrollers, cloud platforms, and machine-learning-based alerts. The reviewed systems are predominantly hardware/sensor dependent and do not specifically disclose the proposed QR-linked, manually logged smallholder workflow with CHDI scoring and veterinarian-feedback learning."),

        ("Kasuga, Ryoichi; and Kasuga, Hisashi (2017). “Livestock Management System,” JP6203238B2, published 27 September 2017.",
         "This patent describes QR-code or barcode tags attached to livestock, scanned using a mobile device and matched with a management database for individual identification. It provides identification and manual assessment support, but does not disclose AI-based multi-signal health-deviation scoring, CHDI computation, confidence-aware abstention, or predictive veterinarian case management."),

        ("Guice, David; Pugh, Warren; and Thompson, Noble (2002). “Method and System for Monitoring the Health and Status of Livestock and Other Animals,” US20020010390A1, published 24 January 2002.",
         "This document describes automated livestock-health monitoring using implanted wireless sensor elements that may measure temperature, blood oxygen, activity, vibration, and heart rate. It relies on implanted or wearable sensor hardware and does not disclose QR/manual-data-only operation, the proposed CHDI score, abstention during insufficient-history periods, or veterinarian-feedback retraining."),

        ("Beckham, Tammy; Coats, Matthew; Korslund, John; Colby, Michelle; Wall, James; Biggers, Keith; Berquist, Melissa; Riddle, Austin; Bilnoski, Paul; Overby, Derek; Booker, Graham; and Holmstrom, Lindsey (2022). “System and Method for Monitoring and Analyzing Animal Related Data,” US11243976B2, published 8 February 2022.",
         "This patent aggregates animal-related data, identifies a baseline, and compares collected data with that baseline for animal-management assessment. It is broad and data-platform oriented; it does not specifically describe QR-based smallholder health logging, covariance-aware CHDI scoring, abstention, or veterinarian-confirmed classifier retraining."),

        ("Diao, Shanghua; and Deng, Yingang (2021). “Livestock Health Monitoring Method and Device, Storage Medium and Electronic Equipment,” CN113488175A, published 8 October 2021.",
         "This patent uses an electronic tag containing temperature, acceleration, microphone, heart-rate, and blood-oxygen sensors, and applies a trained health-monitoring model to derive a health index. It depends on dedicated electronic sensing hardware and a pre-trained model rather than a sensor-optional QR/manual-data approach with individualized CHDI baselines and explicit abstention."),

        ("Subramanian, Srinivas; Kamble, Ramdas; Pote, Supriya; Goel, Neeraj; and Sen, Swapna (2024). “IoT-Based Cattle Health and Heat Monitoring System,” WO2024009326A1, published 11 January 2024.",
         "This document describes wearable collar units using sensor data for activity, rumination, temperature, lameness, and health/heat alerts. It requires collar-based hardware and does not disclose a QR/manual-data-only workflow, a covariance-aware CHDI index, or veterinarian-confirmation-driven model retraining."),

        ("Mindel, Anatoly; and Cohen, Yossi (2025). “Monitoring Livestock in an Agricultural Pen,” US12266142B2, published 1 April 2025.",
         "This patent describes camera-based livestock monitoring that can identify animals using visible identifiers such as coloured tags, barcodes, text, or QR codes and estimate wellbeing-related parameters from images. It is principally vision-based and does not disclose manual/QR-linked multi-signal health logging, CHDI scoring, confidence abstention, or a veterinarian-feedback active-learning loop."),

        ("“A Method for Identifying Dairy Cow Behavior Based on a Six-Axis Inertial Sensor” (2025). CN121148662A, published 14 November 2025.",
         "This patent document describes dairy-cow behaviour recognition and early warning using a six-axis inertial sensor, an individual behavioural baseline, deviation analysis, and threshold-based risk scoring. It requires a sensor-equipped ear tag, collar, or neck device; it does not disclose the proposed sensor-optional QR/manual-data platform, the full CHDI workflow, veterinarian case confirmation and override, or regional multi-farm outbreak aggregation.")
    ]

    for title, desc in prior_arts_continuous:
        p_item = c.add_paragraph()
        p_item.paragraph_format.space_before = Pt(4)
        p_item.paragraph_format.space_after = Pt(8)
        r_t = p_item.add_run(title)
        apply_tnr_black(r_t, font_size=10.5, bold=True)
        r_d = p_item.add_run(" " + desc)
        apply_tnr_black(r_d, font_size=10.5, bold=False)

    # -------------------------------------------------------------------------
    # Table 7: General Overview & Keywords
    # -------------------------------------------------------------------------
    c = doc.tables[7].rows[0].cells[0]
    p = clear_cell_and_get_first_p(c)
    apply_tnr_black(p.add_run("g.  General overview of the invention, including specific keywords and phrases:\n"), font_size=11.5, bold=True)

    ov_text = (
        "The present invention relates to an AI-driven cattle health monitoring and clinical case management system that identifies each animal through a durable optical machine-readable token (QR tag) and evaluates health using a Composite Health Deviation Index (CHDI) computed from asynchronous multi-source data (manual farmer logs, mobile optical camera scan timestamps, and optional IoT feeds), without requiring wearable sensors. "
        "The system establishes a personalized rolling baseline for each animal from its own historical records (weight, daily feed intake, observed physical activity, and milk yield) once a minimum sample threshold is attained. "
        "It calculates real-time deviation from that baseline using a regularized covariance-aware Mahalanobis distance metric, mapping the result to a single composite health score (0–100) with an associated confidence metric. "
        "When historical data is sparse or when the empirical covariance matrix is ill-conditioned, the system enforces a confidence-aware abstention mechanism, withholding speculative verdicts to eliminate false alarms. "
        "Cases falling into 'Watch' or 'At-Risk' bands automatically generate clinical incident records routed to licensed regional veterinarians with a two-tier explainability vector (plain-language factors for farmers, multidimensional breakdowns for clinicians). "
        "The veterinarian's clinical confirmation or diagnostic override is captured as audited ground truth to periodically retrain a supervised classifier over time. "
        "Furthermore, individual deviations are geographically aggregated across discrete farm holdings in spatial-temporal clusters to trigger early-warning alerts for multi-farm disease outbreaks."
    )
    add_black_p(c, ov_text, font_size=10.5, space_after=6)

    add_black_p(c, "Specific Keywords and Phrases Pertaining to the Invention:", font_size=10.5, bold=True, space_before=4, space_after=2)
    keywords = [
        "QR-Based Animal Identification",
        "Sensor-Optional Health Monitoring",
        "Personalized Physiological Baseline",
        "Composite Health Deviation Index (CHDI)",
        "Regularized Mahalanobis Distance Metric",
        "Confidence-Aware Decision Abstention Gate",
        "Matrix Condition Number Verification",
        "Leave-One-Covariate-Out (LOCO) Feature Attribution",
        "Dual-Tier Clinical Explainability",
        "Veterinarian-in-the-Loop Active Learning",
        "Diagnostic Override Ground-Truth Logging",
        "Supervised Disease Re-Classification",
        "Spatio-Temporal Regional Outbreak Aggregation",
        "Multi-Farm Epidemiological Surveillance",
        "Smallholder Precision Livestock Farming"
    ]
    for kw in keywords:
        add_black_p(c, "• " + kw, font_size=10, space_after=1, indent=0.2)

    # -------------------------------------------------------------------------
    # Table 8: Advantages / Benefits (NO EXPLICIT COST/DOLLAR MENTIONS)
    # -------------------------------------------------------------------------
    c = doc.tables[8].rows[0].cells[0]
    p = clear_cell_and_get_first_p(c)
    apply_tnr_black(p.add_run("h.  How the invention is more beneficial or feasible over the prior art:\n"), font_size=11.5, bold=True)

    benefits = [
        ("1. Elimination of On-Animal Electronic Hardware Burden (Democratized Access)",
         "Conventional electronic sensor systems (IoT collars, pedometers, boluses) suffer from battery depletion, harsh barn wear-and-tear, physical tag detachment, and high replacement overhead. The proposed invention uses durable passive 2D QR tags and standard mobile camera scanning, removing hardware dependency while ensuring seamless accessibility for smallholder dairy operations."),

        ("2. Personalized Rolling Baseline Rather Than Population Averages",
         "Prior art evaluates animals against generalized breed/herd norms that produce high false-positive rates due to natural variations across age, parity, and lactation cycle. This invention builds a personalized non-stationary baseline strictly from the animal's own longitudinal history, eliminating breed-specific calibration bias."),

        ("3. Regularized Covariance-Aware Multivariate Scoring",
         "Prior systems either monitor a single condition (e.g., lameness) or apply arbitrary static weights to individual metrics. This invention combines all physiological signals into a single CHDI score using a regularized Mahalanobis distance that accounts for the natural covariance structure of health parameters for that specific animal."),

        ("4. Explicit Mathematical Abstention Drastically Reduces False Alarms",
         "Unlike systems that force a speculative classification upon receiving minimal entries, this invention evaluates sample size (N < N_min) and matrix condition number (cond(Σ) > κ_max) to withhold verdicts during formative periods, preserving farmer trust and preventing unnecessary clinical interventions."),

        ("5. Continuous Autonomous Field Adaptation via Clinical Active Learning",
         "Unlike static rule-based systems, every veterinary confirmation or diagnostic override acts as a labeled clinical datum that progressively refines the model's accuracy on regional disease presentations."),

        ("6. Multi-Farm Epidemiological Protection (Village / Cluster Level)",
         "Extends individual cattle records into a distributed early-warning radar for contagious livestock diseases, notifying state authorities days before formal clinical outbreaks are declared.")
    ]
    for title, desc in benefits:
        add_black_p(c, title, font_size=11, bold=True, space_before=4, space_after=1)
        add_black_p(c, desc, font_size=10.5, space_after=4)

    # -------------------------------------------------------------------------
    # Table 9: Detailed Explanation of the Invention (EXACT REPORT FORMULAS)
    # -------------------------------------------------------------------------
    c = doc.tables[9].rows[0].cells[0]
    p = clear_cell_and_get_first_p(c)
    apply_tnr_black(p.add_run("i.  Detailed explanation of the invention (Modules, Mathematical Formulations & Flow):\n"), font_size=11.5, bold=True)

    add_black_p(c, "1. Technical Architectural Modules:", font_size=11, bold=True, space_before=4, space_after=3)

    modules_desc = [
        ("Module 1 - Cattle Identification & Optical Token Registration Module",
         "Captures static biometric identity parameters (tag ID, breed, gender, date of birth, parity, purpose), generates a unique cryptographically salted 2D QR token linked to the animal's cloud profile, and derives an age-group physiological category (calf/heifer/lactating adult/dry/senior). Initializes the health status in an explicit ABSTAIN state."),

        ("Module 2 - Asynchronous Multi-Signal Data Ingestion Module",
         "Ingests recurring timestamped body weight w(t), daily feed intake f(t), observed physical activity score a(t), milking volume m(t), and optical QR-scan events s(t). Asynchronous logging frequencies are harmonized via an exponential time-decay filter to construct an observation vector x(t)."),

        ("Module 3 - Personalized Rolling Baseline Forecasting Module",
         "Computes, per animal, an expected rolling mean vector μ and covariance matrix Σ from that animal's own historical observations over a sliding temporal window W (past 14-30 days) once a minimum-entry threshold N >= N_min is satisfied."),

        ("Module 4 - Regularized Covariance-Aware CHDI Scoring Module",
         "Computes the Composite Health Deviation Index (CHDI) using a regularized Mahalanobis distance metric, mapped to a bounded score (0–100) and categorized into Normal, Watch, and At-Risk clinical bands."),

        ("Module 5 - Confidence-Aware Decision Abstention Gate",
         "Evaluates data volume and matrix stability. If entries are insufficient (N_obs < 7) or confidence is low (ρ < 0.40), the system withholds classification and returns an ABSTAIN state, eliminating false alarms."),

        ("Module 6 - Two-Tier Explainability & Feature Attribution Engine",
         "Decomposes the composite distance into constituent marginal contributions, generating (i) plain-language alerts for smallholder farmers, and (ii) detailed multidimensional vector charts for veterinary terminals."),

        ("Module 7 - Automated Veterinarian Triage & Case Routing Module",
         "Dispatches flagged cases in Watch and At-Risk bands to assigned regional veterinarians based on geographic proximity, attaching signal trends, explainability outputs, and medical histories."),

        ("Module 8 - Closed-Loop Active Learning & Classifier Retraining Module",
         "Captures attending veterinarian clinical diagnoses, treatments, and binary adjudication labels (CONFIRM vs OVERRIDE) to periodically retrain a secondary supervised classifier over time."),

        ("Module 9 - Spatio-Temporal Regional Outbreak Aggregation Module",
         "Continuously cross-aggregates recent deviations across animals and discrete farms within spatial clusters over a sliding temporal window, triggering regional alerts when multi-farm anomaly density exceeds threshold bounds.")
    ]
    for title, desc in modules_desc:
        add_black_p(c, title, font_size=10.5, bold=True, space_before=3, space_after=1)
        add_black_p(c, desc, font_size=10, space_after=3)

    # 2. MATHEMATICAL FORMULATIONS (USING EXACT REPORT FORMULAS 1 TO 9)
    add_black_p(c, "2. Mathematical Formulation of the Composite Health Deviation Index (CHDI):", font_size=11, bold=True, space_before=8, space_after=4)

    def insert_eq_with_explanation(eq_num, width_in, exp_lines):
        img_file = os.path.join(eq_dir, f'eq_{eq_num}.png')
        if os.path.exists(img_file):
            p_img = c.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.add_run().add_picture(img_file, width=Inches(width_in))

        # "where" text block
        p_where = c.add_paragraph()
        p_where.paragraph_format.left_indent = Inches(0.2)
        p_where.paragraph_format.space_after = Pt(3)
        r_w = p_where.add_run("where " + exp_lines[0])
        apply_tnr_black(r_w, font_size=10)

        for l in exp_lines[1:]:
            p_sub = c.add_paragraph()
            p_sub.paragraph_format.left_indent = Inches(0.4)
            p_sub.paragraph_format.space_after = Pt(1.5)
            r_s = p_sub.add_run("• " + l)
            apply_tnr_black(r_s, font_size=9.5)

    # Equation (4.1): Rolling Baseline Mean
    insert_eq_with_explanation(1, 4.8, [
        "μ_i,j(t) is the personalized rolling baseline average of physiological metric j for animal i at time t over an observation window of W = 14 recorded days:",
        "W = Rolling baseline window length (14 days)",
        "x_i,j(t - k) = Actual recorded vital measurement k days prior"
    ])

    # Equation (4.2): Rolling Sample Variance with Bessel's Correction
    insert_eq_with_explanation(2, 5.8, [
        "σ_i,j²(t) is the unbiased sample variance capturing natural daily biological variability (spread) for animal i and vital parameter j:",
        "W - 1 = Bessel's correction factor ensuring an unbiased variance estimate",
        "μ_i,j(t) = Personalized baseline mean for the corresponding animal and channel"
    ])

    # Equation (4.3): Standardized Normalized Deviation Vector
    insert_eq_with_explanation(3, 4.5, [
        "z_i,j(t) is the dimensionless standardized z-score deviation converting disparate physical units (liters, kg, minutes) into scale-invariant units:",
        "x_i,j(t) = Today's recorded vital observation",
        "σ_i,j(t) = Baseline standard deviation for that metric",
        "ε = Numerical stabilizer constant (10^-4) preventing division by zero"
    ])

    # Equation (4.4): Empirical Telemetry Covariance Matrix
    insert_eq_with_explanation(4, 5.5, [
        "Σ_i(t) is the d x d empirical sample covariance matrix documenting the joint correlation among all physiological variables for individual animal i:",
        "z_i(t - k) = Multivariate normalized deviation vector at time lag k",
        "Captures physiological couplings such as elevated body temperature occurring simultaneously with dropped milk yield and reduced rumination"
    ])

    # Equation (4.5): Tikhonov-Regularized Covariance Inversion
    insert_eq_with_explanation(5, 4.8, [
        "Σ_i,reg^(-1) is the regularized precision matrix guaranteed to be non-singular and strictly invertible across sparse observations:",
        "λ = Tikhonov ridge regularization parameter (10^-3)",
        "I = d x d Identity matrix preventing numerical crashes during collinearity or sparse entries"
    ])

    # Equation (4.6): Tikhonov-Regularized Multivariate Mahalanobis Distance & CHDI Score
    insert_eq_with_explanation(6, 6.2, [
        "D_M(t) is the multidimensional Mahalanobis distance measuring deviation from personal homeostasis, and CHDI(t) is the normalized health index:",
        "z_i(t) = Today's multivariate normalized deviation vector",
        "Σ_i,reg^(-1) = Regularized precision matrix",
        "D_max = Maximum statistical distance limit (4.0, representing the 99.99% chi-squared threshold)",
        "CHDI(t) is strictly bounded between 0 and 100 (100 = optimal homeostasis, <60 = At-Risk)"
    ])

    # Equation (4.7): LOCO Marginal Distance Delta
    insert_eq_with_explanation(7, 5.2, [
        "ΔD_k(t) is the marginal distance drop quantifying the standalone contribution of physiological metric k via Leave-One-Covariate-Out (LOCO) permutation:",
        "D_M(t) = Full multivariate anomaly score across all monitored signals",
        "D_M,(-k)(t) = Anomaly distance recomputed with physiological signal k omitted"
    ])

    # Equation (4.8): Percentage Feature Contribution Attribution
    insert_eq_with_explanation(8, 4.8, [
        "C_k(t) is the percentage contribution share of physiological metric k driving the alert:",
        "ΔD_k(t) = Marginal delta for vital sign k",
        "Σ ΔD_m = Total sum of all individual feature deltas",
        "Normalizes individual feature deltas into intuitive percentage shares summing to 100% for explainable clinical triage"
    ])

    # Equation (4.9): Baseline Confidence Scaling Metric
    insert_eq_with_explanation(9, 4.2, [
        "ρ(t) is the analytical baseline maturity confidence score governing automated decision gating:",
        "N_obs = Number of logged historical observation days recorded to date",
        "W = Baseline window saturation constant (14 days)",
        "Enforces explicit abstention (ABSTAIN state) if N_obs < 7 or ρ(t) < 0.40, suppressing premature false alarms"
    ])

    # 3. Operational Flow & Scenario
    add_black_p(c, "3. End-to-End Operational Lifecycle:", font_size=11, bold=True, space_before=6, space_after=3)
    flow_steps = [
        "1. Animal Registration & Token Binding: Farmer registers cattle metadata via the mobile app; system issues a unique optical QR tag attached to the animal; initial health record created in ABSTAIN state.",
        "2. Multi-Signal Data Ingestion: Farmer scans QR tag using mobile camera and enters daily milk yield and feed intake; activity scores calculated from scan intervals and grazing logs.",
        "3. Personalized Baseline Formation: Upon accumulating N >= 7 valid entries, rolling mean vector μ and covariance matrix Σ are established.",
        "4. Continuous CHDI Evaluation: On each log, covariance condition is validated; regularized Mahalanobis distance D_M is calculated; bounded score S_CHDI is derived.",
        "5. Automated Incident Escalation: Scores below 60 automatically generate an incident record routed to regional veterinary terminal with explainability decomposition.",
        "6. Clinical Examination & Adjudication: Veterinarian examines animal, performs treatment, and logs formal CONFIRM or OVERRIDE outcome.",
        "7. Active Learning Model Retraining: Model weights periodically update based on verified clinical outcomes.",
        "8. Multi-Farm Epidemiological Surveillance: Outbreak aggregator continuously correlates spatial deviations to prevent widespread disease transmission."
    ]
    for s in flow_steps:
        add_black_p(c, s, font_size=10, space_after=2)

    add_black_p(c, "4. Example Field Validation Scenario:", font_size=11, bold=True, space_before=5, space_after=2)
    scen_text = (
        "A lactating dairy cow's daily milk yield and feed intake begin trending below its own established rolling baseline over 3 consecutive days "
        "(milk yield drops from 14.5 L to 9.2 L; feed intake drops from 18 kg to 11 kg), while body weight and activity scores remain temporarily within range. "
        "The CHDI module detects this correlated bivariate deviation, computing a composite score of 52 (placing the animal in the 'At-Risk' band). "
        "The explainability module identifies milk yield and feed intake as contributing 58% and 34% of the deviation respectively. "
        "An automated clinical case is routed to the assigned regional veterinarian, who reviews the trajectory, visits the farm, diagnoses early-stage subclinical ketosis, and confirms the flag as accurate (CONFIRM label). "
        "The verified case is logged into the ground-truth repository, refining future early-stage metabolic risk detection. "
        "Concurrently, if neighboring farms within a 5 km radius report concurrent feed/milk deviations, the regional aggregator evaluates cluster density to rule out contagious local feed contamination or viral spread."
    )
    add_black_p(c, scen_text, font_size=10, space_after=4)

    # -------------------------------------------------------------------------
    # Table 10: Drawings (Section 1.j) - ULTRA-CLEAN PRO DIAGRAM WITHOUT NUMBERS!
    # -------------------------------------------------------------------------
    c = doc.tables[10].rows[0].cells[0]
    p = clear_cell_and_get_first_p(c)
    apply_tnr_black(p.add_run("j.  Provide Drawings, if any.\n"), font_size=11.5, bold=True)

    add_black_p(c, "The invention is illustrated by the following representative system architecture and operational workflow drawing:", font_size=10.5, space_after=4)

    add_black_p(c, "FIGURE 1: MASTER SYSTEM ARCHITECTURE AND COMPUTATIONAL WORKFLOW", font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=4)

    if os.path.exists(pro_fig_path):
        p_img = c.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(pro_fig_path, width=Inches(6.4))

    # NO DESCRIPTIVE NUMBERING TABLE! (Per user explicit request)
    add_black_p(c, "", space_after=2)

    # -------------------------------------------------------------------------
    # Section 2: Disclosure (Tables 11 to 15)
    # -------------------------------------------------------------------------
    p = doc.tables[11].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_black(p.add_run("2.  Disclosure"), font_size=12, bold=True)

    doc.tables[12].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[12].rows[0].cells[0].paragraphs[0].add_run("a.  Has the invention ever been shown or used in public?"), font_size=11, bold=True)
    doc.tables[12].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[12].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No"), font_size=11)

    doc.tables[13].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[13].rows[0].cells[0].paragraphs[0].add_run("If yes, Where / When"), font_size=11, bold=True)
    doc.tables[13].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[13].rows[0].cells[1].paragraphs[0].add_run("Not Applicable (Maintained strictly confidential prior to patent filing)"), font_size=11)

    doc.tables[14].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[14].rows[0].cells[0].paragraphs[0].add_run("b.  Was any Confidentiality Agreement signed regarding the invention?"), font_size=11, bold=True)
    doc.tables[14].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[14].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No"), font_size=11)

    doc.tables[15].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[15].rows[0].cells[0].paragraphs[0].add_run("c.  Has this invention been publicly disclosed (e.g., paper published/presented)?"), font_size=11, bold=True)
    doc.tables[15].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[15].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No (Maintained strictly confidential prior to patent priority date)"), font_size=11)

    # -------------------------------------------------------------------------
    # Section 3: Foreign Patent Protection (Tables 16, 17)
    # -------------------------------------------------------------------------
    p = doc.tables[16].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_black(p.add_run("3.  Foreign Patent Protection"), font_size=12, bold=True)

    doc.tables[17].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[17].rows[0].cells[0].paragraphs[0].add_run("a.  Do you intend to pursue International Patent protection?"), font_size=11, bold=True)
    doc.tables[17].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[17].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No (Indian Jurisdiction Priority Filing First)"), font_size=11)

    # -------------------------------------------------------------------------
    # Section 4: Funding and Sponsorship (Tables 18 to 23)
    # -------------------------------------------------------------------------
    p = doc.tables[18].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_black(p.add_run("4.  Funding and Sponsorship"), font_size=12, bold=True)

    doc.tables[19].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[19].rows[0].cells[0].paragraphs[0].add_run("1. Was this invention developed with external funding?"), font_size=11, bold=True)
    doc.tables[19].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[19].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No"), font_size=11)

    doc.tables[20].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[20].rows[0].cells[0].paragraphs[0].add_run("2. Funding Agency / Sponsor"), font_size=11, bold=True)
    doc.tables[20].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[20].rows[0].cells[1].paragraphs[0].add_run("Not Applicable (Self-funded institutional research)"), font_size=11)

    doc.tables[21].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[21].rows[0].cells[0].paragraphs[0].add_run("3. Grant or Contract number"), font_size=11, bold=True)
    doc.tables[21].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[21].rows[0].cells[1].paragraphs[0].add_run("Not Applicable"), font_size=11)

    doc.tables[22].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[22].rows[0].cells[0].paragraphs[0].add_run("4. Principal Investigator (PI) / Faculty Supervisor"), font_size=11, bold=True)
    doc.tables[22].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[22].rows[0].cells[1].paragraphs[0].add_run("[Faculty Guide / Project Supervisor Name], Department of Computer Science and Engineering, Sona College of Technology"), font_size=11)

    doc.tables[23].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[23].rows[0].cells[0].paragraphs[0].add_run("5. Are there any third-party obligations?"), font_size=11, bold=True)
    doc.tables[23].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[23].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No"), font_size=11)

    # -------------------------------------------------------------------------
    # Section 5: Commercial Potential (Tables 24 to 27)
    # -------------------------------------------------------------------------
    p = doc.tables[24].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_black(p.add_run("5.  Commercial Potential"), font_size=12, bold=True)

    doc.tables[25].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[25].rows[0].cells[0].paragraphs[0].add_run("1. Potential applications / Industries"), font_size=11, bold=True)
    doc.tables[25].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[25].rows[0].cells[1].paragraphs[0].add_run(
        "Smallholder dairy farming, rural milk cooperatives (e.g., Aavin, Amul, Nandini), precision livestock technology, commercial dairy herd management, veterinary tele-triage portals, and livestock micro-insurance underwriting."
    ), font_size=10.5)

    doc.tables[26].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[26].rows[0].cells[0].paragraphs[0].add_run("2. Known competing technologies"), font_size=11, bold=True)
    doc.tables[26].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[26].rows[0].cells[1].paragraphs[0].add_run(
        "Wearable IoT sensor collars and ear tags (e.g., SCR Dairy, Allflex), rumination boluses, RFID tags without multivariate AI analytics, manual registers, and static population-threshold software."
    ), font_size=10.5)

    doc.tables[27].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[27].rows[0].cells[0].paragraphs[0].add_run("3. Companies/organizations that may be interested in licensing the technology"), font_size=11, bold=True)
    doc.tables[27].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_black(doc.tables[27].rows[0].cells[1].paragraphs[0].add_run(
        "National Dairy Development Board (NDDB / INAPH), Stellapps Technologies, Prompt Dairy Tech, DeLaval India, HDFC ERGO Rural Insurance, and State Animal Husbandry Departments."
    ), font_size=10.5)

    # -------------------------------------------------------------------------
    # Section 6: Inventorship Declaration (Tables 28 to 31)
    # -------------------------------------------------------------------------
    p = doc.tables[28].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_black(p.add_run("6.  Inventorship Declaration"), font_size=12, bold=True)

    c = doc.tables[29].rows[0].cells[0]
    p = clear_cell_and_get_first_p(c)
    decl_text = (
        "I/we declare that the information provided in this form is accurate, complete, and true to the best of my/our knowledge. "
        "I/we understand that providing false or misleading information may adversely affect any patent application filed based on this disclosure. "
        "I/we agree to assign all rights, title, and interest in this invention to Sona College of Technology in accordance with the institutional IPR policy."
    )
    apply_tnr_black(p.add_run(decl_text), font_size=10.5)

    # Table 31: Signature Table for Inventors
    t31 = doc.tables[31]
    if len(t31.columns) == 2:
        t31.add_column(Inches(2.4))
        print("Added column 3 to Table 31 for Inventor 4 (Faculty Guide)")

    clear_cell_and_get_first_p(t31.rows[0].cells[0]).add_run("Inventor 1").bold = True
    clear_cell_and_get_first_p(t31.rows[1].cells[0]).add_run("Sabari Karthick A")
    clear_cell_and_get_first_p(t31.rows[2].cells[0]).add_run("Student (B.E. CSE),\nSona College of Technology")
    clear_cell_and_get_first_p(t31.rows[3].cells[0]).add_run("Signature: _______________")
    clear_cell_and_get_first_p(t31.rows[4].cells[0]).add_run("Date: ____ / ____ / 2026")

    clear_cell_and_get_first_p(t31.rows[0].cells[1]).add_run("Inventor 2").bold = True
    clear_cell_and_get_first_p(t31.rows[1].cells[1]).add_run("Sivanarasimman S")
    clear_cell_and_get_first_p(t31.rows[2].cells[1]).add_run("Student (B.E. CSE),\nSona College of Technology")
    clear_cell_and_get_first_p(t31.rows[3].cells[1]).add_run("Signature: _______________")
    clear_cell_and_get_first_p(t31.rows[4].cells[1]).add_run("Date: ____ / ____ / 2026")

    if len(t31.rows[0].cells) > 2:
        clear_cell_and_get_first_p(t31.rows[0].cells[2]).add_run("Inventor 3 & 4 (Guide)").bold = True
        clear_cell_and_get_first_p(t31.rows[1].cells[2]).add_run("Sujeeth Y R & [Faculty Guide]")
        clear_cell_and_get_first_p(t31.rows[2].cells[2]).add_run("Dept. of Computer Science & Engg,\nSona College of Technology")
        clear_cell_and_get_first_p(t31.rows[3].cells[2]).add_run("Signature: _______________")
        clear_cell_and_get_first_p(t31.rows[4].cells[2]).add_run("Date: ____ / ____ / 2026")

    # Table 32: Authorized Person
    t32 = doc.tables[32]
    clear_cell_and_get_first_p(t32.rows[0].cells[1]).add_run("Dr. [Head of Department / Dean R&D Name]")
    clear_cell_and_get_first_p(t32.rows[1].cells[1]).add_run("Head of Department (CSE) / Dean (R&D) / IPR Coordinator, Sona College of Technology")

    # Table 33: Office use only
    t33 = doc.tables[33]
    clear_cell_and_get_first_p(t33.rows[0].cells[1]).add_run("SCT/CIPR/IDF/2026/______")
    clear_cell_and_get_first_p(t33.rows[1].cells[1]).add_run("____ / ____ / 2026")
    clear_cell_and_get_first_p(t33.rows[2].cells[1]).add_run("☒ Recommended for Prior Art Search & Provisional Patent Filing")

    # -------------------------------------------------------------------------
    # FINAL PASS: Ensure EVERY run in doc is Times New Roman and Pure Black!
    # -------------------------------------------------------------------------
    for p in doc.paragraphs:
        for r in p.runs:
            apply_tnr_black(r, font_size=r.font.size.pt if r.font.size else 11, bold=r.bold, italic=r.italic)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        apply_tnr_black(r, font_size=r.font.size.pt if r.font.size else 10.5, bold=r.bold, italic=r.italic)

    # Save to all destination files
    target_paths = [
        r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Final.docx",
        r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent-1.docx",
        r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Perfect.docx"
    ]

    for tp in target_paths:
        try:
            doc.save(tp)
            print(f"Successfully saved to: {tp}")
        except Exception as e:
            print(f"Could not write to {tp} (possibly open in Word): {e}")

if __name__ == "__main__":
    main()
