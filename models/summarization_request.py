from pydantic import BaseModel, Field
from typing import Optional


class SummarizationRequest(BaseModel):
    tone: str = Field(..., description="The tone of the summary, e.g., Professional, Casual.")
    template: str = Field(..., description="The template to use for summarization.")
    user_type: str = Field(..., description="The type of user: Free or Pro.")
    ip_address: str = Field(..., description="The user's IP address for validation.")
    additional_info: Optional[str] = Field(None, description="Optional additional information.")
    language: Optional[str] = Field("en", description="The language of the summary, default is English.")
