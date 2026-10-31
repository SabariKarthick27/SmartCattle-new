# Full dictionary mapping paragraph indices in Patent Sample (1).docx to exact SmartCattle content

SMARTCATTLE_PARAGRAPHS = {
    # 1. Prior Art Comparisons (f. Is there any prior art)
    2: "Bowling et al., 2008:",
    3: "Describes cattle identification and national livestock traceability systems. Conventional electronic traceability relies on passive low-frequency (LF) or ultra-high-frequency (UHF) RFID transponders requiring specialized, high-cost reader hardware and fixed antennas, making them economically infeasible for smallholder farmers with small herds.",
    
    4: "Pereira et al., 2023:",
    5: "Reviews RFID technology for livestock tracking and animal health monitoring. RFID offers non-line-of-sight electronic identification but lacks on-board physiological sensing, personalized baseline calculation, and multivariate anomaly detection, serving only as a static electronic identifier.",
    
    6: "Bumbálek et al., 2025:",
    7: "Compares computer-vision cattle-identification approaches, including body texture biometric recognition, numerical ear-tag OCR, and QR collar tags. The optical methods focus purely on identification accuracy without integrating physiological telemetry, dynamic baseline modeling, clinical disease anomaly detection, or closed-loop veterinary triage.",
    
    8: "Kaur and Virk, 2025:",
    9: "Presents an IoT smart neck-collar system with tri-axial accelerometers and digital thermometers for bovine respiratory disease and mastitis detection. Wearable IoT systems face severe operational bottlenecks including battery life constraints, sensor damage/loss from animal social interactions, and prohibitive hardware investment costs.",
    
    10: "Kamphuis et al., 2010:",
    11: "Studies decision-tree models for automatic mastitis detection using automated milking-system data. The approach applies rigid population-wide diagnostic thresholds without accounting for individual breed or lactation differences and lacks smartphone-based data collection interfaces for resource-constrained farms.",
    
    12: "Subach and Shmeleva, 2022:",
    13: "Discusses digital innovation and cloud data pipelines for livestock farming at a conceptual architectural level. It does not provide an individualized stochastic baseline engine, covariance-weighted anomaly distance metrics, or an explainable clinical decision-support mechanism.",
    
    14: "Ahmad and Salamat, 2023:",
    15: "Describes a web-based veterinary clinical management system with record keeping and vaccination reminders. The system functions merely as a passive data repository without automated physiological time-series analysis, early anomaly screening, or explainable triage prioritization.",
    
    16: "Curti et al., 2023:",
    17: "Reviews livestock monitoring devices and machine-learning applications across animal reproduction. The survey highlights that commercial solutions rely on expensive dedicated hardware and black-box algorithms that lack clinician explainability and automated case-dispatch integration.",
    
    18: "Aquilani et al., 2022:",
    19: "Reviews precision-livestock-farming technologies for pasture systems including GPS collars and thermography. Many approaches are difficult to deploy in smallholder tropical dairy operations due to rugged environmental conditions and high maintenance overhead.",
    
    20: "Barriuso et al., 2018:",
    21: "Presents a multi-agent wireless sensor network (WSN) using MQTT messaging for pasture cattle monitoring. It requires local sensor-network gateways and continuous hardware maintenance, creating cost barriers for resource-limited dairy cooperatives.",
    
    # 2. General Overview & Keywords
    25: "Provide a general overview of your invention, including specific keywords and phrases pertaining to the invention: [Briefly provide the basic understanding of the invention and also point out specific keywords.]",
    27: "The present invention relates to a QR-based cattle management and health-monitoring platform for personalized livestock disease detection using a Composite Health Deviation Index (CHDI). The system assigns a low-cost, durable thermoplastic polyurethane (TPU) ear tag with a cryptographic 128-bit UUID Quick Response (QR) matrix to each animal, enabling smallholder farmers to retrieve digital medical histories and record daily multi-signal vitals (daily milk yield, feed consumption, rumination duration, core body temperature, and locomotion activity) using any commodity smartphone camera without expensive RFID readers. The computational backplane constructs personalized rolling moving-average baselines and evaluates multivariate anomaly departures across historical signal covariances using regularized Mahalanobis distance. A temporal trajectory tracking module computes 7-day regression slopes to detect subclinical mastitis, lameness, and metabolic disorders up to four days prior to acute symptom onset. The invention incorporates dual-tier Leave-One-Covariate-Out (LOCO) permutation feature explainability, an analytical data-sufficiency gate to avoid premature alerts, and an automated closed-loop clinical triage workflow that dispatches prioritized VetCase tickets and ingests verified veterinary feedback to continuously refine machine learning risk classifiers.",
    
    29: "Specific Keywords and Phrases Pertaining to the Invention",
    30: "QR-Based Cattle Identification",
    31: "Smartphone-Readable Ear Tag",
    32: "Personalized Health Baseline",
    33: "Composite Health Deviation Index (CHDI)",
    34: "Multivariate Anomaly Detection",
    35: "Mahalanobis Distance with Tikhonov Regularization",
    36: "Temporal Trajectory Tracking & Slope Regression",
    37: "Subclinical Disease Early Detection",
    38: "Dual-Tier Explainability & Permutation Attribution",
    39: "Data-Sufficiency Abstention Gate",
    40: "Closed-Loop Veterinary Case Dispatch",
    41: "Role-Based Farm & Cooperative Portal",
    42: "Longitudinal Electronic Medical Records",
    43: "Precision Livestock Farming (PLF)",
    44: "Supervised Feedback Machine Learning Refinement",
    
    # 3. Advantages / Improvements over Prior Art
    53: "Describe how the invention is more beneficial or feasible over the prior art. [What are the advantages/improvements of the invention as compared to solutions provided by others]",
    
    55: "Infrastructure-Light, Zero-Cost Optical Identification",
    56: "Prior systems require expensive RFID readers, antennas, or active neck collars with high battery maintenance costs.",
    57: "The invention uses a durable, weather-proof TPU ear tag with a cryptographic 128-bit UUID QR code readable by any commodity smartphone browser, eliminating capital hardware costs for smallholder farmers.",
    
    58: "Adaptive Personalized Baseline vs. Rigid Population Norms",
    59: "Existing livestock tools apply static, global threshold rules (e.g. fixed milk yield drop), ignoring breed, age, and individual baseline differences.",
    60: "The invention constructs dynamic rolling moving-average baselines (μ, σ) unique to each animal, isolating true physiological distress from natural individual variance.",
    
    61: "Multivariate Covariance-Weighted Anomaly Detection (CHDI)",
    62: "Traditional methods analyze single variables in isolation, missing correlated cross-signal distress patterns.",
    63: "The invention calculates regularized Mahalanobis distance across the empirical 4x4 covariance matrix of all monitored signals, capturing multidimensional health departures in a normalized 0–100 index.",
    
    64: "Early Subclinical Disease Onset Detection (4 Days in Advance)",
    65: "Prior art detects bovine disease only when severe, end-stage clinical symptoms appear, leading to permanent milk yield loss.",
    66: "The invention performs rolling 7-day least-squares linear slope regression over CHDI trajectories, detecting subtle subclinical incubation up to four days prior to acute clinical collapse.",
    
    67: "Dual-Tier Explainability and Closed-Loop Veterinary Feedback",
    68: "Commercial machine-learning livestock tools operate as black boxes without clear clinician explanations or clinical feedback capture.",
    69: "The invention provides LOCO permutation feature attributions (plain-text farmer advisories and detailed z-score vet tables) and dispatches prioritized VetCase tickets that log verified diagnoses for continuous model retraining.",
    
    # 4. Detailed Explanation of Modules
    71: "i.Provide a detailed explanation of your invention: [Specifically describe all the element and components of the invention. Also describe how all the elements and components work together to form the invention. For more clarity and understanding, respective examples, diagrams, flowcharts, etc. may be provided]",
    
    # Module 1
    72: "User and Multi-Tenant Farm Management Module",
    73: "This module manages secure user registration, multi-tenant farm hierarchy, role-based access control, and cryptographic session security.",
    74: "Components:",
    75: "Multi-tenant tenant isolation engine",
    76: "Role-Based Access Control (RBAC) coordinator (Farmer, Veterinarian, Admin)",
    77: "Argon2id password hashing and JWT authentication gateway",
    78: "Cooperative hierarchy and farm tenancy mapping database",
    79: "Function:",
    80: "Enables agricultural dairy cooperatives to oversee hundreds of distributed smallholder farms under a single administrative umbrella while strictly isolating herd records between individual farm tenancies.",
    
    # Module 2
    83: "Animal Husbandry and QR Identification Module",
    84: "This module manages cattle biographical records and generates secure optical identification tags.",
    85: "Components:",
    86: "Cattle profile registry (Breed taxonomy, date of birth, parity, reproductive status)",
    87: "Cryptographic 128-bit UUID v4 token generator",
    88: "High-density 2-D QR matrix vector generator (SVG/PNG)",
    89: "Tag-to-profile binding and lifecycle registry",
    90: "Function:",
    91: "Creates tamper-resistant optical QR tags laser-etched onto TPU ear tags. The QR payload contains only an opaque secure URI token, preventing unauthorized clinical data disclosure while enabling instant browser lookup.",
    
    # Module 3
    93: "Longitudinal Multi-Signal Telemetry Logging Module",
    94: "This module provides field-optimized mobile interfaces for farmers to log daily multi-parameter physiological vitals.",
    95: "Components:",
    96: "Mobile web logging interface with offline caching",
    97: "Multi-signal data capture fields (Milk Yield, Feed Intake, Rumination, Temp, Activity)",
    98: "Biological plausibility validator and outlier filter",
    99: "Automatic UTC timestamping and GPS metadata tagger",
    100: "Data-source fidelity classifier (manual | qr_scan | sensor)",
    101: "Function:",
    102: "Captures daily physiological vitals directly at the animal's side. Validates biological bounds before writing to PostgreSQL storage, ensuring clean time-series telemetry for downstream analytics.",
    
    # Module 4
    107: "Medical, Vaccination, and Deworming Management Module",
    108: "This module maintains longitudinal clinical healthcare records, treatment regimens, and preventive vaccination schedules.",
    109: "Components:",
    110: "Clinical diagnosis and treatment prescription logger",
    111: "Vaccination schedule engine with automated booster interval calculator",
    112: "Mandatory drug withdrawal period countdown monitor",
    113: "Preventive health compliance reminder system",
    114: "Function:",
    115: "Tracks lifetime medical interventions (e.g. FMD, Brucellosis, Anthrax, Blackleg), computes booster due dates, and monitors drug withdrawal periods to prevent antibiotic residues in commercial dairy supply chains.",
    
    # Module 5
    123: "Adaptive Baseline and Three-Stage CHDI Computation Engine",
    124: "This computational core computes personalized physiological baselines and evaluates multivariate anomaly deviations.",
    125: "Components:",
    126: "Dynamic rolling moving-average baseline calculator (Window W=14)",
    127: "Empirical 4x4 covariance matrix builder with Tikhonov regularization (lambda=1e-3)",
    128: "Multivariate Mahalanobis distance calculator (D_M)",
    129: "0–100 bounded CHDI normalization and severity band classifier",
    130: "Function:",
    131: "Establishes a personalized moving-average baseline (μ, σ) for each animal and computes regularized Mahalanobis distance across historical covariance structures, outputting healthy (>=75), watch (50-74), or at-risk (<50) status.",
    
    # Module 6
    134: "Temporal Trajectory and Trend Regression Module",
    135: "This module analyzes health score trajectory dynamics over rolling time windows.",
    136: "Components:",
    137: "7-day rolling least-squares linear regression solver",
    138: "Health slope (S) and trajectory velocity calculator",
    139: "Trajectory state classifier (Improving, Stable, Deteriorating, Fluctuating)",
    140: "Subclinical early-warning flag generator",
    141: "Function:",
    142: "Computes health degradation slopes over 7-day windows, distinguishing temporary dietary dips from chronic systemic illness to detect subclinical mastitis and metabolic disorders up to four days prior to acute onset.",
    
    # Module 7
    147: "Dual-Tier Explainability and Permutation Attribution Module",
    148: "This module decomposes complex multivariate anomalies into human-interpretable clinical explanations.",
    149: "Components:",
    150: "Leave-One-Covariate-Out (LOCO) permutation feature decomposition engine",
    151: "Relative percentage factor contribution ranker",
    152: "Dual-tier explanation translator (Plain Farmer Advisory & Clinical Vet Z-Score Matrix)",
    153: "Visualization chart and attribution badge generator",
    154: "Function:",
    155: "Deconstructs mathematical Mahalanobis distance into relative percentage contributions (e.g. Milk: 34%, Rumination: 28%, Temp: 22%), providing transparent diagnostic rationales for farmers and veterinarians.",
    
    # Module 8
    159: "Analytical Confidence and Data-Sufficiency Abstention Gate",
    160: "This module evaluates sample depth to prevent premature false alarms during initial cattle enrollment.",
    161: "Components:",
    162: "Historical sample counter (Minimum N >= 7 over 5+ calendar days)",
    163: "Analytical confidence scoring engine (Saturation constant W=14)",
    164: "Explicit abstention protocol gatekeeper",
    165: "Data-sufficiency status reporter",
    166: "Function:",
    167: "Safely withholds automated alarm scores when historical records are sparse (N < 7 or Confidence < 0.40), ensuring 100% false-alarm suppression during early post-enrollment calibration.",
    
    # Module 9
    171: "Role-Based Web Platform and Veterinary Dashboard",
    172: "This responsive web application provides tailored interfaces for herd monitoring and clinical triage.",
    173: "Components:",
    174: "Farmer mobile portal with herd summary and quick QR logger",
    175: "Regional veterinarian triage dashboard with prioritized alert queue",
    176: "Interactive longitudinal CHDI trajectory and telemetry charts",
    177: "Multi-farm administrative herd health analytics console",
    178: "Function:",
    179: "Delivers responsive, role-segregated interfaces for all dairy stakeholders, displaying live herd health heatmaps, prioritized triage queues, vaccination schedules, and interactive trajectory graphs.",
    
    # Module 10
    182: "Automated VetCase Dispatch and Closed-Loop Feedback Learning Module",
    183: "1. The farmer scans the animal's QR ear tag and logs daily physiological vitals directly in the field.",
    184: "2. The telemetry logging module validates entries and streams data to the cloud database backplane.",
    185: "3. The CHDI engine calculates individual baseline departures using covariance-weighted Mahalanobis distance.",
    186: "4. The temporal regression module evaluates 7-day health slopes to detect early subclinical disease trends.",
    187: "5. The LOCO explainability module ranks contributing physiological factors and verifies data sufficiency.",
    188: "6. Critical health departures (CHDI < 50) automatically generate prioritized VetCase tickets for regional vets.",
    189: "7. The attending veterinarian performs an on-site clinical examination, confirms diagnosis, and logs treatment.",
    190: "8. Confirmed clinical ground-truth feedback is ingested to continuously retrain and refine supervised ML risk models."
}
