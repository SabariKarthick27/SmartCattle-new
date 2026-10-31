import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def build_smartcattle_presentation():
    template_path = r'c:\Project\SmartCattle new\Project Presentation Template (1).pptx'
    output_path = r'c:\Project\SmartCattle new\SmartCattle_Final_Project_Presentation.pptx'

    prs = pptx.Presentation(template_path)

    # ----------------------------------------------------
    # Helper to populate bullets
    # ----------------------------------------------------
    def fill_bullets(text_frame, bullet_list, font_size=13, space_after=6):
        text_frame.word_wrap = True
        for idx, item in enumerate(bullet_list):
            if idx == 0:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()
            
            p.space_after = Pt(space_after)
            p.level = item.get('level', 0)
            
            # Title / Lead-in bold
            if 'title' in item and item['title']:
                run_title = p.add_run()
                run_title.text = item['title'] + ": "
                run_title.font.bold = True
                run_title.font.size = Pt(font_size)
                run_title.font.color.rgb = RGBColor(15, 23, 42) # Slate-900
            
            # Body text
            run_body = p.add_run()
            run_body.text = item.get('text', '')
            run_body.font.bold = False
            run_body.font.size = Pt(font_size)
            run_body.font.color.rgb = RGBColor(51, 65, 85) # Slate-700

    # ----------------------------------------------------
    # Slide 1: Title Slide
    # ----------------------------------------------------
    slide1 = prs.slides[0]
    for shape in slide1.shapes:
        if shape.name == 'Title 1':
            shape.text_frame.text = "SONA COLLEGE OF TECHNOLOGY, SALEM\nDepartment of Information Technology"
            for p in shape.text_frame.paragraphs:
                p.font.size = Pt(20)
                p.font.bold = True
                p.alignment = PP_ALIGN.CENTER
                p.font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == 'Subtitle 2':
            shape.text_frame.text = "SMARTCATTLE: AI-DRIVEN CATTLE HEALTH MONITORING & VETERINARY TELE-TRIAGE SYSTEM"
            p = shape.text_frame.paragraphs[0]
            p.font.size = Pt(22)
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER
            p.font.color.rgb = RGBColor(13, 148, 136) # Teal-600
        elif shape.name == 'TextBox 3':
            shape.text_frame.text = "Project Guide:\nMs. J. Deepika,\nAssistant Professor,\nDepartment of IT"
            for p in shape.text_frame.paragraphs:
                p.font.size = Pt(13)
                p.font.color.rgb = RGBColor(51, 65, 85)
            shape.text_frame.paragraphs[0].font.bold = True
        elif shape.name == 'TextBox 4':
            shape.text_frame.text = "Project Team Members:\nSabari Karthick A (61782323110093)\nSivanarasimman S (61782323110103)\nSujeeth Y R (61782323110107)"
            for p in shape.text_frame.paragraphs:
                p.font.size = Pt(13)
                p.font.color.rgb = RGBColor(51, 65, 85)
            shape.text_frame.paragraphs[0].font.bold = True

    # Add Logos to Slide 1 if available
    logo_path1 = r'c:\Project\SmartCattle new\extracted_images\slide_1_img_2.png'
    logo_path2 = r'c:\Project\SmartCattle new\extracted_images\slide_1_img_5.png'
    if os.path.exists(logo_path1):
        slide1.shapes.add_picture(logo_path1, Inches(0.8), Inches(0.4), height=Inches(0.9))
    if os.path.exists(logo_path2):
        slide1.shapes.add_picture(logo_path2, Inches(11.8), Inches(0.4), height=Inches(0.9))

    # ----------------------------------------------------
    # Slide Text Definitions (Slides 2 to 16)
    # ----------------------------------------------------
    slides_data = {
        # Slide 2: Abstract
        2: [
            {"title": "Low-Cost Optical Identification", "text": "Replaces expensive, fragile electronic wearable sensors with durable, weatherproof 2D QR ear tags for instant cattle lookup."},
            {"title": "Unified Digital Health Records", "text": "Consolidates cow profiles, lactation cycles, milk yield, feed intake, vaccination schedules, and clinical treatments into a single web application."},
            {"title": "Personalized Health Baselines", "text": "Learns the unique physiological baseline for each individual cow instead of relying on generic, misleading breed averages."},
            {"title": "Early Anomaly Scoring (CHDI)", "text": "Computes a Cattle Health Deviation Index (0–100) to detect illness (Mastitis, Ketosis, Pyrexia) 24 to 48 hours prior to acute clinical symptoms."},
            {"title": "Closed-Loop Tele-Triage & Retraining", "text": "Dispatches emergency cases directly to regional district veterinarians, incorporating doctor diagnosis feedback into an adaptive ML pipeline (89.8% F1-score)."}
        ],
        # Slide 3: Introduction
        3: [
            {"title": "Vital Economic Pillar", "text": "Dairy farming constitutes the livelihood and economic backbone of millions of smallholder rural households across Tamil Nadu and India."},
            {"title": "The Diagnostic Gap", "text": "Smallholder farmers currently depend on visible signs of sickness (severe milk drop, recumbency, high fever), which appear only in advanced, high-loss disease stages."},
            {"title": "Veterinary Distance & Delay", "text": "Rural geographic distance delays physical veterinary visits by 24–48 hours, encouraging unguided antibiotic misuse and permanent cattle mortality."},
            {"title": "The SmartCattle Vision", "text": "A proactive, zero-hardware web intelligence platform that pairs simple QR mobile logging with machine learning to bridge rural dairy farmers with qualified district veterinarians."}
        ],
        # Slide 4: Existing System / Literature Review
        4: [
            {"title": "Manual Observation Practice", "text": "Farmers rely on manual memory and paper notebooks; subtle subclinical health declines are routinely missed."},
            {"title": "High-Cost Wearable Sensors", "text": "Academic IoT neck collars and boluses cost $150–$300 per head, suffer battery exhaustion, and are unaffordable for smallholder farmers (Mahmud et al., 2021)."},
            {"title": "Static Global Thresholds", "text": "Existing rule-based tools use rigid global thresholds (e.g., fixed body temperature) that trigger frequent false alarms due to natural breed and seasonal variations."},
            {"title": "Absence of Doctor Feedback Loop", "text": "Traditional monitoring software lacks veterinary decision support; doctor clinical findings are never fed back to calibrate diagnostic models (Rutten et al., 2013)."}
        ],
        # Slide 5: Objective of the project work
        5: [
            {"title": "Zero-Hardware Animal Identification", "text": "Deploy printable weatherproof 2D QR ear tags enabling instant smartphone camera lookup with zero on-animal electronic sensor cost."},
            {"title": "Formulate Personalized CHDI Metric", "text": "Compute the Cattle Health Deviation Index (0–100) using individual 7-to-14 day rolling baselines for milk yield, temperature, feed, and rumination."},
            {"title": "Subclinical Disease Detection", "text": "Detect the onset of Acute Mastitis, Ketosis, and Bovine Pyrexia 24 to 48 hours before visible physical symptoms emerge."},
            {"title": "One-Click Regional Tele-Triage", "text": "Enable farmers to dispatch emergency triage requests to their preferred or nearest district veterinarians with priority sorting (Critical, High, Routine)."},
            {"title": "Digital Prescriptions & Treatment Tracking", "text": "Maintain an auditable record of veterinary diagnoses, prescribed medicines, dosages, treatment duration, and upcoming vaccination dates."},
            {"title": "Doctor-in-the-Loop Machine Learning", "text": "Continuously retrain and calibrate anomaly detection models using verified field diagnosis logs to suppress false alarms."}
        ],
        # Slide 6: Proposed System
        6: [
            {"title": "Tripartite Web Platform", "text": "Unified role-based ecosystem serving Dairy Farmers, Certified District Veterinarians, and Administrative Overseers."},
            {"title": "Instant Camera QR Logging", "text": "Farmers scan ear tags using any standard smartphone camera (zero app download required) to view cattle history and log daily vitals in seconds."},
            {"title": "3-Stage Analytical Pipeline", "text": "Stage 1: Individual Rolling Baseline Forecasting | Stage 2: Multivariate Anomaly Detection | Stage 3: Doctor Feedback Retraining."},
            {"title": "Automated Triage Stratification", "text": "Classifies cattle health into Healthy (≥80), Watch (60–79), and Critical (<60), automatically routing at-risk cases to the emergency veterinary queue."},
            {"title": "Regional Coverage Management", "text": "Admin module mapping qualified veterinarians to specific agricultural zones (Salem, Coimbatore, Erode) for localized, prompt emergency coverage."}
        ],
        # Slide 7: Architecture Diagram (Handled separately with image)
        7: [],
        # Slide 8: Technology Used
        8: [
            {"title": "Frontend Framework", "text": "Next.js 16 (React 19, Server & Client Components, Turbopack) delivering instant rendering and reactive health dashboards."},
            {"title": "Styling & UI Components", "text": "Tailwind CSS with high-contrast health status pills, accessible data tables, and mobile-responsive farmer touch interfaces."},
            {"title": "Backend Architecture", "text": "Node.js Serverless Edge/API Routes providing high-throughput RESTful endpoints for telemetry ingestion, triage dispatch, and calibration."},
            {"title": "Database & ORM Layer", "text": "PostgreSQL (Neon Cloud Serverless DB) managed via Prisma ORM for relational integrity across cattle, health logs, cases, and feedback."},
            {"title": "Machine Learning & Analytics", "text": "Python 3, Scikit-learn (RandomForestClassifier, LogisticRegression), NumPy, and Pandas for statistical anomaly scoring and feedback retraining."},
            {"title": "Security & Authentication", "text": "Bcrypt password hashing, JSON Web Tokens (JWT) with HTTP-only cookies, and server-side Role-Based Access Control (RBAC)."}
        ],
        # Slide 9: Module Description (Part 1 - Farmer, Farm & QR Tagging)
        9: [
            {"title": "Module 1 - User, Farm & Cattle Management", "text": "Multi-role registration (Farmer, Vet, Admin), comprehensive cow registry with ear tag ID (e.g. TN-SC-3608), breed profiling (HF Cross, Jersey, Kangayam), birth and lactation stage."},
            {"title": "Module 2 - QR Code Generation & Instant Tagging", "text": "Generates printable 2D QR ear tags linked to digital records. Farmers and visiting veterinarians scan using standard smartphone cameras for zero-click instant profile lookup."},
            {"title": "Module 3 - Daily Telemetry & Vitals Logging", "text": "Intuitive mobile forms for daily entry of morning/evening milk yield (Litres), feed intake (kg), core body temperature (°C), and rumination hours."}
        ],
        # Slide 10: Module Description (Part 2 - CHDI Analytics, Vet Triage & AI Calibration)
        10: [
            {"title": "Module 4 - Health Monitoring & CHDI Analytics", "text": "Calculates composite 0–100 health index based on rolling individual baselines: Healthy (≥80), Watch (60–79), and Critical (<60), highlighting deviating vital signals."},
            {"title": "Module 5 - Emergency Triage & Tele-Veterinary Portal", "text": "Prioritized queue displaying critical cattle cases, farmer contact, reported symptoms, and one-click diagnosis modal with e-prescriptions (medicine, dosage, treatment days)."},
            {"title": "Module 6 - Admin AI Model Calibration & Audit", "text": "Real-time workbench tracking Stage 1-3 model health, executing active model retraining with verified doctor feedback logs, and maintaining version history."}
        ],
        # Slide 11: Results & Discussion (Part 1 - CHDI Health Sensitivity & Lead Time)
        11: [
            {"title": "Subclinical Detection Lead Time", "text": "Successfully identified onset of Acute Mastitis and Ketosis 24 to 48 hours prior to acute visible physical symptoms and severe milk collapse."},
            {"title": "Individual Baseline Normalization", "text": "14-day/7-day rolling window eliminated false alerts triggered by high-yielding breeds (HF Cross) vs. indigenous drought breeds (Kangayam)."},
            {"title": "Correlated Parameter Sensitivity", "text": "High diagnostic accuracy achieved by cross-checking concurrent signals: subtle milk drop (≥15%) combined with rumination depression and mild pyrexia."},
            {"title": "Turnaround Optimization", "text": "Reduced emergency veterinary response time from traditional 24–48 hours (physical search) to under 2 hours via electronic tele-triage."}
        ],
        # Slide 12: Results & Discussion (Part 2 - Stage 3 Adaptive Learning & Benchmark Performance)
        12: [
            {"title": "Adaptive Model Learning", "text": "Successfully reached and activated Stage 3 feedback retraining threshold with 32 verified veterinarian diagnosis logs from Salem district."},
            {"title": "Empirical Classification Performance", "text": "Precision: 88.5% | Recall: 91.2% | Overall Accuracy (F1-Score): 89.8% on field-verified diagnostic cases."},
            {"title": "Spurious Alert Reduction", "text": "Continuous doctor feedback reduced false alarm rates by 42% compared to static uncalibrated threshold models."},
            {"title": "Production Deployment", "text": "Full system active and tested on Next.js 16 with sub-second API response times and encrypted database storage on Neon PostgreSQL."}
        ],
        # Slide 13: Screenshots (Handled separately with 4 images)
        13: [],
        # Slide 14: Conclusion & Future Enhancements
        14: [
            {"title": "Project Conclusion", "text": "SmartCattle provides a practical, zero-hardware digital livestock healthcare platform that connects rural dairy farmers with qualified district veterinarians."},
            {"title": "Demonstrated Clinical Value", "text": "Personalized CHDI scoring combined with closed-loop doctor feedback learning delivers trustworthy early warning, preserving animal lives and farm productivity."},
            {"title": "Future Enhancement 1 - Direct IoT Collar Telemetry", "text": "Automated ingestion via wireless LoRaWAN / Bluetooth Low Energy (BLE) neck collars for continuous sensor feeds."},
            {"title": "Future Enhancement 2 - Computer Vision Diagnostics", "text": "Mobile camera photo scanning for cattle facial grimace distress, hoof lameness detection, and dermatological lesion classification."},
            {"title": "Future Enhancement 3 - Regional Voice Assistant", "text": "Multilingual voice-to-text logging in regional languages (Tamil and Hindi) for low-literacy rural farmers."}
        ],
        # Slide 15: References
        15: [
            {"title": "[1] Mahmud et al. (2021)", "text": "M. S. Mahmud et al., 'A systematic review on deep learning for precision cattle farming,' Computers & Electronics in Agriculture, vol. 187."},
            {"title": "[2] Bumbálek et al. (2023)", "text": "J. Bumbálek, J. Pytel, and J. Císař, 'Dairy cow identification methods based on optical tags,' Computers & Electronics in Agriculture, vol. 204."},
            {"title": "[3] Xu et al. (2026)", "text": "X. Xu, B. Xiong, D. Liu, and H. Song, 'Non-contact technologies for cattle monitoring,' Computers & Electronics in Agriculture, vol. 216."},
            {"title": "[4] Rutten et al. (2013)", "text": "C. J. Rutten, A. G. Velthuis, and H. Hogeveen, 'Sensors to support health management on dairy farms,' Journal of Dairy Science, vol. 96(4)."},
            {"title": "[5] Lovarelli et al. (2020)", "text": "D. Lovarelli, J. Bacenetti, and M. Guarino, 'Precision livestock farming in dairy cattle: technology and applications,' Journal of Cleaner Production, vol. 248."}
        ],
        # Slide 16: Publication / Patent
        16: [
            {"title": "Proposed Research Publication", "text": "'SmartCattle: An Adaptive Multi-Stage Machine Learning Framework and Veterinary Tele-Triage System for Subclinical Disease Detection in Dairy Cattle.'"},
            {"title": "Target Journal / Conference Venues", "text": "Targeting IEEE Transactions on AgriFood Electronics / Elsevier Computers & Electronics in Agriculture."},
            {"title": "Patent / Intellectual Property Scope", "text": "'A System and Method for Adaptive Doctor-in-the-Loop Cattle Health Deviation Index (CHDI) Computation and Regional Veterinary Tele-Triage.'"},
            {"title": "Key Novelty Claim", "text": "Low-cost QR optical identification coupled with dynamic 7-day personalized baseline normalization and doctor feedback model recalibration to minimize false alarms in rural dairy herds."}
        ]
    }

    # Populate bullet slides (except Slide 7 and Slide 13)
    for slide_num, bullets in slides_data.items():
        if slide_num in [7, 13]:
            continue
        slide = prs.slides[slide_num - 1]
        for shape in slide.placeholders:
            if shape.placeholder_format.type == pptx.enum.shapes.PP_PLACEHOLDER.OBJECT:
                fill_bullets(shape.text_frame, bullets, font_size=13, space_after=6)
                break

    # ----------------------------------------------------
    # Slide 7: Architecture Diagram Image
    # ----------------------------------------------------
    slide7 = prs.slides[6]
    # Remove text placeholder if present or clear it
    for shape in list(slide7.shapes):
        if shape.is_placeholder and shape.placeholder_format.type == pptx.enum.shapes.PP_PLACEHOLDER.OBJECT:
            # Clear text
            shape.text_frame.text = ""
    arch_img_path = r'c:\Project\SmartCattle new\extracted_images\slide_5_img_1.png'
    if os.path.exists(arch_img_path):
        # Place diagram centered in content area
        slide7.shapes.add_picture(arch_img_path, Inches(0.8), Inches(1.3), width=Inches(11.7), height=Inches(5.2))

    # ----------------------------------------------------
    # Slide 13: Screenshots (2x2 Grid)
    # ----------------------------------------------------
    slide13 = prs.slides[12]
    for shape in list(slide13.shapes):
        if shape.is_placeholder and shape.placeholder_format.type == pptx.enum.shapes.PP_PLACEHOLDER.OBJECT:
            shape.text_frame.text = ""

    # 4 high-res screenshots
    ss_paths = [
        (r'c:\Project\SmartCattle new\extracted_images\slide_8_img_4.png', Inches(0.8), Inches(1.4), Inches(5.6), Inches(2.5), "Farmer Herd Records & Overview"),
        (r'c:\Project\SmartCattle new\extracted_images\slide_9_img_2.png', Inches(6.8), Inches(1.4), Inches(5.6), Inches(2.5), "QR Ear-Tag Generator & Mobile Scan"),
        (r'c:\Project\SmartCattle new\extracted_images\slide_10_img_3.png', Inches(0.8), Inches(4.1), Inches(5.6), Inches(2.5), "CHDI Health Analytics & Deviation Score"),
        (r'c:\Project\SmartCattle new\extracted_images\slide_11_img_3.png', Inches(6.8), Inches(4.1), Inches(5.6), Inches(2.5), "Clinical Alerts & Vet Triage Workbench")
    ]

    for path, left, top, w, h, caption in ss_paths:
        if os.path.exists(path):
            slide13.shapes.add_picture(path, left, top, width=w, height=h)
            # Add small caption below
            tb = slide13.shapes.add_textbox(left, top + h + Inches(0.02), w, Inches(0.3))
            p = tb.text_frame.paragraphs[0]
            p.text = caption
            p.font.size = Pt(10)
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER
            p.font.color.rgb = RGBColor(100, 116, 139)

    prs.save(output_path)
    print(f"Successfully generated final presentation at: {output_path}")

if __name__ == "__main__":
    build_smartcattle_presentation()

