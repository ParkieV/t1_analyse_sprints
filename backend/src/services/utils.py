from jose import jwt, JWTError
from fastapi import Depends, HTTPException

from src.jwt import AuthHandler
from src.config import auth_config


def check_token(token: str = Depends(AuthHandler.oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, auth_config.secret_key, algorithms=[auth_config.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
