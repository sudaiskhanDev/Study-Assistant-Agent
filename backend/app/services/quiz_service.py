
from typing import Literal

from pydantic import BaseModel, Field

from app.config import UPLOAD_DIR
from app.services.pdf_service import process_pdf
from app.services.rag_service import create_llm


CURRENT_PDF_PATH = UPLOAD_DIR / "current.pdf"


class QuizOption(BaseModel):
    option_id: Literal["A", "B", "C", "D"]
    text: str


class QuizQuestion(BaseModel):
    question: str
    options: list[QuizOption] = Field(min_length=4, max_length=4)
    correct_answer: Literal["A", "B", "C", "D"]
    explanation: str
    page_number: int = Field(ge=1)


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


def generate_quiz(num_questions: int = 5) -> dict:
    """Generate multiple-choice questions from the uploaded PDF."""

    if not 1 <= num_questions <= 20:
        raise ValueError("Number of questions must be between 1 and 20.")

    if not CURRENT_PDF_PATH.exists():
        raise ValueError("Please upload a PDF before generating a quiz.")

    pages_data = process_pdf(CURRENT_PDF_PATH)

    # Keep each page number attached to its text.
    page_context = "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages_data
    )

    llm = create_llm()
    structured_llm = llm.with_structured_output(QuizResponse)

    prompt = f"""
You are an AI Study Assistant creating a quiz from study notes.

Generate exactly {num_questions} multiple-choice questions
using only the provided PDF text.

Rules:
1. Each question must have exactly four options: A, B, C, and D.
2. There must be exactly one correct answer per question.
3. correct_answer must be the option ID: A, B, C, or D.
4. Explain why the correct answer is right using the source text.
5. page_number must be an actual page number shown in the context
   that supports the question and its answer.
6. Do not invent facts or unsupported page numbers.
7. Cover different concepts where possible.
8. If the PDF does not contain enough information for
   {num_questions} good questions, generate only the questions
   supported by the text.
9. If the PDF only contains questions or headings without answers,
   do not invent missing information.

PDF CONTEXT:
{page_context}
"""

    result = structured_llm.invoke(prompt)

    # Check that every question's options are valid and unique.
    for question in result.questions:
        option_ids = [option.option_id for option in question.options]

        if set(option_ids) != {"A", "B", "C", "D"}:
            raise ValueError(
                "The generated quiz contains invalid option IDs."
            )

        if question.page_number not in {
            page["page_number"] for page in pages_data
        }:
            raise ValueError(
                "The generated quiz contains an invalid page number."
            )

    return {
        "questions": [
            question.model_dump()
            for question in result.questions
        ],
        "total_questions": len(result.questions),
    }
