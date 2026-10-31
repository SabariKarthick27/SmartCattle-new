import os
import subprocess
import shutil

def build_all_word_images():
    workspace_fig_dir = os.path.abspath("patent_figures")
    artifact_dir = r"C:\Users\SABARIKARTHICK\.gemini\antigravity-ide\brain\5ea3760d-61ec-4b9d-a301-3985c4c1874a"
    os.makedirs(workspace_fig_dir, exist_ok=True)
    os.makedirs(artifact_dir, exist_ok=True)
    
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    # =========================================================================
    # VERSION 1: Pristine Human-Made MS Word Shapes Diagram (High-Res 300 DPI)
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
    width: 1720px;
    height: 1080px;
    background-color: #ffffff;
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 35px 50px;
    color: #1a1a1a;
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
  }

  .title-heading {
    font-size: 24px;
    font-weight: 700;
    color: #1E3A8A; /* Word Header Deep Blue */
    letter-spacing: 0.6px;
    margin-bottom: 30px;
    text-align: center;
    text-transform: uppercase;
  }

  .canvas-grid {
    width: 1620px;
    height: 940px;
    position: relative;
  }

  /* Microsoft Word Shape standard styling */
  .word-card {
    position: absolute;
    border-radius: 12px;
    border-width: 2.2px;
    border-style: solid;
    padding: 20px 24px;
    background: #ffffff;
    box-shadow: 2px 3px 8px rgba(0, 0, 0, 0.07);
    display: flex;
    flex-direction: column;
  }

  .card-header {
    font-size: 19px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 18px;
    letter-spacing: 0.3px;
  }

  .card-bullets {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-size: 17px;
    color: #1f2937;
    line-height: 1.35;
  }

  .card-bullets li {
    position: relative;
    padding-left: 24px;
    text-align: left;
  }

  .card-bullets li::before {
    content: "•";
    position: absolute;
    left: 2px;
    top: -1px;
    font-size: 20px;
    color: #374151;
  }

  /* Box 100: PHYSICAL & ACQUISITION TIER */
  #card-100 {
    left: 10px;
    top: 10px;
    width: 470px;
    height: 290px;
    background-color: #F0F6FC;
    border-color: #2E75B6;
  }
  #card-100 .card-header { color: #1B4E82; }

  /* Box 200: EDGE / CLIENT APP TIER */
  #card-200 {
    left: 540px;
    top: 10px;
    width: 520px;
    height: 290px;
    background-color: #F1F8F4;
    border-color: #2E7D32;
  }
  #card-200 .card-header { color: #1E5C25; }

  /* Box 300: USER TERMINAL INTERFACES */
  #card-300 {
    left: 1120px;
    top: 10px;
    width: 490px;
    height: 290px;
    background-color: #F8F3FC;
    border-color: #7030A0;
  }
  #card-300 .card-header { color: #551D7F; }

  /* Box 400: CENTRAL CLOUD COMPUTING & ANALYTICS ENGINE */
  #card-400 {
    left: 10px;
    top: 350px;
    width: 1050px;
    height: 480px;
    background-color: #FDF2F2;
    border-color: #C00000;
  }
  #card-400 .card-header { color: #920000; margin-bottom: 20px; }
  #card-400 .card-bullets { gap: 14px; }

  /* Box 500: SECURE STORAGE TIER */
  #card-500 {
    left: 1120px;
    top: 350px;
    width: 490px;
    height: 480px;
    background-color: #FEFCE8;
    border-color: #D4AC0D;
  }
  #card-500 .card-header { color: #8C7100; margin-bottom: 24px; }
  #card-500 .card-bullets { gap: 18px; }

  /* Overlay SVG for MS Word Arrows */
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

  <div class="title-heading">FIGURE 1: SYSTEM HARDWARE AND LOGICAL ARCHITECTURE</div>

  <div class="canvas-grid">
    <!-- Box 100 -->
    <div class="word-card" id="card-100">
      <div class="card-header">PHYSICAL &amp; ACQUISITION TIER (100)</div>
      <ul class="card-bullets">
        <li>Cattle Tag with Optical QR (102)</li>
        <li>Mobile Optical Camera Sensor (104)</li>
        <li>Manual Entry Interface (106)</li>
        <li>Optional IoT Sensor Array (108)</li>
      </ul>
    </div>

    <!-- Box 200 -->
    <div class="word-card" id="card-200">
      <div class="card-header">EDGE / CLIENT APP TIER (200)</div>
      <ul class="card-bullets">
        <li>Optical Token Decoder (202)</li>
        <li>Multi-Signal Form Validator (204)</li>
        <li>Offline Data Buffer / Cache (206)</li>
        <li>Secure API Dispatcher (208)</li>
      </ul>
    </div>

    <!-- Box 300 -->
    <div class="word-card" id="card-300">
      <div class="card-header">USER TERMINAL INTERFACES (300)</div>
      <ul class="card-bullets">
        <li>Farmer Mobile Dashboard (302)</li>
        <li>Veterinarian Triage Portal (304)</li>
        <li>Admin &amp; Outbreak Monitor (306)</li>
        <li>Push/SMS Alert Dispatch (308)</li>
      </ul>
    </div>

    <!-- Box 400 -->
    <div class="word-card" id="card-400">
      <div class="card-header">CENTRAL CLOUD COMPUTING &amp; ANALYTICS ENGINE (400)</div>
      <ul class="card-bullets">
        <li>Asynchronous Multi-Rate Signal Normalizer &amp; Temporal Imputer (402)</li>
        <li>Personalized Historical Rolling Baseline Generator (404)</li>
        <li>Covariance-Aware Regularized CHDI Calculator (406)</li>
        <li>Confidence-Aware Matrix Condition Abstention Gate (408)</li>
        <li>Two-Tier Feature Explainability Module (410)</li>
        <li>Closed-Loop Supervised Classifier Retraining Pipeline (412)</li>
        <li>Spatial-Temporal Regional Outbreak Aggregator (414)</li>
      </ul>
    </div>

    <!-- Box 500 -->
    <div class="word-card" id="card-500">
      <div class="card-header">SECURE STORAGE TIER (500)</div>
      <ul class="card-bullets">
        <li>Cattle Identity &amp; Life Registry (502)</li>
        <li>Time-Series Physiological DB (504)</li>
        <li>Covariance &amp; Baseline Matrices (506)</li>
        <li>Clinical Cases &amp; Vet Overrides (508)</li>
        <li>Spatial Outbreak Registry (510)</li>
      </ul>
    </div>

    <!-- Connectors -->
    <svg class="svg-arrows" viewBox="0 0 1620 940">
      <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#2E75B6" />
        </marker>
      </defs>

      <!-- Arrow 1: Box 100 right (480, 155) -> Box 200 left (540, 155) -->
      <line x1="480" y1="155" x2="534" y2="155" stroke="#2E75B6" stroke-width="2.6" marker-end="url(#arrowhead)" />

      <!-- Arrow 2: Box 200 right (1060, 155) -> Box 300 left (1120, 155) -->
      <line x1="1060" y1="155" x2="1114" y2="155" stroke="#2E75B6" stroke-width="2.6" marker-end="url(#arrowhead)" />

      <!-- Arrow 3: Box 400 top (580, 350) -> Box 200 bottom (580, 300) -->
      <line x1="580" y1="350" x2="580" y2="306" stroke="#2E75B6" stroke-width="2.6" marker-end="url(#arrowhead)" />

      <!-- Arrow 4: Box 400 right (1060, 590) -> Box 500 left (1120, 590) -->
      <line x1="1060" y1="590" x2="1114" y2="590" stroke="#2E75B6" stroke-width="2.6" marker-end="url(#arrowhead)" />
    </svg>
  </div>

</body>
</html>
"""

    # =========================================================================
    # VERSION 2: Diagram with Authentic MS Word Selection Handles & Editor Feel
    # =========================================================================
    html_word_editor = """<!DOCTYPE html>
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
    width: 1720px;
    height: 1080px;
    background-color: #F3F4F6; /* Word Desk workspace gray */
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    -webkit-font-smoothing: antialiased;
  }

  /* Microsoft Word White Page Sheet */
  .word-page {
    width: 1640px;
    height: 1020px;
    background: #ffffff;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    padding: 30px 40px;
    position: relative;
    border: 1px solid #E5E7EB;
  }

  /* The Selected Shape Group Bounding Box in Word */
  .word-selection-box {
    width: 1560px;
    height: 950px;
    margin: 0 auto;
    position: relative;
    border: 1.5px solid #5A5A5A;
  }

  /* Circular Selection Handles (8 handles around perimeter) */
  .handle {
    position: absolute;
    width: 14px;
    height: 14px;
    background: #ffffff;
    border: 1.8px solid #4A4A4A;
    border-radius: 50%;
    z-index: 50;
  }
  .handle.tl { top: -7px; left: -7px; }
  .handle.tc { top: -7px; left: calc(50% - 7px); }
  .handle.tr { top: -7px; right: -7px; }
  .handle.ml { top: calc(50% - 7px); left: -7px; }
  .handle.mr { top: calc(50% - 7px); right: -7px; }
  .handle.bl { bottom: -7px; left: -7px; }
  .handle.bc { bottom: -7px; left: calc(50% - 7px); }
  .handle.br { bottom: -7px; right: -7px; }

  /* Top Rotation Stalk Handle */
  .rot-stalk {
    position: absolute;
    top: -28px;
    left: calc(50% - 1px);
    width: 2px;
    height: 21px;
    background: #4A4A4A;
    z-index: 49;
  }
  .rot-handle {
    position: absolute;
    top: -36px;
    left: calc(50% - 7px);
    width: 14px;
    height: 14px;
    background: #ffffff;
    border: 1.8px solid #4A4A4A;
    border-radius: 50%;
    z-index: 50;
  }

  /* Microsoft Word Layout Options Button (horseshoe popup button) */
  .layout-options-btn {
    position: absolute;
    top: -6px;
    right: -42px;
    width: 32px;
    height: 32px;
    background: #ffffff;
    border: 1.2px solid #A0A0A0;
    box-shadow: 1px 2px 4px rgba(0,0,0,0.12);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 3px;
    cursor: default;
    z-index: 50;
  }
  .layout-icon-arch {
    width: 18px;
    height: 10px;
    border: 1.8px solid #005A9E;
    border-bottom: none;
    border-top-left-radius: 9px;
    border-top-right-radius: 9px;
  }
  .layout-icon-line {
    width: 20px;
    height: 1.8px;
    background: #005A9E;
  }

  /* Inner Diagram Content */
  .diagram-inner {
    width: 100%;
    height: 100%;
    position: relative;
    padding: 20px 20px;
  }

  .title-heading {
    font-size: 23px;
    font-weight: 700;
    color: #1E3A8A;
    letter-spacing: 0.6px;
    margin-bottom: 25px;
    text-align: center;
    text-transform: uppercase;
  }

  .canvas-grid {
    width: 1520px;
    height: 850px;
    position: relative;
  }

  .word-card {
    position: absolute;
    border-radius: 12px;
    border-width: 2.2px;
    border-style: solid;
    padding: 18px 22px;
    background: #ffffff;
    box-shadow: 1px 2px 6px rgba(0, 0, 0, 0.06);
    display: flex;
    flex-direction: column;
  }

  .card-header {
    font-size: 18px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 16px;
    letter-spacing: 0.3px;
  }

  .card-bullets {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 11px;
    font-size: 16px;
    color: #1f2937;
    line-height: 1.35;
  }

  .card-bullets li {
    position: relative;
    padding-left: 22px;
    text-align: left;
  }

  .card-bullets li::before {
    content: "•";
    position: absolute;
    left: 2px;
    top: -1px;
    font-size: 18px;
    color: #374151;
  }

  #card-100 {
    left: 10px;
    top: 10px;
    width: 440px;
    height: 270px;
    background-color: #F0F6FC;
    border-color: #2E75B6;
  }
  #card-100 .card-header { color: #1B4E82; }

  #card-200 {
    left: 500px;
    top: 10px;
    width: 490px;
    height: 270px;
    background-color: #F1F8F4;
    border-color: #2E7D32;
  }
  #card-200 .card-header { color: #1E5C25; }

  #card-300 {
    left: 1040px;
    top: 10px;
    width: 470px;
    height: 270px;
    background-color: #F8F3FC;
    border-color: #7030A0;
  }
  #card-300 .card-header { color: #551D7F; }

  #card-400 {
    left: 10px;
    top: 320px;
    width: 980px;
    height: 470px;
    background-color: #FDF2F2;
    border-color: #C00000;
  }
  #card-400 .card-header { color: #920000; margin-bottom: 18px; }
  #card-400 .card-bullets { gap: 13px; }

  #card-500 {
    left: 1040px;
    top: 320px;
    width: 470px;
    height: 470px;
    background-color: #FEFCE8;
    border-color: #D4AC0D;
  }
  #card-500 .card-header { color: #8C7100; margin-bottom: 22px; }
  #card-500 .card-bullets { gap: 17px; }

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

  <div class="word-page">
    <div class="word-selection-box">
      <!-- 8 Selection Handles -->
      <div class="handle tl"></div>
      <div class="handle tc"></div>
      <div class="handle tr"></div>
      <div class="handle ml"></div>
      <div class="handle mr"></div>
      <div class="handle bl"></div>
      <div class="handle bc"></div>
      <div class="handle br"></div>
      
      <!-- Rotation Stalk & Handle -->
      <div class="rot-stalk"></div>
      <div class="rot-handle"></div>

      <!-- Layout Options Popout Button -->
      <div class="layout-options-btn">
        <div class="layout-icon-arch"></div>
        <div class="layout-icon-line"></div>
        <div class="layout-icon-line" style="width: 14px;"></div>
      </div>

      <div class="diagram-inner">
        <div class="title-heading">FIGURE 1: SYSTEM HARDWARE AND LOGICAL ARCHITECTURE</div>

        <div class="canvas-grid">
          <!-- Box 100 -->
          <div class="word-card" id="card-100">
            <div class="card-header">PHYSICAL &amp; ACQUISITION TIER (100)</div>
            <ul class="card-bullets">
              <li>Cattle Tag with Optical QR (102)</li>
              <li>Mobile Optical Camera Sensor (104)</li>
              <li>Manual Entry Interface (106)</li>
              <li>Optional IoT Sensor Array (108)</li>
            </ul>
          </div>

          <!-- Box 200 -->
          <div class="word-card" id="card-200">
            <div class="card-header">EDGE / CLIENT APP TIER (200)</div>
            <ul class="card-bullets">
              <li>Optical Token Decoder (202)</li>
              <li>Multi-Signal Form Validator (204)</li>
              <li>Offline Data Buffer / Cache (206)</li>
              <li>Secure API Dispatcher (208)</li>
            </ul>
          </div>

          <!-- Box 300 -->
          <div class="word-card" id="card-300">
            <div class="card-header">USER TERMINAL INTERFACES (300)</div>
            <ul class="card-bullets">
              <li>Farmer Mobile Dashboard (302)</li>
              <li>Veterinarian Triage Portal (304)</li>
              <li>Admin &amp; Outbreak Monitor (306)</li>
              <li>Push/SMS Alert Dispatch (308)</li>
            </ul>
          </div>

          <!-- Box 400 -->
          <div class="word-card" id="card-400">
            <div class="card-header">CENTRAL CLOUD COMPUTING &amp; ANALYTICS ENGINE (400)</div>
            <ul class="card-bullets">
              <li>Asynchronous Multi-Rate Signal Normalizer &amp; Temporal Imputer (402)</li>
              <li>Personalized Historical Rolling Baseline Generator (404)</li>
              <li>Covariance-Aware Regularized CHDI Calculator (406)</li>
              <li>Confidence-Aware Matrix Condition Abstention Gate (408)</li>
              <li>Two-Tier Feature Explainability Module (410)</li>
              <li>Closed-Loop Supervised Classifier Retraining Pipeline (412)</li>
              <li>Spatial-Temporal Regional Outbreak Aggregator (414)</li>
            </ul>
          </div>

          <!-- Box 500 -->
          <div class="word-card" id="card-500">
            <div class="card-header">SECURE STORAGE TIER (500)</div>
            <ul class="card-bullets">
              <li>Cattle Identity &amp; Life Registry (502)</li>
              <li>Time-Series Physiological DB (504)</li>
              <li>Covariance &amp; Baseline Matrices (506)</li>
              <li>Clinical Cases &amp; Vet Overrides (508)</li>
              <li>Spatial Outbreak Registry (510)</li>
            </ul>
          </div>

          <!-- Connectors -->
          <svg class="svg-arrows" viewBox="0 0 1520 850">
            <defs>
              <marker id="arrowhead" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
                <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#2E75B6" />
              </marker>
            </defs>

            <!-- Arrow 1: Box 100 right (450, 145) -> Box 200 left (500, 145) -->
            <line x1="450" y1="145" x2="494" y2="145" stroke="#2E75B6" stroke-width="2.6" marker-end="url(#arrowhead)" />

            <!-- Arrow 2: Box 200 right (990, 145) -> Box 300 left (1040, 145) -->
            <line x1="990" y1="145" x2="1034" y2="145" stroke="#2E75B6" stroke-width="2.6" marker-end="url(#arrowhead)" />

            <!-- Arrow 3: Box 400 top (540, 320) -> Box 200 bottom (540, 280) -->
            <line x1="540" y1="320" x2="540" y2="286" stroke="#2E75B6" stroke-width="2.6" marker-end="url(#arrowhead)" />

            <!-- Arrow 4: Box 400 right (990, 555) -> Box 500 left (1040, 555) -->
            <line x1="990" y1="555" x2="1034" y2="555" stroke="#2E75B6" stroke-width="2.6" marker-end="url(#arrowhead)" />
          </svg>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

    # Generate Version 1
    html1 = os.path.abspath("temp_clean_diag.html")
    with open(html1, "w", encoding="utf-8") as f:
        f.write(html_clean)
    out1 = os.path.abspath("patent_figures/figure1_system_architecture_clean.png")
    subprocess.run([edge_path, "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=1720,1080", f"--screenshot={out1}", f"file:///{html1}"], check=True)
    
    # Generate Version 2
    html2 = os.path.abspath("temp_editor_diag.html")
    with open(html2, "w", encoding="utf-8") as f:
        f.write(html_word_editor)
    out2 = os.path.abspath("patent_figures/figure1_system_architecture_word_editor.png")
    subprocess.run([edge_path, "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=1720,1080", f"--screenshot={out2}", f"file:///{html2}"], check=True)

    # Copy to artifact dir for markdown display
    art_out1 = os.path.join(artifact_dir, "figure1_system_architecture_clean.png")
    art_out2 = os.path.join(artifact_dir, "figure1_system_architecture_word_editor.png")
    shutil.copy2(out1, art_out1)
    shutil.copy2(out2, art_out2)

    # Clean up temp html
    if os.path.exists(html1): os.remove(html1)
    if os.path.exists(html2): os.remove(html2)

    print("Success: Both versions rendered and placed in artifact and patent_figures!")

if __name__ == "__main__":
    build_all_word_images()
