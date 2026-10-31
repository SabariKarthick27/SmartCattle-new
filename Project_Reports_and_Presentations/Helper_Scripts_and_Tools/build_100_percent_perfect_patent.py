import docx
import zipfile
import shutil
import os

def set_paragraph_clean_text(p, text):
    """Sets text on paragraph while preserving its style and first run's font properties."""
    text_runs = [r for r in p.runs if len(r._element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')) > 0]
    if text_runs:
        text_runs[0].text = text
        for r in text_runs[1:]:
            r.text = ""
    else:
        p.text = text

def set_cell_clean_text(cell, text):
    """Updates cell text while preserving cell paragraph styles and drawings."""
    if not cell.paragraphs:
        cell.text = text
        return
        
    # If it's a pure drawing cell (checkboxes without text), preserve
    drawing_count = len(cell._element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing'))
    if drawing_count > 0 and not cell.paragraphs[0].text.strip():
        return
        
    p0 = cell.paragraphs[0]
    set_paragraph_clean_text(p0, text)
    for p in cell.paragraphs[1:]:
        p_drawings = len(p._element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing'))
        if p_drawings == 0:
            set_paragraph_clean_text(p, "")

def build_complete_patent():
    template_file = 'Patent Sample (1).docx'
    temp_docx = 'temp_complete_built.docx'
    final_output_docx = 'QR_Based_Cattle_Management_Patent_Disclosure.docx'
    backup_docx = 'SmartCattle_Patent_Disclosure_Final.docx'
    
    doc = docx.Document(template_file)
    print(f"Loaded template with {len(doc.paragraphs)} paragraphs and {len(doc.tables)} tables.")
    
    # -------------------------------------------------------------
    # 1. PARAGRAPHS MAPPING (ALL 208 PARAGRAPHS)
    # -------------------------------------------------------------
    # Prior Art Comparisons
    set_paragraph_clean_text(doc.paragraphs[2], "Bowling et al., 2008:")
    set_paragraph_clean_text(doc.paragraphs[3], "Describes cattle identification and national livestock traceability systems. Conventional electronic traceability relies on passive low-frequency (LF) or ultra-high-frequency (UHF) RFID transponders requiring specialized, high-cost reader hardware and fixed antennas, making them economically infeasible for smallholder farmers with small herds.")
    
    set_paragraph_clean_text(doc.paragraphs[4], "Pereira et al., 2023:")
    set_paragraph_clean_text(doc.paragraphs[5], "Reviews RFID technology for livestock tracking and animal health monitoring. RFID offers non-line-of-sight electronic identification but lacks on-board physiological sensing, personalized baseline calculation, and multivariate anomaly detection, serving only as a static electronic identifier.")
    
    set_paragraph_clean_text(doc.paragraphs[6], "Bumbálek et al., 2025:")
    set_paragraph_clean_text(doc.paragraphs[7], "Compares computer-vision cattle-identification approaches, including body texture biometric recognition, numerical ear-tag OCR, and QR collar tags. The optical methods focus purely on identification accuracy without integrating physiological telemetry, dynamic baseline modeling, clinical disease anomaly detection, or closed-loop veterinary triage.")
    
    set_paragraph_clean_text(doc.paragraphs[8], "Kaur and Virk, 2025:")
    set_paragraph_clean_text(doc.paragraphs[9], "Presents an IoT smart neck-collar system with tri-axial accelerometers and digital thermometers for bovine respiratory disease and mastitis detection. Wearable IoT systems face severe operational bottlenecks including battery life constraints, sensor damage/loss from animal social interactions, and prohibitive hardware investment costs.")
    
    set_paragraph_clean_text(doc.paragraphs[10], "Kamphuis et al., 2010:")
    set_paragraph_clean_text(doc.paragraphs[11], "Studies decision-tree models for automatic mastitis detection using automated milking-system data. The approach applies rigid population-wide diagnostic thresholds without accounting for individual breed or lactation differences and lacks smartphone-based data collection interfaces for resource-constrained farms.")
    
    set_paragraph_clean_text(doc.paragraphs[12], "Subach and Shmeleva, 2022:")
    set_paragraph_clean_text(doc.paragraphs[13], "Discusses digital innovation and cloud data pipelines for livestock farming at a conceptual architectural level. It does not provide an individualized stochastic baseline engine, covariance-weighted anomaly distance metrics, or an explainable clinical decision-support mechanism.")
    
    set_paragraph_clean_text(doc.paragraphs[14], "Ahmad and Salamat, 2023:")
    set_paragraph_clean_text(doc.paragraphs[15], "Describes a web-based veterinary clinical management system with record keeping and vaccination reminders. The system functions merely as a passive data repository without automated physiological time-series analysis, early anomaly screening, or explainable triage prioritization.")
    
    set_paragraph_clean_text(doc.paragraphs[16], "Curti et al., 2023:")
    set_paragraph_clean_text(doc.paragraphs[17], "Reviews livestock monitoring devices and machine-learning applications across animal reproduction. The survey highlights that commercial solutions rely on expensive dedicated hardware and black-box algorithms that lack clinician explainability and automated case-dispatch integration.")
    
    set_paragraph_clean_text(doc.paragraphs[18], "Aquilani et al., 2022:")
    set_paragraph_clean_text(doc.paragraphs[19], "Reviews precision-livestock-farming technologies for pasture systems including GPS collars and thermography. Many approaches are difficult to deploy in smallholder tropical dairy operations due to rugged environmental conditions and high maintenance overhead.")
    
    set_paragraph_clean_text(doc.paragraphs[20], "Barriuso et al., 2018:")
    set_paragraph_clean_text(doc.paragraphs[21], "Presents a multi-agent wireless sensor network (WSN) using MQTT messaging for pasture cattle monitoring. It requires local sensor-network gateways and continuous hardware maintenance, creating cost barriers for resource-limited dairy cooperatives.")

    # General Overview & Keywords
    set_paragraph_clean_text(doc.paragraphs[25], "Provide a general overview of your invention, including specific keywords and phrases pertaining to the invention: [Briefly provide the basic understanding of the invention and also point out specific keywords.]")
    set_paragraph_clean_text(doc.paragraphs[27], "The present invention relates to a QR-based cattle management and health-monitoring platform for personalized livestock disease detection using a Composite Health Deviation Index (CHDI). The system assigns a low-cost, durable thermoplastic polyurethane (TPU) ear tag with a cryptographic 128-bit UUID Quick Response (QR) matrix to each animal, enabling smallholder farmers to retrieve digital medical histories and record daily multi-signal vitals (daily milk yield, feed consumption, rumination duration, core body temperature, and locomotion activity) using any commodity smartphone camera without expensive RFID readers. The computational backplane constructs personalized rolling moving-average baselines and evaluates multivariate anomaly departures across historical signal covariances using regularized Mahalanobis distance. A temporal trajectory tracking module computes 7-day regression slopes to detect subclinical mastitis, lameness, and metabolic disorders up to four days prior to acute symptom onset. The invention incorporates dual-tier Leave-One-Covariate-Out (LOCO) permutation feature explainability, an analytical data-sufficiency gate to avoid premature alerts, and an automated closed-loop clinical triage workflow that dispatches prioritized VetCase tickets and ingests verified veterinary feedback to continuously refine machine learning risk classifiers.")
    
    set_paragraph_clean_text(doc.paragraphs[29], "Specific Keywords and Phrases Pertaining to the Invention")
    keywords = [
        "QR-Based Cattle Identification",
        "Smartphone-Readable Ear Tag",
        "Personalized Health Baseline",
        "Composite Health Deviation Index (CHDI)",
        "Multivariate Anomaly Detection",
        "Mahalanobis Distance with Tikhonov Regularization",
        "Temporal Trajectory Tracking & Slope Regression",
        "Subclinical Disease Early Detection",
        "Dual-Tier Explainability & Permutation Attribution",
        "Data-Sufficiency Abstention Gate",
        "Closed-Loop Veterinary Case Dispatch",
        "Role-Based Farm & Cooperative Portal",
        "Longitudinal Electronic Medical Records",
        "Precision Livestock Farming (PLF)",
        "Supervised Feedback Machine Learning Refinement"
    ]
    for idx, kw in enumerate(keywords):
        set_paragraph_clean_text(doc.paragraphs[30 + idx], kw)

    # Improvements over Prior Art
    set_paragraph_clean_text(doc.paragraphs[53], "Describe how the invention is more beneficial or feasible over the prior art. [What are the advantages/improvements of the invention as compared to solutions provided by others]")
    
    set_paragraph_clean_text(doc.paragraphs[55], "Infrastructure-Light, Zero-Cost Optical Identification")
    set_paragraph_clean_text(doc.paragraphs[56], "Prior systems require expensive RFID readers, antennas, or active neck collars with high battery maintenance costs.")
    set_paragraph_clean_text(doc.paragraphs[57], "The invention uses a durable, weather-proof TPU ear tag with a cryptographic 128-bit UUID QR code readable by any commodity smartphone browser, eliminating capital hardware costs for smallholder farmers.")
    
    set_paragraph_clean_text(doc.paragraphs[58], "Adaptive Personalized Baseline vs. Rigid Population Norms")
    set_paragraph_clean_text(doc.paragraphs[59], "Existing livestock tools apply static, global threshold rules (e.g. fixed milk yield drop), ignoring breed, age, and individual baseline differences.")
    set_paragraph_clean_text(doc.paragraphs[60], "The invention constructs dynamic rolling moving-average baselines (mean, standard deviation) unique to each animal, isolating true physiological distress from natural individual variance.")
    
    set_paragraph_clean_text(doc.paragraphs[61], "Multivariate Covariance-Weighted Anomaly Detection (CHDI)")
    set_paragraph_clean_text(doc.paragraphs[62], "Traditional methods analyze single variables in isolation, missing correlated cross-signal distress patterns.")
    set_paragraph_clean_text(doc.paragraphs[63], "The invention calculates regularized Mahalanobis distance across the empirical 4x4 covariance matrix of all monitored signals, capturing multidimensional health departures in a normalized 0–100 index.")
    
    set_paragraph_clean_text(doc.paragraphs[64], "Early Subclinical Disease Onset Detection (4 Days in Advance)")
    set_paragraph_clean_text(doc.paragraphs[65], "Prior art detects bovine disease only when severe, end-stage clinical symptoms appear, leading to permanent milk yield loss.")
    set_paragraph_clean_text(doc.paragraphs[66], "The invention performs rolling 7-day least-squares linear slope regression over CHDI trajectories, detecting subtle subclinical incubation up to four days prior to acute clinical collapse.")
    
    set_paragraph_clean_text(doc.paragraphs[67], "Dual-Tier Explainability and Closed-Loop Veterinary Feedback")
    set_paragraph_clean_text(doc.paragraphs[68], "Commercial machine-learning livestock tools operate as black boxes without clear clinician explanations or clinical feedback capture.")
    set_paragraph_clean_text(doc.paragraphs[69], "The invention provides LOCO permutation feature attributions (plain-text farmer advisories and detailed z-score vet tables) and dispatches prioritized VetCase tickets that log verified diagnoses for continuous model retraining.")

    # Detailed Explanation Section
    set_paragraph_clean_text(doc.paragraphs[71], "i.Provide a detailed explanation of your invention: [Specifically describe all the element and components of the invention. Also describe how all the elements and components work together to form the invention. For more clarity and understanding, respective examples, diagrams, flowcharts, etc. may be provided]")
    
    # Module 1
    set_paragraph_clean_text(doc.paragraphs[72], "User and Multi-Tenant Farm Management Module")
    set_paragraph_clean_text(doc.paragraphs[73], "This module manages secure user registration, multi-tenant farm hierarchy, role-based access control, and cryptographic session security.")
    set_paragraph_clean_text(doc.paragraphs[74], "Components:")
    set_paragraph_clean_text(doc.paragraphs[75], "Multi-tenant tenant isolation engine")
    set_paragraph_clean_text(doc.paragraphs[76], "Role-Based Access Control (RBAC) coordinator (Farmer, Veterinarian, Admin)")
    set_paragraph_clean_text(doc.paragraphs[77], "Argon2id password hashing and JWT authentication gateway")
    set_paragraph_clean_text(doc.paragraphs[78], "Cooperative hierarchy and farm tenancy mapping database")
    set_paragraph_clean_text(doc.paragraphs[79], "Function:")
    set_paragraph_clean_text(doc.paragraphs[80], "Enables agricultural dairy cooperatives to oversee hundreds of distributed smallholder farms under a single administrative umbrella while strictly isolating herd records between individual farm tenancies.")
    
    # Module 2
    set_paragraph_clean_text(doc.paragraphs[83], "Animal Husbandry and QR Identification Module")
    set_paragraph_clean_text(doc.paragraphs[84], "This module manages cattle biographical records and generates secure optical identification tags.")
    set_paragraph_clean_text(doc.paragraphs[85], "Components:")
    set_paragraph_clean_text(doc.paragraphs[86], "Cattle profile registry (Breed taxonomy, date of birth, parity, reproductive status)")
    set_paragraph_clean_text(doc.paragraphs[87], "Cryptographic 128-bit UUID v4 token generator")
    set_paragraph_clean_text(doc.paragraphs[88], "High-density 2-D QR matrix vector generator (SVG/PNG)")
    set_paragraph_clean_text(doc.paragraphs[89], "Tag-to-profile binding and lifecycle registry")
    set_paragraph_clean_text(doc.paragraphs[90], "Function:")
    set_paragraph_clean_text(doc.paragraphs[91], "Creates tamper-resistant optical QR tags laser-etched onto TPU ear tags. The QR payload contains only an opaque secure URI token, preventing unauthorized clinical data disclosure while enabling instant browser lookup.")
    
    # Module 3
    set_paragraph_clean_text(doc.paragraphs[93], "Longitudinal Multi-Signal Telemetry Logging Module")
    set_paragraph_clean_text(doc.paragraphs[94], "This module provides field-optimized mobile interfaces for farmers to log daily multi-parameter physiological vitals.")
    set_paragraph_clean_text(doc.paragraphs[95], "Components:")
    set_paragraph_clean_text(doc.paragraphs[96], "Mobile web logging interface with offline caching")
    set_paragraph_clean_text(doc.paragraphs[97], "Multi-signal data capture fields (Milk Yield, Feed Intake, Rumination, Temp, Activity)")
    set_paragraph_clean_text(doc.paragraphs[98], "Biological plausibility validator and outlier filter")
    set_paragraph_clean_text(doc.paragraphs[99], "Automatic UTC timestamping and GPS metadata tagger")
    set_paragraph_clean_text(doc.paragraphs[100], "Data-source fidelity classifier (manual | qr_scan | sensor)")
    set_paragraph_clean_text(doc.paragraphs[101], "Function:")
    set_paragraph_clean_text(doc.paragraphs[102], "Captures daily physiological vitals directly at the animal's side. Validates biological bounds before writing to PostgreSQL storage, ensuring clean time-series telemetry for downstream analytics.")
    set_paragraph_clean_text(doc.paragraphs[103], "Enforces physiological boundary validation (e.g. daily milk yield 0–60 L, temperature 36.5–42.0 °C).")
    set_paragraph_clean_text(doc.paragraphs[104], "Synchronizes mobile field entries seamlessly with cloud backplane via REST API.")

    # Module 4
    set_paragraph_clean_text(doc.paragraphs[107], "Medical, Vaccination, and Deworming Management Module")
    set_paragraph_clean_text(doc.paragraphs[108], "This module maintains longitudinal clinical healthcare records, treatment regimens, and preventive vaccination schedules.")
    set_paragraph_clean_text(doc.paragraphs[109], "Components:")
    set_paragraph_clean_text(doc.paragraphs[110], "Clinical diagnosis and treatment prescription logger")
    set_paragraph_clean_text(doc.paragraphs[111], "Vaccination schedule engine with automated booster interval calculator")
    set_paragraph_clean_text(doc.paragraphs[112], "Mandatory drug withdrawal period countdown monitor")
    set_paragraph_clean_text(doc.paragraphs[113], "Preventive health compliance reminder system")
    set_paragraph_clean_text(doc.paragraphs[114], "Function:")
    set_paragraph_clean_text(doc.paragraphs[115], "Tracks lifetime medical interventions (e.g. FMD, Brucellosis, Anthrax, Blackleg), computes booster due dates, and monitors drug withdrawal periods to prevent antibiotic residues in commercial dairy supply chains.")
    set_paragraph_clean_text(doc.paragraphs[116], "Maintains chronological audit logs of all clinical treatments and veterinary prescriptions.")
    set_paragraph_clean_text(doc.paragraphs[117], "Generates automated compliance reminders for upcoming herd vaccination boosters.")
    set_paragraph_clean_text(doc.paragraphs[118], "Prevents contaminated milk delivery by monitoring drug withdrawal periods.")
    set_paragraph_clean_text(doc.paragraphs[119], "Provides complete electronic healthcare history for veterinary reference during farm visits.")
    set_paragraph_clean_text(doc.paragraphs[120], "Ensures full regulatory compliance with dairy cooperative health standards.")

    # Module 5
    set_paragraph_clean_text(doc.paragraphs[123], "Adaptive Baseline and Three-Stage CHDI Computation Engine")
    set_paragraph_clean_text(doc.paragraphs[124], "This computational core computes personalized physiological baselines and evaluates multivariate anomaly deviations.")
    set_paragraph_clean_text(doc.paragraphs[125], "Components:")
    set_paragraph_clean_text(doc.paragraphs[126], "Dynamic rolling moving-average baseline calculator (Window W=14)")
    set_paragraph_clean_text(doc.paragraphs[127], "Empirical 4x4 covariance matrix builder with Tikhonov regularization (lambda=1e-3)")
    set_paragraph_clean_text(doc.paragraphs[128], "Multivariate Mahalanobis distance calculator (D_M)")
    set_paragraph_clean_text(doc.paragraphs[129], "0–100 bounded CHDI normalization and severity band classifier")
    set_paragraph_clean_text(doc.paragraphs[130], "Function:")
    set_paragraph_clean_text(doc.paragraphs[131], "Establishes a personalized moving-average baseline (mean, standard deviation) for each animal and computes regularized Mahalanobis distance across historical covariance structures, outputting healthy (>=75), watch (50-74), or at-risk (<50) status.")

    # Module 6
    set_paragraph_clean_text(doc.paragraphs[134], "Temporal Trajectory and Trend Regression Module")
    set_paragraph_clean_text(doc.paragraphs[135], "This module analyzes health score trajectory dynamics over rolling time windows.")
    set_paragraph_clean_text(doc.paragraphs[136], "Components:")
    set_paragraph_clean_text(doc.paragraphs[137], "7-day rolling least-squares linear regression solver")
    set_paragraph_clean_text(doc.paragraphs[138], "Health slope (S) and trajectory velocity calculator")
    set_paragraph_clean_text(doc.paragraphs[139], "Trajectory state classifier (Improving, Stable, Deteriorating, Fluctuating)")
    set_paragraph_clean_text(doc.paragraphs[140], "Subclinical early-warning flag generator")
    set_paragraph_clean_text(doc.paragraphs[141], "Function:")
    set_paragraph_clean_text(doc.paragraphs[142], "Computes health degradation slopes over 7-day windows, distinguishing temporary dietary dips from chronic systemic illness to detect subclinical mastitis and metabolic disorders up to four days prior to acute onset.")

    # Module 7
    set_paragraph_clean_text(doc.paragraphs[147], "Dual-Tier Explainability and Permutation Attribution Module")
    set_paragraph_clean_text(doc.paragraphs[148], "This module decomposes complex multivariate anomalies into human-interpretable clinical explanations.")
    set_paragraph_clean_text(doc.paragraphs[149], "Components:")
    set_paragraph_clean_text(doc.paragraphs[150], "Leave-One-Covariate-Out (LOCO) permutation feature decomposition engine")
    set_paragraph_clean_text(doc.paragraphs[151], "Relative percentage factor contribution ranker")
    set_paragraph_clean_text(doc.paragraphs[152], "Dual-tier explanation translator (Plain Farmer Advisory & Clinical Vet Z-Score Matrix)")
    set_paragraph_clean_text(doc.paragraphs[153], "Visualization chart and attribution badge generator")
    set_paragraph_clean_text(doc.paragraphs[154], "Function:")
    set_paragraph_clean_text(doc.paragraphs[155], "Deconstructs mathematical Mahalanobis distance into relative percentage contributions (e.g. Milk: 34%, Rumination: 28%, Temp: 22%), providing transparent diagnostic rationales for farmers and veterinarians.")
    set_paragraph_clean_text(doc.paragraphs[156], "Translates mathematical deviations into plain-language actionable advice for smallholder farmers.")

    # Module 8
    set_paragraph_clean_text(doc.paragraphs[159], "Analytical Confidence and Data-Sufficiency Abstention Gate")
    set_paragraph_clean_text(doc.paragraphs[160], "This module evaluates sample depth to prevent premature false alarms during initial cattle enrollment.")
    set_paragraph_clean_text(doc.paragraphs[161], "Components:")
    set_paragraph_clean_text(doc.paragraphs[162], "Historical sample counter (Minimum N >= 7 over 5+ calendar days)")
    set_paragraph_clean_text(doc.paragraphs[163], "Analytical confidence scoring engine (Saturation constant W=14)")
    set_paragraph_clean_text(doc.paragraphs[164], "Explicit abstention protocol gatekeeper")
    set_paragraph_clean_text(doc.paragraphs[165], "Data-sufficiency status reporter")
    set_paragraph_clean_text(doc.paragraphs[166], "Function:")
    set_paragraph_clean_text(doc.paragraphs[167], "Safely withholds automated alarm scores when historical records are sparse (N < 7 or Confidence < 0.40), ensuring 100% false-alarm suppression during early post-enrollment calibration.")
    set_paragraph_clean_text(doc.paragraphs[168], "Maintains strict confidence scoring to ensure only statistically reliable anomaly alerts are dispatched.")

    # Module 9
    set_paragraph_clean_text(doc.paragraphs[171], "Role-Based Web Platform and Veterinary Dashboard")
    set_paragraph_clean_text(doc.paragraphs[172], "This responsive web application provides tailored interfaces for herd monitoring and clinical triage.")
    set_paragraph_clean_text(doc.paragraphs[173], "Components:")
    set_paragraph_clean_text(doc.paragraphs[174], "Farmer mobile portal with herd summary and quick QR logger")
    set_paragraph_clean_text(doc.paragraphs[175], "Regional veterinarian triage dashboard with prioritized alert queue")
    set_paragraph_clean_text(doc.paragraphs[176], "Interactive longitudinal CHDI trajectory and telemetry charts")
    set_paragraph_clean_text(doc.paragraphs[177], "Multi-farm administrative herd health analytics console")
    set_paragraph_clean_text(doc.paragraphs[178], "Function:")
    set_paragraph_clean_text(doc.paragraphs[179], "Delivers responsive, role-segregated interfaces for all dairy stakeholders, displaying live herd health heatmaps, prioritized triage queues, vaccination schedules, and interactive trajectory graphs.")

    # Module 10 / End-to-End Operational Flow
    set_paragraph_clean_text(doc.paragraphs[182], "Automated VetCase Dispatch and Closed-Loop Feedback Learning Module")
    set_paragraph_clean_text(doc.paragraphs[183], "1. The administrator registers users, farms, and veterinarian assignments.")
    set_paragraph_clean_text(doc.paragraphs[184], "2. The farmer registers each animal and receives a unique cryptographic QR ear tag.")
    set_paragraph_clean_text(doc.paragraphs[185], "3. The farmer scans the QR tag with a smartphone camera and logs daily vitals directly in the field.")
    set_paragraph_clean_text(doc.paragraphs[186], "4. The CHDI engine calculates individual baseline departures using covariance-weighted Mahalanobis distance.")
    set_paragraph_clean_text(doc.paragraphs[187], "5. The temporal regression module evaluates 7-day health slopes to detect early subclinical disease trends.")
    set_paragraph_clean_text(doc.paragraphs[188], "6. The LOCO explainability module ranks contributing physiological factors and verifies data sufficiency.")
    set_paragraph_clean_text(doc.paragraphs[189], "7. Critical health departures (CHDI < 50) automatically generate prioritized VetCase tickets for regional veterinarians.")
    set_paragraph_clean_text(doc.paragraphs[190], "8. The veterinarian records diagnosis, treatment, and follow-up, adding verified ground-truth to the ML retraining loop.")

    # -------------------------------------------------------------
    # 2. TABLES UPDATE (ALL 6 TABLES)
    # -------------------------------------------------------------
    # Table 0: Details of the Invention
    t0 = doc.tables[0]
    for c in t0.rows[1].cells:
        set_cell_clean_text(c, "a.  Title of the invention:\nQR-Based Cattle Management System for Personalized Health Monitoring and Decision Support")
    for c in t0.rows[2].cells:
        set_cell_clean_text(c, "b. Field of the invention [Broader subject area of the invention]:\nPrecision Livestock Farming, Internet of Things (IoT), Machine Learning, and Agricultural Veterinary Informatics")
    
    t0_novel = (
        "e. What is/are the Novel/New aspects of the invention: [Provide point-wise summary of what is new in the invention that is not known/practiced/reported previously]\n\n"
        "1. Zero-cost infrastructure-light animal identification using commodity smartphone-readable cryptographic 128-bit UUID QR ear tags.\n"
        "2. Adaptive Three-Stage Composite Health Deviation Index (CHDI) based on dynamic rolling EWMA baselines and covariance-weighted Mahalanobis distance.\n"
        "3. Temporal trajectory slope regression over 7-day windows to detect subclinical mastitis, lameness, and metabolic disorders up to four days prior to acute onset.\n"
        "4. Dual-tier Leave-One-Covariate-Out (LOCO) permutation feature explainability generating plain-language farmer advisories and granular veterinary z-score triage tables.\n"
        "5. Automated closed-loop clinical triage pipeline generating prioritized VetCase tickets with continuous ML model feedback refinement."
    )
    for c in t0.rows[5].cells:
        set_cell_clean_text(c, t0_novel)
        
    t0_prior = (
        "f. Is there any prior art for this invention: [Has the problem been solved/ Is the problem being solved in any other manner by others? Limitations and drawbacks of prior art]\n\n"
        "Prior art relies on expensive RFID transponders/readers, battery-constrained wearable IoT neck collars, or passive optical vision without health analytics. They apply rigid population-wide diagnostic thresholds, lack individualized baselines, lack explainability, and do not integrate automated closed-loop veterinary triage feedback."
    )
    for c in t0.rows[6].cells:
        set_cell_clean_text(c, t0_prior)

    # Table 1: Detailed Scenario
    t1 = doc.tables[1]
    t1_scenario = (
        "8. Operational Scenario & Verification Workflow:\n\n"
        "A smallholder dairy farmer scans Cow #C-08's TPU ear tag with a standard mobile browser. The farmer logs daily milk yield (23.1 L), rumination time (415 min), and core body temperature (39.2 °C). "
        "The CHDI analytics engine compares these multi-signal vitals against Cow #C-08's personalized 14-day baseline and sample covariance matrix, identifying a significant multivariate departure. "
        "The 7-day temporal trajectory detects an acute deteriorating slope (-2.1), and the LOCO permutation attribution module identifies milk yield drop (34%) and rumination suppression (28%) as primary contributors. "
        "As the score enters the critical At-Risk band (CHDI < 50), the system automatically creates a prioritized VetCase ticket and notifies the regional veterinarian. "
        "The attending veterinarian conducts an on-site clinical examination, confirms early-stage Acute Mastitis, prescribes targeted antibiotic therapy, and logs the clinical outcome. "
        "This confirmed ground-truth diagnosis is stored in the animal's permanent electronic health record and ingested into the ML feedback repository for continuous model refinement."
    )
    set_cell_clean_text(t1.rows[0].cells[0], t1_scenario)

    # Table 3: Funding & Commercial Potential
    t3 = doc.tables[3]
    t3_r0 = (
        "Funding & Sponsorship\n\n"
        "Was this invention developed with any external funding or sponsorship?: No (Institutional Research & Development, Sona College of Technology)\n\n"
        "Potential applications / Industries: Dairy farms, smallholder livestock cooperatives, rural veterinary hospitals, animal-health extension centers, precision livestock farming platforms, and livestock insurance agencies.\n\n"
        "Known Competing technologies: Proprietary RFID electronic ear tag systems, wearable IoT neck collars/accelerometers, sensor-network nodes, standalone desktop dairy registries, and computer-vision animal monitoring tools.\n\n"
        "3. Companies that may be interested in licensing this technology: Dairy cooperatives (e.g., AAVIN, Amul, NDDB, Hatsun), livestock herd management software companies, veterinary health providers, agricultural IoT solution providers, and cattle identification tag manufacturers.\n\n"
        "Principal investigator (PI): Mrs. J. Deepika\n\n"
        "Are there any third-party obligations (e.g. collaborations, industry partners (if yes, provide details): No"
    )
    t3_r1 = (
        "Commercial potential:\n\n"
        "Potential applications / Industries: Precision livestock farming, cooperative milk production societies, rural veterinary health extension networks, automated cattle insurance validation, and commercial dairy herd health management.\n\n"
        "Known Competing technologies: Proprietary RFID ear tags with costly readers, high-cost wearable IoT neck collars, manual paper-based health ledgers, and standalone herd software lacking adaptive multivariate anomaly analytics."
    )
    set_cell_clean_text(t3.rows[0].cells[0], t3_r0)
    set_cell_clean_text(t3.rows[1].cells[0], t3_r1)

    # Table 4: Licensing Companies & Inventorship Declaration
    t4 = doc.tables[4]
    t4_r0 = "3. Companies that may be interested in licensing this technology: Dairy cooperatives (Aavin, Amul, NDDB, Hatsun), veterinary health organizations, livestock farm management software companies, and agricultural IoT device providers."
    for cell in t4.rows[0].cells:
        set_cell_clean_text(cell, t4_r0)

    t4_decl = (
        "6. Inventorship declaration:\n\n"
        "I/ we declare that the information provided in this form is accurate and complete to the best of my/our knowledge. "
        "I/ we agree to assign rights in this invention to Sona College of Technology, in accordance with institutional policy.\n\n"
        "Inventor Signature(s) [If there are more than two inventors enter the details below]:"
    )
    for cell in t4.rows[1].cells:
        set_cell_clean_text(cell, t4_decl)

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
    doc.save(temp_docx)
    print(f"Saved intermediate file: {temp_docx}")

    # -------------------------------------------------------------
    # 3. ZIP INJECTION: Insert SmartCattle Diagram with Arrows into media/image2.png
    # -------------------------------------------------------------
    target_output_docx = 'SmartCattle_Patent_Disclosure_Perfect.docx'
    diagram_png = 'smartcattle_system_modules_diagram.png'
    with zipfile.ZipFile(temp_docx, 'r') as zin:
        with zipfile.ZipFile(target_output_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/media/image2.png':
                    print(f"Replacing {item.filename} with {diagram_png}")
                    with open(diagram_png, 'rb') as img_f:
                        zout.writestr(item.filename, img_f.read())
                else:
                    zout.writestr(item, zin.read(item.filename))

    print(f"SUCCESS: Generated final patent document at: {target_output_docx}")
    
    # Try updating the other filenames if not locked
    for alt_name in [final_output_docx, backup_docx]:
        try:
            shutil.copyfile(target_output_docx, alt_name)
            print(f"Updated: {alt_name}")
        except PermissionError:
            print(f"Notice: {alt_name} is currently open in Microsoft Word.")

if __name__ == "__main__":
    build_complete_patent()
