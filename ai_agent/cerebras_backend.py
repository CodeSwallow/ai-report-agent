import weave
from cerebras.cloud.sdk import Cerebras
from cerebras.cloud.sdk import APIConnectionError as CerebrasAPIConnectionError, RateLimitError as CerebrasRateLimitError, APIStatusError as CerebrasAPIStatusError
from exceptions.backend_exceptions import APIConnectionError, APIRateLimitError, APIStatusError
from typing import Generator, List, Dict

client = Cerebras()

class CerebrasBackend(weave.Model):

    @weave.op()
    def predict(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Generator[str, None, None]:
        try:
            stream = client.chat.completions.create(
                messages=messages,
                model="llama3.1-8b",
                stream=True,
                **kwargs
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except CerebrasAPIConnectionError:
            raise APIConnectionError("The Cerebras server could not be reached.")
        except CerebrasRateLimitError:
            raise APIRateLimitError("Rate limit exceeded for Cerebras API.")
        except CerebrasAPIStatusError as e:
            raise APIStatusError(f"Cerebras API Error: {e.message}")