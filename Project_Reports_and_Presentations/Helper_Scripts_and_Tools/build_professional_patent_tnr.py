import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def apply_tnr_to_run(run, font_size=11, bold=False, italic=False, color_rgb=None):
    run.font.name = "Times New Roman"
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = color_rgb
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(r'<w:rFonts %s w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>' % nsdecls('w'))
    rPr.append(rFonts)

def clear_cell_and_get_first_paragraph(cell):
    p_first = cell.paragraphs[0]
    p_first.text = ""
    for p in cell.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    return p_first

def add_p(cell, text="", font_size=11, bold=False, italic=False, space_before=0, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, color_rgb=None, indent=0):
    p = cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    if text:
        r = p.add_run(text)
        apply_tnr_to_run(r, font_size=font_size, bold=bold, italic=italic, color_rgb=color_rgb)
    return p

def add_formula_block(cell, formula_name, formula_text, variable_explanations):
    """Formats a mathematical formula in a clear, distinct, publication-grade block."""
    # Formula title
    p_title = cell.add_paragraph()
    p_title.paragraph_format.space_before = Pt(5)
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run(formula_name + ":")
    apply_tnr_to_run(r_t, font_size=10.5, bold=True, color_rgb=RGBColor(26, 54, 93))

    # Formula equation block with indentation and distinct styling
    p_eq = cell.add_paragraph()
    p_eq.paragraph_format.left_indent = Inches(0.4)
    p_eq.paragraph_format.space_before = Pt(2)
    p_eq.paragraph_format.space_after = Pt(3)
    r_eq = p_eq.add_run(formula_text)
    apply_tnr_to_run(r_eq, font_size=11, bold=True, color_rgb=RGBColor(0, 0, 0))

    # Explanation lines
    for exp in variable_explanations:
        p_exp = cell.add_paragraph()
        p_exp.paragraph_format.left_indent = Inches(0.4)
        p_exp.paragraph_format.space_after = Pt(1.5)
        r_exp = p_exp.add_run("• " + exp)
        apply_tnr_to_run(r_exp, font_size=9.5, italic=False, color_rgb=RGBColor(45, 55, 72))

def main():
    backup_path = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent-1-backup.docx"
    clean_fig_path = r"c:\Project\SmartCattle new\patent_figures\figure_master_system_architecture_clean.png"

    doc = Document(backup_path)
    print("Loaded original tabular document successfully.")

    # Set document normal style to Times New Roman
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)

    # -------------------------------------------------------------------------
    # Paragraph 0: Document Title Banner
    # -------------------------------------------------------------------------
    p0 = doc.paragraphs[0]
    p0.text = ""
    r0 = p0.add_run("INVENTION DISCLOSURE FORM")
    apply_tnr_to_run(r0, font_size=14, bold=True, color_rgb=RGBColor(26, 54, 93))
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # -------------------------------------------------------------------------
    # Table 0: Section 1 Header
    # -------------------------------------------------------------------------
    p = doc.tables[0].rows[0].cells[0].paragraphs[0]
    p.text = ""
    r = p.add_run("1.  Details of the Invention")
    apply_tnr_to_run(r, font_size=12, bold=True, color_rgb=RGBColor(26, 54, 93))

    # -------------------------------------------------------------------------
    # Table 1: Title of the invention
    # -------------------------------------------------------------------------
    c_lbl = doc.tables[1].rows[0].cells[0]
    c_lbl.paragraphs[0].text = ""
    r = c_lbl.paragraphs[0].add_run("a.  Title of the invention")
    apply_tnr_to_run(r, font_size=11, bold=True)

    c_val = doc.tables[1].rows[0].cells[1]
    p = clear_cell_and_get_first_paragraph(c_val)
    r1 = p.add_run("A SYSTEM AND COMPUTER-IMPLEMENTED METHOD FOR SENSOR-INDEPENDENT LIVESTOCK HEALTH MONITORING USING OPTICAL IDENTIFIERS AND COMPOSITE MULTIVARIATE DEVIATION ANALYSIS\n\n")
    apply_tnr_to_run(r1, font_size=11, bold=True)
    r2 = p.add_run("(Also referred to as: QR-Based Cattle Management System with AI-Driven Health Monitoring and Composite Health Deviation Index - CHDI)")
    apply_tnr_to_run(r2, font_size=10, italic=True)

    # -------------------------------------------------------------------------
    # Table 2: Field of the invention
    # -------------------------------------------------------------------------
    c_lbl = doc.tables[2].rows[0].cells[0]
    c_lbl.paragraphs[0].text = ""
    r = c_lbl.paragraphs[0].add_run("b.  Field of the invention")
    apply_tnr_to_run(r, font_size=11, bold=True)

    c_val = doc.tables[2].rows[0].cells[1]
    p = clear_cell_and_get_first_paragraph(c_val)
    r = p.add_run("Precision Livestock Farming (Animal Husbandry Technology), Artificial Intelligence, Machine Learning, and Veterinary Tele-Informatics\n"
                  "(International Patent Classification [IPC]: A01K 29/00, G16H 50/20, G06N 20/00)")
    apply_tnr_to_run(r, font_size=11)

    # -------------------------------------------------------------------------
    # Table 3: Stage of development
    # -------------------------------------------------------------------------
    c = doc.tables[3].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    r = p.add_run("c.  Stage of development\n\n☐ Idea only        ☐ Proof of concept        ☒ Prototype        ☒ Tested        ☐ In use/deployed\n"
                  "(Functional software prototype integrated with mobile optical scanner, cloud analytics API, and clinical vet portal evaluated on field cattle datasets)")
    apply_tnr_to_run(r, font_size=11)

    # -------------------------------------------------------------------------
    # Table 4: Nature of invention
    # -------------------------------------------------------------------------
    row4 = doc.tables[4].rows[0]
    for cell, txt, b in [(row4.cells[0], "d.  Is the invention based on", True),
                         (row4.cells[1], "☒ Product", True),
                         (row4.cells[2], "☒ Process/Method", True),
                         (row4.cells[3], "☐ Composition", False),
                         (row4.cells[4], "☐ Other", False)]:
        p = clear_cell_and_get_first_paragraph(cell)
        r = p.add_run(txt)
        apply_tnr_to_run(r, font_size=11, bold=b)

    # -------------------------------------------------------------------------
    # Table 5: Novel/New aspects & Inventive Step
    # -------------------------------------------------------------------------
    c = doc.tables[5].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    r = p.add_run("e.  What is/are the Novel/New aspects of the invention? What is the inventive step?\n")
    apply_tnr_to_run(r, font_size=11.5, bold=True, color_rgb=RGBColor(26, 54, 93))

    novelty_points = [
        ("1. Sensor-Optional, QR-Based Identification and Multi-Rate Data Capture",
         "Unlike conventional precision-livestock systems requiring permanent wearable electronic devices (ear tags, collars, boluses costing >$100/animal), this invention identifies each animal using a durable, low-cost optical 2D matrix (QR token) costing under $0.50 and ingests asynchronous multi-rate farmer-logged data (milk yield, feed intake, activity, body weight). An exponential decay interpolation filter reconciles disparate logging intervals, eliminating hardware cost barriers while ensuring data integrity."),

        ("2. Personalized Rolling Physiological Baseline Addressing Biological Non-Stationarity",
         "Rather than comparing an animal against generalized herd or breed averages (which trigger high false-alarm rates due to natural differences across age, parity, and lactation stages), the system constructs a rolling statistical baseline (mean vector μ and empirical covariance matrix Σ) strictly from each animal's own temporal data history."),

        ("3. Regularized Covariance-Aware Multivariate Anomaly Scoring (CHDI)",
         "Health vitals naturally exhibit strong biological co-dependencies in cattle (e.g., feed intake and milk yield drop concurrently during systemic illness). The system combines multi-signal deviations into a single Composite Health Deviation Index using a regularized Mahalanobis distance metric D_M, capturing physiological correlation geometry and preventing matrix singularity from sparse logs."),

        ("4. Strict Matrix-Condition & Confidence-Bounded Decision Abstention Gate",
         "When historical records are sparse (N < N_min during onboarding) or when the empirical covariance matrix is ill-conditioned (condition number cond(Σ) > κ_max), the system mathematically withholds automated verdicts rather than issuing speculative classifications, drastically eliminating false alarm fatigue among farmers."),

        ("5. Dual-Tier Explainable AI (XAI) Architecture",
         "The invention decomposes multivariate deviation vectors into ranked feature attributions, delivering (i) an intuitive plain-language top-contributing factor for low-literacy smallholder farmers, and (ii) a complete multidimensional deviation vector and trend radar for veterinary diagnostic terminals."),

        ("6. Closed-Loop Clinical Veterinarian Active Learning Pipeline",
         "Clinical confirmation (True Anomaly) or override (False Alarm / Contextual deviation like estrus or weather) of each flagged case by attending veterinarians is captured as audited ground-truth clinical data to periodically retrain a supervised classifier, allowing predictive accuracy to continuously improve from verified field outcomes."),

        ("7. Spatio-Temporal Multi-Farm Epidemiological Outbreak Aggregator",
         "Deviations are cross-aggregated across discrete farm holdings in spatial-temporal clusters (radius R and temporal window ΔT). When cluster anomaly density exceeds a dynamic threshold across multiple independent holdings, a regional outbreak alert is automatically distributed to animal husbandry authorities.")
    ]
    for title, desc in novelty_points:
        add_p(c, title, font_size=11, bold=True, space_before=4, space_after=1, color_rgb=RGBColor(43, 108, 176))
        add_p(c, desc, font_size=10.5, space_after=4)

    # -------------------------------------------------------------------------
    # Table 6: Prior Art (ALL 10 ESSENTIAL CITATIONS & DRAWBACKS)
    # -------------------------------------------------------------------------
    c = doc.tables[6].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    r = p.add_run("f.  Is there any prior art for this invention? (Comprehensive Search & Technical Distinctions)\n")
    apply_tnr_to_run(r, font_size=11.5, bold=True, color_rgb=RGBColor(26, 54, 93))

    prior_arts_full = [
        ("1. Haladjian, J.; Haug, J.; Nüske, S.; and Bruegge, B. (2018). “A Wearable Sensor System for Lameness Detection in Dairy Cattle,” Multimodal Technologies and Interaction, 2(2), 27:",
         "Discloses a wearable motion sensor attached to the cow with an individual gait model for lameness detection.",
         "Drawbacks & Distinctions: Strictly limited to gait/lameness monitoring; requires dedicated per-animal wearable body hardware; lacks optical QR data ingestion, covariance-aware composite scoring (CHDI), confidence abstention, veterinarian feedback retraining, and multi-farm outbreak aggregation."),

        ("2. Suchak, V.; Rana, H.; Verma, A.; Dubey, N. K.; Jayswal, H. S.; Damodar, D.; and Patel, C. I. (2026). “IoT-Based Smart Cattle Health Monitoring System Using Machine Learning for Real-Time Anomaly Detection,” LNNS, Vol. 1463, pp. 1-12:",
         "Discloses IoT sensor hardware and machine-learning cattle health anomaly detection.",
         "Drawbacks & Distinctions: Fully reliant on physical electronic sensor hardware fitted to animals; fails to provide a low-cost optical QR/sensor-optional workflow, per-animal CHDI covariance scoring, confidence abstention, or veterinarian-confirmed adaptive retraining."),

        ("3. Modak et al. (2025). “Internet of Things-Based Health Surveillance Systems for Livestock: A Review of Recent Advances and Challenges,” IET Wireless Sensor Systems:",
         "Reviews conventional wearable livestock systems including collars, boluses, and temperature sensors.",
         "Drawbacks & Distinctions: Systems reviewed are hardware-dependent and suffer high capital costs and tag loss; does not disclose an optical QR-linked asynchronous logging workflow, regularized covariance CHDI scoring, or clinical active learning."),

        ("4. Kasuga, Ryoichi; and Kasuga, Hisashi (2017). “Livestock Management System,” JP6203238B2, published 27 September 2017:",
         "Describes QR/barcodes attached to livestock scanned using a mobile device for database lookup.",
         "Drawbacks & Distinctions: Only provides static identification lookups; completely lacks automated AI baseline forecasting, covariance anomaly scoring, confidence abstention, or regional epidemiological outbreak clustering."),

        ("5. Guice, David; Pugh, Warren; and Thompson, Noble (2002). “Method and System for Monitoring the Health and Status of Livestock and Other Animals,” US20020010390A1, published 24 January 2002:",
         "Describes automated livestock monitoring using implanted wireless sensors measuring temperature and blood oxygen.",
         "Drawbacks & Distinctions: Relies on high-cost implanted/body-borne electronic sensors; lacks optical/manual-first scoring architecture, regularized CHDI metric, or veterinarian-in-the-loop retraining."),

        ("6. Beckham, Tammy; Coats, Matthew; et al. (2022). “System and Method for Monitoring and Analyzing Animal Related Data,” US11243976B2, published 8 February 2022:",
         "Aggregates animal-related data and evaluates baseline metrics for herd management assessment.",
         "Drawbacks & Distinctions: Broad centralized data platform; fails to teach regularized covariance-aware multivariate distance scoring, dynamic sample-bounded abstention, or veterinarian active learning triage loops."),

        ("7. Diao, Shanghua; and Deng, Yingang (2021). “Livestock Health Monitoring Method and Device, Storage Medium and Electronic Equipment,” CN113488175A, published 8 October 2021:",
         "Uses an electronic tag containing temperature, acceleration, and heart-rate sensors with a trained health model.",
         "Drawbacks & Distinctions: Requires dedicated electronic sensing hardware and a pre-trained population model rather than an optical-first QR approach with personalized CHDI covariance baselines and explicit abstention."),

        ("8. Subramanian, Srinivas; Kamble, Ramdas; Pote, Supriya; Goel, Neeraj; and Sen, Swapna (2024). “IoT-Based Cattle Health and Heat Monitoring System,” WO2024009326A1, published 11 January 2024:",
         "Describes collar units using sensor data for activity, rumination, and temperature for heat/health alerts.",
         "Drawbacks & Distinctions: Mandates wearable collar hardware; lacks optical-first sensor-optional pipeline, regularized CHDI formulation, or regional multi-farm correlation analysis."),

        ("9. Mindel, Anatoly; and Cohen, Yossi (2025). “Monitoring Livestock in an Agricultural Pen,” US12266142B2, published 1 April 2025:",
         "Describes multi-camera pen monitoring identifying animals using tags/barcodes and estimating wellbeing from images.",
         "Drawbacks & Distinctions: Relies on expensive installed camera infrastructure; does not teach asynchronous multi-rate manual/QR health logging, CHDI scoring, confidence abstention, or clinical active learning."),

        ("10. Chinese Patent Application CN121148662A (2025). “A Method for Identifying Dairy Cow Behavior Based on a Six-Axis Inertial Sensor,” published 14 November 2025:",
         "Describes cow behavior recognition using a six-axis inertial sensor and deviation analysis.",
         "Drawbacks & Distinctions: Strict dependency on body-worn motion sensors; lacks sensor-optional optical input, covariance multi-signal CHDI scoring, clinical override tracking, or regional cluster alerting.")
    ]

    for title, scope, drawb in prior_arts_full:
        add_p(c, title, font_size=10.5, bold=True, space_before=4, space_after=1, color_rgb=RGBColor(45, 55, 72))
        add_p(c, "Disclosed Scope: " + scope, font_size=10, italic=True, space_after=1)
        add_p(c, drawb, font_size=10, space_after=4)

    # -------------------------------------------------------------------------
    # Table 7: General Overview & Keywords
    # -------------------------------------------------------------------------
    c = doc.tables[7].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    r = p.add_run("g.  General overview of the invention, including specific keywords and phrases:\n")
    apply_tnr_to_run(r, font_size=11.5, bold=True, color_rgb=RGBColor(26, 54, 93))

    ov_text = (
        "The present invention relates to an AI-driven cattle health monitoring and clinical case management system that identifies each animal through a durable optical machine-readable token (QR tag) and evaluates health using a Composite Health Deviation Index (CHDI) computed from asynchronous multi-source data (manual farmer logs, mobile optical camera scan timestamps, and optional IoT feeds), without requiring wearable sensors. "
        "The system establishes a personalized rolling baseline for each animal from its own historical records (weight, daily feed intake, observed physical activity, and milk yield) once a minimum sample threshold is attained. "
        "It calculates real-time deviation from that baseline using a regularized covariance-aware Mahalanobis distance metric, mapping the result to a single composite health score (0–100) with an associated confidence metric. "
        "When historical data is sparse or when the empirical covariance matrix is ill-conditioned, the system enforces a confidence-aware abstention mechanism, withholding speculative verdicts to eliminate false alarms. "
        "Cases falling into 'Watch' or 'At-Risk' bands automatically generate clinical incident records routed to licensed regional veterinarians with a two-tier explainability vector (plain-language factors for farmers, multidimensional breakdowns for clinicians). "
        "The veterinarian's clinical confirmation or diagnostic override is captured as audited ground truth to periodically retrain a supervised classifier over time. "
        "Furthermore, individual deviations are geographically aggregated across discrete farm holdings in spatial-temporal clusters to trigger early-warning alerts for multi-farm disease outbreaks."
    )
    add_p(c, ov_text, font_size=10.5, space_after=6)

    add_p(c, "Specific Keywords and Phrases Pertaining to the Invention:", font_size=10.5, bold=True, space_before=4, space_after=2)
    keywords = [
        "QR-Based Animal Identification",
        "Sensor-Optional Health Monitoring",
        "Personalized Physiological Baseline",
        "Composite Health Deviation Index (CHDI)",
        "Regularized Mahalanobis Distance Metric",
        "Confidence-Aware Decision Abstention Gate",
        "Matrix Condition Number Verification",
        "Two-Tier Explainable AI (XAI) for Animal Health",
        "Veterinarian-in-the-Loop Active Learning",
        "Spatio-Temporal Regional Outbreak Aggregation",
        "Asynchronous Multi-Rate Signal Normalization",
        "Smallholder Dairy Herd Tele-Informatics"
    ]
    add_p(c, " • " + "\n • ".join(keywords), font_size=10, space_after=4)

    # -------------------------------------------------------------------------
    # Table 8: How Invention is More Beneficial or Feasible
    # -------------------------------------------------------------------------
    c = doc.tables[8].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    r = p.add_run("h.  How the invention is more beneficial or feasible over the prior art:\n")
    apply_tnr_to_run(r, font_size=11.5, bold=True, color_rgb=RGBColor(26, 54, 93))

    benefits = [
        ("1. Total Elimination of Wearable Hardware Cost Barrier",
         "Prior precision-livestock systems require fitting every animal with an expensive wearable device (ear tag, collar, or bolus costing $80-$150 each), which is commercially unviable for smallholders owning 1-5 cows. This invention functions from weather-resistant optical QR tags costing under $0.50 and accepts mobile-logged data, democratizing precision health monitoring while remaining fully compatible with optional IoT telemetry."),

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
        add_p(c, title, font_size=11, bold=True, space_before=4, space_after=1, color_rgb=RGBColor(43, 108, 176))
        add_p(c, desc, font_size=10.5, space_after=4)

    # -------------------------------------------------------------------------
    # Table 9: Detailed Explanation of the Invention (WITH CLEAR FORMULAS)
    # -------------------------------------------------------------------------
    c = doc.tables[9].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    r = p.add_run("i.  Detailed explanation of the invention (Modules, Mathematical Formulations & Flow):\n")
    apply_tnr_to_run(r, font_size=11.5, bold=True, color_rgb=RGBColor(26, 54, 93))

    add_p(c, "1. Technical Architectural Modules:", font_size=11, bold=True, space_before=4, space_after=3)

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
         "Evaluates data volume and matrix stability. If entries are insufficient or covariance variance is ill-conditioned, the system withholds classification and returns an ABSTAIN state, eliminating false alarms."),

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
        add_p(c, title, font_size=10.5, bold=True, space_before=3, space_after=1, color_rgb=RGBColor(43, 108, 176))
        add_p(c, desc, font_size=10, space_after=3)

    # MATHEMATICAL FORMULATIONS (CLEAR, DISPLAY-MATH STYLE WITH VARIABLE DEFINITIONS)
    add_p(c, "2. Mathematical Formulation of the Composite Health Deviation Index (CHDI):", font_size=11, bold=True, space_before=8, space_after=3)

    # Formula 1: Observation Vector
    add_formula_block(
        c,
        "Formula 1: Multi-Signal Observation Vector",
        "x(t) = [ w(t),   f(t),   a(t),   m(t),   s(t) ]^T",
        ["w(t) = Body weight in kilograms (kg)",
         "f(t) = Daily feed intake in kilograms (kg)",
         "a(t) = Observed physical activity score (arbitrary activity index / daily steps)",
         "m(t) = Daily milk yield volume in liters (L)",
         "s(t) = Optical scan / observation interval in hours (h)"]
    )

    # Formula 2: Rolling Baseline Mean and Covariance
    add_formula_block(
        c,
        "Formula 2: Personalized Rolling Baseline Mean Vector and Covariance Matrix",
        "μ = (1 / N) * Σ_{k=1}^{N} x_k\nΣ = (1 / (N - 1)) * Σ_{k=1}^{N} (x_k - μ) * (x_k - μ)^T",
        ["μ = Individual expected mean vector for the specific animal over rolling window W (14–30 days)",
         "Σ = 5 x 5 Empirical covariance matrix capturing the natural co-dependencies between vitals",
         "N = Number of recorded historical observations (minimum threshold N >= N_min = 7)"]
    )

    # Formula 3: Tikhonov Covariance Regularization
    add_formula_block(
        c,
        "Formula 3: Tikhonov Shrinkage Covariance Regularization",
        "Σ_reg = Σ + λ * I",
        ["Σ_reg = Regularized, well-conditioned covariance matrix guaranteed to be strictly invertible",
         "λ = Dynamic ridge shrinkage regularization parameter (λ > 0, preventing matrix singularity from sparse or collinear vitals)",
         "I = 5 x 5 Identity matrix"]
    )

    # Formula 4: Regularized Mahalanobis Distance
    add_formula_block(
        c,
        "Formula 4: Regularized Mahalanobis Deviation Distance Metric",
        "D_M(x) = sqrt( (x - μ)^T * (Σ_reg)^(-1) * (x - μ) )",
        ["D_M(x) = Multivariate statistical distance measuring how many standard deviations the current multi-signal vector x deviates from the animal's personal baseline μ",
         "(Σ_reg)^(-1) = Inverted regularized covariance matrix weighting deviations inversely to their natural joint variance"]
    )

    # Formula 5: CHDI Normalized Score
    add_formula_block(
        c,
        "Formula 5: Composite Health Deviation Index (CHDI) Normalized Score",
        "S_CHDI = 100 * exp( - D_M(x) / τ )",
        ["S_CHDI = Normalized health score bounded strictly between 0 and 100 (where 100 represents a perfect match to baseline health)",
         "τ = Calibrated biological dispersion scale factor (e.g., τ = 3.0) governing the decay rate of the score relative to distance D_M"]
    )

    # Formula 6: Clinical Decision Bands
    add_formula_block(
        c,
        "Formula 6: Clinical Health Band Decision Rule",
        "Status(x) = Normal (Low Risk),          if S_CHDI >= 80\nStatus(x) = Watch (Moderate Deviation),  if 60 <= S_CHDI < 80\nStatus(x) = At-Risk (Critical Anomaly),   if S_CHDI < 60",
        ["Normal: Animal vitals conform to individual rolling baseline; routine logging continues",
         "Watch: Moderate deviation detected; generates early advisory alert with plain-language factor ranking to farmer",
         "At-Risk: Critical anomaly detected; automatically escalates an urgent clinical case to assigned regional veterinarian"]
    )

    # Formula 7: Confidence Abstention Gate
    add_formula_block(
        c,
        "Formula 7: Mathematical Confidence-Aware Decision Abstention Gate",
        "Decision = ABSTAIN (Verdict Withheld)    if:\n(i)  N < N_min  (Sample count insufficient; formative baseline period)\n(ii) cond(Σ) = σ_max(Σ) / σ_min(Σ) > κ_max  (Ill-conditioned covariance matrix)\n(iii) Missing primary vitals beyond allowable time tolerance",
        ["cond(Σ) = Matrix condition number (ratio of largest to smallest singular values)",
         "κ_max = Configured numerical stability threshold bound",
         "Effect: Prevents speculative false-positive classifications during early animal registration"]
    )

    # Formula 8: Two-Tier Feature Explainability Metric
    add_formula_block(
        c,
        "Formula 8: Two-Tier Marginal Feature Attribution / Explainability Metric",
        "C_i = |x_i - μ_i| * |( (Σ_reg)^(-1) * (x - μ) )_i|\nNormalized Contribution (%) = [ C_i / Σ_{j=1}^{5} C_j ] * 100%",
        ["C_i = Marginal contribution score of individual physiological signal i (e.g., milk yield vs. feed intake)",
         "Farmer Tier: Displays plain-language dominant factor (e.g., 'Milk yield dropped 38% below personal baseline')",
         "Veterinarian Tier: Displays full 5-dimensional deviation radar vector and temporal trajectory curves"]
    )

    # Formula 9: Regional Outbreak Aggregation Index
    add_formula_block(
        c,
        "Formula 9: Spatial-Temporal Cluster Anomaly Index (CAI)",
        "CAI(R, ΔT) = [ Σ_{j in R} 1(S_{CHDI, j} < 60) ] / [ Total Registered Herd in Cluster R ]\nRegional Alert Triggered if:  CAI(R, ΔT) >= Θ_threshold   AND   M_farms >= 3",
        ["R = Geographic spatial cluster radius (e.g., 5 to 10 km radius or GeoHash cell)",
         "ΔT = Sliding temporal observation window (e.g., 48 to 72 hours)",
         "M_farms = Number of distinct independent farm holdings reporting concurrent anomalies",
         "Effect: Distinguishes localized individual illness from contagious multi-farm disease outbreaks"]
    )

    # 3. Operational Flow & Scenario
    add_p(c, "3. End-to-End Operational Lifecycle:", font_size=11, bold=True, space_before=6, space_after=3)
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
        add_p(c, s, font_size=10, space_after=2)

    add_p(c, "4. Example Field Validation Scenario:", font_size=11, bold=True, space_before=5, space_after=2)
    scen_text = (
        "A lactating dairy cow's daily milk yield and feed intake begin trending below its own established rolling baseline over 3 consecutive days "
        "(milk yield drops from 14.5 L to 9.2 L; feed intake drops from 18 kg to 11 kg), while body weight and activity scores remain temporarily within range. "
        "The CHDI module detects this correlated bivariate deviation, computing a composite score of 52 (placing the animal in the 'At-Risk' band). "
        "The explainability module identifies milk yield and feed intake as contributing 58% and 34% of the deviation respectively. "
        "An automated clinical case is routed to the assigned regional veterinarian, who reviews the trajectory, visits the farm, diagnoses early-stage subclinical ketosis, and confirms the flag as accurate (CONFIRM label). "
        "The verified case is logged into the ground-truth repository, refining future early-stage metabolic risk detection. "
        "Concurrently, if neighboring farms within a 5 km radius report concurrent feed/milk deviations, the regional aggregator evaluates cluster density to rule out contagious local feed contamination or viral spread."
    )
    add_p(c, scen_text, font_size=10, space_after=4)

    # -------------------------------------------------------------------------
    # Table 10: Drawings (Section 1.j) - PROFESSIONAL CLEAN DIAGRAM
    # -------------------------------------------------------------------------
    c = doc.tables[10].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    r = p.add_run("j.  Provide Drawings, if any.\n")
    apply_tnr_to_run(r, font_size=11.5, bold=True, color_rgb=RGBColor(26, 54, 93))

    add_p(c, "The invention is illustrated by the following representative system architecture and operational workflow drawing:", font_size=10.5, space_after=4)

    add_p(c, "FIGURE 1: SYSTEM ARCHITECTURE AND OPERATIONAL WORKFLOW (100)", font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=4)

    if os.path.exists(clean_fig_path):
        p_img = c.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(6)
        p_img.add_run().add_picture(clean_fig_path, width=Inches(6.4))

    add_p(c, "Descriptive of Numerical Labeling:", font_size=10, bold=True, space_before=4, space_after=3)

    # Clean 2-column table for numerical labels
    labels_table_data = [
        ("100", "Physical Data Acquisition Tier (Overall Hardware/Input Tier)"),
        ("102", "Cattle Optical Machine-Readable QR Identification Tag"),
        ("104", "Handheld Mobile Optical Camera Scanner"),
        ("106", "Farmer Asynchronous Mobile Data Entry Interface (Milk, Feed, Vitals)"),
        ("108", "Milking / Weighing / Scan Interval Timestamps"),
        ("110", "Optional Environmental / IoT Sensor Data Ingestion Inputs"),
        ("112", "Encrypted Offline Client Data Buffer & Storage Cache"),
        ("200", "Central AI Processing & Analytics Engine Tier"),
        ("202", "Optical Token Authentication & Cattle Identity Registry"),
        ("204", "Asynchronous Multi-Rate Temporal Imputation & Normalization Filter"),
        ("206", "Personalized Rolling Physiological Baseline Generator (Mean μ, Covariance Σ)"),
        ("208", "Tikhonov Shrinkage Covariance Regularizer (Σ_reg = Σ + λ*I)"),
        ("210", "Covariance-Aware Regularized Mahalanobis Distance Metric (D_M)"),
        ("212", "Bounded Composite Health Deviation Index Score Mapper (S_CHDI: 0–100)"),
        ("214", "Confidence-Aware Decision Abstention Gate (Sample Count & Matrix Condition)"),
        ("216", "Two-Tier Feature Attribution & Explainability Engine (XAI)"),
        ("218", "Closed-Loop Supervised Classifier Active Learning Pipeline"),
        ("220", "Spatial-Temporal Multi-Farm Outbreak Cluster Aggregator"),
        ("222", "Secure Encrypted Longitudinal Cattle Database"),
        ("300", "Farmer User Interface Tier"),
        ("302", "Mobile Herd Monitoring & Status Dashboard"),
        ("304", "Visual Health Band Indicators (Normal / Watch / At-Risk)"),
        ("306", "Plain-Language Primary Factor Alert Notification Display"),
        ("308", "Direct Tele-Veterinary Consultation & Assistance Request"),
        ("400", "Clinical Veterinary & Epidemiological Outbreak Tier"),
        ("402", "Veterinary Clinical Case Triage & Workstation Portal"),
        ("404", "Multivariate Diagnostic Trajectory Radar Breakdown Display"),
        ("406", "Veterinary Confirm / Override Clinical Ground-Truth Feedback Loop"),
        ("408", "Multi-Farm Regional Epidemiological Outbreak Alert Gateway")
    ]

    t_lbl = c.add_table(rows=len(labels_table_data), cols=2)
    t_lbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (code, desc) in enumerate(labels_table_data):
        row = t_lbl.rows[idx]
        c0 = row.cells[0]; c1 = row.cells[1]
        c0.width = Inches(1.1); c1.width = Inches(5.3)
        p0 = c0.paragraphs[0]; p0.text = ""
        r0 = p0.add_run(code); apply_tnr_to_run(r0, font_size=9, bold=True)
        p1 = c1.paragraphs[0]; p1.text = ""
        r1 = p1.add_run(desc); apply_tnr_to_run(r1, font_size=9)

    add_p(c, "", space_after=4)

    # -------------------------------------------------------------------------
    # Section 2: Disclosure (Tables 11 to 15)
    # -------------------------------------------------------------------------
    p = doc.tables[11].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_to_run(p.add_run("2.  Disclosure"), font_size=12, bold=True, color_rgb=RGBColor(26, 54, 93))

    doc.tables[12].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[12].rows[0].cells[0].paragraphs[0].add_run("a.  Has the invention ever been shown or used in public?"), font_size=11, bold=True)
    doc.tables[12].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[12].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No"), font_size=11)

    doc.tables[13].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[13].rows[0].cells[0].paragraphs[0].add_run("If yes, Where / When"), font_size=11, bold=True)
    doc.tables[13].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[13].rows[0].cells[1].paragraphs[0].add_run("Where: ________________________     When: ________________________"), font_size=10.5)

    doc.tables[14].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[14].rows[0].cells[0].paragraphs[0].add_run("b.  Was any Confidentiality Agreement signed regarding the invention?"), font_size=11, bold=True)
    doc.tables[14].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[14].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No"), font_size=11)

    doc.tables[15].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[15].rows[0].cells[0].paragraphs[0].add_run("c.  Has this invention been publicly disclosed (e.g., paper presentation)? If yes, provide details on title of publication, or presented, Date of disclosure, Conference /Journal (Attach copies or drafts if available)"), font_size=10, bold=True)
    doc.tables[15].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[15].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No"), font_size=11)

    # -------------------------------------------------------------------------
    # Section 3: Foreign Patent Protection (Tables 16, 17)
    # -------------------------------------------------------------------------
    p = doc.tables[16].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_to_run(p.add_run("3.  Foreign Patent Protection"), font_size=12, bold=True, color_rgb=RGBColor(26, 54, 93))

    doc.tables[17].rows[0].cells[0].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[17].rows[0].cells[0].paragraphs[0].add_run("a.  Do you intend to pursue International Patent protection?"), font_size=11, bold=True)
    doc.tables[17].rows[0].cells[1].paragraphs[0].text = ""
    apply_tnr_to_run(doc.tables[17].rows[0].cells[1].paragraphs[0].add_run("☐ Yes    ☒ No"), font_size=11)

    # -------------------------------------------------------------------------
    # Section 4: Funding & Sponsorship (Tables 18 to 23)
    # -------------------------------------------------------------------------
    p = doc.tables[18].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_to_run(p.add_run("4.  Funding and Sponsorship"), font_size=12, bold=True, color_rgb=RGBColor(26, 54, 93))

    funding_entries = [
        (doc.tables[19], "1. Was this invention developed with external funding", "No"),
        (doc.tables[20], "2. Funding Agency / Sponsor", "N/A"),
        (doc.tables[21], "3. Grant or Contract number", "N/A"),
        (doc.tables[22], "4. Principal Investigator (PI) / Faculty Project Supervisor", "[Faculty Guide / Project Supervisor Name], Department of Artificial Intelligence and Data Science, Sona College of Technology, Salem"),
        (doc.tables[23], "5. Are there any third-party obligations (collaborations, industry partners)?", "No")
    ]
    for tbl, q, a in funding_entries:
        tbl.rows[0].cells[0].paragraphs[0].text = ""
        apply_tnr_to_run(tbl.rows[0].cells[0].paragraphs[0].add_run(q), font_size=10.5, bold=True)
        tbl.rows[0].cells[1].paragraphs[0].text = ""
        apply_tnr_to_run(tbl.rows[0].cells[1].paragraphs[0].add_run(a), font_size=10.5)

    # -------------------------------------------------------------------------
    # Section 5: Commercial Potential (Tables 24 to 27)
    # -------------------------------------------------------------------------
    p = doc.tables[24].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_to_run(p.add_run("5.  Commercial Potential"), font_size=12, bold=True, color_rgb=RGBColor(26, 54, 93))

    com_entries = [
        (doc.tables[25], "1. Potential applications / Industries",
         "Smallholder dairy farming and rural dairy cooperatives (e.g., Aavin, Amul federations), commercial herd management software, veterinary telemedicine portals, livestock micro-insurance underwriting, and government animal health epidemiological monitoring programs."),
        (doc.tables[26], "2. Known competing technologies",
         "Wearable IoT sensor-based livestock monitoring systems (ear tags, collars, boluses); RFID-based cattle identification and traceability systems; manual veterinary record-keeping; general-purpose livestock management software without AI-based health deviation scoring."),
        (doc.tables[27], "3. Companies/organizations that may be interested in licensing this technology",
         "National Dairy Development Board (NDDB), State Milk Federations, agritech startups (Stellapps Technologies, MooFarm, Prompt Dairy Tech), livestock insurance providers, and Department of Animal Husbandry and Dairying (DAHD), Govt. of India.")
    ]
    for tbl, q, a in com_entries:
        tbl.rows[0].cells[0].paragraphs[0].text = ""
        apply_tnr_to_run(tbl.rows[0].cells[0].paragraphs[0].add_run(q), font_size=10.5, bold=True)
        tbl.rows[0].cells[1].paragraphs[0].text = ""
        apply_tnr_to_run(tbl.rows[0].cells[1].paragraphs[0].add_run(a), font_size=10.5)

    # -------------------------------------------------------------------------
    # Section 6: Inventorship Declaration (Tables 28 to 33)
    # -------------------------------------------------------------------------
    p = doc.tables[28].rows[0].cells[0].paragraphs[0]
    p.text = ""; apply_tnr_to_run(p.add_run("6.  Inventorship Declaration"), font_size=12, bold=True, color_rgb=RGBColor(26, 54, 93))

    p = doc.tables[29].rows[0].cells[0].paragraphs[0]
    p.text = ""
    apply_tnr_to_run(p.add_run("I/we declare that the information provided in this form is accurate and complete to the best of my/our knowledge. I/we agree to assign rights in this invention to Sona College of Technology, in accordance with institutional policy."),
                     font_size=10.5, italic=True)

    # Table 30: Inventors 1 & 2
    t30 = doc.tables[30]
    t30_vals = [
        ("Inventor 1", "Inventor 2"),
        ("Sabari Karthick A", "Sivanarasimman S"),
        ("Final-Year Student, Artificial Intelligence and Data Science", "Final-Year Student, Artificial Intelligence and Data Science"),
        ("_______________________", "_______________________"),
        ("_______________________", "_______________________")
    ]
    for r_idx in range(5):
        row = t30.rows[r_idx]
        apply_tnr_to_run(row.cells[0].paragraphs[0].runs[0] if row.cells[0].paragraphs[0].runs else row.cells[0].paragraphs[0].add_run(), font_size=9.5, bold=True)
        for c_idx in [1, 2]:
            p = row.cells[c_idx].paragraphs[0]
            p.text = ""
            apply_tnr_to_run(p.add_run(t30_vals[r_idx][c_idx - 1]), font_size=9.5, bold=(r_idx == 0))

    # Table 31: Symmetrical 3 Columns for Inventor 3 & Inventor 4 (Faculty Guide)
    t31 = doc.tables[31]
    if len(t31.columns) == 2:
        t31.add_column(Inches(2.4))

    t31_vals = [
        ("Inventor 3", "Inventor 4 (Faculty Guide)"),
        ("Sujeeth Y R", "[Faculty Guide / Project Supervisor Name]"),
        ("Final-Year Student, Artificial Intelligence and Data Science", "[Designation - e.g. Assistant Professor],\nDepartment of Artificial Intelligence and Data Science"),
        ("_______________________", "_______________________"),
        ("_______________________", "_______________________")
    ]
    labels_31 = ["", "a.  Full Name", "b.  Designation & Department", "c.  Signature", "d.  Date"]
    for r_idx in range(5):
        row = t31.rows[r_idx]
        row.cells[0].paragraphs[0].text = ""
        apply_tnr_to_run(row.cells[0].paragraphs[0].add_run(labels_31[r_idx]), font_size=9.5, bold=True)

        for c_idx in [1, 2]:
            p = row.cells[c_idx].paragraphs[0]
            p.text = ""
            apply_tnr_to_run(p.add_run(t31_vals[r_idx][c_idx - 1]), font_size=9.5, bold=(r_idx == 0))

    # Table 32: Authorized Person
    t32 = doc.tables[32]
    t32_data = [
        ("Authorized Person - Name", "Dr. [Head of Department / Dean R&D Name]"),
        ("Designation", "Head of Department (AI & DS) / Dean (R&D) / IPR Coordinator"),
        ("Signature", "________________________"),
        ("Date", "________________________")
    ]
    for idx, (lbl, val) in enumerate(t32_data):
        row = t32.rows[idx]
        row.cells[0].paragraphs[0].text = ""; apply_tnr_to_run(row.cells[0].paragraphs[0].add_run(lbl), font_size=9.5, bold=True)
        row.cells[1].paragraphs[0].text = ""; apply_tnr_to_run(row.cells[1].paragraphs[0].add_run(val), font_size=9.5)

    # Paragraph 39: Office use only
    if len(doc.paragraphs) > 39:
        p39 = doc.paragraphs[39]
        p39.text = ""
        apply_tnr_to_run(p39.add_run("Office use only"), font_size=11, bold=True)

    # Table 33: Office use only
    t33 = doc.tables[33]
    t33_data = [
        ("Disclosure number", "SCT/CIPR/IDF/2026/______"),
        ("Date received", "____ / ____ / 2026"),
        ("Next steps", "☐ Approved for Prior Art Search   ☐ Recommended for Filing   ☐ Revision Required")
    ]
    for idx, (lbl, val) in enumerate(t33_data):
        row = t33.rows[idx]
        row.cells[0].paragraphs[0].text = ""; apply_tnr_to_run(row.cells[0].paragraphs[0].add_run(lbl), font_size=9.5, bold=True)
        row.cells[1].paragraphs[0].text = ""; apply_tnr_to_run(row.cells[1].paragraphs[0].add_run(val), font_size=9.5)

    # ENFORCE TIMES NEW ROMAN ON EVERY SINGLE RUN IN THE DOCUMENT
    for p in doc.paragraphs:
        for r in p.runs:
            apply_tnr_to_run(r, font_size=r.font.size.pt if r.font.size else 11, bold=r.bold, italic=r.italic)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        apply_tnr_to_run(r, font_size=r.font.size.pt if r.font.size else 10.5, bold=r.bold, italic=r.italic)

    # Save to targets safely
    targets = [
        r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent-1.docx",
        r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Times New Roman.docx",
        r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Final.docx"
    ]
    for p_tgt in targets:
        try:
            doc.save(p_tgt)
            print("Successfully saved:", p_tgt)
        except PermissionError:
            print("Skipped locked file (open in Word):", p_tgt)

if __name__ == "__main__":
    main()
