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

    MODEL_PROVIDER: str = "huggingface"  # or huggingface / local
    GEMINI_API_KEY: str = "gemini"
    ANTHROPIC_API_KEY: str = "anthropic"
    OPENAI_API_KEY: str = "openai"

settings = Settings()   