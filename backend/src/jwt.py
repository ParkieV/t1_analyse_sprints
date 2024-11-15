from datetime import timedelta, datetime, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.config import auth_config
from src.logger import logger
from src.repositories.mongo import UsersCRUD
from src.repositories.mongo_context import MongoContext


class AuthHandler:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    _auth_config = auth_config

    db_context = MongoContext[UsersCRUD](crud=UsersCRUD())

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=cls._auth_config.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls._auth_config.secret_key, algorithm=cls._auth_config.algorithm)
        return encoded_jwt

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls._pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls._pwd_context.hash(password)

    @classmethod
    async def authenticate_user(cls, username: str, password: str):
        user = await cls.db_context.crud.get_object_by_username(username)
        logger.debug("Found user : %s", user)
        if not user or not cls.verify_password(password, user.hashed_password):
            return False
        return user

if __name__ == "__main__":
    logger.debug(AuthHandler.get_password_hash("Qwerty123."))