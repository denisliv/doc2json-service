from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "", "case_sensitive": False}

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://doc2json:secret@postgres:5432/doc2json"

    # Redis / Celery
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    # LLM
    LLM_API_URL: str = "http://host.docker.internal:11434/v1"
    LLM_API_KEY: str = "token-abc"
    LLM_MODEL_NAME: str = "gpt-oss:20b-new"
    LLM_TEMPERATURE: float = 0.0
    LLM_TOP_P: float = 0.8
    LLM_MAX_TOKENS: int = 4096
    LLM_REASONING_EFFORT: str = "low"
    LLM_TIMEOUT: int = 60

    # PaddleOCR-VL
    OCR_VL_BACKEND: str = "vllm-server"
    OCR_VL_SERVER_URL: str = "http://host.docker.internal:8118/v1"
    OCR_VL_MODEL_NAME: str = "PaddleOCR-VL-0.9B"
    OCR_LAYOUT_MODEL_NAME: str = "PP-DocLayoutV3"
    OCR_LAYOUT_MODEL_DIR: str = "/app/models/PP-DocLayoutV3"
    OCR_ORIENTATION_MODEL_NAME: str = "PP-LCNet_x1_0_doc_ori"
    OCR_ORIENTATION_MODEL_DIR: str = "/app/models/PP-LCNet_x1_0_doc_ori"
    OCR_UNWARPING_MODEL_NAME: str = "UVDoc"
    OCR_UNWARPING_MODEL_DIR: str = "/app/models/UVDoc"
    OCR_USE_ORIENTATION: bool = True
    OCR_USE_UNWARPING: bool = True
    OCR_USE_LAYOUT: bool = True
    OCR_USE_OCR_FOR_IMAGE: bool = True
    OCR_FORMAT_BLOCK_CONTENT: bool = True
    OCR_MERGE_LAYOUT_BLOCKS: bool = True
    OCR_LAYOUT_THRESHOLD: float = 0.3
    OCR_LAYOUT_NMS: bool = True
    OCR_LAYOUT_MERGE_MODE: str = "large"
    OCR_USE_QUEUES: bool = True
    OCR_TEMPERATURE: float = 0.1
    OCR_TOP_P: float = 0.8
    OCR_REPETITION_PENALTY: float = 1.0

    # Storage
    STORAGE_DIR: str = "/app/storage"
    PLUGINS_DIR: str = "/app/plugins"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]


settings = Settings()
