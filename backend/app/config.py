from pydantic_settings import BaseSettings
from typing import List, Union, Optional
import json


class Settings(BaseSettings):
    # ----------------------------
    # Project
    # ----------------------------
    PROJECT_NAME: str = "AI Memory Platform"
    API_V1_STR: str = "/api"

    # ----------------------------
    # Database
    # ----------------------------
    DATABASE_URL: str = "postgresql+asyncpg://postgres:root@localhost:5432/mem0_db"

    # ----------------------------
    # ChromaDB
    # IMPORTANT:
    # If running from VS Code (NOT Docker),
    # use localhost instead of chromadb.
    # ----------------------------
    CHROMA_HOST: str = "127.0.0.1"
    CHROMA_PORT: int = 8000
    CHROMA_COLLECTION: str = "memories"

    # ----------------------------
    # JWT
    # ----------------------------
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ----------------------------
    # Embedding Model
    # ----------------------------
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # ----------------------------
    # Cloud LLM (Optional for 24/7 Cloud Deployment)
    # ----------------------------
    GROQ_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "ollama"  # "ollama", "groq", or "openai"

    # ----------------------------
    # CORS
    # ----------------------------
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ]

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            return json.loads(self.BACKEND_CORS_ORIGINS)
        return self.BACKEND_CORS_ORIGINS

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()