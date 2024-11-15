from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from src.config import auth_config
from src.jwt import AuthHandler
from src.repositories.mongo import UsersCRUD
from src.repositories.mongo_context import MongoContext
from src.schemas.user import UserDBOutDTO

router = APIRouter(tags=["Authorization Endpoints"])


@router.get("/users/{username}", response_model=UserDBOutDTO)
async def read_user_info(username: str, token: str = Depends(AuthHandler.oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, auth_config.secret_key, algorithms=[auth_config.algorithm])
        token_username: str = payload.get("sub")
        if token_username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_context = MongoContext[UsersCRUD](crud=UsersCRUD())
    try:
        return await db_context.crud.get_object_by_username(username)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

