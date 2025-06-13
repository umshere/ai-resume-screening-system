#!/usr/bin/env python3
"""
Comprehensive test suite for AI Resume Screening System
Tests all major components and AI service integrations
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.dirname(__file__))

def test_environment_setup():
    """Test that environment variables are properly loaded"""
    print("🔍 Testing environment setup...")
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        return False
    
    # Check AI_SERVICE is set
    ai_service = os.getenv("AI_SERVICE")
    if not ai_service:
        print("❌ AI_SERVICE not set in .env file")
        return False
    
    print(f"✅ AI_SERVICE set to: {ai_service}")
    
    # Check corresponding API key is set
    if ai_service.lower() == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your-gemini-api-key-here":
            print("❌ GEMINI_API_KEY not properly set")
            return False
        print("✅ Gemini API key configured")
        
    elif ai_service.lower() == "azure":
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not endpoint or not api_key:
            print("❌ Azure OpenAI credentials not properly set")
            return False
        print("✅ Azure OpenAI credentials configured")
        
    elif ai_service.lower() == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sk-your-openai-api-key-here":
            print("❌ OPENAI_API_KEY not properly set")
            return False
        print("✅ OpenAI API key configured")
    
    return True

def test_imports():
    """Test that all required modules can be imported"""
    print("\n📦 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Streamlit: {e}")
        return False
    
    try:
        from src.mas import get_ai_service_config, Orchestrator, MultiAgent
        print("✅ MAS components imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MAS components: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Google Generative AI: {e}")
        return False
    
    return True

def test_ai_service_config():
    """Test AI service configuration"""
    print("\n🤖 Testing AI service configuration...")
    
    try:
        from src.mas import get_ai_service_config
        
        service_type, client, model, model_orchestrator = get_ai_service_config()
        print(f"✅ AI service configured: {service_type}")
        print(f"✅ Model: {model}")
        print(f"✅ Orchestrator model: {model_orchestrator}")
        
        return True
    except Exception as e:
        print(f"❌ AI service configuration failed: {e}")
        return False

def test_orchestrator():
    """Test the Orchestrator component"""
    print("\n🧠 Testing Orchestrator...")
    
    try:
        from src.mas import Orchestrator
        
        # Create a simple test context
        screening_context = {
            "job_profile": "Software Engineer with Python experience",
            "num_resumes": 2
        }
        
        orchestrator = Orchestrator(screening_context, num_agents=3)
        print("✅ Orchestrator created successfully")
        
        # Test agent creation (this will make an API call)
        print("🔄 Testing dynamic agent creation...")
        dynamic_agents = orchestrator.run()
        
        if dynamic_agents and len(dynamic_agents) > 0:
            print(f"✅ Created {len(dynamic_agents)} dynamic agents")
            for agent in dynamic_agents:
                print(f"   - {agent.get('name', 'Unknown')} ({agent.get('role', 'No role')})")
        else:
            print("❌ No dynamic agents created")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        return False

def test_multi_agent():
    """Test the MultiAgent component"""
    print("\n👥 Testing MultiAgent system...")
    
    try:
        from src.mas import MultiAgent
        
        mas = MultiAgent()
        print("✅ MultiAgent system created successfully")
        
        # Create sample agents
        sample_agents = [
            {
                "name": "Skills Analyst",
                "role": "Technical Skills Evaluator", 
                "system_prompt": "You are a technical skills analyst."
            },
            {
                "name": "Experience Evaluator",
                "role": "Work Experience Assessor",
                "system_prompt": "You are an experience evaluation specialist."
            }
        ]
        
        expert_agents = mas.create_agents(sample_agents)
        print(f"✅ Created {len(expert_agents)} expert agents")
        
        # Test selection and termination functions
        selection_function = mas.create_selection_function(expert_agents)
        termination_function = mas.create_termination_function("completed")
        print("✅ Selection and termination functions created")
        
        # Test chat group creation
        group = mas.create_chat_group(
            expert_agents, 
            selection_function, 
            termination_function, 
            "completed"
        )
        print("✅ Chat group created successfully")
        
        return True
    except Exception as e:
        print(f"❌ MultiAgent test failed: {e}")
        return False

async def test_end_to_end():
    """Test complete end-to-end workflow"""
    print("\n🔄 Testing end-to-end workflow...")
    
    try:
        from src.mas import Orchestrator, MultiAgent
        from semantic_kernel.contents.chat_message_content import ChatMessageContent
        from semantic_kernel.contents.utils.author_role import AuthorRole
        
        # Step 1: Create screening context
        screening_context = {
            "job_profile": "Senior Python Developer with 3+ years experience in web development and API design",
            "resumes": [
                {
                    "filename": "test_resume_1.txt",
                    "content": "John Doe, Software Engineer with 4 years Python experience, Django, Flask, REST APIs"
                }
            ],
            "num_resumes": 1
        }
        
        print("📝 Created test screening context")
        
        # Step 2: Create orchestrator and generate agents
        orchestrator = Orchestrator(screening_context, num_agents=2)
        dynamic_agents = orchestrator.run()
        print(f"🤖 Generated {len(dynamic_agents)} dynamic agents")
        
        # Step 3: Create multi-agent system
        mas = MultiAgent()
        expert_agents = mas.create_agents(dynamic_agents)
        print(f"👥 Created {len(expert_agents)} expert agents")
        
        # Step 4: Create chat group
        selection_function = mas.create_selection_function(expert_agents)
        termination_function = mas.create_termination_function("analysis complete")
        
        group = mas.create_chat_group(
            expert_agents,
            selection_function, 
            termination_function,
            "analysis complete"
        )
        print("💬 Created chat group")
        
        # Step 5: Test message processing
        test_message = f"""
        Please analyze the following resume against the job profile:
        
        Job Profile: {screening_context['job_profile']}
        
        Resume: {screening_context['resumes'][0]['content']}
        
        Provide a brief matching analysis. End your response with 'analysis complete'.
        """
        
        await group.add_chat_message(
            ChatMessageContent(role=AuthorRole.USER, content=test_message)
        )
        print("📤 Added test message to chat group")
        
        # Step 6: Process responses (limit to avoid long processing)
        response_count = 0
        async for response in group.invoke_stream():
            response_count += 1
            print(f"📥 Received response from {response.name}: {response.content[:100]}...")
            
            # Limit responses for testing
            if response_count >= 2 or group.is_complete:
                break
        
        print(f"✅ End-to-end test completed with {response_count} responses")
        return True
        
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 AI Resume Screening System - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Module Imports", test_imports),
        ("AI Service Config", test_ai_service_config),
        ("Orchestrator", test_orchestrator),
        ("MultiAgent System", test_multi_agent),
    ]
    
    passed = 0
    total = len(tests)
    
    # Run synchronous tests
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ {test_name} test failed")
        except Exception as e:
            print(f"\n❌ {test_name} test error: {e}")
    
    # Run async end-to-end test
    try:
        if await test_end_to_end():
            passed += 1
            total += 1
        else:
            print(f"\n❌ End-to-end test failed")
            total += 1
    except Exception as e:
        print(f"\n❌ End-to-end test error: {e}")
        total += 1
    
    # Final results
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready to use.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run app.py")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("\n💡 Common fixes:")
        print("   - Verify your .env file configuration")
        print("   - Check your API keys are valid")
        print("   - Ensure all dependencies are installed")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())
