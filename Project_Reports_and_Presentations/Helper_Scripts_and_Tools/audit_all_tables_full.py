import docx
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r'c:\Project\SmartCattle new\QR MINI PROJECT REPORT.docx')

print("="*80)
print(f"EXHAUSTIVE AUDIT OF ALL TABLES IN QR MINI PROJECT REPORT.docx")
print("="*80)

for idx, table in enumerate(doc.tables):
    rows = len(table.rows)
    cols = len(table.columns) if rows > 0 else 0
    # Look for table caption or title in text preceding table
    print(f"\nTABLE OBJECT {idx+1} [Size: {rows} rows x {cols} cols]")
    
    # Check for empty cells or anomalies
    empty_cells = []
    for r_i, row in enumerate(table.rows):
        for c_i, cell in enumerate(row.cells):
            t = cell.text.strip()
            if not t and idx not in [0, 1, 2, 3]: # Skip signature lines in certificates
                empty_cells.append((r_i, c_i))
    
    if empty_cells:
        print(f"  ⚠️ ALERT: Found {len(empty_cells)} EMPTY cell(s) at (row, col): {empty_cells}")

    # Print all rows
    for r_i, row in enumerate(table.rows):
        cells_text = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
        # remove consecutive identical cell texts resulting from column merges
        dedup = []
        for c in cells_text:
            if not dedup or c != dedup[-1]:
                dedup.append(c)
        print(f"  R{r_i}: {' | '.join(dedup)}")
