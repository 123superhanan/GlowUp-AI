import streamlit as st
import requests

# Set page config
st.set_page_config(
    page_title="GlowUP AI | Personal Style Assistant",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0d0f12;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .main .block-container {
        max-width: 780px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    .header-title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 0.2rem;
    }

    .header-icon {
        width: 32px;
        height: 32px;
        fill: #818cf8;
    }

    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    .header-caption {
        color: #94a3b8;
        text-align: center;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    .chat-bubble-user {
        background-color: #1e293b;
        color: #f8fafc;
        padding: 14px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 12px 0 12px auto;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 1px solid #334155;
        font-size: 0.98rem;
        line-height: 1.5;
    }

    .chat-bubble-assistant {
        background-color: #161b22;
        color: #f1f5f9;
        padding: 16px 20px;
        border-radius: 18px 18px 18px 4px;
        margin: 12px 0;
        max-width: 88%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border: 1px solid #2d3748;
        font-size: 0.98rem;
        line-height: 1.6;
    }

    .assistant-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #818cf8;
        margin-bottom: 8px;
    }

    .bot-icon {
        width: 16px;
        height: 16px;
        fill: #818cf8;
    }

    .sources-container {
        margin-top: 10px;
        padding-top: 8px;
        border-top: 1px solid #27272a;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        align-items: center;
    }
    
    .sources-label {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .source-tag {
        background-color: #0f172a;
        color: #38bdf8;
        border: 1px solid #1e293b;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-family: monospace;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .doc-icon {
        width: 12px;
        height: 12px;
        fill: #38bdf8;
    }

    .stChatInputContainer {
        border-radius: 16px !important;
        border: 1px solid #334155 !important;
        background-color: #161b22 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# SVG Icons
SPARKLE_SVG = """<svg class="header-icon" viewBox="0 0 24 24"><path d="M12 2L14.39 8.26L20.65 10.65L14.39 13.04L12 19.3L9.61 13.04L3.35 10.65L9.61 8.26L12 2Z"/></svg>"""
BOT_SVG = """<svg class="bot-icon" viewBox="0 0 24 24"><path d="M12 2A2 2 0 0 1 14 4C14 4.74 13.6 5.39 13 5.73V7H14A7 7 0 0 1 21 14V16A3 3 0 0 1 18 19H16.8V20A2 2 0 0 1 14.8 22H9.2A2 2 0 0 1 7.2 20V19H6A3 3 0 0 1 3 16V14A7 7 0 0 1 10 7H11V5.73C10.4 5.39 10 4.74 10 4A2 2 0 0 1 12 2M7.5 13A1.5 1.5 0 0 0 6 14.5A1.5 1.5 0 0 0 7.5 16A1.5 1.5 0 0 0 9 14.5A1.5 1.5 0 0 0 7.5 13M16.5 13A1.5 1.5 0 0 0 15 14.5A1.5 1.5 0 0 0 16.5 16A1.5 1.5 0 0 0 18 14.5A1.5 1.5 0 0 0 16.5 13Z"/></svg>"""
DOC_SVG = """<svg class="doc-icon" viewBox="0 0 24 24"><path d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2M18 20H6V4H13V9H18V20Z"/></svg>"""

# Header
st.markdown(f'''
<div class="header-title-container">
    {SPARKLE_SVG}
    <div class="header-title">GlowUP AI</div>
</div>
<div class="header-caption">Your personal assistant for beard styles, haircuts, clothing colors & men's grooming.</div>
''', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="chat-bubble-assistant">
            <div class="assistant-header">{BOT_SVG} GlowUP Assistant</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(message["content"])

    if message.get("sources"):
        tags = "".join([f'<span class="source-tag">{DOC_SVG} {s}</span>' for s in message["sources"]])
        st.markdown(f'''
        <div class="sources-container">
            <span class="sources-label">Sources:</span> {tags}
        </div>
        ''', unsafe_allow_html=True)
# Chat input
if prompt := st.chat_input("Ask about hairstyles, face shapes, outfits..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-bubble-user">{prompt}</div>', unsafe_allow_html=True)

    with st.status("Generating response... This may take a few moments", expanded=True) as status:
        st.write("Searching style guides...")

        try:
            response = requests.post(
                "http://localhost:8000/ask",
                json={"question": prompt}
            )
            response.raise_for_status()
            data = response.json()

            answer = data.get("answer", "Sorry, I could not generate an answer.")
            sources = data.get("sources", [])

            status.update(label="Response ready", state="complete", expanded=False)

            # Save to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

            # ===== Safe Rendering =====
            st.markdown(f'''
            <div class="chat-bubble-assistant">
                <div class="assistant-header">{BOT_SVG} GlowUP Assistant</div>
            </div>
            ''', unsafe_allow_html=True)

            # Answer rendered safely
            st.markdown(answer)

            if sources:
                tags = "".join([f'<span class="source-tag">{DOC_SVG} {s}</span>' for s in sources])
                st.markdown(f'''
                <div class="sources-container">
                    <span class="sources-label">Sources:</span> {tags}
                </div>
                ''', unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            status.update(label="Connection failed", state="error")
            st.error("Unable to connect to the server. Please make sure the backend is running.")

        except Exception:
            status.update(label="Something went wrong", state="error")
            st.error("Something went wrong while generating the response. Please try again.")
    
   