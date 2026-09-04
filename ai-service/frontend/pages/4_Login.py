import streamlit as st
from utils.session import init_session_state
from components.styles import load_css

st.set_page_config(page_title="Login | GlowUP AI", layout="centered")
init_session_state()
load_css()

st.markdown("## 🔐 Welcome to GlowUP AI")
st.markdown("Login or continue as guest (auth will be added later)")

col1, col2 = st.columns(2)

with col1:
    if st.button("Continue as Guest", use_container_width=True, type="primary"):
        st.session_state.authenticated = True
        st.session_state.user = {"name": "Guest"}
        st.switch_page("pages/1_Chat.py")

with col2:
    st.button("Login with Email (Coming Soon)", use_container_width=True, disabled=True)

st.markdown("---")
st.info("Full authentication (email / Google) will be added in the next phase.")