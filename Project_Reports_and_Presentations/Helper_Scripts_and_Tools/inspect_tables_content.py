import docx

doc_cattle = docx.Document('QR_Based_Cattle_Management_Patent_Disclosure.docx')

print("================ TABLES IN CATTLE DOC ================")
for t_idx, tbl in enumerate(doc_cattle.tables):
    print(f"\n================ TABLE {t_idx} ({len(tbl.rows)} rows x {len(tbl.columns)} cols) ================")
    for r_idx, row in enumerate(tbl.rows):
        print(f"--- ROW {r_idx} ---")
        for c_idx, cell in enumerate(row.cells):
            # deduplicate printed cells in merged rows
            print(f"  [Cell {c_idx}]: {cell.text.strip()}")
