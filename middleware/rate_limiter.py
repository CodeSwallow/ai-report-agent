from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)


async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    print(f"Rate limit exceeded for {request.client.host}: {exc}")
    return JSONResponse(
        status_code=429,
        content={"error": True, "message": "Rate limit exceeded. Please try again later."},
    )