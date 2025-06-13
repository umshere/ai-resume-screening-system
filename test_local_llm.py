#!/usr/bin/env python3
"""
Test script to verify Local LLM integration
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_local_llm():
    """Test the Local LLM service configuration"""
    print("🔍 Testing Local LLM configuration...")
    print(f"AI_SERVICE setting: {os.getenv('AI_SERVICE', 'Not set')}")
    print("-" * 50)
    
    try:
        from mas import get_ai_service_config
        
        # Set environment variable for testing
        os.environ['AI_SERVICE'] = 'local'
        
        # Get the AI service configuration
        service_type, client, model, model_orchestrator = get_ai_service_config()
        
        print(f"✅ Successfully configured {service_type.upper()} service")
        print(f"Model: {model}")
        print(f"Orchestrator Model: {model_orchestrator}")
        print(f"Base URL: {os.getenv('LOCAL_LLM_BASE_URL', 'http://localhost:1234/v1')}")
        
        # Test a simple request
        print("\n🚀 Testing simple API call...")
        
        response = client.chat.completions.create(
            model=model_orchestrator,
            messages=[
                {"role": "user", "content": "Hello! Please respond with 'Local LLM is working correctly!' and nothing else."}
            ],
            max_completion_tokens=50,
            temperature=0.1
        )
        
        # Parse response
        response_text = response.choices[0].message.content
        print(f"✅ API Response: {response_text}")
        
        # Test JSON parsing capability
        print("\n🧪 Testing JSON response capability...")
        json_test_response = client.chat.completions.create(
            model=model_orchestrator,
            messages=[
                {"role": "user", "content": "Please respond with a valid JSON object containing: {\"status\": \"success\", \"message\": \"JSON test passed\"}"}
            ],
            max_completion_tokens=100,
            temperature=0.1
        )
        
        json_response_text = json_test_response.choices[0].message.content
        print(f"✅ JSON Response: {json_response_text}")
        
        print("\n🎉 Local LLM integration test completed successfully!")
        print("\n💡 To use Local LLM in your application:")
        print("1. Make sure your LLM server is running on http://localhost:1234")
        print("2. Set AI_SERVICE=local in your .env file")
        print("3. Configure LOCAL_LLM_MODEL with your model name")
        
        return True
        
    except Exception as e:
        print(f"❌ Local LLM test failed: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure your Local LLM server is running on http://localhost:1234")
        print("2. Check if the model name matches what's available in your server")
        print("3. Verify the server is accepting connections")
        print("4. Try running: curl http://localhost:1234/v1/models")
        return False

if __name__ == "__main__":
    success = test_local_llm()
    sys.exit(0 if success else 1)
