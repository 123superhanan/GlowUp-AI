import streamlit as st
from utils.session import init_session_state
from components.styles import load_css

st.set_page_config(
    page_title="GlowUP AI | Personal Style Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="✨"
)

init_session_state()
load_css()

# Redirect logic (simple for now)
if not st.session_state.authenticated:
    st.switch_page("pages/4_Login.py")
else:
    st.switch_page("pages/1_Chat.py")