# CBE Career Guide - Full Stack Application

A comprehensive career guidance platform for Kenya's Competency Based Education (CBE) system, featuring AI-powered chat assistance using Google's Gemini API.

## 🌟 Features

### Frontend (HTML/CSS/JavaScript)
- 🎨 **Modern UI/UX** - Responsive design with Bootstrap 5
- 🌍 **Bilingual Support** - English and Kiswahili
- 🔐 **User Authentication** - Supabase Auth integration
- 📊 **Interactive Dashboard** - Progress tracking and analytics
- 🎯 **Career Assessment** - Personalized pathway recommendations
- 📚 **Resource Library** - Educational materials and guides
- 🎮 **Interactive Scenarios** - Gamified learning experiences

### Backend (Python FastAPI)
- 🤖 **Gemini AI Integration** - Secure server-side AI processing
- 🔒 **API Security** - Environment-based configuration
- 💾 **Database Operations** - Supabase integration
- 📝 **Session Management** - Organized conversation tracking
- 🌐 **RESTful API** - Clean endpoints for frontend communication

### Database (Supabase PostgreSQL)
- 👤 **User Management** - Profiles, authentication, preferences
- 💬 **Chat System** - Conversations, sessions, history
- 📈 **Analytics** - User activities, progress tracking
- 🏆 **Gamification** - Achievements, progress levels
- 🔐 **Security** - Row Level Security (RLS) policies

## 🚀 Quick Start

### Option 1: Automated Setup (Windows)
```bash
# Run the automated setup script
start_project.bat
```

### Option 2: Manual Setup

#### 1. Database Setup
1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Run the SQL script in Supabase SQL Editor:
   ```sql
   -- Copy and paste the entire content of updated_script.sql
   ```

#### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your actual credentials
python main.py
```

#### 3. Frontend Setup
- Open `index.html` in your browser
- Or use Live Server extension in VS Code
- Make sure backend is running on port 8000

## 📁 Project Structure

```
CBE-Career-Guide/
├── frontend/
│   ├── index.html              # Landing page
│   ├── chat.html              # AI Chat interface
│   ├── dashboard.html         # User dashboard
│   ├── assessment.html        # Career assessment
│   ├── login.html            # Authentication
│   ├── signup.html           # User registration
│   └── ...                   # Other pages
├── backend/
│   ├── main.py               # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── .env                 # Environment variables
│   └── README.md            # Backend documentation
├── updated_script.sql        # Database schema
├── start_project.bat        # Automated setup
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# Supabase Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Frontend Configuration
Update the API base URL in chat.html if needed:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## 🔑 API Keys Required

1. **Supabase Keys**:
   - Project URL: `https://your-project.supabase.co`
   - Anon Key: For frontend authentication
   - Service Role Key: For backend database operations

2. **Google Gemini API Key**:
   - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Used for AI chat functionality

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Key Endpoints
- `POST /chat` - Send message to AI
- `GET /chat/sessions/{user_id}` - Get user's chat sessions
- `GET /chat/history/{session_id}` - Get chat history

## 🎯 CBE Pathways Supported

1. **STEM Pathway** - Science, Technology, Engineering & Mathematics
2. **Social Sciences** - Humanities & Social Studies
3. **Arts & Sports** - Creative & Physical Education
4. **Technical Pathway** - Vocational & Technical Skills

## 🔒 Security Features

- Environment-based API key management
- Row Level Security (RLS) on all database tables
- CORS protection
- Input validation with Pydantic
- Secure authentication with Supabase Auth

## 🌍 Bilingual Support

The application supports:
- **English** - Default language
- **Kiswahili** - Kenyan national language

AI responses are contextually aware of the selected language.

## 🚀 Deployment

### Backend Deployment
```bash
# Production setup
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment
- Deploy static files to any web server
- Update API_BASE_URL to your backend domain
- Configure CORS in backend for your domain

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section in backend/README.md
2. Verify all environment variables are set correctly
3. Ensure Supabase database is properly configured
4. Check that all required services are running

## 🎉 Acknowledgments

- **Google Gemini AI** - For intelligent chat responses
- **Supabase** - For backend-as-a-service platform
- **FastAPI** - For the Python backend framework
- **Bootstrap** - For responsive UI components
- **Kenya Ministry of Education** - For CBE system guidance