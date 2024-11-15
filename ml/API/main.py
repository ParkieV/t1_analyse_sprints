from fastapi import FastAPI
import uvicorn
import sys
import os
from dotenv import load_dotenv
from routes.base import base_router
load_dotenv()

app = FastAPI(title="T1 Impulse Hack ml http server", docs_url="/docs", openapi_url="/api")

app.include_router(base_router, prefix="/api/base", tags=["base"])

if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST"), port=8000, reload=True)
