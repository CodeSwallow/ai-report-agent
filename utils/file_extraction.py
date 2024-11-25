from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt

def validate_file_type(content_type: str) -> str:
    if content_type == 'application/pdf':
        return "pdf"
    elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return "docx"
    elif content_type == 'text/plain':
        return "txt"
    else:
        raise ValueError("Invalid file type. Only PDF, DOCX, and TXT are accepted.")

async def extract_text(document, file_type: str) -> str:
    content = await document.read()
    if file_type == "pdf":
        return extract_text_from_pdf(content)
    elif file_type == "docx":
        return extract_text_from_docx(content)
    elif file_type == "txt":
        return extract_text_from_txt(content)
