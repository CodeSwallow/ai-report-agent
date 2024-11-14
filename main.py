import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
from ai_agent.ai_agent import call_agent
from utils.pdf_utils import extract_text_from_pdf

app = FastAPI()


@app.post("/summarize")
async def summarize(
    document: UploadFile = File(...),
    tone: str = Form(...),
    template: str = Form(...),
    additional_info: Optional[str] = Form(None)
):
    if document.content_type != 'application/pdf':
        error_response = {
            "error": True,
            "code": 400,
            "message": "Invalid file type. Only PDFs are accepted for now."
        }
        return StreamingResponse(
            (json.dumps(error_response) + "\n" for _ in range(1)),
            media_type="application/x-ndjson",
            status_code=400
        )

    pdf_bytes = await document.read()
    text_content = extract_text_from_pdf(pdf_bytes)

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
