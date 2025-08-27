from fastapi import APIRouter
from chat_models import ChatMessage, ChatResponse
from chat_service import handle_chat

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatMessage):
    return handle_chat(payload)
