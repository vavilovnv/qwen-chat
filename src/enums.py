"""Module for enums."""

from enum import StrEnum

from src import strings


class WorkModes(StrEnum):
    SIMPLE_CHAT = strings.SIMPLE_CHAT
    CHAT_WITH_RAG = strings.CHAT_WITH_RAG
    ADD_URL_RESOURCE = strings.ADD_URL_RESOURCE
    VDB = strings.VDB
