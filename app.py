from pathlib import Path
import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage

from graph import graph

from db import (
    save_message,
    load_messages,
    create_session,
    get_sessions
)


UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)


st.set_page_config(
    page_title="AI Dev Assistant",
    layout="wide"
)


st.markdown(
    """
    <style>

    /* APP */
    .stApp {
        background: #F5F7FB;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #00C6FF 0%,
            #0047FF 100%
        );
        padding-top: 20px;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* TITLE */
    .main-title {
        font-size: 60px;
        font-weight: 800;
        color: #060694;
        margin-bottom: 10px;
    }

    .sub-title {
        font-size: 22px;
        color: #374151;
        margin-bottom: 30px;
    }

    /* CHAT */
    .stChatMessage {
        background: white;
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 14px;
        border: 1px solid #E5E7EB;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    }

    /* INPUT AREA */
    .stChatInputContainer {
        background: transparent !important;
        border-top: none !important;
    }

    .stChatInput {
        background: white !important;
        border-radius: 18px !important;
        padding: 10px !important;
        border: 1px solid #D1D5DB !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    }

    .stChatInput textarea {
        border: none !important;
        box-shadow: none !important;
        font-size: 16px !important;
    }

    /* FILE UPLOADER */
    .stFileUploader {
        background: rgba(255,255,255,0.15);
        padding: 14px;
        border-radius: 18px;
    }

    .stFileUploader button {
        background: white !important;
        color: #060694 !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
    }

    /* DROPDOWN */
    .stSelectbox label {
        display: none;
    }

    .stSelectbox div[data-baseweb="select"] {
        background: white !important;
        border-radius: 12px !important;
    }

    .stSelectbox div[data-baseweb="select"] * {
        color: black !important;
    }

    /* BUTTONS */
    .stButton button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 10px;
        background: rgba(255,255,255,0.15);
        color: white !important;
        font-weight: 600;
    }

    .stButton button:hover {
        background: rgba(255,255,255,0.25);
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="main-title">
        💻 AI Dev Assistant
    </div>

    <div class="sub-title">
        Upload files, inspect images, explain code, debug, optimize and generate frontend code.
    </div>
    """,
    unsafe_allow_html=True
)


username = "Shreya"


if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()


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


# SIDEBAR
st.sidebar.title("💬 Chats")


uploaded_files = st.sidebar.file_uploader(
    "Upload files",
    accept_multiple_files=True
)


if uploaded_files:

    for uploaded_file in uploaded_files:

        file_path = UPLOADS_DIR / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())


st.sidebar.markdown("## 📁 Uploaded Files")


saved_files = []

if UPLOADS_DIR.exists():

    saved_files = [
        file.name
        for file in UPLOADS_DIR.iterdir()
        if file.is_file()
    ]


if saved_files:

    st.sidebar.selectbox(
        "",
        options=saved_files,
        index=None,
        placeholder="Your uploaded files"
    )

else:
    st.sidebar.info("No uploaded files yet.")


st.sidebar.markdown("---")


st.sidebar.markdown("## 🕘 Chat History")


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


if st.sidebar.button("➕ New Chat"):

    st.session_state.session_id = create_session()

    st.session_state.messages = []

    st.rerun()


# CHAT HISTORY
for msg in st.session_state.messages:

    role = "assistant"

    if isinstance(msg, HumanMessage):
        role = "user"

    with st.chat_message(role):
        st.markdown(msg.content)


# INPUT
user_input = st.chat_input(
    "Ask something..."
)


if user_input:

    saved_files = []

    if UPLOADS_DIR.exists():

        saved_files = [
            file.name
            for file in UPLOADS_DIR.iterdir()
            if file.is_file()
        ]


    context_text = ""

    if saved_files:

        context_text = (
            "\n\nUploaded files available:\n"
            + "\n".join(
                f"- {file_name}"
                for file_name in saved_files
            )
        )


    effective_user_input = (
        user_input + context_text
    )


    human_message = HumanMessage(
        content=effective_user_input
    )


    st.session_state.messages.append(
        human_message
    )


    save_message(
        username,
        st.session_state.session_id,
        "user",
        effective_user_input
    )


    with st.chat_message("user"):
        st.markdown(user_input)


    with st.spinner("🧠 AI Dev Assistant is thinking..."):

        response = graph.invoke({
            "messages": st.session_state.messages
        })


    ai_message = None


    for message in reversed(response["messages"]):

        if (
            isinstance(message, AIMessage)
            and message.content
        ):

            ai_message = message
            break


    if ai_message is None:

        ai_message = AIMessage(
            content="I could not generate a final response."
        )


    with st.chat_message("assistant"):
        st.markdown(ai_message.content)


    st.session_state.messages.append(
        ai_message
    )


    save_message(
        username,
        st.session_state.session_id,
        "assistant",
        ai_message.content
    )