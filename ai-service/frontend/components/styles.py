import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* -----------------------------------------------------------------
           1. Core Application Canvas & Typography
        ------------------------------------------------------------------- */
        .stApp {
            background: #080a0f;
            color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Plus Jakarta Sans", sans-serif;
        }

        /* Hide Streamlit Default Chrome & Navigation */
        #MainMenu, footer, header { visibility: hidden; }
        [data-testid="stSidebarNav"] { display: none !important; }

        /* -----------------------------------------------------------------
           2. Sidebar Styling & Navigation Links
        ------------------------------------------------------------------- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d0f12 0%, #161b22 100%);
            border-right: 1px solid #1e293b;
        }

        /* Sidebar Header Component */
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
            animation: float 3s ease-in-out infinite;
        }

        .sidebar-title {
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .sidebar-subtitle {
            color: #94a3b8;
            font-size: 0.85rem;
            margin-top: 4px;
            letter-spacing: 1px;
        }

        .sidebar-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(30, 41, 59, 0.8);
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
            animation: pulse 2s infinite;
        }

        .sidebar-section-title {
            color: #94a3b8;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding-bottom: 10px;
            border-bottom: 1px solid #1e293b;
            margin-bottom: 14px;
        }

        /* st.page_link Overrides */
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
            background: transparent;
            border: 1px solid transparent;
            border-radius: 12px;
            padding: 10px 16px;
            margin: 4px 0;
            transition: all 0.3s ease;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
            background: rgba(30, 41, 59, 0.7);
            border-color: #334155;
            transform: translateX(4px);
        }

        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p {
            color: #94a3b8 !important;
            font-weight: 500;
            font-size: 0.95rem;
            transition: color 0.3s ease;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover p {
            color: #f8fafc !important;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(99, 102, 241, 0.15)) !important;
            border: 1px solid rgba(99, 102, 241, 0.4) !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
        }

        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] p {
            color: #e2e8f0 !important;
            font-weight: 700;
        }

        /* -----------------------------------------------------------------
           3. Banners & Glassmorphism Components
        ------------------------------------------------------------------- */
        .chat-header-banner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 1.5rem;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .banner-title-group {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .banner-title {
            font-size: 1.25rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .banner-badge {
            background: rgba(99, 102, 241, 0.15);
            color: #818cf8;
            border: 1px solid rgba(99, 102, 241, 0.3);
            font-size: 0.72rem;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            letter-spacing: 0.03em;
        }

        /* Expander & File Upload UI */
        [data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.4) !important;
            border: 1px solid rgba(99, 102, 241, 0.2) !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
        }

        [data-testid="stFileUploadDropzone"] {
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1px dashed rgba(99, 102, 241, 0.4) !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stFileUploadDropzone"]:hover {
            border-color: #818cf8 !important;
            background: rgba(30, 27, 75, 0.4) !important;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
        }

        /* -----------------------------------------------------------------
           4. Welcome & Prompt Cards
        ------------------------------------------------------------------- */
        .welcome-card {
            text-align: center;
            padding: 4.5rem 2rem;
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.6) 0%, rgba(8, 10, 15, 0) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 24px;
            margin: 2rem 0;
        }

        .welcome-hero-icon {
            width: 56px;
            height: 56px;
            margin: 0 auto 1.5rem auto;
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.25);
        }

        .welcome-heading {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.03em;
        }

        .welcome-subheading {
            color: #94a3b8;
            font-size: 0.95rem;
            max-width: 500px;
            margin: 0.75rem auto 2.5rem auto;
            line-height: 1.6;
        }

        .prompt-chips-container {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            max-width: 700px;
            margin: 0 auto;
        }

        .prompt-chip {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.25);
            padding: 10px 18px;
            border-radius: 30px;
            font-size: 0.82rem;
            color: #cbd5e1;
            transition: all 0.25s ease;
            cursor: pointer;
        }

        .prompt-chip:hover {
            border-color: #818cf8;
            background: rgba(30, 27, 75, 0.8);
            color: #ffffff;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
            transform: translateY(-2px);
        }

        /* -----------------------------------------------------------------
           5. Chat Interface & Bubbles
        ------------------------------------------------------------------- */
        .user-message-wrapper {
            display: flex;
            justify-content: flex-end;
            margin: 1rem 0;
        }

        .chat-bubble-user {
            background: linear-gradient(135deg, #312e81 0%, #1e1b4b 100%);
            color: #f8fafc;
            padding: 14px 20px;
            border-radius: 18px 18px 4px 18px;
            max-width: 72%;
            border: 1px solid rgba(129, 140, 248, 0.3);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            font-size: 0.92rem;
            line-height: 1.55;
            animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .assistant-message-wrapper {
            display: flex;
            justify-content: flex-start;
            margin: 1rem 0;
        }

        .chat-bubble-assistant {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(8px);
            color: #e2e8f0;
            padding: 18px 22px;
            border-radius: 18px 18px 18px 4px;
            max-width: 82%;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            font-size: 0.93rem;
            line-height: 1.6;
            animation: slideInLeft 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .assistant-header-bar {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .assistant-name {
            font-size: 0.78rem;
            font-weight: 700;
            color: #818cf8;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        /* Sources Section */
        .sources-bar {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: -4px 0 16px 0;
            padding-left: 4px;
        }

        .source-tag {
            background: rgba(15, 23, 42, 0.9);
            color: #818cf8;
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.72rem;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-weight: 500;
        }

        /* -----------------------------------------------------------------
           6. Buttons & Animations
        ------------------------------------------------------------------- */
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }

        .stButton > button:hover {
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5) !important;
            transform: translateY(-1px);
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(30px); }
            to { opacity: 1; transform: translateX(0); }
        }

        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
    """, unsafe_allow_html=True)