import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def add_header_page_number(run):
    """Inserts PAGE field code into run."""
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def add_header_numpages(run):
    """Inserts NUMPAGES field code into run."""
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> NUMPAGES </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
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

def build_patent_document():
    doc = Document()

    # Set margins 0.75 in
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

        # Header: Page X of 10
        header = section.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hp = p_head.add_run("Page ")
        r_hp.font.name = "Calibri"
        r_hp.font.size = Pt(10)
        add_header_page_number(p_head.add_run())
        r_of = p_head.add_run(" of ")
        r_of.font.name = "Calibri"
        r_of.font.size = Pt(10)
        add_header_numpages(p_head.add_run())

    fig_dir = r"c:\Project\SmartCattle new\patent_figures"

    # Helper function for adding paragraphs
    def add_p(text="", bold=False, italic=False, size=11, space_before=0, space_after=4, indent=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        if indent:
            p.paragraph_format.left_indent = Inches(indent)
        if text:
            r = p.add_run(text)
            r.bold = bold
            r.italic = italic
            r.font.name = "Calibri"
            r.font.size = Pt(size)
            r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_prompt_label(label, bracket_text=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(label)
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(11.5)
        if bracket_text:
            r2 = p.add_run(" " + bracket_text)
            r2.italic = True
            r2.font.name = "Calibri"
            r2.font.size = Pt(10)
            r2.font.color.rgb = RGBColor(70, 70, 70)
        return p

    # =========================================================================
    # 1. DETAILS OF THE INVENTION
    # =========================================================================
    add_p("1. Details of the Invention:", bold=True, size=12, space_before=0, space_after=6)

    # a. Title
    add_prompt_label("a. Title of the invention:")
    add_p("             A SYSTEM AND COMPUTER-IMPLEMENTED METHOD FOR SENSOR-INDEPENDENT LIVESTOCK HEALTH MONITORING USING OPTICAL IDENTIFIERS AND COMPOSITE MULTIVARIATE DEVIATION ANALYSIS",
          bold=True, size=11, space_after=2)
    add_p("             (Alternative/Common Title: QR-Based Cattle Management System with AI-Driven Health Monitoring and Composite Health Deviation Index - CHDI)",
          italic=True, size=10, space_after=6)

    # b. Field
    add_prompt_label("b. Field of the invention", "[Broader subject area of the invention]")
    add_p("           Precision Livestock Farming (Animal Husbandry Technology), Artificial Intelligence, Machine Learning, and Veterinary Tele-Informatics\n"
          "           (International Patent Classification [IPC]: A01K 29/00, G16H 50/20, G06N 20/00)", size=11, space_after=6)

    # c. Stage of development
    add_prompt_label("c. Stage of development", "[please tick]:")
    add_p("o Idea only", indent=0.4, space_after=2)
    add_p("o Proof of concept", indent=0.4, space_after=2)
    add_p("☒ Prototype", bold=True, indent=0.4, space_after=2)
    add_p("☒ Tested", bold=True, indent=0.4, space_after=2)
    add_p("o In use/ deployed", indent=0.4, space_after=6)

    # d. Is the invention based on
    p_d = doc.add_paragraph()
    p_d.paragraph_format.space_before = Pt(6)
    p_d.paragraph_format.space_after = Pt(8)
    r = p_d.add_run("d. Is the invention based on  ")
    r.bold = True; r.font.name = "Calibri"; r.font.size = Pt(11)
    
    r_prod = p_d.add_run("☒ Product                                     ")
    r_prod.bold = True; r_prod.font.name = "Calibri"; r_prod.font.size = Pt(11)
    
    r_proc = p_d.add_run("☒ Process/Method                                     ")
    r_proc.bold = True; r_proc.font.name = "Calibri"; r_proc.font.size = Pt(11)
    
    r_comp = p_d.add_run("Composition                                     Other")
    r_comp.font.name = "Calibri"; r_comp.font.size = Pt(11)

    # e. Novel / New aspects & inventive step
    add_prompt_label("e. What is/are the Novel/New aspects of the invention? What is the inventive step?",
                     "[What problems are being solved by the invention]")

    novel_items = [
        ("Sensor-independent optical identifier binding & multi-rate data ingestion",
         "Unlike prior precision livestock monitoring systems that require invasive or high-cost electronic wearable hardware (ear tags, collars, boluses costing >$100/animal), this invention identifies animals through low-cost weather-resistant optical QR tokens and accepts asynchronous multi-rate farmer-logged data (milk yield, feed intake, activity, weight). An exponential decay interpolation filter reconciles disparate logging cadences without capital hardware barriers."),

        ("Personalized rolling physiological baseline addressing biological non-stationarity",
         "Rather than comparing animal vitals against static breed or herd population averages (which suffer massive false alarm rates due to natural differences across age, parity, and lactation cycles), the system builds a rolling statistical expectation (mean vector μ and covariance matrix Σ) constructed strictly from each animal's own temporal data history."),

        ("Regularized covariance-aware multivariate anomaly scoring (CHDI)",
         "Health vitals naturally move together in cattle (e.g., feed intake and milk yield drop concurrently during systemic illness). The invention combines multi-signal deviations into a single Composite Health Deviation Index using regularized Mahalanobis distance D_M(x) = sqrt((x - μ)^T * (Σ + λ*I)^(-1) * (x - μ)), capturing physiological correlation geometry and preventing matrix singularity from sparse logs."),

        ("Strict matrix-condition & confidence-bounded decision abstention gate",
         "When historical records are sparse (N < N_min during onboarding) or when the empirical covariance matrix is ill-conditioned (cond(Σ) > κ_max), the system mathematically withholds automated verdicts rather than issuing speculative classifications, drastically reducing false alarm fatigue."),

        ("Dual-tier explainable AI (XAI) architecture",
         "The invention dynamically decomposes multivariate deviation vectors into ranked feature attributions, delivering (i) an intuitive plain-language top-contributing factor for low-literacy smallholder farmers, and (ii) a complete multidimensional deviation vector and trajectory chart for veterinary diagnostic terminals."),

        ("Closed-loop clinical veterinarian active learning pipeline",
         "Veterinarian confirmation (True Anomaly) or override (False Alarm / Contextual deviation) of each flagged case is archived as audited ground-truth clinical data to periodically retrain a supervised classifier, allowing accuracy to improve continuously from field outcomes."),

        ("Spatio-temporal multi-farm epidemiological outbreak aggregation engine",
         "Deviations are cross-aggregated across discrete farm holdings in spatial-temporal clusters (radius R and time window ΔT). When cluster anomaly density exceeds an epidemiological threshold, a regional early-warning alert is triggered to veterinary authorities days ahead of passive reporting.")
    ]

    for title, desc in novel_items:
        p_it = doc.add_paragraph()
        p_it.paragraph_format.space_before = Pt(4)
        p_it.paragraph_format.space_after = Pt(1)
        r_t = p_it.add_run(title)
        r_t.bold = True
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)
        
        p_id = doc.add_paragraph()
        p_id.paragraph_format.space_after = Pt(4)
        r_d = p_id.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(10.5)

    # f. Prior Art
    add_prompt_label("f. Is there any prior art for this invention:",
                     "[Has the problem been solved/ Is the problem being solved in any other manner by others? Limitations and drawbacks of prior art]")

    prior_arts = [
        ("Haladjian, J.; Haug, J.; Nüske, S.; and Bruegge, B. (2018). “A Wearable Sensor System for Lameness Detection in Dairy Cattle,” Multimodal Technologies and Interaction, 2(2), 27:",
         "Describes a wearable motion sensor attached to the cow with an individual gait model for lameness detection. Limitations: Limited strictly to lameness and requires per-animal wearable hardware; lacks optical QR data ingestion, covariance-aware composite scoring (CHDI), confidence abstention, veterinarian feedback retraining, and multi-farm outbreak aggregation."),

        ("Suchak, V.; Rana, H.; Verma, A.; Dubey, N. K.; Jayswal, H. S.; Damodar, D.; and Patel, C. I. (2026). “IoT-Based Smart Cattle Health Monitoring System Using Machine Learning for Real-Time Anomaly Detection,” LNNS, Vol. 1463, pp. 1-12:",
         "Describes IoT sensor hardware and machine-learning cattle health anomaly detection. Limitations: Fully reliant on physical IoT sensor hardware on the cattle; does not provide an optical QR/sensor-optional workflow, per-animal CHDI covariance scoring, confidence abstention, or veterinarian-confirmed adaptive retraining."),

        ("Modak et al. (2025). “Internet of Things-Based Health Surveillance Systems for Livestock: A Review of Recent Advances and Challenges,” IET Wireless Sensor Systems:",
         "Reviews wearable livestock systems including collars, temperature sensors, and accelerometers. Limitations: Hardware-dependent and does not disclose the proposed optical QR-linked, asynchronous multi-rate logging workflow with CHDI scoring and clinical active learning."),

        ("Kasuga, Ryoichi; and Kasuga, Hisashi (2017). “Livestock Management System,” JP6203238B2:",
         "Describes QR/barcodes attached to livestock scanned using a mobile device for database lookup. Limitations: Provides only manual identification lookups; lacks automated AI baseline forecasting, covariance anomaly scoring, confidence abstention, or regional outbreak clustering."),

        ("Guice, David; Pugh, Warren; and Thompson, Noble (2002). “Method and System for Monitoring the Health and Status of Livestock and Other Animals,” US20020010390A1:",
         "Describes implanted and wireless wearable sensors for cattle vitals. Limitations: Relies exclusively on high-cost body-borne electronic sensors; lacks optical/manual-first scoring architecture, regularized CHDI metric, or veterinarian-in-the-loop retraining."),

        ("Beckham, Tammy; Coats, Matthew; et al. (2022). “System and Method for Monitoring and Analyzing Animal Related Data,” US11243976B2:",
         "Describes aggregating animal data and evaluating baselines. Limitations: Broad centralized data platform; fails to teach regularized covariance-aware multivariate distance scoring, dynamic sample-bounded abstention, or veterinarian active learning triage loops."),

        ("Diao, Shanghua; and Deng, Yingang (2021). “Livestock Health Monitoring Method and Device, Storage Medium and Electronic Equipment,” CN113488175A:",
         "Uses an electronic tag containing temperature, acceleration, and heart-rate sensors with a trained health model. Limitations: Requires dedicated electronic sensing hardware and a pre-trained population model rather than an optical-first QR approach with personalized CHDI covariance baselines and explicit abstention."),

        ("Subramanian, Srinivas; Kamble, Ramdas; Pote, Supriya; Goel, Neeraj; and Sen, Swapna (2024). “IoT-Based Cattle Health and Heat Monitoring System,” WO2024009326A1:",
         "Describes collar units measuring activity, rumination, and temperature for heat/health alerts. Limitations: Hardware-dependent collar requirement; lacks optical-first sensor-optional pipeline, regularized CHDI formulation, or regional multi-farm correlation analysis."),

        ("Mindel, Anatoly; and Cohen, Yossi (2025). “Monitoring Livestock in an Agricultural Pen,” US12266142B2:",
         "Describes pen camera arrays observing cattle tags and estimating wellbeing from images. Limitations: Relies on expensive installed camera infrastructure; does not teach asynchronous multi-rate manual/QR health logging, CHDI scoring, confidence abstention, or clinical active learning."),

        ("Chinese Patent Application CN121148662A (2025). “A Method for Identifying Dairy Cow Behavior Based on a Six-Axis Inertial Sensor”:",
         "Describes cow behavior recognition using a six-axis inertial sensor and deviation analysis. Limitations: Strict dependency on body-worn motion sensors; lacks sensor-optional optical input, covariance multi-signal CHDI scoring, clinical override tracking, or regional cluster alerting.")
    ]

    for title, desc in prior_arts:
        p_it = doc.add_paragraph()
        p_it.paragraph_format.space_before = Pt(4)
        p_it.paragraph_format.space_after = Pt(1)
        r_t = p_it.add_run(title)
        r_t.bold = True
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10.5)

        p_id = doc.add_paragraph()
        p_id.paragraph_format.space_after = Pt(4)
        r_d = p_id.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(10)

    # g. General Overview & Keywords
    add_prompt_label("g. Provide a general overview of your invention, including specific keywords and phrases pertaining to the invention:",
                     "[Briefly provide the basic understanding of the invention and also point out specific keywords.]")

    ov_text = (
        "The present invention relates to an AI-driven cattle health monitoring and clinical case management system that identifies each animal through an optical machine-readable token (QR tag) and evaluates its health using a Composite Health Deviation Index (CHDI) computed from asynchronous multi-source data (manual farmer logs, mobile optical camera scan timestamps, and optional IoT feeds), without requiring dedicated body-worn sensor hardware. "
        "The system establishes a personalized rolling baseline for each animal from its own historical time series (weight, daily feed intake, observed physical activity, and milk yield) once a minimum sample threshold is attained. "
        "It calculates real-time deviation from that baseline using a regularized covariance-aware Mahalanobis distance metric, mapping the result to a single composite health score (0–100) with an associated confidence metric. "
        "When historical data is sparse or when the empirical covariance matrix is ill-conditioned, the system enforces a confidence-aware abstention mechanism, withholding speculative verdicts to eliminate false alarms. "
        "Cases falling into 'Watch' or 'At-Risk' bands automatically generate clinical incident records routed to licensed regional veterinarians with a two-tier explainability vector (plain-language factors for farmers, multidimensional breakdowns for clinicians). "
        "The veterinarian's clinical confirmation or diagnostic override is captured as audited ground truth to periodically retrain a supervised classifier over time. "
        "Furthermore, individual deviations are geographically aggregated across discrete farm holdings in spatial-temporal clusters to trigger early-warning alerts for multi-farm disease outbreaks."
    )
    add_p(ov_text, size=10.5, space_after=6)

    add_p("Specific Keywords and Phrases Pertaining to the Invention", bold=True, size=11, space_before=6, space_after=4)
    keywords = [
        ("h.", "AI-based Livestock Health Monitoring"),
        ("i.", "QR-Based Animal Identification"),
        ("j.", "Sensor-Independent Precision Livestock Farming"),
        ("k.", "Personalized Non-Stationary Health Baseline"),
        ("l.", "Composite Health Deviation Index (CHDI)"),
        ("m.", "Regularized Mahalanobis Distance Metric"),
        ("n.", "Confidence-Aware Decision Abstention Gate"),
        ("o.", "Matrix Condition Number Verification"),
        ("p.", "Two-Tier Explainable AI (XAI) for Animal Health"),
        ("q.", "Veterinarian-in-the-Loop Active Learning"),
        ("r.", "Spatio-Temporal Outbreak Aggregation Engine"),
        ("s.", "Asynchronous Multi-Rate Signal Normalization"),
        ("t.", "Smallholder Dairy Herd Tele-Informatics"),
        ("u.", "Tele-Veterinary Clinical Triage System"),
        ("v.", "Dynamic Covariance Matrix Regularization")
    ]
    for letter, kw in keywords:
        p_k = doc.add_paragraph()
        p_k.paragraph_format.space_after = Pt(2)
        r_l = p_k.add_run(f"{letter} ")
        r_l.bold = True; r_l.font.name = "Calibri"; r_l.font.size = Pt(10.5)
        r_v = p_k.add_run(kw)
        r_v.font.name = "Calibri"; r_v.font.size = Pt(10.5)

    # w. How invention is more beneficial or feasible
    add_prompt_label("w. Describe how the invention is more beneficial or feasible over the prior art.",
                     "[What are the advantages/improvements of the invention as compared to solutions provided by others]")

    adv_items = [
        ("1. Total Elimination of Wearable Hardware Cost Barrier",
         "Prior systems require fitting every animal with an expensive wearable device (ear tag, collar, or bolus costing $80-$150 each), which is commercially unviable for smallholders owning 1-5 cows. This invention operates from weather-resistant optical QR tokens costing under $0.50 and mobile-logged data, eliminating capital hardware barriers while remaining sensor-compatible."),

        ("2. Personalized Rolling Baseline Rather Than Population Averages",
         "Prior art evaluates animals against generalized breed or herd norms that produce high false-positive rates due to natural variations across parity and lactation stages. This invention builds a personalized non-stationary baseline strictly from the animal's own longitudinal history, eliminating breed-specific calibration bias."),

        ("3. Regularized Covariance-Aware Multivariate Scoring",
         "Prior systems monitor a single condition or assign arbitrary static weights to individual metrics. This invention combines all physiological signals into a single CHDI score using a regularized Mahalanobis distance that accounts for the natural covariance structure of health parameters for that specific animal."),

        ("4. Explicit Mathematical Abstention Drastically Reduces False Alarms",
         "Unlike systems that force speculative classifications upon receiving minimal entries, this invention evaluates sample size (N < N_min) and matrix condition number (cond(Σ) > κ_max) to withhold verdicts during formative periods, preserving farmer trust and preventing unnecessary veterinary expenses."),

        ("5. Closed-Loop Clinical Verification Continuously Refines Accuracy",
         "Most prior systems operate as static detectors. This invention captures veterinarian confirm/override decisions as audited ground-truth labels and periodically retrains a secondary supervised classifier, allowing accuracy to improve autonomously from verified field outcomes."),

        ("6. Multi-Farm Epidemiological Radar Built From Distributed Individual Data",
         "Prior art is isolated to single animals or single farms. This invention aggregates geo-tagged deviations across discrete farm holdings in spatial-temporal clusters, detecting correlated disease outbreaks days before traditional passive government reporting.")
    ]

    for title, desc in adv_items:
        p_it = doc.add_paragraph()
        p_it.paragraph_format.space_before = Pt(4)
        p_it.paragraph_format.space_after = Pt(1)
        r_t = p_it.add_run(title)
        r_t.bold = True; r_t.font.name = "Calibri"; r_t.font.size = Pt(11)
        
        p_id = doc.add_paragraph()
        p_id.paragraph_format.space_after = Pt(4)
        r_d = p_id.add_run(desc)
        r_d.font.name = "Calibri"; r_d.font.size = Pt(10.5)

    # i. Detailed Explanation of Invention
    add_prompt_label("       i.Provide a detailed explanation of your invention:",
                     "[Specifically describe all the element and components of the invention. Also describe how all the elements and components work together to form the invention. For more clarity and understanding, respective examples, diagrams, flowcharts, etc. may be provided]")

    modules = [
        ("1. Cattle Registration and Optical Token Module",
         "This module collects static biometric identity parameters and establishes optical tracking tokens.",
         ["Biometric intake interface (Tag ID, breed, DOB, parity, purpose)",
          "Cryptographic 2D QR token generator",
          "Age-group physiological classifier (calf/heifer/lactating adult/dry/senior)",
          "Initial health record initializer (ABSTAIN state)"],
         "Before monitoring begins, each animal is registered in the cloud database and issued a high-density, weather-resistant optical QR token attached to its collar or ear tag. This establishes the cryptographic entity binding all subsequent logs."),

        ("2. Asynchronous Multi-Signal Data Ingestion Module",
         "This module captures recurring health parameters across variable logging cadences.",
         ["Mobile optical camera barcode/QR scanner",
          "Farmer manual data entry interface",
          "Optional IoT sensor ingestion adapter",
          "Exponential time-decay interpolation filter"],
         "Accepts timestamped body weight w(t), daily feed intake f(t), observed activity score a(t), milking volume m(t), and scan interval s(t). Asynchronous logging frequencies are harmonized via an exponential decay filter to construct an aligned observation vector x(t) = [w(t), f(t), a(t), m(t), s(t)]^T."),

        ("3. Personalized Rolling Baseline Generator",
         "This module dynamically builds an expected physiological baseline for each animal.",
         ["Rolling temporal window buffer (W = 14 to 30 days)",
          "Sample-count threshold validator (N >= N_min)",
          "Rolling mean vector estimator (μ = E[x])",
          "Empirical covariance matrix estimator (Σ = Cov(x))"],
         "Builds an individual baseline purely from the animal's historical observations once N >= 7 entries are attained, adapting dynamically as the animal transitions through lactation and aging."),

        ("4. Regularized Covariance-Aware CHDI Scoring Module",
         "This module calculates multivariate physiological deviation accounting for signal co-dependencies.",
         ["Tikhonov shrinkage regularizer (Σ_reg = Σ + λ * I)",
          "Inverted covariance solver (Σ_reg^(-1))",
          "Mahalanobis distance calculator (D_M = sqrt((x - μ)^T * Σ_reg^(-1) * (x - μ)))",
          "Bounded score mapper (S_CHDI = 100 * exp(-D_M / τ))"],
         "Combines multi-signal deviations into a single bounded score (0–100) and categorizes animal state into Normal (S >= 80), Watch (60 <= S < 80), and At-Risk (S < 60) clinical bands."),

        ("5. Confidence-Aware Decision Abstention Gate",
         "This module withholds speculative verdicts during sparse or noisy data periods.",
         ["Sample-count validator (checks if N < N_min)",
          "Matrix condition number validator (checks if cond(Σ) > κ_max)",
          "Critical vital completeness validator (feed/milk presence)",
          "Abstention state dispatcher (returns ABSTAIN status)"],
         "When historical records are insufficient or signal variance is ill-conditioned, the system withholds automated classification, eliminating false positive alarm fatigue."),

        ("6. Two-Tier Explainability & Feature Attribution Engine",
         "This module decomposes composite anomaly scores into interpretable clinical insights.",
         ["Marginal contribution calculator (C_i = |x_i - μ_i| * |(Σ_reg^(-1) * (x - μ))_i|)",
          "Farmer plain-language alert generator",
          "Veterinarian multidimensional radar vector synthesizer"],
         "Translates mathematical deviation into (i) plain-language alerts for farmers (e.g., 'Milk yield dropped 35% below baseline'), and (ii) detailed vector breakdowns for clinicians."),

        ("7. Automated Veterinary Triage & Case Routing Module",
         "This module escalates detected anomalies to licensed veterinary practitioners.",
         ["Geo-spatial proximity dispatcher",
          "Clinical case queue manager",
          "Signal trajectory visualizer",
          "Notification delivery engine (Push, SMS, In-App)"],
         "Automatically generates an incident case when an animal enters Watch or At-Risk bands, routing it to the assigned local veterinarian with diagnostic trajectories attached."),

        ("8. Closed-Loop Clinical Active Learning Pipeline",
         "This module captures clinical adjudications to continuously refine predictive models.",
         ["Veterinary diagnosis and treatment intake interface",
          "Binary adjudication logger (CONFIRM [True Positive] vs. OVERRIDE [False Positive])",
          "Curated ground-truth clinical repository",
          "Background batch classifier retraining service (Gradient Boosted Trees / Random Forest)"],
         "Captures veterinarian verdicts to periodically retrain secondary classifiers, improving field accuracy continuously over time."),

        ("9. Spatio-Temporal Regional Outbreak Aggregation Engine",
         "This module detects multi-farm epidemiological disease outbreaks at the community level.",
         ["Spatial clustering filter (Radius R = 5 to 10 km or GeoHash cells)",
          "Sliding temporal window accumulator (ΔT = 48 to 72 hours)",
          "Cluster Anomaly Index calculator (CAI = Σ Anomalies / Total Herd)",
          "Emergency outbreak broadcast dispatcher"],
         "Monitors correlated deviations across multiple independent farms. If CAI exceeds dynamic threshold Θ across >= M holdings, emergency alerts are dispatched to animal husbandry authorities.")
    ]

    for title, desc, comps, func in modules:
        p_mt = doc.add_paragraph()
        p_mt.paragraph_format.space_before = Pt(6)
        p_mt.paragraph_format.space_after = Pt(2)
        r_mt = p_mt.add_run(title)
        r_mt.bold = True; r_mt.font.name = "Calibri"; r_mt.font.size = Pt(11)

        add_p(desc, size=10.5, space_after=3)
        add_p("Components:", bold=True, size=10.5, space_after=2)
        for c in comps:
            add_p(f"• {c}", size=10, indent=0.3, space_after=1.5)
        add_p("Function:", bold=True, size=10.5, space_before=2, space_after=2)
        add_p(func, size=10, space_after=5)

    # 10. End-to-End Operational Flow
    add_p("10. End-to-End Operational Flow", bold=True, size=11, space_before=8, space_after=4)
    flow_steps = [
        "1. Cattle are registered in the cloud system and fitted with durable optical QR tokens.",
        "2. Multi-signal logs (milk, feed, activity, weight) are captured via mobile optical scan and manual entry.",
        "3. Asynchronous normalizer aligns disparate intervals via exponential time-decay filter.",
        "4. Rolling baseline engine builds individual mean vector μ and covariance matrix Σ once N >= 7 entries.",
        "5. Regularized Mahalanobis distance D_M is computed and mapped to bounded score S_CHDI.",
        "6. Abstention gate evaluates sample bounds and matrix conditioning, withholding score if ill-conditioned.",
        "7. Deviations in Watch/At-Risk bands trigger automated cases to assigned regional veterinarian with XAI explanations.",
        "8. Attending veterinarian examines animal and records formal Confirm/Override clinical verdict.",
        "9. Ground-truth clinical cases periodically retrain supervised classifier to refine detection thresholds.",
        "10. Spatio-temporal aggregator monitors multi-farm clusters to trigger community outbreak early warnings."
    ]
    for step in flow_steps:
        add_p(step, size=10, space_after=2.5)

    # 11. Example Scenario
    add_p("11. Example Scenario", bold=True, size=11, space_before=8, space_after=4)
    scen_text = (
        "A lactating dairy cow's daily milk yield and feed intake begin trending below its own established rolling baseline over 3 consecutive days "
        "(milk yield drops from 14.5 L to 9.2 L; feed intake drops from 18 kg to 11 kg), while body weight and activity scores remain temporarily within range. "
        "The CHDI module detects this correlated bivariate deviation, computing a composite score of 52 (placing the animal in the 'At-Risk' band). "
        "The explainability module identifies milk yield and feed intake as contributing 58% and 34% of the deviation respectively. "
        "An automated clinical case is routed to the assigned regional veterinarian, who reviews the trajectory, visits the farm, diagnoses early-stage subclinical ketosis, and confirms the flag as accurate (CONFIRM label). "
        "The verified case is logged into the ground-truth repository, refining future early-stage metabolic risk detection. "
        "Concurrently, if neighboring farms within a 5 km radius report concurrent feed/milk deviations, the regional aggregator evaluates cluster density to rule out contagious local feed contamination or viral spread."
    )
    add_p(scen_text, size=10, space_after=8)

    # j. Provide Drawings
    add_prompt_label("j.Provide Drawings, if any.",
                     "[Please note: Drawings need to be provided in 2-dimentional line drawing format, with  numerical labeling. We request you to provide the descriptive of numerical labeling below the drawings.]")

    figures = [
        ("FIGURE 1: SYSTEM HARDWARE AND LOGICAL ARCHITECTURE",
         "figure1_system_architecture.png",
         [("100", "Physical & Acquisition Tier"),
          ("102", "Cattle Tag with Optical Machine-Readable QR Token"),
          ("104", "Mobile Optical Camera Sensor"),
          ("106", "Farmer Manual Data Entry Interface"),
          ("108", "Optional Environmental/IoT Sensor Array"),
          ("200", "Edge / Client Application Tier"),
          ("202", "Optical Token Decoder"),
          ("204", "Multi-Signal Form Validator"),
          ("206", "Offline Data Buffer / Cache"),
          ("208", "Secure REST/WebSocket API Dispatcher"),
          ("300", "User Terminal Interfaces Tier"),
          ("302", "Farmer Mobile Monitoring Dashboard"),
          ("304", "Veterinarian Clinical Triage Portal"),
          ("306", "System Administrator & Outbreak Monitor"),
          ("308", "Multi-Channel Push/SMS Alert Gateway"),
          ("400", "Central Cloud Computing & Analytics Engine Tier"),
          ("402", "Asynchronous Multi-Rate Signal Normalizer"),
          ("404", "Personalized Rolling Baseline Generator"),
          ("406", "Regularized Covariance-Aware CHDI Calculator"),
          ("408", "Confidence-Aware Decision Abstention Gate"),
          ("410", "Two-Tier Explainability & Feature Attribution Engine"),
          ("412", "Closed-Loop Classifier Retraining Pipeline"),
          ("414", "Spatio-Temporal Regional Outbreak Aggregator"),
          ("500", "Secure Relational & Time-Series Storage Tier"),
          ("502", "Cattle Identity & Life Registry"),
          ("504", "Time-Series Physiological Metrics Database"),
          ("506", "Covariance & Baseline Matrices Repository"),
          ("508", "Curated Clinical Cases & Ground-Truth Registry"),
          ("510", "Spatial Outbreak Cluster Registry")]),

        ("FIGURE 2: END-TO-END OPERATIONAL WORKFLOW PIPELINE",
         "figure2_operational_workflow.png",
         [("Step 1", "Animal Registration & Optical Token Generation"),
          ("Step 2", "Asynchronous Multi-Signal Data Logging (Mobile Scan & Entry)"),
          ("Step 3", "Rolling Baseline Generation (Sample Count N >= N_min Validation)"),
          ("Step 4", "CHDI Metric Calculation & Confidence Abstention Evaluation"),
          ("Step 5", "Dual-Tier Feature Explainability & Automated Vet Incident Dispatch"),
          ("Step 6", "Veterinary Clinical Diagnosis & Binary Confirm/Override Adjudication"),
          ("Step 7", "Adaptive Supervised Classifier Retraining Pipeline"),
          ("Step 8", "Spatio-Temporal Multi-Farm Epidemiological Outbreak Aggregation")]),

        ("FIGURE 3: CHDI COMPUTATION & CONFIDENCE-AWARE ABSTENTION LOGIC FLOWCHART",
         "figure3_chdi_abstention_logic.png",
         [("301", "New Multi-Signal Observation Vector x(t) Intake"),
          ("302", "Sample Count Gate Evaluation (Is N >= N_min?)"),
          ("303", "Abstention Verdict Dispatch (Verdict Withheld; State = Formative Baseline)"),
          ("304", "Asynchronous Temporal Alignment & Exponential Decay Imputation"),
          ("305", "Covariance Matrix Condition Check (Is cond(Σ) > κ_max?)"),
          ("306", "Tikhonov Shrinkage Regularization (Σ_reg = Σ + λ * I)"),
          ("307", "Regularized Mahalanobis Distance Computation D_M"),
          ("308", "Bounded Health Score Mapping (S_CHDI = 100 * exp(-D_M / τ))"),
          ("309", "Normal Clinical Band Classification (S_CHDI >= 80)"),
          ("310", "Watch Clinical Band Classification (60 <= S_CHDI < 80)"),
          ("311", "At-Risk Clinical Band Classification (S_CHDI < 60)")]),

        ("FIGURE 4: CLOSED-LOOP ACTIVE LEARNING & CLINICAL RETRAINING ARCHITECTURE",
         "figure4_vet_active_learning.png",
         [("401", "At-Risk / Watch Incident Trigger with Feature Attribution Vector"),
          ("402", "Geographic Jurisdictional Case Dispatch Engine"),
          ("403", "Veterinary Triage & Physical Examination Terminal"),
          ("404", "Binary Clinical Adjudication Intake (Confirm [TP] vs Override [FP])"),
          ("405", "Audited Ground-Truth Clinical Evidence Repository"),
          ("406", "Periodic Batch Classifier Retraining Engine (GBDT/Random Forest)"),
          ("407", "Zero-Downtime Hot-Swap Inference Parameter Deployment")]),

        ("FIGURE 5: SPATIO-TEMPORAL REGIONAL OUTBREAK AGGREGATION PIPELINE",
         "figure5_regional_outbreak_engine.png",
         [("501", "Distributed Farm A Cattle Monitoring Node"),
          ("502", "Distributed Farm B Cattle Monitoring Node"),
          ("503", "Distributed Farm C Cattle Monitoring Node"),
          ("504", "Spatial-Temporal Aggregator (Radius R & Sliding Window ΔT)"),
          ("505", "Cluster Anomaly Index (CAI) Evaluation Against Threshold Θ"),
          ("506", "Routine Local Case Queue Management (Isolated Deviations)"),
          ("507", "Emergency Regional Outbreak Alert Broadcast Dispatcher")])
    ]

    for fig_title, img_name, labels in figures:
        p_ft = doc.add_paragraph()
        p_ft.paragraph_format.space_before = Pt(8)
        p_ft.paragraph_format.space_after = Pt(3)
        p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_ft = p_ft.add_run(fig_title)
        r_ft.bold = True; r_ft.font.name = "Calibri"; r_ft.font.size = Pt(11)

        img_p = os.path.join(fig_dir, img_name)
        if os.path.exists(img_p):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_p, width=Inches(5.8))

        p_desc_head = doc.add_paragraph()
        p_desc_head.paragraph_format.space_after = Pt(2)
        r_dh = p_desc_head.add_run("Descriptive of Numerical Labeling:")
        r_dh.bold = True; r_dh.font.name = "Calibri"; r_dh.font.size = Pt(9.5)

        # Table of labels (2 columns)
        t_lbl = doc.add_table(rows=len(labels), cols=2)
        t_lbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(t_lbl, color="CBD5E0", sz="4")
        for idx, (num, desc) in enumerate(labels):
            r = t_lbl.rows[idx]
            c0 = r.cells[0]; c1 = r.cells[1]
            c0.width = Inches(1.2); c1.width = Inches(5.2)
            set_cell_margins(c0, top=40, bottom=40, left=80, right=80)
            set_cell_margins(c1, top=40, bottom=40, left=80, right=80)
            p0 = c0.paragraphs[0]; r0 = p0.add_run(num); r0.bold = True; r0.font.size = Pt(9); r0.font.name = "Calibri"
            p1 = c1.paragraphs[0]; r1 = p1.add_run(desc); r1.font.size = Pt(9); r1.font.name = "Calibri"

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(6)

    # =========================================================================
    # 2. DISCLOSURE
    # =========================================================================
    add_p("2. Disclosure", bold=True, size=12, space_before=10, space_after=4)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.add_run("a. Has the invention ever been shown or used in public?  Yes  ").font.size = Pt(10.5)
    p.add_run("☒ No").bold = True

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.add_run("If yes, Where: ________________________       When: ________________________").font.size = Pt(10)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.add_run("b. Was any Confidentiality Agreement Signed regarding the invention?      Yes  ").font.size = Pt(10.5)
    p.add_run("☒ No").bold = True

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.add_run("c. Has this invention been publicly disclosed (e.g., paper presentation)?\n"
              "If yes, provide details on title of publication, or presented, Date of disclosure, Conference /Journal\n"
              "(Attach copies or drafts if available)                                          Yes  ").font.size = Pt(10)
    p.add_run("☒ No").bold = True

    # =========================================================================
    # 3. FOREIGN PATENT PROTECTION
    # =========================================================================
    add_p("3. Foreign Patent Protection", bold=True, size=12, space_before=8, space_after=4)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.add_run("a. Do you intend to pursue International Patent protection  Yes  ").font.size = Pt(10.5)
    p.add_run("☒ No").bold = True

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run("If  yes, list the countries in which you want to protect your invention:        [Leave blank if unsure]").font.size = Pt(10)

    # =========================================================================
    # 4. FUNDING & SPONSORSHIP
    # =========================================================================
    add_p("4. Funding & Sponsorship", bold=True, size=12, space_before=8, space_after=4)

    funding_items = [
        ("1. Was this invention developed with external funding: ", "No"),
        ("2. Funding Agency /Sponsor: ", "N A"),
        ("3. Grant or Contract number: ", "N A"),
        ("4. Principal investigator (PI): ", "[Faculty Guide / Project Supervisor Name], Department of Artificial Intelligence and Data Science, Sona College of Technology, Salem"),
        ("5. Are there any third -party obligations (e.g. collaborations, industry partners (if yes, provide details): ", "No")
    ]
    for q, a in funding_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r_q = p.add_run(q); r_q.bold = True; r_q.font.size = Pt(10); r_q.font.name = "Calibri"
        r_a = p.add_run(a); r_a.font.size = Pt(10); r_a.font.name = "Calibri"

    # =========================================================================
    # 5. COMMERCIAL POTENTIAL
    # =========================================================================
    add_p("5. Commercial potential:", bold=True, size=12, space_before=8, space_after=4)

    com_items = [
        ("1. Potential applications / Industries: ",
         "The invention can be applied in smallholder dairy farming, rural dairy cooperatives (e.g., Aavin, Amul), commercial herd management, veterinary telemedicine portals, livestock micro-insurance underwriting, and government animal husbandry epidemiological surveillance programs."),
        ("2. Known Competing technologies: ",
         "Known competing technologies include wearable IoT sensor devices (ear tags, smart collars, rumen boluses), RFID-based basic identification systems, manual paper records, and general-purpose management databases lacking predictive multivariate anomaly scoring."),
        ("3. Companies that may be interested in licensing this technology: ",
         "National Dairy Development Board (NDDB), State Milk Marketing Federations, agritech enterprise startups (Stellapps Technologies, MooFarm, Prompt Dairy Tech), livestock insurance providers (IFFCO-Tokio, Agriculture Insurance Company of India), and the Ministry of Fisheries, Animal Husbandry & Dairying (DAHD), Govt. of India.")
    ]
    for q, a in com_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r_q = p.add_run(q); r_q.bold = True; r_q.font.size = Pt(10); r_q.font.name = "Calibri"
        r_a = p.add_run(a); r_a.font.size = Pt(10); r_a.font.name = "Calibri"

    # =========================================================================
    # 6. INVENTORSHIP DECLARATION
    # =========================================================================
    add_p("6. Inventorship declaration:", bold=True, size=12, space_before=8, space_after=4)

    p_dec = doc.add_paragraph()
    p_dec.paragraph_format.space_after = Pt(4)
    r_dec = p_dec.add_run(
        "I/ we declare that the information provided in this form is accurate and complete to the best of my/our "
        "knowledge. I/ we agree to assign rights in this invention to Sona college of Technology, in accordance with "
        "institutional policy."
    )
    r_dec.font.size = Pt(10); r_dec.font.name = "Calibri"

    p_sig_lbl = doc.add_paragraph()
    p_sig_lbl.paragraph_format.space_after = Pt(4)
    r_sl = p_sig_lbl.add_run("Inventor Signature(s) [If there are more than two inventors enter the details below]:")
    r_sl.bold = True; r_sl.font.size = Pt(10); r_sl.font.name = "Calibri"

    # Table for 4 Inventors (3 Students + 1 Faculty Guide)
    t_inv = doc.add_table(rows=5, cols=5)
    t_inv.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_inv, color="CBD5E0", sz="4")

    # Header Row
    inv_headers = ["", "Inventor 1", "Inventor 2", "Inventor 3", "Inventor 4 (Faculty Guide)"]
    for idx, h in enumerate(inv_headers):
        c = t_inv.rows[0].cells[idx]
        set_cell_background(c, "F7FAFC")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]; r = p.add_run(h); r.bold = True; r.font.size = Pt(8.5); r.font.name = "Calibri"

    inv_rows_data = [
        ("a. Full Name",
         ["Sabari Karthick A", "Sivanarasimman S", "Sujeeth Y R", "[Faculty Guide / Mentor Name]"]),
        ("b. Designation &Department",
         ["Final-Year Student,\nAI & DS",
          "Final-Year Student,\nAI & DS",
          "Final-Year Student,\nAI & DS",
          "[Designation - e.g. Asst. Prof],\nAI & DS"]),
        ("c. Signature",
         ["___________________", "___________________", "___________________", "___________________"]),
        ("d. Date",
         ["___________________", "___________________", "___________________", "___________________"])
    ]

    for r_idx, (lbl, vals) in enumerate(inv_rows_data):
        row = t_inv.rows[r_idx + 1]
        c0 = row.cells[0]
        set_cell_background(c0, "F7FAFC")
        set_cell_margins(c0, top=60, bottom=60, left=60, right=60)
        p0 = c0.paragraphs[0]; r0 = p0.add_run(lbl); r0.bold = True; r0.font.size = Pt(8.5); r0.font.name = "Calibri"

        for c_idx, val in enumerate(vals):
            c = row.cells[c_idx + 1]
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            p = c.paragraphs[0]; r = p.add_run(val); r.font.size = Pt(8); r.font.name = "Calibri"

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)

    # Authorized Person
    p_auth = doc.add_paragraph()
    p_auth.paragraph_format.space_before = Pt(6)
    p_auth.paragraph_format.space_after = Pt(2)
    p_auth.add_run("Authorized Person:               Name: Dr. [HOD / Dean R&D Name]          Designation: Head of Department (AI & DS)\n"
                   "                                 Signature:   _____________________ \n"
                   "                                 Date:   _____________________").font.size = Pt(9.5)

    # Office use only
    add_p("Office use only:", bold=True, size=11, space_before=6, space_after=2)
    add_p("Disclosure number: SCT/CIPR/IDF/2026/______", size=9.5, space_after=2)
    add_p("Date received:      ____ / ____ / 2026", size=9.5, space_after=2)
    add_p("Next steps:         ☐ Approved for Prior Art Search   ☐ Recommended for Filing   ☐ Revision Required", size=9.5, space_after=4)

    # Save
    out_docx_1 = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent-1.docx"
    out_docx_rev = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Revised.docx"
    doc.save(out_docx_1)
    print(f"Successfully generated document following Patent Sample (1).pdf template at: {out_docx_1}")
    try:
        doc.save(out_docx_rev)
        print(f"Also saved copy at: {out_docx_rev}")
    except PermissionError:
        out_docx_fallback = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Final.docx"
        doc.save(out_docx_fallback)
        print(f"Could not overwrite {out_docx_rev} (open in Word); saved copy at: {out_docx_fallback}")

if __name__ == "__main__":
    build_patent_document()
