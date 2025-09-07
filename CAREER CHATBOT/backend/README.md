# CBE Career Guide Backend

A Python FastAPI backend for the CBE Career Guide application with Gemini AI integration.

## Features

- 🤖 **Gemini AI Integration** - Secure server-side AI chat processing
- 🔐 **Supabase Integration** - Database operations and authentication
- 🌐 **RESTful API** - Clean API endpoints for frontend communication
- 🔒 **Secure Configuration** - Environment-based API key management
- 📝 **Chat Management** - Session-based conversation tracking
- 🌍 **Bilingual Support** - English and Kiswahili responses

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` - Your Supabase service role key
- `GEMINI_API_KEY` - Your Google Gemini API key

### 3. Run the Server

```bash
# Development mode (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Verify Installation

Visit `http://localhost:8000/docs` to see the interactive API documentation.

## API Endpoints

### Health Check
- `GET /` - Basic API status
- `GET /health` - Detailed health check with service status

### Chat Endpoints
- `POST /chat` - Send message to AI and get response
- `GET /chat/sessions/{user_id}` - Get user's chat sessions
- `GET /chat/history/{session_id}` - Get chat history for a session

## API Usage Examples

### Send Chat Message

```javascript
const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: "What are the CBE pathways?",
        user_id: "user-uuid-here",
        language: "en"
    })
});

const data = await response.json();
console.log(data.response);
```

### Get Chat Sessions

```javascript
const response = await fetch(`http://localhost:8000/chat/sessions/${userId}`);
const data = await response.json();
console.log(data.sessions);
```

## Security Features

- Environment-based configuration
- Server-side API key management
- Supabase authentication integration
- CORS protection
- Input validation with Pydantic

## Development

### Project Structure
```
backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (not in git)
├── .env.example        # Environment template
└── README.md           # This file
```

### Adding New Features

1. Add new Pydantic models for request/response validation
2. Create new route handlers in `main.py`
3. Update database operations as needed
4. Test endpoints using the interactive docs at `/docs`

## Deployment

For production deployment:

1. Set `DEBUG=False` in environment
2. Use a production WSGI server like Gunicorn
3. Configure proper CORS origins
4. Set up SSL/HTTPS
5. Use environment-specific configuration

```bash
# Production example
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Verify environment variables are set correctly
3. **CORS Errors**: Check `ALLOWED_ORIGINS` in `.env`
4. **Database Errors**: Verify Supabase credentials and table structure

### Logs

The application logs important events and errors. Check console output for debugging information.