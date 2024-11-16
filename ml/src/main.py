from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.default_metrics import router
from src.routes.additional_metrics import add_router
from src.repositories.mongo_context import MongoContext

@asynccontextmanager
async def lifespan(app: FastAPI):
    MongoContext.check_connection()
    yield

app = FastAPI(lifespan=lifespan, root_path="/api_ml")
app.include_router(router)
app.include_router(add_router)

if __name__ == "__main__":
    try:
        import uvicorn
        # uvicorn.run("src.main:app", host=os.getenv("ML_HOST"), port=os.getenv("ML_PORT"))
        uvicorn.run("src.main:app", host='localhost', port=8000, reload=True)
    except KeyboardInterrupt:
        print("Сервер остановлен.")