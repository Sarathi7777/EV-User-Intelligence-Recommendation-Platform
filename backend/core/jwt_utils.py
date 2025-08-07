import jwt
import datetime
import os
from fastapi import HTTPException, Request
from typing import Optional

SECRET_KEY = os.getenv('JWT_SECRET', 'supersecret')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# In-memory blacklist for demo (use Redis/DB in prod)
blacklisted_tokens = set()

def create_access_token(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str = 'access'):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token has been revoked")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get('type') != token_type:
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def blacklist_token(token: str):
    blacklisted_tokens.add(token)

def get_token_from_request(request: Request):
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return auth.split(' ')[1]