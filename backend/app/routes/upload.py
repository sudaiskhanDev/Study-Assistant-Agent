
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.upload_service import save_uploaded_pdf


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("/")
def upload_pdf(file: UploadFile = File(...)):
    """Upload and index a PDF for the study assistant."""

    try:
        return save_uploaded_pdf(file)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        print(f"PDF upload error: {error}")

        raise HTTPException(
            status_code=500,
            detail="PDF upload or processing failed.",
        ) from error
