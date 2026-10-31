import re

with open('scripts/build_comprehensive_report_with_code.py', 'r', encoding='utf-8') as f:
    text = f.read()

for line_num, line in enumerate(text.split('\n'), 1):
    if any(k in line for k in ['Figure 4.', 'Figure 5.', 'add_picture', 'image']):
        print(f"L{line_num}: {line.strip()[:100]}")
