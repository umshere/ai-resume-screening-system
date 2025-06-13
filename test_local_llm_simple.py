#!/usr/bin/env python3
"""
Simple test for Local LLM integration
"""

import os
import requests
import json

def test_local_llm_simple():
    """Simple test of Local LLM without complex imports"""
    print("🔍 Testing Local LLM with simple request...")
    
    base_url = "http://localhost:1234/v1"
    model = "gemma-3-4b-it-qat"
    
    # Test payload matching your curl command format
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Always answer in rhymes. Today is Thursday"},
            {"role": "user", "content": "What day is it today?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100,
        "stream": False
    }
    
    try:
        print(f"Making request to: {base_url}/chat/completions")
        print(f"Using model: {model}")
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            response_data = response.json()
            print("✅ Request successful!")
            print(f"Response: {json.dumps(response_data, indent=2)}")
            
            # Extract the actual response text
            if 'choices' in response_data and len(response_data['choices']) > 0:
                message_content = response_data['choices'][0]['message']['content']
                print(f"\n🎉 AI Response: {message_content}")
                return True
            else:
                print("❌ No response content found")
                return False
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to local LLM server")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_local_llm_simple()
    if success:
        print("\n✅ Local LLM is working correctly!")
        print("Your server can handle the resume screening workload.")
    else:
        print("\n❌ Local LLM test failed")
