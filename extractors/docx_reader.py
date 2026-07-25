from docx import Document

def extract_docx_text(file_path):
    """
    Extract text from a DOCX resume.
    """
    doc = Document(file_path)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text