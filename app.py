from pathlib import Path
import base64
import streamlit as st
from ui.ui import load_css
from langchain_core.messages import HumanMessage, AIMessage

from graph import graph

from db import (
    save_message,
    load_messages,
    create_session,
    get_sessions
)

# =========================================
# CONFIG
# =========================================

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp"
}

st.set_page_config(
    page_title="AI Dev Assistant",
    layout="wide"
)


load_css()


# =========================================
# HEADER
# =========================================

st.markdown(
    """
    <div class="main-card">
        <div class="main-title">
            💻 AI Dev Assistant
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Upload files, debug code, inspect UI images, "
    "optimize applications and generate frontend code."
)
# =========================================
# USER
# =========================================

username = "Shreya"

# =========================================
# SESSION
# =========================================

if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()

if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

# =========================================
# LOAD CHAT HISTORY
# =========================================

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

# =========================================
# BUILD HUMAN MESSAGE
# =========================================

def build_human_message(user_text, uploads_dir):

    image_parts = []

    if uploads_dir.exists():

        for file in uploads_dir.iterdir():

            if file.suffix.lower() in IMAGE_EXTENSIONS:

                if file.name.lower() in user_text.lower():

                    with open(file, "rb") as f:

                        b64 = base64.b64encode(
                            f.read()
                        ).decode("utf-8")

                    mime = f"image/{file.suffix.lower()[1:]}"

                    image_parts.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime};base64,{b64}"
                        }
                    })

    if image_parts:

        return HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": user_text
                },
                *image_parts
            ]
        )

    return HumanMessage(content=user_text)

# =========================================
# SIDEBAR
# =========================================

st.sidebar.markdown("""
<div class="sidebar-heading">
💬 Chats
</div>
""", unsafe_allow_html=True)

# =========================================
# FILE UPLOAD
# =========================================

st.sidebar.markdown("""
<div class="label-text">
UPLOAD FILES
</div>
""", unsafe_allow_html=True)

uploaded_files = st.sidebar.file_uploader(
    "Upload",
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:

    for uploaded_file in uploaded_files:

        file_path = UPLOADS_DIR / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

# =========================================
# FILES
# =========================================

saved_files = []

if UPLOADS_DIR.exists():
    saved_files = [
        file.name
        for file in UPLOADS_DIR.iterdir()
        if file.is_file()
    ]

st.sidebar.markdown("""
<div class="label-text">
SELECT FILE
</div>
""", unsafe_allow_html=True)

if saved_files:

    # ✅ Dropdown
    selected = st.sidebar.selectbox(
        "Select File",
        options=saved_files,
        label_visibility="collapsed"
    )

    st.session_state.selected_file = selected

    st.sidebar.markdown("""
    <div class="label-text">
    FILES
    </div>
    """, unsafe_allow_html=True)

    # ✅ Clean File List UI
    for file_name in saved_files:

        col1, col2 = st.sidebar.columns([6, 1])

        with col1:
            st.markdown(
                f"""
                <div class="file-row">
                    <div class="file-name">📄 {file_name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            if st.button("✕", key=f"delete_{file_name}"):
                file_path = UPLOADS_DIR / file_name
                if file_path.exists():
                    file_path.unlink()
                st.rerun()

else:
    st.sidebar.info("No uploaded files.")

# =========================================
# CHAT HISTORY
# =========================================

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div class="label-text">
CHAT HISTORY
</div>
""", unsafe_allow_html=True)

sessions = get_sessions(username)

for s in sessions:

    label = (
        s["first_message"][:25]
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

# =========================================
# NEW CHAT
# =========================================

if st.sidebar.button("➕ New Chat"):

    st.session_state.session_id = create_session()
    st.session_state.messages = []

    st.rerun()

# =========================================
# CHAT DISPLAY
# =========================================

for msg in st.session_state.messages:

    role = "assistant"

    if isinstance(msg, HumanMessage):
        role = "user"

    with st.chat_message(role):

        if isinstance(msg.content, list):

            for item in msg.content:

                if item["type"] == "text":
                    st.markdown(item["text"])

        else:
            st.markdown(msg.content)

# =========================================
# CHAT INPUT
# =========================================

user_input = st.chat_input(
    "Ask something about selected file..."
)

# =========================================
# PROCESS INPUT
# =========================================

if user_input:

    selected_file = st.session_state.selected_file

    context_text = ""

    if selected_file:

        context_text = f"""

Selected file:
{selected_file}

Use this file for the current task.
"""

    effective_user_input = (
        user_input + context_text
    )

    human_message = build_human_message(
        effective_user_input,
        UPLOADS_DIR
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

    with st.spinner("Thinking..."):

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
            content="No response generated."
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