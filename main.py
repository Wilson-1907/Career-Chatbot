from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import auth, chat, health

load_dotenv()  # read .env if present

APP_NAME = os.getenv("APP_NAME", "CBE Career Chatbot Backend")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

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
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/", tags=["Home"])
def home():
    return {"message": "CBE Chatbot backend is running ✅. Visit /docs for the API playground."}
