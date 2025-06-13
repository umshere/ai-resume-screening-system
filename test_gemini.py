import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test the Gemini API key"""
    # Configure the API key
    gemini_api_key = "your-gemini-api-key-here"
    genai.configure(api_key=gemini_api_key)
    
    try:
        # List available models
        print("Available Gemini models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"- {model.name} (display name: {model.display_name})")
        
        # Test with a simple prompt
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello! This is a test. Please respond with 'Gemini API is working correctly!'")
        
        print(f"\nTest response: {response.text}")
        return True
        
    except Exception as e:
        print(f"Gemini API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_api()
