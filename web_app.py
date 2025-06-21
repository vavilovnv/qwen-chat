import streamlit as st
from openai.types.chat import ChatCompletionMessageParam

from settings import app_settings
from src import strings
from src.llm_interaction import ask_llm, ask_llm_rag
from src.rag import add_url_to_vectordb

APP_TITLE = strings.WEB_APP_TITLE.format(llm_name=app_settings.LLM_NAME)

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)

with st.sidebar:
    st.header(strings.SETTINGS)

    chat_mode = st.radio(
        strings.CHOOSE_CHAT_MODE,
        (strings.SIMPLE_CHAT, strings.CHAT_WITH_RAG, strings.ADD_URL_RESOURCE),
    )

    if chat_mode == strings.CHAT_WITH_RAG:
        st.info(strings.CHAT_WITH_RAG_DESCRIPTION)

    # project info
    st.markdown("---")
    st.markdown(strings.ABOUT_PROJECT)
    st.markdown(strings.ABOUT_PROJECT_DESCRIPTION)
    st.markdown(strings.MODEL_DESCRIPTION.format(llm_name=app_settings.LLM_NAME))

if chat_mode == strings.SIMPLE_CHAT:
    message_history: list[ChatCompletionMessageParam] = []

    if "simple_messages" not in st.session_state:
        st.session_state.simple_messages = []

    for message in st.session_state.simple_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(strings.INPUT_YOUR_MESSAGE):
        st.session_state.simple_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(strings.GENERATE_ANSWER):
                answer = ask_llm(prompt, st.session_state.simple_messages)
                st.markdown(answer)

        st.session_state.simple_messages.append(
            {"role": "assistant", "content": answer}
        )

elif chat_mode == strings.CHAT_WITH_RAG:
    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = []

    for message in st.session_state.rag_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(strings.INPUT_YOUR_MESSAGE):
        st.session_state.rag_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(strings.GENERATE_ANSWER):
                response = ask_llm_rag(prompt, st.session_state.rag_messages)
                st.markdown(response)

        st.session_state.rag_messages.append({"role": "assistant", "content": response})

elif chat_mode == strings.ADD_URL_RESOURCE:
    st.header(strings.ADD_URL_RESOURCE_DESCRIPTION)

    with st.form("url_form"):
        url = st.text_input(strings.INPUT_URL_TITLE)
        submitted = st.form_submit_button(strings.ADD_TITLE)

        if submitted and url:
            with st.spinner(strings.LOAD_PAGE_TITLE):
                success, message = add_url_to_vectordb(url)
                if success:
                    st.success(strings.URL_ADDED_TO_VDB.format(url=url))
                else:
                    st.error(strings.ADD_URL_ERROR.format(message=message))
