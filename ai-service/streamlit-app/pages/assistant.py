import streamlit as st
from api import ask_glowup, USE_RAG
from styles import load_css

def render_assistant():
    load_css()
    
    st.markdown('<h1>Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#8B8B8B;">Get personalized recommendations</p>', unsafe_allow_html=True)

    # Show RAG status
    if USE_RAG:
        st.sidebar.success("RAG: Enabled")
    else:
        st.sidebar.info("RAG: Disabled (using mock recommendations)")

    if st.button("← Back to Home"):
        st.switch_page("app.py")

    # Show detected features
    col1, col2 = st.columns(2)

    with col1:
        face = st.session_state.get('face_shape', 'Not detected')
        st.markdown(f"""
            <div class="result-card">
                <p class="label">Face Shape</p>
                <p class="value" style="font-size:20px;">{face}</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        skin = st.session_state.get('skin_tone', 'Not detected')
        st.markdown(f"""
            <div class="result-card">
                <p class="label">Skin Tone</p>
                <p class="value" style="font-size:20px;">{skin}</p>
            </div>
        """, unsafe_allow_html=True)

    if face == 'Not detected':
        st.warning("Please analyze an image first on the Analyzer page.")

    st.divider()

    # Quick actions
    quick_actions = ['Best Hairstyle', 'Best Beard', 'Glasses', 'Skin Care', 'Makeup']
    cols = st.columns(len(quick_actions))
    for i, action in enumerate(quick_actions):
        with cols[i]:
            if st.button(action, key=f"q{i}"):
                st.session_state.quick_query = action

    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"""
                <div class="chat-user">
                    <p class="sender">You</p>
                    <p class="message">{msg['content']}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-ai">
                    <p class="sender">GlowUp AI</p>
                    <p class="message">{msg['content']}</p>
                </div>
            """, unsafe_allow_html=True)

    # Quick query handler
    if 'quick_query' in st.session_state and st.session_state.quick_query:
        query = st.session_state.quick_query
        st.session_state.quick_query = None
        
        if face != 'Not detected':
            with st.spinner("Thinking..."):
                result = ask_glowup(face, skin, query)
                
                if result["success"]:
                    response = result["data"].get('response', 'No response')
                    st.session_state.chat_history.append({'role': 'user', 'content': query})
                    st.session_state.chat_history.append({'role': 'ai', 'content': response})
                    st.rerun()
                else:
                    st.error(f"Error: {result.get('message')}")

    # Chat input
    query = st.text_input("Ask a question", placeholder="Example: Best hairstyle for me?", label_visibility="collapsed")

    if st.button("Send", type="primary") and query:
        if face == 'Not detected':
            st.error("Please analyze an image first.")
        else:
            st.session_state.chat_history.append({'role': 'user', 'content': query})
            with st.spinner("Generating response..."):
                result = ask_glowup(face, skin, query)
                
                if result["success"]:
                    response = result["data"].get('response', 'No response')
                    st.session_state.chat_history.append({'role': 'ai', 'content': response})
                    st.rerun()
                else:
                    st.session_state.chat_history.pop()
                    st.error(f"Error: {result.get('message')}")