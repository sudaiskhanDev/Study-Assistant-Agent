
from fastapi import APIRouter, HTTPException

from app.services.summary_service import generate_summary


router = APIRouter(prefix="/summary", tags=["Summary"])


@router.post("/")
def create_summary():
    try:
        return generate_summary()

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        print(f"Summary endpoint error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate the PDF summary.",
        ) from error
