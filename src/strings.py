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
DOCUMENT_SYMBOLS_AMOUNT = "{avg_len} символов"
WEB_APP_TITLE = "🤖 Чат с LLM моделью {llm_name}"
MODEL_DESCRIPTION = "Используемая модель: **{llm_name}**"
URL_ADDED_TO_VDB = "URL успешно добавлен в базу знаний: {url}"
PAGES_WERE_LOADED = "Загружено {pages_amount} страниц в Chroma DB"
BASE_URL_FOR_VDB = "**Базовый URL для загрузки в RAG:** {url}"
SIMBOLS_IN_DOCUMENT = "Документ #{num} ({content_len}) символов)"
VDB_LOADED_CONTENT = "Загружено {pages_amount} документов из базы"
VDB_COLLECTION_NAME = "collection_{url_hash}"

# error messages
LLM_CLIENT_NOT_INITIALIZED_ERROR = "OpenAI client is not initialized."
RAG_URL_EMPTY_ERROR = "URL for RAG content is not set."
ADD_URL_ERROR = "Ошибка при добавлении URL: {message}"
UNKNOWN_VDB_ERROR = "Неизвестная ошибка при загрузке данных из базы"
VDB_LOAD_DATA_ERROR = "Не удалось загрузить данные из базы Chroma"
VDB_GETTING_DATA_ERROR = "Ошибка при получении данных: {error}"

# strings
ABOUT_PROJECT = "📄 О проекте"
ABOUT_PROJECT_DESCRIPTION = "Чат с оффлайн LLM моделью, поддерживающей OpenAPI"
ADD_TITLE = "Добавить"
ADD_URL_RESOURCE = "Добавить URL"
ADD_URL_RESOURCE_DESCRIPTION = (
    "❕ Добавление веб-ресурса по указанному URL в базу знаний"
)
ADD_URL_RESOURCE_TITLE = "Добавление веб-ресурса в базу знаний"
API_KEY_WAS_SET = "Ключ API указан, можно работать с моделью"
API_KEY_WAD_PROVIDED = "Ключ API уже указан"
AVERAGE_DOCUMENT_LENGTH = "Средняя длина документа"
CHAT_WITH_RAG = "Чат с LLM в RAG режиме"
CHAT_WITH_RAG_DESCRIPTION = "❕ Модель отвечает используя базу загруженных веб-ресурсов"
CHOOSE_CHAT_MODE = "Выберите режим работы:"
CONTENT = "**Содержимое:**"
DOCUMENTS_AMOUNT = "Количество документов"
GENERATE_ANSWER = "Формирую ответ..."
INPUT_URL_TITLE = "Введите URL веб-страницы:"
INPUT_YOUR_MESSAGE = "Введите ваше сообщение..."
INPUT_API_KEY = "Введите ваш ключ к API LLM"
FOUND_SOME_DOCUMENTS = "Найдено {docs_amount} документов, содержащих '{search_term}'"
HISTORY_LENGTH = "Глубина истории сообщений:"
LOAD_PAGE_TITLE = "Загрузка и обработка страницы..."
METADATA = "**Метаданные:**"
PLEASE_INPUT_API_KEY = "Пожалуйста, введите ваш ключ к API LLM!"
SEARCH_IN_CONTENT = "Поиск по содержимому:"
SETTINGS = "⚙️ Настройки"
SIMPLE_CHAT = "Чат с LLM"
SIMPLE_CHAT_DESCRIPTION = "❕ Модель отвечает используя свою знаний"
STATISTIC = "Статистика"
VDB = "Контент для RAG"
VDB_CONTENT = "Содержимое базы"
VDB_DESCRIPTION = "Данные в векторной базе Chroma"
VDB_IS_EMPTY = "База знаний не содержит данных. Сначала добавьте URL в базу."
VDB_LOADING_CONTENT = "Загрузка данных из базы Chroma..."
VDB_TITLE = "📊 Базы знаний RAG в Chroma DB"
URL_SUCCESSFULLY_ADDED = "✅ URL успешно добавлен"
