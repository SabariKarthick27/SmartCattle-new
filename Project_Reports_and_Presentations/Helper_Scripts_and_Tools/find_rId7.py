import zipfile
import re

with zipfile.ZipFile('Patent Sample (1).docx') as z:
    xml = z.read('word/document.xml').decode('utf-8')
    matches = [m.start() for m in re.finditer(r'rId7', xml)]
    for m in matches:
        print("Match rId7 context:")
        print(xml[max(0, m-200):min(len(xml), m+300)])
