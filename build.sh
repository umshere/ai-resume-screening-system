#!/bin/bash

# Build script for cloud deployment platforms like Railway, Render, etc.

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
mkdir -p .streamlit

# Verify environment
python test_ai_config.py || echo "Warning: AI configuration test failed - please check your environment variables"

echo "Build completed successfully!"
