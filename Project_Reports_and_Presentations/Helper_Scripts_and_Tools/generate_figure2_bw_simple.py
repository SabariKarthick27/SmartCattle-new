import os
import subprocess
import shutil

def generate_figure2_bw_simple():
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
    width: 1160px;
    height: 800px;
    background-color: #ffffff;
    font-family: Arial, Calibri, 'Segoe UI', sans-serif;
    color: #000000;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 18px 25px;
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
  }

  .main-title {
    font-size: 21px;
    font-weight: bold;
    color: #000000;
    letter-spacing: 0.5px;
    margin-bottom: 22px;
    text-align: center;
    text-transform: uppercase;
  }

  .canvas-area {
    width: 1110px;
    height: 720px;
    position: relative;
  }

  /* Black & White MS Word Shape Boxes */
  .step-box {
    position: absolute;
    width: 505px;
    height: 125px;
    border: 2px solid #000000;
    border-radius: 8px;
    background: #ffffff;
    padding: 12px 18px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  .step-title {
    font-size: 14.5px;
    font-weight: bold;
    color: #000000;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-bottom: 8px;
    border-bottom: 1px solid #000000;
    padding-bottom: 4px;
    width: 100%;
  }

  .step-desc {
    font-size: 13px;
    color: #111111;
    line-height: 1.35;
  }

  /* Left Column (x = 10px) */
  #step-1 { left: 10px; top: 10px; }
  #step-3 { left: 10px; top: 190px; }
  #step-5 { left: 10px; top: 370px; }
  #step-7 { left: 10px; top: 550px; }

  /* Right Column (x = 595px) */
  #step-2 { left: 595px; top: 10px; }
  #step-4 { left: 595px; top: 190px; }
  #step-6 { left: 595px; top: 370px; }
  #step-8 { left: 595px; top: 550px; }

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

  <div class="main-title">FIGURE 2: END-TO-END OPERATIONAL WORKFLOW PIPELINE</div>

  <div class="canvas-area">
    <!-- STEP 1 -->
    <div class="step-box" id="step-1">
      <div class="step-title">STEP 1: ANIMAL REGISTRATION &amp; QR CODE ISSUANCE</div>
      <div class="step-desc">Register cattle details, issue unique QR code ear tag, and initialize animal health record in system.</div>
    </div>

    <!-- STEP 2 -->
    <div class="step-box" id="step-2">
      <div class="step-title">STEP 2: DAILY HEALTH DATA COLLECTION</div>
      <div class="step-desc">Farmer scans QR tag and logs daily milk yield, feed intake, body weight, and rumination activity.</div>
    </div>

    <!-- STEP 3 -->
    <div class="step-box" id="step-3">
      <div class="step-title">STEP 3: 14-DAY HEALTH BASELINE CALCULATION</div>
      <div class="step-desc">Calculates individualized rolling averages and normal health variation after 7–14 days of logged data.</div>
    </div>

    <!-- STEP 4 -->
    <div class="step-box" id="step-4">
      <div class="step-title">STEP 4: CHDI HEALTH SCORE COMPUTATION</div>
      <div class="step-desc">Computes 0–100 composite health score; safely holds alerts if data is insufficient to prevent false alarms.</div>
    </div>

    <!-- STEP 5 -->
    <div class="step-box" id="step-5">
      <div class="step-title">STEP 5: ALERT EXPLANATION &amp; VET CASE DISPATCH</div>
      <div class="step-desc">Identifies which vitals caused the health drop and automatically creates a priority ticket for the regional vet.</div>
    </div>

    <!-- STEP 6 -->
    <div class="step-box" id="step-6">
      <div class="step-title">STEP 6: VETERINARY CHECKUP &amp; DIAGNOSIS</div>
      <div class="step-desc">Vet examines cow on-site, records diagnosis, logs medical treatments, and confirms or overrides the alert.</div>
    </div>

    <!-- STEP 7 -->
    <div class="step-box" id="step-7">
      <div class="step-title">STEP 7: AI MODEL RETRAINING &amp; IMPROVEMENT</div>
      <div class="step-desc">Uses verified veterinary diagnoses to periodically update and refine the AI health prediction models.</div>
    </div>

    <!-- STEP 8 -->
    <div class="step-box" id="step-8">
      <div class="step-title">STEP 8: REGIONAL OUTBREAK MONITORING</div>
      <div class="step-desc">Groups health anomalies across nearby farms on a map to detect and warn of contagious epidemics early.</div>
    </div>

    <!-- Directional Connectors -->
    <svg class="svg-arrows" viewBox="0 0 1110 720">
      <defs>
        <marker id="black-arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000" />
        </marker>
      </defs>

      <!-- Horizontal Arrow: Step 1 -> Step 2 (y = 72) -->
      <line x1="515" y1="72" x2="587" y2="72" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Vertical Arrow: Step 1 -> Step 3 (x = 262) -->
      <line x1="262" y1="135" x2="262" y2="182" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Vertical Arrow: Step 2 -> Step 4 (x = 847) -->
      <line x1="847" y1="135" x2="847" y2="182" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Horizontal Arrow: Step 3 -> Step 4 (y = 252) -->
      <line x1="515" y1="252" x2="587" y2="252" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Vertical Arrow: Step 3 -> Step 5 (x = 262) -->
      <line x1="262" y1="315" x2="262" y2="362" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Vertical Arrow: Step 4 -> Step 6 (x = 847) -->
      <line x1="847" y1="315" x2="847" y2="362" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Horizontal Arrow: Step 5 -> Step 6 (y = 432) -->
      <line x1="515" y1="432" x2="587" y2="432" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Vertical Arrow: Step 5 -> Step 7 (x = 262) -->
      <line x1="262" y1="495" x2="262" y2="542" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />

      <!-- Vertical Arrow: Step 6 -> Step 8 (x = 847) -->
      <line x1="847" y1="495" x2="847" y2="542" stroke="#000000" stroke-width="2.2" marker-end="url(#black-arr)" />
    </svg>
  </div>

</body>
</html>
"""

    temp_html = os.path.abspath("temp_fig2_bw_simple.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    out_png = os.path.abspath("patent_figures/figure2_operational_workflow_bw.png")
    subprocess.run([
        edge_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1160,800",
        f"--screenshot={out_png}",
        f"file:///{temp_html}"
    ], check=True)

    # Save to artifacts directory for chat view
    art_png = os.path.join(artifact_dir, "figure2_operational_workflow_bw.png")
    shutil.copy2(out_png, art_png)

    # Backup old figure2 and replace with clean B&W
    backup_fig2 = os.path.abspath("patent_figures/figure2_operational_workflow_original.png")
    if not os.path.exists(backup_fig2):
        shutil.copy2("patent_figures/figure2_operational_workflow.png", backup_fig2)
    shutil.copy2(out_png, "patent_figures/figure2_operational_workflow.png")

    # Update in Word docx files if they contain figure2
    for docx_file in ["SmartCattle_Project_Report_Aligned_MASTER.docx", "SmartCattle_Project_Report_Aligned.docx", "SmartCattle_Project_Report.docx", "SmartCattle_Project_Report_PERFECT_MATH.docx"]:
        if os.path.exists(docx_file):
            try:
                import zipfile
                with open(out_png, 'rb') as f:
                    new_img_data = f.read()
                in_zip = zipfile.ZipFile(docx_file, 'r')
                zip_dict = {}
                found_fig2 = False
                # Figure 2 is image4.png in the report
                for item in in_zip.infolist():
                    if item.filename == 'word/media/image4.png':
                        zip_dict[item.filename] = new_img_data
                        found_fig2 = True
                    else:
                        zip_dict[item.filename] = in_zip.read(item.filename)
                in_zip.close()
                if found_fig2:
                    temp_docx = "temp_upd_f2.docx"
                    with zipfile.ZipFile(temp_docx, 'w', compression=zipfile.ZIP_DEFLATED) as out_zip:
                        for fname, data in zip_dict.items():
                            out_zip.writestr(fname, data)
                    shutil.copy2(temp_docx, docx_file)
                    os.remove(temp_docx)
                    print(f"Updated Figure 2 in {docx_file}")
            except Exception as e:
                print(f"Could not update {docx_file}: {e}")

    if os.path.exists(temp_html):
        os.remove(temp_html)

    print("Success: Generated Figure 2 B&W simple words workflow pipeline!")

if __name__ == "__main__":
    generate_figure2_bw_simple()
