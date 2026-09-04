import streamlit as st
from components.styles import load_css

LOGO_SVG = """<svg viewBox="0 0 24 24"><path d="M12 2L14.39 8.26L20.65 10.65L14.39 13.04L12 19.3L9.61 13.04L3.35 10.65L9.61 8.26L12 2Z"/></svg>"""

def render_sidebar():
    with st.sidebar:
        # Logo first, at the very top
        st.markdown(f'''
        <div class="sidebar-header">
            <div class="sidebar-logo">{LOGO_SVG}</div>
            <div class="sidebar-title">GlowUP AI</div>
            <div class="sidebar-subtitle">Personal Style Assistant</div>
            <div class="sidebar-status">
                <span class="status-dot"></span> Online
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # Navigation without emojis
        st.page_link("pages/1_Chat.py", label="Chat")
        st.page_link("pages/2_Profile.py", label="Profile")
        st.page_link("pages/3_Settings.py", label="Settings")
        
        if not st.session_state.get("authenticated"):
            st.page_link("pages/4_Login.py", label="Login / Signup")
        else:
            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()

        st.markdown("---")
        st.caption("Quick Tips")
        st.markdown("""
        - Best haircut for oval face  
        - Beard styles for round face  
        - Outfit colors for olive skin  
        - Grooming routine for men
        """)