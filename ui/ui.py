import streamlit as st


def load_css():

    with open("ui/styles.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


def render_main_header():

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


def render_sidebar_heading(text):

    st.sidebar.markdown(
        f"""
        <div class="sidebar-heading">
        {text}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_label(text):

    st.sidebar.markdown(
        f"""
        <div class="label-text">
        {text}
        </div>
        """,
        unsafe_allow_html=True
    )