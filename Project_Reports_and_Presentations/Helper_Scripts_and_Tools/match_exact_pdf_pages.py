import sys
import pypdf
import re

def analyze_pdf():
    reader = pypdf.PdfReader('SmartCattle_Mini_Project_Report_v6.pdf')
    total_pages = len(reader.pages)
    print(f"Total Pages in PDF: {total_pages}", flush=True)

    # In our document:
    # Pages 1..11 are Front Matter (i to xi)
    # Page 12 is Body Page 1 (Chapter 1)
    
    # Let's extract text for all pages
    page_texts = []
    for i, page in enumerate(reader.pages):
        raw_text = page.extract_text() or ""
        # Clean up whitespace
        clean_text = " ".join(raw_text.split())
        page_texts.append((i + 1, clean_text))

    def get_body_page(pdf_pg):
        # Front matter is pages 1..11
        # Body starts at pdf_pg 12 -> body page 1
        if pdf_pg >= 12:
            return str(pdf_pg - 11)
        roman = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi"]
        return roman[pdf_pg] if pdf_pg < len(roman) else str(pdf_pg)

    # Headings to locate
    toc_items = [
        ("1.1", "BACKGROUND AND DOMAIN CONTEXT"),
        ("1.2", "PROBLEM STATEMENT"),
        ("1.3", "MOTIVATION AND OBJECTIVES"),
        ("1.4", "SCOPE OF THE PROJECT"),
        ("1.5", "REPORT ORGANIZATION"),
        ("CHAPTER 2", "LITERATURE SURVEY"),
        ("2.1", "HISTORICAL EVOLUTION OF CATTLE MONITORING"),
        ("2.2", "WEARABLE IOT SENSOR ARCHITECTURES"),
        ("2.3", "THERMAL IMAGING AND OPTICAL SENSING"),
        ("2.4", "EDGE-AI AND IN-SITU TIME-SERIES INFERENCE"),
        ("2.5", "LONG-RANGE TELEMETRY AND MESH TOPOLOGIES"),
        ("2.6", "COMPUTER VISION AND LIVESTOCK BIOMETRICS"),
        ("2.7", "CLOUD DECISION ENGINES AND HERD ANALYTICS"),
        ("2.8", "SYNTHESIS AND IDENTIFIED RESEARCH GAPS"),
        ("CHAPTER 3", "SYSTEM ARCHITECTURE AND HARDWARE DESIGN"),
        ("3.1", "OVERALL MULTI-TIER SYSTEM ARCHITECTURE"),
        ("3.2", "HARDWARE TIER: BIOMETRIC COLLAR AND THERMAL POD"),
        ("3.3", "HARDWARE SELECTION RATIONALE"),
        ("3.4", "PIN MAPPING AND SENSOR BUS INTERFACES"),
        ("3.5", "COMMUNICATION PROTOCOLS AND TELEMETRY"),
        ("3.6", "BACKEND AND TIME-SERIES DATA ARCHITECTURE"),
        ("3.7", "CLUSTER AND HIGH-AVAILABILITY DEPLOYMENT"),
        ("CHAPTER 4", "SYSTEM IMPLEMENTATION AND METHODOLOGY"),
        ("4.1", "CHDI MATHEMATICAL ENGINE AND SCORE FORMULATION"),
        ("4.1.1", "Composite Metric Mathematical Breakdown"),
        ("4.1.2", "Confidence-Decay Temporal Attenuation"),
        ("4.1.3", "Clinical Risk Tiering and Dynamic Alerting"),
        ("4.1.4", "Explainable AI & Feature Attribution Engine"),
        ("4.2", "MULTI-TIER COMPUTE WORKFLOW"),
        ("4.3", "HARDWARE POWER BUDGET AND SENSOR TIMINGS"),
        ("4.4", "FIRMWARE ALGORITHMIC IMPLEMENTATION"),
        ("4.5", "WEARABLE FORM FACTOR AND ENCLOSURE DESIGN"),
        ("4.6", "CLOUD INGESTION PIPELINE AND MICROSERVICES"),
        ("4.7", "REAL-TIME EVENT STREAMING AND ALERT ROUTING"),
        ("4.8", "MULTI-TENANT WEB APPLICATION AND DASHBOARD"),
        ("4.9", "CORE PRODUCTION IMPLEMENTATION CODE"),
        ("4.9.1", "CHDI Anomaly Detection and Score Engine"),
        ("4.9.2", "Wearable Multi-Sensor ESP32 Firmware"),
        ("4.9.3", "QR Telemetry Ingestion API Service"),
        ("4.9.4", "Real-Time Health Analytics Dashboard"),
        ("CHAPTER 5", "EXPERIMENTAL RESULTS AND PERFORMANCE ANALYSIS"),
        ("5.1", "HARDWARE EXPERIMENTAL SETUP"),
        ("5.2", "TIME-SERIES AND ANOMALY DETECTION EVALUATION"),
        ("5.3", "FIELD TRIAL SENSOR TELEMETRY ANALYSIS"),
        ("5.4", "POWER CONSUMPTION AND BATTERY PROFILES"),
        ("5.5", "COMPARATIVE SYSTEM BENCHMARKING"),
        ("CHAPTER 6", "CONCLUSION AND FUTURE ENHANCEMENTS"),
        ("6.1", "KEY FINDINGS AND CONTRIBUTIONS"),
        ("6.2", "CURRENT LIMITATIONS"),
        ("6.3", "FUTURE RESEARCH DIRECTIONS"),
        ("REFERENCES", "REFERENCES"),
        ("APPENDIX", "APPENDIX")
    ]

    print("\n=== DETECTED TOC ITEM BODY PAGES ===")
    detected_toc = {}
    for code, title in toc_items:
        # Search starting from page 12
        found_pg = None
        for pdf_pg, text in page_texts:
            if pdf_pg < 12:
                continue
            # Search for pattern
            # For chapter, check 'CHAPTER 1' or 'CHAPTER 2'
            search_str = f"{code} {title}".upper()
            if code.startswith("CHAPTER"):
                if code in text and title in text:
                    found_pg = get_body_page(pdf_pg)
                    break
            elif code in ["REFERENCES", "APPENDIX"]:
                if code in text:
                    found_pg = get_body_page(pdf_pg)
                    break
            else:
                # normal section
                if code in text and title.upper() in text.upper():
                    found_pg = get_body_page(pdf_pg)
                    break
                elif f"{code} " in text:
                    # check title snippet
                    snippet = title.split()[0].upper()
                    if snippet in text.upper():
                        found_pg = get_body_page(pdf_pg)
                        break
        detected_toc[code] = found_pg
        print(f"'{code}' ({title[:35]}) -> Body Page {found_pg}", flush=True)

    # Tables
    tables = [
        ("Table 3.1", "Hardware Component Specifications"),
        ("Table 3.2", "Microcontroller Comparative Evaluation"),
        ("Table 3.3", "ESP32 Master Node Pin Mapping"),
        ("Table 3.4", "Telemetry Payload Data Structure"),
        ("Table 4.1", "CHDI Metric Weight Distribution"),
        ("Table 4.2", "CHDI Clinical Health Risk Tiers"),
        ("Table 4.3", "Component Power Consumption"),
        ("Table 4.4", "Enclosure Physical and Environmental"),
        ("Table 4.5", "REST API Endpoint Specifications"),
        ("Table 5.1", "Multi-Sensor Anomaly Detection"),
        ("Table 5.2", "72-Hour Continuous Sensor Validation"),
        ("Table 5.3", "Empirical Operating Power Modes"),
        ("Table 5.4", "Comprehensive Technical Feature"),
        ("Table 5.5", "Economic Cost Breakdown")
    ]

    print("\n=== DETECTED LOT ITEM BODY PAGES ===")
    detected_lot = {}
    for t_id, t_title in tables:
        found_pg = None
        for pdf_pg, text in page_texts:
            if pdf_pg < 12:
                continue
            if t_id in text:
                found_pg = get_body_page(pdf_pg)
                break
        detected_lot[t_id] = found_pg
        print(f"'{t_id}' -> Body Page {found_pg}", flush=True)

    # Figures
    figures = [
        ("Figure 3.1", "Complete End-to-End Multi-Tier"),
        ("Figure 3.2", "Biometric Collar Hardware Functional"),
        ("Figure 3.3", "Hardware Electrical Wiring Diagram"),
        ("Figure 4.1", "End-to-End Multi-Tier Compute"),
        ("Figure 4.2", "Biometric Collar 3D Enclosure"),
        ("Figure 4.3", "Real-Time Cattle Health Monitoring"),
        ("Figure 5.1", "Empirical Battery Discharge Curve"),
        ("Figure 5.2", "Multi-Sensor 72-Hour Telemetry")
    ]

    print("\n=== DETECTED LOF ITEM BODY PAGES ===")
    detected_lof = {}
    for f_id, f_title in figures:
        found_pg = None
        for pdf_pg, text in page_texts:
            if pdf_pg < 12:
                continue
            if f_id in text:
                found_pg = get_body_page(pdf_pg)
                break
        detected_lof[f_id] = found_pg
        print(f"'{f_id}' -> Body Page {found_pg}", flush=True)

if __name__ == "__main__":
    analyze_pdf()
