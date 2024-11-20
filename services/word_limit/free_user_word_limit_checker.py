from services.word_limit.word_limit_checker import WordLimitChecker


class FreeUserWordLimitChecker(WordLimitChecker):
    def __init__(self, max_words: int):
        self.max_words = max_words

    def check_word_limit(self, text: str) -> bool:
        word_count = len(text.split())
        print(f"Word count: {word_count}")
        return word_count <= self.max_words
