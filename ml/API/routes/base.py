from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
import sys
import os
from dotenv import load_dotenv
load_dotenv()

base_router = APIRouter()

@base_router.get("/")
def get_base():
    return "Hello world"
