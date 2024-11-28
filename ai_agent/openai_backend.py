import weave
import openai
from openai import OpenAI
from exceptions.backend_exceptions import APIConnectionError, APIRateLimitError, APIStatusError
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
                if chunk.choices:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
        except openai.APIConnectionError:
            raise APIConnectionError("The OpenAI server could not be reached.")
        except openai.RateLimitError:
            raise APIRateLimitError("Rate limit exceeded for OpenAI API.")
        except openai.OpenAIError as e:
            raise APIStatusError(f"OpenAI API Error: {e}")