import os
import pytesseract
from PIL import Image

extract_dir = r'c:\Project\SmartCattle new\report_extracted_figures'

for img_name in ['image17.png', 'image18.png', 'image19.png', 'image20.png', 'image21.png', 'image22.png', 'image23.png', 'image24.png']:
    fp = os.path.join(extract_dir, img_name)
    im = Image.open(fp)
    print(f"\n--- {img_name} ({im.width}x{im.height}) ---")
    # Try OCR if pytesseract or print image stats
    try:
        import pytesseract
        txt = pytesseract.image_to_string(im)
        first_lines = [l.strip() for l in txt.split('\n') if l.strip()][:4]
        print("  OCR: " + " | ".join(first_lines))
    except Exception as e:
        # If no tesseract, let's print color stats
        colors = im.getcolors(maxcolors=10)
        print(f"  No OCR available: {e}")
