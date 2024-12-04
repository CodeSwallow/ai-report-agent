from utils.localization import MESSAGES

def get_translated_message(exception_name: str, language: str) -> str:
    return MESSAGES.get(exception_name, {}).get(language, MESSAGES[exception_name]["en"])
