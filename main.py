from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ai_agent import call_agent

app = FastAPI()


class SummarizeRequest(BaseModel):
    content: str
    agent_name: str = None  # Optional, in case you want to specify an agent


@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    return StreamingResponse(call_agent(request.content, request.agent_name), media_type="text/plain")
