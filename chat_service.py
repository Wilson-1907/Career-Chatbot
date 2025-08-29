from chat_models import ChatMessage, ChatResponse


def simple_rule_engine(msg: str) -> str:
    text = msg.lower()
    if "hello" in text or "hi" in text:
        return "Hello! I’m your CBE career assistant. What subjects do you enjoy most?"
    if "math" in text:
        return "Nice! Math strength often fits Data Science, Engineering, or Actuarial Science."
    if "biology" in text or "chemistry" in text:
        return "Great! You could explore Medicine, Pharmacy, or Biotechnology."
    if "art" in text or "design" in text:
        return "Awesome! Consider Design, Media, Fine Arts, or UX."
    return "Tell me your favorite subjects or interests, and I’ll suggest career paths."


def handle_chat(payload: ChatMessage) -> ChatResponse:
    reply = simple_rule_engine(payload.message)
    return ChatResponse(user_id=payload.user_id, reply=reply)
