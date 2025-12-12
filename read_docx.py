from docx import Document
import os

docx_file = "fastapi_app/excelAnalysis/15712999190(15712999190)_20251212165312.docx"
abs_path = os.path.abspath(docx_file)

if os.path.exists(abs_path):
    doc = Document(abs_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    print("\n".join(full_text))
else:
    print("File not found")