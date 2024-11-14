from ai_agent.base_llm_backend import BaseLLMBackend
from cerebras.cloud.sdk import Cerebras
from cerebras.cloud.sdk import APIConnectionError, RateLimitError, APIStatusError
from typing import Generator, List, Dict


class CerebrasBackend(BaseLLMBackend):
    def __init__(self):
        self.client = Cerebras()

    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Generator[str, None, None]:
        try:
            stream = self.client.chat.completions.create(
                messages=messages,
                model="llama3.1-8b",
                stream=True,
                **kwargs
            )
            for chunk in stream:
                text_content = chunk.choices[0].delta.content
                if text_content is not None:
                    yield text_content
        except APIConnectionError:
            raise ConnectionError("The Cerebras server could not be reached.")
        except RateLimitError:
            raise ValueError("Rate limit exceeded for Cerebras API.")
        except APIStatusError as e:
            raise ValueError(f"Cerebras API Error: {e.message}")
