import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r'c:\Project\SmartCattle new\QR MINI PROJECT REPORT.docx')
academic_words = [
    'learner', 'learners', 'explore the concept', 'student', 'students',
    'assignment', 'syllabus', 'exercise', 'instructor', 'curriculum',
    'grade', 'homework', 'tutorial', 'lab manual'
]

print("=== CHECKING FOR COURSE / STUDENT / SYLLABUS ARTIFACTS ===")
for i, p in enumerate(doc.paragraphs):
    text = p.text
    for w in academic_words:
        if w in text.lower():
            print(f"P[{i}] (found '{w}'):\n  {text}\n")
            break
