from pydantic import BaseModel, Field


class QuizGenerateRequest(BaseModel):
    num_questions: int = Field(default=5, ge=1, le=20)


class QuizQuestion(BaseModel):
    question: str
    options: dict[str, str]
    correct_answer: str
    explanation: str
    source_pages: list[int]


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


class QuizEvaluateRequest(BaseModel):
    quiz_data: QuizResponse
    user_answers: dict[int, str]


class QuizResultItem(BaseModel):
    question_number: int
    question: str
    user_answer: str | None
    correct_answer: str
    is_correct: bool
    explanation: str
    source_pages: list[int]


class QuizEvaluationResponse(BaseModel):
    score: int
    total_questions: int
    percentage: float
    results: list[QuizResultItem]