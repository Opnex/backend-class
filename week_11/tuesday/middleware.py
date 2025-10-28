import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security

bearer = HTTPBearer()

load_dotenv()
secret_key = os.getenv("secret_key")
if not secret_key:
    # Provide a clear error so it's obvious why token signing might fail
    raise RuntimeError("secret_key not set in environment (.env) - cannot create tokens")

def create_token(details: dict, expiry: int):
    expire = datetime.now() + timedelta(minutes=expiry)
    details.update({"exp": expire})
    token = jwt.encode(details, secret_key, algorithm="HS256")
    return token

def verify_token(request: HTTPAuthorizationCredentials = Security(bearer)):

    token = request.credentials

    verify_token = jwt.decode(token, secret_key, algorithms=["HS256"])

    return {
        "email": verify_token.get("email"),
        "userType": verify_token.get("userType")
    }