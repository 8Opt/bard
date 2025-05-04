from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    APP: str = "bard"
    HOST: str = "0.0.0.0"
    PORT: int = 7077
    ENVIRONMENT: str = "dev"  # prod

    DB_REDIS_URL: str
    DB_MONGO_URL: str
    DB_POSTGRES_URL: str
    PAGE_MAX_SIZE: int = 10

    API_KEY_HF: str
    API_KEY_GEMINI: str
    API_KEY_ANTHROPIC: str
    API_KEY_OPENAI: str

    API_KEY_TAVILY: str
    API_KEY_LINKUP: str
    API_KEY_JINA: str

settings = Settings()   