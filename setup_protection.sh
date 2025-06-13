#!/bin/bash

# Usage Protection Setup Script
# Run this script to configure usage protection for deployment

echo "🛡️  AI Resume Screening - Usage Protection Setup"
echo "================================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from protected template..."
    cp .env.protected .env
    echo "✅ .env file created with usage protection settings"
else
    echo "✅ .env file already exists"
fi

# Create logs directory for usage tracking
mkdir -p logs
echo "📁 Created logs directory for usage tracking"

# Set appropriate permissions
chmod 644 .env
chmod 755 logs
echo "🔒 Set appropriate file permissions"

# Display current protection settings
echo ""
echo "🔍 Current Protection Settings:"
echo "--------------------------------"

if [ -f .env ]; then
    echo "Daily cost limit: $(grep MAX_DAILY_COST .env | cut -d'=' -f2 | tr -d '"')"
    echo "Session limit: $(grep MAX_RESUMES_PER_SESSION .env | cut -d'=' -f2 | tr -d '"')"
    echo "AI Service: $(grep AI_SERVICE .env | cut -d'=' -f2 | tr -d '"')"
    echo "Emergency shutdown: $(grep EMERGENCY_SHUTDOWN .env | cut -d'=' -f2 | tr -d '"')"
fi

echo ""
echo "💡 Configuration Tips:"
echo "----------------------"
echo "1. Edit .env file to set your API keys"
echo "2. Adjust MAX_DAILY_COST for your budget"
echo "3. Set EMERGENCY_SHUTDOWN=true to disable the app quickly"
echo "4. Monitor usage in the logs/ directory"

echo ""
echo "🚀 Ready for deployment with usage protection!"
echo ""
echo "Next steps:"
echo "1. Configure your API keys in .env"
echo "2. Test locally: streamlit run app.py"
echo "3. Deploy using ./deploy.sh"

# Test configuration
echo ""
echo "🧪 Testing configuration..."
python3 -c "
from src.usage_protection import UsageTracker
tracker = UsageTracker()
print(f'✅ Usage tracker initialized')
print(f'   Daily limit: \${tracker.max_daily_cost}')
print(f'   Session limit: {tracker.max_resumes_per_session}')
print(f'   Cost per resume: \${tracker.cost_per_resume}')
" 2>/dev/null || echo "⚠️  Could not test configuration - ensure dependencies are installed"

echo ""
echo "✅ Usage protection setup complete!"
