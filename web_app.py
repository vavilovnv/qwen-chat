import streamlit as st

from settings import app_settings
from src import strings
from src.enums import WorkModes
from src.llm_interaction import ask_llm, ask_llm_rag
from src.rag import add_url_to_vectordb, get_chroma_content

APP_TITLE = strings.WEB_APP_TITLE.format(llm_name=app_settings.LLM_NAME)

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)


def set_project_setting():
    with st.sidebar:
        # project info
        st.subheader(strings.ABOUT_PROJECT)
        st.markdown(strings.ABOUT_PROJECT_DESCRIPTION)
        st.markdown(strings.MODEL_DESCRIPTION.format(llm_name=app_settings.LLM_NAME))
        if app_settings.API_KEY:
            st.success(strings.API_KEY_WAD_PROVIDED, icon="✅")
        else:
            api_key = st.text_input(strings.INPUT_API_KEY, type="password")
            if not len(api_key):
                st.warning(strings.PLEASE_INPUT_API_KEY, icon="⚠️")
            else:
                st.success(strings.API_KEY_WAS_SET, icon="✅")
                app_settings.API_KEY = api_key

        st.markdown("---")

        # settings
        st.subheader(strings.SETTINGS)

        work_mode = st.radio(
            strings.CHOOSE_CHAT_MODE,
            (
                WorkModes.SIMPLE_CHAT,
                WorkModes.CHAT_WITH_RAG,
                WorkModes.ADD_URL_RESOURCE,
                WorkModes.VDB,
            ),
        )

        if work_mode == WorkModes.SIMPLE_CHAT:
            st.info(strings.SIMPLE_CHAT_DESCRIPTION)
        elif work_mode == WorkModes.CHAT_WITH_RAG:
            st.info(strings.CHAT_WITH_RAG_DESCRIPTION)
        elif work_mode == WorkModes.ADD_URL_RESOURCE:
            st.info(strings.ADD_URL_RESOURCE_DESCRIPTION)
        elif work_mode == WorkModes.VDB:
            st.info(strings.VDB_DESCRIPTION)

        history_length = st.sidebar.slider(
            strings.HISTORY_LENGTH, min_value=0, max_value=100, value=10, step=10
        )
        app_settings.CHAT_HISTORY_LENGTH = history_length

    return work_mode


def handle_simple_chat():
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


def handle_chat_with_rag():
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


def handle_adding_url():
    st.subheader(strings.ADD_URL_RESOURCE_TITLE)

    with st.form("url_form"):
        url = st.text_input(strings.INPUT_URL_TITLE)
        submitted = st.form_submit_button(strings.ADD_TITLE)

        if submitted and url:
            with st.spinner(strings.LOAD_PAGE_TITLE):
                success, message = add_url_to_vectordb(url)
                if success:
                    st.success(strings.URL_ADDED_TO_VDB.format(url=url), icon="✅")
                else:
                    st.error(strings.ADD_URL_ERROR.format(message=message), icon="☠️")


def handle_show_vector_db():
    st.subheader(strings.VDB_TITLE)

    if not app_settings.URL_FOR_RAG_CONTENT:
        st.warning(strings.VDB_IS_EMPTY, icon="⚠️")
        return

    st.write(strings.BASE_URL_FOR_VDB.format(url=app_settings.URL_FOR_RAG_CONTENT))

    with st.spinner(strings.VDB_LOADING_CONTENT):
        content_data = get_chroma_content()

    if not (content_data and "error" not in content_data[0]):
        if content_data:
            st.error(content_data[0].get("error", strings.UNKNOWN_VDB_ERROR))
        else:
            st.error(strings.VDB_LOAD_DATA_ERROR)
        return

    st.success(
        strings.VDB_LOADED_CONTENT.format(pages_amount=len(content_data)), icon="✅"
    )

    st.subheader(strings.STATISTIC)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(strings.DOCUMENTS_AMOUNT, len(content_data))

    with col2:
        avg_len = (
            sum(len(item["content"]) for item in content_data) / len(content_data)
            if content_data
            else 0
        )
        st.metric(
            strings.AVERAGE_DOCUMENT_LENGTH,
            strings.DOCUMENT_SYMBOLS_AMOUNT.format(avg_len=f"{avg_len:.2f}"),
        )

    st.subheader(strings.VDB_CONTENT)

    search_term = st.text_input(strings.SEARCH_IN_CONTENT)

    filtered_data = content_data
    if search_term:
        filtered_data = [
            item
            for item in content_data
            if search_term.lower() in item["content"].lower()
        ]
        st.write(
            strings.FOUND_SOME_DOCUMENTS.format(
                docs_amount=search_term, search_term=search_term
            )
        )

    for i, item in enumerate(filtered_data):
        doc_title = strings.SIMBOLS_IN_DOCUMENT.format(
            num=i + 1, content_len=len(item["content"])
        )
        with st.expander(doc_title):
            st.markdown(strings.CONTENT)
            st.text(item["content"])

            st.markdown(strings.METADATA)
            st.json(item["metadata"])


def handle_selected_mode(work_mode):
    if work_mode == WorkModes.SIMPLE_CHAT:
        handle_simple_chat()
    elif work_mode == WorkModes.CHAT_WITH_RAG:
        handle_chat_with_rag()
    elif work_mode == WorkModes.ADD_URL_RESOURCE:
        handle_adding_url()
    elif work_mode == WorkModes.VDB:
        handle_show_vector_db()


def main():
    handle_selected_mode(set_project_setting())


if __name__ == "__main__":
    main()
