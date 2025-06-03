"""LLM OpenAI client."""

from dataclasses import dataclass

from langchain_chroma import Chroma
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from settings import app_settings
from src import strings
from src.rag import EmbeddingStore

SYSTEM_PROMPT = ChatCompletionSystemMessageParam(
    role="system",
    content=strings.DEFAULT_CONTENT,
)


@dataclass
class LLMClient:
    _client: OpenAI | None = None
    _vector_store: Chroma | None = None

    def _ask_llm(
        self,
        *,
        question: str,
        message_history: list[ChatCompletionMessageParam] | None = None,
    ) -> tuple[str, list[ChatCompletionMessageParam]]:
        """Gets answer from LLM."""
        if not self._client:
            raise ValueError(strings.LLM_CLIENT_NOT_INITIALIZED_ERROR)

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

        response = self._client.chat.completions.create(
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

    def get_client(self) -> OpenAI:
        """Returns the OpenAI client."""
        if not self._client:
            self._client: OpenAI = OpenAI(
                base_url=app_settings.API_BASE_URL, api_key=app_settings.API_KEY
            )

        return self._client

    def close_client(self) -> None:
        """Closes the OpenAI client."""
        if self._client:
            self._client.close()

    def ask(
        self,
        *,
        question: str,
        message_history: list[ChatCompletionMessageParam] | None = None,
    ) -> tuple[str, list[ChatCompletionMessageParam]]:
        """Asks the model a question based on the message history."""
        return self._ask_llm(question=question, message_history=message_history)

    def ask_with_rag(
        self,
        *,
        question: str,
        message_history: list[ChatCompletionMessageParam] | None = None,
    ) -> tuple[str, list[ChatCompletionMessageParam]]:
        """Asks the model a question based on the RAG and message history."""
        if not self._vector_store:
            self._vector_store = EmbeddingStore().init_store()

        rag_data = self._vector_store.similarity_search(question, k=5)
        rag_content = "\n".join([doc.page_content for doc in rag_data])
        rag_question = strings.RAG_QUESTION_PROMPT.format(
            question=question, context=rag_content
        )

        return self._ask_llm(question=rag_question, message_history=message_history)


llm = LLMClient()
