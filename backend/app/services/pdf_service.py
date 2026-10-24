
import pymupdf

from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_pdf(pdf_path: str | Path) -> list[dict]:
    """
    Extract text from each PDF page.

    Returns:
        A list containing each page's number and extracted text.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    pages_data = [] 

    with pymupdf.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf):
            text = page.get_text("text").strip()

            # Skip pages without extractable text
            if not text:
                continue

            pages_data.append(
                {
                    "page_number": page_index + 1,
                    "text": text,
                }
            )

    if not pages_data:
        raise ValueError(
            "No extractable text found in this PDF. "
            "It may be scanned or image-based."
        )

    return pages_data


def create_chunks(
    pages_data: list[dict],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[Document]:
    """
    Split extracted page text into smaller chunks.

    Each chunk keeps its original PDF page number in metadata.
    """

    if not pages_data:
        raise ValueError("pages_data is empty. Process a PDF first.")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be non-negative and smaller than chunk_size."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = []

    for page_data in pages_data:
        page_number = page_data["page_number"]
        page_text = page_data["text"].strip()

        if not page_text:
            continue

        page_documents = splitter.create_documents(
            texts=[page_text],
            metadatas=[{"page_number": page_number}],
        )

        chunks.extend(page_documents)

    if not chunks:
        raise ValueError("No chunks could be created from the PDF.")

    return chunks
