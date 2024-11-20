from prompts.prompt_builder import build_prompt, TONE_DESCRIPTIONS, TEMPLATE_DESCRIPTIONS


def test_build_prompt_with_invalid_inputs():
    invalid_tone = "NonexistentTone"
    invalid_template = "NonexistentTemplate"
    result = build_prompt(invalid_tone, invalid_template)
    
    assert "Tone: NonexistentTone (Use a neutral tone.)" in result
    assert "Template: NonexistentTemplate (Provide a general summary.)" in result
    assert "Maintain clarity and coherence at all times." in result
    assert "Stay within the provided tone and template." in result
    assert "Use markdown syntax for headers, lists, and code blocks where applicable." in result


def test_build_prompt_with_additional_info():
    tone = "Professional"
    template = "Brief Summary"
    additional_info = "Focus on financial aspects"
    result = build_prompt(tone, template, additional_info)

    assert f"Tone: {tone}" in result
    assert f"Template: {template}" in result
    assert "Additional Information:\nFocus on financial aspects" in result
    assert "Maintain clarity and coherence at all times." in result
    assert "Stay within the provided tone and template." in result
    assert "Use markdown syntax for headers, lists, and code blocks where applicable." in result
