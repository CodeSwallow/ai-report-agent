import weave
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from routers.summarize_router import router as summarize_router
from middleware.rate_limiter import limiter, custom_rate_limit_handler
from fastapi.responses import JSONResponse
from exceptions.backend_exceptions import APIConnectionError, APIRateLimitError, APIStatusError
from exceptions.summarization_exceptions import WordLimitExceededError

# Initialize Weave
weave.init('summarizer-agent')

# Initialize FastAPI
app = FastAPI()
app.state.limiter = limiter

# Add exception handler for rate limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add centralized exception handlers
@app.exception_handler(WordLimitExceededError)
async def word_limit_error_handler(request: Request, exc: WordLimitExceededError):
    return JSONResponse(
        status_code=402,
        content={"error": True, "message": exc.message}
    )

@app.exception_handler(APIConnectionError)
async def api_connection_error_handler(request: Request, exc: APIConnectionError):
    return JSONResponse(
        status_code=503,
        content={"error": True, "message": exc.message}
    )

@app.exception_handler(APIRateLimitError)
async def api_rate_limit_error_handler(request: Request, exc: APIRateLimitError):
    return JSONResponse(
        status_code=429,
        content={"error": True, "message": exc.message}
    )

@app.exception_handler(APIStatusError)
async def api_status_error_handler(request: Request, exc: APIStatusError):
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": exc.message}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": True, "message": str(exc)}
    )

app.include_router(summarize_router, prefix="/api/v1", tags=["Summarization"])
