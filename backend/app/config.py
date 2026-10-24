
import os
from pathlib import Path

from dotenv import load_dotenv


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the root .env file
load_dotenv(BASE_DIR / ".env")


# API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM configuration
LLM_MODEL_NAME = "openai/gpt-oss-120b"

# Embedding configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Directory configuration
UPLOAD_DIR = BASE_DIR / "uploads"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Create required directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)


# Validate required configuration
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Please add it to the root .env file."
    )
