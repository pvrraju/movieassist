import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    PINECONE_INDEX_NAME: str = "movieassist"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    RAG_MODEL: str = "o4-mini" # or your specific o4-mini model name
    OPENAI_API_BASE: str = "https://api.openai.com/v1" # IMPORTANT: Replace with your actual model provider's base URL

    class Config:
        case_sensitive = True

settings = Settings()
