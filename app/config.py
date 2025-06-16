from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "MovieAssist API"
    LOG_LEVEL: str = "INFO"

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str = "gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL_NAME: str = "text-embedding-3-small"
    OPENAI_EMBEDDING_DIMENSIONS: int = 1536

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str = "movieassist"
    PINECONE_HOST: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
