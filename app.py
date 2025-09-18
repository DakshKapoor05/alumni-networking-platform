import streamlit as st
from auth import AuthManager
from database import DatabaseManager
import pandas as pd
from datetime import datetime
import re

# Page config
st.set_page_config(
    page_title="Alumni Network",
    page_icon="🎓",
    layout="wide"
)

# Initialize managers
auth = AuthManager()
db = DatabaseManager()

def add_custom_css(theme_mode):
    """Add beautiful CSS styling with user-selectable theme"""
    
    # Define theme colors based on user selection
    if theme_mode == "Dark":
        theme_colors = {
            'bg_color': '#0f172a',
            'card_bg': '#1e293b',
            'text_primary': '#f8fafc',
            'text_secondary': '#cbd5e1',
            'text_muted': '#64748b',
            'border_color': '#374151',
            'success_bg': '#064e3b',
            'success_border': '#059669',
            'success_text': '#6ee7b7',
            'error_bg': '#7f1d1d',
            'error_border': '#dc2626',
            'error_text': '#fca5a5',
            'info_bg': '#1e3a8a',
            'info_text': '#93c5fd'
        }
    else:  # Light mode
        theme_colors = {
            'bg_color': '#f8fafc',
            'card_bg': '#ffffff',
            'text_primary': '#1f2937',
            'text_secondary': '#6b7280',
            'text_muted': '#9ca3af',
            'border_color': '#e5e7eb',
            'success_bg': '#ecfdf5',
            'success_border': '#10b981',
            'success_text': '#065f46',
            'error_bg': '#fef2f2',
            'error_border': '#ef4444',
            'error_text': '#991b1b',
            'info_bg': '#eff6ff',
            'info_text': '#1e40af'
        }
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling with user-selected theme */
    .stApp {{
        font-family: 'Inter', sans-serif;
        background-color: {theme_colors['bg_color']} !important;
        color: {theme_colors['text_primary']} !important;
    }}
    
    /* Force theme colors */
    .main {{
        background-color: {theme_colors['bg_color']} !important;
        color: {theme_colors['text_primary']} !important;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: {theme_colors['card_bg']} !important;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background-color: {theme_colors['card_bg']} !important;
        border-right: 1px solid {theme_colors['border_color']} !important;
    }}
    
    /* Override container backgrounds */
    [data-testid="stAppViewContainer"] {{
        background-color: {theme_colors['bg_color']} !important;
    }}
    
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    
    /* FIX: remove extra top padding */
    .main .block-container {{
        padding-top: 0rem !important;
        margin-top: 0rem !important;
        background-color: {theme_colors['bg_color']} !important;
    }}
    
    /* Hide default streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Main header gradient */
    .main-header {{
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white !important;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
    }}
    
    .main-header h1, .main-header p {{
        color: white !important;
    }}
    
    /* Feature cards */
    .feature-card {{
        background: {theme_colors['card_bg']} !important;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid {theme_colors['border_color']};
        height: 100%;
    }}
    
    .feature-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5p rgba(0, 0, 0, 0.15);
    }}
    
    .feature-card p {{
        color: {theme_colors['text_secondary']} !important;
    }}
    
    .feature-card h4 {{
        color: {theme_colors['text_primary']} !important;
    }}
    
    /* Beautiful buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }}
    
    .stButton > button:hover {{
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }}
    
    /* 🔥 THEME TOGGLE BUTTON - STYLED AS CIRCLE */
    .theme-button > button {{
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 1000 !important;
        width: 60px !important;
        height: 60px !important;
        background: {theme_colors['card_bg']} !important;
        border: 2px solid {theme_colors['border_color']} !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.8rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        padding: 0 !important;
        min-height: unset !important;
    }}
    
    .theme-button > button:hover {{
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
        background: {theme_colors['card_bg']} !important;
    }}
    
    .theme-button > button:active {{
        transform: translateY(-1px) scale(0.98) !important;
    }}
    
    /* SIDEBAR USER PROFILE */
    .sidebar-profile {{
        background: {theme_colors['card_bg']} !important;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid {theme_colors['border_color']};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    .sidebar-profile h3 {{
        color: {theme_colors['text_primary']} !important;
    }}
    
    .sidebar-profile p {{
        color: {theme_colors['text_secondary']} !important;
    }}
    
    /* Post cards */
    .post-card {{
        background: {theme_colors['card_bg']} !important;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid {theme_colors['border_color']};
        transition: all 0.3s ease;
    }}
    
    .post-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }}
    
    .post-card h4 {{
        color: {theme_colors['text_primary']} !important;
    }}
    
    .post-card p {{
        color: {theme_colors['text_secondary']} !important;
    }}
    
    /* Connection status styling */
    .connection-connected {{
        background: #10b981;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }}
    
    .connection-you {{
        background: #3b82f6;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }}
    
    /* Form styling */
    .stSelectbox > div > div {{
        background: {theme_colors['card_bg']} !important;
        border-radius: 10px;
        border: 2px solid {theme_colors['border_color']};
        color: {theme_colors['text_primary']} !important;
    }}
    
    .stTextInput > div > div > input {{
        background: {theme_colors['card_bg']} !important;
        border-radius: 10px;
        border: 2px solid {theme_colors['border_color']};
        font-family: 'Inter', sans-serif;
        color: {theme_colors['text_primary']} !important;
    }}
    
    .stTextArea textarea {{
        background: {theme_colors['card_bg']} !important;
        border-radius: 10px;
        border: 2px solid {theme_colors['border_color']};
        font-family: 'Inter', sans-serif;
        color: {theme_colors['text_primary']} !important;
    }}
    
    /* Success/Error messages */
    .stSuccess {{
        background: {theme_colors['success_bg']} !important;
        border: 1px solid {theme_colors['success_border']};
        border-radius: 10px;
        color: {theme_colors['success_text']} !important;
    }}
    
    .stError {{
        background: {theme_colors['error_bg']} !important;
        border: 1px solid {theme_colors['error_border']};
        border-radius: 10px;
        color: {theme_colors['error_text']} !important;
    }}
    
    .stInfo {{
        background: {theme_colors['info_bg']} !important;
        border: 1px solid {theme_colors['border_color']};
        border-radius: 10px;
        color: {theme_colors['info_text']} !important;
    }}
    
    /* Directory cards */
    .directory-card {{
        background: {theme_colors['card_bg']} !important;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid {theme_colors['border_color']};
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }}
    
    .directory-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }}
    
    .directory-card h4 {{
        color: {theme_colors['text_primary']} !important;
    }}
    
    .directory-card p {{
        color: {theme_colors['text_secondary']} !important;
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: {theme_colors['text_primary']} !important;
    }}
    
    /* All markdown text */
    .stMarkdown {{
        color: {theme_colors['text_primary']} !important;
    }}
    
    /* Metrics styling */
    [data-testid="metric-container"] {{
        background: {theme_colors['card_bg']} !important;
        border: 1px solid {theme_colors['border_color']};
        border-radius: 10px;
        padding: 1rem;
        color: {theme_colors['text_primary']} !important;
    }}
    
    /* Force theme colors for expanders */
    .streamlit-expanderHeader {{
        background: {theme_colors['card_bg']} !important;
        color: {theme_colors['text_primary']} !important;
    }}
    
    /* Links in posts */
    .post-content a {{
        color: #6366f1 !important;
        text-decoration: underline;
        font-weight: 500;
        transition: color 0.2s ease;
    }}
    
    .post-content a:hover {{
        color: #4338ca !important;
    }}
    
    /* Muted text */
    .text-muted {{
        color: {theme_colors['text_muted']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def render_theme_toggle():
    """Render working theme toggle button styled as circle"""
    
    theme_icon = "🌙" if st.session_state.theme_mode == "Light" else "☀️"
    
    # Create a container that won't interfere with the main content
    st.markdown('<div style="height: 1px;"></div>', unsafe_allow_html=True)
    
    # Create the theme toggle button with proper CSS class
    st.markdown(f'<div class="theme-button">', unsafe_allow_html=True)
    
    if st.button(theme_icon, key="theme_toggle_button", help="Toggle Theme"):
        st.session_state.theme_mode = "Dark" if st.session_state.theme_mode == "Light" else "Light"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def make_links_clickable(text):
    """Convert URLs in text to clickable links"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    
    def replace_url(match):
        url = match.group()
        return f'<a href="{url}" target="_blank" style="color: #6366f1; text-decoration: underline; font-weight: 500;">{url}</a>'
    
    return re.sub(url_pattern, replace_url, text)

def main():
    """Main application with USER-SELECTABLE THEMES"""
    
    # Initialize theme preference
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = "Light"
    
    # Apply custom CSS with current theme
    add_custom_css(st.session_state.theme_mode)
    
    # Initialize modal state
    if 'show_login_modal' not in st.session_state:
        st.session_state.show_login_modal = False
    if 'show_register_modal' not in st.session_state:
        st.session_state.show_register_modal = False
    
    # Authentication check
    if not auth.is_authenticated():
        # Check if modals should be shown
        if st.session_state.show_login_modal:
            show_login_modal()
        elif st.session_state.show_register_modal:
            show_register_modal()
        else:
            show_landing_page()
            
    else:
        # Beautiful main header for logged-in users
        st.markdown("""
        <div class="main-header">
            <h1 style="font-size: 3rem; margin: 0; font-weight: 700; color: white !important;">🎓 Alumni Network</h1>
            <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9; color: white !important;">Connect with Your Alumni Community</p>
        </div>
        """, unsafe_allow_html=True)
        
        show_main_app()

def show_landing_page():
    """Beautiful landing page with theme toggle"""
    
    # Header buttons
    header_col1, header_col2 = st.columns([3, 1])
    
    with header_col2:
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            if st.button("🔑 Login", key="header_login_btn", use_container_width=True):
                st.session_state.show_login_modal = True
                st.rerun()
        with button_col2:
            if st.button("📝 Register", key="header_register_btn", use_container_width=True):
                st.session_state.show_register_modal = True
                st.rerun()
    
    # Beautiful header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 1.5rem; margin: 0.5rem -1rem 1.5rem -1rem; text-align: center;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; color: white;">
                <span style="font-size: 2rem;">🎓</span>
                <h1 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: white !important;">Alumni Network</h1>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section
    text_color = "#f8fafc" if st.session_state.theme_mode == "Dark" else "#1f2937"
    subtitle_color = "#cbd5e1" if st.session_state.theme_mode == "Dark" else "#6b7280"
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        <h2 style="font-size: 2.5rem; font-weight: bold; color: {text_color} !important; margin-bottom: 0.5rem;">Connect with Your Alumni Community</h2>
        <p style="font-size: 1.2rem; color: {subtitle_color} !important; max-width: 600px; margin: 0 auto;">Reconnect with classmates, share experiences, and grow your professional network.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("### ✨ Why Join Our Alumni Network?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style="color: #6366f1; font-size: 2.5rem; margin-bottom: 1rem;">👥</div>
            <h4 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Network Building</h4>
            <p>Connect with alumni across different industries and graduation years to expand your professional network.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style="color: #6366f1; font-size: 2.5rem; margin-bottom: 1rem;">💼</div>
            <h4 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Career Opportunities</h4>
            <p>Discover job opportunities, mentorship programs, and career advice from experienced alumni.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div style="color: #6366f1; font-size: 2.5rem; margin-bottom: 1rem;">💬</div>
            <h4 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Community Engagement</h4>
            <p>Participate in discussions, share your experiences, and stay updated with alumni events.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 🔥 ADD THE WORKING THEME TOGGLE
    render_theme_toggle()

@st.dialog("🔑 Login to Your Account")
def show_login_modal():
    """LOGIN MODAL - STREAMLIT DIALOG VERSION"""
    
    # Close button
    if st.button("← Back to Home", key="close_login"):
        st.session_state.show_login_modal = False
        st.rerun()
    
    st.markdown("---")
    
    # Login form
    auth.login_form()
    
    st.markdown("---")
    
    # Switch to register
    if st.button("📝 Don't have an account? Register here", key="switch_to_register", use_container_width=True):
        st.session_state.show_login_modal = False
        st.session_state.show_register_modal = True
        st.rerun()

@st.dialog("📝 Create Your Account")  
def show_register_modal():
    """REGISTER MODAL - STREAMLIT DIALOG VERSION"""
    
    # Close button
    if st.button("← Back to Home", key="close_register"):
        st.session_state.show_register_modal = False
        st.rerun()
    
    st.markdown("---")
    
    # Register form
    show_register_form()
    
    st.markdown("---")
    
    # Switch to login
    if st.button("🔑 Already have an account? Login here", key="switch_to_login", use_container_width=True):
        st.session_state.show_register_modal = False
        st.session_state.show_login_modal = True
        st.rerun()

def show_register_form():
    """Beautiful register form"""
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name", placeholder="John")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Doe")
        
        email = st.text_input("Email", placeholder="john.doe@email.com")
        password = st.text_input("Password", placeholder="Create a password", type="password")
        
        col3, col4 = st.columns(2)
        
        with col3:
            current_year = datetime.now().year
            graduation_years = list(range(2000, current_year + 11))[::-1]
            graduation_year = st.selectbox("Graduation Year", 
                                         options=graduation_years, 
                                         index=graduation_years.index(2024) if 2024 in graduation_years else 0)
        
        with col4:
            majors = [
                "Computer Science", "Engineering", "Business Administration", "Psychology",
                "Biology", "Chemistry", "Physics", "Mathematics", "English", "History",
                "Art", "Music", "Economics", "Political Science", "Sociology", "Philosophy", "Other"
            ]
            major = st.selectbox("Major", options=majors, index=0)
        
        submit = st.form_submit_button("🚀 Create Account", use_container_width=True)
        
        if submit:
            if all([first_name, last_name, email, password, major]):
                result = db.create_user(
                    email=email, password=password,
                    first_name=first_name, last_name=last_name,
                    graduation_year=int(graduation_year), major=major
                )
                if result["success"]:
                    st.success("🎉 Registration successful! Please login.")
                    st.session_state.show_register_modal = False
                    st.session_state.show_login_modal = True
                    st.rerun()
                else:
                    st.error(f"❌ Registration failed: {result['message']}")
            else:
                st.error("⚠️ Please fill in all fields")

def show_main_app():
    """Show main application after authentication with theme toggle"""
    user = auth.get_current_user()
    
    # BEAUTIFUL SIDEBAR
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-profile">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎓</div>
            <h3 style="margin: 0;">{user['first_name']} {user['last_name']}</h3>
            <p style="margin: 0.5rem 0;">Class of {user['graduation_year']}</p>
            <p style="margin: 0;">{user['major']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Navigation header
        st.markdown("**🧭 Navigate:**")
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard"
        
        # Navigation buttons
        if st.button("🏠 Dashboard", use_container_width=True, 
                    type="primary" if st.session_state.current_page == "Dashboard" else "secondary"):
            st.session_state.current_page = "Dashboard"
            st.rerun()
        
        if st.button("👥 Alumni Directory", use_container_width=True,
                    type="primary" if st.session_state.current_page == "Alumni Directory" else "secondary"):
            st.session_state.current_page = "Alumni Directory"
            st.rerun()
        
        if st.button("🔔 Connection Requests", use_container_width=True,
                    type="primary" if st.session_state.current_page == "Connection Requests" else "secondary"):
            st.session_state.current_page = "Connection Requests"
            st.rerun()
        
        if st.button("👤 My Profile", use_container_width=True,
                    type="primary" if st.session_state.current_page == "My Profile" else "secondary"):
            st.session_state.current_page = "My Profile"
            st.rerun()
        
        if st.button("🔗 My Connections", use_container_width=True,
                    type="primary" if st.session_state.current_page == "My Connections" else "secondary"):
            st.session_state.current_page = "My Connections"
            st.rerun()
        
        page = st.session_state.current_page
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
    
    # 🔥 ADD THE WORKING THEME TOGGLE FOR MAIN APP
    render_theme_toggle()
    
    # Main content
    if page == "Dashboard":
        show_dashboard()
    elif page == "Alumni Directory":
        show_directory()
    elif page == "My Profile":
        show_profile()
    elif page == "My Connections":
        show_connections()
    elif page == "Connection Requests":
        show_connection_requests()

def show_dashboard():
    """Beautiful dashboard"""
    st.markdown("## 🏠 Dashboard")
    
    with st.expander("✍️ Create New Post", expanded=False):
        with st.form("create_post"):
            content = st.text_area("What's on your mind?", height=100, 
                                 placeholder="Share your thoughts... You can include links like https://example.com")
            submit = st.form_submit_button("📤 Post", use_container_width=True)
            
            if submit and content:
                user = auth.get_current_user()
                result = db.create_post(user['id'], content)
                
                if result["success"]:
                    st.success("✅ " + result["message"])
                    st.rerun()
                else:
                    st.error("❌ " + result["message"])
    
    st.markdown("### 📰 Recent Posts")
    
    posts_df = db.get_all_posts()
    
    if not posts_df.empty:
        for idx, post in posts_df.iterrows():
            st.markdown(f"""
            <div class="post-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <h4 style="margin: 0; font-weight: 600;">{post['first_name']} {post['last_name']}</h4>
                        <p style="margin: 0; font-size: 0.9rem;">Class of {post['graduation_year']}</p>
                    </div>
                    <span class="text-muted" style="font-size: 0.8rem;">{post['created_at'][:10]}</span>
                </div>
                <div class="post-content">
                    <p style="margin: 0; line-height: 1.6;">{make_links_clickable(post['content'])}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📝 No posts yet. Be the first to share something!")

def show_directory():
    """🔥 LINKEDIN-STYLE Alumni Directory - INCLUDING CURRENT USER AS 'YOU'"""
    st.markdown("## 👥 Alumni Directory")
    
    col1, col2 = st.columns(2)
    with col1:
        majors = [
            "All", "Computer Science", "Engineering", "Business Administration", "Psychology",
            "Biology", "Chemistry", "Physics", "Mathematics", "English", "History",
            "Art", "Music", "Economics", "Political Science", "Sociology", "Philosophy", "Other"
        ]
        selected_major = st.selectbox("🎯 Search by major", options=majors, index=0)
        
    with col2:
        graduation_year = st.selectbox("📅 Filter by graduation year", 
                                     ["All"] + list(range(2010, 2025)))
    
    search_term = "" if selected_major == "All" else selected_major
    
    if graduation_year == "All":
        graduation_year = None
    
    users_df = db.search_users(search_term, graduation_year)
    current_user = auth.get_current_user()
    
    if not users_df.empty:
        st.markdown(f"### 🔍 Found {len(users_df)} alumni")
        
        for idx, user in users_df.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="directory-card">
                    <h4 style="margin: 0 0 0.5rem 0;">{user['first_name']} {user['last_name']}</h4>
                    <p style="margin: 0;">🎓 Class of {user['graduation_year']} • 📚 {user['major']}</p>
                    <p class="text-muted" style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">Joined: {user['created_at'][:10]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.write("")  # Spacer
            
            with col3:
                # 🔥 CHECK IF THIS IS THE CURRENT USER - SHOW AS "YOU"
                if user['id'] == current_user['id']:
                    st.markdown('<div class="connection-you">👤 You</div>', unsafe_allow_html=True)
                else:
                    # 🔥 CHECK CONNECTION STATUS (LinkedIn-style)
                    connection_status = db.check_connection_status(current_user['id'], user['id'])
                    
                    if connection_status == "connected":
                        st.markdown('<div class="connection-connected">✅ Connected</div>', unsafe_allow_html=True)
                    elif connection_status == "pending_sent":
                        st.markdown('<div style="background: #f59e0b; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; text-align: center;">⏳ Pending</div>', unsafe_allow_html=True)
                    elif connection_status == "pending_received":
                        st.markdown('<div style="background: #8b5cf6; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; text-align: center;">📨 Respond</div>', unsafe_allow_html=True)
                    else:
                        if st.button(f"🔗 Connect", key=f"connect_{user['id']}", use_container_width=True):
                            # 🔥 SHOW CONNECTION REQUEST MODAL
                            st.session_state[f'show_connect_modal_{user["id"]}'] = True
                            st.rerun()
                    
                    # 🔥 CONNECTION REQUEST MODAL
                    if st.session_state.get(f'show_connect_modal_{user["id"]}', False):
                        show_connection_request_modal(user)
    else:
        st.info("🔍 No alumni found with the current search criteria")

@st.dialog("🔗 Send Connection Request")
def show_connection_request_modal(target_user):
    """🔥 LINKEDIN-STYLE Connection Request Modal"""
    
    st.markdown(f"### Connect with {target_user['first_name']} {target_user['last_name']}")
    st.markdown(f"**Class of {target_user['graduation_year']} • {target_user['major']}**")
    
    with st.form("connection_request_form"):
        message = st.text_area("Add a personal message (optional)", 
                             placeholder="Hi! I'd like to connect with you on Alumni Network.",
                             max_chars=300)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("✅ Send Request", use_container_width=True):
                current_user = auth.get_current_user()
                result = db.send_connection_request(current_user['id'], target_user['id'], message)
                
                if result["success"]:
                    st.success("🎉 " + result["message"])
                    st.session_state[f'show_connect_modal_{target_user["id"]}'] = False
                    st.rerun()
                else:
                    st.error("❌ " + result["message"])
        
        with col2:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state[f'show_connect_modal_{target_user["id"]}'] = False
                st.rerun()

def show_connection_requests():
    """🔥 LINKEDIN-STYLE Connection Requests Page"""
    st.markdown("## 🔔 Connection Requests")
    
    current_user = auth.get_current_user()
    
    tab1, tab2 = st.tabs(["📥 Received Requests", "📤 Sent Requests"])
    
    with tab1:
        st.markdown("### 📥 Requests You've Received")
        
        received_requests = db.get_connection_requests(current_user['id'], "received")
        
        if not received_requests.empty:
            for idx, request in received_requests.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="directory-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h4 style="margin: 0 0 0.5rem 0;">{request['first_name']} {request['last_name']}</h4>
                                <p style="margin: 0;">🎓 Class of {request['graduation_year']} • 📚 {request['major']}</p>
                                {f'<p style="margin: 0.5rem 0; font-style: italic;">"{request["message"]}"</p>' if request['message'] else ''}
                                <p class="text-muted" style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">Sent: {request['created_at'][:10]}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ Accept", key=f"accept_{request['request_id']}", use_container_width=True):
                            result = db.accept_connection_request(request['request_id'])
                            if result["success"]:
                                st.success("🎉 " + result["message"])
                                st.rerun()
                            else:
                                st.error("❌ " + result["message"])
                    
                    with col2:
                        if st.button(f"❌ Decline", key=f"reject_{request['request_id']}", use_container_width=True):
                            result = db.reject_connection_request(request['request_id'])
                            if result["success"]:
                                st.info("ℹ️ " + result["message"])
                                st.rerun()
                            else:
                                st.error("❌ " + result["message"])
                    
                    st.markdown("---")
        else:
            st.info("📭 No pending connection requests!")
    
    with tab2:
        st.markdown("### 📤 Requests You've Sent")
        
        sent_requests = db.get_connection_requests(current_user['id'], "sent")
        
        if not sent_requests.empty:
            for idx, request in sent_requests.iterrows():
                st.markdown(f"""
                <div class="directory-card">
                    <h4 style="margin: 0 0 0.5rem 0;">{request['first_name']} {request['last_name']}</h4>
                    <p style="margin: 0;">🎓 Class of {request['graduation_year']} • 📚 {request['major']}</p>
                    {f'<p style="margin: 0.5rem 0; font-style: italic;">Your message: "{request["message"]}"</p>' if request['message'] else ''}
                    <p class="text-muted" style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">Sent: {request['created_at'][:10]}</p>
                    <div style="background: #f59e0b; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; text-align: center; width: fit-content; margin-top: 0.5rem;">⏳ Awaiting Response</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📤 No sent requests!")

def show_profile():
    """Beautiful user profile"""
    user = auth.get_current_user()
    st.markdown(f"## 👤 {user['first_name']} {user['last_name']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Profile Information")
        st.markdown(f"""
        <div class="feature-card">
            <p><strong>📧 Email:</strong> {user['email']}</p>
            <p><strong>🎓 Graduation Year:</strong> {user['graduation_year']}</p>
            <p><strong>📚 Major:</strong> {user['major']}</p>
            <p><strong>📅 Member Since:</strong> {user['created_at'][:10]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        
        user_posts = db.get_user_posts(user['id'])
        posts_count = len(user_posts) if not user_posts.empty else 0
        
        user_connections = db.get_user_connections(user['id'])
        connections_count = len(user_connections) if not user_connections.empty else 0
        
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.metric("📝 Posts", posts_count)
        with col2_2:
            st.metric("🔗 Connections", connections_count)
    
    st.markdown("### 📝 My Posts")
    if not user_posts.empty:
        for idx, post in user_posts.iterrows():
            st.markdown(f"""
            <div class="post-card">
                <div class="post-content">
                    <p style="margin: 0; line-height: 1.6;">{make_links_clickable(post['content'])}</p>
                </div>
                <p class="text-muted" style="margin-top: 1rem; font-size: 0.8rem;">Posted: {post['created_at'][:10]}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📝 You haven't posted anything yet!")

def show_connections():
    """Beautiful connections page"""
    st.markdown("## 🔗 My Connections")
    user = auth.get_current_user()
    
    connections_df = db.get_user_connections(user['id'])
    
    if not connections_df.empty:
        st.markdown(f"### 👥 You have {len(connections_df)} connections")
        
        for idx, connection in connections_df.iterrows():
            st.markdown(f"""
            <div class="directory-card" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0 0 0.5rem 0;">{connection['first_name']} {connection['last_name']}</h4>
                    <p style="margin: 0;">🎓 Class of {connection['graduation_year']} • 📚 {connection.get('major', 'N/A')}</p>
                </div>
                <div style="text-align: right;">
                    <p class="text-muted" style="margin: 0; font-size: 0.8rem;">Connected: {connection['created_at'][:10]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔗 You don't have any connections yet. Visit the Alumni Directory to connect with other alumni!")

if __name__ == "__main__":
    main()
