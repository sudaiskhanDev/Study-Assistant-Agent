
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import CHROMA_DIR
from app.services.embedding_service import create_embeddings


# Collection name for the currently uploaded PDF
COLLECTION_NAME = "study_assistant"


def create_vector_store(
    chunks: list[Document],
) -> Chroma:
    """
    Create a persistent Chroma vector store and save PDF chunks.

    Each chunk should contain its page_number in metadata.
    """

    if not chunks:
        raise ValueError("No chunks provided to store in Chroma.")

    embedding_model = create_embeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
    )

    return vector_store


def get_vector_store() -> Chroma:
    """
    Load the existing persistent Chroma vector store.
    """

    embedding_model = create_embeddings()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_DIR),
    )

    return vector_store


def delete_vector_store() -> None:
    """
    Delete the current Chroma collection before indexing a new PDF.
    """

    embedding_model = create_embeddings()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_DIR),
    )

    vector_store.delete_collection()


def search_similar_chunks(
    question: str,
    vector_store: Chroma,
    k: int = 3,
) -> list[Document]:
    """
    Retrieve the top-k chunks relevant to a question.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if k < 1:
        raise ValueError("k must be at least 1.")

    return vector_store.similarity_search(
        query=question,
        k=k,
    )
