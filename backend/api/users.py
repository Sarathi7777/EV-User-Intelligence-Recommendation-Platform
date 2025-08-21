from fastapi import APIRouter, HTTPException, Response, Request, Cookie
import json
import os
from typing import Optional
from models.schemas import UserLogin, UserResponse, UserRegistration
from core.security import verify_password, get_user_by_email, hash_password
from core.jwt_utils import (
    create_access_token, create_refresh_token, verify_token, blacklist_token, get_token_from_request
)
from slowapi.util import get_remote_address
from slowapi import Limiter
from fastapi import Depends
import sys
import os

# Add the parent directory to the path to import db modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.snowflake_connector import get_snowflake_manager

router = APIRouter(prefix="/login", tags=["Users"])

limiter = Limiter(key_func=get_remote_address)

@router.post("/register", response_model=UserResponse)
@limiter.limit("3/minute")
def register(user: UserRegistration, response: Response, request: Request):
    """Register a new user and save to Snowflake database."""
    try:
        # Check if user already exists
        snowflake_manager = get_snowflake_manager()
        existing_user = snowflake_manager.get_user_by_email(user.email)
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Hash password
        password_hash = hash_password(user.password)
        
        # Insert user into Snowflake database
        user_id = snowflake_manager.insert_user(
            email=user.email,
            password_hash=password_hash,
            eco_score=0.0,
            first_name=user.first_name,
            last_name=user.last_name,
            vehicle_type=user.vehicle_type,
            phone=user.phone
        )
        
        if not user_id:
            raise HTTPException(status_code=500, detail="Failed to create user in database")
        
        # Also save to mock data for backward compatibility
        try:
            mock_data_path = "mock_data/users.json"
            users = []
            if os.path.exists(mock_data_path):
                with open(mock_data_path, 'r') as f:
                    users = json.load(f)
            
            new_user = {
                "id": user_id,
                "email": user.email,
                "password_hash": password_hash,
                "eco_score": 0.0,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "vehicle_type": user.vehicle_type,
                "phone": user.phone
            }
            users.append(new_user)
            
            with open(mock_data_path, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save to mock data: {e}")
        
        # Issue tokens
        payload = {"user_id": user_id, "email": user.email}
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)
        
        # Set refresh token in HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # Set True in production
            samesite="lax",
            max_age=7*24*60*60
        )
        
        return {
            "id": user_id,
            "email": user.email,
            "eco_score": 0.0,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "access_token": access_token
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=UserResponse)
@limiter.limit("5/minute")
def login(user: UserLogin, response: Response, request: Request):
    """Login user and issue JWT tokens."""
    try:
        # First try to authenticate from Snowflake database
        try:
            snowflake_manager = get_snowflake_manager()
            db_user = snowflake_manager.get_user_by_email((user.email or "").strip())

            if db_user:
                # Columns are normalized to lowercase by the connector
                if not verify_password(user.password, db_user["password_hash"]):
                    raise HTTPException(status_code=401, detail="Invalid credentials")

                # Issue tokens
                payload = {"user_id": db_user["id"], "email": db_user["email"]}
                access_token = create_access_token(payload)
                refresh_token = create_refresh_token(payload)

                # Set refresh token in HttpOnly cookie
                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token,
                    httponly=True,
                    secure=False,  # Set True in production
                    samesite="lax",
                    max_age=7*24*60*60
                )

                return {
                    "id": db_user["id"],
                    "email": db_user["email"],
                    "eco_score": db_user.get("eco_score", 0.0),
                    "first_name": db_user.get("first_name"),
                    "last_name": db_user.get("last_name"),
                    "access_token": access_token
                }
        except Exception as e:
            print(f"Snowflake authentication failed, falling back to mock data: {e}")
        
        # Fallback to mock data for backward compatibility
        mock_data_path = "mock_data/users.json"
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                users_data = json.load(f)
            for user_data in users_data:
                if user_data["email"] == user.email:
                    if verify_password(user.password, user_data["password_hash"]):
                        # Issue tokens
                        payload = {"user_id": user_data["id"], "email": user_data["email"]}
                        access_token = create_access_token(payload)
                        refresh_token = create_refresh_token(payload)
                        # Set refresh token in HttpOnly cookie
                        response.set_cookie(
                            key="refresh_token",
                            value=refresh_token,
                            httponly=True,
                            secure=False,  # Set True in production
                            samesite="lax",
                            max_age=7*24*60*60
                        )
                        return {
                            "id": user_data["id"],
                            "email": user_data["email"],
                            "eco_score": user_data["eco_score"],
                            "access_token": access_token
                        }
                    else:
                        raise HTTPException(status_code=401, detail="Invalid credentials")
            raise HTTPException(status_code=401, detail="User not found")
        else:
            if user.email == "test@example.com" and user.password == "123":
                payload = {"user_id": 1, "email": "test@example.com"}
                access_token = create_access_token(payload)
                refresh_token = create_refresh_token(payload)
                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token,
                    httponly=True,
                    secure=False,
                    samesite="lax",
                    max_age=7*24*60*60
                )
                return {"id": 1, "email": "test@example.com", "eco_score": 85.0, "access_token": access_token}
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/refresh-token")
@limiter.limit("10/minute")
def refresh_token(request: Request, refresh_token: Optional[str] = Cookie(None)):
    """Issue a new access token using a valid refresh token."""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    payload = verify_token(refresh_token, token_type='refresh')
    new_access_token = create_access_token({"user_id": payload["user_id"], "email": payload["email"]})
    return {"access_token": new_access_token}

@router.post("/logout")
def logout(request: Request, response: Response, access_token: Optional[str] = Cookie(None)):
    """Logout user by blacklisting access token and clearing refresh token cookie."""
    # Try to get access token from header or cookie
    token = access_token
    if not token:
        try:
            token = get_token_from_request(request)
        except Exception:
            token = None
    if token:
        blacklist_token(token)
    response.delete_cookie("refresh_token")
    return {"success": True, "message": "Logged out"}