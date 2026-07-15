import streamlit as st
from styles import load_css
from api import health_check
from pages.analyzer import render_analyzer
from pages.assistant import render_assistant

st.set_page_config(
    page_title="GlowUp AI",
    page_icon="",
    layout="wide"
)

load_css()

# Session state
if "face_shape" not in st.session_state:
    st.session_state.face_shape = None
if "skin_tone" not in st.session_state:
    st.session_state.skin_tone = None
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar navigation
with st.sidebar:
    st.markdown('<div class="sidebar-brand">GlowUp AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Personal Transformation</div>', unsafe_allow_html=True)
    
    st.divider()
    
    page = st.radio(
        "Navigation",
        ["Home", "Analyzer", "Assistant"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Status
    status = health_check()
    if status["success"]:
        st.markdown('<div class="status-online">● API Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">● API Offline</div>', unsafe_allow_html=True)

# Page routing
if page == "Home":
    st.markdown('<h1>GlowUp AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#8B8B8B;">Upload a photo or ask the assistant</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="result-card">
                <p style="font-size:24px;font-weight:600;margin:0;">Analyzer</p>
                <p style="color:#8B8B8B;">Upload and analyze your photo</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Analyzer"):
            st.switch_page("pages/analyzer.py")
    
    with col2:
        st.markdown("""
            <div class="result-card">
                <p style="font-size:24px;font-weight:600;margin:0;">Assistant</p>
                <p style="color:#8B8B8B;">Get personalized recommendations</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Assistant"):
            st.switch_page("pages/assistant.py")

elif page == "Analyzer":
    render_analyzer()

elif page == "Assistant":
    render_assistant()