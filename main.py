"""
AI Multi-Agent Resume Screening & Matching System
Main entry point - run the Streamlit application
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    # Run the Streamlit app
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())

    # Create the termination function
    termination_keyword = 'yes'
    termination_function = mas.create_termination_function(termination_keyword)

    # Create the chat group
    group = mas.create_chat_group(expert_agents, 
                                  selection_function, 
                                  termination_function, 
                                  termination_keyword)
    
    return group

async def main():   
    
    is_complete: bool = False
    while not is_complete:
        user_input = input("User:> ")
        if not user_input:
            continue

        if user_input.lower() == "exit":
            is_complete = True
            break
        
        # Run the orchestrator and get the chat group
        group = await run(user_input)
    
        if user_input.lower() == "reset":
            await group.reset()
            print("[Conversation has been reset]")
            continue

        if user_input.startswith("@") and len(input) > 1:
            file_path = input[1:]
            try:
                if not os.path.exists(file_path):
                    print(f"Unable to access file: {file_path}")
                    continue
                with open(file_path) as file:
                    user_input = file.read()
            except Exception:
                print(f"Unable to access file: {file_path}")
                continue

        await group.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=user_input))

        async for response in group.invoke():
            print(f"'***** {response.role} - {response.name or '*'} ***** '" )
            print('*****************************')
            print('\n')
            print('\n')
            
            print(f"'{response.content}'")
            print('----------------------------------')
            print('\n')
            print('\n')

        if group.is_complete:
            is_complete = True
            break

if __name__ == "__main__":
    asyncio.run(main())