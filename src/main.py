from typing import Set

from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

st.header("LLM Documentation Helper")

q = st.text_input("Question", placeholder="Enter question...")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answer_history" not in st.session_state:
    st.session_state["chat_answer_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def create_sources_string(sources_urls: Set[str]) -> str:
    sources_list = list(sources_urls)
    sources_list.sort()
    sources_str = "Sources:\n"
    for i, source in enumerate(sources_urls):
        sources_str += f"{i+1}. {source}"
    return sources_str


if q:
    with st.spinner("Generating response..."):
        generated_response = run_llm(query=q, chat_history=st.session_state["chat_history"])
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['result']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(q)
        st.session_state["chat_answer_history"].append(formatted_response)
        st.session_state["chat_answer_history"].append(("human", q))
        st.session_state["chat_answer_history"].append(("ai", generated_response['result']))

if st.session_state["chat_answer_history"]:
    for user_query, generated_response in zip(
        st.session_state["user_prompt_history"], st.session_state["chat_answer_history"]
    ):
        message(user_query, is_user=True)
        message(generated_response, is_user=False)
