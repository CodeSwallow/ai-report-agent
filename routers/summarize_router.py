from fastapi import APIRouter, UploadFile, Form, Depends
from typing import Optional
from services.summarize_service import process_summarization
from utils.response_helpers import create_error_response

router = APIRouter()

@router.post("/summarize")
async def summarize(
    document: UploadFile = Form(...),
    tone: str = Form(...),
    template: str = Form(...),
    user_type: str = Form(...),
    ip_address: str = Form(...),
    additional_info: Optional[str] = Form(None),
):
    try:
        return await process_summarization(
            document=document,
            tone=tone,
            template=template,
            user_type=user_type,
            ip_address=ip_address,
            additional_info=additional_info
        )
    except ValueError as e:
        return create_error_response(str(e), 400)