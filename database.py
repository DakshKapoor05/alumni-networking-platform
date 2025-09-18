import streamlit as st
import pandas as pd
import bcrypt
from datetime import datetime
from supabase import create_client, Client


class DatabaseManager:
    """Handle all database operations for Alumni Network"""
    
    def __init__(self):
        # Use direct Supabase client
        url = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
        key = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]
        self.supabase: Client = create_client(url, key)
    
    def hash_password(self, password):
        """Hash password for secure storage"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, email, password, first_name, last_name, graduation_year, major):
        """Register new alumni user"""
        try:
            # Check if user exists
            existing_user = self.supabase.table("users").select("*").eq("email", email).execute()
            if existing_user.data:
                return {"success": False, "message": "Email already registered!"}
            
            # Create new user
            user_data = {
                "email": email,
                "password_hash": self.hash_password(password),
                "first_name": first_name,
                "last_name": last_name,
                "graduation_year": graduation_year,
                "major": major,
                "created_at": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table("users").insert(user_data).execute()
            return {"success": True, "message": "Registration successful!", "user_id": result.data[0]['id']}
            
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}
    
    def authenticate_user(self, email, password):
        """Login user with email and password"""
        try:
            user = self.supabase.table("users").select("*").eq("email", email).execute()
            
            if user.data and len(user.data) > 0:
                user_data = user.data[0]
                if self.verify_password(password, user_data['password_hash']):
                    return {"success": True, "user": user_data}
            
            return {"success": False, "message": "Invalid email or password"}
            
        except Exception as e:
            return {"success": False, "message": f"Login failed: {str(e)}"}
    
    def get_all_users(self):
        """Get all alumni for directory"""
        try:
            users = self.supabase.table("users").select("id, first_name, last_name, graduation_year, major, created_at").execute()
            return pd.DataFrame(users.data) if users.data else pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching users: {e}")
            return pd.DataFrame()
    
    def search_users(self, search_term="", graduation_year=None):
        """Search alumni by name, major, or graduation year"""
        try:
            if graduation_year:
                users = self.supabase.table("users").select("id, first_name, last_name, graduation_year, major, created_at").eq("graduation_year", graduation_year).execute()
                return pd.DataFrame(users.data) if users.data else pd.DataFrame()
            
            users = self.supabase.table("users").select("id, first_name, last_name, graduation_year, major, created_at").execute()
            df = pd.DataFrame(users.data) if users.data else pd.DataFrame()
            
            if search_term and not df.empty:
                mask = (df['first_name'].str.contains(search_term, case=False, na=False) |
                       df['last_name'].str.contains(search_term, case=False, na=False) |
                       df['major'].str.contains(search_term, case=False, na=False))
                return df[mask]
            
            return df
            
        except Exception as e:
            st.error(f"Error searching users: {e}")
            return pd.DataFrame()
    
    # ==================== POST OPERATIONS ====================
    
    def create_post(self, user_id, content):
        """Create new alumni post"""
        try:
            post_data = {
                "user_id": user_id,
                "content": content,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table("posts").insert(post_data).execute()
            return {"success": True, "message": "Post created successfully!"}
            
        except Exception as e:
            return {"success": False, "message": f"Failed to create post: {str(e)}"}
    
    def get_all_posts(self):
        """Get all posts with user information"""
        try:
            # Get posts
            posts = self.supabase.table("posts").select("*").execute()
            if not posts.data:
                return pd.DataFrame()
            
            # Get all users
            users = self.supabase.table("users").select("id, first_name, last_name, graduation_year").execute()
            if not users.data:
                return pd.DataFrame()
            
            # Create user lookup dictionary
            user_lookup = {user['id']: user for user in users.data}
            
            # Build result
            result_data = []
            for post in posts.data:
                user_info = user_lookup.get(post['user_id'], {})
                
                post_data = {
                    'id': post['id'],
                    'content': post['content'],
                    'created_at': post['created_at'],
                    'first_name': user_info.get('first_name', 'Unknown'),
                    'last_name': user_info.get('last_name', 'User'),
                    'graduation_year': user_info.get('graduation_year', 'N/A')
                }
                result_data.append(post_data)
            
            result_df = pd.DataFrame(result_data)
            return result_df.sort_values('created_at', ascending=False)
            
        except Exception as e:
            st.error(f"Error fetching posts: {e}")
            return pd.DataFrame()
    
    def get_user_posts(self, user_id):
        """Get posts by specific user"""
        try:
            posts = self.supabase.table("posts").select("*").eq("user_id", user_id).execute()
            return pd.DataFrame(posts.data) if posts.data else pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching user posts: {e}")
            return pd.DataFrame()
    
    # ==================== CONNECTION OPERATIONS ====================
    
    def create_connection(self, sender_id, receiver_id):
        """Connect two alumni"""
        try:
            # Check if connection already exists (both directions)
            existing1 = self.supabase.table("connections").select("*").eq("sender_id", sender_id).eq("receiver_id", receiver_id).execute()
            existing2 = self.supabase.table("connections").select("*").eq("sender_id", receiver_id).eq("receiver_id", sender_id).execute()
            
            if existing1.data or existing2.data:
                return {"success": False, "message": "Already connected!"}
            
            connection_data = {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "created_at": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table("connections").insert(connection_data).execute()
            return {"success": True, "message": "Connected successfully!"}
            
        except Exception as e:
            return {"success": False, "message": f"Connection failed: {str(e)}"}
    
    def get_user_connections(self, user_id):
        """Get all connections for a user WITH MAJOR INFO - FIXED VERSION"""
        try:
            # Get connections where user is sender
            sent_connections = self.supabase.table("connections").select(
                "created_at, receiver_id"
            ).eq("sender_id", user_id).execute()
            
            # Get connections where user is receiver  
            received_connections = self.supabase.table("connections").select(
                "created_at, sender_id"
            ).eq("receiver_id", user_id).execute()
            
            connection_user_ids = []
            connection_dates = {}
            
            # Collect connected user IDs and dates
            for conn in sent_connections.data:
                connection_user_ids.append(conn['receiver_id'])
                connection_dates[conn['receiver_id']] = conn['created_at']
                
            for conn in received_connections.data:
                connection_user_ids.append(conn['sender_id'])
                connection_dates[conn['sender_id']] = conn['created_at']
            
            if not connection_user_ids:
                return pd.DataFrame()
            
            # Get user details for all connected users (INCLUDING MAJOR)
            users_result = self.supabase.table("users").select(
                "id, first_name, last_name, graduation_year, major"
            ).in_("id", connection_user_ids).execute()
            
            connections = []
            for user_data in users_result.data:
                connections.append({
                    'id': user_data['id'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'graduation_year': user_data['graduation_year'],
                    'major': user_data.get('major', 'N/A'),  # 🔥 NOW INCLUDES MAJOR!
                    'created_at': connection_dates.get(user_data['id'], '')
                })
            
            return pd.DataFrame(connections)
            
        except Exception as e:
            print(f"Error getting connections: {e}")
            st.error(f"Error getting connections: {e}")
            return pd.DataFrame()
