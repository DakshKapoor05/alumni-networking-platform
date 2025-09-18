#import streamlit as st
# from auth import AuthManager
# from database import DatabaseManager
# import pandas as pd
# from datetime import datetime
# import re


# # Page config
# st.set_page_config(
#     page_title="Alumni Network",
#     page_icon="🎓"
# )


# # Initialize managers
# auth = AuthManager()
# db = DatabaseManager()


# def make_links_clickable(text):
#     """Convert URLs in text to clickable links"""
#     # Regular expression to find URLs
#     url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    
#     # Replace URLs with clickable links
#     def replace_url(match):
#         url = match.group()
#         return f'<a href="{url}" target="_blank" style="color: #1f77b4; text-decoration: underline;">{url}</a>'
    
#     return re.sub(url_pattern, replace_url, text)


# def main():
#     """Main application"""
    
#     # Custom CSS - Clean version
#     st.markdown("""
#     <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: bold;
#         text-align: center;
#         color: #1f77b4;
#         margin-bottom: 2rem;
#     }
#     </style>
#     """, unsafe_allow_html=True)
    
#     # Header
#     st.markdown('<h1 class="main-header">🎓 Alumni Network</h1>', unsafe_allow_html=True)
    
#     # Authentication check
#     if not auth.is_authenticated():
#         # Show login/register tabs
#         tab1, tab2 = st.tabs(["Login", "Register"])
        
#         with tab1:
#             auth.login_form()
        
#         with tab2:
#             # Custom register form with dropdowns
#             show_register_form()
            
#     else:
#         # Show main app
#         show_main_app()


# def show_register_form():
#     """Register form with dropdowns"""
#     st.subheader("Create Account")
    
#     with st.form("register_form"):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             first_name = st.text_input("First Name", placeholder="John")
#         with col2:
#             last_name = st.text_input("Last Name", placeholder="Doe")
        
#         email = st.text_input("Email", placeholder="john.doe@email.com")
#         password = st.text_input("Password", placeholder="Create a password", type="password")
        
#         col3, col4 = st.columns(2)
        
#         with col3:
#             # Graduation year dropdown
#             current_year = datetime.now().year
#             graduation_years = list(range(2000, current_year + 11))[::-1]  # Reverse for newest first
#             graduation_year = st.selectbox("Graduation Year", 
#                                          options=graduation_years, 
#                                          index=graduation_years.index(2024) if 2024 in graduation_years else 0)
        
#         with col4:
#             # Major dropdown
#             majors = [
#                 "Computer Science", "Engineering", "Business Administration", "Psychology",
#                 "Biology", "Chemistry", "Physics", "Mathematics", "English", "History",
#                 "Art", "Music", "Economics", "Political Science", "Sociology", "Philosophy", "Other"
#             ]
#             major = st.selectbox("Major", options=majors, index=0)
        
#         submit = st.form_submit_button("Create Account", use_container_width=True)
        
#         if submit:
#             if all([first_name, last_name, email, password, major]):
#                 result = db.create_user(
#                     email=email, password=password,
#                     first_name=first_name, last_name=last_name,
#                     graduation_year=int(graduation_year), major=major
#                 )
#                 if result["success"]:
#                     st.success("Registration successful! Please login.")
#                 else:
#                     st.error(f"Registration failed: {result['message']}")
#             else:
#                 st.error("Please fill in all fields")


# def show_main_app():
#     """Show main application after authentication"""
#     user = auth.get_current_user()
    
#     # Sidebar navigation
#     with st.sidebar:
#         st.markdown(f"""
#     <div style="text-align: center; padding: 15px; background-color: var(--background-color); border-radius: 10px; margin-bottom: 20px;">
#         <div style="font-size: 50px; margin-bottom: 10px;">🎓</div>
#         <h3>{user['first_name']} {user['last_name']}</h3>
#         <p>Class of {user['graduation_year']}</p>
#         <p>{user['major']}</p>
#     </div>
#     """, unsafe_allow_html=True)

#         st.write("---")
        
#         # NAVIGATION WITH BUTTONS INSTEAD OF DROPDOWN
#         st.markdown("**Navigate:**")
        
#         # Initialize page state
#         if 'current_page' not in st.session_state:
#             st.session_state.current_page = "Dashboard"
        
#         # Navigation buttons
#         if st.button("🏠 Dashboard", use_container_width=True, 
#                     type="primary" if st.session_state.current_page == "Dashboard" else "secondary"):
#             st.session_state.current_page = "Dashboard"
#             st.rerun()
        
#         if st.button("👥 Alumni Directory", use_container_width=True,
#                     type="primary" if st.session_state.current_page == "Alumni Directory" else "secondary"):
#             st.session_state.current_page = "Alumni Directory"
#             st.rerun()
        
#         if st.button("👤 My Profile", use_container_width=True,
#                     type="primary" if st.session_state.current_page == "My Profile" else "secondary"):
#             st.session_state.current_page = "My Profile"
#             st.rerun()
        
#         if st.button("🔗 My Connections", use_container_width=True,
#                     type="primary" if st.session_state.current_page == "My Connections" else "secondary"):
#             st.session_state.current_page = "My Connections"
#             st.rerun()
        
#         # Use session state for page
#         page = st.session_state.current_page
        
#         st.write("---")
#         if st.button("Logout", use_container_width=True):
#             auth.logout()
    
#     # Main content based on navigation
#     if page == "Dashboard":
#         show_dashboard()
#     elif page == "Alumni Directory":
#         show_directory()
#     elif page == "My Profile":
#         show_profile()
#     elif page == "My Connections":
#         show_connections()


# def show_dashboard():
#     """Dashboard with posts and create post - WITH CLICKABLE LINKS"""
#     st.header("🏠 Dashboard")
    
#     # Create post section
#     with st.expander("✍️ Create New Post", expanded=False):
#         with st.form("create_post"):
#             content = st.text_area("What's on your mind?", height=100, 
#                                  placeholder="Share your thoughts... You can include links like https://example.com")
#             submit = st.form_submit_button("Post")
            
#             if submit and content:
#                 user = auth.get_current_user()
#                 result = db.create_post(user['id'], content)
                
#                 if result["success"]:
#                     st.success(result["message"])
#                     st.rerun()
#                 else:
#                     st.error(result["message"])
    
#     # Display all posts
#     st.subheader("📰 Recent Posts")
    
#     posts_df = db.get_all_posts()
    
#     if not posts_df.empty:
#         # Display posts WITH CLICKABLE LINKS
#         for idx, post in posts_df.iterrows():
#             with st.container():
#                 col1, col2 = st.columns([4, 1])
                
#                 with col1:
#                     st.markdown(f"**{post['first_name']} {post['last_name']}** *(Class of {post['graduation_year']})*")
                    
#                     # 🔥 MAKE LINKS CLICKABLE - Convert URLs to clickable links
#                     content_with_links = make_links_clickable(post['content'])
#                     st.markdown(f"📝 {content_with_links}", unsafe_allow_html=True)
                    
#                     st.caption(f"Posted: {post['created_at'][:10]}")
                
#                 with col2:
#                     # Optional: Add like/share buttons here later
#                     pass
                
#                 st.divider()
#     else:
#         st.info("No posts yet. Be the first to share something!")


# def show_directory():
#     """Alumni directory with search - WITH CONNECTION STATUS CHECK"""
#     st.header("👥 Alumni Directory")
    
#     # Search filters - BOTH DROPDOWNS NOW
#     col1, col2 = st.columns(2)
#     with col1:
#         # Major dropdown (same as register page)
#         majors = [
#             "All", "Computer Science", "Engineering", "Business Administration", "Psychology",
#             "Biology", "Chemistry", "Physics", "Mathematics", "English", "History",
#             "Art", "Music", "Economics", "Political Science", "Sociology", "Philosophy", "Other"
#         ]
#         selected_major = st.selectbox("Search by major", options=majors, index=0)
        
#     with col2:
#         graduation_year = st.selectbox("Filter by graduation year", 
#                                      ["All"] + list(range(2010, 2025)))
    
#     # Get users based on filters
#     search_term = "" if selected_major == "All" else selected_major
    
#     if graduation_year == "All":
#         graduation_year = None
    
#     users_df = db.search_users(search_term, graduation_year)
#     current_user = auth.get_current_user()
    
#     # 🔥 GET USER'S CONNECTIONS TO CHECK STATUS
#     user_connections = db.get_user_connections(current_user['id'])
#     connected_user_ids = set()
#     if not user_connections.empty:
#         connected_user_ids = set(user_connections['id'].tolist())
    
#     if not users_df.empty:
#         st.subheader(f"Found {len(users_df)} alumni")
        
#         # Display users in cards
#         for idx, user in users_df.iterrows():
#             col1, col2, col3 = st.columns([3, 1, 1])
            
#             with col1:
#                 st.write(f"**{user['first_name']} {user['last_name']}**")
#                 st.write(f"Class of {user['graduation_year']} • {user['major']}")
            
#             with col2:
#                 st.write(f"Joined: {user['created_at'][:10]}")
            
#             with col3:
#                 if user['id'] != current_user['id']:
#                     # 🔥 CHECK CONNECTION STATUS
#                     if user['id'] in connected_user_ids:
#                         # Already connected - show status
#                         st.success("✅ Connected")
#                     else:
#                         # Not connected - show connect button
#                         if st.button(f"Connect", key=f"connect_{user['id']}"):
#                             result = db.create_connection(current_user['id'], user['id'])
#                             if result["success"]:
#                                 st.success(result["message"])
#                                 st.rerun()
#                             else:
#                                 st.error(result["message"])
#                 else:
#                     # Current user - show "You"
#                     st.info("👤 You")
            
#             st.write("---")
#     else:
#         st.info("No alumni found with the current search criteria")


# def show_profile():
#     """User profile page - WITH CLICKABLE LINKS IN POSTS"""
#     user = auth.get_current_user()
#     st.header(f"👤 {user['first_name']} {user['last_name']}")
    
#     # User info
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("Profile Information")
#         st.write(f"**Email:** {user['email']}")
#         st.write(f"**Graduation Year:** {user['graduation_year']}")
#         st.write(f"**Major:** {user['major']}")
#         st.write(f"**Member Since:** {user['created_at'][:10]}")
    
#     with col2:
#         st.subheader("Quick Stats")
        
#         # Get user's posts count
#         user_posts = db.get_user_posts(user['id'])
#         posts_count = len(user_posts) if not user_posts.empty else 0
        
#         # Get connections count
#         user_connections = db.get_user_connections(user['id'])
#         connections_count = len(user_connections) if not user_connections.empty else 0
        
#         st.metric("Posts", posts_count)
#         st.metric("Connections", connections_count)
    
#     # User's posts WITH CLICKABLE LINKS
#     st.subheader("My Posts")
#     if not user_posts.empty:
#         for idx, post in user_posts.iterrows():
#             with st.container():
#                 # 🔥 MAKE LINKS CLICKABLE in user profile too
#                 content_with_links = make_links_clickable(post['content'])
#                 st.markdown(f"📝 {content_with_links}", unsafe_allow_html=True)
#                 st.caption(f"Posted: {post['created_at'][:10]}")
#                 st.divider()
#     else:
#         st.info("You haven't posted anything yet!")


# def show_connections():
#     """User connections page - SHOWS MAJOR INFO"""
#     st.header("🔗 My Connections")
#     user = auth.get_current_user()
    
#     connections_df = db.get_user_connections(user['id'])
    
#     if not connections_df.empty:
#         st.subheader(f"You have {len(connections_df)} connections")
        
#         for idx, connection in connections_df.iterrows():
#             col1, col2 = st.columns([3, 1])
            
#             with col1:
#                 st.write(f"**{connection['first_name']} {connection['last_name']}**")
#                 # 🔥 SHOWS GRADUATION YEAR AND MAJOR
#                 st.write(f"🎓 Class of {connection['graduation_year']} • 📚 {connection.get('major', 'N/A')}")
            
#             with col2:
#                 st.write(f"Connected: {connection['created_at'][:10]}")
            
#             st.write("---")
#     else:
#         st.info("You don't have any connections yet. Visit the Alumni Directory to connect with other alumni!")


# if __name__ == "__main__":
#     main()


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


def add_custom_css():
    """Add beautiful CSS styling - CLEAN STABLE VERSION"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }
    
    /* FIX: remove extra top padding */
    .main .block-container {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main header gradient */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid #e5e7eb;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15);
    }
    
    /* Beautiful buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    /* SIDEBAR USER PROFILE - LIGHT MODE VERSION */
    .sidebar-profile {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Post cards */
    .post-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .post-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Connection status styling */
    .connection-connected {
        background: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .connection-you {
        background: #3b82f6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Form styling */
    .stSelectbox > div > div {
        background: white;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
    }
    
    .stTextInput > div > div > input {
        background: white;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea textarea {
        background: white;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        font-family: 'Inter', sans-serif;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: #ecfdf5;
        border: 1px solid #10b981;
        border-radius: 10px;
        color: #065f46;
    }
    
    .stError {
        background: #fef2f2;
        border: 1px solid #ef4444;
        border-radius: 10px;
        color: #991b1b;
    }
    
    /* Directory cards */
    .directory-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .directory-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #1f2937;
    }
    </style>
    """, unsafe_allow_html=True)
    

def make_links_clickable(text):
    """Convert URLs in text to clickable links"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    
    def replace_url(match):
        url = match.group()
        return f'<a href="{url}" target="_blank" style="color: #6366f1; text-decoration: underline; font-weight: 500;">{url}</a>'
    
    return re.sub(url_pattern, replace_url, text)


def main():
    """Main application with WORKING MODALS"""
    
    # Apply custom CSS
    add_custom_css()
    
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
            <h1 style="font-size: 3rem; margin: 0; font-weight: 700;">🎓 Alumni Network</h1>
            <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">Connect with Your Alumni Community</p>
        </div>
        """, unsafe_allow_html=True)
        
        show_main_app()


def show_landing_page():
    """Beautiful landing page with STABLE layout"""
    
    # Header buttons FIRST
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
    
    # Beautiful header with CENTERED text
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 1.5rem; margin: 0.5rem -1rem 1.5rem -1rem; text-align: center;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; color: white;">
                <span style="font-size: 2rem;">🎓</span>
                <h1 style="margin: 0; font-size: 1.8rem; font-weight: 700;">Alumni Network</h1>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div style="text-align: center; margin: 1rem 0;">
        <h2 style="font-size: 2.5rem; font-weight: bold; color: #1f2937; margin-bottom: 0.5rem;">Connect with Your Alumni Community</h2>
        <p style="font-size: 1.2rem; color: #6b7280; max-width: 600px; margin: 0 auto;">Reconnect with classmates, share experiences, and grow your professional network.</p>
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
            <p style="color: #6b7280;">Connect with alumni across different industries and graduation years to expand your professional network.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style="color: #6366f1; font-size: 2.5rem; margin-bottom: 1rem;">💼</div>
            <h4 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Career Opportunities</h4>
            <p style="color: #6b7280;">Discover job opportunities, mentorship programs, and career advice from experienced alumni.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div style="color: #6366f1; font-size: 2.5rem; margin-bottom: 1rem;">💬</div>
            <h4 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Community Engagement</h4>
            <p style="color: #6b7280;">Participate in discussions, share your experiences, and stay updated with alumni events.</p>
        </div>
        """, unsafe_allow_html=True)


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
    """Show main application after authentication"""
    user = auth.get_current_user()
    
    # BEAUTIFUL SIDEBAR WITH LIGHT MODE
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-profile">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎓</div>
            <h3 style="margin: 0; color: #1f2937;">{user['first_name']} {user['last_name']}</h3>
            <p style="margin: 0.5rem 0; color: #4b5563;">Class of {user['graduation_year']}</p>
            <p style="margin: 0; color: #4b5563;">{user['major']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        
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
    
    # Main content
    if page == "Dashboard":
        show_dashboard()
    elif page == "Alumni Directory":
        show_directory()
    elif page == "My Profile":
        show_profile()
    elif page == "My Connections":
        show_connections()


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
                        <h4 style="margin: 0; color: #1f2937; font-weight: 600;">{post['first_name']} {post['last_name']}</h4>
                        <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">Class of {post['graduation_year']}</p>
                    </div>
                    <span style="color: #9ca3af; font-size: 0.8rem;">{post['created_at'][:10]}</span>
                </div>
                <div class="post-content">
                    <p style="margin: 0; line-height: 1.6; color: #374151;">{make_links_clickable(post['content'])}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📝 No posts yet. Be the first to share something!")


def show_directory():
    """Beautiful alumni directory"""
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
    
    user_connections = db.get_user_connections(current_user['id'])
    connected_user_ids = set()
    if not user_connections.empty:
        connected_user_ids = set(user_connections['id'].tolist())
    
    if not users_df.empty:
        st.markdown(f"### 🔍 Found {len(users_df)} alumni")
        
        for idx, user in users_df.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="directory-card">
                    <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{user['first_name']} {user['last_name']}</h4>
                    <p style="margin: 0; color: #6b7280;">🎓 Class of {user['graduation_year']} • 📚 {user['major']}</p>
                    <p style="margin: 0.5rem 0 0 0; color: #9ca3af; font-size: 0.8rem;">Joined: {user['created_at'][:10]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.write("")  # Spacer
            
            with col3:
                if user['id'] != current_user['id']:
                    if user['id'] in connected_user_ids:
                        st.markdown('<div class="connection-connected">✅ Connected</div>', unsafe_allow_html=True)
                    else:
                        if st.button(f"🔗 Connect", key=f"connect_{user['id']}", use_container_width=True):
                            result = db.create_connection(current_user['id'], user['id'])
                            if result["success"]:
                                st.success("✅ " + result["message"])
                                st.rerun()
                            else:
                                st.error("❌ " + result["message"])
                else:
                    st.markdown('<div class="connection-you">👤 You</div>', unsafe_allow_html=True)
    else:
        st.info("🔍 No alumni found with the current search criteria")


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
                <p style="margin-top: 1rem; color: #9ca3af; font-size: 0.8rem;">Posted: {post['created_at'][:10]}</p>
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
                    <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{connection['first_name']} {connection['last_name']}</h4>
                    <p style="margin: 0; color: #6b7280;">🎓 Class of {connection['graduation_year']} • 📚 {connection.get('major', 'N/A')}</p>
                </div>
                <div style="text-align: right;">
                    <p style="margin: 0; color: #9ca3af; font-size: 0.8rem;">Connected: {connection['created_at'][:10]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔗 You don't have any connections yet. Visit the Alumni Directory to connect with other alumni!")


if __name__ == "__main__":
    main()

