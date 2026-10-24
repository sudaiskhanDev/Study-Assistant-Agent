
from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import answer_question


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
def chat_with_pdf(request: ChatRequest):
    """
    Answer a question using the current PDF's context.
    """

    try:
        result = answer_question(
            question=request.question,
            k=request.k,
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        # Keep internal exception details out of the API response.
        print(f"Chat endpoint error: {error}")

        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the answer.",
        ) from error
