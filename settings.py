import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_BASE_URL: str = os.getenv("API_BASE_URL", "")
    API_KEY: str = os.getenv("API_KEY", "")
    LLM_NAME: str = os.getenv("LLM_NAME", "")


app_settings = Settings()
