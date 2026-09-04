import streamlit as st
from utils.session import init_session_state
from components.styles import load_css
from components.sidebar import render_sidebar

st.set_page_config(page_title="Profile | GlowUP AI", layout="wide")
init_session_state()
load_css()
render_sidebar()

st.title("👤 Your Style Profile")

FACE_OPTIONS = ["", "Oval", "Round", "Square", "Rectangular", "Heart", "Diamond"]
SKIN_OPTIONS = ["", "Fair", "Light", "Medium", "Olive", "Tan", "Deep"]
BODY_OPTIONS = ["", "Ectomorph", "Mesomorph", "Endomorph"]
HAIR_OPTIONS = ["Straight", "Wavy", "Curly", "Dreadlocks", "Kinky"]
BALD_OPTIONS = ["", "Not Bald", "Receding", "Bald"]

col1, col2 = st.columns(2)

with col1:
    st.session_state.face_shape = st.selectbox("Face Shape", FACE_OPTIONS, 
        index=FACE_OPTIONS.index(st.session_state.face_shape) if st.session_state.face_shape in FACE_OPTIONS else 0)
    
    st.session_state.skin_tone = st.selectbox("Skin Tone", SKIN_OPTIONS,
        index=SKIN_OPTIONS.index(st.session_state.skin_tone) if st.session_state.skin_tone in SKIN_OPTIONS else 0)
    
    st.session_state.body_type = st.selectbox("Body Type", BODY_OPTIONS,
        index=BODY_OPTIONS.index(st.session_state.body_type) if st.session_state.body_type in BODY_OPTIONS else 0)

with col2:
    st.session_state.hair_type = st.selectbox("Hair Type", HAIR_OPTIONS,
        index=HAIR_OPTIONS.index(st.session_state.hair_type) if st.session_state.hair_type in HAIR_OPTIONS else 0)
    
    st.session_state.bald_status = st.selectbox("Scalp / Bald Status", BALD_OPTIONS,
        index=BALD_OPTIONS.index(st.session_state.bald_status) if st.session_state.bald_status in BALD_OPTIONS else 0)
    
    st.session_state.preferences = st.text_input("Style Preferences", 
        value=st.session_state.preferences, placeholder="clean, professional, streetwear...")

st.success("Profile updated! These values will be used in Chat recommendations.")