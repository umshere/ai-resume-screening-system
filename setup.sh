#!/bin/bash

# =============================================================================
# AI Resume Screening System - Quick Setup Script
# =============================================================================

echo "🚀 AI Resume Screening System - Quick Setup"
echo "============================================="
echo

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to backup and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mv .env .env.backup.$(date +%Y%m%d_%H%M%S)
        echo "✅ Backed up existing .env file"
    else
        echo "ℹ️  Keeping existing .env file. You can manually edit it or run this script later."
        exit 0
    fi
fi

# Copy example file
cp .env.example .env
echo "✅ Created .env file from template"

echo
echo "🤖 Choose your AI service:"
echo "1. Google Gemini (Recommended - cost effective)"
echo "2. Local LLM (Zero cost - requires local server)"
echo "3. Azure OpenAI (Enterprise grade)"
echo "4. OpenAI Direct (Latest models)"
echo

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🌟 Setting up Google Gemini..."
        sed -i.bak 's/AI_SERVICE=.*/AI_SERVICE=gemini/' .env
        echo
        echo "📝 Next steps:"
        echo "1. Get your free API key: https://aistudio.google.com/app/apikey"
        echo "2. Edit .env file and add: GEMINI_API_KEY=your-actual-key"
        ;;
    2)
        echo "🏠 Setting up Local LLM..."
        sed -i.bak 's/AI_SERVICE=.*/AI_SERVICE=local/' .env
        echo
        echo "📝 Next steps:"
        echo "1. Make sure your LLM server is running on http://localhost:1234"
        echo "2. Edit .env file and set LOCAL_LLM_MODEL to your model name"
        echo "3. Test with: python test_local_llm.py"
        ;;
    3)
        echo "🔷 Setting up Azure OpenAI..."
        sed -i.bak 's/AI_SERVICE=.*/AI_SERVICE=azure/' .env
        echo
        echo "📝 Next steps:"
        echo "1. Create Azure OpenAI resource in Azure Portal"
        echo "2. Edit .env file with your endpoint and API key"
        ;;
    4)
        echo "🔸 Setting up OpenAI Direct..."
        sed -i.bak 's/AI_SERVICE=.*/AI_SERVICE=openai/' .env
        echo
        echo "📝 Next steps:"
        echo "1. Get API key from: https://platform.openai.com/api-keys"
        echo "2. Edit .env file and add: OPENAI_API_KEY=your-key"
        ;;
    *)
        echo "❌ Invalid choice. Please edit .env file manually."
        ;;
esac

# Remove backup file
rm -f .env.bak

echo
echo "✅ Setup complete!"
echo
echo "🚀 Next steps:"
echo "1. Edit .env file with your API credentials"
echo "2. Test configuration: python test_ai_config.py"
echo "3. Start the application: streamlit run app.py"
echo
echo "📚 Documentation:"
echo "- README.md - Complete setup guide"
echo "- LOCAL_LLM_GUIDE.md - Local LLM setup (if chosen)"
echo "- .env.example - All configuration options"
