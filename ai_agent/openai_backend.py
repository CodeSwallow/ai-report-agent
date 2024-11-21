import weave
import openai
from openai import OpenAI
from typing import Generator, List, Dict

client = OpenAI()


class OpenAIBackend(weave.Model):

    @weave.op()
    def predict(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Generator[str, None, None]:
        try:
            stream = client.chat.completions.create(
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
