import hashlib
import os
import json

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == hashed

def get_user_by_email(email: str):
    """Get user from mock data by email."""
    try:
        mock_data_path = "mock_data/users.json"
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                users_data = json.load(f)
            
            for user_data in users_data:
                if user_data["email"].lower().strip() == email.lower().strip():
                    return type('User', (), {
                        'id': user_data["id"],
                        'email': user_data["email"],
                        'password_hash': user_data["password_hash"],
                        'eco_score': user_data["eco_score"]
                    })()
        return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

def create_user(email: str, password: str):
    """Create a new user in mock data and optionally in Snowflake database."""
    try:
        # Try to save to Snowflake database first
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from db.snowflake_connector import get_snowflake_manager
            
            snowflake_manager = get_snowflake_manager()
            password_hash = hash_password(password)
            user_id = snowflake_manager.insert_user(email, password_hash, 0.0)
            
            if user_id:
                print(f"User created in Snowflake with ID: {user_id}")
        except Exception as e:
            print(f"Could not save to Snowflake database: {e}")
        
        # Also save to mock data for backward compatibility
        mock_data_path = "mock_data/users.json"
        users = []
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                users = json.load(f)
        
        password_hash = hash_password(password)
        new_user = {
            "id": len(users) + 1,
            "email": email,
            "password_hash": password_hash,
            "eco_score": 0.0
        }
        users.append(new_user)
        
        with open(mock_data_path, 'w') as f:
            json.dump(users, f, indent=2)
        
        return {"status": "success", "message": "User created"}
    except Exception as e:
        print(f"Error creating user: {e}")
        return {"status": "error", "message": "Failed to create user"} 