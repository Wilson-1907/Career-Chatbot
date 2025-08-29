from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

import chat

load_dotenv()  # read .env if present

APP_NAME = os.getenv("APP_NAME", "CBE Career Chatbot Backend")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5500", 
    "http://localhost:5500").split(",")

app = FastAPI(
    title=APP_NAME,
    description="Foundation API for CBE Career Chatbot (clean architecture, ready to scale).",
    version="0.1.0",
)

# Allow frontend apps to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers (endpoints)
app.include_router(chat.router)

@app.get("/", tags=["Home"])
def home():
    return {"message": "CBE Chatbot backend is running ✅. Visit /docs for the API playground."}



