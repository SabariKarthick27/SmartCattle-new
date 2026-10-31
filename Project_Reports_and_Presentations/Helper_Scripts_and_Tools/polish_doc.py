import docx

doc = docx.Document(r'Project_Report_Final_Updated.docx')

for p in doc.paragraphs:
    if "5-dimensional standardized deviation vector" in p.text:
        p.text = p.text.replace("5-dimensional standardized deviation vector", "4-dimensional standardized deviation vector")
        print("Updated 5-dimensional to 4-dimensional in p.text")

# Let's inspect Table 4.3 (CHDI Bands table)
# Let's find Table 4.3
for t_idx, t in enumerate(doc.tables):
    for r in t.rows:
        for c in r.cells:
            if "80 – 100" in c.text or "80 - 100" in c.text:
                c.text = c.text.replace("80 – 100", "≥ 75").replace("80 - 100", "≥ 75")
                print("Updated Table 4.3 healthy band")
            if "60 – 79" in c.text or "60 - 79" in c.text:
                c.text = c.text.replace("60 – 79", "50 – 74").replace("60 - 79", "50 - 74")
                print("Updated Table 4.3 watch band")
            if "40 – 59" in c.text or "40 - 59" in c.text:
                c.text = c.text.replace("40 – 59", "< 50 (At-Risk)").replace("40 - 59", "< 50 (At-Risk)")
                print("Updated Table 4.3 warning band")
            if "0 – 39" in c.text or "0 - 39" in c.text:
                c.text = c.text.replace("0 – 39", "Abstain (N < 7)").replace("0 - 39", "Abstain (N < 7)")
                print("Updated Table 4.3 critical/abstain band")

doc.save(r'Project_Report_Final_Updated.docx')
print("Successfully polished Project_Report_Final_Updated.docx!")
