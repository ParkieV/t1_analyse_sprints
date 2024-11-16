from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.logger import logger
from src.presentations.api import router
from src.repositories.mongo_context import MongoContext


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug('1')
    MongoContext.check_connection()
    logger.debug('2')
    yield

try:
    app = FastAPI(lifespan=lifespan, root_path="/api")
    logger.debug('3')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
except Exception as e:
    print(e.__class__.__name__, e)
    raise e
except BaseException as e:
    print(e.__class__.__name__, e)
    raise e
