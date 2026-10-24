from pydantic import BaseModel, Field


class FlashcardGenerateRequest(BaseModel):
    num_cards: int = Field(default=5, ge=1, le=20)


class Flashcard(BaseModel):
    question: str
    answer: str
    source_pages: list[int]


class FlashcardResponse(BaseModel):
    flashcards: list[Flashcard]