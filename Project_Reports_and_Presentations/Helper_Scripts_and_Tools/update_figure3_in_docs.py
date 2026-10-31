import os
import zipfile
import shutil

def update_figure3():
    new_fig3_path = os.path.abspath("patent_figures/figure3_chdi_abstention_logic_bw.png")
    if not os.path.exists(new_fig3_path):
        print(f"File not found: {new_fig3_path}")
        return

    with open(new_fig3_path, "rb") as f:
        new_fig3_data = f.read()

    docx_files = [
        "SmartCattle_Project_Report_Aligned_MASTER.docx",
        "SmartCattle_Project_Report_PERFECT_MATH.docx",
        "SmartCattle_Project_Report_Aligned.docx",
        "SmartCattle_Project_Report.docx"
    ]

    for docx_file in docx_files:
        if not os.path.exists(docx_file):
            continue

        temp_docx = docx_file + ".tmp"
        with zipfile.ZipFile(docx_file, 'r') as zin, zipfile.ZipFile(temp_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            replaced = False
            for item in zin.infolist():
                if item.filename == "word/media/image5.png":
                    zout.writestr(item.filename, new_fig3_data)
                    replaced = True
                else:
                    zout.writestr(item, zin.read(item.filename))

        if replaced:
            try:
                if os.path.exists(docx_file):
                    os.replace(temp_docx, docx_file)
                else:
                    shutil.move(temp_docx, docx_file)
                print(f"Successfully updated image5.png (Figure 3) in {docx_file}")
            except Exception as e:
                print(f"Notice: Could not replace {docx_file} directly (may be open in Word): {e}")
                if os.path.exists(temp_docx):
                    os.remove(temp_docx)
        else:
            if os.path.exists(temp_docx):
                os.remove(temp_docx)
            print(f"image5.png not found in {docx_file}")

    # Also update artifact files if present
    artifact_dir = r"C:\Users\SABARIKARTHICK\.gemini\antigravity-ide\brain\5ea3760d-61ec-4b9d-a301-3985c4c1874a"
    for docx_file in ["SmartCattle_Project_Report_Aligned.docx", "SmartCattle_Project_Report_PERFECT_MATH.docx", "SmartCattle_Project_Report_Aligned_MASTER_CLEAN_MATH.docx"]:
        full_p = os.path.join(artifact_dir, docx_file)
        if os.path.exists(full_p):
            temp_docx = full_p + ".tmp"
            with zipfile.ZipFile(full_p, 'r') as zin, zipfile.ZipFile(temp_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    if item.filename == "word/media/image5.png":
                        zout.writestr(item.filename, new_fig3_data)
                    else:
                        zout.writestr(item, zin.read(item.filename))
            shutil.move(temp_docx, full_p)
            print(f"Updated artifact {docx_file}")

if __name__ == "__main__":
    update_figure3()
