class RateLimitError(Exception):
    """Exception raised when the user exceeds the rate limit."""
    def __init__(self, message="Rate limit exceeded. Please try again later."):
        self.message = message
        super().__init__(self.message)
