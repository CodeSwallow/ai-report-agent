import weave
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from routers.summarize_router import router as summarize_router
from middleware.rate_limiter import limiter, custom_rate_limit_handler
from fastapi.responses import JSONResponse
from exceptions.backend_exceptions import APIConnectionError, APIRateLimitError, APIStatusError
from exceptions.summarization_exceptions import WordLimitExceededError
from utils.translations import get_translated_message

weave.init('summarizer-agent')

app = FastAPI()
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(WordLimitExceededError)
async def word_limit_error_handler(request: Request, exc: WordLimitExceededError):
    # Retrieve language from request.state (fallback to 'en')
    language = getattr(request.state, "language", "en")
    message = get_translated_message("WordLimitExceededError", language)
    return JSONResponse(
        status_code=402,
        content={"error": True, "message": message}
    )

@app.exception_handler(APIConnectionError)
async def api_connection_error_handler(request: Request, exc: APIConnectionError):
    language = getattr(request.state, "language", "en")
    message = get_translated_message("APIConnectionError", language)
    return JSONResponse(
        status_code=503,
        content={"error": True, "message": message}
    )

@app.exception_handler(APIRateLimitError)
async def api_rate_limit_error_handler(request: Request, exc: APIRateLimitError):
    language = getattr(request.state, "language", "en")
    message = get_translated_message("APIRateLimitError", language)
    return JSONResponse(
        status_code=429,
        content={"error": True, "message": message}
    )

@app.exception_handler(APIStatusError)
async def api_status_error_handler(request: Request, exc: APIStatusError):
    language = getattr(request.state, "language", "en")
    message = get_translated_message("APIStatusError", language)
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": message}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    language = getattr(request.state, "language", "en")
    message = get_translated_message("ValueError", language)
    return JSONResponse(
        status_code=400,
        content={"error": True, "message": message}
    )

app.include_router(summarize_router, prefix="/api/v1", tags=["Summarization"])
