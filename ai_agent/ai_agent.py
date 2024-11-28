import json
import weave
from typing import Generator, Optional
from prompts.prompt_builder import build_prompt
from config import BACKEND_PROVIDER
from ai_agent.cerebras_backend import CerebrasBackend
from ai_agent.openai_backend import OpenAIBackend


def get_backend() -> weave.Model:
    if BACKEND_PROVIDER == "cerebras":
        return CerebrasBackend()
    elif BACKEND_PROVIDER == "openai":
        return OpenAIBackend()
    else:
        raise ValueError(f"Unsupported backend provider: {BACKEND_PROVIDER}")


def call_agent(
    content: str,
    tone: str,
    template: str,
    additional_info: Optional[str] = None,
    language: str = "en"
) -> Generator[str, None, None]:
    prompt = build_prompt(tone, template, additional_info, language)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": content}
    ]

    backend = get_backend()

    for text_content in backend.predict(messages):
        json_chunk = json.dumps({
            "role": "assistant",
            "content": text_content
        })
        yield json_chunk + "\n"
