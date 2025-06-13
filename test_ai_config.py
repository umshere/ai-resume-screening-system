#!/usr/bin/env python3
"""
Test script to verify AI service configuration
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_ai_service():
    """Test the AI service configuration"""
    try:
        from mas import get_ai_service_config
        
        print("🔍 Testing AI service configuration...")
        print(f"AI_SERVICE setting: {os.getenv('AI_SERVICE', 'Not set')}")
        print("-" * 50)
        
        # Get the AI service configuration
        service_type, client, model, model_orchestrator = get_ai_service_config()
        
        print(f"✅ Successfully configured {service_type.upper()} service")
        print(f"Model: {model}")
        print(f"Orchestrator Model: {model_orchestrator}")
        
        # Test a simple request
        print("\n🚀 Testing simple API call...")
        
        response = client.chat.completions.create(
            model=model_orchestrator,
            messages=[
                {"role": "user", "content": "Say 'Hello from AI service test!' in exactly those words."}
            ],
            max_completion_tokens=50
        )
        
        # Parse response based on service type
        if service_type == "gemini":
            response_text = response.choices[0].message.content
        else:
            response_text = response.choices[0].message.content
        
        print(f"✅ API Response: {response_text}")
        print("\n🎉 AI service test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ AI service test failed: {str(e)}")
        print("\n💡 Please check your .env file and ensure:")
        print("1. AI_SERVICE is set to 'azure', 'openai', or 'gemini'")
        print("2. The corresponding API credentials are properly configured")
        print("3. The API key is valid and has sufficient quota")
        return False

if __name__ == "__main__":
    success = test_ai_service()
    sys.exit(0 if success else 1)
