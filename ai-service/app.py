import streamlit as st
import requests
import json
from time import time

st.set_page_config(
    page_title="GlowUP AI | Personal Style Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0d0f12;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .stSidebarNav {display: none;}
    
    .css-1d391kg, .css-12oz5g7 {
        background: linear-gradient(180deg, #0d0f12 0%, #161b22 100%);
        border-right: 1px solid #1e293b;
    }

    /* Sidebar Header */
    .sidebar-header {
        padding: 2rem 1.5rem 1.5rem 1.5rem;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 1.5rem;
        text-align: center;
        position: relative;
    }

    .sidebar-header::after {
        content: '';
        position: absolute;
        bottom: -1px;
        left: 20%;
        right: 20%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #6366f1, transparent);
    }

    .sidebar-logo {
        width: 80px;
        height: 80px;
        margin: 0 auto 14px auto;
        background: linear-gradient(135deg, #a855f7, #6366f1, #3b82f6);
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 18px;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
        transition: transform 0.3s;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }

    .sidebar-logo:hover {
        transform: scale(1.05);
    }

    .sidebar-logo svg {
        width: 100%;
        height: 100%;
        fill: white;
    }

    .sidebar-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        letter-spacing: -0.02em;
        text-shadow: 0 0 40px rgba(99, 102, 241, 0.2);
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 4px;
        letter-spacing: 1px;
        font-weight: 300;
    }

    .sidebar-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        padding: 5px 16px;
        border-radius: 20px;
        font-size: 0.7rem;
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.2);
        margin-top: 10px;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background: #34d399;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px rgba(52, 211, 153, 0.5);
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.8); }
    }

    /* Sidebar Sections */
    .sidebar-section {
        margin-bottom: 1.5rem;
    }

    .sidebar-section-title {
        color: #94a3b8;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 0 0 10px 0;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sidebar-section-title .icon {
        font-size: 1rem;
    }

    /* Form elements in sidebar */
    .stSelectbox, .stTextInput {
        margin-bottom: 4px;
    }

    .stSelectbox > div > div,
    .stTextInput > div > div {
        background: #0d0f12 !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
        transition: all 0.2s !important;
    }

    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }

    .stSelectbox label,
    .stTextInput label {
        color: #94a3b8 !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Upload Area */
    .upload-wrapper {
        background: #0d0f12;
        border: 1px dashed #1e293b;
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        transition: all 0.3s;
        text-align: center;
    }

    .upload-wrapper:hover {
        border-color: #6366f1;
        background: #161b22;
    }

    .upload-wrapper .stFileUploader {
        margin: 0;
    }

    .upload-wrapper .stFileUploader > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e293b, #2d3748) !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2d3748, #3d4a5e) !important;
        border-color: #6366f1 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .detect-btn > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border-color: #6366f1 !important;
        color: white !important;
        font-weight: 600 !important;
    }

    .detect-btn > button:hover {
        background: linear-gradient(135deg, #818cf8, #a78bfa) !important;
        box-shadow: 0 4px 24px rgba(99, 102, 241, 0.4);
    }

    .clear-btn > button {
        background: #1a1a1a !important;
        border-color: #2d2d2d !important;
        color: #94a3b8 !important;
    }

    .clear-btn > button:hover {
        background: #2d2d2d !important;
        border-color: #ef4444 !important;
        color: #ef4444 !important;
    }

    /* Main Chat Area */
    .main .block-container {
        max-width: 950px;
        padding: 2rem 3rem 6rem 3rem;
    }

    /* Chat Bubbles */
    .chat-bubble-user {
        background: linear-gradient(135deg, #1e293b, #2d3748);
        color: #f8fafc;
        padding: 14px 20px;
        border-radius: 20px 20px 4px 20px;
        margin: 8px 0 8px auto;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        border: 1px solid #334155;
        font-size: 0.98rem;
        line-height: 1.6;
        animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .chat-bubble-assistant {
        background: linear-gradient(135deg, #161b22, #1a1f2e);
        color: #f1f5f9;
        padding: 16px 22px;
        border-radius: 20px 20px 20px 4px;
        margin: 8px 0;
        max-width: 88%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
        border: 1px solid #2d3748;
        font-size: 0.98rem;
        line-height: 1.7;
        animation: slideInLeft 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .assistant-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #818cf8;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #1e293b;
    }

    .assistant-header .typing-indicator {
        display: inline-flex;
        gap: 4px;
        margin-left: 8px;
    }

    .assistant-header .typing-indicator span {
        width: 6px;
        height: 6px;
        background: #818cf8;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }

    .assistant-header .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .assistant-header .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.3; }
        30% { transform: translateY(-8px); opacity: 1; }
    }

    .bot-icon {
        width: 18px;
        height: 18px;
        fill: #818cf8;
    }

    .user-icon {
        display: inline-block;
        width: 28px;
        height: 28px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 50%;
        text-align: center;
        line-height: 28px;
        font-size: 14px;
        margin-right: 8px;
        flex-shrink: 0;
    }

    /* Sources */
    .sources-container {
        margin-top: 14px;
        padding-top: 12px;
        border-top: 1px solid #27272a;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
    }
    
    .sources-label {
        font-size: 0.7rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .source-tag {
        background: linear-gradient(135deg, #0f172a, #1a1f2e);
        color: #38bdf8;
        border: 1px solid #1e293b;
        padding: 4px 12px;
        border-radius: 14px;
        font-size: 0.7rem;
        font-family: monospace;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: all 0.3s;
    }

    .source-tag:hover {
        border-color: #38bdf8;
        transform: translateY(-1px);
    }

    .doc-icon {
        width: 12px;
        height: 12px;
        fill: #38bdf8;
    }

    /* Chat Input */
    .stChatInputContainer {
        border-radius: 16px !important;
        border: 1px solid #334155 !important;
        background: #161b22 !important;
        transition: all 0.3s !important;
    }

    .stChatInputContainer:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15) !important;
    }

    /* Welcome */
    .welcome-container {
        text-align: center;
        padding: 4rem 2rem;
        color: #94a3b8;
    }

    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }

    .welcome-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e2e8f0, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .welcome-sub {
        font-size: 1.05rem;
        max-width: 550px;
        margin: 0 auto;
        line-height: 1.7;
        color: #94a3b8;
    }

    .welcome-tips {
        display: flex;
        gap: 0.8rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 2rem;
    }

    .welcome-tip {
        background: #161b22;
        padding: 10px 20px;
        border-radius: 24px;
        border: 1px solid #1e293b;
        font-size: 0.85rem;
        color: #94a3b8;
        transition: all 0.3s;
        cursor: default;
    }

    .welcome-tip:hover {
        border-color: #6366f1;
        color: #e2e8f0;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
    }

    /* Image preview in chat */
    .chat-image {
        border-radius: 12px;
        border: 1px solid #1e293b;
        margin-top: 8px;
    }

    /* Success/Info messages */
    .stAlert {
        background: rgba(30, 41, 59, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
    }

    .stAlert > div {
        color: #e2e8f0 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0d0f12;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# SVG Icons
LOGO_SVG = """<svg viewBox="0 0 24 24"><path d="M12 2L14.39 8.26L20.65 10.65L14.39 13.04L12 19.3L9.61 13.04L3.35 10.65L9.61 8.26L12 2Z"/></svg>"""
BOT_SVG = """<svg class="bot-icon" viewBox="0 0 24 24"><path d="M12 2A2 2 0 0 1 14 4C14 4.74 13.6 5.39 13 5.73V7H14A7 7 0 0 1 21 14V16A3 3 0 0 1 18 19H16.8V20A2 2 0 0 1 14.8 22H9.2A2 2 0 0 1 7.2 20V19H6A3 3 0 0 1 3 16V14A7 7 0 0 1 10 7H11V5.73C10.4 5.39 10 4.74 10 4A2 2 0 0 1 12 2M7.5 13A1.5 1.5 0 0 0 6 14.5A1.5 1.5 0 0 0 7.5 16A1.5 1.5 0 0 0 9 14.5A1.5 1.5 0 0 0 7.5 13M16.5 13A1.5 1.5 0 0 0 15 14.5A1.5 1.5 0 0 0 16.5 16A1.5 1.5 0 0 0 18 14.5A1.5 1.5 0 0 0 16.5 13Z"/></svg>"""
DOC_SVG = """<svg class="doc-icon" viewBox="0 0 24 24"><path d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2M18 20H6V4H13V9H18V20Z"/></svg>"""
USER_SVG = """<svg viewBox="0 0 24 24" width="14" height="14" fill="white"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>"""

# Options
FACE_OPTIONS = ["", "Oval", "Round", "Square", "Rectangular", "Heart", "Diamond"]
SKIN_OPTIONS = ["", "Fair", "Light", "Medium", "Olive", "Tan", "Deep", "White", "Black", "Brown", "Yellow", "Red", "Pink"]
BODY_OPTIONS = ["", "Ectomorph", "Mesomorph", "Endomorph"]

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "face_shape" not in st.session_state:
    st.session_state.face_shape = ""
if "skin_tone" not in st.session_state:
    st.session_state.skin_tone = ""
if "body_type" not in st.session_state:
    st.session_state.body_type = ""
if "preferences" not in st.session_state:
    st.session_state.preferences = ""
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown(f'''
    <div class="sidebar-header">
        <div class="sidebar-logo">
            {LOGO_SVG}
        </div>
        <div class="sidebar-title">GlowUP AI</div>
        <div class="sidebar-subtitle">Personal Style Assistant</div>
        <div class="sidebar-status">
            <span class="status-dot"></span>
            Online
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Profile Section
    st.markdown('''
    <div class="sidebar-section">
        <div class="sidebar-section-title">
            <span class="icon">✧</span> Your Style Profile
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.session_state.face_shape = st.selectbox(
        "Face Shape",
        FACE_OPTIONS,
        index=FACE_OPTIONS.index(st.session_state.face_shape) if st.session_state.face_shape in FACE_OPTIONS else 0
    )

    st.session_state.skin_tone = st.selectbox(
        "Skin Tone",
        SKIN_OPTIONS,
        index=SKIN_OPTIONS.index(st.session_state.skin_tone) if st.session_state.skin_tone in SKIN_OPTIONS else 0
    )

    st.session_state.body_type = st.selectbox(
        "Body Type",
        BODY_OPTIONS,
        index=BODY_OPTIONS.index(st.session_state.body_type) if st.session_state.body_type in BODY_OPTIONS else 0
    )

    st.session_state.preferences = st.text_input(
        "Style Preferences",
        value=st.session_state.preferences,
        placeholder="messy, clean, professional..."
    )

    # Photo Upload
    uploaded_file = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.session_state.uploaded_image = uploaded_file
        st.image(uploaded_file, use_container_width=True)

        # Detect button with custom class
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(" Detect Face & Skin", key="detect", use_container_width=True):
                with st.spinner("Analyzing your photo..."):
                    files = {
                        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                    }

                    # Face shape
                    try:
                        r1 = requests.post("http://localhost:8000/face-shape/predict", files=files, timeout=60)
                        if r1.ok:
                            pred = r1.json().get("prediction", {})
                            shape = pred.get("class") if isinstance(pred, dict) else pred
                            if shape:
                                st.session_state.face_shape = str(shape).title()
                                st.success(f" Face shape: {st.session_state.face_shape}")
                        else:
                            st.warning("Face shape detection failed")
                    except Exception as e:
                        st.warning(f"Face shape error: {e}")

                    # Skin tone
                    try:
                        r2 = requests.post("http://localhost:8000/skin-tone/predict", files=files, timeout=60)
                        if r2.ok:
                            pred = r2.json().get("prediction", {})
                            tone = pred.get("class") if isinstance(pred, dict) else pred
                            if tone:
                                st.session_state.skin_tone = str(tone).title()
                                st.success(f" Skin tone: {st.session_state.skin_tone}")
                        else:
                            st.warning("Skin tone detection failed")
                    except Exception as e:
                        st.warning(f"Skin tone error: {e}")

                st.rerun()
        
        with col2:
            if st.button("delete", key="clear_img", help="Remove photo"):
                st.session_state.uploaded_image = None
                st.rerun()

    # Clear chat
    if st.button(" Clear Chat History", key="clear_chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.7rem; color: #64748b; text-align: center; padding: 0.5rem;">
        <div style="margin-bottom: 8px; font-weight: 600; color: #94a3b8;"> Quick Tips</div>
        <div style="line-height: 1.8;">
            • "Best haircut for oval face"<br>
            • "Beard styles for round face"<br>
            • "Outfit colors for olive skin"<br>
            • "Grooming routine for men"
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- MAIN CHAT AREA ----------
if not st.session_state.messages:
    st.markdown('''
    <div class="welcome-container">
        <div class="welcome-icon">✨</div>
        <div class="welcome-title">How can I help you look your best?</div>
        <div class="welcome-sub">
            Your personal AI style assistant for beard styles, haircuts, 
            outfit colors, and grooming advice.
        </div>
        <div class="welcome-tips">
            <span class="welcome-tip"> Best haircut for my face</span>
            <span class="welcome-tip"> Beard style guide</span>
            <span class="welcome-tip"> Outfit color combos</span>
            <span class="welcome-tip"> Grooming routine</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">{message["content"]}</div>', unsafe_allow_html=True)
            if message.get("image"):
                st.image(message["image"], width=140, output_format="JPEG")
        else:
            st.markdown(f'''
            <div class="chat-bubble-assistant">
                <div class="assistant-header">{BOT_SVG} GlowUP Assistant</div>
                {message["content"]}
            </div>
            ''', unsafe_allow_html=True)

            if message.get("sources"):
                tags = "".join([f'<span class="source-tag">{DOC_SVG} {s}</span>' for s in message["sources"]])
                st.markdown(f'''
                <div class="sources-container">
                    <span class="sources-label">Sources:</span> {tags}
                </div>
                ''', unsafe_allow_html=True)

# ---------- CHAT INPUT ----------
if prompt := st.chat_input("Ask about hairstyles, outfits, grooming..."):
    user_msg = {
        "role": "user",
        "content": prompt,
        "image": st.session_state.uploaded_image.getvalue() if st.session_state.uploaded_image else None
    }
    st.session_state.messages.append(user_msg)

    # Display user message
    st.markdown(f'<div class="chat-bubble-user">{prompt}</div>', unsafe_allow_html=True)
    if st.session_state.uploaded_image:
        st.image(st.session_state.uploaded_image, width=140, output_format="JPEG")

    # Assistant response placeholder with typing indicator
    response_placeholder = st.empty()
    
    # Show typing indicator
    with response_placeholder.container():
        st.markdown(f'''
        <div class="chat-bubble-assistant">
            <div class="assistant-header">
                {BOT_SVG} GlowUP Assistant
                <span class="typing-indicator">
                    <span></span><span></span><span></span>
                </span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    full_answer = ""
    sources = []

    try:
        response = requests.post(
            "http://localhost:8000/rag/ask/stream",
            json={
                "question": prompt,
                "face_shape": st.session_state.face_shape or None,
                "skin_tone": st.session_state.skin_tone or None,
                "body_type": st.session_state.body_type or None,
                "preferences": st.session_state.preferences or None
            },
            stream=True,
            timeout=60
        )
        response.raise_for_status()

        # Clear typing indicator and show streaming response
        response_placeholder.empty()
        answer_container = st.empty()
        sources_container = st.empty()

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            if line.startswith("data: "):
                payload = line[6:]
                data = json.loads(payload)

                if data.get("type") == "token":
                    full_answer += data.get("content", "")
                    answer_container.markdown(f'''
                    <div class="chat-bubble-assistant">
                        <div class="assistant-header">{BOT_SVG} GlowUP Assistant</div>
                        {full_answer}
                    </div>
                    ''', unsafe_allow_html=True)

                elif data.get("type") == "sources":
                    sources = data.get("sources", [])
                    if sources:
                        tags = "".join([f'<span class="source-tag">{DOC_SVG} {s}</span>' for s in sources])
                        sources_container.markdown(f'''
                        <div class="sources-container">
                            <span class="sources-label">Sources:</span> {tags}
                        </div>
                        ''', unsafe_allow_html=True)

                elif data.get("type") == "done":
                    break

        # Save to session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_answer,
            "sources": sources
        })

    except requests.exceptions.ConnectionError:
        st.error(" Unable to connect to the server. Please make sure the backend is running.")
    except requests.exceptions.Timeout:
        st.error("⏱ Request timed out. Please try again.")
    except Exception as e:
        st.error(f" Something went wrong: {str(e)}")
    
    st.rerun()