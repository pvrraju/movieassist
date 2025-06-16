from functools import lru_cache

from openai import OpenAI
from app.config import settings


@lru_cache(maxsize=1)
def get_embedding_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def get_embedding(text: str, model: str = settings.OPENAI_EMBEDDING_MODEL_NAME) -> list[float]:
    """Get embedding for a text."""
    client = get_embedding_client()
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding
