import docx
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r'c:\Project\SmartCattle new\QR MINI PROJECT REPORT.docx')

full_text = " ".join(p.text for p in doc.paragraphs)
for t in doc.tables:
    for row in t.rows:
        full_text += " " + " ".join(c.text for c in row.cells)

# Find all uppercase acronyms of 2 to 6 letters
acronyms = set(re.findall(r'\b[A-Z]{2,6}\b', full_text))

# Filter out common English words or non-abbreviations
exclude = {'AND', 'THE', 'FOR', 'NOT', 'ALL', 'SEE', 'NEW', 'DAY', 'ANY', 'OUT', 'RAW', 'DROP', 'DATE', 'CODE', 'PAGE', 'UNIT', 'TIME', 'WHAT', 'WITH', 'FROM', 'EACH', 'THIS', 'THAT', 'INTO', 'SOME', 'BOTH', 'WELL', 'MUCH', 'VERY', 'HIGH', 'LOW', 'OPEN', 'TRUE', 'DATA', 'BASE', 'USER', 'ROLE', 'HERD', 'MORE', 'LESS', 'SHOW', 'WILL', 'HAVE', 'BEEN', 'WERE', 'THEY', 'THEM', 'THEN', 'ALSO', 'ONLY', 'SUCH', 'EVEN', 'OVER', 'LIKE', 'JUST', 'MOST', 'WAYS', 'MAKE', 'MADE', 'USED', 'USES', 'CASE', 'CARE', 'COST', 'PLAN', 'PART', 'PASS', 'FORM', 'FULL', 'FAST', 'FEED', 'MILK', 'COW', 'COWS', 'BULL', 'CALF', 'CALVES', 'HERD', 'FARM', 'FARMS', 'SOIL', 'CROP', 'LEAD', 'RISK', 'WARN', 'BAND', 'PEAK', 'ZERO', 'GOAL', 'POST', 'SEND', 'SCAN', 'READ', 'SAVE', 'FIND', 'CALL', 'JSON', 'HTML', 'HTTP', 'HTTPS', 'UUID', 'CUID', 'BLOB', 'CRUD', 'TEXT', 'NULL', 'MEAN', 'IEEE', 'USA', 'UK'}

found_acronyms = {}
for ac in sorted(acronyms - exclude):
    matches = len(re.findall(r'\b' + re.escape(ac) + r'\b', full_text))
    if matches >= 1:
        found_acronyms[ac] = matches

print("All Acronyms found in document:")
for ac, count in sorted(found_acronyms.items(), key=lambda x: x[1], reverse=True):
    print(f"  {ac:10s}: {count:3d} occurrence(s)")
