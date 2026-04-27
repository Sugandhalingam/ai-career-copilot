import fitz  # this is pymupdf

def extract_text_from_pdf(file_path):
    # Open the PDF file
    doc = fitz.open(file_path)
    
    text = ""
    
    # Loop through every page and extract text
    for page in doc:
        text += page.get_text()
    
    doc.close()
    
    return text.strip()