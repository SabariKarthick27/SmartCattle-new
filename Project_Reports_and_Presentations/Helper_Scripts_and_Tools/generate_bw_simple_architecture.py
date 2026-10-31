import os
import subprocess
import shutil

def generate_perfect_bw_architecture():
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
    width: 1220px;
    height: 600px;
    background-color: #ffffff;
    font-family: Arial, Calibri, 'Segoe UI', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px 22px;
    color: #000000;
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
  }

  .main-title {
    font-size: 21px;
    font-weight: bold;
    color: #000000;
    letter-spacing: 0.5px;
    margin-bottom: 16px;
    text-align: center;
    text-transform: uppercase;
  }

  .canvas-container {
    width: 1160px;
    height: 525px;
    position: relative;
  }

  /* Black & White MS Word Shape Boxes */
  .word-box {
    position: absolute;
    border-radius: 8px;
    border: 2px solid #000000;
    background: #ffffff;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
  }

  .box-title {
    font-size: 15.5px;
    font-weight: bold;
    color: #000000;
    text-align: center;
    margin-bottom: 10px;
    letter-spacing: 0.2px;
    text-transform: uppercase;
    border-bottom: 1px solid #000000;
    padding-bottom: 5px;
  }

  .box-bullets {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 14.5px;
    color: #000000;
    line-height: 1.25;
  }

  .box-bullets li {
    position: relative;
    padding-left: 18px;
    text-align: left;
  }

  .box-bullets li::before {
    content: "•";
    position: absolute;
    left: 2px;
    top: -1px;
    font-size: 17px;
    color: #000000;
  }

  /* TOP ROW: 3 Boxes */
  #box-phys {
    left: 5px;
    top: 5px;
    width: 345px;
    height: 185px;
  }

  #box-edge {
    left: 395px;
    top: 5px;
    width: 365px;
    height: 185px;
  }

  #box-user {
    left: 805px;
    top: 5px;
    width: 345px;
    height: 185px;
  }

  /* BOTTOM ROW: 2 Boxes (Snug & Perfectly Balanced) */
  #box-cloud {
    left: 5px;
    top: 230px;
    width: 755px;
    height: 285px;
  }
  #box-cloud .box-bullets {
    gap: 9px;
  }

  #box-store {
    left: 805px;
    top: 230px;
    width: 345px;
    height: 285px;
  }
  #box-store .box-bullets {
    gap: 15px;
  }

  /* SVG Arrows Layer */
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

  <div class="canvas-container">
    <!-- Box 1: Physical Tier -->
    <div class="word-box" id="box-phys">
      <div class="box-title">PHYSICAL &amp; DATA CAPTURE TIER</div>
      <ul class="box-bullets">
        <li>Cattle Tag with QR Code</li>
        <li>Smartphone Camera Scanner</li>
        <li>Farmer Manual Entry (Milk &amp; Feed)</li>
        <li>Optional IoT Sensors</li>
      </ul>
    </div>

    <!-- Box 2: Edge Tier -->
    <div class="word-box" id="box-edge">
      <div class="box-title">EDGE &amp; MOBILE APP TIER</div>
      <ul class="box-bullets">
        <li>QR Code Scanner &amp; Decoder</li>
        <li>Data Validation &amp; Error Checks</li>
        <li>Offline Data Storage &amp; Cache</li>
        <li>Secure API Dispatcher</li>
      </ul>
    </div>

    <!-- Box 3: User Terminals -->
    <div class="word-box" id="box-user">
      <div class="box-title">USER INTERFACES TIER</div>
      <ul class="box-bullets">
        <li>Farmer Mobile Dashboard</li>
        <li>Veterinarian Triage Portal</li>
        <li>Admin &amp; Outbreak Dashboard</li>
        <li>Push &amp; SMS Alerts</li>
      </ul>
    </div>

    <!-- Box 4: Cloud Engine -->
    <div class="word-box" id="box-cloud">
      <div class="box-title">CLOUD COMPUTING &amp; ANALYTICS ENGINE</div>
      <ul class="box-bullets">
        <li>Data Cleaning &amp; Missing Value Imputation</li>
        <li>14-Day Rolling Health Baseline Calculation</li>
        <li>CHDI Health Anomaly Score Calculator</li>
        <li>Data Quality &amp; Uncertainty Checks</li>
        <li>Root-Cause Feature Explainability</li>
        <li>AI Model Retraining Pipeline</li>
        <li>Regional Outbreak Detection Engine</li>
      </ul>
    </div>

    <!-- Box 5: Storage -->
    <div class="word-box" id="box-store">
      <div class="box-title">DATABASE &amp; STORAGE TIER</div>
      <ul class="box-bullets">
        <li>Cattle Profiles &amp; Life Records</li>
        <li>Time-Series Health Database</li>
        <li>Baseline &amp; Covariance Data</li>
        <li>Vet Diagnosis &amp; Clinical Overrides</li>
        <li>Regional Outbreak Records</li>
      </ul>
    </div>

    <!-- Connectors -->
    <svg class="svg-arrows" viewBox="0 0 1160 525">
      <defs>
        <marker id="black-arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000" />
        </marker>
      </defs>

      <!-- Arrow 1: Physical Tier (350, 97) -> Edge App Tier (395, 97) -->
      <line x1="350" y1="97" x2="387" y2="97" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Arrow 2: Edge App Tier (760, 97) -> User Interfaces (805, 97) -->
      <line x1="760" y1="97" x2="797" y2="97" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Arrow 3: Cloud Engine (435, 230) -> Edge App Tier bottom (435, 190) (pointing UP) -->
      <line x1="435" y1="230" x2="435" y2="198" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Arrow 4: Cloud Engine (760, 372) -> Database Tier (805, 372) -->
      <line x1="760" y1="372" x2="797" y2="372" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />
    </svg>
  </div>

</body>
</html>
"""

    temp_html = os.path.abspath("temp_bw_snug.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    out_png = os.path.abspath("patent_figures/figure1_bw_simple_architecture.png")
    subprocess.run([
        edge_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1220,600",
        f"--screenshot={out_png}",
        f"file:///{temp_html}"
    ], check=True)

    # Copy to artifact folder for chat display
    art_png = os.path.join(artifact_dir, "figure1_bw_simple_architecture.png")
    shutil.copy2(out_png, art_png)

    # Update master figure1_system_architecture.png
    dest_fig = os.path.abspath("patent_figures/figure1_system_architecture.png")
    shutil.copy2(out_png, dest_fig)

    # Update docx image3 as well
    docx_path = 'SmartCattle_Project_Report_Aligned.docx'
    if os.path.exists(docx_path):
        import zipfile
        with open(out_png, 'rb') as f:
            new_img_data = f.read()
        in_zip = zipfile.ZipFile(docx_path, 'r')
        zip_dict = {}
        for item in in_zip.infolist():
            if item.filename == 'word/media/image3.png':
                zip_dict[item.filename] = new_img_data
            else:
                zip_dict[item.filename] = in_zip.read(item.filename)
        in_zip.close()
        temp_docx = 'temp_update_bw.docx'
        with zipfile.ZipFile(temp_docx, 'w', compression=zipfile.ZIP_DEFLATED) as out_zip:
            for fname, data in zip_dict.items():
                out_zip.writestr(fname, data)
        shutil.copy2(temp_docx, docx_path)
        if os.path.exists('SmartCattle_Project_Report.docx'):
            try: shutil.copy2(temp_docx, 'SmartCattle_Project_Report.docx')
            except Exception: pass
        if os.path.exists(temp_docx):
            os.remove(temp_docx)

    if os.path.exists(temp_html):
        os.remove(temp_html)

    print("Success: Generated snug B&W simple words architecture diagram!")

if __name__ == "__main__":
    generate_perfect_bw_architecture()
