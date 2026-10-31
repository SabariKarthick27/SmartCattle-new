import os
import hashlib

def sha256(fname):
    h = hashlib.sha256()
    with open(fname, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

target_hashes = {
    'image17.png': '0b3eec42d945',
    'image18.png': 'fd897024d0ac',
    'image19.png': 'f056e54a018b',
    'image20.png': '6bdbc209c960',
    'image21.png': '0d01b0f3be06',
    'image22.png': '1eb8',
    'image23.png': '2acb',
    'image24.png': '3d4e'
}

for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root or '.next' in root:
        continue
    for f in files:
        if f.endswith(('.png', '.jpg', '.jpeg')):
            fp = os.path.join(root, f)
            try:
                h = sha256(fp)
                for img_name, prefix in target_hashes.items():
                    if h.startswith(prefix):
                        print(f"Match for {img_name}: {fp} ({os.path.getsize(fp):,} bytes)")
            except Exception:
                pass
