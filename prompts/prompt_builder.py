from typing import Optional


def build_prompt(tone: str, template: str, additional_info: Optional[str] = None) -> str:
    prompt = f"""
    You are to summarize documents using the following guidelines:

    - Tone: {tone}
    - Template: {template}
    """

    if additional_info:
        prompt += f"\nAdditional Information:\n{additional_info}\n"

    prompt += """
    Use the following general guidelines:
    - Use a single blank line to separate sections.
    - Use proper markdown syntax for headers, lists, and code blocks.
    """

    return prompt
