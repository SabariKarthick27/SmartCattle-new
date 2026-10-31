import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def clear_cell_and_get_first_paragraph(cell):
    """Clears all paragraphs in cell except the first, which is emptied and returned."""
    p_first = cell.paragraphs[0]
    p_first.text = ""
    for p in cell.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    return p_first

def add_p(cell, text="", font_name="Calibri", font_size=11, bold=False, italic=False, space_before=0, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        r = p.add_run(text)
        r.font.name = font_name
        r.font.size = Pt(font_size)
        r.bold = bold
        r.italic = italic
    return p

def main():
    backup_path = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent-1-backup.docx"
    fig_path = r"c:\Project\SmartCattle new\patent_figures\figure_master_system_architecture.png"
    
    doc = Document(backup_path)
    print(f"Loaded original tabular template. Tables count: {len(doc.tables)}")

    # -------------------------------------------------------------------------
    # Table 1: Title of the invention
    # -------------------------------------------------------------------------
    c = doc.tables[1].rows[0].cells[1]
    p = clear_cell_and_get_first_paragraph(c)
    r = p.add_run("QR-Based Cattle Management System with AI-Driven Health Monitoring and Composite Health Deviation Index (CHDI)")
    r.font.name = "Calibri"; r.font.size = Pt(11); r.bold = True

    # -------------------------------------------------------------------------
    # Table 2: Field of the invention
    # -------------------------------------------------------------------------
    c = doc.tables[2].rows[0].cells[1]
    p = clear_cell_and_get_first_paragraph(c)
    r = p.add_run("Artificial Intelligence, Machine Learning, and Precision Livestock Farming (Animal Husbandry Technology)")
    r.font.name = "Calibri"; r.font.size = Pt(11)

    # -------------------------------------------------------------------------
    # Table 3: Stage of development
    # -------------------------------------------------------------------------
    c = doc.tables[3].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    p.add_run("c.  Stage of development\n\n☐ Idea only        ☐ Proof of concept        ☒ Prototype        ☒ Tested        ☐ In use/deployed")

    # -------------------------------------------------------------------------
    # Table 4: Nature of invention (Product & Process)
    # -------------------------------------------------------------------------
    row4 = doc.tables[4].rows[0]
    p = clear_cell_and_get_first_paragraph(row4.cells[1])
    p.add_run("☒ Product").bold = True
    p = clear_cell_and_get_first_paragraph(row4.cells[2])
    p.add_run("☒ Process/Method").bold = True

    # -------------------------------------------------------------------------
    # Table 5: Novel/New aspects of the invention & Inventive Step
    # -------------------------------------------------------------------------
    c = doc.tables[5].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    p.add_run("e.  What is/are the Novel/New aspects of the invention? What is the inventive step?\n").bold = True

    novelty_points = [
        ("Sensor-Optional, QR-Based Health Identification and Data Capture",
         "Existing precision-livestock systems rely on expensive wearable IoT hardware (ear tags, collars, boluses) fitted to every animal. This invention identifies each animal through a low-cost, durable QR tag and accepts manually logged or QR-scan-linked data (weight, feed intake, activity, milk yield), removing the hardware cost barrier for smallholder dairy farmers while remaining sensor-compatible."),

        ("Personalized, Per-Animal Physiological Baseline",
         "Rather than comparing an animal against generalized herd or breed averages, the system constructs a rolling statistical baseline unique to each animal from its own historical data, accounting for natural physiological variations across age, parity, and lactation cycles."),

        ("Composite Health Deviation Index (CHDI) Scoring",
         "Deviations across multiple vitals (weight, feed intake, activity, milk yield, and scan frequency) are integrated into a single Composite Health Deviation Index using a covariance-aware distance calculation, capturing the natural correlation geometry of physiological signals."),

        ("Confidence-Aware Decision Abstention Mechanism",
         "When historical records are insufficient (e.g., newly registered animals) or signal variance is unstable, the system explicitly withholds a verdict rather than issuing potentially unreliable classifications, drastically minimizing false alarms."),

        ("Veterinarian-Verified Active Feedback Loop",
         "Clinical confirmation or override of each system-flagged case by attending veterinarians is captured as labeled outcome data to periodically retrain a supervised classifier, allowing predictive accuracy to continuously improve from verified field outcomes."),

        ("Regional Multi-Farm Outbreak Early-Warning Aggregation",
         "Individual health deviations are aggregated across farms within a geographic region. Correlated deviation patterns across multiple animals and discrete holdings automatically trigger regional alerts for early-stage disease outbreak containment.")
    ]

    for title, desc in novelty_points:
        add_p(c, title, bold=True, space_before=4, space_after=1, font_size=11)
        add_p(c, desc, space_after=4, font_size=10.5)

    # -------------------------------------------------------------------------
    # Table 6: Prior Art
    # -------------------------------------------------------------------------
    c = doc.tables[6].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    p.add_run("f.  Is there any prior art for this invention?\n").bold = True

    prior_arts = [
        ("Haladjian et al. (2018). “A Wearable Sensor System for Lameness Detection in Dairy Cattle,” Multimodal Tech. & Interaction, 2(2), 27.",
         "Uses a wearable motion sensor attached to the cow for lameness detection. Limitations: Limited strictly to lameness and requires per-animal wearable hardware; lacks QR/sensor-independent operation, composite multi-signal CHDI scoring, confidence abstention, and regional outbreak aggregation."),

        ("Suchak et al. (2026). “IoT-Based Smart Cattle Health Monitoring System Using Machine Learning for Real-Time Anomaly Detection,” LNNS, Vol. 1463.",
         "Covers IoT- and machine-learning-based cattle monitoring. Limitations: Fully reliant on physical sensor hardware; lacks the proposed low-cost QR workflow, per-animal CHDI covariance scoring, confidence abstention, or veterinarian-feedback retraining."),

        ("Kasuga & Kasuga (2017). “Livestock Management System,” JP6203238B2.",
         "Describes QR-code tags attached to livestock matched with a management database. Limitations: Only provides static identification lookups; does not disclose automated AI health deviation scoring, CHDI baseline forecasting, confidence abstention, or predictive triage."),

        ("Subramanian et al. (2024). “IoT-Based Cattle Health and Heat Monitoring System,” WO2024009326A1.",
         "Describes wearable collar units using sensor data for activity and health alerts. Limitations: Dependent on body-worn collar devices; lacks an optical sensor-independent workflow, regularized CHDI metric, and clinical active learning.")
    ]

    for title, desc in prior_arts:
        add_p(c, title, bold=True, space_before=4, space_after=1, font_size=10.5)
        add_p(c, desc, space_after=4, font_size=10)

    # -------------------------------------------------------------------------
    # Table 7: General Overview & Keywords
    # -------------------------------------------------------------------------
    c = doc.tables[7].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    p.add_run("g.  General overview of the invention, including specific keywords and phrases:\n").bold = True

    ov_text = (
        "The present invention relates to an AI-driven cattle health monitoring and management system that identifies each animal through a low-cost optical QR tag and evaluates health using a Composite Health Deviation Index (CHDI) computed from manually logged and QR-scan-linked data, without requiring wearable sensors. "
        "The system establishes a personalized rolling baseline for each animal from its own historical records (weight, feed intake, activity, and milk yield), computes real-time deviation from that baseline using a covariance-aware distance method, and expresses the result as a single composite score with an associated confidence level. "
        "Cases falling below healthy thresholds or during formative baseline periods trigger a confidence-aware abstention mechanism, withholding speculative labels. "
        "Flagged cases are routed to veterinarians with plain-language factor summaries; clinical confirmations or overrides are captured to periodically retrain a supervised classifier. "
        "Furthermore, deviations are aggregated across local farms to detect regional disease outbreaks early. The system operates via role-specific web interfaces for Farmers, Veterinarians, and Administrators."
    )
    add_p(c, ov_text, space_after=6, font_size=10.5)

    add_p(c, "Specific Keywords and Phrases Pertaining to the Invention:", bold=True, space_before=4, space_after=2, font_size=10.5)
    keywords = [
        "QR-Based Animal Identification",
        "Sensor-Optional Health Monitoring",
        "Personalized Physiological Baseline",
        "Composite Health Deviation Index (CHDI)",
        "Covariance-Aware Anomaly Detection",
        "Confidence-Aware Decision Abstention",
        "Veterinarian Feedback Loop / Active Learning",
        "Regional Outbreak Early-Warning Aggregation",
        "Explainable AI for Animal Health",
        "Precision Livestock Farming"
    ]
    add_p(c, " • " + "\n • ".join(keywords), space_after=4, font_size=10)

    # -------------------------------------------------------------------------
    # Table 8: How Invention is More Beneficial or Feasible
    # -------------------------------------------------------------------------
    c = doc.tables[8].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    p.add_run("h.  How the invention is more beneficial or feasible over the prior art:\n").bold = True

    benefits = [
        ("1. Total elimination of wearable hardware cost barrier",
         "Prior systems require expensive wearable hardware ($80-$150 per animal), which is unaffordable for smallholders. This invention functions from weather-resistant optical QR tags costing under $0.50, removing capital barriers while remaining sensor-compatible."),

        ("2. Personalized rolling baseline rather than population averages",
         "Prior art evaluates cattle against generalized breed or herd norms that trigger high false alarms due to natural biological variations. This invention builds an individualized rolling baseline strictly from the animal's own data history."),

        ("3. Covariance-aware multivariate scoring",
         "Rather than monitoring single vitals or assigning arbitrary heuristic weights, this invention combines multi-signal deviations into a single score using a covariance-aware distance calculation that reflects how vitals naturally move together."),

        ("4. Explicit abstention reduces false alarms",
         "Unlike systems that force classifications on minimal data, this invention withholds verdicts when data volume is insufficient, preserving farmer trust and preventing unnecessary clinical costs."),

        ("5. Continuous clinical verification improves accuracy",
         "Most prior art operates as a static rule detector. This invention captures veterinarian confirm/override decisions as labeled data to retrain the classifier on real field outcomes."),

        ("6. Multi-farm population-level outbreak radar",
         "Extends individual cattle tracking across neighboring farms in a region, automatically alerting authorities on correlated health deviations indicative of infectious outbreaks.")
    ]

    for title, desc in benefits:
        add_p(c, title, bold=True, space_before=4, space_after=1, font_size=10.5)
        add_p(c, desc, space_after=4, font_size=10)

    # -------------------------------------------------------------------------
    # Table 9: Detailed Explanation of the Invention
    # -------------------------------------------------------------------------
    c = doc.tables[9].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    p.add_run("i.  Detailed explanation of the invention:\n").bold = True

    add_p(c, "The invention comprises the following interoperating modules:", bold=True, space_after=4, font_size=10.5)

    modules = [
        ("1. Cattle Identification & Registration Module",
         "Captures identity details (tag ID, breed, gender, date of birth, purpose), generates a unique QR token linked to the animal's cloud profile, and initializes health status in an explicit ABSTAIN state."),

        ("2. Multi-Signal Data Logging Module",
         "Accepts timestamped milk yield, feed intake, activity score, body weight, and scan frequency via mobile optical QR scanning and farmer manual entry, with optional IoT input compatibility."),

        ("3. Personalized Baseline Forecasting Module",
         "Computes an expected rolling mean and covariance baseline strictly from the animal's own historical entries once a minimum threshold (N >= 7 entries) is achieved."),

        ("4. Composite Health Deviation Index (CHDI) Scoring Module",
         "Computes multivariate deviation from baseline using a regularized Mahalanobis distance metric: D_M = sqrt((x - μ)^T * (Σ + λ*I)^(-1) * (x - μ)), mapped to a bounded score (0–100) and categorized into Normal (>=80), Watch (60–79), and At-Risk (<60) bands."),

        ("5. Confidence-Aware Abstention Module",
         "Evaluates historical sample count and signal stability. If entries are insufficient or variance is ill-conditioned, the system returns an ABSTAIN state, avoiding false positive alerts."),

        ("6. Two-Tier Explainability Module",
         "Ranks signal-level contribution to deviations, displaying intuitive plain-language summaries for farmers and complete multidimensional breakdown charts for veterinarians."),

        ("7. Veterinarian Case Management & Active Feedback Module",
         "Automatically routes cases entering Watch or At-Risk bands to assigned regional veterinarians, capturing clinical diagnosis, treatments, and a binary Confirm/Override label as ground-truth training data."),

        ("8. Adaptive Classifier Retraining Module",
         "Periodically retrains a supervised classifier using accumulated veterinarian-confirmed outcomes to continuously refine health-risk prediction accuracy."),

        ("9. Regional Outbreak Aggregation Module",
         "Aggregates recent deviations across discrete farms within a geographic cluster. Correlated multi-farm anomalies exceeding a density threshold trigger an emergency regional disease alert.")
    ]

    for title, desc in modules:
        add_p(c, title, bold=True, space_before=3, space_after=1, font_size=10.5)
        add_p(c, desc, space_after=3, font_size=10)

    add_p(c, "End-to-End Operational Flow:", bold=True, space_before=5, space_after=2, font_size=10.5)
    flow_steps = [
        "1. Farmer registers animal and attaches optical QR tag; initial record initialized in ABSTAIN state.",
        "2. Farmer logs milk yield, feed intake, and activity via mobile camera scan and app interface.",
        "3. System establishes rolling baseline once minimum entries (N >= 7) accumulate.",
        "4. CHDI module computes ongoing deviation, confidence score, and clinical status.",
        "5. Watch and At-Risk cases route automatically to assigned veterinarians with explainability summaries.",
        "6. Veterinarian examines animal, administers care, and records clinical confirmation or override.",
        "7. Retraining module incorporates clinical feedback to continuously update model accuracy.",
        "8. Outbreak engine cross-correlates multi-farm data to alert on potential contagious outbreaks."
    ]
    for s in flow_steps:
        add_p(c, s, space_after=2, font_size=10)

    add_p(c, "Example Scenario:", bold=True, space_before=5, space_after=2, font_size=10.5)
    scen_text = (
        "A dairy cow's milk yield and daily feed intake trend downward over three consecutive days while its body weight and activity remain normal. "
        "The CHDI module detects this correlated bivariate deviation and places the animal in the 'Watch' band, identifying milk yield drop as the dominant factor. "
        "An automated clinical case is routed to the regional veterinarian, who reviews the trajectory, visits the animal, diagnoses early subclinical ketosis, and confirms the flag. "
        "This verified outcome is archived to refine future early detection, while the cow receives prompt care before severe lactation loss occurs."
    )
    add_p(c, scen_text, space_after=4, font_size=10)

    # -------------------------------------------------------------------------
    # Table 10: Drawings (Section 1.j) - EXACTLY ONE PERFECT DIAGRAM!
    # -------------------------------------------------------------------------
    c = doc.tables[10].rows[0].cells[0]
    p = clear_cell_and_get_first_paragraph(c)
    p.add_run("j.  Provide Drawings, if any.\n").bold = True

    add_p(c, "The invention is illustrated by the following representative system architecture and operational workflow drawing:", space_after=4, font_size=10.5)

    add_p(c, "FIGURE 1: SYSTEM ARCHITECTURE AND OPERATIONAL WORKFLOW (100)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=4, font_size=11)

    if os.path.exists(fig_path):
        p_img = c.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(fig_path, width=Inches(6.2))

    add_p(c, "Descriptive of Numerical Labeling:", bold=True, space_before=4, space_after=2, font_size=10)
    labels_desc = [
        "100 - Physical & Acquisition Tier: Includes cattle optical QR tag (102), mobile camera scanner (104), farmer manual entry interface (106), optional IoT inputs (108), and local offline buffer (110).",
        "200 - Central AI Analytics Engine: Houses token verifier (202), signal normalizer (204), rolling baseline model (206), covariance-aware CHDI calculator (208), confidence abstention filter (210), two-tier explainability engine (212), classifier retraining pipeline (214), regional aggregator (216), and secure database (218).",
        "300 - Farmer Interface Tier: Provides mobile monitoring dashboard (302), visual health status bands (304), plain-language factor alerts (306), and direct vet consultation requests (308).",
        "400 - Veterinary & Outbreak Tier: Provides clinical case queue (402), multivariate diagnostic radar (404), confirm/override feedback loop (406), and regional outbreak alert gateway (408)."
    ]
    for ld in labels_desc:
        add_p(c, "• " + ld, space_after=2, font_size=9.5)

    # -------------------------------------------------------------------------
    # Section 4: Funding & PI (Table 22)
    # -------------------------------------------------------------------------
    doc.tables[22].rows[0].cells[0].paragraphs[0].text = "4. Principal Investigator (PI) / Faculty Project Supervisor"
    doc.tables[22].rows[0].cells[1].paragraphs[0].text = "[Faculty Guide / Project Supervisor Name], Department of AI & DS, Sona College of Technology, Salem"

    # -------------------------------------------------------------------------
    # Section 5: Commercial Potential (Tables 25, 26, 27)
    # -------------------------------------------------------------------------
    doc.tables[25].rows[0].cells[1].paragraphs[0].text = (
        "Smallholder dairy farming, rural dairy cooperatives (e.g., Aavin, Amul), commercial herd management software, veterinary telemedicine portals, livestock micro-insurance underwriting, and government animal health monitoring programs."
    )
    doc.tables[26].rows[0].cells[1].paragraphs[0].text = (
        "Wearable IoT sensor systems (ear tags, collars, boluses), RFID identification systems without AI analytics, manual paper records, and general-purpose herd databases without multivariate health scoring."
    )
    doc.tables[27].rows[0].cells[1].paragraphs[0].text = (
        "National Dairy Development Board (NDDB), State Milk Federations, agritech startups (Stellapps, MooFarm, Prompt Dairy Tech), livestock insurance providers, and Department of Animal Husbandry and Dairying (DAHD), Govt. of India."
    )

    # -------------------------------------------------------------------------
    # Section 6: Inventorship (Table 31) - Add Inventor 4 (Faculty Guide)
    # -------------------------------------------------------------------------
    t31 = doc.tables[31]
    if len(t31.columns) == 2:
        t31.add_column(Inches(2.5))
        print("Added column 3 to Table 31 for Inventor 4 (Faculty Guide)")

    clear_cell_and_get_first_paragraph(t31.rows[0].cells[2]).add_run("Inventor 4 (Faculty Guide)").bold = True
    clear_cell_and_get_first_paragraph(t31.rows[1].cells[2]).add_run("[Faculty Guide / Project Supervisor Name]")
    clear_cell_and_get_first_paragraph(t31.rows[2].cells[2]).add_run("[Designation, e.g. Assistant Professor],\nDepartment of Artificial Intelligence and Data Science")
    clear_cell_and_get_first_paragraph(t31.rows[3].cells[2]).add_run("_______________________")
    clear_cell_and_get_first_paragraph(t31.rows[4].cells[2]).add_run("_______________________")

    # Table 32: Authorized Person
    t32 = doc.tables[32]
    clear_cell_and_get_first_paragraph(t32.rows[0].cells[1]).add_run("Dr. [Head of Department / Dean R&D Name]")
    clear_cell_and_get_first_paragraph(t32.rows[1].cells[1]).add_run("Head of Department (AI & DS) / Dean (R&D) / IPR Coordinator, Sona College of Technology")

    # Table 33: Office use only
    t33 = doc.tables[33]
    clear_cell_and_get_first_paragraph(t33.rows[0].cells[1]).add_run("SCT/CIPR/IDF/2026/______")
    clear_cell_and_get_first_paragraph(t33.rows[1].cells[1]).add_run("____ / ____ / 2026")
    clear_cell_and_get_first_paragraph(t33.rows[2].cells[1]).add_run("☐ Approved for Prior Art Search   ☐ Recommended for Filing   ☐ Revision Required")

    # Save to multiple targets safely
    save_targets = [
        r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Final.docx",
        r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent-1.docx",
        r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Revised.docx"
    ]
    for path in save_targets:
        try:
            doc.save(path)
            print(f"Successfully saved to: {path}")
        except PermissionError:
            print(f"Skipped saving {path} (currently open in another program).")

    fallback = r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Essential Tabular.docx"
    doc.save(fallback)
    print(f"Guaranteed clean copy saved to: {fallback}")

if __name__ == "__main__":
    main()
