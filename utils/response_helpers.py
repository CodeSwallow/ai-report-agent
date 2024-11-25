from fastapi.responses import StreamingResponse
import json


def create_error_response(message: str, code: int) -> StreamingResponse:
    error_response = {
        "error": True,
        "code": code,
        "message": message,
    }
    return StreamingResponse(
        (json.dumps(error_response) + "\n" for _ in range(1)),
        media_type="application/x-ndjson",
        status_code=code
    )
