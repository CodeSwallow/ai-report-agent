from services.word_limit.free_user_word_limit_checker import FreeUserWordLimitChecker
from services.word_limit.pro_user_word_limit_checker import ProUserWordLimitChecker
from services.word_limit.word_limit_checker import WordLimitChecker
from config import FREE_USER_MAX_WORD_LIMIT


class WordLimitCheckerFactory:
    @staticmethod
    def get_checker(user_type: str) -> WordLimitChecker:
        """
        Returns the appropriate WordLimitChecker instance based on the user type.

        Parameters:
        - user_type (str): "free" or "pro".

        Returns:
        - WordLimitChecker: The appropriate checker instance.
        """
        user_type = user_type.lower()

        if user_type == "free":
            return FreeUserWordLimitChecker(max_words=FREE_USER_MAX_WORD_LIMIT)
        elif user_type == "pro":
            return ProUserWordLimitChecker()
        else:
            raise ValueError(f"Unsupported user type: {user_type}")
