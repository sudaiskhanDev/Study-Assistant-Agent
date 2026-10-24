
from fastapi import APIRouter, HTTPException, Query

from app.services.flashcard_service import generate_flashcards


router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcards"],
)


@router.post("/")
def create_flashcards(
    num_cards: int = Query(default=10, ge=1, le=30),
):
    try:
        return generate_flashcards(num_cards=num_cards)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        print(f"Flashcard endpoint error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate flashcards.",
        ) from error
