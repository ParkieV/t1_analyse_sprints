from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.jwt import AuthHandler

router = APIRouter(prefix="/auth", tags=["Authorization endpoints"])


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_handler = AuthHandler()
    user = await auth_handler.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth_handler.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
