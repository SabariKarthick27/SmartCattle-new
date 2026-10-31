import os
from PIL import Image

ext_dir = r'c:\Project\SmartCattle new\report_extracted_figures'

# Let's inspect the top-left area of image17, 18, 19, 20, 21
for img_name in ['image17.png', 'image18.png', 'image19.png', 'image20.png', 'image21.png']:
    p = os.path.join(ext_dir, img_name)
    im = Image.open(p)
    print(f"=== {img_name} ({im.size}) ===")
    # Check bounding box of non-empty content
    bbox = im.getbbox()
    print(f"  BBox: {bbox}")
