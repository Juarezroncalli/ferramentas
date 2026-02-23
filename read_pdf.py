import sys
try:
    import fitz
    doc = fitz.open('renata.pdf')
    with open('out.txt', 'w', encoding='utf-8') as f:
        for page in doc:
            f.write(page.get_text())
except ImportError:
    import PyPDF2
    with open('renata.pdf', 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        with open('out.txt', 'w', encoding='utf-8') as f:
            for page in reader.pages:
                f.write(page.extract_text() + '\n')
except Exception as e:
    with open('out_error.txt', 'w', encoding='utf-8') as f:
        f.write(str(e))
