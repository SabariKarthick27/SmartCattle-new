import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('comprehensive_section_audit.txt', 'r', encoding='utf-8') as f:
    text = f.read()

sections = text.split('='*70)

print(f"Total sections: {len(sections)}")

for sec in sections:
    lines = sec.strip().split('\n')
    if not lines or not lines[0]:
        continue
    header = lines[0]
    content = '\n'.join(lines[1:])
    # check for interesting patterns or anomalies
    # e.g., check mention of datasets, numbers, technologies
    if "SECTION:" in header:
        sec_name = header.replace("SECTION:", "").split("(")[0].strip()
        has_smartcattle = "smartcattle" in content.lower()
        has_qr = "qr" in content.lower()
        has_chdi = "chdi" in content.lower()
        # print summary
        p_count = len([l for l in lines if l.startswith('[')])
        print(f"Section: {sec_name} | Paras: {p_count}")
