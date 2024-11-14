import json
from typing import Generator, Optional
from prompts.prompt_builder import build_prompt
from config import BACKEND_PROVIDER
from ai_agent.base_llm_backend import BaseLLMBackend
from ai_agent.cerebras_backend import CerebrasBackend
from ai_agent.openai_backend import OpenAIBackend


def get_backend() -> BaseLLMBackend:
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
    additional_info: Optional[str] = None
) -> Generator[str, None, None]:
    prompt = build_prompt(tone, template, additional_info)
    print(f"Generated Prompt:\n{prompt}")

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": content}
    ]

    backend = get_backend()

    try:
        for text_content in backend.generate_stream(messages):
            json_chunk = json.dumps({"content": text_content})
            yield json_chunk + "\n"
    except ConnectionError as e:
        error_response = json.dumps({
            "error": True,
            "code": 502,
            "message": str(e)
        })
        yield error_response + "\n"
    except ValueError as e:
        error_response = json.dumps({
            "error": True,
            "code": 400,
            "message": str(e)
        })
        yield error_response + "\n"
    except Exception as e:
        error_response = json.dumps({
            "error": True,
            "code": 500,
            "message": "An unexpected error occurred."
        })
        yield error_response + "\n"
