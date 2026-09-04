import streamlit as st

def init_session_state():
    defaults = {
        "authenticated": False,
        "user": None,
        "messages": [],
        "face_shape": "",
        "skin_tone": "",
        "body_type": "",
        "hair_type": "Straight",
        "bald_status": "",
        "preferences": "",
        "uploaded_image": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value