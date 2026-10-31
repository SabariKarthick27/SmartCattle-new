import os
import hashlib

def sha256(fname):
    h = hashlib.sha256()
    with open(fname, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

ui_dir = r'c:\Project\SmartCattle new\captured_ui_screenshots'
ext_dir = r'c:\Project\SmartCattle new\report_extracted_figures'

print("--- CAPTURED UI SCREENSHOTS ---")
for f in os.listdir(ui_dir):
    p = os.path.join(ui_dir, f)
    print(f"{f:20s}: {os.path.getsize(p):,} bytes | sha256={sha256(p)[:12]}")

print("\n--- EXTRACTED REPORT IMAGES 17 TO 21 ---")
for f in ['image17.png', 'image18.png', 'image19.png', 'image20.png', 'image21.png']:
    p = os.path.join(ext_dir, f)
    print(f"{f:20s}: {os.path.getsize(p):,} bytes | sha256={sha256(p)[:12]}")
