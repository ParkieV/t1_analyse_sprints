from datetime import timedelta, datetime, timezone
from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.config import auth_config, db_config
from src.repositories.mongo_context import MongoContext


class AuthHandler:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    _auth_config = auth_config

    db_context = MongoContext(collection_name='users')

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=self._auth_config.access_token_expires))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._auth_config.secret_key, algorithm=self._auth_config.algorithm)
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    async def authenticate_user(self, user_id: UUID, password: str):
        user = await self.db_context.crud.get_object_by_id(user_id)
        if not user or not self.verify_password(password, user.hashed_password):
            return False
        return user