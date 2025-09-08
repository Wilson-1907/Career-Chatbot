from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Debug: confirm which file is running
print("👉 Running THIS main.py:", __file__)

# ✅ Load environment variables
load_dotenv()

api_key = os.getenv("AIzaSyDDyRSRBIEC-OZYoiw9dNPwdWd9p8PMBLw")  # must exist in .env file
if not api_key:
    raise RuntimeError("❌ GEMINI_API_KEY not set in .env file!")

print("DEBUG: GEMINI_API_KEY =", api_key[:8] + "*****")  # Mask most of it

# ✅ Configure Gemini
genai.configure(api_key=api_key)

# ✅ Create FastAPI app
app = FastAPI(title="Career Guidance & CBE Chatbot", version="1.0")

# ✅ Enable CORS (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request model
class ChatRequest(BaseModel):
    question: str

# ✅ Conversation memory
conversation_history = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Backend running! Use POST /chat to talk to the bot."}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # Save user input in memory
        conversation_history.append({"role": "user", "content": request.question})

        # Build conversation context
        history_context = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in conversation_history]
        )

        prompt = f"""
        You are an AI-powered education and career guidance assistant.
        - Your expertise covers Competency-Based Education (CBE) in Kenya, KUCCPS, and how universities/TVETs handle student placements.
        - Provide accurate, clear, and structured answers.
        - Use simple examples when possible.
        - Give career guidance across fields, explaining pathways and opportunities.
        - If the question is outside education or career, politely say you can only answer education & career-related questions.

        Conversation so far:
        {history_context}
        """

        # Call Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Save assistant reply in memory
        conversation_history.append({"role": "assistant", "content": response.text})

        return {"answer": response.text.strip()}

    except Exception as e:
        return {"error": str(e)}
