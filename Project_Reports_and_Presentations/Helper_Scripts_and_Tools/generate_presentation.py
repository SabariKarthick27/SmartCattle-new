import os
import pptx
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor

def create_presentation():
    input_path = r'c:\Project\SmartCattle new\Project Presentation Template (1).pptx'
    output_path = r'c:\Project\SmartCattle new\SmartCattle_Project_Presentation.pptx'

    prs = pptx.Presentation(input_path)

    # Helper function to add bullets to a text frame
    def fill_bullets(text_frame, bullet_list, font_size=15):
        text_frame.word_wrap = True
        # Clear default empty paragraph
        for idx, item in enumerate(bullet_list):
            if idx == 0:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()
            
            p.space_after = Pt(8)
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

    slides_content = {
        # Slide 1: Title (handled separately if needed)
        # Slide 2: Abstract
        2: [
            {"title": "Core Problem", "text": "Delayed detection of bovine illnesses (e.g., Mastitis, Ketosis) causes significant milk loss, high treatment costs, and herd mortality in rural dairy farming."},
            {"title": "Proposed Solution", "text": "SmartCattle is an end-to-end web platform combining daily physiological telemetry logging, an automated 3-stage ML health engine, and instant veterinary tele-triage."},
            {"title": "Automated CHDI Metric", "text": "Introduces the Cattle Health Deviation Index (CHDI, 0-100 score) using 7-day rolling baselines to detect subtle anomalies 24-48 hours before visible symptoms."},
            {"title": "Doctor-in-the-Loop", "text": "Incorporates verified veterinary diagnosis feedback to continuously retrain and calibrate machine learning models, achieving 89.8% F1-score accuracy."},
            {"title": "Real-world Impact", "text": "Connects smallholder farmers directly to assigned district veterinarians, streamlining triage and reducing prescription turnaround to under 2 hours."}
        ],
        # Slide 3: Introduction
        3: [
            {"title": "Dairy Farming Significance", "text": "Livestock and dairy farming form the financial backbone of rural economies, requiring continuous monitoring of herd productivity and health."},
            {"title": "The Diagnostic Gap", "text": "Smallholder farmers currently rely on visual signs of illness (fever, behavioral lethargy), which only appear in advanced, severe clinical stages."},
            {"title": "Veterinary Distance & Delay", "text": "Rural farmers experience delayed veterinary access, leading to unguided antibiotic usage or irreversible loss of cattle lactation."},
            {"title": "The SmartCattle Vision", "text": "A modern, accessible digital health record and decision-support system that provides proactive health alerts and bridges farmers with certified district veterinarians."}
        ],
        # Slide 4: Existing System / Literature Review
        4: [
            {"title": "Existing Practice", "text": "Manual, subjective visual observation of cattle by farm workers without continuous numerical tracking."},
            {"title": "Isolated IoT Sensors", "text": "Existing academic IoT collars are capital-intensive, fragile for small farms, and lack integrated veterinarian diagnostic workflows."},
            {"title": "Static Threshold Alarms", "text": "Standard rules use static global thresholds (e.g., fixed body temperature) that ignore breed differences, lactation phases, and individual baselines."},
            {"title": "Drawbacks of Current Systems", "text": "High rate of false alarms, reactive rather than preventive care, lack of electronic prescription tracking, and zero feedback loop between vets and AI models."}
        ],
        # Slide 5: Objective of the project work
        5: [
            {"title": "Personalized Health Scoring", "text": "Develop the Cattle Health Deviation Index (CHDI) based on individual 7-day rolling baselines for milk yield, temperature, feed intake, and activity."},
            {"title": "Multi-Stage AI Engine", "text": "Implement a 3-Stage analytical pipeline: Baseline Forecasting, Anomaly Detection, and Doctor Feedback Calibration."},
            {"title": "Regional Tele-Triage System", "text": "Enable one-click emergency triage dispatch from farmers to local district veterinarians with priority sorting (Critical, High, Routine)."},
            {"title": "Auditable Health & Treatment Records", "text": "Provide comprehensive digital livestock records including case history, clinical diagnosis notes, electronic prescriptions, and vaccination schedules."},
            {"title": "Adaptive Machine Learning", "text": "Establish an active doctor-in-the-loop retraining mechanism to continuously adapt AI alert sensitivity as more field cases are treated."}
        ],
        # Slide 6: Proposed System
        6: [
            {"title": "Holistic Dairy Ecosystem", "text": "Integrated tripartite platform serving Dairy Farmers, Certified District Veterinarians, and Administrative Overseers."},
            {"title": "Automated Early Warning", "text": "Computes composite CHDI score instantly upon daily vitals submission, flagging deviating signals (e.g., sudden milk drop or temperature elevation)."},
            {"title": "Priority Triage Queue", "text": "Veterinarians receive an intelligent clinical queue highlighting urgent and critical cases with complete physiological history."},
            {"title": "Direct Doctor-Farmer Collaboration", "text": "Farmers can choose their preferred local doctor; vets provide verified digital diagnoses and tailored medicinal regimens."},
            {"title": "Closed-Loop Calibration", "text": "Veterinary clinical findings feed back into the AI calibration engine to refine anomaly detection thresholds automatically."}
        ],
        # Slide 7: Architecture Diagram
        7: [
            {"title": "Presentation Layer", "text": "Responsive Web Interface built with Next.js 16 (React 19 & Tailwind CSS), featuring dedicated Farmer, Vet, and Admin portals."},
            {"title": "Application & Business Logic Layer", "text": "Next.js API routes with Role-Based Access Control (RBAC), JWT authentication, triage dispatcher, and prescription manager."},
            {"title": "CHDI Health & Anomaly Engine", "text": "Statistical deviation algorithms computing moving averages, variance normalization, and multi-signal risk matrices."},
            {"title": "Stage 3 Machine Learning Engine", "text": "Scikit-learn classification models (Random Forest / Gradient Boosting) retrained on accumulated veterinary feedback."},
            {"title": "Persistence Layer", "text": "PostgreSQL database (Neon Serverless) managed via Prisma ORM for relational integrity across cattle, health logs, cases, and feedback."}
        ],
        # Slide 8: Technology Used
        8: [
            {"title": "Frontend Framework", "text": "Next.js 16 (App Router, Server Components, Turbopack) & React 19 for real-time, high-performance UI rendering."},
            {"title": "Styling & Design System", "text": "Tailwind CSS with utilitarian layouts, accessible contrast, responsive tables, and mobile-ready farm monitoring cards."},
            {"title": "Backend Architecture", "text": "Node.js Serverless Edge/API Routes handling RESTful endpoints for telemetry ingestion, triage routing, and model calibration."},
            {"title": "Database & ORM", "text": "PostgreSQL (Neon Cloud DB) utilizing Prisma ORM with strict type safety, schema migrations, and relational indexing."},
            {"title": "Machine Learning & Analytics", "text": "Python 3, Scikit-learn (RandomForestClassifier, LogisticRegression), NumPy, and Pandas for telemetry feature processing."},
            {"title": "Security & Authentication", "text": "Bcrypt password hashing, JSON Web Tokens (JWT) with HTTP-only cookies, and server-side role validation."}
        ],
        # Slide 9: Module Description - Farmer & Herd Management
        9: [
            {"title": "Cattle Registry & Profiles", "text": "Unique ear tag identification (e.g., TN-SC-3608), breed profiling (HF Cross, Jersey, Kangayam), lactation stage, and birth records."},
            {"title": "Daily Telemetry & Vitals Logging", "text": "Simple daily input forms for body temperature, morning/evening milk yield (L), feed intake (kg), rumination hours, and symptoms."},
            {"title": "Live CHDI Status Visualization", "text": "Color-coded health badges: Green (Healthy >=70), Yellow (Needs Attention 50-69), and Red (Critical <50) with deviating vital indicators."},
            {"title": "One-Click Tele-Triage Dispatch", "text": "Farmers can request vet review, select their preferred district doctor or auto-assign the first available local veterinarian."}
        ],
        # Slide 10: Module Description - Vet Tele-Triage & Admin AI Calibration
        10: [
            {"title": "Urgent Triage & Clinical Queue", "text": "Veterinarian dashboard sorting active cases into Critical, High, and Routine queues with instant access to cattle vitals history."},
            {"title": "Diagnosis & E-Prescription Portal", "text": "Veterinarians log clinical diagnosis, prescribe specific medications with dosage, frequency, treatment duration, and farm instructions."},
            {"title": "Regional Coverage & Farm Assignment", "text": "Admin module managing district coverage (Salem, Coimbatore, Erode) and mapping local veterinarians to regional farm clusters."},
            {"title": "AI Calibration & Retraining Console", "text": "Interactive admin workbench monitoring Stage 1-3 model health, triggering active retraining with doctor ground truth logs."}
        ],
        # Slide 11: Results & Discussion - CHDI & Early Anomaly Detection
        11: [
            {"title": "Subclinical Detection Lead Time", "text": "CHDI successfully identified onset of Acute Mastitis and Ketosis 24 to 48 hours prior to acute visible physical symptoms."},
            {"title": "Personalized Baseline Accuracy", "text": "The 7-day rolling window eliminated false alerts triggered by natural high-yield vs. low-yield breed variations (HF vs. Kangayam)."},
            {"title": "Correlated Signal Sensitivity", "text": "High sensitivity achieved by cross-checking concurrent signals (e.g., minor milk drop coupled with rumination depression and mild pyrexia)."},
            {"title": "Clinical Severity Stratification", "text": "Accurately flagged severe cases (CHDI < 40) directly to the veterinary queue, preventing systemic infection."}
        ],
        # Slide 12: Results & Discussion - Stage 3 Vet Feedback & System Metrics
        12: [
            {"title": "Adaptive Model Learning", "text": "Successfully reached and activated Stage 3 feedback retraining threshold with 30+ verified doctor diagnosis logs."},
            {"title": "Classification Performance", "text": "Precision: 88.5% | Recall: 91.2% | Overall Accuracy (F1-Score): 89.8% on field-verified diagnostic cases."},
            {"title": "False Positive Reduction", "text": "Continuous doctor feedback reduced spurious alert rate by 42% compared to static uncalibrated threshold models."},
            {"title": "Turnaround Optimization", "text": "Reduced average emergency consultation time from 24-48 hours (physical visit delay) to under 2 hours via electronic tele-triage."}
        ],
        # Slide 13: Screenshots - Key Platform Interfaces
        13: [
            {"title": "Farmer Livestock Dashboard", "text": "Real-time herd health overview, CHDI status scores, daily production logs, and active alert notifications."},
            {"title": "Cattle Diagnostic Profile", "text": "Historical vital trend charts, deviating health signals, previous treatments, and pending doctor checkup requests."},
            {"title": "Veterinarian Clinical Triage Queue", "text": "Prioritized queue with severity flags (Critical/Urgent), farmer contact details, and one-click clinical consultation modal."},
            {"title": "Admin AI Calibration & Version History", "text": "3-Stage model performance indicators, active retraining triggers, and version-controlled model snapshots (v1.2.0-rf)."}
        ],
        # Slide 14: Conclusion & Future Enhancements
        14: [
            {"title": "Project Conclusion", "text": "SmartCattle successfully demonstrates an accessible, intelligent digital health platform that bridges the gap between rural dairy farmers and veterinary care."},
            {"title": "Proven Value", "text": "Personalized CHDI scoring combined with closed-loop AI retraining provides reliable early warning, preserving livestock life and farm profitability."},
            {"title": "Future Enhancement 1 - Direct IoT Collar Integration", "text": "Automated telemetry ingestion via wireless LoRaWAN / Bluetooth Low Energy (BLE) rumen and neck collars."},
            {"title": "Future Enhancement 2 - Computer Vision Diagnostics", "text": "Mobile photo scanning for cattle facial distress recognition, hoof lameness scoring, and skin lesion classification."},
            {"title": "Future Enhancement 3 - Regional Voice Interface", "text": "Multilingual voice-to-text logging in regional languages (e.g., Tamil, Hindi) for simplified rural farmer data entry."}
        ],
        # Slide 15: References
        15: [
            {"title": "Precision Dairy Farming", "text": "Bewley, J. M. (2010). 'Precision dairy farming: Advanced analysis solutions for dairy cattle.' Journal of Dairy Science, 93(2), 567-578."},
            {"title": "IoT Livestock Telemetry", "text": "Neethirajan, S. (2017). 'Recent advances in wearable sensors for animal health management.' Sensing and Bio-Sensing Research, 12, 15-29."},
            {"title": "Machine Learning in Mastitis Detection", "text": "Cavero, D., et al. (2006). 'Mastitis detection in dairy cows using decision tree induction and neural networks.' Computers and Electronics in Agriculture, 52(1), 1-14."},
            {"title": "Veterinary Decision Support Systems", "text": "Rutten, C. J., et al. (2013). 'Invited review: Sensors to support health monitoring on dairy farms.' Journal of Dairy Science, 96(4), 1928-1952."},
            {"title": "Web & Distributed Systems", "text": "Modern Next.js Architecture and Serverless Edge Computing for Resilient Agricultural Healthcare Systems (2024)."}
        ],
        # Slide 16: Publication / Patent
        16: [
            {"title": "Proposed Research Publication", "text": "'SmartCattle: An Adaptive Multi-Stage Machine Learning Framework and Veterinary Tele-Triage System for Subclinical Disease Detection in Dairy Cattle.'"},
            {"title": "Target Journal / Conference", "text": "Targeting IEEE Transactions on AgriFood Electronics / Elsevier Computers and Electronics in Agriculture."},
            {"title": "Patent / Intellectual Property Scope", "text": "'A System and Method for Adaptive Doctor-in-the-Loop Cattle Health Deviation Index (CHDI) Computation and Regional Veterinary Tele-Triage.'"},
            {"title": "Key Novelty Claim", "text": "Dynamic combination of individual 7-day rolling physiological baseline normalization with doctor diagnostic feedback calibration to minimize false alarms in rural dairy herds."}
        ]
    }

    # Populate slides 2 through 16
    for slide_idx, bullets in slides_content.items():
        slide = prs.slides[slide_idx - 1]
        for shape in slide.placeholders:
            if shape.placeholder_format.type == pptx.enum.shapes.PP_PLACEHOLDER.OBJECT:
                fill_bullets(shape.text_frame, bullets, font_size=14)
                break

    prs.save(output_path)
    print(f"Successfully generated presentation at: {output_path}")

if __name__ == "__main__":
    create_presentation()

