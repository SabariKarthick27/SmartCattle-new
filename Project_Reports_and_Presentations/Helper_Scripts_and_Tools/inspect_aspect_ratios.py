import os
from PIL import Image

ext_dir = r'c:\Project\SmartCattle new\report_extracted_figures'
ui_dir = r'c:\Project\SmartCattle new\captured_ui_screenshots'

print("--- EXAMINING EXTRACTED UI IMAGES ---")
for f in ['image17.png', 'image18.png', 'image19.png', 'image20.png', 'image21.png']:
    p = os.path.join(ext_dir, f)
    im = Image.open(p)
    print(f"{f}: size={im.size}, aspect_ratio={im.width/im.height:.2f}")

print("\n--- EXAMINING CAPTURED UI SCREENSHOTS ---")
for f in os.listdir(ui_dir):
    p = os.path.join(ui_dir, f)
    im = Image.open(p)
    print(f"{f}: size={im.size}, aspect_ratio={im.width/im.height:.2f}")
