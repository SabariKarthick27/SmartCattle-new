import docx

doc_sample = docx.Document('Patent Sample (1).docx')
doc_cattle = docx.Document('QR_Based_Cattle_Management_Patent_Disclosure.docx')

print("=== CHECKING PARAGRAPH LEVEL DIFFERENCES ===")
for i, (sp, cp) in enumerate(zip(doc_sample.paragraphs, doc_cattle.paragraphs)):
    # Check if text is same or different
    s_runs_fonts = [(r.font.name, r.font.size.pt if r.font.size else None, r.bold, r.italic) for r in sp.runs]
    c_runs_fonts = [(r.font.name, r.font.size.pt if r.font.size else None, r.bold, r.italic) for r in cp.runs]
    
    # Check if formatting matches
    if sp.style.name != cp.style.name or sp.alignment != cp.alignment:
        print(f"P{i} Style/Align diff: Sample({sp.style.name}, {sp.alignment}) vs Cattle({cp.style.name}, {cp.alignment})")
    
    if len(sp.runs) != len(cp.runs):
        # check if font styles differ
        pass

print("=== DONE CHECKING ===")
