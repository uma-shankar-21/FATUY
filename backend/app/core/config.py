import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # ==========================================
    # POSTGRES
    # ==========================================

    POSTGRES_DB: str | None = os.getenv(
        "POSTGRES_DB"
    )

    POSTGRES_USER: str | None = os.getenv(
        "POSTGRES_USER"
    )

    POSTGRES_PASSWORD: str | None = os.getenv(
        "POSTGRES_PASSWORD"
    )

    POSTGRES_HOST: str | None = os.getenv(
        "POSTGRES_HOST"
    )

    POSTGRES_PORT: int = int(
        os.getenv("POSTGRES_PORT", "5432")
    )


    # ==========================================
    # REDIS
    # ==========================================

    REDIS_HOST: str = os.getenv(
        "REDIS_HOST",
        "redis",
    )

    REDIS_PORT: int = int(
        os.getenv("REDIS_PORT", "6379")
    )

    REDIS_DB: int = int(
        os.getenv("REDIS_DB", "0")
    )


    @property
    def REDIS_URL(self) -> str:

        return (
            f"redis://"
            f"{self.REDIS_HOST}:"
            f"{self.REDIS_PORT}/"
            f"{self.REDIS_DB}"
        )


    # ==========================================
    # JWT
    # ==========================================

    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "change_this_to_a_long_random_secret",
    )

    JWT_ALGORITHM: str = os.getenv(
        "JWT_ALGORITHM",
        "HS256",
    )

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "60",
        )
    )


    # ==========================================
    # MCP
    # ==========================================

    MCP_API_BASE_URL: str | None = os.getenv(
        "MCP_API_BASE_URL"
    )


    # ==========================================
    # GROQ
    # ==========================================

    GROQ_API_KEY: str | None = os.getenv(
        "GROQ_API_KEY"
    )

    GROQ_MODEL: str | None = os.getenv(
        "GROQ_MODEL"
    )


    # ==========================================
    # OLLAMA
    # ==========================================

    OLLAMA_BASE_URL: str | None = os.getenv(
        "OLLAMA_BASE_URL"
    )

    OLLAMA_MODEL: str | None = os.getenv(
        "OLLAMA_MODEL"
    )


    # ==========================================
    # VLLM
    # ==========================================

    VLLM_BASE_URL: str | None = os.getenv(
        "VLLM_BASE_URL"
    )

    VLLM_MODEL: str | None = os.getenv(
        "VLLM_MODEL"
    )


    # ==========================================
    # KAFKA
    # ==========================================

    KAFKA_BOOTSTRAP_SERVERS: str | None = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS"
    )


    # ==========================================
    # AI
    # ==========================================

    AI_PROVIDER_PRIORITY: str = (
        "ollama,vllm"
    )

    AI_MAX_TOOL_ROUNDS: int = 3


    # ==========================================
    # SESSION
    # ==========================================

    SESSION_TTL_SECONDS: int = int(
        os.getenv(
            "SESSION_TTL_SECONDS"
        )
    )


    class Config:

        env_file = ".env"


settings = Settings()