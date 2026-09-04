import streamlit as st
from utils.session import init_session_state
from components.styles import load_css
from components.sidebar import render_sidebar

st.set_page_config(page_title="Settings | GlowUP AI", layout="wide")
init_session_state()
load_css()
render_sidebar()

st.title("⚙️ Settings")

st.subheader("Chat")
if st.button("Clear Chat History", type="secondary"):
    st.session_state.messages = []
    st.success("Chat history cleared.")

st.subheader("Backend")
st.text_input("API Base URL", value="http://localhost:8000", disabled=True)

st.subheader("About")
st.info("GlowUP AI v0.1 — Men's Style & Grooming Assistant")