import os


class Settings:
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "change_this_to_a_long_random_secret",
    )
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )
    MCP_API_BASE_URL = os.getenv("MCP_API_BASE_URL")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")

    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

    VLLM_BASE_URL = os.getenv("VLLM_BASE_URL")
    VLLM_MODEL = os.getenv("VLLM_MODEL")

    AI_PROVIDER_PRIORITY: str = "ollama,vllm"

    AI_MAX_TOOL_ROUNDS = 3
    SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS"))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
settings = Settings()