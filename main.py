import argparse

from settings import app_settings
from src.llm_interaction import simple_chat, chat_with_rag
from src.rag import input_url


def main():
    parser = argparse.ArgumentParser(
        description=f"Chat with LLM {app_settings.LLM_NAME}"
    )
    parser.add_argument(
        "-r",
        "--rag",
        action="store_true",
        help="Use web-based RAG to generate responses",
    )
    parser.add_argument(
        "-u", "--url", action="store_true", help="URL of the webpage to parse for RAG"
    )

    args = parser.parse_args()

    match (args.rag, args.url):
        case (True, _):
            chat_with_rag()
        case (_, True):
            input_url()
        case _:
            simple_chat()


if __name__ == "__main__":
    main()
