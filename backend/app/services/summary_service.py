
from langchain_core.documents import Document

from app.services.rag_service import create_llm
from app.services.pdf_service import process_pdf
from app.config import UPLOAD_DIR


CURRENT_PDF_PATH = UPLOAD_DIR / "current.pdf"


def generate_summary() -> dict:
    """Generate a summary of the currently uploaded PDF."""

    if not CURRENT_PDF_PATH.exists():
        raise ValueError("Please upload a PDF before generating a summary.")

    pages_data = process_pdf(CURRENT_PDF_PATH)

    if not pages_data:
        raise ValueError("No readable text found in the PDF.")

    llm = create_llm()

    # Keep page numbers attached to each section of source text.
    page_sections = [
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages_data
    ]

    # Process pages in batches to avoid sending too much text at once.
    batch_size = 3
    summaries = []

    for start in range(0, len(page_sections), batch_size):
        batch = "\n\n".join(page_sections[start:start + batch_size])

        prompt = f"""
You are an AI Study Assistant.

Summarize the following PDF text for a student.

Rules:
1. Use only the provided text.
2. Explain concepts in simple, clear language.
3. Preserve important facts, definitions, and key points.
4. Cite supporting page numbers using [Page N].
5. Do not invent information or page citations.
6. If the text only lists questions or headings without answers,
   summarize what is actually present. Do not invent missing answers.

PDF TEXT:
{batch}

Write a concise, structured summary with page citations.
"""

        response = llm.invoke(prompt)
        summaries.append(response.content)

    return {
        "summary": "\n\n".join(summaries),
        "pages_processed": len(pages_data),
    }
