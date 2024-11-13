from cerebras.cloud.sdk import Cerebras
from prompts.document_summarizer_prompt import DOCUMENT_SUMMARIZER_PROMPT
from fastapi import HTTPException
from typing import Generator

client = Cerebras()


def call_agent(message: str, agent_name: str = None) -> Generator[str, None, None]:
    messages = [
        {"role": "system", "content": DOCUMENT_SUMMARIZER_PROMPT},
        {"role": "user", "content": message}
    ]
    try:
        stream = client.chat.completions.create(
            messages=messages,
            model="llama3.1-8b",
            stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            yield content if content is not None else ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
