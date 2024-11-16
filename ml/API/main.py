from fastapi import FastAPI
import uvicorn
import sys
import os
from dotenv import load_dotenv
from routes.base import base_router
load_dotenv()

app = FastAPI(title="T1 Impulse Hack ml http server",root_path="/api_ml")

app.include_router(base_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv("HOST"), port=8010)
