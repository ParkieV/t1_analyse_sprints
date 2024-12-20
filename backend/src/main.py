from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.logger import logger
from src.presentations.api import router
from src.repositories.mongo_context import MongoContext


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoContext.check_connection()
    yield

app = FastAPI(lifespan=lifespan, root_path="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
