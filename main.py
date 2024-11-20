import json
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional
from ai_agent.ai_agent import call_agent
from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from services.word_limit.word_limit_checker_factory import WordLimitCheckerFactory

app = FastAPI()


@app.post("/summarize")
async def summarize(
    document: UploadFile = File(...),
    tone: str = Form(...),
    template: str = Form(...),
    user_type: str = Form(...),
    additional_info: Optional[str] = Form(None)
):
    """
    This function handles the summarization request by accepting a PDF document, tone, template, and additional information.
    It validates the document type, extracts text from the PDF, and calls the AI agent to generate a summary.
    The summary is then streamed back as a JSON response.

    Parameters:
    - document (UploadFile): The uploaded PDF document.
    - tone (str): The tone of the summary.
    - template (str): The template for the summary.
    - additional_info (Optional[str]): Additional information for the AI agent.

    Returns:
    - StreamingResponse: A JSON response containing the summary or an error message.
    """
    if document.content_type == 'application/pdf':
        pdf_bytes = await document.read()
        text_content = extract_text_from_pdf(pdf_bytes)
    elif document.content_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        docx_bytes = await document.read()
        text_content = extract_text_from_docx(docx_bytes)
    elif document.content_type in ['text/plain']:
        txt_bytes = await document.read()
        text_content = extract_text_from_txt(txt_bytes)
    else:
        error_response = {
            "error": True,
            "code": 400,
            "message": "Invalid file type. Only PDF, DOCX, and TXT are accepted.",
            "content": "Please upload a valid PDF, DOCX, or TXT file."
        }
        return StreamingResponse(
            (json.dumps(error_response) + "\n" for _ in range(1)),
            media_type="application/x-ndjson",
            status_code=400
        )

    word_limit_checker = WordLimitCheckerFactory.get_checker(user_type)
    if not word_limit_checker.check_word_limit(text_content):
        error_response = {
            "error": True,
            "code": 400,
            "message": "Document exceeds the word limit for free users.",
            "content": "Please upgrade to a pro account to access unlimited word limits."
        }
        print(f"Error: {error_response['message']}"),
        return StreamingResponse(
            (json.dumps(error_response) + "\n" for _ in range(1)),
            media_type="application/x-ndjson",
            status_code=400
        )

    def stream_response():
        for json_chunk in call_agent(
            content=text_content,
            tone=tone,
            template=template,
            additional_info=additional_info
        ):
            yield json_chunk

    return StreamingResponse(
        stream_response(),
        media_type="application/x-ndjson"
    )
