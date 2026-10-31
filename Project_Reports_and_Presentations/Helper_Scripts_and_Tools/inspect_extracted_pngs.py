import os
from PIL import Image

extract_dir = r'c:\Project\SmartCattle new\report_extracted_figures'
files = sorted(os.listdir(extract_dir), key=lambda x: int(x.replace('image', '').replace('.png', '').replace('.jpeg', '').replace('.jpg', '')) if any(c.isdigit() for c in x) else 0)

for f in files:
    fp = os.path.join(extract_dir, f)
    try:
        im = Image.open(fp)
        print(f"{f:12s}: {im.width}x{im.height} | Mode: {im.mode} | Format: {im.format} | Size: {os.path.getsize(fp):,} bytes")
    except Exception as e:
        print(f"{f:12s}: Error {e}")
