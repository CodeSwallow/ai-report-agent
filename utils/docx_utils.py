import io
from docx import Document


def extract_text_from_docx(docx_bytes: bytes) -> str:
    docx_file = io.BytesIO(docx_bytes)
    document = Document(docx_file)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text
