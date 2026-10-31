import os
import sys
import win32com.client

def get_pages():
    doc_path = os.path.abspath("SmartCattle_Mini_Project_Report_v6.docx")
    if not os.path.exists(doc_path):
        print(f"File not found: {doc_path}")
        return

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(doc_path, ReadOnly=True)
        print("TOTAL PAGES:", doc.ComputeStatistics(2))
        
        # Search targets
        targets = [
            "BONAFIDE CERTIFICATE",
            "DECLARATION",
            "ACKNOWLEDGEMENT",
            "ABSTRACT",
            "TABLE OF CONTENTS",
            "LIST OF TABLES",
            "LIST OF FIGURES",
            "LIST OF ABBREVIATIONS",
            "CHAPTER 1",
            "1.1 BACKGROUND AND DOMAIN CONTEXT",
            "1.2 PROBLEM STATEMENT",
            "1.3 MOTIVATION AND OBJECTIVES",
            "1.4 SCOPE OF THE PROJECT",
            "1.5 REPORT ORGANIZATION",
            "CHAPTER 2",
            "2.1 HISTORICAL EVOLUTION OF CATTLE MONITORING",
            "2.2 WEARABLE IOT SENSOR ARCHITECTURES",
            "2.3 THERMAL IMAGING AND OPTICAL SENSING",
            "2.4 EDGE-AI AND IN-SITU TIME-SERIES INFERENCE",
            "2.5 LONG-RANGE TELEMETRY AND MESH TOPOLOGIES",
            "2.6 COMPUTER VISION AND LIVESTOCK BIOMETRICS",
            "2.7 CLOUD DECISION ENGINES AND HERD ANALYTICS",
            "2.8 SYNTHESIS AND IDENTIFIED RESEARCH GAPS",
            "CHAPTER 3",
            "3.1 OVERALL MULTI-TIER SYSTEM ARCHITECTURE",
            "3.2 HARDWARE TIER: BIOMETRIC COLLAR AND THERMAL POD",
            "3.3 HARDWARE SELECTION RATIONALE",
            "3.4 PIN MAPPING AND SENSOR BUS INTERFACES",
            "3.5 COMMUNICATION PROTOCOLS AND TELEMETRY",
            "3.6 BACKEND AND TIME-SERIES DATA ARCHITECTURE",
            "3.7 CLUSTER AND HIGH-AVAILABILITY DEPLOYMENT",
            "CHAPTER 4",
            "4.1 CHDI MATHEMATICAL ENGINE AND SCORE FORMULATION",
            "4.2 MULTI-TIER COMPUTE WORKFLOW",
            "4.3 HARDWARE POWER BUDGET AND SENSOR TIMINGS",
            "4.4 FIRMWARE ALGORITHMIC IMPLEMENTATION",
            "4.5 WEARABLE FORM FACTOR AND ENCLOSURE DESIGN",
            "4.6 CLOUD INGESTION PIPELINE AND MICROSERVICES",
            "4.7 REAL-TIME EVENT STREAMING AND ALERT ROUTING",
            "4.8 MULTI-TENANT WEB APPLICATION AND DASHBOARD",
            "4.9 CORE PRODUCTION IMPLEMENTATION CODE",
            "CHAPTER 5",
            "5.1 HARDWARE EXPERIMENTAL SETUP",
            "5.2 TIME-SERIES AND ANOMALY DETECTION EVALUATION",
            "5.3 FIELD TRIAL SENSOR TELEMETRY ANALYSIS",
            "5.4 POWER CONSUMPTION AND BATTERY PROFILES",
            "5.5 COMPARATIVE SYSTEM BENCHMARKING",
            "CHAPTER 6",
            "6.1 KEY FINDINGS AND CONTRIBUTIONS",
            "6.2 CURRENT LIMITATIONS",
            "6.3 FUTURE RESEARCH DIRECTIONS",
            "REFERENCES",
            "APPENDIX"
        ]
        
        # Figures
        figures = [
            "Figure 3.1: Complete End-to-End Multi-Tier",
            "Figure 3.2: Biometric Collar Hardware Functional",
            "Figure 3.3: Hardware Electrical Wiring Diagram",
            "Figure 4.1: End-to-End Multi-Tier Compute",
            "Figure 4.2: Biometric Collar 3D Enclosure",
            "Figure 4.3: Real-Time Cattle Health Monitoring",
            "Figure 5.1: Empirical Battery Discharge Curve",
            "Figure 5.2: Multi-Sensor 72-Hour Telemetry"
        ]
        
        # Tables
        tables = [
            "Table 3.1: Hardware Component Specifications",
            "Table 3.2: Microcontroller Comparative Evaluation",
            "Table 3.3: ESP32 Master Node Pin Mapping",
            "Table 3.4: Telemetry Payload Data Structure",
            "Table 4.1: CHDI Metric Weight Distribution",
            "Table 4.2: CHDI Clinical Health Risk Tiers",
            "Table 4.3: Component Power Consumption",
            "Table 4.4: Enclosure Physical and Environmental",
            "Table 4.5: REST API Endpoint Specifications",
            "Table 5.1: Multi-Sensor Anomaly Detection",
            "Table 5.2: 72-Hour Continuous Sensor Validation",
            "Table 5.3: Empirical Operating Power Modes",
            "Table 5.4: Comprehensive Technical Feature",
            "Table 5.5: Economic Cost Breakdown"
        ]
        
        def find_item_page(query):
            find_obj = doc.Content.Find
            find_obj.ClearFormatting()
            find_obj.Text = query
            find_obj.MatchCase = False
            find_obj.MatchWholeWord = False
            find_obj.Forward = True
            find_obj.Wrap = 0 # wdFindStop
            if find_obj.Execute():
                rng = find_obj.Parent
                # Use wdActiveEndAdjustedPageNumber (3) for roman/arabic page numbers
                adj_page = rng.Information(3)
                raw_page = rng.Information(1)
                return adj_page, raw_page
            return None, None

        print("\n--- FRONT MATTER & HEADINGS ---")
        for t in targets:
            adj_p, raw_p = find_item_page(t)
            print(f"[{t}] -> Adj Page: {adj_p} (Raw: {raw_p})")

        print("\n--- FIGURES ---")
        for f in figures:
            adj_p, raw_p = find_item_page(f)
            print(f"[{f}] -> Adj Page: {adj_p} (Raw: {raw_p})")

        print("\n--- TABLES ---")
        for tb in tables:
            adj_p, raw_p = find_item_page(tb)
            print(f"[{tb}] -> Adj Page: {adj_p} (Raw: {raw_p})")

    finally:
        doc.Close(False)
        word.Quit()

if __name__ == "__main__":
    get_pages()
