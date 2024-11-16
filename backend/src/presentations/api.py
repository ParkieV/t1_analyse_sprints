from fastapi import APIRouter

from src.presentations import *

router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(data_router)