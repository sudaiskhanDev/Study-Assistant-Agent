
from fastapi import APIRouter, HTTPException, Query

from app.services.quiz_service import generate_quiz


router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.post("/")
def create_quiz(
    num_questions: int = Query(default=5, ge=1, le=20)
):
    try:
        return generate_quiz(num_questions=num_questions)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        print(f"Quiz endpoint error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate the quiz.",
        ) from error
