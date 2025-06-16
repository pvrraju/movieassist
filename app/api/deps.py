from app.core.llm import get_completion
from app.core.vector_store import query_vector_store


def get_retriever():
    """Dependency to get the vector store retriever."""
    return query_vector_store


def get_llm():
    """Dependency to get the language model."""
    return get_completion
