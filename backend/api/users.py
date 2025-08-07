from fastapi import APIRouter, HTTPException, Response, Request, Cookie
import json
import os
from typing import Optional
from models.schemas import UserLogin, UserResponse
from core.security import verify_password, get_user_by_email
from core.jwt_utils import (
    create_access_token, create_refresh_token, verify_token, blacklist_token, get_token_from_request
)
from slowapi.util import get_remote_address
from slowapi import Limiter
from fastapi import Depends

router = APIRouter(prefix="/login", tags=["Users"])

limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=UserResponse)
@limiter.limit("5/minute")
def login(user: UserLogin, response: Response, request: Request):
    """Login user and issue JWT tokens."""
    try:
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