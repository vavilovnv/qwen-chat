import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_BASE_URL: str = os.getenv("API_BASE_URL", "")
    API_KEY: str = os.getenv("API_KEY", "")
    LLM_NAME: str = os.getenv("LLM_NAME", "")

    CHAT_HISTORY_LENGTH: int = int(os.getenv("CHAT_HISTORY_LENGTH", 10))

    URL_FOR_RAG_CONTENT: str = os.getenv("URL_FOR_RAG_CONTENT", "")

    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-small"  # TODO: check other models
    EMBEDDING_DB_FOLDER: str = "./chroma_db"
    EMBEDDING_PAGE_CHUNK_SIZE: int = 600
    EMBEDDING_PAGE_CHUNK_OVERLAP: int = 200

    USER_AGENT: str = os.getenv("USER_AGENT", "qwen-chat/0.0.1")
    os.environ["USER_AGENT"] = os.getenv("USER_AGENT", "qwen-chat/0.0.1")


app_settings = Settings()
