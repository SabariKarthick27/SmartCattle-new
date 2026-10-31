import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def clear_cell_and_get_first_paragraph(cell):
    """Clears all paragraphs in cell except the first, which is emptied and returned."""
    p_first = cell.paragraphs[0]
    p_first.text = ""
    # remove extra paragraphs
    for p in cell.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    return p_first

def add_styled_paragraph(cell, text="", font_name="Calibri", font_size=11, bold=False, italic=False, color_rgb=None, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.bold = bold
        run.italic = italic
        if color_rgb:
            run.font.color.rgb = color_rgb
    return p

def main():
    backup_path = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent-1-backup.docx"
    output_path = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent-1.docx"
    revised_path = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Revised.docx"
    fig_dir = r"c:\Project\SmartCattle new\patent_figures"

    doc = Document(backup_path)
    print(f"Loaded template from {backup_path}. Total tables: {len(doc.tables)}")

    # -------------------------------------------------------------------------
    # Table 1: Title of the invention
    # -------------------------------------------------------------------------
    t1_c1 = doc.tables[1].rows[0].cells[1]
    p = clear_cell_and_get_first_paragraph(t1_c1)
    run = p.add_run(
        "A SYSTEM AND COMPUTER-IMPLEMENTED METHOD FOR SENSOR-INDEPENDENT LIVESTOCK HEALTH MONITORING USING OPTICAL IDENTIFIERS AND COMPOSITE MULTIVARIATE DEVIATION ANALYSIS\n\n"
        "(Also known as: QR-Based Cattle Management System with AI-Driven Health Monitoring and Composite Health Deviation Index - CHDI)"
    )
    run.font.size = Pt(11)
    run.font.name = "Calibri"
    run.bold = True

    # -------------------------------------------------------------------------
    # Table 2: Field of the invention
    # -------------------------------------------------------------------------
    t2_c1 = doc.tables[2].rows[0].cells[1]
    p = clear_cell_and_get_first_paragraph(t2_c1)
    run = p.add_run(
        "Precision Livestock Farming (Animal Husbandry Technology), Artificial Intelligence, Machine Learning, and Veterinary Tele-Informatics\n"
        "(International Patent Classification [IPC]: A01K 29/00, G16H 50/20, G06N 20/00)"
    )
    run.font.size = Pt(11)
    run.font.name = "Calibri"

    # -------------------------------------------------------------------------
    # Table 3: Stage of development
    # -------------------------------------------------------------------------
    t3_c0 = doc.tables[3].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(t3_c0)
    run = p.add_run(
        "c.  Stage of development\n\n"
        "☐ Idea only        ☐ Proof of concept        ☒ Prototype        ☒ Tested        ☐ In use/deployed\n"
        "(Functional software prototype integrated with mobile optical QR scanner, cloud analytics API, and clinical vet portal tested on field cattle datasets)"
    )
    run.font.size = Pt(11)
    run.font.name = "Calibri"

    # -------------------------------------------------------------------------
    # Table 4: Is the invention based on (Product & Process)
    # -------------------------------------------------------------------------
    t4 = doc.tables[4].rows[0]
    # Cell 0: 'd.  Is the invention based on'
    # Cell 1: '☒ Product'
    # Cell 2: '☒ Process/Method' (Checked both to prevent Sec 3(k) CRI objection!)
    # Cell 3: '☐ Composition'
    # Cell 4: '☐ Other'
    p = clear_cell_and_get_first_paragraph(t4.cells[1])
    p.add_run("☒ Product").bold = True
    p = clear_cell_and_get_first_paragraph(t4.cells[2])
    p.add_run("☒ Process/Method").bold = True

    # -------------------------------------------------------------------------
    # Table 5: Novel/New aspects & Inventive step
    # -------------------------------------------------------------------------
    t5_c0 = doc.tables[5].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(t5_c0)
    p.add_run("e.  What is/are the Novel/New aspects of the invention? What is the inventive step?\n").bold = True

    novelty_points = [
        ("1. Sensor-Independent Optical Identifier Data Binding & Multi-Rate Ingestion",
         "Unlike conventional precision livestock monitoring systems requiring invasive or expensive wearable IoT devices (ear tags, boluses, collar accelerometers costing >$100/animal), this invention identifies each animal using a durable, low-cost optical 2D matrix (QR token) and ingests asynchronous multi-source data (manual farmer logs, mobile camera scan timestamps, and optional sensor inputs). An exponential decay interpolation filter reconciles disparate logging intervals (e.g., weekly weights vs. daily feed vs. twice-daily milk yields), eliminating hardware cost barriers while ensuring continuous data integrity."),

        ("2. Personalized Rolling Physiological Baseline Addressing Biological Non-Stationarity",
         "Instead of comparing animals against static breed or herd population averages (which fail due to significant natural variance across parity, age, and lactation stages), the system dynamically computes an individual rolling statistical expectation (mean vector μ and covariance matrix Σ) constructed strictly from each animal's own historical observations once a minimum registration sample threshold is reached."),

        ("3. Regularized Covariance-Aware Multivariate Anomaly Metric (CHDI)",
         "Cattle health signals exhibit strong natural physiological interdependencies (e.g., milk yield and feed intake drop concurrently during acute illness). The system combines deviations across weight, feed interval, activity, milk volume, and scan patterns into a Composite Health Deviation Index (CHDI) using a regularized Mahalanobis distance metric: D_M(x) = sqrt((x - μ)^T * (Σ + λ*I)^(-1) * (x - μ)), where λ is a ridge shrinkage parameter preventing singular covariance matrices from sparse metrics."),

        ("4. Strict Matrix-Condition & Confidence-Aware Decision Abstention Gate",
         "When historical records are insufficient (sample count N < N_min during onboarding) or when the empirical covariance matrix is ill-conditioned (condition number exceeds κ_max), the system mathematically withholds a healthy/at-risk verdict rather than issuing potentially erroneous speculative scores, drastically reducing false alarm fatigue among farmers."),

        ("5. Dual-Tier Explainable AI (XAI) Architecture",
         "The system decomposes the composite deviation vector into ranked feature contributions, automatically synthesizing two distinct presentation tiers: (i) an intuitive plain-language top-contributing factor for low-literacy smallholder farmers (e.g., 'Milk yield dropped 35% below baseline'), and (ii) a complete multidimensional deviation vector and trajectory chart for veterinary diagnostic terminals."),

        ("6. Closed-Loop Clinical Veterinarian Active Learning Pipeline",
         "Veterinarian confirmation (True Anomaly) or override (False Alarm / Contextual deviation like estrus or weather) of each system-flagged case is captured as audited ground-truth clinical outcome data. This curated data periodically retrains a secondary supervised classifier, enabling predictive accuracy to continuously improve from field-verified clinical outcomes."),

        ("7. Spatio-Temporal Multi-Farm Epidemiological Outbreak Aggregator",
         "Individual animal deviations are continuously cross-aggregated across discrete farms within geographic clusters (defined by spatial radius R or GeoHash cells) over a sliding temporal window (e.g., 72 hours). When the cluster anomaly density exceeds a dynamic threshold across multiple independent holdings, a regional outbreak alert is automatically distributed to animal husbandry authorities, regional veterinarians, and dairy cooperatives.")
    ]

    for title, desc in novelty_points:
        p_t = t5_c0.add_paragraph()
        p_t.paragraph_format.space_before = Pt(6)
        p_t.paragraph_format.space_after = Pt(2)
        r_t = p_t.add_run(title)
        r_t.bold = True
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)

        p_d = t5_c0.add_paragraph()
        p_d.paragraph_format.space_after = Pt(4)
        r_d = p_d.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(10.5)

    # -------------------------------------------------------------------------
    # Table 6: Prior Art
    # -------------------------------------------------------------------------
    t6_c0 = doc.tables[6].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(t6_c0)
    p.add_run("f.  Is there any prior art for this invention?\n").bold = True

    prior_arts = [
        ("Haladjian, J.; Haug, J.; Nüske, S.; and Bruegge, B. (2018). “A Wearable Sensor System for Lameness Detection in Dairy Cattle,” Multimodal Technologies and Interaction, 2(2), 27.",
         "This work uses a wearable motion sensor attached to the cow and builds an individual gait model to detect deviations associated with lameness. Distinction: It is strictly limited to gait/lameness monitoring and requires per-animal wearable body hardware; it does not describe QR/optical sensor-independent operation, a composite multi-signal CHDI metric, confidence-aware abstention, closed-loop veterinarian feedback retraining, or regional multi-farm epidemiological aggregation."),

        ("Suchak, V.; Rana, H.; Verma, A.; Dubey, N. K.; Jayswal, H. S.; Damodar, D.; and Patel, C. I. (2026). “IoT-Based Smart Cattle Health Monitoring System Using Machine Learning for Real-Time Anomaly Detection,” Lecture Notes in Networks and Systems, Vol. 1463, pp. 1-12.",
         "This work concerns IoT- and machine-learning-based cattle health monitoring. Distinction: It relies fully on physical electronic sensor-derived inputs and does not disclose the proposed optical QR/sensor-optional workflow, per-animal CHDI formulation with regularized covariance-aware distance scoring, confidence abstention, or veterinarian-confirmed adaptive retraining."),

        ("Modak et al. (2025). “Internet of Things-Based Health Surveillance Systems for Livestock: A Review of Recent Advances and Challenges,” IET Wireless Sensor Systems.",
         "This review describes the general wearable-livestock-monitoring field, including smart collars, temperature sensors, accelerometers, heart-rate sensors, microcontrollers, cloud platforms, and ML alerts. Distinction: The reviewed systems are predominantly hardware/wearable dependent and do not disclose the proposed QR-linked, asynchronous multi-rate logging workflow with CHDI scoring and clinical active learning."),

        ("Kasuga, Ryoichi; and Kasuga, Hisashi (2017). “Livestock Management System,” JP6203238B2, published 27 September 2017.",
         "This patent describes QR-code or barcode tags attached to livestock, scanned using a mobile device and matched with a management database for individual identification. Distinction: It provides static identification and database indexing support, but does not disclose AI-based multi-signal health-deviation scoring, covariance-aware CHDI computation, confidence-aware abstention, clinical feedback loops, or regional outbreak clustering."),

        ("Guice, David; Pugh, Warren; and Thompson, Noble (2002). “Method and System for Monitoring the Health and Status of Livestock and Other Animals,” US20020010390A1, published 24 January 2002.",
         "This document describes automated livestock-health monitoring using implanted wireless sensor elements measuring temperature, blood oxygen, activity, and heart rate. Distinction: It relies on high-cost implanted or wearable sensor hardware and fails to teach QR/sensor-independent operation, regularized CHDI scoring, abstention during sparse initial histories, or clinical feedback retraining."),

        ("Beckham, Tammy; Coats, Matthew; et al. (2022). “System and Method for Monitoring and Analyzing Animal Related Data,” US11243976B2, published 8 February 2022.",
         "This patent aggregates animal-related data, identifies a baseline, and compares collected data with that baseline for herd management. Distinction: It is a broad, centralized data platform; it does not specifically disclose optical QR-based smallholder health logging, regularized covariance-aware CHDI scoring, dynamic matrix condition abstention, or veterinarian-confirmed classifier retraining."),

        ("Diao, Shanghua; and Deng, Yingang (2021). “Livestock Health Monitoring Method and Device, Storage Medium and Electronic Equipment,” CN113488175A, published 8 October 2021.",
         "This patent uses an electronic tag containing temperature, acceleration, microphone, and heart-rate sensors with a trained health model. Distinction: It requires dedicated electronic sensing hardware and a pre-trained population model rather than an optical-first QR approach with personalized CHDI covariance baselines and explicit abstention."),

        ("Subramanian, Srinivas; Kamble, Ramdas; Pote, Supriya; Goel, Neeraj; and Sen, Swapna (2024). “IoT-Based Cattle Health and Heat Monitoring System,” WO2024009326A1, published 11 January 2024.",
         "This document describes wearable collar units using sensor data for activity, rumination, temperature, and heat alerts. Distinction: It mandates collar hardware and does not disclose a QR/manual-first workflow, a covariance-aware CHDI index, or veterinarian-confirmation-driven model retraining."),

        ("Mindel, Anatoly; and Cohen, Yossi (2025). “Monitoring Livestock in an Agricultural Pen,” US12266142B2, published 1 April 2025.",
         "This patent describes multi-camera pen monitoring identifying animals using tags/barcodes and estimating wellbeing from images. Distinction: It is principally fixed pen vision-based requiring expensive infrastructure; it does not teach asynchronous multi-rate manual/QR health logging, CHDI scoring, confidence abstention, or a veterinarian active-learning loop."),

        ("Chinese Patent Application CN121148662A (2025). “A Method for Identifying Dairy Cow Behavior Based on a Six-Axis Inertial Sensor,” published 14 November 2025.",
         "This patent describes cow behavior recognition using a six-axis inertial sensor, individual behavioral baseline, and deviation analysis. Distinction: It requires sensor-equipped body hardware; it does not disclose the proposed sensor-independent QR platform, regularized CHDI calculation, veterinarian override tracking, or regional multi-farm outbreak aggregation.")
    ]

    for title, desc in prior_arts:
        p_t = t6_c0.add_paragraph()
        p_t.paragraph_format.space_before = Pt(5)
        p_t.paragraph_format.space_after = Pt(2)
        r_t = p_t.add_run(title)
        r_t.bold = True
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10.5)

        p_d = t6_c0.add_paragraph()
        p_d.paragraph_format.space_after = Pt(4)
        r_d = p_d.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(10)

    # -------------------------------------------------------------------------
    # Table 7: General Overview & Keywords
    # -------------------------------------------------------------------------
    t7_c0 = doc.tables[7].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(t7_c0)
    p.add_run("g.  General overview of the invention, including specific keywords and phrases:\n").bold = True

    overview_text = (
        "The present invention relates to an AI-driven livestock health monitoring and clinical case management system that identifies each animal through an optical machine-readable token (QR tag) and evaluates its health using a Composite Health Deviation Index (CHDI) computed from asynchronous multi-source data (manual farmer logs, mobile optical scan timestamps, and optional IoT feeds), without requiring dedicated body-worn sensor hardware.\n\n"
        "The system establishes a personalized rolling baseline for each animal from its own historical time series (weight, daily feed, physical activity, and milk yield) once a minimum sample threshold is attained. It calculates real-time deviation from that baseline using a regularized covariance-aware Mahalanobis distance metric, mapping the result to a single composite health score (0–100) with an associated confidence metric. When insufficient historical data exists or when the covariance matrix is ill-conditioned, the system enforces a confidence-aware abstention mechanism, withholding speculative verdicts.\n\n"
        "Cases falling into 'Watch' or 'At-Risk' bands automatically generate clinical records routed to licensed regional veterinarians with a two-tier explainability vector (plain-language factors for farmers, multidimensional breakdowns for clinicians). The veterinarian's clinical confirmation or diagnostic override is captured as audited ground-truth data to periodically retrain a supervised classifier over time. Furthermore, individual deviations are geographically aggregated across discrete farm holdings in spatial-temporal clusters to trigger early-warning alerts for multi-farm disease outbreaks. The invention operates via role-specific mobile and web interfaces for Farmers, Veterinarians, and Administrators backed by a secure cloud database."
    )
    p_ov = t7_c0.add_paragraph()
    p_ov.add_run(overview_text).font.size = Pt(10.5)

    p_kw_title = t7_c0.add_paragraph()
    p_kw_title.paragraph_format.space_before = Pt(8)
    p_kw_title.add_run("Specific Keywords and Phrases Pertaining to the Invention:\n").bold = True

    keywords_list = [
        "QR-Based Animal Identification",
        "Sensor-Independent Precision Livestock Farming",
        "Personalized Non-Stationary Health Baseline",
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
    p_kw = t7_c0.add_paragraph()
    p_kw.add_run(" • " + "\n • ".join(keywords_list)).font.size = Pt(10)

    # -------------------------------------------------------------------------
    # Table 8: How invention is more beneficial or feasible
    # -------------------------------------------------------------------------
    t8_c0 = doc.tables[8].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(t8_c0)
    p.add_run("h.  How the invention is more beneficial or feasible over the prior art:\n").bold = True

    benefits = [
        ("1. Total elimination of wearable hardware cost barrier",
         "Prior precision-livestock systems require fitting every animal with an expensive wearable device (ear tag, collar, or bolus costing $80-$150 each), which is commercially unviable for smallholder farmers owning 1-5 cows. This invention functions from weather-resistant optical QR tags costing under $0.50 and accepts mobile-logged data, democratizing precision health monitoring while remaining fully compatible with optional IoT telemetry."),

        ("2. Personalized rolling baseline rather than population averages",
         "Prior art evaluates animals against generalized breed/herd norms that produce high false-positive rates due to natural variations across age, parity, and lactation cycle. This invention builds a personalized non-stationary baseline strictly from the animal's own longitudinal history, eliminating breed-specific calibration bias."),

        ("3. Regularized covariance-aware multivariate scoring instead of arbitrary heuristic weights",
         "Prior systems either monitor a single condition (e.g., lameness) or apply arbitrary static weights to individual metrics. This invention combines all physiological signals into a single CHDI score using a regularized Mahalanobis distance that accounts for the natural covariance structure of health parameters for that specific animal."),

        ("4. Explicit mathematical abstention drastically reduces false alarms",
         "Unlike systems that force a speculative classification upon receiving minimal entries, this invention evaluates sample size (N < N_min) and matrix condition number (cond(Σ) > κ_max) to withhold verdicts during formative periods, preserving farmer trust and preventing unnecessary clinical interventions."),

        ("5. Closed-loop clinical verification continuously refines accuracy",
         "Most prior systems operate as static detectors. This invention captures veterinarian confirm/override decisions as audited ground-truth labels and periodically retrains a secondary supervised classifier, allowing accuracy to improve autonomously from verified field outcomes."),

        ("6. Multi-farm epidemiological radar built from distributed individual data",
         "Prior art is isolated to single animals or single farms. This invention aggregates geo-tagged deviations across discrete farm holdings in spatial-temporal clusters, detecting correlated disease outbreaks days before traditional passive government reporting.")
    ]

    for title, desc in benefits:
        p_t = t8_c0.add_paragraph()
        p_t.paragraph_format.space_before = Pt(5)
        p_t.paragraph_format.space_after = Pt(2)
        r_t = p_t.add_run(title)
        r_t.bold = True
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)

        p_d = t8_c0.add_paragraph()
        p_d.paragraph_format.space_after = Pt(4)
        r_d = p_d.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(10.5)

    # -------------------------------------------------------------------------
    # Table 9: Detailed explanation of the invention
    # -------------------------------------------------------------------------
    t9_c0 = doc.tables[9].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(t9_c0)
    p.add_run("i.  Detailed explanation of the invention:\n").bold = True

    p_intro = t9_c0.add_paragraph()
    p_intro.add_run("1. Technical Architectural Modules:\nThe invention comprises ten interoperating hardware-interfaced modules:\n").bold = True

    detailed_modules = [
        ("Module 1 - Cattle Identification & Optical Token Registration Module",
         "Captures static biometric identity parameters (tag ID, breed, gender, date of birth/approximate age, purpose) for each animal at registration, generates a unique cryptographically salted 2D QR token linked to the animal's cloud record, and derives an age-group classification (calf, heifer, lactating adult, dry, senior). Initializes the health status in an explicit ABSTAIN state."),

        ("Module 2 - Asynchronous Multi-Signal Data Ingestion & Normalizer",
         "Accepts timestamped multi-source entries for body weight w(t), daily feed intake f(t), observed physical activity score a(t), milking volume m(t), and optical QR-scan events s(t). Asynchronous logging cadences (e.g., bi-daily milk vs. weekly weight) are aligned via an exponential decay interpolation filter to construct an observation vector x(t) = [w(t), f(t), a(t), m(t), s(t)]^T."),

        ("Module 3 - Personalized Rolling Baseline Forecasting Module",
         "Computes, per animal, an expected rolling mean vector μ and covariance matrix Σ from that animal's own historical observations over a sliding temporal window W (past 14-30 days) once a minimum-entry threshold N >= N_min (e.g., N >= 7 entries) is satisfied."),

        ("Module 4 - Regularized Covariance-Aware CHDI Scoring Module",
         "Computes the Composite Health Deviation Index (CHDI). To guarantee numerical stability against multicollinear health signals, the empirical covariance matrix is regularized via Tikhonov shrinkage: Σ_reg = Σ + λ * I, where λ > 0 is a ridge regularization parameter. The Mahalanobis deviation distance is computed as:\n"
         "      D_M(x) = sqrt( (x - μ)^T * (Σ_reg)^(-1) * (x - μ) )\n"
         "The composite health score S_CHDI is then normalized to an intuitive bounded scale [0, 100]:\n"
         "      S_CHDI = 100 * exp( - D_M / τ )\n"
         "where τ is a calibrated biological dispersion factor. Clinical bands are assigned: Normal (S >= 80), Watch (60 <= S < 80), and At-Risk (S < 60)."),

        ("Module 5 - Confidence-Aware Decision Abstention Gate",
         "Evaluates whether data sufficiency and signal consistency support a reliable verdict: (i) Sample count check: if N < N_min, returns ABSTAIN (Formative baseline); (ii) Matrix condition check: if condition number cond(Σ) > κ_max, returns ABSTAIN (Ill-conditioned covariance); (iii) Missing vital check: if critical parameter (feed or milk) is missing beyond tolerance window, returns ABSTAIN, eliminating false positive alerts."),

        ("Module 6 - Two-Tier Explainability & Feature Attribution Engine",
         "Decomposes the composite distance D_M into constituent marginal contributions: C_i = |x_i - μ_i| * |(Σ_reg^(-1) * (x - μ))_i|. Synthesizes: (i) an intuitive plain-language top-factor summary for smallholder farmers (e.g., 'Feed intake dropped 38% below baseline'), and (ii) a complete multidimensional deviation breakdown and trend vector for veterinary terminals."),

        ("Module 7 - Automated Veterinarian Triage & Case Routing Module",
         "Automatically generates a clinical incident record when an animal's CHDI status enters 'Watch' or 'At-Risk' bands, or upon farmer-initiated request. Routes the case to the assigned regional veterinarian based on geo-spatial jurisdiction, attaching signal trends, explainability outputs, and past medical history."),

        ("Module 8 - Closed-Loop Active Learning & Classifier Retraining Module",
         "The attending veterinarian examines the animal and logs clinical diagnosis, treatment administered, and an explicit binary adjudication: CONFIRM (True Anomaly) or OVERRIDE (False Alarm / Contextual deviation). Verified clinical cases are archived in a ground-truth database. A background retraining service periodically updates a secondary supervised classifier (Gradient Boosted Decision Trees / Random Forest) to refine detection boundaries over time."),

        ("Module 9 - Spatio-Temporal Regional Outbreak Aggregation Module",
         "Continuously cross-aggregates recent CHDI deviations across animals and discrete farms within spatial clusters (radius R or GeoHash cells) over a sliding temporal window ΔT (e.g., 72 hours). Calculates the Cluster Anomaly Index: CAI = (Σ At-Risk Animals in Cluster) / (Total Registered Herd in Cluster). When CAI >= Θ_threshold across >= M distinct farm holdings, an emergency regional outbreak alert is distributed to animal husbandry officials, regional veterinarians, and affected farmers."),

        ("Module 10 - Role-Based Telecommunication & Notification Layer",
         "Provides three role-specific interfaces—Farmer, Veterinarian, and Administrator—with cryptographically isolated access, real-time push/SMS alert dispatch, and offline caching.")
    ]

    for title, desc in detailed_modules:
        p_t = t9_c0.add_paragraph()
        p_t.paragraph_format.space_before = Pt(5)
        p_t.paragraph_format.space_after = Pt(2)
        r_t = p_t.add_run(title)
        r_t.bold = True
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)

        p_d = t9_c0.add_paragraph()
        p_d.paragraph_format.space_after = Pt(4)
        r_d = p_d.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(10)

    p_flow_title = t9_c0.add_paragraph()
    p_flow_title.paragraph_format.space_before = Pt(8)
    p_flow_title.add_run("2. End-to-End Operational Lifecycle:\n").bold = True

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
        p_s = t9_c0.add_paragraph()
        p_s.paragraph_format.space_after = Pt(3)
        p_s.add_run(s).font.size = Pt(10)

    p_scen_title = t9_c0.add_paragraph()
    p_scen_title.paragraph_format.space_before = Pt(8)
    p_scen_title.add_run("3. Example Field Validation Scenario:\n").bold = True

    scen_text = (
        "A lactating dairy cow's daily milk yield and feed intake begin trending below its own established rolling baseline over 3 consecutive days (milk yield drops from 14.5 L to 9.2 L; feed intake drops from 18 kg to 11 kg), while body weight and activity scores remain temporarily within range. The CHDI module detects this correlated bivariate deviation, computing a composite score of 52 (placing the animal in the 'At-Risk' band). The explainability module identifies milk yield and feed intake as contributing 58% and 34% of the deviation respectively. An automated clinical case is routed to the assigned regional veterinarian, who reviews the trajectory, visits the farm, diagnoses early-stage subclinical ketosis, and confirms the flag as accurate (CONFIRM label). The verified case is logged into the ground-truth repository, refining future early-stage metabolic risk detection. Concurrently, if neighboring farms within a 5 km radius report concurrent feed/milk deviations, the regional aggregator evaluates cluster density to rule out contagious local feed contamination or viral spread."
    )
    p_sc = t9_c0.add_paragraph()
    p_sc.add_run(scen_text).font.size = Pt(10)

    # -------------------------------------------------------------------------
    # Table 10: Drawings (Section 1.j)
    # -------------------------------------------------------------------------
    t10_c0 = doc.tables[10].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(t10_c0)
    p.add_run("j.  Provide Drawings, if any.\n").bold = True

    p_draw_intro = t10_c0.add_paragraph()
    p_draw_intro.add_run(
        "The following five formal patent drawings illustrate the architectural embodiments, mathematical logic, operational flows, and epidemiological clustering mechanisms of the present invention:\n"
    ).font.size = Pt(10.5)

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
         "The system evaluates the Cluster Anomaly Index (CAI). If CAI exceeds dynamic threshold Θ across multiple farms, a high-priority regional outbreak emergency alert is broadcast to government animal husbandry officials, regional veterinarians, and dairy cooperatives.")
    ]

    for title, img_name, desc in figures_info:
        img_path = os.path.join(fig_dir, img_name)

        p_t = t10_c0.add_paragraph()
        p_t.paragraph_format.space_before = Pt(10)
        p_t.paragraph_format.space_after = Pt(4)
        p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_t = p_t.add_run(title)
        r_t.bold = True
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)

        if os.path.exists(img_path):
            p_img = t10_c0.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=Inches(6.0))

        p_d = t10_c0.add_paragraph()
        p_d.paragraph_format.space_after = Pt(8)
        r_d = p_d.add_run("Detailed Description: " + desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(9.5)

    # -------------------------------------------------------------------------
    # Table 22: Principal Investigator (PI) / Faculty Project Supervisor
    # -------------------------------------------------------------------------
    t22_c0 = doc.tables[22].rows[0].cells[0]
    t22_c1 = doc.tables[22].rows[0].cells[1]
    clear_cell_and_get_first_paragraph(t22_c0).add_run("4. Principal Investigator (PI) / Faculty Project Supervisor").bold = True
    clear_cell_and_get_first_paragraph(t22_c1).add_run(
        "[Faculty Guide / Project Supervisor Name],\n"
        "Department of Artificial Intelligence and Data Science,\n"
        "Sona College of Technology, Salem - 636005"
    )

    # -------------------------------------------------------------------------
    # Table 25: Commercial Potential - Applications
    # -------------------------------------------------------------------------
    t25_c1 = doc.tables[25].rows[0].cells[1]
    p = clear_cell_and_get_first_paragraph(t25_c1)
    p.add_run(
        "• Smallholder dairy farming and rural dairy cooperatives (e.g., Aavin, Amul federations).\n"
        "• Commercial dairy herd management software and veterinary telemedicine portals.\n"
        "• Livestock micro-insurance underwriters (loss prevention & automated health verification).\n"
        "• Government Animal Husbandry Departments (epidemiological outbreak surveillance and disease containment programs).\n"
        "• Agricultural extension services and rural veterinary dispensaries."
    )

    # -------------------------------------------------------------------------
    # Table 26: Known competing technologies
    # -------------------------------------------------------------------------
    t26_c1 = doc.tables[26].rows[0].cells[1]
    p = clear_cell_and_get_first_paragraph(t26_c1)
    p.add_run(
        "• Wearable IoT sensor-based livestock monitoring systems (ear tags, collars, rumen boluses);\n"
        "• RFID-based cattle identification and traceability systems without AI analytics;\n"
        "• Static manual paper records and basic spreadsheet logging systems;\n"
        "• General-purpose livestock management databases lacking predictive multivariate anomaly scoring."
    )

    # -------------------------------------------------------------------------
    # Table 27: Licensing companies
    # -------------------------------------------------------------------------
    t27_c1 = doc.tables[27].rows[0].cells[1]
    p = clear_cell_and_get_first_paragraph(t27_c1)
    p.add_run(
        "• National Dairy Development Board (NDDB) and State Milk Marketing Federations;\n"
        "• Agritech enterprise startups (Stellapps Technologies, MooFarm, Prompt Dairy Tech);\n"
        "• Livestock insurance companies (Agriculture Insurance Company of India, IFFCO-Tokio, HDFC ERGO);\n"
        "• Department of Animal Husbandry and Dairying (DAHD), Ministry of Fisheries, Animal Husbandry and Dairying, Govt. of India."
    )

    # -------------------------------------------------------------------------
    # Table 31: Add Inventor 4 (Faculty Guide) to mirror Table 30
    # -------------------------------------------------------------------------
    t31 = doc.tables[31]
    # Check if already 3 columns or 2 columns
    if len(t31.columns) == 2:
        t31.add_column(Inches(2.5))
        print("Added column 3 to Table 31 for Inventor 4 (Faculty Guide)")

    # Set Inventor 4 details in Col 2 of Table 31
    clear_cell_and_get_first_paragraph(t31.rows[0].cells[2]).add_run("Inventor 4 (Faculty Guide)").bold = True
    clear_cell_and_get_first_paragraph(t31.rows[1].cells[2]).add_run("[Faculty Guide / Project Supervisor Name]")
    clear_cell_and_get_first_paragraph(t31.rows[2].cells[2]).add_run(
        "[Designation - e.g. Assistant Professor],\nDepartment of Artificial Intelligence and Data Science"
    )
    clear_cell_and_get_first_paragraph(t31.rows[3].cells[2]).add_run("_______________________")
    clear_cell_and_get_first_paragraph(t31.rows[4].cells[2]).add_run("_______________________")

    # -------------------------------------------------------------------------
    # Table 32: Authorized Person
    # -------------------------------------------------------------------------
    t32 = doc.tables[32]
    clear_cell_and_get_first_paragraph(t32.rows[0].cells[1]).add_run("Dr. [Head of Department / Dean R&D Name]")
    clear_cell_and_get_first_paragraph(t32.rows[1].cells[1]).add_run("Head of Department (AI & DS) / Dean (R&D) / IPR Coordinator, Sona College of Technology")

    # Save to original filename and revised filename
    doc.save(output_path)
    doc.save(revised_path)
    print(f"Successfully updated document in place at: {output_path}")
    print(f"Also saved copy at: {revised_path}")

if __name__ == "__main__":
    main()
