from functools import lru_cache
from pinecone import Pinecone

from app.config import settings
from app.core.embeddings import get_embedding


@lru_cache(maxsize=1)
def get_pinecone_client() -> Pinecone:
    """Get a Pinecone client."""
    return Pinecone(api_key=settings.PINECONE_API_KEY)


def get_index():
    """Get the Pinecone index."""
    pc = get_pinecone_client()
    index = pc.Index(host=settings.PINECONE_HOST)
    return index


def query_vector_store(query: str, top_k: int = 5) -> list[dict]:
    """Query the vector store with a text query."""
    index = get_index()
    query_embedding = get_embedding(query)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )
    return results["matches"]
