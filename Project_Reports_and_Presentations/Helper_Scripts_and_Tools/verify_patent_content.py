import docx

doc = docx.Document('Qr Based Cattle Management Patent-1.docx')
text = '\n'.join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])

print('Contains dollar sign:', chr(36) in text)
print('Contains cost figures (e.g. 150, 350, 0.50):', any(k in text for k in ['150', '350', '0.50']))

# Also try writing to Final if Word has been closed or switched
try:
    doc.save(r"c:\Project\SmartCattle new\Qr Based Cattle Management Patent - Final.docx")
    print("Successfully updated 'Qr Based Cattle Management Patent - Final.docx' as well!")
except Exception as e:
    print("Final docx currently locked in Word. Please close Word to unlock.")
