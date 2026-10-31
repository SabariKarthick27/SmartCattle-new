import docx
import difflib

# Load current docx
doc = docx.Document(r'Project_Report_Final_20_10_26 (1).docx')
current_paras = [p.text for p in doc.paragraphs if p.text.strip()]

# Load old dump
with open('scratch_report_text.txt', 'r', encoding='utf-8') as f:
    old_lines = [line.strip() for line in f if line.strip() and not line.startswith('--- TABLE')]
# Strip [P...] prefix from old_lines
old_paras = []
for line in old_lines:
    if line.startswith('[P') and ']' in line:
        old_paras.append(line.split(']', 1)[1].strip())
    else:
        old_paras.append(line)

print(f"Old paragraphs count: {len(old_paras)}")
print(f"Current paragraphs count: {len(current_paras)}")

diff = list(difflib.unified_diff(old_paras, current_paras, fromfile='before_edit', tofile='after_edit', lineterm=''))
with open('user_changes_diff.txt', 'w', encoding='utf-8') as out:
    for line in diff:
        out.write(line + '\n')

print(f"Total diff lines: {len(diff)}")
