# CBE Career Guide

Career guidance platform for Kenya's Competency Based Education system.

## Quick Start

### 1. Run Database Script

Execute in your Supabase SQL editor.

### 2. Start Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

You should see:

```
Starting CBE Career Guide API...
API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs
```

### 3. Test the API

Open `chat.html` in your browser to test the chat functionality.

### 4. Use in Your Frontend

Replace your chat functionality with calls to the backend API:

```javascript
// Example chat request
fetch("http://127.0.0.1:8000/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    message: "What careers are in STEM?",
    language: "en",
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data.response));
```

## API Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `POST /chat` - Send chat message
- `GET /pathways` - Get CBE pathways info
- `GET /docs` - API documentation

That's it! The backend handles all AI chat functionality.
