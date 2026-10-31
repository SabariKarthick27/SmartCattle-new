import docx
import zipfile
import xml.etree.ElementTree as ET

# Check relationships in document.xml.rels
with zipfile.ZipFile('Patent Sample (1).docx') as z:
    doc_xml = z.read('word/document.xml').decode('utf-8')
    rels_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')
    print("=== SAMPLE RELS ===")
    print(rels_xml)

with zipfile.ZipFile('QR_Based_Cattle_Management_Patent_Disclosure.docx') as z:
    c_doc_xml = z.read('word/document.xml').decode('utf-8')
    c_rels_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')
    print("=== CATTLE RELS ===")
    print(c_rels_xml)
