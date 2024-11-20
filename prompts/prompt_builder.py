from typing import Optional

# Define tone descriptions for LLM guidance
TONE_DESCRIPTIONS = {
    "Professional": "Use formal language that is suitable for business or official communication.",
    "Casual": "Use friendly, conversational language that is informal and approachable.",
    "Academic": "Use technical and precise language appropriate for educational or scientific content.",
    "Persuasive": "Use influential language that aims to convince the reader of key points.",
    "Narrative": "Summarize with a storytelling approach, making the content engaging and sequential.",
    "Concise": "Use direct and to-the-point language, focusing only on essential information.",
    "Descriptive": "Include rich detail and imagery, highlighting visual or sensory elements.",
    "Inspirational": "Use motivational language, with a focus on uplifting themes and encouragement.",
    "Analytical": "Use logical, structured language that breaks down complex ideas or arguments."
}

TEMPLATE_DESCRIPTIONS = {
    "Brief Summary": "Provide a concise overview of the key points of the document.",
    "Detailed Summary": "Provide a detailed summary that covers important points with context and supporting details.",
    "Standard Report": "Format the response as a structured report with headers and sections to organize information.",
    "Executive Report": "Focus on high-level information and key takeaways, tailored for decision-makers.",
    "Technical Report": "Provide a detailed technical breakdown, including specific data and complex concepts.",
    "Key Findings": "Highlight the most important findings or results from the document.",
    "Pros and Cons": "Summarize the document by listing advantages and disadvantages.",
    "Cause and Effect Analysis": "Analyze and explain causal relationships within the document.",
    "Narrative Rewrite": "Rewrite the document in a storytelling format, making it engaging and sequential.",
    "Descriptive Overview": "Provide a description that includes rich sensory details and imagery.",
    "Q&A Format": "Transform the document into a question-and-answer format, summarizing key points as answers to potential questions.",
    "Bullet Points": "Condense information into a list of bullet points for a quick overview."
}


def build_prompt(tone: str, template: str, additional_info: Optional[str] = None) -> str:
    """
    Builds a prompt for document summarization based on specified tone, template, and additional information.

    This function constructs a structured prompt that guides an AI model in summarizing documents
    according to the given tone and template. It also incorporates any additional information provided.

    Parameters:
    tone (str): The desired tone for the summary. Should be a key from the TONE_DESCRIPTIONS dictionary.
    template (str): The desired template for the summary structure. Should be a key from the TEMPLATE_DESCRIPTIONS dictionary.
    additional_info (Optional[str]): Any additional information or instructions to be included in the prompt. Defaults to None.

    Returns:
    str: A formatted prompt string that includes guidelines for tone, template, and general summarization instructions.
    """
    tone_description = TONE_DESCRIPTIONS.get(tone, "Use a neutral tone.")
    template_description = TEMPLATE_DESCRIPTIONS.get(template, "Provide a general summary.")

    prompt = f"""
    You are to summarize documents using the following guidelines:

    - Tone: {tone} ({tone_description})
    - Template: {template} ({template_description})
    """

    if additional_info:
        prompt += f"\nAdditional Information:\n{additional_info}\n"

    prompt += """
    Follow these general guidelines carefully:
    - Maintain clarity and coherence at all times.
    - Stay within the provided tone and template.
    - If additional instructions conflict with these guidelines, prioritize these instructions.

    Formatting:
    - Use a single blank line to separate sections.
    - Use markdown syntax for headers, lists, and code blocks where applicable.
    """

    return prompt
