class SummarizationError(Exception):
    """Base exception for summarization errors."""
    pass

class WordLimitExceededError(SummarizationError):
    """Exception raised when the document exceeds the word limit."""
    def __init__(self, message="Document exceeds the word limit for free users. Upgrade to pro."):
        self.message = message
        super().__init__(self.message)
