from abc import ABC, abstractmethod
from typing import Generator, List, Dict


class BaseLLMBackend(ABC):
    @abstractmethod
    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Generator[str, None, None]:
        pass
