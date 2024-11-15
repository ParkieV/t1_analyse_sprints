from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm


class AuthRequestSchema(OAuth2PasswordRequestForm):
    client_id: UUID
    username: str | None = None