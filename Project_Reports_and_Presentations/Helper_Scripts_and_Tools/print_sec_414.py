import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r'c:\Project\SmartCattle new\QR MINI PROJECT REPORT.docx')
for i in range(379, 401):
    p = doc.paragraphs[i]
    print(f"P[{i}]: text='{p.text}'")
