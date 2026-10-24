
from typing import Literal

from pydantic import BaseModel, Field

from app.config import UPLOAD_DIR
from app.services.pdf_service import process_pdf
from app.services.rag_service import create_llm


CURRENT_PDF_PATH = UPLOAD_DIR / "current.pdf"


class Flashcard(BaseModel):
    front: str
    back: str
    page_number: int = Field(ge=1)


class FlashcardResponse(BaseModel):
    flashcards: list[Flashcard]


def generate_flashcards(num_cards: int = 10) -> dict:
    """Generate study flashcards from the currently uploaded PDF."""

    if not 1 <= num_cards <= 30:
        raise ValueError("Number of flashcards must be between 1 and 30.")

    if not CURRENT_PDF_PATH.exists():
        raise ValueError("Please upload a PDF before generating flashcards.")

    pages_data = process_pdf(CURRENT_PDF_PATH)

    page_context = "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages_data
    )

    llm = create_llm()
    structured_llm = llm.with_structured_output(FlashcardResponse)

    prompt = f"""
You are an AI Study Assistant creating revision flashcards.

Generate up to {num_cards} useful flashcards using only the PDF text.

Rules:
1. Each front should contain one clear question or term.
2. Each back should contain its correct answer or definition.
3. Keep cards concise and useful for revision.
4. page_number must be an actual PDF page number that supports the answer.
5. Do not invent facts, answers, or page numbers.
6. Cover different important concepts where possible.
7. If the PDF does not contain enough information, generate fewer cards.
8. If the PDF only lists questions without answers, do not invent answers.

PDF CONTEXT:
{page_context}
"""

    result = structured_llm.invoke(prompt)

    valid_pages = {
    page["page_number"] for page in pages_data
}

    valid_flashcards = [
        card
        for card in result.flashcards
        if card.page_number in valid_pages
    ]

    return {
        "flashcards": [
            card.model_dump()
            for card in valid_flashcards
        ],
        "total_flashcards": len(valid_flashcards),
    }
