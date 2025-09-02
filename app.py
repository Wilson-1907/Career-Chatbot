from flask import Flask, request, jsonify, Response
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Configure Gemini with API key
genai.configure(api_key=os.environ.get("AIzaSyDDyRSRBIEC-OZYoiw9dNPwdWd9p8PMBLw
"))
model = genai.GenerativeModel("gemini-pro")

# System instruction to restrict topics
SYSTEM_PROMPT = """
You are an assistant that ONLY answers questions related to EDUCATION and CAREERS.
- If the question is about school, courses, universities, job opportunities, skills, salaries, career guidance, etc., give a clear and helpful answer.
- If the question is NOT related to education or career, politely say: 
  "I’m here to help with education and career guidance only."
"""

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    def generate():
        try:
            stream = model.generate_content_stream(f"{SYSTEM_PROMPT}\nUser: {user_message}\nAssistant:")
            for chunk in stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error: {str(e)}"

    return Response(generate(), mimetype='text/plain')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)

