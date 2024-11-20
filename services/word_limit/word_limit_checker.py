from abc import ABC, abstractmethod


class WordLimitChecker(ABC):
    @abstractmethod
    def check_word_limit(self, text: str) -> bool:
        """
        Check if the document complies with the word limit.

        Parameters:
        - text (str): The content of the document.

        Returns:
        - bool: True if the document meets the word limit, False otherwise.
        """
        pass
