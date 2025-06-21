"""Module for interacting with the LLM."""

from typing import Callable

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionUserMessageParam,
)

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


def _ask(*, question: str, history: list[dict], ask_method: Callable) -> str:
    message_history: list[ChatCompletionMessageParam] = []
    history = history[:-1]
    if len(history):
        for message in history:
            if message["role"] == "user":
                message_history.append(
                    ChatCompletionUserMessageParam(
                        role="user",
                        content=message["content"],
                    )
                )
            elif message["role"] == "assistant":
                message_history.append(
                    ChatCompletionAssistantMessageParam(
                        role="assistant",
                        content=message["content"],
                    )
                )

    answer, _ = ask_method(question=question, message_history=message_history)

    return answer


def simple_chat() -> None:
    llm.get_client()

    _chat(ask_method=llm.ask)


def chat_with_rag() -> None:
    llm.get_client()

    _chat(ask_method=llm.ask_with_rag)


def ask_llm(question: str, history: list[dict]) -> str:
    if not question:
        return ""

    llm.get_client()

    return _ask(question=question, history=history, ask_method=llm.ask)


def ask_llm_rag(question: str, history: list[dict]) -> str:
    if not question:
        return ""

    llm.get_client()

    return _ask(question=question, history=history, ask_method=llm.ask_with_rag)
