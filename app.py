# import streamlit as st
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
#     """Alumni directory with search - WITH MAJOR DROPDOWN MATCHING REGISTER PAGE"""
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
#                 current_user = auth.get_current_user()
#                 if user['id'] != current_user['id']:
#                     if st.button(f"Connect", key=f"connect_{user['id']}"):
#                         result = db.create_connection(current_user['id'], user['id'])
#                         if result["success"]:
#                             st.success(result["message"])
#                         else:
#                             st.error(result["message"])
            
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
#     """User connections page - WITH MAJOR INFO"""
#     st.header("🔗 My Connections")
#     user = auth.get_current_user()
    
#     connections_df = db.get_user_connections(user['id'])
    
#     if not connections_df.empty:
#         st.subheader(f"You have {len(connections_df)} connections")
        
#         for idx, connection in connections_df.iterrows():
#             col1, col2 = st.columns([3, 1])
            
#             with col1:
#                 st.write(f"**{connection['first_name']} {connection['last_name']}**")
#                 # 🔥 ADDED MAJOR INFO - Show graduation year AND major
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
    page_icon="🎓"
)


# Initialize managers
auth = AuthManager()
db = DatabaseManager()


def make_links_clickable(text):
    """Convert URLs in text to clickable links"""
    # Regular expression to find URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    
    # Replace URLs with clickable links
    def replace_url(match):
        url = match.group()
        return f'<a href="{url}" target="_blank" style="color: #1f77b4; text-decoration: underline;">{url}</a>'
    
    return re.sub(url_pattern, replace_url, text)


def main():
    """Main application"""
    
    # Custom CSS - Clean version
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🎓 Alumni Network</h1>', unsafe_allow_html=True)
    
    # Authentication check
    if not auth.is_authenticated():
        # Show login/register tabs
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            auth.login_form()
        
        with tab2:
            # Custom register form with dropdowns
            show_register_form()
            
    else:
        # Show main app
        show_main_app()


def show_register_form():
    """Register form with dropdowns"""
    st.subheader("Create Account")
    
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
            # Graduation year dropdown
            current_year = datetime.now().year
            graduation_years = list(range(2000, current_year + 11))[::-1]  # Reverse for newest first
            graduation_year = st.selectbox("Graduation Year", 
                                         options=graduation_years, 
                                         index=graduation_years.index(2024) if 2024 in graduation_years else 0)
        
        with col4:
            # Major dropdown
            majors = [
                "Computer Science", "Engineering", "Business Administration", "Psychology",
                "Biology", "Chemistry", "Physics", "Mathematics", "English", "History",
                "Art", "Music", "Economics", "Political Science", "Sociology", "Philosophy", "Other"
            ]
            major = st.selectbox("Major", options=majors, index=0)
        
        submit = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit:
            if all([first_name, last_name, email, password, major]):
                result = db.create_user(
                    email=email, password=password,
                    first_name=first_name, last_name=last_name,
                    graduation_year=int(graduation_year), major=major
                )
                if result["success"]:
                    st.success("Registration successful! Please login.")
                else:
                    st.error(f"Registration failed: {result['message']}")
            else:
                st.error("Please fill in all fields")


def show_main_app():
    """Show main application after authentication"""
    user = auth.get_current_user()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
    <div style="text-align: center; padding: 15px; background-color: var(--background-color); border-radius: 10px; margin-bottom: 20px;">
        <div style="font-size: 50px; margin-bottom: 10px;">🎓</div>
        <h3>{user['first_name']} {user['last_name']}</h3>
        <p>Class of {user['graduation_year']}</p>
        <p>{user['major']}</p>
    </div>
    """, unsafe_allow_html=True)

        st.write("---")
        
        # NAVIGATION WITH BUTTONS INSTEAD OF DROPDOWN
        st.markdown("**Navigate:**")
        
        # Initialize page state
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
        
        # Use session state for page
        page = st.session_state.current_page
        
        st.write("---")
        if st.button("Logout", use_container_width=True):
            auth.logout()
    
    # Main content based on navigation
    if page == "Dashboard":
        show_dashboard()
    elif page == "Alumni Directory":
        show_directory()
    elif page == "My Profile":
        show_profile()
    elif page == "My Connections":
        show_connections()


def show_dashboard():
    """Dashboard with posts and create post - WITH CLICKABLE LINKS"""
    st.header("🏠 Dashboard")
    
    # Create post section
    with st.expander("✍️ Create New Post", expanded=False):
        with st.form("create_post"):
            content = st.text_area("What's on your mind?", height=100, 
                                 placeholder="Share your thoughts... You can include links like https://example.com")
            submit = st.form_submit_button("Post")
            
            if submit and content:
                user = auth.get_current_user()
                result = db.create_post(user['id'], content)
                
                if result["success"]:
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])
    
    # Display all posts
    st.subheader("📰 Recent Posts")
    
    posts_df = db.get_all_posts()
    
    if not posts_df.empty:
        # Display posts WITH CLICKABLE LINKS
        for idx, post in posts_df.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**{post['first_name']} {post['last_name']}** *(Class of {post['graduation_year']})*")
                    
                    # 🔥 MAKE LINKS CLICKABLE - Convert URLs to clickable links
                    content_with_links = make_links_clickable(post['content'])
                    st.markdown(f"📝 {content_with_links}", unsafe_allow_html=True)
                    
                    st.caption(f"Posted: {post['created_at'][:10]}")
                
                with col2:
                    # Optional: Add like/share buttons here later
                    pass
                
                st.divider()
    else:
        st.info("No posts yet. Be the first to share something!")


def show_directory():
    """Alumni directory with search - WITH CONNECTION STATUS CHECK"""
    st.header("👥 Alumni Directory")
    
    # Search filters - BOTH DROPDOWNS NOW
    col1, col2 = st.columns(2)
    with col1:
        # Major dropdown (same as register page)
        majors = [
            "All", "Computer Science", "Engineering", "Business Administration", "Psychology",
            "Biology", "Chemistry", "Physics", "Mathematics", "English", "History",
            "Art", "Music", "Economics", "Political Science", "Sociology", "Philosophy", "Other"
        ]
        selected_major = st.selectbox("Search by major", options=majors, index=0)
        
    with col2:
        graduation_year = st.selectbox("Filter by graduation year", 
                                     ["All"] + list(range(2010, 2025)))
    
    # Get users based on filters
    search_term = "" if selected_major == "All" else selected_major
    
    if graduation_year == "All":
        graduation_year = None
    
    users_df = db.search_users(search_term, graduation_year)
    current_user = auth.get_current_user()
    
    # 🔥 GET USER'S CONNECTIONS TO CHECK STATUS
    user_connections = db.get_user_connections(current_user['id'])
    connected_user_ids = set()
    if not user_connections.empty:
        connected_user_ids = set(user_connections['id'].tolist())
    
    if not users_df.empty:
        st.subheader(f"Found {len(users_df)} alumni")
        
        # Display users in cards
        for idx, user in users_df.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{user['first_name']} {user['last_name']}**")
                st.write(f"Class of {user['graduation_year']} • {user['major']}")
            
            with col2:
                st.write(f"Joined: {user['created_at'][:10]}")
            
            with col3:
                if user['id'] != current_user['id']:
                    # 🔥 CHECK CONNECTION STATUS
                    if user['id'] in connected_user_ids:
                        # Already connected - show status
                        st.success("✅ Connected")
                    else:
                        # Not connected - show connect button
                        if st.button(f"Connect", key=f"connect_{user['id']}"):
                            result = db.create_connection(current_user['id'], user['id'])
                            if result["success"]:
                                st.success(result["message"])
                                st.rerun()
                            else:
                                st.error(result["message"])
                else:
                    # Current user - show "You"
                    st.info("👤 You")
            
            st.write("---")
    else:
        st.info("No alumni found with the current search criteria")


def show_profile():
    """User profile page - WITH CLICKABLE LINKS IN POSTS"""
    user = auth.get_current_user()
    st.header(f"👤 {user['first_name']} {user['last_name']}")
    
    # User info
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Profile Information")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Graduation Year:** {user['graduation_year']}")
        st.write(f"**Major:** {user['major']}")
        st.write(f"**Member Since:** {user['created_at'][:10]}")
    
    with col2:
        st.subheader("Quick Stats")
        
        # Get user's posts count
        user_posts = db.get_user_posts(user['id'])
        posts_count = len(user_posts) if not user_posts.empty else 0
        
        # Get connections count
        user_connections = db.get_user_connections(user['id'])
        connections_count = len(user_connections) if not user_connections.empty else 0
        
        st.metric("Posts", posts_count)
        st.metric("Connections", connections_count)
    
    # User's posts WITH CLICKABLE LINKS
    st.subheader("My Posts")
    if not user_posts.empty:
        for idx, post in user_posts.iterrows():
            with st.container():
                # 🔥 MAKE LINKS CLICKABLE in user profile too
                content_with_links = make_links_clickable(post['content'])
                st.markdown(f"📝 {content_with_links}", unsafe_allow_html=True)
                st.caption(f"Posted: {post['created_at'][:10]}")
                st.divider()
    else:
        st.info("You haven't posted anything yet!")


def show_connections():
    """User connections page - SHOWS MAJOR INFO"""
    st.header("🔗 My Connections")
    user = auth.get_current_user()
    
    connections_df = db.get_user_connections(user['id'])
    
    if not connections_df.empty:
        st.subheader(f"You have {len(connections_df)} connections")
        
        for idx, connection in connections_df.iterrows():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{connection['first_name']} {connection['last_name']}**")
                # 🔥 SHOWS GRADUATION YEAR AND MAJOR
                st.write(f"🎓 Class of {connection['graduation_year']} • 📚 {connection.get('major', 'N/A')}")
            
            with col2:
                st.write(f"Connected: {connection['created_at'][:10]}")
            
            st.write("---")
    else:
        st.info("You don't have any connections yet. Visit the Alumni Directory to connect with other alumni!")


if __name__ == "__main__":
    main()

