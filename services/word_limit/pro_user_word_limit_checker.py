from services.word_limit.word_limit_checker import WordLimitChecker


class ProUserWordLimitChecker(WordLimitChecker):
    def check_word_limit(self, text: str) -> bool:
        # Pro users have no word limit
        return True
