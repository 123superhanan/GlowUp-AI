import streamlit as st
from styles import load_css
from api import health_check
from pages.analyzer import render_analyzer
from pages.assistant import render_assistant

# Page config
st.set_page_config(
    page_title="GlowUp AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
load_css()

# Session state
if "page" not in st.session_state:
    st.session_state.page = "Analyzer"
if "face_shape" not in st.session_state:
    st.session_state.face_shape = None
if "skin_tone" not in st.session_state:
    st.session_state.skin_tone = None
if "confidence_face" not in st.session_state:
    st.session_state.confidence_face = 0.0
if "confidence_skin" not in st.session_state:
    st.session_state.confidence_skin = 0.0
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-brand">GlowUp AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Personal Transformation</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Navigation
    if st.button("Analyzer", use_container_width=True):
        st.session_state.page = "Analyzer"
    if st.button("Assistant", use_container_width=True):
        st.session_state.page = "Assistant"
    
    st.divider()
    
    # Status
    status = health_check()
    if status["success"]:
        st.markdown('<div class="status-online">● API Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">● API Offline</div>', unsafe_allow_html=True)
    
    # Show detected features if available
    if st.session_state.face_shape:
        st.caption(f"Face: {st.session_state.face_shape}")
    if st.session_state.skin_tone:
        st.caption(f"Skin: {st.session_state.skin_tone}")

# Page routing
if st.session_state.page == "Analyzer":
    render_analyzer()
else:
    render_assistant()