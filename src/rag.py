"""Module for RAG methods."""

import hashlib

import bs4
import requests
from chromadb import GetResult
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
    app_settings.URL_FOR_RAG_CONTENT = input(strings.INPUT_URL_TITLE)

    url = app_settings.URL_FOR_RAG_CONTENT
    update_rag_embeddings(url)


def _get_chroma_db_collection_name(url: str) -> str:
    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()

    return strings.VDB_COLLECTION_NAME.format(url_hash=url_hash[:15])


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


def update_rag_embeddings(url: str) -> None:
    if not url:
        raise ValueError(strings.RAG_URL_EMPTY_ERROR)

    # classes = _get_available_classes()
    strainer = bs4.SoupStrainer(class_="md-content")  # TODO: add more classes here
    loader = WebBaseLoader(
        web_paths=[url],
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
    print(strings.PAGES_WERE_LOADED.format(pages_amount=len(ids)))


def add_url_to_vectordb(url: str) -> tuple[bool, str]:
    try:
        update_rag_embeddings(url)
    except Exception as e:
        return False, str(e)

    return True, strings.URL_SUCCESSFULLY_ADDED


def get_chroma_content() -> list[dict]:
    vector_store = EmbeddingStore().init_store()
    try:
        collection = vector_store._collection  # noqa
    except Exception as e:
        return [{"error": strings.VDB_GETTING_DATA_ERROR.format(error=str(e))}]

    documents: GetResult = collection.get()

    content_list = []
    if documents and "documents" in documents:
        base_data = zip(documents["documents"], documents["metadatas"])  # type: ignore
        for obj_id, (doc, metadata) in enumerate(base_data):
            content_list.append(
                {
                    "id": obj_id,
                    "content": doc[:300] + "..." if len(doc) > 300 else doc,
                    "metadata": metadata,
                }
            )

    return content_list
