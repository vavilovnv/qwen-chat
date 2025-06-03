"""Module for RAG methods."""

import hashlib

import bs4
import requests
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from settings import app_settings
from src import strings


class EmbeddingStore:
    @classmethod
    def init_store(cls) -> Chroma:
        return Chroma(
            collection_name=_get_chroma_db_collection_name(
                url=strings.RAG_URL_EMPTY_ERROR
            ),
            embedding_function=HuggingFaceEmbeddings(
                model_name=app_settings.EMBEDDING_MODEL,
            ),
            persist_directory=app_settings.EMBEDDING_DB_FOLDER,
        )


def input_url() -> None:
    app_settings.URL_FOR_RAG_CONTENT = input("Enter URL for RAG content: ")
    update_rag_embeddings()


def _get_chroma_db_collection_name(url: str) -> str:
    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()

    return strings.CHROMA_DB_COLLECTION_NAME.format(url_hash=url_hash[:15])


def _get_available_classes() -> set[str]:
    response = requests.get(app_settings.URL_FOR_RAG_CONTENT)
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    content_containers = [  # TODO: check and make this more flexible
        soup.find("article"),
        soup.find("main"),
        soup.find(id="content"),
        soup.find(class_="content"),
        soup.find(class_="post-title"),
        soup.find(class_="post-header"),
        soup.find(class_="post-content"),
    ]

    classes = set()
    for container in content_containers:
        if not isinstance(container, bs4.BeautifulSoup):
            continue

        if container and (curr_class := container.get("class")):
            classes |= set(curr_class)

    return classes


def update_rag_embeddings() -> None:
    if not app_settings.URL_FOR_RAG_CONTENT:
        raise ValueError(strings.RAG_URL_EMPTY_ERROR)

    # classes = _get_available_classes()
    strainer = bs4.SoupStrainer(class_="md-content")  # TODO: add more classes here
    loader = WebBaseLoader(
        web_paths=[app_settings.URL_FOR_RAG_CONTENT],
        bs_kwargs={"parse_only": strainer},
    )

    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", ".\n"],
        chunk_size=app_settings.EMBEDDING_PAGE_CHUNK_SIZE,  # TODO: link to content size
        chunk_overlap=app_settings.EMBEDDING_PAGE_CHUNK_OVERLAP,  # TODO: link to content size
        add_start_index=True,
    )
    splits = text_splitter.split_documents(docs)

    vector_store = EmbeddingStore().init_store()

    ids = vector_store.add_documents(splits)
    print(f"Загружено {len(ids)} страниц в Chroma DB")
