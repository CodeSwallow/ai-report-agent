from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.summarize_router import router as summarize_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,  # Allows cookies to be sent with requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the summarize router
app.include_router(summarize_router, prefix="/api/v1", tags=["Summarization"])
