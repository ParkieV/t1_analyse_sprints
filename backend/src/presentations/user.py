from fastapi import Depends, APIRouter, HTTPException, status

from src.repositories.mongo import UsersCRUD
from src.repositories.mongo_context import MongoContext
from src.schemas.user import UserDBOutDTO
from src.services.utils import check_token

router = APIRouter(tags=["Authorization Endpoints"])


@router.get("/users/{username}", response_model=UserDBOutDTO, dependencies=[Depends(check_token)])
async def read_user_info(username: str):
    db_context = MongoContext[UsersCRUD](crud=UsersCRUD())
    try:
        return await db_context.crud.get_object_by_username(username)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
