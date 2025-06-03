"""Module for the project strings."""

# roles
SYSTEM_ROLE = "system"
USER_ROLE = "user"

# default content strings
DEFAULT_CONTENT = "You are an AI assistant who only responds in Russian."
RAG_QUESTION_PROMPT = (
    "Use the following pieces of retrieved context to answer the questions."
    "If you don't know the answer, simply respond with “Я не знаю ответ.” "
    "Question: {question} "
    "Context: {context}"
)

# templates
CHROMA_DB_COLLECTION_NAME = "collection_{url_hash}"

# error messages
LLM_CLIENT_NOT_INITIALIZED_ERROR = "OpenAI client is not initialized."
RAG_URL_EMPTY_ERROR = "URL for RAG content is not set."
