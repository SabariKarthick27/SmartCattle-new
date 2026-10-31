import docx
import shutil

src_path = r'Project_Report_Final_20_10_26 (1).docx'
dst_path = r'Project_Report_Final_Updated.docx'

# Copy first to preserve everything (styles, images, rels, formatting)
shutil.copyfile(src_path, dst_path)
doc = docx.Document(dst_path)

print(f"Total paragraphs before: {len(doc.paragraphs)}")

# Let's inspect where drawing images are for 4.7, 4.8, 4.9
# We want to insert narrative paragraphs before Eq 4.7, Eq 4.8, and Eq 4.9
for i, p in enumerate(doc.paragraphs):
    # Eq 4.4 updates
    if "5 × 5 empirical covariance matrix" in p.text:
        p.text = p.text.replace("5 × 5 empirical covariance matrix capturing dependencies across all 5 telemetry features.", 
                                "4 × 4 empirical covariance matrix capturing dependencies across the 4 core telemetry features (body weight, feed intake, milk production, core temperature).")
        print(f"Updated Eq 4.4 text in P{i}")
    
    # Eq 4.5 updates
    if "Standardized 5-signal deviation vector" in p.text:
        p.text = p.text.replace("Standardized 5-signal deviation vector across all monitored features [zweight, zfeed, zmilk, ztemp]ᵀ.",
                                "Standardized 4-signal deviation vector across all monitored features [zweight, zfeed, zmilk, ztemp]ᵀ.")
        print(f"Updated Eq 4.5 text in P{i}")

    # Eq 4.6 bands updates
    if "Clinical Bands: Healthy (80–100)" in p.text:
        p.text = p.text.replace("Clinical Bands: Healthy (80–100), Watch (60–79), Warning (40–59), and Critical (0–39).",
                                "Clinical Bands: Healthy (≥ 75), Watch (50–74), At-Risk (< 50), and Abstain (N < 7 or Ct < 0.40).")
        print(f"Updated Eq 4.6 bands in P{i}")

    # Eq 4.8 text updates
    if "Full Mahalanobis anomaly distance across all 5 telemetry features." in p.text:
        p.text = p.text.replace("all 5 telemetry features.", "all 4 telemetry features (body weight, feed intake, milk production, core temperature).")
        print(f"Updated Eq 4.8 text in P{i}")

doc.save(dst_path)
print("Saved basic replacements.")
