"""OpenAI client."""

from openai import OpenAI

from settings import app_settings


def get_client() -> OpenAI:
    return OpenAI(base_url=app_settings.API_BASE_URL, api_key=app_settings.API_KEY)


def close_client() -> None:
    client.close()


client = get_client()
