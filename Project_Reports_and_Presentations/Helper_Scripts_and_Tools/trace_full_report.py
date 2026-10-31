import docx
import math

doc = docx.Document("SmartCattle_Mini_Project_Report_v4.docx")

# Page dimensions (A4, 1.25" left, 1.0" right, 1.0" top, 1.0" bottom)
PAGE_HEIGHT_PT = 11.69 * 72 # 841.68 pt
MARGIN_TOP_PT = 1.0 * 72 # 72 pt
MARGIN_BOTTOM_PT = 1.0 * 72 # 72 pt
USABLE_HEIGHT_PT = PAGE_HEIGHT_PT - MARGIN_TOP_PT - MARGIN_BOTTOM_PT # 697.68 pt

# Printable width
PAGE_WIDTH_PT = 8.27 * 72 # 595.44 pt
MARGIN_LEFT_PT = 1.25 * 72 # 90 pt
MARGIN_RIGHT_PT = 1.0 * 72 # 72 pt
USABLE_WIDTH_PT = PAGE_WIDTH_PT - MARGIN_LEFT_PT - MARGIN_RIGHT_PT # 433.44 pt (~6.02 in)

# Line pitch at 1.45 line spacing with 12pt font = 17.4 pt
LINE_PITCH_12PT = 12.0 * 1.45 # 17.4 pt
CHARS_PER_LINE = 88 # Approximate characters per line for Times New Roman 12pt in 433pt

# Preliminary pages mapping:
# 1: Title Page -> Page i (no page number displayed)
# 2: Bonafide Certificate -> Page ii
# 3: Declaration -> Page iii
# 4: Acknowledgement -> Page iv
# 5: Abstract -> Page v
# 6: Table of Contents (Starts on Page vi)
# Let's see how many pages TOC takes:
# TOC has ~55 entries. At ~22pt per entry, 55 entries = 1210 pt -> takes 2 full pages (Pages vi and vii)!
# 8: List of Tables (Starts on Page viii) - 13 tables = 1 page (Page viii)
# 9: List of Figures (Starts on Page ix) - 7 figures = 1 page (Page ix)
# 10: List of Abbreviations (Starts on Page x) - 20 items = 1 page (Page x)
# Chapter 1 starts on Page 1!

print("Preliminary Pages Breakdown:")
print("Cover Page: Page i")
print("Bonafide Certificate: Page ii")
print("Declaration: Page iii")
print("Acknowledgement: Page iv")
print("Abstract: Page v")
print("Table of Contents: Page vi - vii")
print("List of Tables: Page viii")
print("List of Figures: Page ix")
print("List of Abbreviations: Page x")
print("Chapter 1 Start: Page 1")
