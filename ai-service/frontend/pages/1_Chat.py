import streamlit as st
from utils.session import init_session_state
from components.styles import load_css
from components.sidebar import render_sidebar
from utils.api import stream_rag_response, detect_features

st.set_page_config(
    page_title="Chat | GlowUP AI",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="✨"
)

init_session_state()
load_css()
render_sidebar()  # <--- Keep this, remove the extra 'with st.sidebar:' block below

# Custom Inline Icons
SPARKLES_SVG = """<svg class="glow-icon" viewBox="0 0 24 24" width="20" height="20"><path fill="url(#indigo-grad)" d="M12 2L14.39 8.26L20.65 10.65L14.39 13.04L12 19.3L9.61 13.04L3.35 10.65L9.61 8.26L12 2Z"/><defs><linearGradient id="indigo-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#a855f7"/><stop offset="100%" stop-color="#6366f1"/></linearGradient></defs></svg>"""
CAMERA_SVG = """<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>"""
DOC_SVG = """<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#6366f1" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>"""

# Header Banner
st.markdown(f'''
<div class="chat-header-banner">
    <div class="banner-title-group">
        {SPARKLES_SVG}
        <span class="banner-title">Style Studio</span>
    </div>
    <span class="banner-badge">AI Assistant Active</span>
</div>
''', unsafe_allow_html=True)

# Image Upload Card
with st.expander("AI Feature Scanner & Analysis", expanded=False):
    col1, col2 = st.columns([1, 1.8])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Drop photo here or browse", 
            type=["jpg", "jpeg", "png"],
            help="Upload a clear front-facing portrait"
        )
    
    with col2:
        if uploaded_file:
            st.session_state.uploaded_image = uploaded_file
            st.image(uploaded_file, width=160, use_container_width=False)
            
            if st.button("Run Feature Analysis", use_container_width=True):
                with st.spinner("Analyzing Facial Geometry..."):
                    results = detect_features(uploaded_file)
                    
                    features = [
                        ("face_shape", "Face Shape"),
                        ("skin_tone", "Skin Tone"),
                        ("bald_status", "Scalp Status"),
                        ("hair_type", "Hair Type")
                    ]
                    
                    tags_html = ""
                    for key, label in features:
                        if results.get(key):
                            val = str(results[key]).title()
                            st.session_state[key] = val
                            tags_html += f'<div class="feature-tag"><span class="tag-label">{label}</span><span class="tag-val">{val}</span></div>'
                    
                    st.markdown(f'<div class="detected-grid">{tags_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="upload-placeholder-info">
                <div class="info-title">Scan Face Features</div>
                <div class="info-desc">Upload a photo to detect face shape, skin undertone, and hair type automatically for instant personalized recommendations.</div>
            </div>
            ''', unsafe_allow_html=True)

# Main Chat Display
if not st.session_state.messages:
    st.markdown(f'''
    <div class="welcome-card">
        <div class="welcome-hero-icon">{SPARKLES_SVG}</div>
        <div class="welcome-heading">GlowUP AI Assistant</div>
        <div class="welcome-subheading">Elevate your hair, grooming, and clothing style choices with tailored AI analysis.</div>
        <div class="prompt-chips-container">
            <div class="prompt-chip">Best haircuts for my face shape</div>
            <div class="prompt-chip">Beard grooming & trimming routine</div>
            <div class="prompt-chip">Color matching outfit combinations</div>
            <div class="prompt-chip">Skincare routine for daily glow</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message-wrapper"><div class="chat-bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="assistant-message-wrapper">
                <div class="chat-bubble-assistant">
                    <div class="assistant-header-bar">
                        {SPARKLES_SVG}
                        <span class="assistant-name">GlowUP Engine</span>
                    </div>
                    <div class="assistant-body">{msg["content"]}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            if msg.get("sources"):
                tags = "".join([f'<span class="source-tag">{DOC_SVG} {s}</span>' for s in msg["sources"]])
                st.markdown(f'<div class="sources-bar"><span class="sources-title">Verified Sources</span> {tags}</div>', unsafe_allow_html=True)

# Chat Input & Streaming
if prompt := st.chat_input("Ask for style advice, haircuts, outfit pairings..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    response_placeholder = st.empty()
    with response_placeholder.container():
        st.markdown(f'''
        <div class="assistant-message-wrapper">
            <div class="chat-bubble-assistant pulsing-border">
                <div class="assistant-header-bar">
                    {SPARKLES_SVG}
                    <span class="assistant-name">GlowUP Engine</span>
                    <span class="typing-indicator">Analyzing parameters...</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    full_answer = ""
    sources = []

    try:
        for data in stream_rag_response(
            question=prompt,
            face_shape=st.session_state.get("face_shape"),
            skin_tone=st.session_state.get("skin_tone"),
            body_type=st.session_state.get("body_type"),
            hair_type=st.session_state.get("hair_type"),
            preferences=st.session_state.get("preferences"),
        ):
            if data.get("type") == "token":
                full_answer += data.get("content", "")
                response_placeholder.markdown(f'''
                <div class="assistant-message-wrapper">
                    <div class="chat-bubble-assistant">
                        <div class="assistant-header-bar">
                            {SPARKLES_SVG}
                            <span class="assistant-name">GlowUP Engine</span>
                        </div>
                        <div class="assistant-body">{full_answer}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            elif data.get("type") == "sources":
                sources = data.get("sources", [])

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_answer,
            "sources": sources
        })
        st.rerun()

    except Exception as e:
        st.error(f"Execution Error: {str(e)}")