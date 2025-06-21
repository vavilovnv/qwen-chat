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
WEB_APP_TITLE = "Чат с LLM моделью {llm_name}"
MODEL_DESCRIPTION = "Используемая модель: **{llm_name}**"
URL_ADDED_TO_VDB = "URL успешно добавлен в базу знаний: {url}"
PAGES_WERE_LOADED = "Загружено {pages_amount} страниц в Chroma DB"

# error messages
LLM_CLIENT_NOT_INITIALIZED_ERROR = "OpenAI client is not initialized."
RAG_URL_EMPTY_ERROR = "URL for RAG content is not set."
ADD_URL_ERROR = "Ошибка при добавлении URL: {message}"

# strings
ABOUT_PROJECT = "### О проекте"
ABOUT_PROJECT_DESCRIPTION = "Простой чат с оффлайн LLM моделью, поддерживающей OpenAPI"
ADD_TITLE = "Добавить"
ADD_URL_RESOURCE_DESCRIPTION = "Добавление веб-ресурса в базу знаний"
INPUT_URL_TITLE = "Введите URL веб-страницы:"
INPUT_YOUR_MESSAGE = "Введите ваше сообщение..."
LOAD_PAGE_TITLE = "Загрузка и обработка страницы..."
SETTINGS = "Настройки"
CHOOSE_CHAT_MODE = "Выберите режим чата:"
SIMPLE_CHAT = "Обычный чат"
CHAT_WITH_RAG = "Чат в RAG режиме"
CHAT_WITH_RAG_DESCRIPTION = (
    "В этом режиме модель отвечает на основе загруженных веб-ресурсов"
)
ADD_URL_RESOURCE = "Добавить URL в базу RAG"
URL_SUCCESSFULLY_ADDED = "URL успешно добавлен"
GENERATE_ANSWER = "Формирую ответ..."
