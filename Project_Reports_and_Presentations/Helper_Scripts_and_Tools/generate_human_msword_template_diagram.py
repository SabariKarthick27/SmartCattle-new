import os
import subprocess
import shutil

def generate_msword_human_template():
    workspace_fig_dir = os.path.abspath("patent_figures")
    artifact_dir = r"C:\Users\SABARIKARTHICK\.gemini\antigravity-ide\brain\5ea3760d-61ec-4b9d-a301-3985c4c1874a"
    os.makedirs(workspace_fig_dir, exist_ok=True)
    os.makedirs(artifact_dir, exist_ok=True)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    width: 1400px;
    background-color: #ffffff;
    font-family: Arial, Calibri, 'Segoe UI', sans-serif;
    color: #000000;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 30px;
    -webkit-font-smoothing: antialiased;
  }

  /* -------------------------------------------------------------
     TOP INPUT BOX
  ------------------------------------------------------------- */
  .top-input-box {
    width: 580px;
    border: 1.8px solid #000000;
    background: #ffffff;
    padding: 10px 16px;
    text-align: center;
    margin-bottom: 2px;
  }
  .top-input-title {
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .top-input-sub {
    font-size: 13px;
    color: #222222;
    margin-bottom: 3px;
  }
  .top-input-dots {
    font-size: 12.5px;
    color: #444444;
  }

  /* Vertical Connector Arrow */
  .v-arrow-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 24px;
    width: 100%;
  }

  /* -------------------------------------------------------------
     MAJOR LAYER CONTAINER BOXES (1, 2, 3, 4)
  ------------------------------------------------------------- */
  .layer-container {
    width: 1340px;
    border: 1.8px solid #000000;
    background: #ffffff;
    padding: 12px 18px 10px 18px;
    margin-bottom: 2px;
    display: flex;
    flex-direction: column;
  }

  .layer-header {
    font-size: 14.5px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 12px;
    text-align: left;
  }

  /* Row of sub-boxes inside a layer */
  .boxes-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin-bottom: 10px;
  }

  /* Inner Sub-Boxes */
  .sub-box {
    border: 1.4px solid #000000;
    background: #ffffff;
    padding: 10px 10px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 74px;
    flex: 1;
  }

  .sub-box-title {
    font-size: 13.5px;
    font-weight: bold;
    color: #000000;
    line-height: 1.25;
    margin-bottom: 4px;
  }

  .sub-box-desc {
    font-size: 11.5px;
    color: #222222;
    line-height: 1.25;
  }

  /* Horizontal Arrow between sub-boxes */
  .h-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    flex-shrink: 0;
  }

  /* Layer Bottom Technology / Note Line */
  .layer-footer-note {
    font-size: 12px;
    color: #333333;
    text-align: center;
    border-top: 1px dotted #bbbbbb;
    padding-top: 6px;
    margin-top: 2px;
  }

  /* -------------------------------------------------------------
     BOTTOM OUTPUT BOX & FOOTER
  ------------------------------------------------------------- */
  .bottom-output-box {
    width: 620px;
    border: 1.8px solid #000000;
    background: #ffffff;
    padding: 10px 16px;
    text-align: center;
    margin-top: 2px;
    margin-bottom: 10px;
  }
  .bottom-output-title {
    font-size: 14.5px;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .bottom-output-sub {
    font-size: 12.5px;
    color: #222222;
  }

  .master-footer-note {
    font-size: 12.5px;
    color: #333333;
    text-align: center;
    margin-top: 4px;
    font-weight: 500;
  }
</style>
</head>
<body>

  <!-- ============================================================
       TOP INPUT BOX
  ============================================================ -->
  <div class="top-input-box">
    <div class="top-input-title">MULTILINGUAL LIVESTOCK TELEMETRY &amp; IDENTIFIER INPUT</div>
    <div class="top-input-sub">Dynamic QR Animal Passports &nbsp;|&nbsp; Daily Dairy Farmer Observations</div>
    <div class="top-input-dots">Optical Ear Tag Scan &nbsp;&bull;&nbsp; Milk &amp; Feed Logs &nbsp;&bull;&nbsp; Smartphone Camera Capture</div>
  </div>

  <!-- Downward Arrow 1 -->
  <div class="v-arrow-container">
    <svg width="20" height="24" viewBox="0 0 20 24">
      <defs>
        <marker id="arr1" viewBox="0 0 10 10" refX="5" refY="6" markerWidth="6" markerHeight="6" orient="auto">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#000000" />
        </marker>
      </defs>
      <line x1="10" y1="0" x2="10" y2="18" stroke="#000000" stroke-width="1.6" marker-end="url(#arr1)" />
    </svg>
  </div>

  <!-- ============================================================
       LAYER 1: INPUT HANDLING AND IMAGE PREPROCESSING
  ============================================================ -->
  <div class="layer-container">
    <div class="layer-header">1. INPUT HANDLING AND EDGE DATA INGESTION</div>
    <div class="boxes-row">
      <!-- Box 1.1 -->
      <div class="sub-box">
        <div class="sub-box-title">Image Upload / Optical Scan</div>
        <div class="sub-box-desc">Commodity smartphone camera scans QR collar tag</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 1.2 -->
      <div class="sub-box">
        <div class="sub-box-title">Token Decoding &amp; Parsing</div>
        <div class="sub-box-desc">Decodes 128-bit UUID &amp; matches cattle registry profile</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 1.3 -->
      <div class="sub-box">
        <div class="sub-box-title">Multi-Signal Form Logging</div>
        <div class="sub-box-desc">Captures milk yield (L), feed intake (kg) &amp; rumination score</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 1.4 -->
      <div class="sub-box">
        <div class="sub-box-title">Edge Validation &amp; Boundary Check</div>
        <div class="sub-box-desc">Filters spurious anomalies &amp; sensor noise at entry</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 1.5 -->
      <div class="sub-box">
        <div class="sub-box-title">Offline Cache &amp; REST Dispatch</div>
        <div class="sub-box-desc">IndexedDB local storage with async HTTPS API push</div>
      </div>
    </div>
    <div class="layer-footer-note">
      Technologies: Next.js PWA &bull; HTML5 Camera API &bull; IndexedDB Local Storage &bull; JSON Telemetry API
    </div>
  </div>

  <!-- Downward Arrow 2 -->
  <div class="v-arrow-container">
    <svg width="20" height="24" viewBox="0 0 20 24">
      <line x1="10" y1="0" x2="10" y2="18" stroke="#000000" stroke-width="1.6" marker-end="url(#arr1)" />
    </svg>
  </div>

  <!-- ============================================================
       LAYER 2: CENTRAL CLOUD COMPUTING & CHDI ANALYTICS ENGINE
  ============================================================ -->
  <div class="layer-container">
    <div class="layer-header">2. CENTRAL CLOUD COMPUTING AND CHDI ANALYTICS ENGINE</div>
    <div class="boxes-row">
      <!-- Box 2.1 -->
      <div class="sub-box">
        <div class="sub-box-title">M1 &mdash; Multi-Rate Signal Normalizer</div>
        <div class="sub-box-desc">Temporal alignment &amp; cubic spline missing-value imputation</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 2.2 -->
      <div class="sub-box">
        <div class="sub-box-title">M2 &mdash; Personalized Baseline Generator</div>
        <div class="sub-box-desc">Computes 14-day rolling mean vector &mu; and covariance matrix &Sigma;</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 2.3 -->
      <div class="sub-box">
        <div class="sub-box-title">M3 &mdash; Regularized CHDI Calculator</div>
        <div class="sub-box-desc">Tikhonov ridge Mahalanobis distance D_M mapped to 0&ndash;100 score</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 2.4 -->
      <div class="sub-box">
        <div class="sub-box-title">M4 &mdash; Uncertainty Abstention Gate</div>
        <div class="sub-box-desc">Suppresses false alarms for N &lt; 7 &amp; computes 7-day OLS slope</div>
      </div>
    </div>
    <div class="layer-footer-note">
      Mathematical Core: Multivariate Mahalanobis Distance &bull; Tikhonov Shrinkage Regularization &bull; OLS Trend Regression
    </div>
  </div>

  <!-- Downward Arrow 3 -->
  <div class="v-arrow-container">
    <svg width="20" height="24" viewBox="0 0 20 24">
      <line x1="10" y1="0" x2="10" y2="18" stroke="#000000" stroke-width="1.6" marker-end="url(#arr1)" />
    </svg>
  </div>

  <!-- ============================================================
       LAYER 3: DUAL-TIER EXPLAINABILITY & CLINICAL VET TRIAGE
  ============================================================ -->
  <div class="layer-container">
    <div class="layer-header">3. DUAL-TIER EXPLAINABILITY AND CLINICAL VET TRIAGE</div>
    <div class="boxes-row">
      <!-- Box 3.1 -->
      <div class="sub-box">
        <div class="sub-box-title">M5 &mdash; LOCO Feature Attribution</div>
        <div class="sub-box-desc">Quantifies individual metric delta: milk yield, feed &amp; rumination</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 3.2 -->
      <div class="sub-box">
        <div class="sub-box-title">Automated Priority Escalation</div>
        <div class="sub-box-desc">Automatically routes At-Risk tickets (CHDI &lt; 60) to assigned vet</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 3.3 -->
      <div class="sub-box">
        <div class="sub-box-title">Clinical Diagnosis &amp; Rx Tracking</div>
        <div class="sub-box-desc">Vet enters diagnostic label &amp; tracks antibiotic withdrawal dates</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 3.4 -->
      <div class="sub-box">
        <div class="sub-box-title">Closed-Loop Active Retraining</div>
        <div class="sub-box-desc">Curated Confirm / Override labels retrain supervised classifier</div>
      </div>
    </div>
    <div class="layer-footer-note">
      Explainability &amp; Clinical Loop: Leave-One-Covariate-Out (LOCO) &bull; Priority Triage Portal &bull; Supervised Active Learning
    </div>
  </div>

  <!-- Downward Arrow 4 -->
  <div class="v-arrow-container">
    <svg width="20" height="24" viewBox="0 0 20 24">
      <line x1="10" y1="0" x2="10" y2="18" stroke="#000000" stroke-width="1.6" marker-end="url(#arr1)" />
    </svg>
  </div>

  <!-- ============================================================
       LAYER 4: USER TERMINAL INTERFACES & SECURE PERSISTENCE
  ============================================================ -->
  <div class="layer-container">
    <div class="layer-header">4. USER TERMINAL INTERFACES AND SECURE PERSISTENCE</div>
    <div class="boxes-row">
      <!-- Box 4.1 -->
      <div class="sub-box">
        <div class="sub-box-title">Farmer Mobile Dashboard</div>
        <div class="sub-box-desc">Real-time herd roster, health status badges &amp; action cards</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 4.2 -->
      <div class="sub-box">
        <div class="sub-box-title">Veterinarian Triage Portal</div>
        <div class="sub-box-desc">Prioritized triage queue, longitudinal trends &amp; clinical history</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 4.3 -->
      <div class="sub-box">
        <div class="sub-box-title">Spatial Outbreak Aggregator</div>
        <div class="sub-box-desc">Regional GeoHash clustering for 24&ndash;48h epidemic alerts</div>
      </div>
      <!-- Arrow -->
      <div class="h-arrow">
        <svg width="22" height="14" viewBox="0 0 22 14">
          <line x1="0" y1="7" x2="16" y2="7" stroke="#000000" stroke-width="1.5" marker-end="url(#arr1)" />
        </svg>
      </div>
      <!-- Box 4.4 -->
      <div class="sub-box">
        <div class="sub-box-title">Secure Database &amp; Storage Tier</div>
        <div class="sub-box-desc">PostgreSQL time-series records, baseline matrices &amp; audit logs</div>
      </div>
    </div>
    <div class="layer-footer-note">
      Interface Stack: Responsive Web Dashboard &bull; PostgreSQL Database &bull; Prisma ORM &bull; Multi-Channel Push / SMS Gateway
    </div>
  </div>

  <!-- Downward Arrow 5 -->
  <div class="v-arrow-container">
    <svg width="20" height="24" viewBox="0 0 20 24">
      <line x1="10" y1="0" x2="10" y2="18" stroke="#000000" stroke-width="1.6" marker-end="url(#arr1)" />
    </svg>
  </div>

  <!-- ============================================================
       BOTTOM OUTPUT BOX
  ============================================================ -->
  <div class="bottom-output-box">
    <div class="bottom-output-title">APPLICATION OUTPUT &amp; CLINICAL DECISION SUPPORT</div>
    <div class="bottom-output-sub">Continuous CHDI Score (0&ndash;100) &bull; 2.4-Day Early Anomaly Warning &bull; Safe Antibiotic Withdrawal Tracking</div>
  </div>

  <!-- Master Tech Stack Note at Very Bottom -->
  <div class="master-footer-note">
    Core technologies: Python &bull; OpenCV / Camera API &bull; FastAPI &bull; Next.js PWA &bull; PostgreSQL &bull; Prisma ORM &bull; Mahalanobis CHDI &bull; Optical QR
  </div>

</body>
</html>
"""

    temp_html = os.path.abspath("temp_msword_human_template.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    out_png = os.path.abspath("patent_figures/smartcattle_academic_architecture_diagram.png")
    subprocess.run([
        edge_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1400,980",
        f"--screenshot={out_png}",
        f"file:///{temp_html}"
    ], check=True)

    # Copy to artifact folder for direct markdown display
    art_png = os.path.join(artifact_dir, "smartcattle_academic_architecture_diagram.png")
    shutil.copy2(out_png, art_png)

    # Clean up temp html
    if os.path.exists(temp_html):
        os.remove(temp_html)

    print("Success: Generated authentic MS Word style academic architecture diagram matching the left template!")

if __name__ == "__main__":
    generate_msword_human_template()
