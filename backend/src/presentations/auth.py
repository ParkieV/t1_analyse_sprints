from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.authentication import AuthenticationError

from src.jwt import AuthHandler

router = APIRouter(prefix="/auth", tags=["Authorization endpoints"])


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_handler = AuthHandler()
    try:
        user = await auth_handler.authenticate_user(form_data.username, form_data.password)
    except AuthenticationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth_handler.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
