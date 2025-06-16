from functools import lru_cache

from openai import OpenAI
from app.config import settings


@lru_cache(maxsize=1)
def get_llm_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def get_completion(prompt: str, model: str = settings.OPENAI_MODEL_NAME) -> str:
    """Get a completion from the LLM."""
    client = get_llm_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful movie assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content
