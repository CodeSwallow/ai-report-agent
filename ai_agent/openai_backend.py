from ai_agent.base_llm_backend import BaseLLMBackend
import openai
from openai import OpenAI
from typing import Generator, List, Dict


class OpenAIBackend(BaseLLMBackend):
    def __init__(self):
        self.client = OpenAI()

    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Generator[str, None, None]:
        try:
            stream = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
                **kwargs
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except openai.APIConnectionError:
            raise ConnectionError("The OpenAI server could not be reached.")
        except openai.RateLimitError:
            raise ValueError("Rate limit exceeded for OpenAI API.")
        except openai.OpenAIError as e:
            raise ValueError(f"OpenAI API Error: {e}")
