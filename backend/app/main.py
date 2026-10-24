
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.upload import router as upload_router
from app.routes.summary import router as summary_router
from app.routes.quiz import router as quiz_router
from app.routes.flashcards import router as flashcards_router


app = FastAPI(
    title="AI Study Assistant API",
    description="Upload PDFs, ask questions, and generate summaries.",
    version="1.0.0",
)

# Allow requests from the local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(summary_router)
app.include_router(quiz_router)
app.include_router(flashcards_router)


@app.get("/")
def home():
    return {"message": "AI Study Assistant API is running."}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
