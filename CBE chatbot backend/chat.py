from fastapi import APIRouter
from models.chat_models import ChatMessage, ChatResponse
from services.chat_service import handle_chat

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
def chat(payload: ChatMessage):
    return handle_chat(payload)
