from fastapi import APIRouter, UploadFile, Form, Request
from fastapi.responses import StreamingResponse
from typing import Optional
from services.summarize_service import process_summarization
from middleware.rate_limiter import limiter
from config import MINUTE_RATE_LIMIT, DAY_RATE_LIMIT

router = APIRouter()

@router.post("/summarize")
@limiter.limit(f"{MINUTE_RATE_LIMIT}/minute")
@limiter.limit(f"{DAY_RATE_LIMIT}/day")
async def summarize(
    request: Request,
    document: UploadFile = Form(...),
    tone: str = Form(...),
    template: str = Form(...),
    user_type: str = Form(...),
    ip_address: str = Form(...),
    additional_info: Optional[str] = Form(None),
    language: str = Form("en")
) -> StreamingResponse:
    print(f"Received request: {request}")
    return await process_summarization(
        document=document,
        tone=tone,
        template=template,
        user_type=user_type,
        ip_address=ip_address,
        additional_info=additional_info,
        language=language
    )