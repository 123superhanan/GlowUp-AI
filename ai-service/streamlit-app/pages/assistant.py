import streamlit as st
from api import ask_glowup

def render_assistant():
    st.markdown('<h1>Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#8B8B8B;">Ask questions about your features</p>', unsafe_allow_html=True)
    
    # Show detected features
    col1, col2 = st.columns(2)
    with col1:
        face = st.session_state.get('face_shape', 'Not detected')
        conf_face = st.session_state.get('confidence_face', 0) * 100
        st.markdown(f'''
            <div class="result-card">
                <p class="label">Face Shape</p>
                <p class="value" style="font-size:20px;">{face}</p>
                <p class="confidence">{conf_face:.1f}% confidence</p>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        skin = st.session_state.get('skin_tone', 'Not detected')
        conf_skin = st.session_state.get('confidence_skin', 0) * 100
        st.markdown(f'''
            <div class="result-card">
                <p class="label">Skin Tone</p>
                <p class="value" style="font-size:20px;">{skin}</p>
                <p class="confidence">{conf_skin:.1f}% confidence</p>
            </div>
        ''', unsafe_allow_html=True)
    
    if face == 'Not detected':
        st.warning('Please analyze an image first on the Analyzer page.')
    
    st.divider()
    
    # Quick actions
    st.markdown('<p style="color:#8B8B8B;font-size:14px;">Quick questions</p>', unsafe_allow_html=True)
    
    quick_actions = ['Best Hairstyle', 'Best Beard', 'Glasses', 'Skin Care', 'Clothing Colors']
    cols = st.columns(len(quick_actions))
    
    for i, action in enumerate(quick_actions):
        with cols[i]:
            if st.button(action, key=f"quick_{i}"):
                st.session_state.quick_query = action
    
    # Chat input
    st.divider()
    
    # Display chat history
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f'''
                <div class="chat-user">
                    <p class="sender">You</p>
                    <p class="message">{msg['content']}</p>
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="chat-ai">
                    <p class="sender">GlowUp AI</p>
                    <p class="message">{msg['content']}</p>
                </div>
            ''', unsafe_allow_html=True)
    
    # Handle quick query
    if 'quick_query' in st.session_state and st.session_state.quick_query:
        query = st.session_state.quick_query
        st.session_state.quick_query = None
        
        if face != 'Not detected':
            with st.spinner('Thinking...'):
                result = ask_glowup(face, skin, query)
                if result["success"]:
                    data = result["data"]
                    response = data.get('response', 'No response generated.')
                    st.session_state.chat_history.append({'role': 'user', 'content': query})
                    st.session_state.chat_history.append({'role': 'ai', 'content': response})
                    st.rerun()
                else:
                    st.error(f'Error: {result.get("message", "Unknown error")}')
    
    # Chat input
    query = st.text_input(
        "Ask a question",
        placeholder="Example: What skincare routine works best?",
        label_visibility="collapsed",
        key="chat_input"
    )
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        send = st.button("Send", type="primary", use_container_width=True)
    
    if send and query:
        if face == 'Not detected':
            st.error('Please analyze an image first on the Analyzer page.')
        else:
            # Add user message
            st.session_state.chat_history.append({'role': 'user', 'content': query})
            
            with st.spinner('Generating response...'):
                result = ask_glowup(face, skin, query)
                
                if result["success"]:
                    data = result["data"]
                    response = data.get('response', 'No response generated.')
                    st.session_state.chat_history.append({'role': 'ai', 'content': response})
                    st.rerun()
                else:
                    st.session_state.chat_history.pop()
                    st.error(f'Error: {result.get("message", "Unknown error")}')
    
    # If no chat history, show placeholder
    if not st.session_state.chat_history and face != 'Not detected':
        st.markdown('''
            <div style="text-align:center;padding:40px 0;color:#8B8B8B;">
                <p>Ask me anything about your features</p>
                <p style="font-size:14px;">Try: Best hairstyle for my face shape</p>
            </div>
        ''', unsafe_allow_html=True)