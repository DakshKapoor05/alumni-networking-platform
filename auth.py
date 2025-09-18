import streamlit as st
from database import DatabaseManager

class AuthManager:
    """Handle user authentication and session management for Streamlit"""
    
    def __init__(self):
        self.db = DatabaseManager()
        
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
    
    def login_form(self):
        """Display login form"""
        st.subheader("🔐 Alumni Login")
        
        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if email and password:
                    result = self.db.authenticate_user(email, password)
                    
                    if result["success"]:
                        st.session_state.authenticated = True
                        st.session_state.user_data = result["user"]
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(result["message"])
                else:
                    st.error("Please fill in all fields")
    
    def register_form(self):
        """Display registration form"""
        st.subheader("📝 Alumni Registration")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                email = st.text_input("Email Address")
            
            with col2:
                graduation_year = st.number_input("Graduation Year", 
                                                min_value=1950, 
                                                max_value=2030, 
                                                value=2020)
                major = st.text_input("Major/Field of Study")
                password = st.text_input("Password", type="password")
            
            submit = st.form_submit_button("Register")
            
            if submit:
                if all([first_name, last_name, email, password, major]):
                    result = self.db.create_user(
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        graduation_year=int(graduation_year),
                        major=major
                    )
                    
                    if result["success"]:
                        st.success(result["message"])
                        st.info("Please login with your new credentials")
                    else:
                        st.error(result["message"])
                else:
                    st.error("Please fill in all fields")
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.success("Logged out successfully")
        st.rerun()
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.authenticated
    
    def get_current_user(self):
        """Get current user data"""
        return st.session_state.user_data
