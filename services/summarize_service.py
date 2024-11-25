from utils.file_extraction import validate_file_type, extract_text
from utils.ip_validation import validate_ip
from ai_agent.ai_agent import call_agent
from services.word_limit.word_limit_checker_factory import WordLimitCheckerFactory
from fastapi.responses import StreamingResponse


async def process_summarization(
    document,
    tone,
    template,
    user_type,
    ip_address,
    additional_info
):
    validate_ip(ip_address)

    file_type = validate_file_type(document.content_type)
    text_content = await extract_text(document, file_type)

    word_limit_checker = WordLimitCheckerFactory.get_checker(user_type)
    if not word_limit_checker.check_word_limit(text_content):
        raise ValueError("Document exceeds the word limit for free users. Upgrade to pro.")

    def stream_response():
        for json_chunk in call_agent(
            content=text_content,
            tone=tone,
            template=template,
            additional_info=additional_info
        ):
            yield json_chunk

    return StreamingResponse(
        stream_response(),
        media_type="application/x-ndjson"
    )
