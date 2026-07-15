import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* Main */
        .stApp {
            background: #0E1117;
        }
        
        .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Sidebar */
        .sidebar-brand {
            font-size: 24px;
            font-weight: 700;
            color: #FFFFFF;
            text-align: center;
            padding: 12px 0 4px 0;
        }
        
        .sidebar-sub {
            font-size: 14px;
            color: #8B8B8B;
            text-align: center;
            padding-bottom: 12px;
        }
        
        .status-online {
            color: #3FB950;
            font-size: 14px;
            padding: 8px 0;
        }
        
        .status-offline {
            color: #F85149;
            font-size: 14px;
            padding: 8px 0;
        }
        
        /* Headers */
        h1 {
            text-align: center;
            font-weight: 700;
            font-size: 28px;
            color: #FFFFFF;
        }
        
        h2 {
            font-weight: 600;
            font-size: 20px;
            color: #FFFFFF;
        }
        
        h3 {
            font-weight: 500;
            font-size: 16px;
            color: #C9D1D9;
        }
        
        /* Upload Box */
        .upload-box {
            border: 1px solid #30363D;
            border-radius: 12px;
            padding: 24px;
            background: #161B22;
            text-align: center;
        }
        
        /* Result Cards */
        .result-card {
            background: #161B22;
            border: 1px solid #30363D;
            border-radius: 12px;
            padding: 18px 20px;
            margin-top: 12px;
        }
        
        .result-card .label {
            color: #8B8B8B;
            font-size: 13px;
            margin: 0;
        }
        
        .result-card .value {
            color: #FFFFFF;
            font-size: 26px;
            font-weight: 700;
            margin: 4px 0;
        }
        
        .result-card .sub {
            color: #8B8B8B;
            font-size: 13px;
            margin: 0;
        }
        
        .result-card .confidence {
            color: #58A6FF;
            font-size: 14px;
            font-weight: 500;
        }
        
        /* Progress Bar */
        .progress-bar {
            width: 100%;
            height: 4px;
            background: #21262D;
            border-radius: 2px;
            margin-top: 8px;
            overflow: hidden;
        }
        
        .progress-bar .fill {
            height: 100%;
            border-radius: 2px;
            transition: width 0.4s ease;
        }
        
        /* Chat */
        .chat-user {
            background: #21262D;
            padding: 14px 18px;
            border-radius: 12px 12px 4px 12px;
            margin: 10px 0 10px 80px;
        }
        
        .chat-user .sender {
            color: #8B8B8B;
            font-size: 12px;
            margin-bottom: 4px;
        }
        
        .chat-user .message {
            color: #FFFFFF;
            margin: 0;
        }
        
        .chat-ai {
            background: #161B22;
            padding: 14px 18px;
            border-radius: 12px 12px 12px 4px;
            margin: 10px 80px 10px 0;
            border: 1px solid #30363D;
        }
        
        .chat-ai .sender {
            color: #58A6FF;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .chat-ai .message {
            color: #C9D1D9;
            margin: 0;
            line-height: 1.6;
        }
        
        .chat-ai .message strong {
            color: #FFFFFF;
        }
        
        .chat-ai .message ul {
            margin: 6px 0;
            padding-left: 20px;
        }
        
        .chat-ai .message li {
            margin: 4px 0;
        }
        
        /* Quick Actions */
        .quick-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin: 12px 0;
        }
        
        .quick-action {
            background: #21262D;
            border: 1px solid #30363D;
            border-radius: 20px;
            padding: 6px 16px;
            color: #C9D1D9;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .quick-action:hover {
            border-color: #58A6FF;
            background: #1C2333;
        }
        
        /* Buttons */
        .stButton > button {
            width: 100%;
            height: 46px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            background: #FA008A;
            color: #FFFFFF;
            border: none;
        }
        
        .stButton > button:hover {
            background: #2EA043;
        }
        
        .stButton > button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .stButton.secondary > button {
            background: #21262D;
            border: 1px solid #30363D;
            color: #C9D1D9;
        }
        
        .stButton.secondary > button:hover {
            background: #30363D;
        }
        
        /* Inputs */
        .stTextInput > div > div > input {
            border-radius: 10px;
            background: #161B22;
            border: 1px solid #30363D;
            color: #FFFFFF;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #58A6FF;
        }
        
        /* File Uploader */
        .stFileUploader > div {
            background: transparent;
        }
        
        .stFileUploader > div > div {
            border: 1px dashed #30363D;
            border-radius: 12px;
            padding: 24px;
            background: #161B22;
        }
        
        /* Divider */
        hr {
            border: none;
            border-top: 1px solid #21262D;
            margin: 20px 0;
        }
        
        /* Hide defaults */
        footer {
            visibility: hidden;
        }
        #MainMenu {
            visibility: hidden;
        }
        header {
            visibility: hidden;
        }
        
        /* Spacing */
        .mt-1 { margin-top: 8px; }
        .mt-2 { margin-top: 16px; }
        .mt-3 { margin-top: 24px; }
        .mb-1 { margin-bottom: 8px; }
        .mb-2 { margin-bottom: 16px; }
        
        /* Loading */
        .loading-dots::after {
            content: '...';
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        @keyframes dots {
            0% { content: ''; }
            25% { content: '.'; }
            50% { content: '..'; }
            75% { content: '...'; }
        }
    </style>
    """, unsafe_allow_html=True)