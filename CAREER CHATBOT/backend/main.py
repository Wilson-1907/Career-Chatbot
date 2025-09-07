from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
import google.generativeai as genai
from supabase import create_client, Client
from pydantic import BaseModel
from typing import Optional, List
import json
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CBE Career Guide API",
    description="Backend API for CBE Career Guide with Gemini AI integration",
    version="1.0.0"
)

# CORS configuration
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Add common local development origins
local_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "file://",  # For opening HTML files directly
    "null"      # For file:// protocol
]

# Combine configured origins with local development origins
all_origins = list(set(origins + local_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(supabase_url, supabase_service_key)

# Initialize Gemini AI
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

# Security
security = HTTPBearer()

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    language: str = "en"

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None

class UserContext(BaseModel):
    full_name: Optional[str] = None
    grade: Optional[str] = None
    school: Optional[str] = None
    pathway_recommendation: Optional[str] = None
    interests: Optional[dict] = None

# Helper functions
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Supabase JWT token"""
    try:
        token = credentials.credentials
        # Verify token with Supabase
        user = supabase.auth.get_user(token)
        return user
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication token")

async def get_user_context(user_id: str) -> UserContext:
    """Get user context from database"""
    try:
        # Get user profile
        profile_response = supabase.table('user_profiles').select('full_name, grade, school').eq('user_id', user_id).single().execute()
        
        # Get latest assessment
        assessment_response = supabase.table('assessment_results').select('pathway_recommendation, interests').eq('user_id', user_id).order('created_at', desc=True).limit(1).execute()
        
        context = UserContext()
        
        if profile_response.data:
            context.full_name = profile_response.data.get('full_name')
            context.grade = profile_response.data.get('grade')
            context.school = profile_response.data.get('school')
        
        if assessment_response.data and len(assessment_response.data) > 0:
            context.pathway_recommendation = assessment_response.data[0].get('pathway_recommendation')
            context.interests = assessment_response.data[0].get('interests')
        
        return context
    except Exception as e:
        logger.error(f"Error getting user context: {e}")
        return UserContext()

async def get_or_create_session(user_id: str, session_name: str = "CBE Career Chat") -> str:
    """Get or create chat session"""
    try:
        # Try to get existing session
        response = supabase.table('chat_sessions').select('id').eq('user_id', user_id).order('last_message_at', desc=True).limit(1).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]['id']
        
        # Create new session
        new_session = supabase.table('chat_sessions').insert({
            'user_id': user_id,
            'session_name': session_name
        }).execute()
        
        return new_session.data[0]['id']
    except Exception as e:
        logger.error(f"Error managing session: {e}")
        return None

def create_system_prompt(context: UserContext, language: str) -> str:
    """Create system prompt for Gemini AI"""
    user_context = ""
    if context.full_name:
        user_context += f"Student: {context.full_name}, "
    if context.grade:
        user_context += f"Grade: {context.grade}, "
    if context.school:
        user_context += f"School: {context.school}. "
    if context.pathway_recommendation:
        user_context += f"Recommended pathway: {context.pathway_recommendation}. "
    if context.interests:
        user_context += f"Interests: {json.dumps(context.interests)}. "

    return f"""You are an AI Career Guidance Assistant for Kenya's Competency Based Education (CBE) system. Your role is to help students navigate their educational and career choices.

CONTEXT: {user_context}

KEY INFORMATION ABOUT CBE:
- STEM Pathway: Science, Technology, Engineering & Mathematics (leads to medicine, engineering, tech careers)
- Social Sciences: Humanities & Social Studies (leads to law, teaching, journalism, government)
- Arts & Sports: Creative & Physical Education (leads to arts, music, sports, entertainment)
- Technical Pathway: Vocational & Technical Skills (leads to construction, automotive, hospitality, trades)

KENYAN EDUCATION SYSTEM:
- KCSE (Kenya Certificate of Secondary Education) is the main exam
- University entry requires C+ overall minimum
- KUCCPS handles university placement
- HELB provides student loans

GUIDELINES:
- Be encouraging and supportive
- Provide specific, actionable advice
- Reference Kenyan context (universities, job market, requirements)
- Use emojis to make responses engaging
- Keep responses concise but informative
- If asked about specific careers, mention salary ranges, requirements, and growth prospects in Kenya
- Always encourage taking the career assessment if they haven't

Respond in {'Kiswahili' if language == 'sw' else 'English'}."""

# API Routes
@app.get("/")
async def root():
    return {"message": "CBE Career Guide API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "gemini_configured": bool(gemini_api_key), "supabase_configured": bool(supabase_url)}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(chat_request: ChatMessage):
    """Handle chat requests with Gemini AI"""
    try:
        user_context = UserContext()
        session_id = None
        
        # Get user context if user_id is provided
        if chat_request.user_id:
            user_context = await get_user_context(chat_request.user_id)
            session_id = await get_or_create_session(chat_request.user_id)
            
            # Save user message to database
            supabase.table('chat_conversations').insert({
                'user_id': chat_request.user_id,
                'session_id': session_id,
                'message': chat_request.message,
                'language': chat_request.language
            }).execute()
        
        # Create system prompt
        system_prompt = create_system_prompt(user_context, chat_request.language)
        
        # Generate AI response
        full_prompt = f"{system_prompt}\n\nStudent Question: {chat_request.message}"
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_k=40,
                top_p=0.95,
                max_output_tokens=1024,
            )
        )
        
        ai_response = response.text
        
        # Update conversation in database
        if chat_request.user_id and session_id:
            # Update the conversation with AI response
            supabase.table('chat_conversations').update({
                'response': ai_response
            }).eq('user_id', chat_request.user_id).eq('session_id', session_id).eq('message', chat_request.message).order('timestamp', desc=True).limit(1).execute()
            
            # Update session
            supabase.table('chat_sessions').update({
                'last_message_at': 'now()',
                'total_messages': supabase.table('chat_sessions').select('total_messages').eq('id', session_id).single().execute().data['total_messages'] + 1
            }).eq('id', session_id).execute()
        
        return ChatResponse(response=ai_response, session_id=session_id)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        # Fallback response
        fallback_responses = {
            'en': "I'm here to help with your career journey! I can assist with CBE pathway guidance, career exploration, university requirements, and more. What would you like to know?",
            'sw': "Nipo hapa kukusaidia katika safari yako ya kazi! Ninaweza kusaidia na mwongozo wa njia za CBE, uchunguzi wa kazi, mahitaji ya chuo kikuu, na zaidi. Ungependa kujua nini?"
        }
        
        response_text = fallback_responses.get(chat_request.language, fallback_responses['en'])
        return ChatResponse(response=response_text, session_id=session_id)

@app.get("/chat/sessions/{user_id}")
async def get_user_sessions(user_id: str):
    """Get user's chat sessions"""
    try:
        response = supabase.table('chat_sessions').select('*').eq('user_id', user_id).order('last_message_at', desc=True).execute()
        return {"sessions": response.data}
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sessions")

@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    try:
        response = supabase.table('chat_conversations').select('*').eq('session_id', session_id).order('timestamp', desc=False).execute()
        return {"messages": response.data}
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"🚀 Starting CBE Career Guide Backend...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"🔧 Debug Mode: {debug}")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )