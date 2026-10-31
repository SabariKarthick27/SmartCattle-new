import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('current_report_dump.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

sections = {}
current_sec = "PRELIMINARIES"
sections[current_sec] = []

for line in lines:
    line_clean = line.strip()
    if any(h in line_clean for h in [
        "1. INTRODUCTION",
        "2. LITERATURE REVIEW",
        "3. CHAPTER 1",
        "4. CHAPTER 2",
        "5. CHAPTER 3",
        "6. CHAPTER 4",
        "SDG GOALS",
        "REFERENCES"
    ]):
        current_sec = line_clean
        sections[current_sec] = []
    sections[current_sec].append(line_clean)

for sec_title, sec_lines in sections.items():
    print(f"\n==================================================")
    print(f"SECTION: {sec_title} ({len(sec_lines)} lines)")
    print(f"==================================================")
    for l in sec_lines[:5]:
        print("  " + l[:120])
    if len(sec_lines) > 5:
        print("  ...")
        for l in sec_lines[-3:]:
            print("  " + l[:120])
