
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import EMBEDDING_MODEL_NAME


def create_embeddings() -> HuggingFaceEmbeddings:
    """
    Initialize and return the HuggingFace embedding model.

    The model converts text into numerical vectors that can
    later be stored and searched in Chroma.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    return embedding_model
