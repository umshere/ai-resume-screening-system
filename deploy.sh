#!/bin/bash

# Quick deployment script for AI Resume Screening System
# This script helps you deploy to various platforms quickly

set -e

echo "🚀 AI Resume Screening System - Quick Deploy"
echo "============================================="

# Setup usage protection first
echo "🛡️  Setting up usage protection..."
if [ -x "./setup_protection.sh" ]; then
    ./setup_protection.sh
else
    echo "⚠️  Protection setup script not found - using basic setup"
fi

echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Creating .env from template..."
    cp .env.production .env
    echo "✅ Please edit .env file with your API keys before deploying"
    echo "💡 For Gemini API key, visit: https://aistudio.google.com/app/apikey"
    exit 1
fi

# Test configuration
echo "🔍 Testing AI configuration..."
python3 test_ai_config.py

if [ $? -ne 0 ]; then
    echo "❌ Configuration test failed. Please check your .env file."
    exit 1
fi

echo "✅ Configuration test passed!"

# Show deployment options
echo ""
echo "🎯 Choose your deployment option:"
echo "1. Streamlit Community Cloud (Free)"
echo "2. Docker (Local test)"
echo "3. Railway (Cloud)"
echo "4. Render (Cloud)"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "📚 Streamlit Community Cloud Deployment:"
        echo "1. Push your code to GitHub"
        echo "2. Visit https://share.streamlit.io"
        echo "3. Connect your repository"
        echo "4. Set app.py as main file"
        echo "5. Add secrets (AI_SERVICE and your API key)"
        echo ""
        echo "🔗 Your app will be live at: https://your-app-name.streamlit.app"
        ;;
    2)
        echo "🐳 Building Docker image..."
        docker build -t ai-resume-screening .
        echo "🚀 Starting local container..."
        echo "💡 Your app will be available at: http://localhost:8501"
        docker run -p 8501:8501 --env-file .env ai-resume-screening
        ;;
    3)
        echo "🚂 Railway Deployment:"
        echo "1. Visit https://railway.app"
        echo "2. Connect your GitHub repository"
        echo "3. Add environment variables:"
        echo "   - AI_SERVICE=gemini"
        echo "   - GEMINI_API_KEY=your-key"
        echo "4. Deploy automatically on push"
        ;;
    4)
        echo "🎨 Render Deployment:"
        echo "1. Visit https://render.com"
        echo "2. Create new Web Service"
        echo "3. Connect GitHub repository"
        echo "4. Build Command: pip install -r requirements.txt"
        echo "5. Start Command: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0"
        echo "6. Add environment variables in dashboard"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment instructions provided!"
echo "📖 For detailed instructions, see DEPLOYMENT.md"
