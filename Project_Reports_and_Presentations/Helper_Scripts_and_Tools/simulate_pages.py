import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Load doc
doc = docx.Document("SmartCattle_Mini_Project_Report_v4.docx")

# Let's inspect the exact elements from Chapter 1 to Appendix
# In docx, the body elements are in document.element.body
body = doc._element.body

print("Analyzing document structure element by element...")
element_types = []
for child in body:
    tag = child.tag.split('}')[-1]
    if tag in ['p', 'tbl', 'sectPr']:
        element_types.append(tag)

print(f"Total top-level elements: {len(element_types)} ({element_types.count('p')} paragraphs, {element_types.count('tbl')} tables, {element_types.count('sectPr')} sections)")
