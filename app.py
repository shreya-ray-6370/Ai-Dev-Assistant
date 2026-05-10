import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage

from graph import graph

from db import (
    save_message,
    load_messages,
    create_session,
    get_sessions
)


st.set_page_config(
    page_title="AI Dev Assistant",
    layout="wide"
)

st.title("💻 AI Dev Assistant")


username = "Shreya"


# Session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()


# Load Messages
if "messages" not in st.session_state:

    raw_messages = load_messages(
        username,
        st.session_state.session_id
    )

    st.session_state.messages = []

    for msg in raw_messages:

        if msg["role"] == "user":
            st.session_state.messages.append(
                HumanMessage(content=msg["content"])
            )

        else:
            st.session_state.messages.append(
                AIMessage(content=msg["content"])
            )


# Sidebar
st.sidebar.title("💬 Chats")


sessions = get_sessions(username)


for s in sessions:

    label = (
        s["first_message"][:30]
        if s["first_message"]
        else "New Chat"
    )

    if st.sidebar.button(label, key=s["_id"]):

        st.session_state.session_id = s["_id"]

        raw_messages = load_messages(
            username,
            s["_id"]
        )

        st.session_state.messages = []

        for msg in raw_messages:

            if msg["role"] == "user":
                st.session_state.messages.append(
                    HumanMessage(content=msg["content"])
                )

            else:
                st.session_state.messages.append(
                    AIMessage(content=msg["content"])
                )

        st.rerun()


# New Chat
if st.sidebar.button("➕ New Chat"):

    st.session_state.session_id = create_session()

    st.session_state.messages = []

    st.rerun()


# Display Messages
for msg in st.session_state.messages:

    role = "assistant"

    if isinstance(msg, HumanMessage):
        role = "user"

    with st.chat_message(role):
        st.markdown(msg.content)


# User Input
user_input = st.chat_input("Ask something...")


if user_input:

    human_message = HumanMessage(content=user_input)

    st.session_state.messages.append(human_message)


    save_message(
        username,
        st.session_state.session_id,
        "user",
        user_input
    )


    with st.chat_message("user"):
        st.markdown(user_input)


    response = graph.invoke({
        "messages": st.session_state.messages
    })


    ai_message = response["messages"][-1]


    with st.chat_message("assistant"):
        st.markdown(ai_message.content)


    st.session_state.messages.append(ai_message)


    save_message(
        username,
        st.session_state.session_id,
        "assistant",
        ai_message.content
    )
