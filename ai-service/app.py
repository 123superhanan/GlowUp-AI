import streamlit as st
import requests
import json
# Set page config
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
    
    /* Hide default sidebar navigation */
    .stSidebarNav {display: none;}
    
    /* Sidebar Styling */
    .css-1d391kg, .css-12oz5g7 {
        background: linear-gradient(180deg, #0d0f12 0%, #161b22 100%);
        border-right: 1px solid #1e293b;
    }
    
    .css-1d391kg .st-emotion-cache-16idsys, 
    .css-12oz5g7 .st-emotion-cache-16idsys {
        padding: 0;
    }

    .sidebar-header {
        padding: 2rem 1.5rem 1.5rem 1.5rem;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .sidebar-logo {
        width: 72px;
        height: 72px;
        margin: 0 auto 12px auto;
        background: linear-gradient(135deg, #a855f7, #6366f1, #3b82f6);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 16px;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
    }

    .sidebar-logo svg {
        width: 100%;
        height: 100%;
        fill: white;
    }

    .sidebar-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 4px;
        letter-spacing: 0.5px;
    }

    .sidebar-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #1e293b;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.7rem;
        color: #34d399;
        border: 1px solid #064e3b;
        margin-top: 8px;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        background: #34d399;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }

    .sidebar-section-title {
        color: #94a3b8;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 0 0 8px 0;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 14px;
    }

    /* Profile fields in sidebar */
    .profile-field {
        margin-bottom: 12px;
    }

    .profile-field label {
        color: #94a3b8;
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: block;
        margin-bottom: 4px;
    }

    .profile-field select, 
    .profile-field input {
        width: 100%;
        background: #0d0f12;
        border: 1px solid #1e293b;
        color: #e2e8f0;
        padding: 8px 12px;
        border-radius: 10px;
        font-size: 0.85rem;
        transition: all 0.2s;
    }

    .profile-field select:focus,
    .profile-field input:focus {
        border-color: #6366f1;
        outline: none;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }

    .profile-field select option {
        background: #0d0f12;
    }

    .upload-area {
        background: #0d0f12;
        border: 1px dashed #334155;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        transition: all 0.2s;
        cursor: pointer;
        margin-top: 4px;
    }

    .upload-area:hover {
        border-color: #6366f1;
        background: #161b22;
    }

    .upload-area .upload-icon {
        color: #94a3b8;
        font-size: 1.5rem;
        display: block;
        margin-bottom: 4px;
    }

    .upload-area .upload-text {
        color: #94a3b8;
        font-size: 0.75rem;
    }

    .image-preview {
        max-width: 100%;
        border-radius: 10px;
        margin-top: 8px;
        border: 1px solid #1e293b;
    }

    /* Main chat area */
    .main .block-container {
        max-width: 900px;
        padding: 2rem 3rem 6rem 3rem;
    }

    /* Chat Bubbles */
    .chat-bubble-user {
        background: linear-gradient(135deg, #1e293b, #2d3748);
        color: #f8fafc;
        padding: 14px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px auto;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        border: 1px solid #334155;
        font-size: 0.98rem;
        line-height: 1.5;
        animation: slideInRight 0.3s ease;
    }

    .chat-bubble-assistant {
        background: linear-gradient(135deg, #161b22, #1a1f2e);
        color: #f1f5f9;
        padding: 16px 20px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 88%;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
        border: 1px solid #2d3748;
        font-size: 0.98rem;
        line-height: 1.6;
        animation: slideInLeft 0.3s ease;
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .assistant-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #818cf8;
        margin-bottom: 10px;
    }

    .bot-icon {
        width: 18px;
        height: 18px;
        fill: #818cf8;
    }

    /* Sources */
    .sources-container {
        margin-top: 12px;
        padding-top: 10px;
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
        background: #0f172a;
        color: #38bdf8;
        border: 1px solid #1e293b;
        padding: 3px 12px;
        border-radius: 14px;
        font-size: 0.7rem;
        font-family: monospace;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
    }

    .source-tag:hover {
        background: #1e293b;
        border-color: #38bdf8;
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
        transition: border-color 0.3s;
    }

    .stChatInputContainer:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    }

    /* Welcome message */
    .welcome-container {
        text-align: center;
        padding: 3rem 2rem;
        color: #94a3b8;
    }

    .welcome-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .welcome-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }

    .welcome-sub {
        font-size: 1rem;
        max-width: 500px;
        margin: 0 auto;
        line-height: 1.6;
    }

    .welcome-tips {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 1.5rem;
    }

    .welcome-tip {
        background: #161b22;
        padding: 8px 16px;
        border-radius: 20px;
        border: 1px solid #1e293b;
        font-size: 0.8rem;
        color: #94a3b8;
    }

    /* Misc */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
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

</style>
""", unsafe_allow_html=True)

# SVG Icons
LOGO_SVG = """<svg viewBox="0 0 24 24"><path d="M12 2L14.39 8.26L20.65 10.65L14.39 13.04L12 19.3L9.61 13.04L3.35 10.65L9.61 8.26L12 2Z"/></svg>"""
BOT_SVG = """<svg class="bot-icon" viewBox="0 0 24 24"><path d="M12 2A2 2 0 0 1 14 4C14 4.74 13.6 5.39 13 5.73V7H14A7 7 0 0 1 21 14V16A3 3 0 0 1 18 19H16.8V20A2 2 0 0 1 14.8 22H9.2A2 2 0 0 1 7.2 20V19H6A3 3 0 0 1 3 16V14A7 7 0 0 1 10 7H11V5.73C10.4 5.39 10 4.74 10 4A2 2 0 0 1 12 2M7.5 13A1.5 1.5 0 0 0 6 14.5A1.5 1.5 0 0 0 7.5 16A1.5 1.5 0 0 0 9 14.5A1.5 1.5 0 0 0 7.5 13M16.5 13A1.5 1.5 0 0 0 15 14.5A1.5 1.5 0 0 0 16.5 16A1.5 1.5 0 0 0 18 14.5A1.5 1.5 0 0 0 16.5 13Z"/></svg>"""
DOC_SVG = """<svg class="doc-icon" viewBox="0 0 24 24"><path d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2M18 20H6V4H13V9H18V20Z"/></svg>"""

# Initialize session state
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

def normalize_face_shape(value: str) -> str:
    if not value:
        return ""
    v = str(value).strip().lower()
    mapping = {
        "oval": "Oval",
        "round": "Round",
        "square": "Square",
        "rectangular": "Rectangular",
        "oblong": "Rectangular",
        "heart": "Heart",
        "diamond": "Diamond",
    }
    return mapping.get(v, value.title())


def normalize_skin_tone(value: str) -> str:
    if not value:
        return ""
    v = str(value).strip().lower()
    mapping = {
        "fair": "Fair",
        "light": "Light",
        "white": "Fair",          # map model "White" -> Fair
        "pale": "Fair",
        "medium": "Medium",
        "olive": "Olive",
        "tan": "Tan",
        "brown": "Tan",
        "dark": "Deep",
        "deep": "Deep",
        "black": "Deep",
    }
    return mapping.get(v, value.title())


FACE_OPTIONS = ["", "Oval", "Round", "Square", "Rectangular", "Heart", "Diamond"]
SKIN_OPTIONS = ["", "Fair", "Light", "Medium", "Olive", "Tan", "Deep"]
BODY_OPTIONS = ["", "Ectomorph", "Mesomorph", "Endomorph"]


with st.sidebar:
    st.markdown(f'''
    <div class="sidebar-header">
        <div class="sidebar-logo">{LOGO_SVG}</div>
        <div class="sidebar-title">GlowUP AI</div>
        <div class="sidebar-subtitle">Personal Style Assistant</div>
        <div class="sidebar-status"><span class="status-dot"></span>Online</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Your Style Profile</div>', unsafe_allow_html=True)

    # Keep values stable
    if "face_shape" not in st.session_state:
        st.session_state.face_shape = ""
    if "skin_tone" not in st.session_state:
        st.session_state.skin_tone = ""
    if "body_type" not in st.session_state:
        st.session_state.body_type = ""
    if "preferences" not in st.session_state:
        st.session_state.preferences = ""

    st.selectbox(
        "Face Shape",
        FACE_OPTIONS,
        key="face_shape"
    )

    st.selectbox(
        "Skin Tone",
        SKIN_OPTIONS,
        key="skin_tone"
    )

    st.selectbox(
        "Body Type",
        BODY_OPTIONS,
        key="body_type"
    )

    st.text_input(
        "Style Preferences",
        key="preferences",
        placeholder="messy, clean, professional..."
    )

    uploaded_file = st.file_uploader(
        "Upload Photo",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.session_state.uploaded_image = uploaded_file
        st.image(uploaded_file, use_container_width=True)

        if st.button("Detect Face Shape & Skin Tone", use_container_width=True):
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }

            with st.spinner("Detecting..."):
                # Face shape
                try:
                    r1 = requests.post(
                        "http://localhost:8000/face-shape/predict",
                        files=files,
                        timeout=120
                    )
                    if r1.ok:
                        pred = r1.json().get("prediction", {})
                        raw_shape = pred.get("class") if isinstance(pred, dict) else pred
                        shape = normalize_face_shape(raw_shape)
                        if shape in FACE_OPTIONS:
                            st.session_state.face_shape = shape
                            st.success(f"Face shape: {shape}")
                        else:
                            st.warning(f"Face shape detected as '{raw_shape}' (not in list)")
                    else:
                        st.error(f"Face shape API error: {r1.text}")
                except Exception as e:
                    st.error(f"Face shape failed: {e}")

                # Skin tone
                try:
                    r2 = requests.post(
                        "http://localhost:8000/skin-tone/predict",
                        files=files,
                        timeout=120
                    )
                    if r2.ok:
                        pred = r2.json().get("prediction", {})
                        raw_tone = pred.get("class") if isinstance(pred, dict) else pred
                        tone = normalize_skin_tone(raw_tone)
                        if tone in SKIN_OPTIONS:
                            st.session_state.skin_tone = tone
                            st.success(f"Skin tone: {tone}")
                        else:
                            st.warning(f"Skin tone detected as '{raw_tone}' (not in list)")
                    else:
                        st.error(f"Skin tone API error: {r2.text}")
                except Exception as e:
                    st.error(f"Skin tone failed: {e}")

            st.rerun()
# ---------- MAIN CHAT AREA ----------
# Display chat history
if not st.session_state.messages:
    # Welcome message
    st.markdown('''
    <div class="welcome-container">
        <div class="welcome-logo">✨</div>
        <div class="welcome-title">How can I help you look your best?</div>
        <div class="welcome-sub">
            I'm your personal style assistant. Ask me about hairstyles, 
            beard grooming, outfits, colors, and more.
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
                st.image(message["image"], width=140)
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

if prompt := st.chat_input("Ask about hairstyles, outfits, grooming..."):
    user_msg = {
        "role": "user",
        "content": prompt,
        "image": st.session_state.uploaded_image.getvalue() if st.session_state.uploaded_image else None
    }
    st.session_state.messages.append(user_msg)

    st.markdown(f'<div class="chat-bubble-user">{prompt}</div>', unsafe_allow_html=True)
    if st.session_state.uploaded_image:
        st.image(st.session_state.uploaded_image, width=140)

    st.markdown(f'''
    <div class="chat-bubble-assistant">
        <div class="assistant-header">{BOT_SVG} GlowUP Assistant</div>
    </div>
    ''', unsafe_allow_html=True)

    answer_placeholder = st.empty()
    sources_placeholder = st.empty()

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
            stream=True
        )
        response.raise_for_status()

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            if line.startswith("data: "):
                payload = line[6:]
                data = json.loads(payload)

                if data.get("type") == "token":
                    full_answer += data.get("content", "")
                    answer_placeholder.markdown(full_answer)

                elif data.get("type") == "sources":
                    sources = data.get("sources", [])

                elif data.get("type") == "done":
                    break

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_answer,
            "sources": sources
        })

        if sources:
            tags = "".join([f'<span class="source-tag">{DOC_SVG} {s}</span>' for s in sources])
            sources_placeholder.markdown(f'''
            <div class="sources-container">
                <span class="sources-label">Sources:</span> {tags}
            </div>
            ''', unsafe_allow_html=True)
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the server. Please make sure the backend is running.")
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")