
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the uploaded PDF",
    )
    k: int = Field(
        default=4,
        ge=1,
        le=10,
        description="Number of relevant chunks to retrieve",
    )


class SourceItem(BaseModel):
    page_number: int | None = None
    text: str


class ChatResponse(BaseModel):
    answer: str
    source_pages: list[int]
    sources: list[SourceItem]
