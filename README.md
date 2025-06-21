### Простой чат с оффлайн llm моделью, которая поддерживает OpenAPI

Оффлайн модель можно взять на [huggingface](https://huggingface.co/), их там тысячи. Собирать модель лучше в отдельной от проекта директории.

Стянуть llm с huggingface можно вручную, а можно при помощи huggingface-cli. Это удобнее, если модель большая и архив разбит на файлы. Обычно команда для загрузки есть на странице нужной модели:
```bash
huggingface-cli download ...
```

Далее собираем модель и поднимаем сервер при помощи [llama.cpp](https://github.com/ggml-org/llama.cpp):

```bash
./llama-server -m ./llm_file --port 8080
```

Установка и запуск чата с моделью:

1. Установить менеджер пакетов [uv](https://pypi.org/project/uv/):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2. Установить зависимости:
```bash
uv sync
```
3. На базе файла `.env_example` создать файл `.env` и заполнить значения переменных
4. Запустить `main.py` с нужным параметром, либо без него
```bash
# чат с моделью на произвольную тему
python main.py

# загрузка web-ресурса по указанному url в базу векторов RAG
python main.py -u 

# чат с моделью в рамках RAG контента
python main.py -r

# помощь по доступным параметрам
python main.py -h
```

Также с моделью можно общаться через web-клиент:
```bash
streamlit run web_app.py
```

В планах:
- Подобрать оффлайн модель для генерации embeddings
- ...

Simple chat with an offline llm model that supports OpenAPI. Supports chat in RAG mode.
