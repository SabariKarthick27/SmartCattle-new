import os
from PIL import Image

def analyze_image(path):
    im = Image.open(path)
    # Check if there are distinct headers or text by sampling horizontal strips
    print(f"File: {os.path.basename(path)} | Size: {im.size} | Mode: {im.mode}")

for i in range(14, 25):
    p = rf"c:\Project\SmartCattle new\report_extracted_figures\image{i}.png"
    if os.path.exists(p):
        analyze_image(p)
