import os

ext_dir = r'c:\Project\SmartCattle new\report_extracted_figures'
html_path = r'c:\Project\SmartCattle new\view_extracted_figures.html'

with open(html_path, 'w', encoding='utf-8') as f:
    f.write("<html><body style='font-family:sans-serif; background:#f0f0f0; padding:20px;'>\n")
    f.write("<h1>All Extracted Figures from QR MINI PROJECT REPORT.docx</h1>\n")
    for i in range(1, 25):
        ext = '.png' if i > 2 else '.jpeg'
        fname = f"image{i}{ext}"
        fpath = os.path.join(ext_dir, fname)
        if os.path.exists(fpath):
            f.write(f"<div style='background:#fff; margin:20px 0; padding:15px; border-radius:8px;'>\n")
            f.write(f"<h3>{fname}</h3>\n")
            f.write(f"<img src='report_extracted_figures/{fname}' style='max-width:800px; display:block; margin-bottom:10px; border:1px solid #ccc;'/>\n")
            f.write("</div>\n")
    f.write("</body></html>\n")

print("Created view_extracted_figures.html")
