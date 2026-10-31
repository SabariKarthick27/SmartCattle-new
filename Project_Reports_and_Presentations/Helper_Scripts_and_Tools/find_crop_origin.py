from PIL import Image
import os

ext_dir = r'c:\Project\SmartCattle new\report_extracted_figures'
ui_dir = r'c:\Project\SmartCattle new\captured_ui_screenshots'

# Check if image17, 19, 20, 21 match subregions of any of the 5 full screenshots
full_images = {}
for f in os.listdir(ui_dir):
    full_images[f] = Image.open(os.path.join(ui_dir, f))

for sub_name in ['image17.png', 'image19.png', 'image20.png', 'image21.png']:
    sub_im = Image.open(os.path.join(ext_dir, sub_name)).convert('RGB')
    sub_w, sub_h = sub_im.size
    print(f"\nSearching origin of {sub_name} ({sub_w}x{sub_h})...")
    
    found = False
    for full_name, full_im in full_images.items():
        # sample 5 pixel positions
        sample_pts = [(10, 10), (sub_w//2, sub_h//2), (sub_w-10, sub_h-10)]
        # let's check average color
        sub_pixels = list(sub_im.getdata())
        sub_avg_r = sum(p[0] for p in sub_pixels) / len(sub_pixels)
        sub_avg_g = sum(p[1] for p in sub_pixels) / len(sub_pixels)
        sub_avg_b = sum(p[2] for p in sub_pixels) / len(sub_pixels)
        
        # let's do a simple template match or correlation
        # check top-left pixel block
        sub_sample = [sub_im.getpixel((x, y)) for x in range(0, min(sub_w, 20), 5) for y in range(0, min(sub_h, 20), 5)]
        
        for y in range(0, full_im.height - sub_h, 20):
            for x in range(0, full_im.width - sub_w, 20):
                full_sample = [full_im.getpixel((x+px, y+py))[:3] for px in range(0, min(sub_w, 20), 5) for py in range(0, min(sub_h, 20), 5)]
                if sub_sample == full_sample:
                    print(f"  FOUND EXACT MATCH! {sub_name} was cropped from: {full_name} at (x={x}, y={y})!")
                    found = True
                    break
            if found:
                break
    if not found:
        print(f"  {sub_name} did not match an exact crop of captured_ui_screenshots.")
