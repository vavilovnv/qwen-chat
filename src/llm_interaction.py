"""Module for interacting with the LLM."""

from typing import Callable

from openai.types.chat import ChatCompletionMessageParam

from src.llm_client import llm


def _chat(*, ask_method: Callable) -> None:
    message_history: list[ChatCompletionMessageParam] = []

    print("Привет!\nВведите ваш вопрос или 'q, quit, exit' для выхода.")

    try:
        while True:
            user_input = input("> ")  # TODO: convert to utf-8 input
            if user_input.lower() in ["exit", "quit", "q"]:
                break

            print("\nГенерация ответа, пожалуйста, подождите...")
            answer, message_history = ask_method(
                question=user_input, message_history=message_history
            )
            print(f"\n{answer}\n")

    except KeyboardInterrupt:
        print("\nПока!")

    finally:
        llm.close_client()


def simple_chat() -> None:
    llm.get_client()

    _chat(ask_method=llm.ask)


def chat_with_rag() -> None:
    llm.get_client()

    _chat(ask_method=llm.ask_with_rag)
