from fastapi import APIRouter, HTTPException
import json
import os
# from backend.models.schemas import UserLogin, UserResponse
from models.schemas import UserLogin, UserResponse
from core.security import verify_password, get_user_by_email

router = APIRouter(prefix="/login", tags=["Users"])

@router.post("/", response_model=UserResponse)
def login(user: UserLogin):
    """Login user with mock data."""
    try:
        # Load mock users
        mock_data_path = "mock_data/users.json"
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                users_data = json.load(f)
            
            # Find user by email
            for user_data in users_data:
                if user_data["email"] == user.email:
                    if verify_password(user.password, user_data["password_hash"]):
                        return UserResponse(
                            id=user_data["id"],
                            email=user_data["email"],
                            eco_score=user_data["eco_score"]
                        )
                    else:
                        raise HTTPException(status_code=401, detail="Invalid credentials")
            
            raise HTTPException(status_code=401, detail="User not found")
        else:
            # Fallback to hardcoded test user
            if user.email == "test@example.com" and user.password == "123":
                return UserResponse(id=1, email="test@example.com", eco_score=85.0)
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")