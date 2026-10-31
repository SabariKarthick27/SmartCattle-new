import docx
import os
import hashlib

def sha256_bytes(b):
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

target_hashes = {
    '0b3eec42d945': 'image17',
    'fd897024d0ac': 'image18 (qr_scan)',
    'f056e54a018b': 'image19',
    '6bdbc209c960': 'image20',
    '0d01b0f3be06': 'image21'
}

for f in os.listdir('.'):
    if f.endswith('.docx') and not f.startswith('~$'):
        try:
            d = docx.Document(f)
            found = []
            for r_id, rel in d.part.rels.items():
                if "image" in rel.target_ref:
                    h = sha256_bytes(rel.target_part.blob)[:12]
                    if h in target_hashes:
                        found.append((target_hashes[h], rel.target_ref))
            if found:
                print(f"File {f} contains: {found}")
        except Exception as e:
            pass
