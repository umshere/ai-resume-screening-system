import os
import sys
from dotenv import load_dotenv

try:
    # Print current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if .env file exists
    env_path = os.path.join(os.getcwd(), '.env')
    print(f"Checking for .env file at: {env_path}")
    print(f"File exists: {os.path.exists(env_path)}")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Print the environment variables to check if they're loaded correctly
    print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    print(f"AZURE_OPENAI_API_KEY: {os.getenv('AZURE_OPENAI_API_KEY')[:10]}... (truncated)")
    print(f"AZURE_OPENAI_MODEL: {os.getenv('AZURE_OPENAI_MODEL')}")
    print(f"AZURE_OPENAI_MODEL_ORCHESTRATOR: {os.getenv('AZURE_OPENAI_MODEL_ORCHESTRATOR')}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
