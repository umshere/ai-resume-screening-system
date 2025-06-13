import asyncio
import streamlit as st
import pandas as pd
import io
import PyPDF2
import docx
from typing import List, Dict
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from src.mas import Orchestrator, MultiAgent

st.set_page_config(
    page_title="AI Resume Screening & Matching System",
    page_icon="📋",
    layout="wide"
)

# Function to check if API key is provided
def check_api_configuration():
    """Check if API is configured via environment or user input"""
    # Check if API key is set in environment (for personal/demo deployments)
    env_api_key = os.getenv('GEMINI_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')
    
    if env_api_key and env_api_key != "your-gemini-api-key-here":
        return True, "environment"
    
    # Check if user has provided API key in session
    if st.session_state.get('user_api_key'):
        return True, "user_provided"
    
    return False, None

def show_api_key_input():
    """Show API key input form for users"""
    st.warning("🔑 **API Key Required** - Choose your AI service and provide your API key")
    
    # API Service Selection
    api_service = st.selectbox(
        "Select AI Service:",
        ["gemini", "azure", "openai"],
        help="Choose your preferred AI service"
    )
    
    # API Key Input
    if api_service == "gemini":
        st.info("🌟 **Recommended**: Gemini offers the best value for money")
        st.markdown("Get your free API key at: [Google AI Studio](https://aistudio.google.com/app/apikey)")
        
        api_key = st.text_input(
            "Gemini API Key:",
            type="password",
            placeholder="Enter your Gemini API key",
            help="Your API key is used only for this session and is not stored"
        )
        
        if api_key:
            # Temporarily set environment variables for this session
            os.environ['AI_SERVICE'] = 'gemini'
            os.environ['GEMINI_API_KEY'] = api_key
            st.session_state.user_api_key = api_key
            st.session_state.ai_service = 'gemini'
            st.success("✅ Gemini API key configured!")
            st.rerun()
    
    elif api_service == "azure":
        st.info("🏢 **Enterprise Choice**: Azure OpenAI for business use")
        
        col1, col2 = st.columns(2)
        with col1:
            endpoint = st.text_input(
                "Azure Endpoint:",
                placeholder="https://your-resource.openai.azure.com/"
            )
        with col2:
            api_key = st.text_input(
                "Azure API Key:",
                type="password",
                placeholder="Enter your Azure OpenAI API key"
            )
        
        if endpoint and api_key:
            os.environ['AI_SERVICE'] = 'azure'
            os.environ['AZURE_OPENAI_ENDPOINT'] = endpoint
            os.environ['AZURE_OPENAI_API_KEY'] = api_key
            st.session_state.user_api_key = api_key
            st.session_state.ai_service = 'azure'
            st.success("✅ Azure OpenAI configured!")
            st.rerun()
    
    elif api_service == "openai":
        st.info("🚀 **Direct Access**: OpenAI for latest models")
        st.markdown("Get your API key at: [OpenAI Platform](https://platform.openai.com/api-keys)")
        
        api_key = st.text_input(
            "OpenAI API Key:",
            type="password",
            placeholder="sk-..."
        )
        
        if api_key:
            os.environ['AI_SERVICE'] = 'openai'
            os.environ['OPENAI_API_KEY'] = api_key
            st.session_state.user_api_key = api_key
            st.session_state.ai_service = 'openai'
            st.success("✅ OpenAI API key configured!")
            st.rerun()

# Enhanced CSS for resume screening interface
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    
    .api-info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 20px 0;
    }
    
    .cost-info {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    /* ...existing styles... */
    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(-45deg, #667eea, #764ba2, #6b73ff, #9a9ce1);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        margin: 0;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("🤖 AI Resume Screening & Matching System")
    st.markdown("### Intelligent Resume Analysis with Multi-Agent AI")
    
    # Check API configuration
    is_configured, config_type = check_api_configuration()
    
    if not is_configured:
        # Show API key input if not configured
        st.markdown(
            """
            <div class="api-info-box">
                <h3>🔑 API Configuration Required</h3>
                <p>This application uses AI services to analyze resumes. You need to provide your own API key.</p>
                <p><strong>Why?</strong> This ensures you have full control over costs and usage.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Cost information
        st.markdown(
            """
            <div class="cost-info">
                <h4>💰 Estimated Costs</h4>
                <ul>
                    <li><strong>Gemini (Recommended):</strong> ~$0.01-0.05 per resume analysis</li>
                    <li><strong>OpenAI:</strong> ~$0.05-0.15 per resume analysis</li>
                    <li><strong>Azure OpenAI:</strong> ~$0.05-0.15 per resume analysis</li>
                </ul>
                <p><em>Analyzing 100 resumes typically costs $1-15 depending on the service.</em></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        show_api_key_input()
        return
    
    # Show current configuration
    if config_type == "environment":
        st.success("✅ API configured via environment variables")
    else:
        service = st.session_state.get('ai_service', 'Unknown')
        st.success(f"✅ API configured: {service.upper()} service")
        
        # Option to change API key
        if st.button("🔄 Change API Configuration"):
            st.session_state.user_api_key = None
            st.session_state.ai_service = None
            st.rerun()
    
    # Initialize session state
    if 'resumes' not in st.session_state:
        st.session_state.resumes = []
    if 'job_profile' not in st.session_state:
        st.session_state.job_profile = ""
    if 'num_agents' not in st.session_state:
        st.session_state.num_agents = 4
    if 'analysis_depth' not in st.session_state:
        st.session_state.analysis_depth = "Standard Analysis"

    # Rest of your existing app code...
    # [Include all the existing tab-based interface code here]

if __name__ == "__main__":
    main()
