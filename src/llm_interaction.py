"""Module for interacting with the LLM."""

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from settings import app_settings
from src import strings
from src.open_api import client

SYSTEM_PROMPT = ChatCompletionSystemMessageParam(
    role="system",
    content=strings.DEFAULT_CONTENT,
)


def ask(
    *, question: str, message_history: list[ChatCompletionMessageParam] | None = None
) -> tuple[str, list[ChatCompletionMessageParam]]:
    """Asks the model a question based on the message history."""
    if message_history is None:
        message_history = []

    messages: list[ChatCompletionMessageParam] = [SYSTEM_PROMPT]
    messages.extend(message_history)
    messages.append(
        ChatCompletionUserMessageParam(
            role="user",
            content=question,
        )
    )

    response = client.chat.completions.create(
        model=app_settings.LLM_NAME,
        messages=messages,
    )

    if not response.choices:
        return "", message_history

    message = response.choices[0].message
    message_content = message.content or ""

    message_history.append(
        ChatCompletionUserMessageParam(
            role="user",
            content=question,
        )
    )
    message_history.append(
        ChatCompletionAssistantMessageParam(
            role="assistant",
            content=message_content,
        )
    )

    return message_content, message_history
