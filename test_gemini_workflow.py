import asyncio
import os
import sys
sys.path.append(os.path.dirname(__file__))

from src.mas import Orchestrator, MultiAgent
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

async def test_gemini_workflow():
    """Test the complete Gemini workflow"""
    print("🧪 Testing Gemini Resume Screening Workflow")
    print("=" * 50)
    
    # Sample job profile
    job_profile = """
    Senior Python Developer
    Requirements:
    - 5+ years of Python experience
    - Django framework expertise
    - SQL database knowledge
    - AWS cloud experience preferred
    """
    
    # Sample resumes
    resumes = [
        {
            "filename": "candidate1.txt",
            "content": "John Doe - Python Developer with 6 years experience in Django, PostgreSQL, and AWS deployment"
        },
        {
            "filename": "candidate2.txt", 
            "content": "Jane Smith - Full-stack developer with 3 years Python, React experience, familiar with MySQL"
        }
    ]
    
    try:
        # Create screening context
        screening_context = {
            "job_profile": job_profile,
            "resumes": resumes,
            "num_resumes": len(resumes)
        }
        
        print("📋 Creating orchestrator...")
        orchestrator = Orchestrator(screening_context, num_agents=2)
        
        print("🤖 Generating dynamic agents...")
        dynamic_agents = orchestrator.run()
        
        print(f"✅ Created {len(dynamic_agents)} agents:")
        for agent in dynamic_agents:
            print(f"  - {agent['name']}: {agent['role']}")
        
        print("\n🔄 Setting up multi-agent system...")
        mas = MultiAgent()
        expert_agents = mas.create_agents(dynamic_agents)
        
        if mas.service_type == "gemini":
            print("✅ Using Gemini simplified chat group")
            
            # Create a simplified chat group for testing
            termination_keyword = 'complete'
            group = mas.create_chat_group(expert_agents, None, None, termination_keyword)
            
            # Test message
            test_message = f"""
            Please screen these candidates for the job:
            
            Job Profile: {job_profile}
            
            Candidates:
            1. {resumes[0]['filename']}: {resumes[0]['content']}
            2. {resumes[1]['filename']}: {resumes[1]['content']}
            
            Provide scores and recommendations for each candidate. End your response with 'COMPLETE' when done.
            """
            
            print("\n📨 Sending screening request...")
            await group.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=test_message))
            
            print("\n🎯 Processing responses...")
            response_count = 0
            async for response in group.invoke():
                response_count += 1
                print(f"\n--- Response {response_count} from {response.name} ---")
                print(response.content[:500] + "..." if len(response.content) > 500 else response.content)
                
                if response_count >= 2:  # Limit responses for testing
                    break
                    
            print(f"\n✅ Workflow completed successfully with {response_count} responses!")
            
        else:
            print("⚠️ Non-Gemini service detected - skipping simplified test")
            
    except Exception as e:
        print(f"❌ Error in workflow: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemini_workflow())
