import streamlit as st
from PIL import Image
import io
import time
from api import predict_face, predict_skin

def render_analyzer():
    st.markdown('<h1>Image Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#8B8B8B;">Upload a photo for AI analysis</p>', unsafe_allow_html=True)
    
    # File upload
    uploaded = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    if uploaded:
        # Display image
        image = Image.open(uploaded)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, use_container_width=True)
        
        with col2:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f'<p class="label">File Info</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="sub">Size: {image.width} x {image.height}</p>', unsafe_allow_html=True)
            
            file_size = uploaded.size / (1024 * 1024)
            st.markdown(f'<p class="sub">File: {file_size:.2f} MB</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Analyze Image"):
                try:
                    # Convert to bytes
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format='PNG')
                    img_data = img_bytes.getvalue()
                    
                    # Show loading
                    status_placeholder = st.empty()
                    status_placeholder.markdown('<p style="color:#8B8B8B;">Processing image...</p>', unsafe_allow_html=True)
                    
                    # Call both APIs
                    face_result = predict_face(img_data)
                    skin_result = predict_skin(img_data)
                    
                    status_placeholder.empty()
                    
                    if face_result["success"] and skin_result["success"]:
                        face_data = face_result["data"]
                        skin_data = skin_result["data"]
                        
                        # Extract predictions
                        face_pred = face_data.get('prediction', {})
                        skin_pred = skin_data.get('prediction', {})
                        
                        face_shape = face_pred.get('class', 'Unknown')
                        skin_tone = skin_pred.get('class', 'Unknown')
                        face_conf = face_pred.get('confidence', 0)
                        skin_conf = skin_pred.get('confidence', 0)
                        
                        # Save to session
                        st.session_state.face_shape = face_shape
                        st.session_state.skin_tone = skin_tone
                        st.session_state.confidence_face = face_conf
                        st.session_state.confidence_skin = skin_conf
                        
                        # Store recommendations
                        recs = face_data.get('recommendations', []) + skin_data.get('recommendations', [])
                        st.session_state.recommendations = recs
                        
                        # Save history
                        st.session_state.history.append({
                            'face': face_shape,
                            'skin': skin_tone,
                            'time': time.strftime('%H:%M'),
                            'date': time.strftime('%Y-%m-%d')
                        })
                        
                        # Display results
                        st.markdown('<h3>Results</h3>', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            conf_pct = face_conf * 100
                            bar_color = '#58A6FF'
                            st.markdown(f'''
                                <div class="result-card">
                                    <p class="label">Face Shape</p>
                                    <p class="value">{face_shape}</p>
                                    <p class="confidence">{conf_pct:.1f}% confidence</p>
                                    <div class="progress-bar">
                                        <div class="fill" style="width:{conf_pct}%;background:{bar_color};"></div>
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                        
                        with col2:
                            conf_pct = skin_conf * 100
                            bar_color = '#F0883E'
                            st.markdown(f'''
                                <div class="result-card">
                                    <p class="label">Skin Tone</p>
                                    <p class="value">{skin_tone}</p>
                                    <p class="confidence">{conf_pct:.1f}% confidence</p>
                                    <div class="progress-bar">
                                        <div class="fill" style="width:{conf_pct}%;background:{bar_color};"></div>
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                        
                        # Show recommendations
                        if recs:
                            st.markdown('<h3>Recommendations</h3>', unsafe_allow_html=True)
                            for rec in recs[:3]:
                                if isinstance(rec, dict):
                                    title = rec.get('query', '')
                                    content = rec.get('response', '')
                                    st.markdown(f'''
                                        <div class="result-card" style="border-left: 3px solid #58A6FF;">
                                            <p style="color:#58A6FF;font-weight:500;margin:0;">{title}</p>
                                            <p style="color:#C9D1D9;font-size:14px;margin:4px 0 0 0;">{content}</p>
                                        </div>
                                    ''', unsafe_allow_html=True)
                        else:
                            st.info('No recommendations available. Go to Assistant for personalized advice.')
                        
                    else:
                        error = face_result.get('message') or skin_result.get('message')
                        st.error(f'Error: {error}')
                        
                except Exception as e:
                    st.error(f'Error: {str(e)}')
    
    else:
        # Placeholder
        st.markdown('''
            <div class="upload-box">
                <p style="color:#8B8B8B;font-size:18px;">Drop your image here</p>
                <p style="color:#8B8B8B;font-size:14px;">Supports JPG, PNG</p>
            </div>
        ''', unsafe_allow_html=True)