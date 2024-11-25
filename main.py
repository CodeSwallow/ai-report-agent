from fastapi import FastAPI
from routers.summarize_router import router as summarize_router

app = FastAPI()

# Include the summarize router
app.include_router(summarize_router, prefix="/api/v1", tags=["Summarization"])
