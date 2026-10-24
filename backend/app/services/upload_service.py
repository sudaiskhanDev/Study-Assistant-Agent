
from pathlib import Path

from fastapi import UploadFile

from app.config import UPLOAD_DIR
from app.services.pdf_service import process_pdf, create_chunks
from app.services.vector_service import (
    create_vector_store,
    delete_vector_store,
)


CURRENT_PDF_PATH = UPLOAD_DIR / "current.pdf"


def save_uploaded_pdf(file: UploadFile) -> dict:
    """
    Save a new PDF and index its content in Chroma.
    Replaces the previously uploaded PDF.
    """

    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise ValueError("Please upload a valid PDF file.")

    temporary_path = UPLOAD_DIR / "uploading.tmp.pdf"

    try:
        # Save upload in temporary storage first
        with temporary_path.open("wb") as destination:
            while True:
                data = file.file.read(1024 * 1024)

                if not data:
                    break

                destination.write(data)

        if temporary_path.stat().st_size == 0:
            raise ValueError("The uploaded PDF is empty.")

        # Validate and extract text before replacing the current PDF
        pages_data = process_pdf(temporary_path)
        chunks = create_chunks(pages_data)

        # Replace the old vector collection
        delete_vector_store()

        # Replace the stored PDF
        temporary_path.replace(CURRENT_PDF_PATH)

        # Index the new document
        create_vector_store(chunks)

        return {
            "message": "PDF uploaded and indexed successfully.",
            "filename": file.filename,
            "pages_processed": len(pages_data),
            "chunks_created": len(chunks),
        }

    except Exception:
        if temporary_path.exists():
            temporary_path.unlink()

        raise

    finally:
        file.file.close()
