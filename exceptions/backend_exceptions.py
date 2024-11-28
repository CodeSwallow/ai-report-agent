class BackendError(Exception):
    """Base exception for AI backend errors."""
    pass

class APIConnectionError(BackendError):
    """Exception raised when an API connection fails."""
    def __init__(self, message="The backend server could not be reached."):
        self.message = message
        super().__init__(self.message)

class APIRateLimitError(BackendError):
    """Exception raised when API rate limit is exceeded."""
    def __init__(self, message="Rate limit exceeded for backend API."):
        self.message = message
        super().__init__(self.message)

class APIStatusError(BackendError):
    """Exception raised for general backend API status errors."""
    def __init__(self, message="Backend API returned an error status."):
        self.message = message
        super().__init__(self.message)
