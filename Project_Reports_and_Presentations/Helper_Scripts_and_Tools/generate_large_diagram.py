import os
import subprocess
import shutil

def generate_perfect_compact_large_diagram():
    workspace_fig_dir = os.path.abspath("patent_figures")
    artifact_dir = r"C:\Users\SABARIKARTHICK\.gemini\antigravity-ide\brain\5ea3760d-61ec-4b9d-a301-3985c4c1874a"
    os.makedirs(workspace_fig_dir, exist_ok=True)
    os.makedirs(artifact_dir, exist_ok=True)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    # =========================================================================
    # Clean Big & Bold Diagram (No Numbers, Zero Empty Space, Ultra Readable)
    # =========================================================================
    html_clean = """<!DOCTYPE html>
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
    width: 1260px;
    height: 760px;
    background-color: #ffffff;
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 22px 28px;
    color: #0f172a;
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
  }

  .main-title {
    font-size: 24px;
    font-weight: 800;
    color: #1E3A8A;
    letter-spacing: 0.6px;
    margin-bottom: 20px;
    text-align: center;
    text-transform: uppercase;
  }

  .diagram-area {
    width: 1200px;
    height: 670px;
    position: relative;
  }

  /* Microsoft Word Style Shape Cards */
  .word-box {
    position: absolute;
    border-radius: 10px;
    border-width: 2.5px;
    border-style: solid;
    padding: 14px 18px;
    background: #ffffff;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
  }

  .box-title {
    font-size: 18.5px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 12px;
    letter-spacing: 0.2px;
    padding-bottom: 5px;
  }

  .box-bullets {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 9px;
    font-size: 16.5px;
    font-weight: 600;
    color: #1e293b;
    line-height: 1.25;
  }

  .box-bullets li {
    position: relative;
    padding-left: 20px;
    text-align: left;
  }

  .box-bullets li::before {
    content: "•";
    position: absolute;
    left: 2px;
    top: -1px;
    font-size: 19px;
    color: #0f172a;
  }

  /* TOP ROW: 3 Blocks */
  #box-phys {
    left: 5px;
    top: 5px;
    width: 355px;
    height: 220px;
    background-color: #F0F6FC;
    border-color: #2563EB;
  }
  #box-phys .box-title { color: #1E40AF; border-bottom: 1.5px solid #BFDBFE; }

  #box-edge {
    left: 405px;
    top: 5px;
    width: 380px;
    height: 220px;
    background-color: #F0FDF4;
    border-color: #16A34A;
  }
  #box-edge .box-title { color: #15803D; border-bottom: 1.5px solid #BBF7D0; }

  #box-user {
    left: 835px;
    top: 5px;
    width: 360px;
    height: 220px;
    background-color: #FAF5FF;
    border-color: #9333EA;
  }
  #box-user .box-title { color: #7E22CE; border-bottom: 1.5px solid #E9D5FF; }

  /* BOTTOM ROW: 2 Blocks */
  #box-cloud {
    left: 5px;
    top: 265px;
    width: 780px;
    height: 385px;
    background-color: #FEF2F2;
    border-color: #DC2626;
  }
  #box-cloud .box-title { color: #B91C1C; border-bottom: 1.5px solid #FECACA; margin-bottom: 14px; }
  #box-cloud .box-bullets { gap: 11px; font-size: 16.5px; }

  #box-store {
    left: 835px;
    top: 265px;
    width: 360px;
    height: 385px;
    background-color: #FEFCE8;
    border-color: #CA8A04;
  }
  #box-store .box-title { color: #A16207; border-bottom: 1.5px solid #FEF08A; margin-bottom: 18px; }
  #box-store .box-bullets { gap: 18px; font-size: 16.5px; }

  /* SVG Connectors */
  .svg-arrows {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 10;
  }
</style>
</head>
<body>

  <div class="main-title">FIGURE 1: SYSTEM HARDWARE AND LOGICAL ARCHITECTURE</div>

  <div class="diagram-area">
    <!-- Box 1 -->
    <div class="word-box" id="box-phys">
      <div class="box-title">PHYSICAL &amp; ACQUISITION TIER</div>
      <ul class="box-bullets">
        <li>Cattle Tag with Optical QR</li>
        <li>Mobile Optical Camera Scanner</li>
        <li>Farmer Manual Entry Interface</li>
        <li>Optional IoT Sensor Array</li>
      </ul>
    </div>

    <!-- Box 2 -->
    <div class="word-box" id="box-edge">
      <div class="box-title">EDGE / CLIENT APP TIER</div>
      <ul class="box-bullets">
        <li>Optical Token Decoder</li>
        <li>Multi-Signal Form Validator</li>
        <li>Offline Data Buffer &amp; Cache</li>
        <li>Secure API Dispatcher</li>
      </ul>
    </div>

    <!-- Box 3 -->
    <div class="word-box" id="box-user">
      <div class="box-title">USER TERMINAL INTERFACES</div>
      <ul class="box-bullets">
        <li>Farmer Mobile Dashboard</li>
        <li>Veterinarian Triage Portal</li>
        <li>Admin &amp; Outbreak Monitor</li>
        <li>Push / SMS Alert Dispatch</li>
      </ul>
    </div>

    <!-- Box 4 -->
    <div class="word-box" id="box-cloud">
      <div class="box-title">CENTRAL CLOUD COMPUTING &amp; ANALYTICS ENGINE</div>
      <ul class="box-bullets">
        <li>Asynchronous Signal Normalizer &amp; Temporal Imputer</li>
        <li>Personalized Historical Rolling Baseline Generator</li>
        <li>Covariance-Aware Regularized CHDI Calculator</li>
        <li>Confidence-Aware Matrix Condition Abstention Gate</li>
        <li>Two-Tier Feature Explainability Module</li>
        <li>Closed-Loop Supervised Classifier Retraining Pipeline</li>
        <li>Spatial-Temporal Regional Outbreak Aggregator</li>
      </ul>
    </div>

    <!-- Box 5 -->
    <div class="word-box" id="box-store">
      <div class="box-title">SECURE STORAGE TIER</div>
      <ul class="box-bullets">
        <li>Cattle Identity &amp; Life Registry</li>
        <li>Time-Series Physiological Database</li>
        <li>Covariance &amp; Baseline Matrices</li>
        <li>Clinical Cases &amp; Vet Overrides</li>
        <li>Spatial Outbreak Registry</li>
      </ul>
    </div>

    <svg class="svg-arrows" viewBox="0 0 1200 670">
      <defs>
        <marker id="word-arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#1E40AF" />
        </marker>
      </defs>

      <!-- Arrow 1: Physical Tier -> Edge App Tier -->
      <line x1="360" y1="115" x2="397" y2="115" stroke="#1E40AF" stroke-width="3" marker-end="url(#word-arr)" />

      <!-- Arrow 2: Edge App Tier -> User Terminal Tier -->
      <line x1="785" y1="115" x2="827" y2="115" stroke="#1E40AF" stroke-width="3" marker-end="url(#word-arr)" />

      <!-- Arrow 3: Central Cloud -> Edge App Tier (vertical) -->
      <line x1="440" y1="265" x2="440" y2="233" stroke="#1E40AF" stroke-width="3" marker-end="url(#word-arr)" />

      <!-- Arrow 4: Central Cloud -> Secure Storage -->
      <line x1="785" y1="460" x2="827" y2="460" stroke="#1E40AF" stroke-width="3" marker-end="url(#word-arr)" />
    </svg>
  </div>

</body>
</html>
"""

    # Generate the compact large clean image
    temp_clean = os.path.abspath("temp_compact.html")
    with open(temp_clean, "w", encoding="utf-8") as f:
        f.write(html_clean)

    out_clean = os.path.abspath("patent_figures/figure1_system_architecture_clean_large.png")
    subprocess.run([edge_path, "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=1260,760", f"--screenshot={out_clean}", f"file:///{temp_clean}"], check=True)

    # Copy to artifact folder
    art_clean = os.path.join(artifact_dir, "figure1_system_architecture_clean_large.png")
    shutil.copy2(out_clean, art_clean)
    
    # Also update patent_figures/figure1_system_architecture.png
    dest_fig = os.path.abspath("patent_figures/figure1_system_architecture.png")
    shutil.copy2(out_clean, dest_fig)

    if os.path.exists(temp_clean):
        os.remove(temp_clean)

    print("Success: Updated with perfect compact large-text diagram without numbers!")

if __name__ == "__main__":
    generate_perfect_compact_large_diagram()
