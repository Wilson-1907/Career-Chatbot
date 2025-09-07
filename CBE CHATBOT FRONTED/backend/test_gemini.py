#!/usr/bin/env python3
"""
Simple test to verify Gemini API is working
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini():
    print("🧪 Testing Gemini AI API...")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        print("💡 Make sure your .env file has GEMINI_API_KEY=your-key-here")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-10:]}")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        print("🤖 Testing Gemini API call...")
        
        # Test prompt
        test_prompt = "What are the main pathways in Kenya's CBE system? Give a brief answer."
        
        response = model.generate_content(
            test_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_k=40,
                top_p=0.95,
                max_output_tokens=200,
            )
        )
        
        print("✅ Gemini API call successful!")
        print("🤖 Response:")
        print("-" * 30)
        print(response.text)
        print("-" * 30)
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        print("💡 Check your API key and internet connection")
        return False

if __name__ == "__main__":
    success = test_gemini()
    if success:
        print("\n🎉 Gemini API is working correctly!")
    else:
        print("\n💥 Gemini API test failed!")