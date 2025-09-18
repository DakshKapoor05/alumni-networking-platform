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
    
    # ==================== CONNECTION REQUEST SYSTEM (LinkedIn-style) ====================
    
    def send_connection_request(self, sender_id, receiver_id, message=""):
        """Send a connection request to another user"""
        try:
            # Check if users are already connected
            existing_connection = self.check_connection_status(sender_id, receiver_id)
            
            if existing_connection == "connected":
                return {"success": False, "message": "Already connected!"}
            elif existing_connection == "pending_sent":
                return {"success": False, "message": "Connection request already sent!"}
            elif existing_connection == "pending_received":
                return {"success": False, "message": "This user already sent you a request!"}
            
            # Create connection request
            request_data = {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "status": "pending",
                "message": message,
                "created_at": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table("connection_requests").insert(request_data).execute()
            return {"success": True, "message": "Connection request sent!"}
            
        except Exception as e:
            return {"success": False, "message": f"Failed to send request: {str(e)}"}
    
    def get_connection_requests(self, user_id, request_type="received"):
        """Get connection requests for a user"""
        try:
            if request_type == "received":
                # Get requests received by user
                requests = self.supabase.table("connection_requests").select("*").eq("receiver_id", user_id).eq("status", "pending").execute()
            else:
                # Get requests sent by user
                requests = self.supabase.table("connection_requests").select("*").eq("sender_id", user_id).eq("status", "pending").execute()
            
            if not requests.data:
                return pd.DataFrame()
            
            # Get user details for the requests
            user_ids = []
            for req in requests.data:
                if request_type == "received":
                    user_ids.append(req['sender_id'])
                else:
                    user_ids.append(req['receiver_id'])
            
            users_result = self.supabase.table("users").select("id, first_name, last_name, graduation_year, major").in_("id", user_ids).execute()
            user_lookup = {user['id']: user for user in users_result.data}
            
            # Build result
            result_data = []
            for req in requests.data:
                target_user_id = req['sender_id'] if request_type == "received" else req['receiver_id']
                user_info = user_lookup.get(target_user_id, {})
                
                request_data = {
                    'request_id': req['id'],
                    'user_id': target_user_id,
                    'first_name': user_info.get('first_name', 'Unknown'),
                    'last_name': user_info.get('last_name', 'User'),
                    'graduation_year': user_info.get('graduation_year', 'N/A'),
                    'major': user_info.get('major', 'N/A'),
                    'message': req.get('message', ''),
                    'created_at': req['created_at']
                }
                result_data.append(request_data)
            
            return pd.DataFrame(result_data)
            
        except Exception as e:
            st.error(f"Error fetching connection requests: {e}")
            return pd.DataFrame()
    
    def accept_connection_request(self, request_id):
        """Accept a connection request"""
        try:
            # Get the request details
            request = self.supabase.table("connection_requests").select("*").eq("id", request_id).execute()
            
            if not request.data:
                return {"success": False, "message": "Request not found!"}
            
            request_data = request.data[0]
            sender_id = request_data['sender_id']
            receiver_id = request_data['receiver_id']
            
            # Create the actual connection
            connection_data = {
                "user1_id": min(sender_id, receiver_id),  # Always store smaller ID first
                "user2_id": max(sender_id, receiver_id),  # Larger ID second
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Insert connection
            self.supabase.table("connections").insert(connection_data).execute()
            
            # Update request status to accepted
            self.supabase.table("connection_requests").update({"status": "accepted"}).eq("id", request_id).execute()
            
            return {"success": True, "message": "Connection request accepted!"}
            
        except Exception as e:
            return {"success": False, "message": f"Failed to accept request: {str(e)}"}
    
    def reject_connection_request(self, request_id):
        """Reject a connection request"""
        try:
            # Update request status to rejected
            self.supabase.table("connection_requests").update({"status": "rejected"}).eq("id", request_id).execute()
            
            return {"success": True, "message": "Connection request rejected."}
            
        except Exception as e:
            return {"success": False, "message": f"Failed to reject request: {str(e)}"}
    
    def check_connection_status(self, user1_id, user2_id):
        """Check connection status between two users"""
        try:
            # Check if they are already connected
            min_id = min(user1_id, user2_id)
            max_id = max(user1_id, user2_id)
            
            existing_connection = self.supabase.table("connections").select("*").eq("user1_id", min_id).eq("user2_id", max_id).execute()
            
            if existing_connection.data:
                return "connected"
            
            # Check pending requests
            pending_sent = self.supabase.table("connection_requests").select("*").eq("sender_id", user1_id).eq("receiver_id", user2_id).eq("status", "pending").execute()
            
            if pending_sent.data:
                return "pending_sent"
            
            pending_received = self.supabase.table("connection_requests").select("*").eq("sender_id", user2_id).eq("receiver_id", user1_id).eq("status", "pending").execute()
            
            if pending_received.data:
                return "pending_received"
            
            return "not_connected"
            
        except Exception as e:
            print(f"Error checking connection status: {e}")
            return "not_connected"
    
    def get_user_connections(self, user_id):
        """Get all accepted connections for a user"""
        try:
            # Get connections where user is either user1 or user2
            connections1 = self.supabase.table("connections").select("*").eq("user1_id", user_id).execute()
            connections2 = self.supabase.table("connections").select("*").eq("user2_id", user_id).execute()
            
            connected_user_ids = []
            connection_dates = {}
            
            # Collect connected user IDs and dates
            for conn in connections1.data:
                connected_user_ids.append(conn['user2_id'])
                connection_dates[conn['user2_id']] = conn['created_at']
                
            for conn in connections2.data:
                connected_user_ids.append(conn['user1_id'])
                connection_dates[conn['user1_id']] = conn['created_at']
            
            if not connected_user_ids:
                return pd.DataFrame()
            
            # Get user details for all connected users
            users_result = self.supabase.table("users").select("id, first_name, last_name, graduation_year, major").in_("id", connected_user_ids).execute()
            
            connections = []
            for user_data in users_result.data:
                connections.append({
                    'id': user_data['id'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'graduation_year': user_data['graduation_year'],
                    'major': user_data.get('major', 'N/A'),
                    'created_at': connection_dates.get(user_data['id'], '')
                })
            
            return pd.DataFrame(connections)
            
        except Exception as e:
            print(f"Error getting connections: {e}")
            st.error(f"Error getting connections: {e}")
            return pd.DataFrame()

    # ==================== LEGACY METHOD (for backward compatibility) ====================
    
    def create_connection(self, sender_id, receiver_id):
        """Legacy method - now redirects to send_connection_request"""
        return self.send_connection_request(sender_id, receiver_id)
